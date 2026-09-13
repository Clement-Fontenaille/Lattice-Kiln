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
- **The live set** is this component's record of what is in context, or is to be
  placed there this turn. References and metadata.
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
  claim_ref,            # into 12-knowledge-model
  crossing_type,        # read | generation | retrieval | effect_response
  registered_at,        # per-run monotonic sequence, not wall clock
  policy_metadata       # whatever the configured recall policy needs
}
```

- A live set is **empty at turn zero**, by construction. Register records what a
  crossing returned and recall presents what is already held, so neither operation
  can put anything into a live set before the first crossing. How a live set is
  seeded is an open contract below, not an omission.
- **The live set is not monotonic.** An item that is not recalled after a cache
  reset has left the discussion and drops out.
- **It is not durable memory.** It is an index over a run. What an item leaves
  behind is its content in `12-knowledge-model.md`, which persists until the
  retention sweep reaches it.

## Recall

**Recall is the positive operation: it presents.** It brings something the live
set already holds back in front of the model.

- Recall **MUST NOT fetch**. It works only over what the live set holds, and that
  boundedness is the point rather than a limitation: given a fixed live set, a
  policy chooses what to put in front of the model, which makes **two policies
  directly comparable** while the live set is held constant.
- **What leaves the live set is out of reach of recall.** Bringing such an item
  back is not a recall at all; it is a **retrieval** — a fresh crossing, gated and
  registered like any other.
- There is **no "archived, then recalled later" tier**. An item is live or it is
  gone from here. An implementation that adds an archive tier has invented a
  second state the vocabulary does not have and made "restore" ambiguous between
  two operations with different gating.

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

- **Live-set seeding.** A live set is empty at turn zero, and neither register nor
  recall can fill it before the first crossing. Two shapes are available.
  **Inheritance** as a third primitive alongside register and recall, moving or
  referencing already-registered artifacts across live sets with no crossing
  involved. Or **no new mechanism**: the preceding step writes a handoff into
  something durable — an attachment on a work item (`13-work-record.md`) is the
  obvious candidate — and the next instance reads it, registering the result like
  any other read. The second is cheaper and fits what exists, which is a reason to
  investigate it first and not a reason to treat it as settled.

  This is **not** the fork/join-versus-continuation question
  (`00-design/22-arch-cognition/08-decomposition.md`). That one governs whether
  sibling instances see each other's crossings, which is live-set *isolation*; it
  says nothing about how much any single live set starts with, and either
  recombination model works with a thin or a fat seed.
- **What the recall policy is.** Named as a required, distinct responsibility and
  left arbitrary by design. Nothing here fixes what triggers a drop or what
  ordering is applied.
- **Whether "not yet taken" is indexable for generations.** An unread file and an
  unretrieved claim are both enumerable as crossings not yet taken. Whether the
  same holds for the model's own possible output is unsettled
  (`10-foundations/04`).
- **KV footprint estimation.** `05-provisional-invariant-list.md` R4 refuses a turn
  input exceeding the resident envelope, which requires estimating its footprint
  **before** composing it. Nothing here supplies that estimate.
- **Isolation.** Whether two live sets can share entries, and what it means for
  one to be derived from another, is untouched — it depends on the seeding answer
  and on the decomposition question above.
