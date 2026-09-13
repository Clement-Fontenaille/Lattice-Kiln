# Context Manager (v0)

**Traces to:** `00-design/23-arch-context-management/01-context-manager.md`,
`00-design/23-arch-context-management/02-context-as-experimental-surface.md`,
`00-design/10-foundations/04-context-as-governed-resource.md`,
`00-design/10-foundations/07-the-integrated-system-and-its-operator.md`,
`00-design/00-project/05-vocabulary.md`,
`00-design/40-roadmap/01-MILESTONES/09-context-governance-measurement.md` (M9);
binds to `10-technical/12-knowledge-model.md`,
`10-technical/06-processor-contract.md`,
`10-technical/07-naive-context-assembly.md`,
`10-technical/02-observability-event-model.md`.

## TL;DR

Three operations — **register**, **track**, **recall** — over a **live set** that
holds references and metadata, never content. It composes the **turn input**
afresh on every turn. It initiates nothing, gates nothing, and holds no artifact
of its own.

> **Motto:** Nothing crosses without being counted.

## Three words, fixed before anything else

The specification is unusable if these blur, and one word was hiding two
activities (`00-design/00-project/05-vocabulary.md`).

- **Context** is the model's own production state, living in the inference
  substrate and bounded by GPU memory rather than by text size. This component
  *manages* it and never *holds* it.
- **The live set** is the set of artifacts **attached to a task**. References and
  metadata. Membership follows the task, not the model: an artifact is in the live
  set because it crossed while working on that task, and it stays there whether or
  not any given turn puts it in front of the model.
- **The turn input** is what is actually transmitted on a given turn.

An implementation MUST NOT name a single object "the context". Reasoning about
context and being context are different activities.

## Status of this document

v0. `07-naive-context-assembly.md` implements a fragment of this already and is
credited rather than replaced: it is a **degenerate recall policy** — recall
everything until the budget runs out, then drop the rest — which puts it on the
same axis as anything richer rather than making it a different kind of thing.

What is specified ahead of any implementation: registration, the live record, and
the composition path. What is deliberately not specified: **what the recall policy
actually is**. That is named as a required responsibility and left arbitrary, and
`00-design/23-arch-context-management/02-context-as-experimental-surface.md` holds
why — it is the project's experimental surface, not a gap to close by writing a
better rule here.

## Responsibility

**Register** artifacts as they cross in. **Track** the live set that registration
populates. **Recall** — present, to the model, material the live set already
holds.

It does not decide what to fetch, does not fetch, does not gate, and does not
judge relevance beyond whatever policy it was configured with.

## Narrowing

`23-arch-context-management/01` states an actor, three operations, and a
provisional storage position. This document narrows to:

- **The live set holds references plus metadata and no content**, for every
  crossing type. Discarded: a live set holding copies, which can drift from the
  record and forces a content-moving step at promotion time.
- **Composition happens per turn, with no per-invocation object.** Discarded: the
  `context_bundle` — bound once at instantiation and held — which
  `06-processor-contract.md` used to carry and no longer does.
- **Crossing type as a first-class field on every entry**, rather than a property
  recoverable from the source. The presentation constraint below needs it at
  composition time.

## Register

Every artifact crossing in is registered: from a tool call — a read, a test run,
any effect response — or from the model's own generated output.

- What crossed in is written to `12-knowledge-model.md`. What this component keeps
  is a **reference to that entry plus its own tracking metadata**: crossing type,
  the moment it happened, and whatever else recall needs.
- This component **MUST NOT initiate a crossing**. It records what came back once
  something else did. There is no path by which it fetches on a processor's
  behalf.
- Registration is bookkeeping, not a proposed effect. It is ungated, for the same
  reason the Observation write path in `12-knowledge-model.md` is.

### Event and content are separate, and only the event is universal

A registration records two things: **that a crossing happened**, with its type and
moment, and **what that crossing returned**.

- For a tool call or a generation the two coincide — the event and the content
  obtained are one Observation.
