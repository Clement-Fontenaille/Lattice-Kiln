# Deterministic Runtime

## TL;DR

The runtime is the substrate that preserves reality, limits effects, records history, and makes experiments reproducible.

> **Motto:** Flexible cognition requires a stable world.

## Architecture map

This document is the entry point into the architecture space: runtime sits underneath every other concern here, since it is what actually executes what any of them propose.

- [`21-arch-knowledge-model/`](21-arch-knowledge-model/01-knowledge-model.md) — `10-foundations/03`'s substrate, realized.
- [`22-arch-cognition/`](22-arch-cognition/01-work-intent-and-task-model.md) — the reasoning and coordinating actors: task representation, processors, the orchestrator, decomposition.
- [`23-arch-context-management/`](23-arch-context-management/01-context-manager.md) — `10-foundations/04`'s account, realized.
- [`24-arch-permission-layer/`](24-arch-permission-layer/01-capabilities-and-authority.md) — what an actor may request.
- [`25-arch-invariant-layer/`](25-arch-invariant-layer/01-invariant-enforcement.md) — what may never happen, regardless of what any actor requests.
- [`26-arch-observability/`](26-arch-observability/01-observability.md) — what has to be reconstructable after the fact.
- [`27-arch-adaptation-and-evolution/`](27-arch-adaptation-and-evolution/) — feedback, evaluation, generations, bootstrap.
- [`28-arch-work-record/`](28-arch-work-record/01-work-record.md) — intent and the work derived from it, held durably.

Split out of a single `20-cognitive-architecture/` folder on 2026-09-11: only `22` holds actors that reason or coordinate anything; the rest are resources or constraints those actors operate with, on, or under. `28` was added the same day, once consolidation found that `22-arch-cognition/01`'s work model had no actor holding it; its number is higher than `27`'s for no reason beyond the lower ones being taken.

## Motivation

The AI layers need freedom to reason, but the system must retain an authoritative record of what actually happened.

The runtime provides that authority.

## Expected responsibilities

What the runtime decides for itself is narrow: it invokes processors, exposes tools, executes the calls and effects a cognitive component proposes, isolates experiments, manages resources, and supports rollback or reconstruction when practical.

Several responsibilities this document once listed as the runtime's own now have owners elsewhere in this band. The runtime is where they become real, which is not the same as deciding them:

- **Capability boundaries** are described by `24-arch-permission-layer`. The policy is theirs; the enforcement point is here.
- **The invariant check** is specified by `25-arch-invariant-layer`. Where the gate sits relative to this document is deliberately left open, below.
- **What gets recorded** is `26-arch-observability`'s to define. The runtime emits it.
- **Persisted state** has several owners: `21-arch-knowledge-model` holds claims, `23-arch-context-management` the live record, `28-arch-work-record` intent and work items, `26-arch-observability` its own history. The runtime persists whatever their writes resolve to without owning what any of them decided to write.

Keeping that distinction sharp is what stops the runtime from becoming the place every unowned concern quietly lands.

## The path an invocation takes

Each document in this band names its own edges and none of them draws the sequence. It is stated once here so those edges can be checked against each other.

**Instantiation.** The orchestrator (`22-arch-cognition/03`) reads current work state from `28-arch-work-record`, decides a processor is needed, and formulates its role and objective. Instantiating it is itself an effect — processor invocation, `10-technical/01-effect-vocabulary.md` type 6 — so it is proposed, gated, and realized like anything else. Realizing it binds four things into a running instance: the role definition, the objective, a capability set under `24-arch-permission-layer`'s policy, and a context bundle from `23-arch-context-management`. The runtime is what requests that bundle. Neither the orchestrator nor the instance being created asks for it, which is what keeps the orchestrator's "it does not govern its own context" true in the case where the instance being invoked is the orchestrator itself.

**Action.** The instance reasons and proposes. A read — a file, a knowledge-model query — is not an effect (`10-technical/01`, What is not an effect); it may still be capability-gated, and the runtime executes it either way. An effect is checked against current policy (`24`), then against the invariant gate (`25`), and only then realized.

**Recording.** Whatever comes back — a read's content, an effect's outcome, or the model's own generated output — is registered by `23-arch-context-management` into the live record. Separately, `26-arch-observability` records the event into its own history. These are two writes into two stores, not one write read twice, for the retention reasons `26` gives.

Two of the effect types resolve into a third and fourth store as well: a claim to `21-arch-knowledge-model`, a work-record mutation — including the instance's own recorded conclusion of answered, blocked, or declined — to `28-arch-work-record`. Four stores, each with its own retention discipline, is the deliberate shape rather than an accident of how this was assembled.

The runtime should make all of this observable enough for later feedback analysis.

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
