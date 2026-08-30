# Execution Cadence

## TL;DR

Three activities could each run ahead of the others: writing specification, writing code, and advancing the milestone sequence. They should not. The milestone is the unit of progress, and it pulls the other two.

> **Motto:** The milestone pulls the work; spec and dev do not push it.

## Three tracks, one pace

**Specification is just-in-time.** Write only the contracts the current milestone and the next one need. Everything not yet decidable is parked as an open contract, using the mechanism the specification conventions already define. Specification that runs ahead of the milestone sequence is speculative — it is the documentation-set equivalent of evolving by taste rather than evidence.

**Development is thin.** Boring, stable, observable, and scoped to the current milestone. Do not build for milestones not yet reached. Observability is the one exception to "only what the current milestone needs": it is a research requirement, not an operational nicety, and it is deliberately placed early in the sequence for that reason.

**Milestone progress is the pace-setter.** A milestone is done when its evidence question is answered — or is shown to be unanswerable with current machinery, which is itself a finding worth recording. Completed code is not the criterion.

One-line loop: **spec the next milestone, build it thin, answer its evidence question, record the finding, update design first, repeat.**

## The specification backlog is the milestone sequence

There is no standalone specification roadmap to maintain. The backlog is always "the contracts the next one or two milestones need," and its order falls out of the milestone order.

A specification document must not exist for a milestone beyond *current plus one*. If a later milestone's contract seems urgent to write, that urgency is a signal to record an open contract, not to spec ahead.

## What "done" means for a milestone

Each milestone carries an explicit evidence question. The milestone is complete when that question has an answer supported by a reconstructable run, or when the attempt establishes that the question cannot yet be answered and why.

This restates the progress criterion from the project-management principles in operational terms: a milestone is valuable when it reduces uncertainty, and "reduces uncertainty" is made concrete by the evidence question.

## The feedback flow

Findings flow in one direction, in this order:

1. **Design first.** A finding that bears on a concept updates the design document, preserving the historical rationale rather than overwriting it, per the revision policy.
2. **Then specification.** The corresponding open contracts are revisited. A finding may close one, reopen one, or add one.
3. **Then the sequence.** Milestone reordering happens only at a scheduled rework point — not continuously. The exception is a finding that invalidates a foundational constraint, which is handled immediately.

The concrete artifact carrying findings is the findings log in the roadmap space. One entry per completed milestone.

Task-level decomposition and execution state are tracked separately, in the `PROGRESS` folder, which changes continuously and is not part of the design set.

## Scheduled sequence rework

The milestone sequence is reworked in batches, not continuously, so that findings accumulate into a coherent revision rather than causing drift.

The first rework batch happens after the MVP slice — end of Milestone 5 — produces its findings. A second happens near the literal midpoint of the sequence. Between those points, ad-hoc reordering is discouraged; a finding that seems to demand it is recorded and left for the batch unless it touches a foundational constraint.

## The MVP slice

The minimum viable product is Milestones 0 through 5: a local assistant on measured hardware, fully observable, sitting on a safety floor, that decomposes work across ephemeral role-specific processors coordinated by a language-model orchestrator.

It is chosen to be the smallest slice that is independently useful *and* tests three core hypotheses at once — that orchestration compensates for model limits, that ephemeral roles improve reasoning quality, and that natural-language coordination can outperform a fixed workflow. The end-of-Milestone-5 findings batch is therefore the first substantial feedback into design.

### Crossing Milestone 3 for the MVP

Milestone 3, the invariant floor, is crossed in reduced form for the MVP. It is not considered complete until the deferred items land.

In scope for the MVP:

- the effect vocabulary;
- the capability and authority model;
- a hardcoded deny-list enforcement gate;
- a small, provisional, human-authored invariant list;
- a human supervising every run.

Deferred, still owed before Milestone 3 is complete, none blocking the MVP:

- composition and sequence-check hardening of the gate;
- the whole of Milestone 9 — triage role, decommissioning as a distinct non-retryable signal, escalating-alert thresholds, and the literature-grounding pass against corrigibility, scalable oversight, specification gaming, and interruptibility work (moved here from the M3-completion checklist so the whole safety-response elaboration lands together).

Milestone 9 is genuinely not needed through Milestone 5. There is no self-modifying loop until Milestone 10, and a human is in the loop throughout the MVP.

## Near-term specification backlog

Ordered by the milestone that needs each. Every document traces to the design documents it specifies.

1. **Observability event model** — Milestone 2. A v0 with many open contracts, since the schema is expected to emerge from the first experiments. Must pin invocation identity, the realized-effect record, the distinct safety-intervention outcome category, and per-actor and per-intent sequence reconstructability.
2. **Capability and authority model** — Milestone 3. The actor-and-policy dimension the effect vocabulary deliberately omits. Unblocks the gate.
3. **Enforcement gate** — Milestone 3. The minimal deny-list form: where it sits relative to the runtime, reject versus gate, and a stubbed sequence-evaluation hook.
4. **Provisional invariant list** — Milestone 3. The concrete, checkable list itself, as a normative artifact in the specification set. Small, and explicitly provisional pending the literature pass.
5. **Processor contract** — Milestone 4. Role-definition structure, objective, the processor input and output envelope, and lifecycle; detail on the processor-invocation effect.
6. **Naive context assembly** — Milestone 4. Deliberately simple, specified as a v0 expected to be replaced, and the measurable baseline for Milestone 7.
7. **Orchestrator contract** — Milestone 5. Responsibility, what it receives while itself under context governance, what it decides, discussion mediation, synthesis, and stopping rules.
8. **Orchestrator and runtime boundary** — Milestone 5. The seam the next-conceptual-pass note flags as highest value, and the reasoning-versus-runtime open question about validation depth.

Milestones 0 and 1 need no contract documents — at most a measurement protocol and an environment manifest, which belong with their milestone deliverables rather than in the specification set.
