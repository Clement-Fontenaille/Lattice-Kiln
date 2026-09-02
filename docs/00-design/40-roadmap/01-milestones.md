# Project Milestones

## TL;DR

The milestones are ordered to create evidence before adding abstraction, and to put a non-negotiable floor beneath the system before any part of it can adapt itself.

> **Motto:** Every phase should make the next design decision easier.

## Status of this sequence

This sequence is provisional and reworked in batches rather than continuously.

- **Rework 1** ran at the end of the MVP slice (Milestone 5) — `40-roadmap/06-sequence-rework-01.md`. Outcome: no reordering.
- **Rework 2** ran after the M5-follow-up investigation (attractor census, judge-lab, loop-lab, super-pipeline; findings-log entry 7 and its addenda) — `40-roadmap/07-sequence-rework-02.md`. Outcome: **two milestones inserted after M5** — an evaluation task suite (M6) and a static supervised workflow (M7) — and everything from the old "Persistent work and knowledge" onward shifted down by two. The mapping table is in rework 2. References in earlier documents to "Milestone _n_" for _n_ ≥ 6 mean the pre-rework-2 number unless they post-date 2026-09-02.

Near-term entries — roughly through the first adaptive loop — are firm enough to plan against. Later entries are deliberately loose: they name an intended direction and the question each phase should answer, not a committed design.

The sequence also serves a second purpose. Laying the concepts out in execution order is a test of whether they articulate: whether each one can be built from the evidence and machinery the previous ones produce. Where a milestone cannot be stated without assuming something no earlier milestone delivers, that is a conceptual gap to record rather than an ordering to force.

Milestones 0 through 5 were the MVP slice. Each carried an explicit evidence question, and completing it meant answering that question from a reconstructable run — or establishing that it could not yet be answered, and why. Milestones 6 and 7 continue that discipline. Later milestones will gain evidence questions as they come into focus.

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
- The effect vocabulary: the closed set of effect types the runtime can produce, since the gate binds to it.
- A minimal deterministic enforcement gate that checks proposed effects and effect sequences against the invariant list and refuses those that cross it.
- The capability and authority model, sitting above the gate.

The literature-grounding pass against work on corrigibility, scalable oversight, specification gaming, and shutdown and interruptibility — before that list and its enforcement are treated as settled — is a deliverable of Milestone 11, not of this milestone. It is grouped with the rest of the safety-response elaboration rather than gating the floor's first form.

This milestone is placed early on purpose. The rest of the architecture defers many decisions to evidence, and that deferral is only safe with this floor in place. The elaboration of the safety response — triage, decommissioning signal, escalation thresholds, and the literature-grounding pass — is deferred to Milestone 11, once there are adaptive loops for it to watch and mature observability for it to run against.

For the MVP slice this milestone was crossed in a reduced form — effect vocabulary, capability model, a deny-list gate, a provisional invariant list, and a human supervising every run — with the sequence-check hardening still owed, and the literature-grounding pass folded into Milestone 11, before it counts as complete. The execution-cadence document details what is in and out.

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

A follow-up investigation (findings-log entry 7) established: a 7B does the *doing* with scaffolding but not the *judging*, no reviewer framing lifts it above an approval bias, execution grounding is the only reliable verification lever, and a cheap test-gated loop with an incumbent-protected keeper already captures most of the achievable value. That investigation is what motivated Milestones 6 and 7.

## Milestone 6 — Evaluation task suite

Everything downstream — the static workflow (M7) and every adaptive loop after it — is judged by running it against tasks. The MVP used a 4-then-6-task fixture that was too small and too synthetic to separate arms at N ≤ 3, and it missed whole classes of common request.

This milestone builds a proper suite and the conceptual treatment behind it:

- A **taxonomy of dev-request shapes** (fix, feature, refactor, perf, migration, robustness, API/contract change, dependency, cleanup) crossed with a **trap taxonomy** (misdirection, backward-compat, behaviour-preserving, edge coverage, false premise / push-back, silent-failure).
- **20–30 tasks**, each: a realistic request; a deterministic partial-credit check (behavioural subtests, plus structural scores where behaviour under-determines the deliverable); an explicit *correct vs plausible-wrong* discriminator the check enforces; a `stresses:` tag naming which pipeline capability it exercises; a `decline_correct` flag where pushing back is the right move.
- Each task ships a **pre-existing passing test** alongside the new ones, so the regression guard is exercised across the suite.
- A **conceptual document** — how the project evaluates — so later milestones consume one shared method instead of each reinventing it. This addresses the gap that the MVP's evaluation was ad hoc per experiment.

The existing `experiments/M5-intelligent-orchestration/fixture_workflow/` (wf1–wf6) is folded in as the seed; the full spec is `10-technical/10-evaluation-task-suite.md`.

**Evidence question:** does a trap-structured task suite separate pipeline variants that a toy fixture cannot, and does it surface failure modes the MVP fixture missed?

## Milestone 7 — Static supervised workflow

The M5-follow-up established the near-term deliverable: a **supervised local assistant on 7–8B**, not a self-improving loop. It also produced a **leading candidate** for the shape — but the milestone is deliberately kept open about strategy, because the evidence so far is 6 tasks at low N and the M6 suite exists precisely to test these choices at scale.

**Leading candidate (from `loop_lab` + `pipeline_lab`, findings-log entry 7):** a cheap reliable spine — test-gated iteration, incumbent-protected keeper, escalate-on-stall — with heavier stages (premise audit, concern-split + combined-score keeper, structural verification) fired **conditionally** by task class, and every stage's influence on the outcome recorded so redundant stages retire on evidence. The always-on super-pipeline was a negative result: worse-or-tied on 5/6 tasks, four stages that moved zero outcomes.

