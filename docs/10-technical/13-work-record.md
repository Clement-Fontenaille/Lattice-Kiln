# Work Record (v0)

**Traces to:** `00-design/28-arch-work-record/01-work-record.md`,
`00-design/22-arch-cognition/01-work-intent-and-task-model.md`,
`00-design/24-arch-permission-layer/01-capabilities-and-authority.md`,
`00-design/40-roadmap/01-MILESTONES/completed/04-ephemeral-processors.md` (M4),
`00-design/40-roadmap/01-MILESTONES/completed/05-intelligent-orchestration.md` (M5);
binds to `10-technical/01-effect-vocabulary.md` (effect type 4),
`10-technical/03-capability-authority-model.md`,
`10-technical/02-observability-event-model.md`,
`10-technical/08-orchestrator-contract.md`.

## TL;DR

The durable store for intent and the work derived from it. It holds **three kinds
of record**: intent, written from outside and never rewritten by the system; work
items, whose current formulation is directly readable; and an append-only
transition log for each item. It decides nothing about the work — it persists what
a realized effect changed.

> **Motto:** The goal outlives every formulation of it.

## Status of this document

v0, written against a store that already exists in practice. Work-record mutation
(effect type 4) has a schema, a capability policy, and exercised M3 runs behind
it; what had no specification was the record those effects mutate.

Two things here are specified ahead of any run. The **declared scope** fields
exist because `03-capability-authority-model.md` needs somewhere to read a mandate
from, and nothing derives one yet. The **containment checks** on split and refine
are stated normatively and enforced nowhere.

## Responsibility

Hold intent, work items, their declared scopes, their transitions, their
attachment edges, and their recorded conclusions — durably, and readably enough
that an ephemeral processor can cooperate on work it did not start.

It does **not** decide anything about the work. Whether an item should be split is
the orchestrator's call; whether a formulation is well-formed is nobody's job
here; whether a recorded conclusion is correct is not judged. This store records
what something else decided and the runtime realized.

## Narrowing

`28-arch-work-record/01` states a responsibility, a service surface, and a general
shape, deliberately stopping short of a schema. This document narrows to:

- **Three record kinds**, not one: intent, work item, transition. They are three
  because they are written under three different disciplines. Intent is written
  once and never again. A work item is rewritten in place every time it changes. A
  transition is appended and never touched afterwards.
- **This store is separate from `12-knowledge-model.md`**, and the reason is what a
  work item *is* rather than what it costs to read. A work item is not a claim; it
  is what claims attach to. The knowledge model is also append-and-supersede
  throughout, which is the wrong discipline for a record whose whole purpose is to
  be rewritten as the work changes.
- **Scope as three fields on the work item** — boundary, derivation, state — not
  one opaque string and not a structured predicate.
- **An append-only transition log kept alongside an item rather than inside it.**
- **Work units are not given a record kind.** `22-arch-cognition/01` leaves open
  whether they need first-class persistence; this document holds two kinds of
  work record rather than three until that is answered, which is the cheaper
  assumption to reverse.

## Inputs

- **Realized type-4 effects**, from the runtime. This store is written by nothing
  else (below).
- **Intent**, written from outside the system, out of band.
- **Derived or narrowed scopes**, from an invariant processor (the ceiling) or the
  orchestrator (a narrowing), each arriving as a type-4 mutation like any other.

## The three record kinds

Fields marked *(illustrative)* name intent, not a fixed shape.

### 1. Intent

The simplest of the three, and the only one the system may not write.

MUST carry: `intent_id`, the **original human-authored content verbatim**, and
when it entered.

- The original content MUST NOT be modified by any in-system actor.
  `01-effect-vocabulary.md` type 4 excludes it by name, and the reason is heavier
  than records hygiene: mandate descends from intent, so a system able to write
  its own intent could write its own mandate, which is what
  `10-foundations/06`'s membership test disqualifies. Work may be rewritten
  freely; what the work is *for* may not.
- Intent needs **no transition log**. It is written once and read thereafter.
- Amendment is direct human action, out of band, and produces a new version
  rather than editing in place — so that work items already descending from the
  old one remain interpretable.

### 2. Work item

One record per item, holding current state as **directly readable fields**.

MUST carry:

- `work_item_id`, `intent_ref`, `parent_item_id` (null for a root).
- `formulation` — the current statement of what may need to be done, in natural
  language.