- For a **knowledge-base retrieval they come apart**. The event happened, but what
  came back is a claim that already exists, so **no content is written** and the
  registration carries a pointer.

Writing a retrieval as content is a defect rather than waste. A second node would
exist for one claim, and a later provenance walk would see two — the exact
confusion `10-foundations/03`'s graph is built to avoid.

The separation earns something besides. A retrieval's event record is a trace of a
claim being **used**, and `10-foundations/03` holds that friction is noticed when
a claim is put to load-bearing use rather than by scheduled audit. Retrieval
events are the signal saying which claims carry weight and how often — the data
friction detection would run on, not bookkeeping noise.

So the **shape** is uniform — every crossing produces a registration, the live set
holds a reference either way — while the **cost** is not, since only some
crossings add content. An implementation that flattens the two makes a retrieval
look as expensive as a first read.

## Track — the live set

*(Illustrative entry shape.)*

```
LiveSetEntry := {
  live_set_id,
  claim_ref,              # into 12-knowledge-model
  crossing_type,          # read | generation | retrieval | effect_response
                          # generation subdivides: see Splitting a generation
  origin_invocation_id,   # which instance obtained it -- the only primitive here
  registered_at,          # per-run monotonic sequence, not wall clock
  policy_metadata         # whatever the configured recall policy needs
}
```

### The policy is mechanical, and this is its input domain

**Recall runs on every turn, so it MUST be a deterministic function over recorded
facts.** A model call to decide what to show the model is a recursion — something
would have to compose a context in order to choose a context — and this project's own
evidence points the other way besides: a deterministic gate scored 9/10 alone and
6/10 with a 7B panel added (M5 follow-up).

That the policy's **content** is deliberately unspecified
(`00-design/23-arch-context-management/02-context-as-experimental-surface.md`) says
nothing about its **kind**. What is open is which function; that it is a function
over these fields is not.

So the fields above are not bookkeeping. They are the **vocabulary every candidate
policy is written in**, and a fact this entry does not carry is a fact no policy can
branch on. That makes omissions expensive in a specific way: they do not make a
policy harder to write, they make a whole class of policy **inexpressible**.

Concretely, each field earns its place by a policy that needs it:

- `crossing_type` — *a retrieval was deliberately fetched; an incidental read was not.*
  Order by how the artifact was obtained.

#### Splitting a generation

A processor's output is not one artifact. A turn producing reasoning and a conclusion
registers two, and the distinction between them rides on **`crossing_type`, by
subdividing `generation`** — not on a separate field and not on the edge. Which
channel produced an output is a fact about the crossing, and nothing else should
repeat it.

`generation` is therefore the axis that grows if outputs are split further than two
ways. What the subdivisions are, and whether they differ per role, is open
(`06-processor-contract.md`).

Two things depend on the subdivision existing. A `review` instance receives a prior
processor's conclusion and not its reasoning (`06-processor-contract.md`,
independence), and that cut is made here. And the largest saving available to a recall
policy is dropping reasoning while keeping conclusions, which is a branch on this
field.
- `origin_invocation_id` — *everything this instance obtained, before anything an
  earlier one did.* Also what an isolation preference is enforced against: a judge
  binding `share_nothing` needs to know which entries carry the reasoning it judges.
- `registered_at` — recency, and the ordered tail of the discussion.

**What a policy needs and this entry does not store.** *What this task found, before
what it inherited* is a policy worth being able to write, and the fact it branches on
is **derived rather than stored**: the originating task resolves through
`origin_invocation_id`, since the kind-1 record carries `work_item_ref`
(`02-observability-event-model.md`), and own-versus-inherited follows from comparing
that task against this one.

Storing either would be a denormalisation, justified only by the cost of resolving
it on every entry on every turn. Nobody has measured that cost, and this project's
standing position is not to optimise ahead of evidence. So they are derived until
measurement says otherwise.

**Why inherited is not equally pertinent, stated correctly.** Not because the parent's
scope was wider — a child narrows or leaves the boundary unchanged, so a parent's
scope is never narrower and is often identical. The reason is the **objective**: an
artifact obtained under a parent was fetched in pursuit of what the parent was for,
and a child exists because that was split or refined into something else. Fetched for
one purpose is not thereby fetched for another.

