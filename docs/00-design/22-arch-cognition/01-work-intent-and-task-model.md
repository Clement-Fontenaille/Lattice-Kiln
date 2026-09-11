# Work, Intent, and Task Representation

## TL;DR

A human request is not assumed to be an executable task. The system must preserve intent while allowing its representation of the work to change.

> **Motto:** Preserve the goal; question the task.

## Motivation

Human requests often contain assumptions about causes, implementation choices, scope, or sequencing.

A development system that treats every request as an execution command may efficiently solve the wrong problem.

## Where this model is held

This document defines the vocabulary. It does not hold anything: the durable record of intent, work items, and their transitions belongs to `28-arch-work-record`, which realizes what is defined here and adds no concepts to it.

The separation matters because a work item is revisable by design (below), and something has to hold both its current formulation and the history of how it got there without either one being reconstructed from the other.

## Intent

Intent represents the underlying desired outcome or concern.

It should remain traceable even when the system rewrites the work derived from it. That traceability is a service `28-arch-work-record` provides as intent lineage, and `10-technical/01-effect-vocabulary.md` already depends on it: a realized effect must be reconstructable per intent lineage, not only per actor.

## Work representation

A work item is a current formulation of what may need to be investigated or done.

It can be refined, challenged, split, merged, deferred, abandoned, or executed.

This flexibility is deliberate.

## Work unit

A work unit is a bounded piece of cognitive or practical work suitable for one processor or a short interaction.

The project has not yet decided whether work units need first-class persistent representation or can remain an emergent orchestration concept. `28-arch-work-record` inherits that question rather than answering it: how many kinds of record it holds depends on which way this goes.

## Expected behavior

The system should be capable of deciding that the correct response to a task is not execution.

It may discover that the task is based on a false assumption, that a different problem is more relevant, that the request already has been satisfied, or that more investigation is necessary.

## Open question

The project should avoid over-structuring task semantics too early. We need enough structure for persistence and provenance without forcing models to reason through a workflow schema they do not naturally use well.
