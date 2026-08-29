# Project Milestones

## TL;DR

The milestones are ordered to create evidence before adding abstraction.

> **Motto:** Every phase should make the next design decision easier.

## Milestone 0 — Characterize the local inference envelope

The project first needs a factual understanding of what the current machine can run comfortably.

The outcome should describe usable models, quantization choices, context sizes, model-switching cost, inference latency, GPU/CPU split, and the practical effect of running inference alongside the development environment.

This milestone exists to prevent later architectural assumptions from depending on hardware behavior we have not measured.

## Milestone 1 — Reproducible baseline development environment

Create the scripted Windows/WSL/local-model/VS Code/Cline development environment.

The baseline should be intentionally boring, stable, and observable.

Its job is to provide a known reference installation that later generations can improve upon.

## Milestone 2 — Observability foundation

Ensure that important AI-assisted work can be reconstructed well enough for later analysis.

This should include invocation identity, model/configuration, context, outputs, tool activity, repository effects, objective verification, and human correction where available.

The milestone should stay lightweight; the goal is useful evidence, not a perfect telemetry platform.

## Milestone 3 — Ephemeral processor experiments

Introduce independent role-specific invocations outside a monolithic coding conversation.

Use a small set of roles only to learn whether role separation, fresh context, independent assessment, and adversarial review provide practical value.

## Milestone 4 — Intelligent orchestration experiments

Introduce an LLM-based orchestrator capable of deciding which cognitive operation appears useful next.

The main objective is not autonomy. It is to study whether natural-language coordination outperforms a fixed workflow while remaining understandable.

## Milestone 5 — Persistent work and knowledge

Add enough durable structure for ephemeral processors to cooperate across time.

Intent, work, observations, evidence, findings, proposals, decisions, artifacts, and memory should be represented only as far as necessary to support real use cases.

## Milestone 6 — Context governance

Make context construction explicit and measurable.

Begin comparing strategies for file selection, knowledge retrieval, summary use, processor-requested context expansion, and context budgeting.

## Milestone 7 — Project-level adaptation

Use observed project work to improve project-local knowledge.

The key test is whether later work in the same repository improves without polluting global system behavior.

## Milestone 8 — System-level candidate tuning

Use recurring evidence across tasks or projects to propose changes to processors, orchestration, context policy, and evaluation behavior.

Changes remain candidates until independently evaluated.

## Milestone 9 — Reproducible generations and promotion

Define trusted system generations, lineage, candidate variants, promotion, rejection, rollback, and bootstrap reconstruction.

At this point the system itself becomes an experimental artifact.

## Milestone 10 — Meta-evaluation

Introduce explicit evaluation of the improvement process.

Measure whether benchmarks, promotion criteria, and feedback mechanisms actually distinguish transferable improvements from local or metric-specific gains.

## Milestone 11 — Cross-generation comparison

Compare models, strategies, and system generations under controlled conditions.

Use this milestone to decide whether the project is producing cumulative system capability rather than merely increasing architectural complexity.

## Milestone 12 — Bootstrap generation closure

Promoted system generations should produce reproducible bootstrap artifacts.

A fresh instance should inherit validated system-level learning without replaying the full history that discovered it.