**Judgement is available to a mechanical policy, provided it was made elsewhere and
recorded.** Whether a claim is promoted is a decided fact readable through
`claim_ref`; so is its claim type; so is a curated attachment on the work item
(`13-work-record.md`). A policy may branch on all of them. What it may not do is
*form* a judgement at recall time — ask whether this artifact is pertinent to this
objective — which is the one thing `10-foundations/03` holds must be judged live by
whoever is asking.

The pipeline is therefore one-way: **something judges, the judgement is recorded as
a fact, the policy reads facts.** Never the policy asking for a judgement.

**The criterion for adding a field**: record a fact when a plausible policy would
branch on it **and nothing else already carries it**. Not because it is true, and not
because it is cheap.

The second clause does most of the work in a system with several stores. A claim's
type and whether it is promoted are on the artifact and readable through `claim_ref`.
The task's scope is on the work item. The originating task is on the invocation
record. None of them belongs here, and copying any of them creates a second place
that can go stale.

**Every field here is a proxy for pertinence, and none of them is pertinence.**
`10-foundations/03` holds that pertinence is a property of a comparison, judged live
by whoever is asking, and a policy that runs every turn cannot do that. So a policy
combines proxies — how the artifact was obtained, how recently, under which objective,
whether someone judged it worth keeping — and is better or worse according to how well
that combination predicts what would actually have helped.

That is what makes the policy's content an experimental surface rather than an
unfinished specification. The search is for which proxies, combined how.

- **A live set belongs to a task, not to an instance.** Every artifact that crosses
  while work proceeds on a task attaches to that task's live set, including a
  knowledge-base retrieval, which attaches to the task that triggered it.
- **It grows within a task's life and does not shrink.** Registration only adds. An
  artifact the recall policy passed over on some turn is still a member; it was not
  shown, which is a different thing from not being held.
- **A new task's live set is not empty either.** The intent has crossed into the
  work, and a crossing registers — so the set holds at least an Observation of the
  operator's request before any tool is called. Whether the objective and the scope
  follow by the same argument, and by what crossing type any of them arrives, is
  open (`70-THINKING/18-task-artifact-edges.md`).
- A second instance working under the same task finds the set already populated,
  because it outlived the instance that filled it.
- **It ends when its task does.** That is what removes its members from the root set
  and triggers their deletion (`12-knowledge-model.md`).
- **It is not durable memory.** It is an index over a task. What an item leaves
  behind is its content in `12-knowledge-model.md`, which persists exactly as long as
  something still reaches it.

## Recall

**Recall is the positive operation: it presents.** It brings something the live
set already holds back in front of the model.

- Recall **MUST NOT fetch**. It works only over what the live set holds, and that
  boundedness is the point rather than a limitation: given a fixed live set, a
  policy chooses what to put in front of the model, which makes **two policies
  directly comparable** while the live set is held constant.
- **Not being shown is not leaving.** An artifact the policy passed over on one
  turn can be recalled on the next. That is an ordinary recall, not a fresh
  crossing, because the artifact never stopped being a member.
- **What is out of reach of recall is what was never attached to this task.**
  Obtaining it is a **retrieval** — a fresh crossing, gated and registered like any
  other, attaching to the task that triggered it.
- There is **no "archived, then recalled later" tier**. An artifact is attached to
  a live task or it is not held here at all. An implementation that adds an archive
  tier has invented a state the vocabulary does not have.

### Prefix persistence changes the shape of the policy space

Whether the serving arrangement keeps a reusable prefix across turns is not a
performance detail underneath recall. It decides what kind of question recall is,
so an implementation MUST NOT assume one arrangement in the policy interface.

**Without prefix persistence**, everything the model is to see is sent again every
turn. The whole live set is recalled by necessity; leaving something out is
possible but it is not an optimisation — it simply denies the model that material.
The strategy space collapses to two levers: what is included at all, and in what
**order**. Ordering then carries most of the question, and it is a real one,
because position affects what a model attends to.

