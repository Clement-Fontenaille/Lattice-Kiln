# Recursive Symmetry as an Observation

## TL;DR

The same abstract loop appears at the project, system, and meta levels. That recurrence is an implementation observation to exploit where it happens to save effort. It has no standing as a design principle, and it never justifies creating a new kind of agent.

> **Motto:** Notice the symmetry; do not design toward it.

## The observation

Project learning, system tuning, and meta-evaluation share a family resemblance:

```text
observe
    ↓
assess
    ↓
challenge
    ↓
propose
    ↓
experiment
    ↓
evaluate
    ↓
accept or reject
    ↓
persist
```

This is worth noticing. It is not worth building toward.

## Why this is not a design principle

An earlier formulation in this project treated symmetry as something to design toward cautiously — a principle to apply with restraint. That was an overreach of early intuition.

Symmetry that is discovered can be exploited cheaply. Symmetry that is designed toward becomes a reason to force unlike problems into one shape because the shape is elegant, which is the failure the caution was meant to prevent in the first place. Retaining it as a principle-applied-carefully preserved the risk while adding a rule.

The observation is retained. The principle is dropped.

## Structural symmetry is worth exploiting

Where the levels genuinely do the same thing, shared machinery is low-risk and reduces duplication.

A candidate-change record, a comparison mechanism, an evidence and provenance model, or a promotion-decision structure can reasonably serve project-level, system-level, and meta-level feedback alike.

The test is whether sharing saves implementation effort without obscuring a real difference. A project memory update may still need very different validation from a system generation promotion, even if both are represented as candidate changes.

## Role symmetry should generally be avoided

The more consequential correction is this: a repeating loop shape does not justify a separate kind of agent per level.

There is no strong reason a single evaluation-capable role cannot be invoked at different scopes, with different context, objectives, and evidence thresholds, rather than the role itself multiplying into a project-evaluator, a system-evaluator, and a meta-evaluator as distinct species.

The multiplicity belongs to invocation, not to identity. Scope recurses; actors need not.

## Consequence for the feedback levels

The three feedback documents describe genuinely distinct scopes, evidence requirements, and promotion criteria. They should continue to be read that way.

They should not be read as implying three separate kinds of agents. Nothing in their distinctness requires distinct actors, and treating it as though it does would inflate the system's cognitive vocabulary for no evidenced gain.

## Relation to role commissioning

System-level feedback may commission new roles when evidence justifies them. This conclusion constrains how that capability should be used.

The default assumption remains reuse of an existing role at a new scope. A new role is warranted when evidence shows an existing role genuinely cannot serve the need — not because a familiar loop shape recurred somewhere new.

## Where this reasoning does not apply

This concerns roles the feedback loops commission. Some roles are fixed outside those loops, because the loops structurally cannot decide them — a watcher cannot be commissioned by what it watches. Those are specified alongside the invariant layer and are not subject to the reasoning above.

The distinction matters in one direction in particular. An argument that such a role should be collapsed into an existing role at a new scope, on the grounds of avoiding role symmetry, would be misapplying this document.

## Open question

The degree of shared implementation among feedback levels should remain undecided until at least one working feedback loop exists to study.

Whether a single evaluation role invoked at three scopes actually performs as well as three specialized ones is an empirical question, and this document states a default rather than a finding.
