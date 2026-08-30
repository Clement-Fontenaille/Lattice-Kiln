# Project Milestones

## TL;DR

The milestones are ordered to create evidence before adding abstraction, and to put a non-negotiable floor beneath the system before any part of it can adapt itself.

> **Motto:** Every phase should make the next design decision easier.

## Status of this sequence

This sequence is provisional and expected to be reworked in batches rather than continuously. The first rework happens after the MVP slice — end of Milestone 5 — produces its findings; a second happens near the literal midpoint of the sequence. Between those points, a finding that seems to demand reordering is recorded in the findings log and left for the batch, unless it invalidates a foundational constraint.

Its near-term entries — roughly through the first adaptive loop — are firm enough to plan against. Its later entries are deliberately loose. They name an intended direction and the question each phase should answer, not a committed design.

The sequence also serves a second purpose. Laying the concepts out in execution order is a test of whether they articulate: whether each one can be built from the evidence and machinery the previous ones produce. Where a milestone cannot be stated without assuming something no earlier milestone delivers, that is a conceptual gap to record rather than an ordering to force.

Milestones 0 through 5 are the MVP slice. Each carries an explicit evidence question, and completing it means answering that question from a reconstructable run — or establishing that it cannot yet be answered, and why. The execution-cadence document describes how those findings feed back. Later milestones will gain evidence questions as they come into focus.

## Milestone 0 — Characterize the local inference envelope

The project first needs a factual understanding of what the current machine can run comfortably.

The outcome should describe usable models, quantization choices, context sizes, model-switching cost, inference latency, GPU/CPU split, and the practical effect of running inference alongside the development environment.

This milestone exists to prevent later architectural assumptions from depending on hardware behavior we have not measured.

**Evidence question:** what is the real local inference envelope, and how tight is the constraint the constrained-intelligence thesis assumes?

## Milestone 1 — Reproducible baseline development environment

Create the scripted Windows/WSL/local-model/VS Code/Cline development environment.

The baseline should be intentionally boring, stable, and observable.

Its job is to provide a known reference installation that later generations can improve upon.

**Evidence question:** can the baseline be reconstructed from scripts without manual repair, and where does reproducibility actually break?

## Milestone 2 — Observability foundation

Ensure that important AI-assisted work can be reconstructed well enough for later analysis.

This should include invocation identity, model and configuration, context, outputs, tool activity, repository effects, objective verification, and human correction where available.

Three requirements are load-bearing and should not be traded away for a simpler format:

- Reconstruction must be good enough to detect composed and drifting behavior across sequences of effects, not only to review effects one at a time.
- The event model must be able to represent a safety intervention as an outcome category distinct from ordinary task failure — traceable, and not eligible for automatic retry without human review.
- Recorded behavior must be relatable to hypotheses about the system, not only to a narrative of what happened.

The storage format can stay simple. What must be reconstructable cannot.

**Evidence question:** can a run be reconstructed well enough to answer a question we have not thought to ask yet?

## Milestone 3 — The invariant floor

The first thing that must exist before any component acts with authority to cause effects.

Deliverables:

- A first human-authored invariant list: goals, resource ceilings, and hard constraints — specific enough to check, small enough to stay stable.
- A literature-grounding pass against work on corrigibility, scalable oversight, specification gaming, and shutdown and interruptibility, before that list and its enforcement are treated as settled.
- The effect vocabulary: the closed set of effect types the runtime can produce, since the gate binds to it.
- A minimal deterministic enforcement gate that checks proposed effects and effect sequences against the invariant list and refuses those that cross it.
- The capability and authority model, sitting above the gate.

This milestone is placed early on purpose. The rest of the architecture defers many decisions to evidence, and that deferral is only safe with this floor in place. The elaboration of the safety response — triage, decommissioning signal, escalation thresholds — is deferred to Milestone 9, once there are adaptive loops for it to watch and mature observability for it to run against.

For the MVP slice this milestone is crossed in a reduced form — effect vocabulary, capability model, a deny-list gate, a provisional invariant list, and a human supervising every run — with the literature-grounding pass and the sequence-check hardening still owed before it counts as complete. The execution-cadence document details what is in and out.

