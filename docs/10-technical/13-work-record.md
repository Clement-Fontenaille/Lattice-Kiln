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

- **Three record kinds**, not one. Intent, work item, transition — with different
  write disciplines, which is the reason they are not one store. Discarded:
  folding work into `21-arch-knowledge-model`, where a record is append-only and
  its current truth sits at the end of a chain. A work item's current state must
  be readable without walking anything, because the orchestrator reads current
  work on every loop step.
- **Scope as three fields on the work item** — boundary, derivation, state — not
  one opaque string and not a structured predicate.
- **An append-only transition log kept alongside an item rather than inside it.**
  Discarded: reconstructing current state by folding the log, which makes the
  read the orchestrator performs most often the most expensive one.
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
- `attachments` *(illustrative)* — references into `21-arch-knowledge-model` for
  the findings, proposals and decisions attached to this item, plus this store's
  own metadata about each edge. The claim's **content** lives there and MUST NOT
  be copied here. Two stores point into one claim store; neither owns it.

Reading an item's current state MUST NOT require replaying its transitions.

**Which reads this is about.** The orchestrator's observe step, once per loop step
and once per item it has in view: `get_item`, `children`, `scope_of`. That is the
hottest read in the system. It is *not* about `transitions`, which is the history
read and is supposed to walk, nor about `lineage`, which walks parents along a
chain bounded by how deep the work tree goes, nor about `change_set`, which runs
once per task for the scope check.

**Two store shapes would force a replay, by different mechanisms.** Under **event
sourcing** — holding only the append-only log — `get_item` means reading every
transition for that item and folding them in order, so the cost grows with the
number of transitions. The hot read gets slower exactly as the loop runs longer
and the item accumulates history, which is the worst possible direction for it to
grow. Under **append-and-supersede**, which is `12-knowledge-model.md`'s
discipline, nothing is edited and a correction is a new entry pointing at the old
one, so current truth sits at the tip of a supersession chain and reading it means
chasing pointers. Not a fold, the same class of cost. That second one is the
actual argument for this being a separate store rather than a region of the
knowledge model: two different write disciplines, and collapsing them forces one
to give.

### 3. Transition

One append-only log per work item, kept **alongside** the item.

MUST carry: `work_item_id`, `transition` (refined / challenged / split / merged /
deferred / abandoned / executed), the effect that realized it, the invocation that
proposed it, and a timestamp.

- The log is **append-only**. A transition is never edited or removed.
- Current state and history are **both held**. The redundancy is deliberate:
  computing state from the log makes the common read expensive, and the log cannot
  be computed from the state at all, since it holds strictly more — every
  superseded formulation, who proposed each change, which effect realized it, and
  when.

### Not derived on read is not the same as not determined

`28-arch-work-record` says the two are held such that "neither is derived from the
other", and that phrase needs one distinction drawn before an implementation can
act on it.

The state is **not computed at read time** by folding the log. It is nonetheless
**logically determined** by it: the state record is what the log's transitions add
up to. Only the second half of the architecture's phrase is unqualified — the log
really is not derivable from the state, because it holds more.

That matters for two concrete things.

**A repair path exists.** A state record lost or corrupted can be rebuilt by
folding the log. The redundancy buys a cheap read without costing recoverability,
which it would if the two were genuinely independent.

**Write order decides which drift is possible, so it is pinned.** A transition MUST
be appended to the log **before** the state record is updated. With that order the
only reachable inconsistency is *state behind log* — a crash between the two
writes — and repair is a fold. The reverse order admits *state ahead of log*, where
a real transition exists only in the record that gets rewritten, and no repair
recovers it.

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
- **State and log disagreeing.** The two are separately written, which means they
  can drift. An implementation MUST be able to detect that the current state is not
  what the log adds up to, and MUST halt rather than continue on the discrepancy.
  **The log is authoritative for repair** — not because it is more recent, but
  because it is the only one of the two that is never rewritten, and because the
  pinned write order makes *state behind log* the only reachable case. Rebuilding
  the state by folding is a repair; editing the log to match the state is data
  loss.
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
- **Observability** (`02-observability-event-model.md`) — keeps its own copy of
  work-record events, for the same retention and compression reasons it does not
  read the other stores directly. It also supplies the realized-effect history
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
