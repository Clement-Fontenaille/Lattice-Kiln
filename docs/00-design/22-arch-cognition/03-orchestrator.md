# The Orchestrator

## TL;DR

The orchestrator owns the strategy of the current cognitive effort, but it does not own truth, runtime authority, or the definition of its own success.

> **Motto:** Coordinate the work; do not become the system.

## Motivation

A fixed workflow cannot anticipate every shape of development problem.

An intelligent coordinator can instead decide whether the current situation calls for investigation, clarification, debate, decomposition, implementation, review, or additional evidence.

## Responsibility

The orchestrator interprets current work and knowledge, decides what cognitive operation appears useful next, selects or defines a processor role, formulates the processor objective and the scope that objective implies, mediates discussions, and synthesizes results.

Its responsibility is strategic coordination.

## Deliberate limits

The orchestrator should not become the sole authority over persistent truth, runtime effects, system-wide evaluation criteria, or its own performance assessment.

Higher-level evaluation systems must be able to observe and criticize orchestration behavior.

## Context constraint

The orchestrator's own turn input is composed by `23-arch-context-management` turn by turn, the same way any processor's is. It does not govern its own context and has no special reach into how that composition is made — the context manager is not a processor, so it sits outside what the orchestrator coordinates.

That holds without anything having to fetch context on the orchestrator's behalf. The context manager is in the path everything to and from the model takes, so it composes because a turn is happening; there is no request to place and therefore no awkward case where the orchestrator would have to place it for itself. The relationship is not coordinator to coordinated, and it is not quite consumer to service either, since a consumer calls and the orchestrator never does.

Giving the orchestrator every conversation and every repository detail would recreate the same working-memory problem the processor architecture is intended to solve — the risk this section originally named before an actor existed to answer it.

## Deriving scope

The orchestrator derives a work item's scope, at the moment it formulates that item. Stated as a choice rather than a deduction, with the reasons and the things that would overturn it.

**Why here.** It already formulates the objective, and a scope follows from an objective rather than being independent of it — "add another output format to this CLI tool" carries its boundary with it. Deriving at formulation is close to one act rather than two. It also satisfies the constraint `24-arch-permission-layer` places on any deriver: it does not execute the work item it creates, so it is deriving for work it is not doing. And it holds the ceiling, operating at intent level, so what it derives for a child is bounded without anything extra having to enforce it.

**The same act at every level, including the first.** A root work item has no parent to inherit from; it derives from the intent, which is the operator's own request and is not system-authored. That is the same derivation performed against a different source, not a separate intake mechanism.

**The objection, and why it does not land.** This role is tunable system configuration, so system-level feedback can retune the thing that writes mandates. But a generously-tuned orchestrator derives up to the intent's ceiling and no further, which is the same degradation profile as any lax deriver: it fails to narrow, and it cannot widen past intent. The failure mode is a scope that does nothing, not a scope that permits something new.

**What is given up, and why it is affordable.** Merging formulation with derivation means nothing independent checks whether a derived boundary actually matches the objective it came from. That would matter if the derivation were the only check — it is not. The verification is downstream and independent by construction, sitting in the invariant layer (`25-arch-invariant-layer`). The independence that matters here is between *deriving* and *verifying*, not between *formulating* and *deriving*.

**What would argue for splitting them later.** Evidence that orchestrators derive systematically generously, since the ceiling bounds that but does not prevent it. Or a finding that the two acts want different context or different role instructions, in which case they are two roles by `27-arch-adaptation-and-evolution/08`'s own test rather than by preference.

## Scope constraint

Every processor is instantiated with a scope it cannot widen (`24-arch-permission-layer`). The orchestrator is a processor, so it has one too, and what it is is the one case that arrangement does not settle.

It reads work state across items rather than operating under a single one, which means a work item's scope is the wrong size for it. The natural reading is that it holds the **intent's** scope, with the work items it formulates inheriting narrowed versions — consistent with mandate descending from intent, and with this role being the place that descent happens. Not yet argued, and recorded here as the open end rather than assumed.

What is clear either way: whatever scope the orchestrator holds bounds every work item it creates, since a child's boundary must sit inside its parent's. So this is not a detail that can be left to specification — it sets the ceiling for everything below it.

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