- `state` — one of the transitions below, as a current value: refined, challenged,
  split, merged, deferred, abandoned, executed.
- `scope` — three parts, specified in the next section.
- `conclusion` — null until recorded; see below.
- `attachments` — references into `12-knowledge-model.md`, plus this store's own
  metadata about each edge. The claim's **content** lives there and MUST NOT be
  copied here. Two stores point into one claim store; neither owns it. See
  Attachment edges below for what an edge may say.

An item's current state is what the item record says. A reader MUST get it in one
fetch, without reconstructing it from the transition log.

The orchestrator performs this read on every loop step, for every item it has in
view, which makes it the most frequent read in the system. A store that rebuilt
state by folding the log would make that read cost grow with the item's history,
so it would get slower exactly as the loop ran longer.

### 3. Transition

One append-only log per work item, kept **alongside** the item.

MUST carry: `work_item_id`, `transition` (refined / challenged / split / merged /
deferred / abandoned / executed), the effect that realized it, the invocation that
proposed it, and a timestamp.

- The log is **append-only**. A transition is never edited or removed.
- The log holds what the item record does not keep: every superseded formulation,
  who proposed each change, which effect realized it, and when. The item record
  keeps only where the work stands now.

**One write path keeps the two in step.** A work item changes only when the runtime
realizes a type-4 effect, and that one call writes both — the log entry first, then
the item record. Nothing else writes either, so there is no route by which a change
reaches one and not the other, except a crash between the two writes.

**The log says whether it was applied.** Rather than inferring from the write order
what a crash left behind, each transition carries its **application state**:

- `logged` — the entry is durable; the item record does not yet reflect it.
- `applied` — the item record reflects it.

Recovery then reads rather than infers. Any transition left `logged` is replayed
against the item record, and the ambiguous case disappears. The ordering above is
still what makes this work — appending first is what guarantees the log is the
complete side — but the marker is what a recovery procedure actually consults.

**The state advances by a second append, never by editing the entry.** The log is
append-only and that property is load-bearing, so `applied` is recorded as a small
commit entry following the transition it completes. A transition whose commit entry
is absent is the one to replay. Editing the original entry in place would buy one
write and give up the guarantee that nothing in this log is ever rewritten.

**Two states, not four.** *Requested* and *rejected* belong to a proposed effect's
path and never reach this store: nothing is written here until the runtime has
realized the type-4 effect, so capability and gate have already passed by the time
the log sees anything. Those dispositions are recorded once, by
`02-observability-event-model.md` (kind 4). Carrying them here as well would make
this store shadow observability, and two records of one fact that can disagree is a
failure mode with no owner.

The application state is a different thing from a disposition. It is local to this
store and describes only whether **this store** finished its own write.

## The declared scope

Three fields on the work item, and they are three rather than one because each
answers a different question in the check.

- `boundary` — the mandate, as **natural-language text**. This store holds it
  without interpreting it, consistent with holding a formulation without judging
  whether it is well-formed.
- `derivation` — what the boundary was derived from. Required whenever the
  boundary was not stated by the operator. A derivation nobody can read cannot be
  contested, and an uncontested wrong derivation is ratified rather than caught
  (`03-capability-authority-model.md`).
- `scope_state` — `stated` (the operator gave one), `derived` (an invariant
  processor produced it from intent, or the orchestrator narrowed it), or
  `pending` (the reading was ambiguous, and the question went to the operator).

Normative:

- `pending` and **absent** MUST be distinguishable. The first is the check working
  as designed; the second is the check not having run. They call for opposite
  responses, and the second stops work.
- The scope MUST be readable **at any point during the task**, not only at its
  end. The irreversible half of the check runs before an effect happens.
- A change to any of the three MUST appear in the transition log. Two reasons, and
  both matter: a mandate widened mid-task is what an audit needs to *see* rather
  than find silently already true, and an item that is refined or split has its
  scope legitimately re-derived — those two look identical unless the history
  distinguishes them.
- An operator's own indication of a boundary is carried as part of the scope and
  **governs** the derived portion. Explicit beats derived.

The scope needs **no special protection** in this store, and that is a result
rather than an oversight. Widening it is a type-4 mutation, which is an effect,
which the scope check sees — modifying the scope is inside the current scope or it
is not. What that costs is a default rather than a mechanism: a scope permitting
its own modification is excluded unless explicitly granted
(`03-capability-authority-model.md`).

