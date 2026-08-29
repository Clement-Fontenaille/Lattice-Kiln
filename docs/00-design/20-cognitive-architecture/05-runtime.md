# Deterministic Runtime

## TL;DR

The runtime is the substrate that preserves reality, limits effects, records history, and makes experiments reproducible.

> **Motto:** Flexible cognition requires a stable world.

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

## Open question

The practical boundary between runtime policy and AI-mediated policy remains one of the most important implementation questions and should be approached conservatively at first.