**Strategies still to explore, not foreclosed:**

- **Blind K-way test synthesis, fixed.** It was inert in the super-pipeline only because its suites crashed on an unfinished implementation before emitting a check line. A version that tolerates partial code, or runs after the first coding pass, may be the missing verifier for no-test tasks — the `ground_notest` 3/10 hole.
- **Dueling advocates with executable claims.** Two context-diverse readers (one sees only the diff, one only the pre-change file + objective) emit *falsifiable* input/output claims; the interpreter, not a third model, adjudicates. Attacks the same no-test hole from the other side.
- **Cross-model / stronger-model review.** Once a second resident model is available (the planned second GPU), the reviewer is a different model — the one intervention the judge-lab said could lift evaluation above the approval bias. This may change how much verification machinery the static workflow needs.
- **Task-type-adaptive stage selection.** The premise audit already classifies bugfix / feature / refactor / perf; the conditional-firing rules can be learned from M6 `stresses`-slice data rather than hand-set.
- **The natural-language orchestrator, reconsidered.** M5 showed its only gain was adaptive retry (already in the spine) at 5–7× cost — on toy tasks. Whether it earns its cost on the harder M6 tasks (multi-file, migration, multi-concern) is an open question the suite can now answer; it returns at minimum as a comparison arm.
- **Human-in-the-loop shape.** The escalation payload (a precise, human-answerable question rather than a dump) is itself a design surface — how the assistant asks for the one thing it cannot decide.

This milestone turns the chosen strategy into a specified, observable component on the M3 floor: the flow, the per-stage contract, the firing rules, the escalation payload, and per-stage outcome-influence observability.

**Evidence question:** on the M6 suite, which workflow strategy gives the best outcome-per-call against the plain monolith and the always-on super-pipeline, and does the chosen one degrade safely — no regressions, honest escalation — on the tasks it cannot do?

## Milestone 8 — Persistent work and knowledge

Add enough durable structure for ephemeral processors to cooperate across time.

Intent, work, observations, evidence, findings, proposals, decisions, artifacts, and memory should be represented only as far as necessary to support real use cases.

## Milestone 9 — Context governance measurement

The goal is not to design good context governance. It is to establish the naive default from Milestone 4 as a measurable baseline, and to develop metrics for context quality that are independent of final task success.

Without those metrics, a later decision to commission a context-curator role cannot be made on evidence. This milestone produces the evidence base; it does not pick the mechanism.

## Milestone 10 — Project-level adaptation

Use observed project work to improve project-local knowledge.

The key test is whether later work in the same repository improves without polluting global system behavior.

This is a scope of feedback, not a new kind of agent. The same holds for Milestones 12 and 14: the levels differ in scope, evidence, and promotion criteria — not necessarily in which processor performs them.

## Milestone 11 — Safety response mechanisms

The elaboration of the floor from Milestone 3, required before any loop can modify the system itself.

Deliverables:

- A triage role that assesses a tripped gate and routes: log and let the original gated effect proceed unchanged, escalate, or halt. It may never grant an exception the gate refused.
- Decommissioning as an immediate, unilateral runtime action, and as a failure signal distinct from ordinary task failure — not eligible for automatic retry without human review.
- An escalating-alert threshold that converts accumulated, individually innocuous trips into a mandatory stop no loop can reason past.
- The triage role fixed outside the feedback loops, since a loop cannot commission its own watcher.
- The literature-grounding pass against corrigibility, scalable oversight, specification gaming, and shutdown and interruptibility work — moved here from Milestone 3. Milestone 3's provisional invariant list and deny-list gate, and this milestone's safety-response elaboration, are all revised against what that pass finds before the floor is treated as settled.

## Milestone 12 — System-level candidate tuning

Use recurring evidence across tasks or projects to propose changes to processors, orchestration, context policy, and evaluation behavior.

Valid categories of change include processor definitions, orchestrator instructions, delegation behavior, context policy, review and evaluation strategy — and proposing a processor role that does not yet exist.

Role commissioning likely carries a higher evidence bar than role tuning; establishing that threshold is part of this milestone.

Changes remain candidates until independently evaluated.

## Milestone 13 — Reproducible generations and promotion

Define trusted system generations, lineage, candidate variants, promotion, rejection, rollback, and bootstrap reconstruction.

At this point the system itself becomes an experimental artifact.

## Milestone 14 — Meta-evaluation

Introduce explicit evaluation of the improvement process.

Measure whether benchmarks, promotion criteria, and feedback mechanisms actually distinguish transferable improvements from local or metric-specific gains.

This level is bounded by construction: it asks one generic question about whether self-tuning produces trustworthy improvement, not a meta-question per parameter, and it terminates on the invariant layer and frozen baselines as non-self-tuned anchors.

## Milestone 15 — Cross-generation comparison

Compare models, strategies, and system generations under controlled conditions.

Per-role model assignment — which model plans, which implements, which evaluates — is one of the dimensions compared here. Whether two models are independent enough to provide genuine adversarial evaluation, rather than merely correlated judgment, is a question this milestone can begin to answer.

Use this milestone to decide whether the project is producing cumulative system capability rather than merely increasing architectural complexity.

## Milestone 16 — Bootstrap generation closure

Promoted system generations should produce reproducible bootstrap artifacts.

A fresh instance should inherit validated system-level learning without replaying the full history that discovered it.
