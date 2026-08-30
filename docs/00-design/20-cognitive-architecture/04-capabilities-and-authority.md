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

## Open question

Capability granularity should be derived from actual needs. Overly coarse capabilities weaken control; overly fine capabilities create administrative complexity and can distract the model from the cognitive objective.
