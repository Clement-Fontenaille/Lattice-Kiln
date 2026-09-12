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

**Whether an instance actually performs that check is its own strategy.** Nothing needs building for it: a processor reasoning over what it was given is what a processor is, and recording the verdict is already a work-record mutation. `10-foundations/04`, On ownership, sets out why this is a configuration choice rather than something the architecture owes an actor. What the architecture does owe is that the verdict be *recordable distinguishably* once reached, and that is `28-arch-work-record`'s recorded conclusion.

For "the request has already been satisfied" specifically, `10-foundations/04` also names what context management must supply rather than judge: candidate matches from the knowledge base that plausibly converge with the objective, surfaced as ordinary retrieval artifacts. Whether one of them genuinely resolves the objective is the processor's call.

**Two of the four are conclusions and two are transitions**, which is worth separating because they land in different places. A false assumption and an already-satisfied request end the work item — they are recorded conclusions. A different problem being more relevant, or more investigation being needed, do not end anything: they are work-item transitions, a refinement or a split, and the item continues.

**An open question this exposes.** `28-arch-work-record` currently keeps three conclusions: *answered*, *blocked*, *declined*. A false-premise refusal and an already-satisfied request are both refusals to execute, so both land on *declined* — yet they call for entirely different follow-ups, and telling them apart matters to whoever reads the record afterwards. That is the same shape of collapse Milestone 5 recorded when an orchestrator resolved "false premise" and "cannot find a next step" both to *blocked*. Whether three verdicts are enough, or whether this vocabulary reproduces that collapse one level down, is unresolved and belongs with the processor contract rather than here.

## Open question

The project should avoid over-structuring task semantics too early. We need enough structure for persistence and provenance without forcing models to reason through a workflow schema they do not naturally use well.