**With prefix persistence**, the stable part of the sequence is not recomputed.
Appending is cheap; disturbing anything before the append point is not. The space
opens considerably: what belongs in the stable prefix and what in the mutable
tail, whether anything is ever removed from the prefix and what that costs, what
happens when something dropped has to come back, whether several live sets can
share a prefix, whether a policy should shape the sequence for reuse rather than
purely for relevance.

Those are not settleable from this project's first principles. They need
experiment and whatever the literature already holds.

### Several prefixes can be resident, so the lever is selection

Keep-or-drop is not the choice. A serving arrangement holds more than one cached
sequence at a time, so the lever is **which resident prefix this turn input
continues from**, bounded by memory rather than by exclusivity. This extends the
strategy space above; it does not replace it
(`00-design/23-arch-context-management/01-context-manager.md`, The policy governs
several contexts at once).

Prefix identity is therefore a **third axis**, distinct from which live set an
instance registers into and distinct from what recall selects out of that live
set. A policy interface MUST be written against selection. One written against
keep-or-drop cannot express selection later without changing every call site, while
one written against selection degenerates to keep-or-drop at N=1 with nothing lost.

#### What llama.cpp offers

The MVP host runs llama.cpp, so the mechanisms available to a policy are its
mechanisms. *(Illustrative — flag names and behaviour drift between versions, and
this MUST be verified against the installed build before anything is written
against it.)*

- **Slots.** `--parallel N` gives N independent sequences, each with its own KV
  region. This is the multiple-prefix primitive.
- **Per-slot prefix reuse.** A request assigned to a slot is matched against what
  that slot already holds, and only the divergent suffix is reprocessed.
- **A divided envelope.** The total context is shared among slots, so roughly
  `ctx_size / N` each. **Isolation costs context, permanently, for every slot that
  exists** — this is the price of the whole arrangement and it is paid whether or
  not a slot is busy.
- **Slot save and restore.** A slot's KV state can be written to disk and brought
  back. This is the concrete form of trading disk space for memory space.
- **Reuse with gaps.** Some builds can reuse a cached prefix across a removed
  chunk rather than requiring a strict common prefix.

#### Two limits, and a cost model nobody has

Capacity is bounded in **two** ways, and a policy has to respect both:

- a **per-context limit** on any single context;
- a **global limit** on all resident contexts together.

They are independent. One oversized turn input trips the first while the machine has
room; several individually-reasonable contexts trip the second while each looks fine
alone. `05-provisional-invariant-list.md` R4 carries both as clauses.

What neither has is a **number**, and getting one is a cost model to build rather
than a figure to look up. KV footprint depends on the model, the quantisation, the
arrangement and how much of this the build understands, and that understanding is
expected to improve. The v0 stands in for the model rather than guessing it:

**A naive calibration test, triggered automatically the first time an unknown model
is invoked.** Measure what one context costs, record it against the model identity,
and use that until something better exists. The ceiling is enforceable on day one
and nobody has to pretend the number is principled.

One further comparison is unmeasured and matters for the disk-for-memory trade:
restoring a saved context from disk against simply recomputing its prefix. Restoring
is bounded by disk throughput and linear in KV bytes, which run orders of magnitude
above the text; recomputing is a prefill pass bounded by compute. Both are plausible
winners.

#### The isolation preference

An instance binds an `isolation` value at instantiation
(`06-processor-contract.md`), and the policy consumes it when choosing which prefix
a turn input continues from.

*(Illustrative shape.)*

```
isolation := share_nothing | share_base | continue(prefix_id)
```

- `share_nothing` — a fresh sequence, inheriting no prefix that carries another
  instance's reasoning.
- `share_base` — may continue a prefix designated as a common base (role
  instructions, a repository tree), and no prefix carrying a conclusion.
- `continue(prefix_id)` — resume a named prefix, normally the preceding step on the
  same task, where the material is the instance's own work and resuming it is
  cheap.

