# Experiments and Candidate Systems

## TL;DR

A system change should be treated as a hypothesis that creates a candidate, not as an improvement merely because it sounds plausible.

> **Motto:** Change is a claim; experiment is the evidence.

## Motivation

Prompt edits, context-policy changes, new processor roles, and orchestration tweaks can all produce appealing anecdotal results.

Without controlled comparison, the project risks evolving by taste rather than evidence.

## Experiment concept

An experiment compares a candidate configuration with a known baseline under conditions that make the result interpretable.

The project should preserve the hypothesis, tested configuration, evaluation inputs, observations, and promotion decision.

**Motivated, and its interpretations framed, before it is run.** A method is not an experiment: describing what apparatus should exist commits to nothing, while running something commits to reading what comes out of it. So each experiment names what decision it is for and who will make it — `10-foundations/07`'s standard for any measurement taken without an operator in it, which most of this project's are — and states beforehand how its possible outcomes will be read.

That second half is not bureaucracy, and Resolution before precision below is why. How a null result reads depends on the effect-size regime: where a large effect was expected and none appears, that is a finding, while in a small-effect regime the same observation usually means only that nothing could be seen. If the regime is decided *after* the result is in hand, either reading is available for any outcome, and the experiment establishes nothing while appearing to. Fixing the expected effect size in advance is what keeps a null informative.

## Candidate systems

A candidate system is an isolated variation of a trusted generation.

Candidate status allows the system to explore aggressive changes without contaminating the baseline.

## Repetition and stochasticity

LLM behavior is stochastic. A single successful run is therefore weak evidence.

The project should later establish practical repetition policies based on cost, variance, and the importance of the proposed change.

One consumer of that policy is already waiting on it. `23-arch-context-management/02-context-as-experimental-surface.md` declines to solve credit assignment — determining which artifacts contributed to a result — and relies on aggregate comparison instead. That bet is only good if repetition is sufficient to separate policies, so the repetition policy is not a refinement there but a precondition.

## Everything here depends on expected effect size

How much repetition an experiment needs is governed by how large a difference it is looking for, and that is the variable to establish first rather than a detail to refine later.

**The differences currently under study are enormous.** A monolithic implementer against a three-role chain against an orchestrator. No context management against naive substring matching. No retrieval against retrieval. These are not variants of one design, they are different designs, and the effects they produce should be correspondingly large. In that regime a single run over a well-resolved suite is adequate, and the statistical worry below does not bite.

This also decides how a **null result** reads, which is not obvious and matters for how existing findings should be understood. When a large effect was expected and none appears, that is a result — Milestone 4 expected role separation to help and found it did not, which is informative precisely because the expectation was strong. In a small-effect regime the same observation usually means only that the experiment could not see anything. The identical output supports opposite readings depending on which regime produced it.

**It is a phase, not a permanent condition.** As the large design questions get settled, the remaining differences shrink, and precision starts to matter in a way it does not now. The machinery for that regime should not be built in advance, for the same reason no vector index is being built in advance: it is sequencing, not doubt.

**The transition is not announced, so it needs a signal.** Drifting into the small-effect regime while still running one repeat is how noise starts getting reported as findings. A cheap diagnostic is available and reuses the stability classification below: run one arm twice and compare its variation against itself to the variation between arms. While between-arm differences clearly exceed within-arm ones, one run is enough. When they become comparable, the regime has changed and the experimental protocol has to change with it.

## Resolution before precision

There is a wrong way to reason about how much repetition is needed, and it is worth naming because it is the intuitive one, and because it is the one that becomes tempting as soon as effects shrink.

The wrong way treats an eight-task suite as eight samples of a single quantity, computes a pass rate, and asks how tightly that rate is estimated. Under that framing the answer is discouraging — separating two arms differing by ten points of pass rate would need something like forty repeats of the suite per arm, and halving the effect quadruples it. That arithmetic is correct and, in the regime described above, irrelevant.

It is irrelevant because the tasks are not interchangeable draws. They are **distinct measurement points**, each a different scenario, and the average over them estimates a quantity that does not correspond to any situation the system will actually be in. This project's own positions say so directly: too much context is a relation and not a property (`10-foundations/04`), adequacy runs on a gradient indexed by model, task and budget (`23-arch-context-management/02-context-as-experimental-surface.md`), and what varies with an assembly's capability is where a boundary sits rather than a scalar score (`22-arch-cognition/08-decomposition.md`). If effects are conditional, averaging across heterogeneous conditions is the wrong operation before it is an imprecise one.

**Resolution is how many distinguishable conditions an experiment can see. Precision is how tightly it pins one number.** Adding scenarios buys resolution. Repeating a scenario buys precision. For nearly every question this project asks, resolution is worth more — knowing that a policy wins on tasks needing cross-file knowledge and loses on tasks needing long single-file reasoning is more useful than knowing it wins by eight points on average, and it is also more actionable, because it names a condition rather than a magnitude.

**A suite already carries its own error information.** Grouped into clusters of similar scenarios, the consistency within a cluster is itself a reliability signal, and it costs no repetition. Three related tasks all flipping the same way at one run each is unlikely by chance and says something a tighter estimate of a mean would not. Consistency across related scenarios substitutes for repetition of one scenario, and is more informative per unit of compute.

**What repetition is actually for.** Not tightening a mean, but classifying whether a given scenario is stable. Five runs distinguishes a task that passes five times out of five from one that passes three — the first is a usable measurement point, the second is noise-dominated and should be treated separately rather than folded into a total. Five is a reasonable default for that purpose. **One remains valid**, particularly on a well-resolved suite, and is the right starting point rather than a compromise.

Many repeats are right in one case: measuring a precisely specified effect inside an exactly defined frame. That is a rare situation and should be recognised as the exception rather than the standard to which ordinary experiments are held.

Two practices follow that do not depend on any of this arithmetic.

**Compare paired, not aggregate.** Running both arms on the same tasks with the same seeds removes task-difficulty variance entirely, and the measurement becomes which scenarios *flipped* rather than which total was higher. This is the resolution view applied to comparison, and it is where the interesting information was all along. Milestone 4 and Milestone 5 reported totals — 5/8 against 6/8, then 7/8, 6/8 and 5/8 — while running their arms on a shared suite, so the per-scenario pattern may be recoverable from data already collected. That would be the cheapest experimental improvement available here, and it needs no new runs.

**Prefer graded objective outcomes over binary ones.** A pass or fail discards information about how a scenario went. Calls-to-success, retries needed, or regression counts are graded, objective, and already produced — Milestone 5's adaptive-retry finding used exactly that kind of quantity. What they must not be is model-judged, for the reasons the judge-lab result gives.

## What follows for spending

Given a fixed budget, add scenarios before adding repeats.

A new scenario can reveal a condition under which the answer changes. A repeat of an existing one can only make an answer already in hand slightly less noisy. The first can surprise; the second cannot.

## Open question

We still need to determine how to build benchmark suites that are representative enough to guide evolution without becoming so expensive that experimentation becomes impractical on local hardware. Under Resolution before precision that question sharpens: representativeness is a resolution property — how many distinguishable conditions the suite covers — rather than a matter of size.

When the small-effect regime actually arrives, and whether the within-arm against between-arm diagnostic above is sensitive enough to notice it before a few noisy findings have already been recorded.