## Creating a task, and where decomposition lives

**Any processor holding the work-record-mutation grant may create a task from the
one it is working under.** Decomposition needs no mechanism of its own: it is task
creation, effect type 4, gated and recorded like any other
(`03-capability-authority-model.md`).

Which actor actually holds that grant is **configuration, not architecture**. An
orchestrator is the obvious candidate; a planner, a reviewer or a judge are equally
admissible, and different system arrangements may assign it differently. That is the
same reason operational constraint is expressed over effects rather than over roles
(`01-effect-vocabulary.md`): the role vocabulary is open, so nothing normative may
be keyed to it.

**Creating a task triggers a call to the invariant processor, which writes the new
task's ceiling.** This is what gives every task a scope by construction. There is no
separate moment at which a ceiling gets derived and no path by which a task comes
into existence without one — a task that exists was created, and creation derives.

Two consequences worth stating.

**The child's ceiling is still bounded by the parent's**, so deriving at creation is
not a way to obtain a wider mandate. The derivation runs under containment, below.

**What remains hard about decomposition is not the creating.** It is writing the
sub-objectives: each part needs a formulation, and a model writes it, which is the
one composition case `06-processor-contract.md`'s handoff rule explicitly does not
support. Splitting a task is cheap; saying what each part is for is not.

## Attachment edges

An attachment edge runs from a work item to a claim in `12-knowledge-model.md`. It
is the **curated** relation: this claim, deliberately, as opposed to everything that
happened to cross while the task ran. The bulk relation is the task's live set
(`14-context-manager.md`), which every crossing joins automatically.

**The edge label vocabulary is not fixed, and there is a mismatch to resolve before
it can be.** What the design set names informally is *finding*, *proposal* and
*decision*. Two of those three are claim types in `12-knowledge-model.md`, which
holds `observation`, `evidence`, `finding` and `decision`. **There is no proposal
claim type**, so as written an attachment may be labelled with something the claim
store cannot be holding.

Three readings, and the set does not choose:

- A *proposal* is a **pre-realization** object — what a thinking processor produces
  before the type-5 mutation is gated (`00-design/22-arch-cognition/04-thinking.md`).
  If so it is not yet a claim, and an attachment pointing at one contradicts
  attachments pointing into the claim store.
- A *proposal* is a **decision not yet taken** — a course of action put forward and
  not accepted. That is a real thing with no type, and it would need one.
- *Proposal* is loose usage for a Finding that recommends something, in which case
  the label should go.

Until this resolves, an implementation MUST record the label it used and MUST NOT
treat the three words as a closed set.

**The edge carries more than a label.** What the design set already implies it must
hold: which claim, under which work item, when, and by which invocation. Whether it
also carries a *reason* for the attachment — why this claim was singled out from the
live set — is unspecified, and it is the field that would make a curated attachment
distinguishable from an arbitrary one.

## Containment on split and refine

Two constraints belong to this store because they are about the **shape of the
lineage** rather than about any judgment. A conforming implementation MUST reject
a transition that violates either.

- **A split's children inherit the parent's scope and may narrow it, never widen
  it.** A proposed child whose boundary is not contained in its parent's is not a
  split; it is a new root, and a new root needs intent, which only arrives from
  outside. Without this, splitting is a way to manufacture mandate — widen in the
  child, act under the child.
- **A refinement stays under its item's intent.** Scope derives from a
  formulation, so refining broadly and re-deriving would widen the scope without
  anything ever splitting. What bounds it is that a refinement changes the
  formulation and not the intent: a re-derived scope may move underneath the
  intent's scope and MUST NOT push past it.

The two are one rule seen from two sides — **mandate descends and never widens on
the way down** — and the third side of it, nested invocation, is
`06-processor-contract.md`'s.

Deciding containment is a natural-language judgment and this store does not make
it. It rejects a transition whose containment check did not pass; the check itself
is `03-capability-authority-model.md`'s.

## Recorded conclusions

A processor's own recorded conclusion is a **type-4 work-record mutation**, not a
memory write. The M4 runs found this boundary carved cleanly once chosen, though
it was not self-evident from the vocabulary alone (findings-log entry 4).

Three verdicts, each with its reasoning:

