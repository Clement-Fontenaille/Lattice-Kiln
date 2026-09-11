# The Orchestrator

## TL;DR

The orchestrator owns the strategy of the current cognitive effort, but it does not own truth, runtime authority, or the definition of its own success.

> **Motto:** Coordinate the work; do not become the system.

## Motivation

A fixed workflow cannot anticipate every shape of development problem.

An intelligent coordinator can instead decide whether the current situation calls for investigation, clarification, debate, decomposition, implementation, review, or additional evidence.

## Responsibility

The orchestrator interprets current work and knowledge, decides what cognitive operation appears useful next, selects or defines a processor role, formulates the processor objective, mediates discussions, and synthesizes results.

Its responsibility is strategic coordination.

## Deliberate limits

The orchestrator should not become the sole authority over persistent truth, runtime effects, system-wide evaluation criteria, or its own performance assessment.

Higher-level evaluation systems must be able to observe and criticize orchestration behavior.

## Context constraint

The orchestrator's own context is composed by `23-arch-context-management` turn by turn, the same way any processor's is. It does not govern its own context and has no special reach into how that composition is made — the context manager is not a processor, so it sits outside what the orchestrator coordinates.

That holds without anything having to fetch context on the orchestrator's behalf. The context manager is in the path everything to and from the model takes, so it composes because a turn is happening; there is no request to place and therefore no awkward case where the orchestrator would have to place it for itself. The relationship is not coordinator to coordinated, and it is not quite consumer to service either, since a consumer calls and the orchestrator never does.

Giving the orchestrator every conversation and every repository detail would recreate the same working-memory problem the processor architecture is intended to solve — the risk this section originally named before an actor existed to answer it.

## Expected evolution

The orchestrator role is explicitly considered tunable system configuration.

System-level feedback may later refine its instructions, capabilities, context policy, or coordination style.

## First evidence (Milestone 5)

A small experiment (findings-log entry 6) compared an LLM orchestrator against
the Milestone 4 fixed planner→implementer→reviewer chain and a monolith, on a 7B
model with naive context. The orchestrator scored 7/8 versus 6/8 (monolith) and
5/8 (fixed chain) — the first arm to beat the monolith. The gain was entirely
**adaptive retry**: on the tasks the other arms failed, the orchestrator spawned
a second implementer after the first attempt missed the objective check. Cost was
~5× the model calls and ~4.5× the wall-clock, so the overhead only paid off where
a single pass would have failed.

Two weaknesses showed up. The orchestrator's **stop decisions were
under-explained** — it recorded why it acted at each step but usually not why it
judged the work done. And it **conflated "the task rests on a false premise" with
"I cannot find a next step"**: both resolved to a generic `blocked`, where the
simpler arms explicitly *declined*. Understandability of the acting half of the
loop held up; the stopping half did not.

## Open question

The project has not yet determined whether one orchestrator is sufficient, whether orchestration can be delegated recursively, or whether multiple competing orchestrators should sometimes be compared.

Milestone 5 adds: how should the orchestrator's stopping rules tell a principled
stop (objective met; task refused on inspection) from an unprincipled one (stuck;
budget hit), and does that distinction need to be a first-class terminal state
rather than left to free-text rationale?
