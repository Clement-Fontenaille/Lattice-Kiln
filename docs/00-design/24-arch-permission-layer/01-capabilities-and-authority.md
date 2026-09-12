# Capabilities and Authority

## TL;DR

Knowing how to request an action is not the same as being authorized to make that action real.

> **Motto:** Capability enables proposals; authority governs effects.

## Motivation

The system needs flexibility to introduce new processor roles without hardcoding every role into the runtime.

A capability model provides a stable way to describe what kinds of operations a processor may request.

## Capability concept

Capabilities may cover areas such as workspace access, repository inspection, file modification, process execution, task manipulation, processor invocation, memory proposals, or system experimentation.

Capabilities describe available operations, not a guaranteed right to perform arbitrary effects.

**On that list.** It was written before the effect vocabulary existed, and it is one of three overlapping lists `10-technical/01-effect-vocabulary.md` later reconciled into nine types. It should be read as the areas a policy concerns itself with, not as the enumeration — the enumeration is the effect vocabulary's, and a capability policy is expressed over that. Two of the areas have since acquired owners worth naming: memory proposals are proposals to `21-arch-knowledge-model`, which only a thinking processor makes (`22-arch-cognition/04-thinking.md`), and task manipulation is work-record mutation against `28-arch-work-record`.

## Reads, and where the permissive default lives

A read is not a typed effect, and it is still something an actor may or may not be allowed to perform. `10-foundations/02`'s 2026-09-11 Qualification withdrew the claim that reads are outside what may be checked, and `25-arch-invariant-layer` now carries reads in the gate's input domain — but the question of what *ordinarily* happens to a read is a policy question, which makes it this document's.

The default is permissive: reads pass unless a rule names them. That is a configuration this model expresses, not a property of reads, and it is stated as a default precisely so that it can be changed without anything structural having to move.

What granularity a rule may use to name a class of reads — by path, by crossing type, by volume against a ceiling — is unresolved, and is the same open question `10-foundations/02` holds from the foundational side.

## Authority

The runtime remains responsible for interpreting a requested operation under the current policy.

A reviewer may be allowed to inspect files but not modify them. An implementer may be allowed to propose and perform bounded workspace changes. A system-level optimizer may be able to create candidate configurations without being able to promote them into the trusted baseline.

## Why the distinction matters

Without this separation, role definitions become entangled with runtime security and system governance.

With it, roles can evolve experimentally while operational boundaries remain explicit.

## What this model does not provide

Capability and authority govern what a given actor may request under current policy, and that policy is legitimately adjustable as the system learns.

They are therefore not a floor. A separate, non-adjustable check sits beneath them, testing whether an effect is permissible at all rather than whether this actor is presently authorized to request it. An effect must pass both, and passing capability gating is not evidence of passing that check.

The two also differ in what they are keyed to. Capabilities are described per role, which works because policy can be revised as roles are added. The invariant check cannot be keyed to roles at all, since the role vocabulary is deliberately open-ended; it binds effects instead.

Neither of them answers a third question, and it is worth naming here so that this model is not asked to carry it. **Whether an effect is worth what it forecloses** is not a permission question. An effect can be requestable by this actor, permissible in general, and still a bad idea in this particular situation — most obviously when it is irreversible by nature, which `10-foundations/02` says cannot be refused on reversibility grounds alone without refusing the work itself. That judgment is reasoning-based, belongs to `22-arch-cognition/04-thinking.md`, and happens while the proposal is being formed rather than as a stage in the gating path. `25-arch-invariant-layer` sets out why it must sit upstream rather than inside the pipeline.

So: this model asks whether the actor may request it, the invariant gate asks whether it may happen at all, and thinking asks whether it should. Three questions, three owners, and only the first two are gates.

## Open question

Capability granularity should be derived from actual needs. Overly coarse capabilities weaken control; overly fine capabilities create administrative complexity and can distract the model from the cognitive objective.

Reads are the first concrete instance of that trade-off rather than a separate question. Naming a class of reads by path, by crossing type, or by volume against a ceiling are granularities with very different administrative costs, and the permissive default above means none of them has to be chosen before there is a reason to.
