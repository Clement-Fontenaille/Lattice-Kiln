# System Generations

## TL;DR

A trusted system version is a reproducible package of cognitive configuration, runtime assumptions, evaluation machinery, and known evidence.

> **Motto:** A generation is something we can rebuild, compare, and explain.

## Motivation

If improvements exist only as runtime memory, every fresh installation begins from an inferior state and must rediscover previous lessons.

The project instead promotes validated system-level learning into versioned generations.

## Generation content

A generation may include processor definitions, orchestrator definition, context policy, evaluation mechanisms, feedback configuration, model selection, runtime configuration, benchmark references, and migration or bootstrap metadata.

The exact package format is an implementation detail to be designed later.

## Lineage

Generations should preserve ancestry and reasons for significant changes.

A future maintainer should be able to identify which experiment introduced a processor revision or which evaluation justified a change to the orchestrator.

## Branching

The project should not assume that evolution converges on one universal configuration.

Different hardware, models, repository types, or developer preferences may justify different system branches.

## Open question

We need to decide when configurations should be considered distinct generations versus parameterized variants of the same generation.
