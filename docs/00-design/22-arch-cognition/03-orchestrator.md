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

Giving the orchestrator every conversation and every repository detail would recreate the same working-memory problem the processor architecture exists to solve.

## Scope

Every processor is instantiated with a scope it cannot widen (`24-arch-permission-layer`), and the orchestrator is a processor. It reads work state across items rather than operating under a single one, so a work item's scope is the wrong size for it: it holds the **intent's** scope, received as a constraint rather than written. Every work item it formulates inherits from that and may be narrower, never wider.

**This role narrows scope; it does not write the ceiling.**

Deriving a mandate from intent belongs to the invariant layer (`25-arch-invariant-layer`), and the reason is that this role is tunable system configuration by its own account below. A mandate written by something feedback can retune is a mandate the loops can widen indirectly, by adjusting the thing that writes it rather than by proposing a widening any check would see. The tempting counter-argument — that a generously-tuned orchestrator still derives no further than the intent's ceiling — is circular, since it would be this role writing that ceiling too.

What stays here is narrowing. The orchestrator formulates work items under a scope already set above it and may give a child a boundary narrower than its parent's. Narrowing needs no protection: it makes the end-of-task check stricter rather than looser, and declining to narrow leaves everything at the inherited boundary. A scope follows from an objective rather than standing apart from it, which is a reason for narrowing to sit with formulation and not a reason for the ceiling to.

## Expected evolution

The orchestrator role is explicitly considered tunable system configuration.

System-level feedback may later refine its instructions, capabilities, or coordination style.

Not a context policy, though. The orchestrator does not govern its own context, so there is none belonging to it for feedback to refine. What feedback tunes is the **recall policy**, which belongs to `23-arch-context-management` and applies to every instance rather than to this role — it sits on `27-arch-adaptation-and-evolution/02`'s list in its own right.

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

**How stopping rules tell a principled stop from an unprincipled one** — objective met or task refused on inspection, against stuck or budget-hit. That the distinction is a **first-class terminal state** rather than free-text rationale is settled: it lives in `28-arch-work-record` as a recorded conclusion keeping *answered*, *blocked* and *declined* apart, and Milestone 5's collapse of "false premise" into a generic `blocked` is the evidence that prose does not survive the question. How a verdict is actually reached is open, and probably not architecture's to settle — whether an instance inspects its objective at all is that instance's strategy (`10-foundations/04`). What the architecture owes is that the verdict be recordable, which it is.