- `answered` — the objective was pursued to a conclusion.
- `blocked` — could not proceed: missing context, capability, or dependency.
- `declined` — the correct response is not execution.

**Keeping `declined` distinct from `blocked` is load-bearing.** Milestone 5
recorded an orchestrator collapsing "the task rests on a false premise" and "I
cannot find a next step" into one generic outcome, losing a distinction the
simpler Milestone 4 arms had made. Whatever verdicts exist, an implementation MUST
keep them distinguishable in the record.

Two of the four reasons `22-arch-cognition/01` gives for not executing are
conclusions and two are transitions, and they land in different places here. A
false assumption and an already-satisfied request **end** the item — they are
conclusions. A different problem being more relevant, or more investigation being
needed, end nothing — they are a refinement or a split, and the item continues.

Whether an instance judges objective validity at all is that instance's strategy
(`10-foundations/04`). Being able to record the verdict once it does is not
optional.

A **decommission** MUST be distinguishable from ordinary task failure. The half of
that which is a recorded conclusion lands here; the event-history half is
`02-observability-event-model.md`'s kind-3 record.

## Service surface

What callers may ask for. This is the part that has to survive the store changing
shape, so it is specified while the storage is not.

*(Illustrative signatures — intent, not a fixed interface.)*

```
get_intent(intent_id)                -> Intent
lineage(work_item_id)                -> [work_item, …, intent]
get_item(work_item_id)               -> WorkItem          # current state, one read
children(work_item_id)               -> [WorkItem]
transitions(work_item_id | lineage)  -> [Transition]      # ordered
attachments(work_item_id)            -> [ClaimRef]        # resolve against 12
scope_of(work_item_id)               -> (boundary, derivation, scope_state)
change_set(work_item_id)             -> [EffectRef]       # for the scope check
```

`lineage` is what `01-effect-vocabulary.md` already depends on: a realized effect
must be reconstructable **per intent lineage**, not only per actor, and nothing in
the architecture band supplied that chain. This store is what knows it.

`change_set` exists for `03-capability-authority-model.md`'s aggregate check. It
composes the store's attribution with observability's realized-effect history
rather than duplicating either.

## General shape and the naive default

The same restraint `12-knowledge-model.md` commits to: **the filesystem, no
database, no index**, until evidence says the naive version is the actual
bottleneck.

Read that as sequencing rather than as doubt that a real store will eventually be
needed. The consequence for this document is where the normative weight sits: the
**service surface above is binding, the storage below is not**, and a caller MUST
NOT be able to learn that a work item is a file.

Illustrative default:

```
work/
  intents/<intent_id>.json              # written once, out of band
  items/<work_item_id>.json             # current state, rewritten in place
  transitions/<work_item_id>.jsonl      # append-only, one line per transition
```

## Authority

- This store **MUST NOT be written except by the runtime realizing a type-4
  effect**, plus intent arriving out of band. A cognitive component reaching the
  files directly is a defect of the same class as bypassing the gate — it
  persists what was proposed rather than what was permitted.
- It **may refuse a transition** that breaks the lineage constraints above. It may
  never judge whether the work is right, whether a conclusion is correct, or
  whether a scope is well-chosen.
- It is **queried and never pushes**. `23-arch-context-management` registers a
  work item reaching a processor as a crossing like any other; this store does not
  put anything into a context.

## Failure modes

- **Written outside the effect path.** A work item changed without a realized
  type-4 effect behind it has no proposed→realized chain, no capability decision,
  and no gate decision. It MUST be detectable: every transition names the effect
  that realized it, and one that names none is a defect.
- **Intent edited in place.** The heaviest failure here, because mandate descends
  from intent: a system that can rewrite what the work is for can rewrite what
  bounds it. Intent records MUST be write-once from the system's side.
- **State and log disagreeing.** An implementation MUST detect that the item record
  is not what the log adds up to, and MUST halt rather than continue. Repair
  rebuilds the item record from the log; editing the log to match the record
  destroys history.
- **An application state edited in place.** Recording `applied` by rewriting the
  transition entry gives up the one property that makes the log worth trusting for
  repair. It MUST be a second append.
