# Observability Event Model (v0)

**Traces to:** `00-design/26-arch-observability/01-observability.md`,
`00-design/10-foundations/03-evidence-belief-and-provenance.md`,
`00-design/25-arch-invariant-layer/01-invariant-enforcement.md`,
`00-design/23-arch-context-management/01-context-manager.md`,
`00-design/40-roadmap/01-MILESTONES/completed/02-observability-foundation.md` (M2);
binds to `10-technical/01-effect-vocabulary.md`,
`10-technical/12-knowledge-model.md`,
`10-technical/13-work-record.md`,
`10-technical/14-context-manager.md`.

## TL;DR

This document fixes the set of things the record of a run **must** capture for
that run to be reconstructable against a question nobody asked in advance: who was
invoked and in what lineage, every operation the runtime realized — reads
included — what the model was actually shown each turn, what changed in what the
project holds, what changed about the work, the distinct outcome category for a
safety intervention, and the conditions under which all of it was produced.

Storage shape, retention, redaction and summarisation stay open, because the
schema is expected to emerge from real feedback experiments rather than from
design.

> **Motto:** Pin what must be reconstructable; let the format follow the experiments.

## Status of this document

v0. Four of the eight record kinds below were exercised by Milestones 2–5; four
are specified ahead of any run — the turn input, knowledge-state transitions, work
transitions, and the conditions in force. Writing them ahead costs them no
authority (`00-specification-conventions.md`); the reason to write early is that a
later finding needs something to contradict.

## Responsibility

Own the **recorded form of a run** and its **reconstruction guarantees**: the
record kinds that must exist, the identity and lineage that must link them, and
the outcome categories that must be distinguishable. It does not own effect
typing (`01-effect-vocabulary.md`), gate logic, or the capability model.

## Narrowing

The design set describes what should be reconstructable without fixing a record
structure. This document narrows to a **record-per-event model** with eight
mandatory kinds, rather than a single narrative log or a periodic state snapshot.

Discarded: a pure append-only text log (fails the "relatable to hypotheses" and
per-actor-query requirements); a snapshot/diff model (loses the ordered history
the gate needs).

One further narrowing, made here because it is not obvious: **reads and typed
effects share one record kind**, rather than getting one each. The gate's
sequence evaluation reads a single ordered history whose canonical pattern is
accumulated reads followed by one carrying effect. Two kinds would force a merge
at query time and invite an implementation to build the query over effects alone —
which is the exact blindness the requirement exists to remove.

## Record greedily; decide later what it was worth

The costs are asymmetric and the asymmetry decides the default. Recording too much
costs storage and some query speed, both recoverable later once something is known
about which parts were ever consulted. Recording too little costs a question that
can never be answered, because nothing regenerates a record that was never
written.

So the working rule is to record more than seems necessary and resist pruning
early. What should end the greedy default is a **measured** cost or a concrete
privacy requirement, not an anticipated one.

## The unit: a run

A **run** is one coherent piece of AI-assisted work with a single originating
human intent. It has a stable `run_id`. Every record carries its `run_id`, an
ISO-8601 `timestamp`, and a `conditions_ref` (kind 8). Records within a run are
totally ordered by a per-run monotonic sequence number; wall-clock timestamps are
not assumed sufficient.

## Mandatory record kinds

An implementation MUST emit all eight. Fields marked *(illustrative)* name intent,
not a fixed shape.

### 1. Invocation record — identity and lineage

One per processor invocation (effect type 6, as seen from the observability side).

MUST carry:

- `invocation_id` — stable, unique within the run.
- `parent_invocation_id` — the invocation that caused this one, or null for the
  root. This is what makes **per-actor** and **per-intent-lineage** history
  reconstructable.
- `intent_ref` — link to the originating intent record (`13-work-record.md`).
- `work_item_ref` — the item this instance is working under. Effects inherit their
  work item through the instance that proposed them, which is what makes the
  aggregate scope check possible with no per-effect attachment mechanism.
- `role` — the role definition bound at instantiation (text or reference, not an
  enum — the role vocabulary is open).
- `scope` — the mandate bound at instantiation, verbatim, plus its state
  (`13-work-record.md`). Recorded **as bound**, because an instance's scope is
  static and the work item's may move underneath it; a reconstruction that reads
  the item's current scope would be reading the wrong boundary.
- `live_set_id` — the live set this instance's crossings register into. **Not** a
  reference to an assembled context: nothing is bound at instantiation, and what
  the instance saw is the sequence of kind-5 records.
- `model_identity` — model name, quantisation, and **whether inference was
  offloaded from GPU**. *(M0, findings-log entry 1: on the measured host this flag
  predicts latency by 10–20×; any performance hypothesis needs it.)*

