# Open Questions Register

## TL;DR

Unresolved questions are first-class project state. They should remain visible until evidence or explicit design work closes them.

> **Motto:** Unknown is better than silently assumed.

## Work representation

How much structure does persistent work need before structure starts constraining reasoning?

Should work units be explicit persistent objects or temporary orchestration constructs?

How should intent survive rewriting, merging, or abandonment of derived tasks?

## Processor architecture

How narrow should processor roles become?

When does role specialization outperform a general-purpose processor?

How independent must adversarial processors be to provide useful disagreement?

Does using different models for different roles produce enough benefit to justify runtime complexity?

## Orchestration

How much context should the orchestrator receive?

Should orchestration sessions persist or be repeatedly reconstructed from curated state?

Can orchestration itself be delegated?

What practical stopping rules prevent useless reasoning loops without reintroducing a rigid workflow?

## Runtime boundary

Which low-risk effects can be executed directly?

Which actions should always remain proposals requiring a runtime policy gate?

How should destructive operations, network access, secrets, and system modification be isolated?

## Memory

Who decides that a finding deserves persistence?

How should contradictory memories coexist?

When should memory be revised rather than appended?

How should stale knowledge be detected and retired?

## Context governance

How should relevance be estimated?

Can a context curator become a bottleneck or a source of systematic blindness?

How should processors request missing context?

How do we evaluate context quality independently from final task success?

## Evaluation

Which metrics correlate with meaningful developer value?

How much human evaluation is required?

How can independent evaluators remain sufficiently independent when they use the same underlying model?

How do we detect benchmark overfitting?

## System evolution

What amount of evidence is sufficient to promote a candidate?

How should stochastic variation be handled?

When should multiple competing branches remain alive instead of selecting one winner?

How are regressions weighted against improvements?

## Meta-evaluation

Which evaluation anchors must remain fixed long enough to detect moving-goalpost failures?

Which parts of the evaluation system should themselves evolve?

How do we recognize that the feedback architecture adds more complexity than value?

## Bootstrapping

Which parts of a generation belong in scripts, declarative configuration, local knowledge, or external model assets?

How portable must a generation be across machines?

How do we preserve the ability to reproduce an older generation after runtimes and model ecosystems have changed?

## Project process

At what point is a conceptual document mature enough to derive technical contracts?

How should experiments that invalidate conceptual assumptions feed back into this documentation set?

What level of historical rationale should remain after a concept is replaced?
