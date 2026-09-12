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

One consumer of that policy is already waiting on it. `23-arch-context-management/02-context-as-experimental-surface.md` declines to solve credit assignment — determining which artifacts contributed to a result — and relies on aggregate comparison instead. That bet is only good if repetition is sufficient to separate policies, so the repetition policy is not a refinement there but a precondition. If it turns out that the difference between two context policies is smaller than the run-to-run variance this project can afford to average out, that framework's central measurement does not work and the elided problem returns.

## Open question

We still need to determine how to build benchmark suites that are representative enough to guide evolution without becoming so expensive that experimentation becomes impractical on local hardware.
