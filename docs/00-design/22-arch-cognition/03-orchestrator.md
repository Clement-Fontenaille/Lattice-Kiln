# The Orchestrator

## TL;DR

The orchestrator owns the strategy of the current cognitive effort, but it does not own truth, runtime authority, or the definition of its own success.

> **Motto:** Coordinate the work; do not become the system.

## Motivation

A fixed workflow cannot anticipate every shape of development problem.

An intelligent coordinator can instead decide whether the current situation calls for investigation, clarification, debate, decomposition, implementation, review, or additional evidence.

## Responsibility

The orchestrator interprets current work and knowledge, decides what cognitive operation appears useful next, selects or defines a processor role, formulates the processor objective, narrows the inherited scope where the objective warrants it, mediates discussions, and synthesizes results.

Its responsibility is strategic coordination.

## Deliberate limits

The orchestrator should not become the sole authority over persistent truth, runtime effects, system-wide evaluation criteria, or its own performance assessment.

Higher-level evaluation systems must be able to observe and criticize orchestration behavior.

## Context constraint

The orchestrator's own turn input is composed by `23-arch-context-management` turn by turn, the same way any processor's is. It does not govern its own context and has no special reach into how that composition is made — the context manager is not a processor, so it sits outside what the orchestrator coordinates.

That holds without anything having to fetch context on the orchestrator's behalf. The context manager is in the path everything to and from the model takes, so it composes because a turn is happening; there is no request to place and therefore no awkward case where the orchestrator would have to place it for itself. The relationship is not coordinator to coordinated, and it is not quite consumer to service either, since a consumer calls and the orchestrator never does.

Giving the orchestrator every conversation and every repository detail would recreate the same working-memory problem the processor architecture is intended to solve — the risk this section originally named before an actor existed to answer it.

## Scope: what this role may and may not do

This document briefly assigned scope derivation here, and that was wrong. The correction is worth keeping visible because the argument for it failed at the exact point it looked strongest.

The argument was that a generously-tuned orchestrator derives up to the intent's ceiling and no further, so its failure mode is a scope that does nothing rather than one that permits something new. That holds only if something else writes the ceiling. It does not: the same passage claimed a root work item derives from intent by *the same act at every level*, which puts the ceiling in this role's hands too. "Bounded by the intent's scope" is circular when this role writes the intent's scope. The uniformity that looked economical was what removed the bound.

And this role is tunable system configuration by its own account, above. A mandate written by something feedback can retune is a mandate the loops can widen indirectly, by adjusting the thing that writes it rather than by proposing a widening that a check would see.

**So derivation from intent belongs to the invariant layer** (`25-arch-invariant-layer`), not here.

**What stays here is narrowing.** The orchestrator formulates work items under a scope already set above it, and may give a child a boundary narrower than its parent's. Narrowing needs no protection: it makes the end-of-task check stricter rather than looser, and a role that declines to narrow simply leaves everything at the inherited boundary. The part of the original argument that survives is the observation underneath it — a scope follows from an objective rather than standing apart from it — which is a reason for narrowing to sit with formulation, and not a reason for the ceiling to.

## Scope constraint

Every processor is instantiated with a scope it cannot widen (`24-arch-permission-layer`). The orchestrator is a processor, so it has one too.

It reads work state across items rather than operating under a single one, so a work item's scope is the wrong size for it: it holds the **intent's** scope, derived above it by an invariant processor. Every work item it formulates inherits from that and may be narrower, never wider.

The earlier reading of this section had the orchestrator holding the intent's scope *because this role is where the descent from intent happens*. That was the circularity the section above corrects. It holds the intent's scope as a constraint it received, not as one it wrote.

## Expected evolution

The orchestrator role is explicitly considered tunable system configuration.

System-level feedback may later refine its instructions, capabilities, or coordination style.

"Context policy" used to appear on that list and has been removed, because it contradicted the section above. The orchestrator does not govern its own context, so there is no context policy belonging to it for feedback to refine. What feedback tunes is the **recall policy**, which belongs to `23-arch-context-management` and applies to every instance rather than to this role — it is on `27-arch-adaptation-and-evolution/02`'s list in its own right, not as a property of the orchestrator.

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

The second half of that is now answered and the first is not, which is worth
separating. **Yes, it is a first-class terminal state**, and it lives in
`28-arch-work-record` as a recorded conclusion keeping *answered*, *blocked* and
*declined* distinct — Milestone 5's own collapse of "false premise" into a generic
`blocked` is the evidence that free-text rationale does not survive the question.
How an orchestrator should actually reach that verdict remains open, and it is
probably not architecture's to settle: whether an instance inspects its objective
at all is that instance's strategy (`10-foundations/04`, On ownership). What the
architecture owes is that the verdict be recordable once reached, which it now is.