**Arbitration when preferences exceed capacity.** Slots are finite and the envelope
divides, so a policy will not always grant what was asked. It MAY degrade a
preference, and it MUST record what was actually granted rather than only what was
requested (`02-observability-event-model.md`, kind 5). A judge whose isolation was
silently degraded is indistinguishable afterwards from one that had it, which is
the case the record exists for.

**One class of processor is not negotiable.** An **invariant processor** binds
`share_nothing` and the policy MUST NOT degrade it. A scope check assembled on the
prefix of the work it is checking has been handed the reasoning it exists to
assess, and it then passes for the wrong reason — a failure that looks like a
passing check. Where `share_nothing` cannot be provided, the check **has not run**,
and `03-capability-authority-model.md` already says what follows from that: it fails
closed, and work stops.

That is the one place isolation stops being an economy and becomes a correctness
property.

#### If the substrate cannot isolate

The rule above is written from the caller's side, where isolation is simply
required. That leaves the question of what happens when the serving arrangement
cannot provide it, and the answer is not a fallback.

**Isolation capability is a prerequisite of the deployment, not a runtime
negotiation.** A conforming arrangement holds at least two independent contexts at
once, each large enough to do its work. This is recorded as a precondition on G4
(`05-provisional-invariant-list.md`), it is verifiable before any work starts, and
a system that fails it cannot provide a functioning scope check whatever else it
builds.

Putting it at deployment rather than at runtime is what keeps the rule clean. A
runtime fallback would have to choose between running an unisolated check — which
is worse than none, since it looks like a pass — and halting on every check, which
is an unusable system discovered one task at a time. Neither is better than
refusing to start.

Note what the prerequisite is actually about, because the count is the easy half.
Two sequences are trivially available; two sequences **each still large enough** is
the constraint, since the resident envelope divides among them. An arrangement that
isolates by halving both contexts below what the work needs has traded one failure
for another, and R4 is where that shows up.

## Compose — the turn input

- The turn input is composed **at the moment of feeding**, out of what the live
  set holds and what recall selects from it.
- It is **recomposed every turn**, over a live set that grew since the last one.
  There is no package delivered once per invocation and then held.
- **Nothing requests one.** This component sits in the path everything to and from
  the model takes, so it composes because a turn is happening. There is no
  assembly call to place and no caller to name.

### Generated content MUST NOT silently occupy the place of authored content

`10-foundations/07` places this on the system, and composing the system's own
inputs is this component's business and nobody else's.

Honouring it costs nothing new. Every entry carries its crossing type, and a
generation is a different crossing from a read or a retrieval, so the distinction
is available at composition time. `10-foundations/03`'s **source** axis carries
the second cut, between a human's contribution and the system's own.

What the requirement asks is that the distinction **survive into the turn input**
rather than being flattened there. A turn input presenting a generated artifact
indistinguishably from a retrieved claim has erased something it was holding, at
the one point where the erasure is invisible afterwards: the model sees the
flattened version, not the record.

This is a **presentation** constraint, not a permission one. Nothing here decides
what may be recalled; it decides that what is recalled arrives marked as what it
is.

## Live-state query

A read-only query over the live set, for `10-foundations/04`'s failure-mode checks
to consult.

One of those checks is answerable here and one is not, and the split is worth
stating because it bounds what this component can be asked for. **Insufficiency**
divides into material that never crossed and material that crossed but was not
recalled. The second is visible by comparing the live set against what was
composed. **The first is not visible from here at all**, since nothing can be
compared against what was never fetched.

## Observability, and why it is not optional here

`02-observability-event-model.md` MUST record **each turn input** and the live-set
lifecycle transitions. Two things depend on it:

- Answering what a processor was actually shown, and when.
- The comparability argument above. Two policies over the same live set are
  comparable **only if what each presented was recorded**. Without that history,
  comparability is a property of the design that nobody can take a reading of.

The recorded unit is therefore the turn input, not a per-invocation bundle. That
is a change `02-observability-event-model.md` owes.

## Authority

- **None.** This component gates nothing. What reaches it has already been allowed
  — a read by capability, an effect by capability and then the gate.
