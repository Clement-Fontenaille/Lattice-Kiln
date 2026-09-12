# Deterministic Runtime

## TL;DR

The runtime is the substrate that preserves reality, limits effects, emits the record, and makes experiments reproducible.

> **Motto:** Flexible cognition requires a stable world.

## Architecture map

This document is the entry point into the architecture space: runtime sits underneath every other concern here, since it is what actually executes what any of them propose.

- [`21-arch-knowledge-model/`](21-arch-knowledge-model/01-knowledge-model.md) — `10-foundations/03`'s substrate, realized.
- [`22-arch-cognition/`](22-arch-cognition/01-work-intent-and-task-model.md) — the reasoning and coordinating actors: task representation, processors, the orchestrator, thinking, decomposition.
- [`23-arch-context-management/`](23-arch-context-management/01-context-manager.md) — `10-foundations/04`'s account, realized.
- [`24-arch-permission-layer/`](24-arch-permission-layer/01-capabilities-and-authority.md) — the model for what an actor may request; the policy is configuration, the engine is `25`'s.
- [`25-arch-invariant-layer/`](25-arch-invariant-layer/01-invariant-enforcement.md) — the mechanisms no loop may adjust: the gate, which is the floor, plus triage, the scope check, and the capability engine.
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

- **Capability boundaries** are described by `24-arch-permission-layer` as a model, and the policy content is configuration that feedback revises. The engine applying them is one of `25-arch-invariant-layer`'s non-adjustable mechanisms rather than this document's, for the reason that layer gives: an engine a loop could route around would gate nothing.
- **The invariant check** is specified by `25-arch-invariant-layer`. Where the gate sits relative to this document is deliberately left open, below.
- **What gets recorded** is `26-arch-observability`'s to define. The runtime emits it.
- **Persisted state** has several owners: `21-arch-knowledge-model` holds claims, `23-arch-context-management` the live record, `28-arch-work-record` intent and work items, `26-arch-observability` its own history. The runtime persists whatever their writes resolve to without owning what any of them decided to write.

Keeping that distinction sharp is what stops the runtime from becoming the place every unowned concern quietly lands.

## Instantiation, and then a loop

Each document in this band names its own edges and none of them draws the sequence. It is stated once here so those edges can be checked against each other.

There is no assembly step. Context is not gathered, packaged, and handed to a processor at the moment it starts. That shape belongs to `10-technical/07-naive-context-assembly.md`, which is one-shot by its own account and has no recall in any real sense, and it is the shape this band has moved off. What replaces it is a loop, with `23-arch-context-management` sitting inside it rather than being consulted before it.

**Instantiation happens once.** The orchestrator (`22-arch-cognition/03`) reads current work state from `28-arch-work-record`, decides a processor is needed, and formulates its role and objective. Instantiating it is itself an effect — processor invocation, `10-technical/01-effect-vocabulary.md` type 6 — so it is proposed, gated, and realized like anything else.

What gets bound is only what can be fixed in advance: role instructions, an objective, a capability set under `24-arch-permission-layer`'s policy, and a **scope** — the mandate the work is to stay within, inherited from the work item and narrowable but never wider. Context is not among them, because context is not the kind of thing that can be bound. What the instance gets instead is an identity: a live set, which its own crossings register into and which recall runs over each time it is fed.

