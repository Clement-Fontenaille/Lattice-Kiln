# Constrained Intelligence Thesis

## TL;DR

The project assumes that a smaller local model can become substantially more useful when the surrounding system manages decomposition, context, memory, verification, and feedback well.

> **Motto:** Spend system design to save model capacity.

## Motivation

A constrained local model cannot reliably hold an entire large repository, a long task history, a complex plan, previous failures, and every relevant architectural decision in one context window.

Attempting to compensate only by increasing context length risks replacing missing information with excessive irrelevant information.

The system should instead reduce the amount of simultaneous reasoning each invocation must perform.

## Working hypothesis

Useful capability can emerge from the combination of limited models and stronger external cognitive structure.

That structure includes selective context, bounded cognitive roles, explicit evidence, durable project knowledge, independent review, deterministic tooling, and orchestration that can distribute reasoning across multiple short-lived invocations.

The hypothesis is empirical. It should eventually be tested against simpler approaches.

## Expected consequence

Model quality remains important, but model size should not be the only or primary optimization axis.

A system with better context discipline and better verification may outperform a larger but poorly orchestrated system on practical development work.

## Open question

We do not yet know where orchestration overhead exceeds the benefits of decomposition. Measuring that boundary is part of the project.