**Evidence question:** do the enumerated effect types carve cleanly when real effects flow through the gate, or does the boundary between types blur under use?

## Milestone 4 — Ephemeral processor experiments

Introduce independent role-specific invocations outside a monolithic coding conversation.

Use a small set of roles only, to learn whether role separation, fresh context, independent assessment, and adversarial review provide practical value.

Processors receive deliberately naive context assembly at this stage — some unglamorous, possibly poor, default. Its job is to be a measurable baseline, not to be good.

**Evidence question:** do ephemeral roles, fresh context, and independent review beat a monolithic agent on a small task set?

## Milestone 5 — Intelligent orchestration experiments

Introduce an LLM-based orchestrator capable of deciding which cognitive operation appears useful next.

The main objective is not autonomy. It is to study whether natural-language coordination outperforms a fixed workflow while remaining understandable.

**Evidence question:** does natural-language orchestration beat a fixed workflow while staying understandable, and where does its overhead start to exceed the benefit of decomposition?

## Milestone 6 — Persistent work and knowledge

Add enough durable structure for ephemeral processors to cooperate across time.

Intent, work, observations, evidence, findings, proposals, decisions, artifacts, and memory should be represented only as far as necessary to support real use cases.

## Milestone 7 — Context governance measurement

The goal is not to design good context governance. It is to establish the naive default from Milestone 4 as a measurable baseline, and to develop metrics for context quality that are independent of final task success.

Without those metrics, a later decision to commission a context-curator role cannot be made on evidence. This milestone produces the evidence base; it does not pick the mechanism.

## Milestone 8 — Project-level adaptation

Use observed project work to improve project-local knowledge.

The key test is whether later work in the same repository improves without polluting global system behavior.

This is a scope of feedback, not a new kind of agent. The same holds for Milestones 10 and 12: the levels differ in scope, evidence, and promotion criteria — not necessarily in which processor performs them.

## Milestone 9 — Safety response mechanisms

The elaboration of the floor from Milestone 3, required before any loop can modify the system itself.

Deliverables:

- A triage role that assesses a tripped gate and routes: log and let the original gated effect proceed unchanged, escalate, or halt. It may never grant an exception the gate refused.
- Decommissioning as an immediate, unilateral runtime action, and as a failure signal distinct from ordinary task failure — not eligible for automatic retry without human review.
- An escalating-alert threshold that converts accumulated, individually innocuous trips into a mandatory stop no loop can reason past.
- The triage role fixed outside the feedback loops, since a loop cannot commission its own watcher.

## Milestone 10 — System-level candidate tuning

Use recurring evidence across tasks or projects to propose changes to processors, orchestration, context policy, and evaluation behavior.

Valid categories of change include processor definitions, orchestrator instructions, delegation behavior, context policy, review and evaluation strategy — and proposing a processor role that does not yet exist.

Role commissioning likely carries a higher evidence bar than role tuning; establishing that threshold is part of this milestone.

Changes remain candidates until independently evaluated.

## Milestone 11 — Reproducible generations and promotion

Define trusted system generations, lineage, candidate variants, promotion, rejection, rollback, and bootstrap reconstruction.

At this point the system itself becomes an experimental artifact.

## Milestone 12 — Meta-evaluation

Introduce explicit evaluation of the improvement process.

Measure whether benchmarks, promotion criteria, and feedback mechanisms actually distinguish transferable improvements from local or metric-specific gains.

This level is bounded by construction: it asks one generic question about whether self-tuning produces trustworthy improvement, not a meta-question per parameter, and it terminates on the invariant layer and frozen baselines as non-self-tuned anchors.

## Milestone 13 — Cross-generation comparison

Compare models, strategies, and system generations under controlled conditions.

Per-role model assignment — which model plans, which implements, which evaluates — is one of the dimensions compared here. Whether two models are independent enough to provide genuine adversarial evaluation, rather than merely correlated judgment, is a question this milestone can begin to answer.

Use this milestone to decide whether the project is producing cumulative system capability rather than merely increasing architectural complexity.

## Milestone 14 — Bootstrap generation closure

Promoted system generations should produce reproducible bootstrap artifacts.

A fresh instance should inherit validated system-level learning without replaying the full history that discovered it.