- **A containment refusal left unrecorded.** A split or refinement this store
  refuses for containment is an attempt to widen a mandate, which is the clearest
  boundary-probing signal the scope apparatus can produce. It is recorded by
  observability as a kind-4 disposition (`02-observability-event-model.md`), not
  here — the item's log records what happened to the item, and nothing happened to
  it. An implementation that records the refusal in neither place has discarded the
  signal.
- **Scope change absent from the log.** Then a mid-task widening is
  indistinguishable from a boundary that was always there, which is exactly what
  the audit exists to catch.
- **`pending` collapsed into `derived`.** Converts a correctly-detected ambiguity
  into a silently chosen reading.
- **Containment unchecked on refinement.** An implementation that checks splits
  and not refinements has left open the route splitting alone did not close.
- **Verdict collapse.** `declined` folded into `blocked`, or the two reasons for
  declining folded into one, reproduces the failure M5 recorded.
- **Claim content copied here.** An attachment holding a claim's text rather than
  a reference creates a second copy that goes stale silently.
- **An attachment left dangling after its task ends.** While a task lives, anything
  attached to it is a root and cannot be deleted (`12-knowledge-model.md`). When the
  task ends, a curated attachment is not by itself a promotion as specified, so the
  claim can be removed and the edge left pointing at nothing. An implementation MUST
  be able to detect an attachment that no longer resolves rather than returning it
  silently.

## Relationships

- **`22-arch-cognition/01-work-intent-and-task-model.md`** — owns the vocabulary
  this store persists. It adds no concepts to it.
- **Effect vocabulary** (`01-effect-vocabulary.md`) — type 4 is the only write
  path, and type 4's exclusion of intent content is what makes intent immutable
  here.
- **Capability and authority model** (`03-capability-authority-model.md`) — owns
  the scope check; this store owns the declaration it reads.
- **Knowledge model** (`12-knowledge-model.md`) — holds the claims this store's
  attachment edges point at. Separate stores, one direction of reference.
- **Observability** (`02-observability-event-model.md`) — this store is
  authoritative for what the work currently is; observability's copy of a work
  transition is a witness, and a disagreement between them is a partial write to be
  reported rather than resolved by preference (`02`, Which copy is authoritative).
  It keeps that copy for the same retention and compression reasons it does not read
  the other stores directly, and it supplies the realized-effect history
  `change_set` composes with.
- **Orchestrator** (`08-orchestrator-contract.md`) — reads current work state
  every loop step and proposes the transitions that change it.
- **Runtime** (`20-arch-runtime.md`) — gates and realizes a type-4 mutation; this
  store persists what was realized, never what was proposed.

## Open contracts

- **Work units.** Whether they need first-class persistent representation or
  remain an emergent orchestration concept. Inherited from
  `22-arch-cognition/01`, and it decides whether this store holds two record kinds
  or three.
- **Split and merge.** One primitive exercised in two directions, or two genuinely
  different transitions? This decides what the parent and child links have to be
  able to express, and a merge with multiple parents does not fit the single
  `parent_item_id` above.
- **Abandoned items.** Retained or removed. Retention is the cheaper assumption
  and keeps "why was this dropped" answerable, but nothing establishes that it is
  required.
- **The attachment label vocabulary.** *Finding*, *proposal* and *decision* are
  what the design set names, and *proposal* has no counterpart among the claim
  types. Resolving it decides whether a new claim type is needed, whether the label
  goes, or whether attachments may point at something that is not yet a claim.
- **Whether an attachment edge carries a reason.** Without one, a curated
  attachment and an arbitrary one are indistinguishable afterwards, which undercuts
  the point of curating.
- **Verdict granularity.** Whether three conclusions suffice. A false-premise
  refusal and an already-satisfied request both land on `declined` while calling
  for different follow-ups — possibly M5's collapse reproduced one level down.
  Owned with `06-processor-contract.md`; what this store owes is only that
  whatever verdicts exist stay distinguishable.
- **What `change_set` actually returns.** A list of effect references, a
  summarised diff, or something the scope check can read without re-deriving the
  whole run. Shared with `03-capability-authority-model.md`, where it is the
  largest unknown in the mandate half.
- **Intent versioning.** Amendment produces a new version rather than an edit;
  what a work item descending from a superseded version reads, and whether its
  scope is re-derived, is not settled.
- **Concurrency.** Nothing here establishes what happens when two invocations
  transition the same item. R2 currently bounds the system to one active
  invocation, so the question has not arisen; it will when R2 relaxes.