The scope is static for the life of the instance (`24-arch-permission-layer`, An instance's scope is static). An instance that finds it needs to reach further stops and reports rather than extending itself, and a mid-task widening of the work item reaches the next invocation rather than this one.

**Then, on every turn, the turn input is composed.** `23-arch-context-management` renders it at the moment of feeding, out of what is in the live set and under the recall policy. Not once at the start: every turn, over a live set that has changed since the last one.

Nothing requests this, which is why the question of who asks for a processor's context has no answer — nothing asks. Everything moving to or from the model passes through this actor by construction, so it is traversed, not called. That is also what keeps the orchestrator's "it does not govern its own context" (`22-arch-cognition/03`) true without needing anyone else to fetch on its behalf.

**The model acts.** An effect is checked against current policy (`24`), then against the invariant gate (`25`), and only then realized.

A read of something already inside the workspace — a file, a prior observation, a knowledge-model query — is not a typed effect, and not because it leaves the world untouched. It does not: it leaves an access record, makes a store do work and compete for its capacity, spends any quota the source meters, and is sometimes a state transition in its own right. `10-foundations/02`'s 2026-09-11 Qualification withdraws that basis, and `25-arch-invariant-layer` states what replaces it — the gate's input domain is runtime-mediated operations, and the typed-effect vocabulary is the subset whose **footprint** this project has chosen to name and track. Footprint is a gradient; membership is a judgment about where tracking pays.

So a read takes a shorter path by default, not by construction. The default is permissive — reads pass unless a rule names them — and that is a configuration the system may change, rather than a capability the architecture has removed. This is also why the runtime's own classification work below is ordinary and not a special case: distinguishing a destructive filesystem action from a read-only inspection is a judgment about footprint, which is the same axis everything else on this path sits on.

**What comes back crosses in.** The result of the call, or the model's own generated output, is registered by `23-arch-context-management` into the live set, and the next turn composes over what the live set now holds. Compose, act, register, compose again — that is the whole loop, and its state lives in the live set rather than in anything handed between steps.

The live set does not only grow. It tracks what is in context, so items leave it as well as enter: something not recalled after a cache reset has left the discussion and drops out (`23-arch-context-management`, What leaves the live set). Bringing such an item back is a retrieval rather than a recall, which means it re-enters through the same path as anything else — a crossing, gated and registered. The loop is therefore not an accumulation, and nothing in it is monotonic.

Alongside it, writes land elsewhere, each into its own store with its own retention discipline: `26-arch-observability` records the event, a claim resolves to `21-arch-knowledge-model`, and a work-record mutation — including the instance's own recorded conclusion of answered, blocked, or declined — resolves to `28-arch-work-record`. None of these is the same write read several times.

The runtime should make all of this observable enough for later feedback analysis.

## What instantiation does not settle

What is in an instance's live set at the moment it starts is open, and dropping the bundle is what exposes it: a bundle made the question look answered, since a bundle is by definition what an instance begins with.

The mechanics tighten it further. A live set is populated by registration, and registration records what a crossing returned — so at turn zero, before anything has crossed, a live set is empty by construction. Anything an instance "inherits" therefore has to arrive one of two ways, and `23-arch-context-management` owns the choice between them. Either inheritance is a new operation, in which case already-registered artifacts move or are referenced across live sets without any crossing having occurred, which is neither register nor recall and would be a third primitive. Or a live set genuinely starts empty and inheritance is an ordinary crossing: the preceding step wrote a handoff somewhere durable, and the new instance reads it like anything else.

The second needs no new mechanism and has somewhere to live already — a handoff is an attachment on a work item (`28-arch-work-record`), read like any other read. That is the cheaper hypothesis, not yet an adopted position.

This is a context-management question and not a decomposition one. How split work recombines (`22-arch-cognition/08`, fork/join or continuation) constrains whether sibling instances see each other's crossings, which is live-set isolation. It does not constrain how much any one live set starts with: fork/join runs perfectly well with richly seeded branches, and continuation runs perfectly well handing forward almost nothing. The two questions are orthogonal and should not be settled together.

## What the runtime should avoid

The runtime should not become a hidden cognitive workflow engine.

It should not decide that every work item must pass through predetermined phases simply because those phases were useful in early experiments.

Operational constraints belong here. Cognitive strategy generally does not.

## Mechanical intelligence

Some runtime decisions may require semantic classification at an operational level, such as distinguishing a destructive filesystem action from a read-only repository inspection.

This does not require the runtime to understand the project's broader intent.

## Relationship to invariant enforcement

Invariant enforcement is specified separately from the runtime's ordinary responsibilities, because it answers a different question. The runtime asks whether a requested effect is representable, permitted under current policy, attributable, and reversible **where required**. The invariant gate asks whether the effect is permissible at all, and its answer is not adjustable by anything inside the system.

That qualifier is load-bearing and this document used to drop it. `10-foundations/02` concedes what has to be conceded: some effects are irreversible by nature, that is what was asked for rather than an accident of execution, and refusing them on reversibility grounds alone would be refusing the work. What such an effect needs instead is a judgment of whether it is worth what it forecloses — and that judgment is neither of the two checks here. It belongs to `22-arch-cognition/04-thinking.md` and runs **upstream of the proposal**, while the effect is being formed, rather than as a stage in this path. `25-arch-invariant-layer` sets out why: a judgment stage inside the enforcement path would be a reasoning component sitting in that path, which is the persuadable mechanism the gate exists to exclude.

So the runtime never asks whether an effect was well-considered, and must not learn to. An irreversible effect that passes is permitted, not endorsed.

The two are closely related in practice. Both are deterministic, both operate on effects, and both sit outside cognition. Whether the gate is best understood as a component of the runtime or as a layer the runtime is itself subordinate to is deliberately left open.

What separates them is adjustability. The runtime is legitimately configurable as the system learns which operational policies work, and that is exactly why it cannot serve as the floor. A mechanism the system can tune is not a mechanism that constrains the system's tuning.

## Open question

The practical boundary between runtime policy and AI-mediated policy remains one of the most important implementation questions and should be approached conservatively at first.

What a read's permissive default should actually be, now that the framework is required to permit gating one. "Reads pass unless a rule names them" fixes the shape and leaves the content open, including at what granularity a rule may name a class of reads — by path, by crossing type, by volume against a ceiling, or something else. `10-foundations/02`'s own Open question holds the same item from the foundational side.

Whether footprint admits a measure the gate can actually apply. It is now what separates a read from a typed effect, and a gradient nothing can quantify is not obviously better than a binary that was at least checkable. `10-foundations/02`'s Open question holds the same item and names the partial candidates already in this set — volume against a ceiling, reversibility class, quota consumed — none of which is known to compose with the others.

Whether a read stays outside the typed-effect vocabulary permanently, or eventually earns a type of its own. The Qualification keeps reads out of the vocabulary and inside the gate's domain, which settles the capability question and leaves the representation one open.