- It **MUST NOT initiate a crossing**, on a processor's behalf or otherwise.
  Knowledge-base retrieval is a tool like any other: the model calls it, the
  runtime executes it, this component registers the reference.
- It **MUST NOT hold artifact content**. One copy exists, in
  `12-knowledge-model.md`.
- The recall policy is **tunable system configuration**
  (`00-design/27-arch-adaptation-and-evolution/`): system-level feedback may
  propose a revision, a generation carries one, a bootstrapped instance inherits
  the validated version. It is not this component's to choose at runtime.

## Failure modes

- **Content in the live set.** Two copies that can drift, and a promotion path
  that has to move content between stores. The single copy is what makes drift
  impossible rather than merely unlikely.
- **A retrieval written as new content.** Creates a second node for one claim and
  corrupts every later provenance walk. Silent at the time.
- **Crossing type flattened in the turn input.** Violates the authored-content
  constraint at the one point where the erasure cannot be recovered afterwards.
- **Turn inputs unrecorded.** Costs nothing at runtime and destroys the entire
  policy-comparison programme. The measurement is the reason recall was made
  bounded in the first place.
- **Recall reaching outside the live set.** Turns recall into retrieval without
  gating, registration, or a record that a crossing happened.
- **An archive tier.** Makes "bring it back" ambiguous between a free presentation
  and a gated crossing.
- **A bundle bound at instantiation.** Reintroduces the object the processor
  contract removed, and makes the turn input stale by construction after turn one.
- **The live set treated as memory.** It is an index over a run; what persists is
  in the knowledge model, subject to the sweep.

## Relationships

- **`10-foundations/04`** — owns the concepts this component realizes.
- **Knowledge model** (`12-knowledge-model.md`) — where every crossing's content
  is written and what the live set points at. Queried only when the model calls
  the retrieval tool.
- **Processor contract** (`06-processor-contract.md`) — binds a `live_set_id`, not
  context. What an instance sees is composed turn by turn.
- **Naive context assembly** (`07-naive-context-assembly.md`) — the degenerate
  recall policy and the naive seeding procedure. A fragment of this component, not
  a competitor to it.
- **Observability** (`02-observability-event-model.md`) — a separate store holding
  its own copy of turn inputs and lifecycle transitions.
- **Runtime** (`20-arch-runtime.md`) — executes the crossings whose outputs this
  component registers.
- **Capability and authority model** (`03-capability-authority-model.md`) —
  decides whether a call is allowed at all, before this component sees what it
  produced.

## Open contracts

- **Seeding a new task's live set.** Continuation within a task no longer needs
  seeding: the set belongs to the task, so a second instance finds it populated. What
  remains is the genuinely new task — a split creating a child, an unrelated request —
  whose live set starts empty. Whether a child inherits anything from its parent's,
  and whether that inheritance is a reference or a fresh crossing, is unsettled.
  This is where `00-design/22-arch-cognition/08-decomposition.md`'s
  fork/join-versus-continuation question actually bites.
- **What the recall policy is.** Named as a required, distinct responsibility and
  left arbitrary by design. Nothing here fixes what triggers a drop or what
  ordering is applied.
- **Whether "not yet taken" is indexable for generations.** An unread file and an
  unretrieved claim are both enumerable as crossings not yet taken. Whether the
  same holds for the model's own possible output is unsettled
  (`10-foundations/04`).
- **The KV cost model.** First-call calibration is the v0 and is deliberately
  crude: one measurement per model identity, no account of how footprint scales with
  context length, quantisation, or the arrangement's own overhead. What replaces it
  has to predict a turn input's cost **before** the turn is composed, or R4 reports a
  crash instead of refusing.
- **Whether an artifact can be detached from a live task.** The set only grows
  within a task's life as specified. If something can be removed early — a
  correction, an artifact recognised as noise — that is a second deletion trigger and
  nothing describes it.
- **Isolation.** Whether two live sets can share entries, and what it means for
  one to be derived from another, is untouched — it depends on the seeding answer
  and on the decomposition question above.
