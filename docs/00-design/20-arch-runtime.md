# Deterministic Runtime

## TL;DR

The runtime is the substrate that preserves reality, limits effects, records history, and makes experiments reproducible.

> **Motto:** Flexible cognition requires a stable world.

## Architecture map

This document is the entry point into the architecture space: runtime sits underneath every other concern here, since it is what actually executes what any of them propose.

- [`21-arch-knowledge-model/`](21-arch-knowledge-model/README.md) — `10-foundations/03`'s substrate, realized.
- [`22-arch-cognition/`](22-arch-cognition/01-work-intent-and-task-model.md) — the reasoning and coordinating actors: task representation, processors, the orchestrator, decomposition.
- [`23-arch-context-management/`](23-arch-context-management/README.md) — `10-foundations/04`'s account, realized.
- [`24-arch-permission-layer/`](24-arch-permission-layer/01-capabilities-and-authority.md) — what an actor may request.
- [`25-arch-invariant-layer/`](25-arch-invariant-layer/01-invariant-enforcement.md) — what may never happen, regardless of what any actor requests.
- [`26-arch-observability/`](26-arch-observability/01-observability.md) — what has to be reconstructable after the fact.
- [`27-arch-adaptation-and-evolution/`](27-arch-adaptation-and-evolution/) — feedback, evaluation, generations, bootstrap.

Split out of a single `20-cognitive-architecture/` folder on 2026-09-11: only `22` holds actors that reason or coordinate anything; the rest are resources or constraints those actors operate with, on, or under.

## Motivation

The AI layers need freedom to reason, but the system must retain an authoritative record of what actually happened.

The runtime provides that authority.

## Expected responsibilities

The runtime invokes processors, exposes tools, applies capability boundaries, persists selected state, records observations, isolates experiments, manages resources, and supports rollback or reconstruction when practical.

The runtime should also make system behavior observable enough for later feedback analysis.

## What the runtime should avoid

The runtime should not become a hidden cognitive workflow engine.

It should not decide that every work item must pass through predetermined phases simply because those phases were useful in early experiments.

Operational constraints belong here. Cognitive strategy generally does not.

## Mechanical intelligence

Some runtime decisions may require semantic classification at an operational level, such as distinguishing a destructive filesystem action from a read-only repository inspection.

This does not require the runtime to understand the project's broader intent.

## Relationship to invariant enforcement

Invariant enforcement is specified separately from the runtime's ordinary responsibilities, because it answers a different question. The runtime asks whether a requested effect is representable, permitted under current policy, attributable, and reversible. The invariant gate asks whether the effect is permissible at all, and its answer is not adjustable by anything inside the system.

The two are closely related in practice. Both are deterministic, both operate on effects, and both sit outside cognition. Whether the gate is best understood as a component of the runtime or as a layer the runtime is itself subordinate to is deliberately left open.

What separates them is adjustability. The runtime is legitimately configurable as the system learns which operational policies work, and that is exactly why it cannot serve as the floor. A mechanism the system can tune is not a mechanism that constrains the system's tuning.

## Open question

The practical boundary between runtime policy and AI-mediated policy remains one of the most important implementation questions and should be approached conservatively at first.
