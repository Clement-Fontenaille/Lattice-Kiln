# Work, Intent, and Task Representation

## TL;DR

A human request is not assumed to be an executable task. The system must preserve intent while allowing its representation of the work to change.

> **Motto:** Preserve the goal; question the task.

## Motivation

Human requests often contain assumptions about causes, implementation choices, scope, or sequencing.

A development system that treats every request as an execution command may efficiently solve the wrong problem.

## Intent

Intent represents the underlying desired outcome or concern.

It should remain traceable even when the system rewrites the work derived from it.

## Work representation

A work item is a current formulation of what may need to be investigated or done.

It can be refined, challenged, split, merged, deferred, abandoned, or executed.

This flexibility is deliberate.

## Work unit

A work unit is a bounded piece of cognitive or practical work suitable for one processor or a short interaction.

The project has not yet decided whether work units need first-class persistent representation or can remain an emergent orchestration concept.

## Expected behavior

The system should be capable of deciding that the correct response to a task is not execution.

It may discover that the task is based on a false assumption, that a different problem is more relevant, that the request already has been satisfied, or that more investigation is necessary.

## Open question

The project should avoid over-structuring task semantics too early. We need enough structure for persistence and provenance without forcing models to reason through a workflow schema they do not naturally use well.
