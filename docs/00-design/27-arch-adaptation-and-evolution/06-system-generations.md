# System Generations

## TL;DR

A trusted system version is a reproducible package of cognitive configuration, runtime assumptions, evaluation machinery, and known evidence.

> **Motto:** A generation is something we can rebuild, compare, and explain.

## Motivation

If improvements exist only as runtime memory, every fresh installation begins from an inferior state and must rediscover previous lessons.

The project instead promotes validated system-level learning into versioned generations.

## Generation content

A generation may include processor definitions, orchestrator definition, the recall policy (`23-arch-context-management`), evaluation mechanisms, feedback configuration, model selection, runtime configuration, benchmark references, and migration or bootstrap metadata.

**What it does not include is accumulated knowledge.** A generation is configuration; a corpus is whatever happened to accumulate while that configuration ran. The two co-vary in ordinary operation, which is exactly why a system's evidence about itself is weak, and separating them is what makes a candidate judgeable outside the conditions that produced it (`07-bootstrapper-as-transfer-mechanism.md`). Packaging a corpus into a generation would reinstate that coupling while still looking like a clean instantiation, which is the worst form of it.

The exact package format is an implementation detail to be designed later.

## Lineage

Generations should preserve ancestry and reasons for significant changes.

A future maintainer should be able to identify which experiment introduced a processor revision or which evaluation justified a change to the orchestrator.

## Branching

The project should not assume that evolution converges on one universal configuration.

Different hardware, models, repository types, or developer preferences may justify different system branches.

There is now a specific reason to expect that rather than merely to allow it. `23-arch-context-management/02-context-as-experimental-surface.md` argues that policy adequacy runs on a gradient indexed by the model: this project is operated by hand as a knowledge base by a model capable enough not to need a context manager, and a weaker one manifestly cannot do the same. If adequacy depends on the model, branching is the mechanism that expresses it, and convergence on one configuration would be the surprising outcome rather than the expected one.

## Open question

We need to decide when configurations should be considered distinct generations versus parameterized variants of the same generation.