### 2. Realized-operation record

One per runtime-mediated operation the runtime **realizes** — a typed effect or a
read. Proposed-but-rejected operations are also recorded (kind 4).

MUST carry:

- `operation_id`, `invocation_id` (the proposer).
- `type` — `1..9` per `01-effect-vocabulary.md`, or `read`.
- For a typed effect, enough to judge it after the fact **representable,
  permitted, attributable, reversible** — the same four properties the runtime
  judges at submission. The concrete carrier is an open contract shared with the
  effect vocabulary.
- `outcome` — realized / failed / **safety-intervened** (kind 3).
- `result_ref` *(illustrative)* — repository diff, process exit and output,
  network response metadata, claim id, by type.

The ordered sequence per `invocation_id` and per parent lineage MUST be queryable
without replaying the whole run, and MUST include reads. Gate sequence evaluation
runs against this; what is omitted here is invisible to the gate
(`04-enforcement-gate.md`).

### 3. Safety-intervention outcome — its own category

A gate trip that stops or alters an operation, and any decommissioning, MUST be
recorded as a **distinct terminal outcome**, never folded into generic task
failure (bad output, timeout, low quality).

MUST carry:

- `intervention_id`, and the `operation_id` / `invocation_id` it acted on.
- `kind` — gate-refusal / gate-alter / decommission / accumulation-stop.
- `disposition` from triage — logged-and-proceeded / escalated / halted — and that
  triage never granted what the gate refused.
- `retry_eligible: false` — explicit. A safety intervention is **not** eligible
  for automatic retry without recorded human review. A consumer that retries a
  rephrased proposal past this flag is defective.
- `human_review_ref` — null until a human review record is attached.

### 4. Proposed-operation disposition

One per operation **proposed** by a cognitive component, whether or not realized.
This is what lets a reconstruction see boundary-probing: repeated rephrased
proposals after a refusal.

MUST carry: `invocation_id`, proposed `type` and payload ref, and the disposition
— realized (links to a kind-2 record) / rejected-by-capability /
rejected-by-gate (links to a kind-3 record) / **rejected-by-containment**.

That fourth disposition covers a refusal neither of the other two describes. A
proposed split or refinement whose scope is not contained in its parent's is
refused by the work record acting on the scope check's verdict
(`13-work-record.md`), which is not a capability decision and not a gate trip. It
is also the clearest **boundary-probing** signal the scope apparatus can produce —
an attempt to widen a mandate, caught — so a system that records it nowhere has
discarded exactly the evidence this record kind exists to surface.

A **mandate-conformance verdict** is recorded here too, with its natural-language
reasoning, and `within` is recorded as explicitly as `outside`
(`03-capability-authority-model.md`). A check that never ran and a check that
passed must not be the same absence.

### 5. Turn-input record

One per turn, per invocation. **The recorded unit is the turn, not the
invocation** — what a processor sees is composed afresh every turn out of a live
set that grew since the last one, and there is no bundle handed over at the start
(`14-context-manager.md`).

MUST carry:

- `invocation_id`, `live_set_id`, turn index.
- **What was presented** — the live-set entries recall included, in order, each
  with its **crossing type**. Flattening crossing type here defeats the
  authored-versus-generated requirement at the one point where the erasure cannot
  be recovered.
- **What was held back** — the entries recall dropped, and any truncation.
- `policy_ref` — which recall policy produced this selection (resolvable through
  kind 8).
- **Which prefix this turn input continued from**, and the **isolation actually
  granted** alongside the isolation the instance requested. Recording only the
  request is not enough: a judge whose isolation was degraded under capacity
  pressure is otherwise indistinguishable afterwards from one that had it, and that
  difference decides whether its verdict means anything
  (`14-context-manager.md`, The isolation preference).

This record is what makes recall policies comparable. Two policies over the same
live set choose different subsets, and that comparability is a **measurement**
only if what each presented was recorded; without it, it is a property of the
design nobody can take a reading of.

### 6. Knowledge-state transition

One per change to what the project holds: a claim asserted, a qualification
appended, a claim requalified, a working compressed to a souvenir, an entry swept
(`12-knowledge-model.md`, `00-design/22-arch-cognition/04-thinking.md`).

MUST carry, **as fields rather than as narration**: the `claim_ref`, the **kind of
change**, the **grounds** given, and the proposing `invocation_id`.

The field requirement is not formatting preference. Milestone 4 (findings-log
entry 3) found unplanned questions answerable by ad-hoc joins across record kinds,
and the one failure was a conclusion recorded as free-text prose only, which
degraded the question to string matching. A qualification recorded as prose has
the same defect: "what changed about this claim, and on what grounds" stops
joining and stops aggregating.

