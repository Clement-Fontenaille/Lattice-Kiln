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

## Candidate systems

A candidate system is an isolated variation of a trusted generation.

Candidate status allows the system to explore aggressive changes without contaminating the baseline.

## Repetition and stochasticity

LLM behavior is stochastic. A single successful run is therefore weak evidence.

The project should later establish practical repetition policies based on cost, variance, and the importance of the proposed change.

One consumer of that policy is already waiting on it. `23-arch-context-management/02-context-as-experimental-surface.md` declines to solve credit assignment — determining which artifacts contributed to a result — and relies on aggregate comparison instead. That bet is only good if repetition is sufficient to separate policies, so the repetition policy is not a refinement there but a precondition.

## What the numbers say, roughly

The gap is larger than "later" suggests, and the project's own findings are the evidence.

With a binary pass or fail per task and a suite of eight, the standard error around a pass rate of 0.7 is about 0.16 — roughly ±1.3 tasks. A one-task difference from a single run is therefore inside the noise, not a measurement. Milestone 4 reported 5/8 against 6/8 and Milestone 5 reported 7/8, 6/8 and 5/8. Those findings hedge correctly, but the reason is sharper than the hedging says: at one run of eight tasks, one task of difference is not a result.

Detecting a 0.10 absolute difference in pass rate at conventional power needs on the order of 350 task-runs per arm — about 44 repeats of an eight-task suite. Halving the effect to 0.05 quadruples it. The project currently runs one. The assumptions behind that arithmetic are also generous: it treats tasks as independent and equally hard, and they are neither.

Three consequences, and none of them is "run more and hope".

**Compare paired, not aggregate.** Running both arms on the same tasks with the same seeds removes task-to-task difficulty variance entirely, leaving only model stochasticity. The measurement then becomes which tasks *flipped* rather than which score was higher, and discordant pairs carry far more signal than a score difference. The existing arms already ran on a shared suite, so this may be recoverable from data already collected rather than requiring new runs — which would be the cheapest experimental improvement available to this project.

**Prefer graded objective outcomes over binary ones.** A pass/fail result discards information and inflates the N required. Calls-to-success, retries needed, or regression counts are graded, objective, and already produced — Milestone 5's adaptive-retry finding used exactly this kind of quantity. What they must not be is model-judged, for the reasons the judge-lab result gives.

**Accept that only large effects are visible, and aim at large effects.** This bounds what the experimental framework can be used for. It can answer whether retrieval helps at all; it cannot rank two nearby parameter settings. Fine-grained tuning is out of reach at this scale and attempting it produces noise dressed as evidence.

## Open question

We still need to determine how to build benchmark suites that are representative enough to guide evolution without becoming so expensive that experimentation becomes impractical on local hardware.