`12-knowledge-model.md` holds the graph's **current state**; this record kind
holds the **history of how it was reached**. That distinction is what makes two
classes of question answerable and nothing else can: whether friction is in fact
noticed on load-bearing use rather than by audit, and how the corpus's mode-of-
acquisition mix drifts over time as read and reasoned claims accumulate faster
than operated ones.

### 7. Work transition

One per change to a work item, and one per recorded conclusion
(`13-work-record.md`).

MUST carry: `work_item_ref`, the transition, the realizing operation, the
proposing `invocation_id`, and — for a conclusion — the verdict with its
reasoning.

`answered`, `blocked` and `declined` MUST stay distinct. Milestone 5 recorded an
orchestrator collapsing "the task rests on a false premise" and "I cannot find a
next step" into one generic outcome, losing a distinction the simpler Milestone 4
arms had made.

A **scope change** is a work transition and MUST be recorded as one. An audit needs
to *see* a mandate widened mid-task rather than find it silently already true, and
a re-derivation after a refinement is indistinguishable from a widening unless the
history separates them.

### 8. Conditions in force

One record per **stretch** of history rather than one per event: emitted when a
run starts and whenever any of it changes. Every other record carries a
`conditions_ref` into it.

MUST carry: which **recall policy**, which **model identity**, and which
**configuration / generation** were operating.

This is not metadata for tidiness. The record a system accumulates is a **product
of that system**, so a later comparison between policies is never against a
neutral corpus and needs to know which lineage it is reading.
`10-foundations/03` makes the same point about a single claim under the name
**scope** — the domain it was born into cannot be recovered afterwards, only
recorded near the time. The corpus has a scope in that sense, and this is where it
is written down.

## Human correction

Where a human corrects, overrides, or annotates during or after a run, that MUST
be recordable and linked to the invocation or operation it concerns. Its structure
is an open contract.

Note that a human's contribution enters as an **observation** — the operator
stated something, at a time, in a context — while what the statement *carries* may
be an observation, a finding, or a decision. The record must not collapse the two.

## Authority

This is a specification document; it has no runtime authority. Normative force is
on any conforming recorder: it MUST emit the eight kinds with the mandatory
fields, MUST preserve per-run total order, MUST keep the safety-intervention
category distinct, MUST include reads in the ordered operation history, and MUST
NOT reduce that history to a form that only supports one-operation-at-a-time
review.

## Failure modes

- **Silent gap.** A realized operation with no record. Reconstruction under-counts
  behaviour and the gate's sequence view has holes. The recorder MUST fail loudly
  — halt the run, or mark it non-reconstructable — rather than proceed with an
  unrecorded operation.
- **Effects-only history.** Recording typed effects and omitting reads leaves the
  gate able to see the carrying step with nothing of what filled it, which is the
  half that decides whether the step mattered.
- **Category collapse.** A safety intervention recorded as generic failure invites
  retry-past-refusal.
- **Lineage break.** A dangling or missing `parent_invocation_id` breaks
  per-intent reconstruction; MUST be detectable.
- **Per-invocation context record.** One `context_ref` in place of per-turn
  records makes the run look like it had a fixed input, and destroys the policy
  comparison.
- **Prose where fields are required.** A knowledge-state transition or a conclusion
  recorded as narration does not join and does not aggregate. Re-derived
  independently at M2 and M5.
- **Missing conditions.** A corpus whose conditions were never recorded cannot be
  compared against anything, and the loss is unrecoverable: which policy or model
  produced a stretch of history is not inferable from the history.
- **Unresolvable reference.** A reference that cannot be resolved within the
  retention window makes the run partially unreconstructable; MUST be reported,
  not hidden.

## Two diagnostics this makes possible

`00-design/22-arch-cognition/05-curation.md` names two failure modes for which it
proposes no detector. Recording greedily supplies material for both, which is a
reason for the greed beyond general caution. Neither is a mechanism — they are
stated so the material is not discarded before anyone tries.

- **A sweep that took something needed.** The evidence went with it — but only from
  `12-knowledge-model.md`. It is still here. A later pass can ask whether anything
  swept was subsequently searched for, re-fetched, or re-derived, which is exactly
  the signal that reachability cut too early.
- **A curator that has stopped discriminating.** Over-generous remembrance grows
  the store without corrupting it and produces an absence rather than an error. The
  ratio of registered observations to remembered ones, tracked over time, is a
  drift signal computable from nothing else.

## Relationships

- **Effect vocabulary** (`01-effect-vocabulary.md`) — supplies the `type` domain
  and shares the four-property carrier open contract.
- **Enforcement gate** (`04-enforcement-gate.md`) — consumes the ordered operation
  history and emits kind-3 records. Owns sequence-window semantics.
- **Capability and authority model** (`03-capability-authority-model.md`) — a
  capability rejection and a conformance verdict are both kind-4 dispositions; the
  policy lives there.
- **Knowledge model** (`12-knowledge-model.md`) — holds current state; this holds
  the history of how it was reached, and the entries the sweep removed.
- **Work record** (`13-work-record.md`) — supplies work transitions and recorded
  conclusions.
- **Context manager** (`14-context-manager.md`) — supplies per-turn turn inputs
  and live-set transitions.
- **Runtime** (`20-arch-runtime.md`) — emits all eight kinds as a side effect of
  doing its job; recording is runtime bookkeeping, not a cognitive action.

### Why this keeps its own copy

This store keeps its own copy rather than reading the knowledge model's graph, the
live record, or the work items directly. Those three have different lifecycles: a
claim persists as curated memory, a live entry persists only while its discussion
needs it, a work item persists until the work is done and then stops changing.
None of their retention needs match a full historical log's, and a greedy log's
needs least of all.

The sweep sharpens this rather than softening it. A swept entry stops being
something the system knows and stops being available to reason from, while
remaining reconstructable here. Reasoning and auditing are different uses, and
this store is what makes the sweep safe to perform at all.

### Which copy is authoritative

Keeping copies raises a question the set had not answered: when this store and an
owning store disagree about the same fact, which one is right.

**Each store is authoritative in its own domain.** `13-work-record.md` is
authoritative for what the work currently is, `12-knowledge-model.md` for what the
project currently holds, `14-context-manager.md` for what is currently live. On any
fact that also lives in one of those, this store is a **witness** rather than the
source, and the owning store wins.

**A disagreement is itself a defect and MUST be reported.** Both copies are written
by the runtime while realizing one operation, so drift means a partial write rather
than a difference of opinion. Neither copy should be quietly preferred without the
condition being surfaced.

**The exception is temporal rather than a matter of trust.** Once the sweep has
removed an entry, or a work item's retention has ended, this store's copy is the
only one left. It is not a witness to anything at that point — it is the record.
Nothing changes about its accuracy; what changes is that there is no longer an
owning store to defer to.

That is also why this store's retention is greedy while the others' is not. A
witness that expires before what it witnessed is useless, and the whole argument for
performing the sweep at all is that this store outlives it.

## Open contracts

- **Storage shape.** JSONL-per-run, one growing event log, or a small embedded DB?
  Deferred until volume and query patterns are real. Illustrative default: one
  JSONL file per run under a results tree.
- **The four-property carrier.** Shared with `01-effect-vocabulary.md`: one common
  envelope across all nine effect types, or per-type shapes?
- **What a knowledge-state transition looks like as a structured record.** Required
  to be fields rather than prose; the fields are not fixed.
  `12-knowledge-model.md`'s write-time tag question is adjacent and probably
  answered by the same work.
- **Turn-input content versus reference.** Whether a kind-5 record holds what was
  presented, or a reference plus the policy decision that produced it. The second
  is far smaller and reconstructs the first **only if the live set's own history is
  complete** — which it is here, and is not in `12-knowledge-model.md` after the
  sweep.
- **Retention and tiering.** Full-token retention forever is not a long-term
  position. What is the forensic window, and what is the summarised long-term form?
- **Redaction.** Secrets, personal data, and large blobs — redact at capture, at
  read, or tier into a restricted store?
- **Hypothesis linkage.** Records must be relatable to hypotheses. A `tags` /
  `experiment_id` field on the run, a separate experiment-registry join, or
  something richer?
- **Structured outcome on the operation envelope** *(findings 3, 6)*. Reconstruction
  answered unplanned questions **only where the envelope carried structured outcome
  rather than prose**. Does the envelope gain a required `verdict` and
  `terminal_reason`, are they per-type, and what is the closed set of values?
- **Source as an axis across record kinds** *(`10-foundations/03`)*. Is source a
  field on every record, a property of the actor, or a distinct kind — and how does
  it interact with findings, which may be **negative**?
- **Objective signals.** Are they realized-operation results (type 2, process
  execution) or their own kind?
- **Sequence-evaluation interface.** The exact query the gate issues against the
  ordered history. This document guarantees the history exists and is per-actor and
  per-intent queryable; the query contract is not written.
- **Clock and ordering.** Per-run monotonic sequence is required; is a global
  cross-run ordering ever needed, for concurrent runs sharing a workspace?
- **Run boundaries.** What starts and ends a run when work spans sessions, or when
  one intent spawns long-lived background activity?
