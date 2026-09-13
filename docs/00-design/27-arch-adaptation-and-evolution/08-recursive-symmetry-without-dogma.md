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

Symmetry that is discovered can be exploited cheaply. Symmetry that is designed toward becomes a reason to force unlike problems into one shape because the shape is elegant.

Treating it as a principle to apply cautiously does not help: that keeps the risk and adds a rule. The observation is worth holding; the principle is not.

## Structural symmetry is worth exploiting

Where the levels genuinely do the same thing, shared machinery is low-risk and reduces duplication.

A candidate-change record, a comparison mechanism, an evidence and provenance model, or a promotion-decision structure can reasonably serve project-level, system-level, and meta-level feedback alike.

One of those is concrete: the evidence and provenance model is `21-arch-knowledge-model`, realizing `10-foundations/03`, and nothing about it is scoped to a particular feedback level. That is this section working as intended — shared machinery kept because the levels genuinely do the same thing with it, not because a shape recurred.

The test is whether sharing saves implementation effort without obscuring a real difference. A project memory update may still need very different validation from a system generation promotion, even if both are represented as candidate changes.

## Role symmetry should generally be avoided

This is not a second rule pulling against the one above. Exploiting a structural symmetry **is** factoring: noticing that the levels do the same thing and therefore keeping one of something rather than three. Avoiding role symmetry is that same operation applied to roles, and commissioning a new role on evidence is the de-factoring condition for when the symmetry proves not to be real. One principle, one release valve.

The consequential part: a repeating loop shape does not justify a separate kind of agent per level.

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

The same question has a second instance outside the feedback levels. `22-arch-cognition/04-thinking.md` groups several knowledge-state transitions — the walk, requalification, curation, souvenir compression, irreversible-effect risk evaluation — as a *family*, and defers to the default here rather than assuming a split.

That case carries the one argument for splitting this document does not already answer, and it is worth having in view. Scope and cost are invocation properties, so they dissolve. **Evolutionary independence** does not: system-level feedback revises role definitions, so two capabilities sharing one definition are tuned together whether or not that is wanted, and no amount of varying the invocation separates them. That is a genuine role-level consideration rather than a disguised invocation one.

It is set aside as premature rather than refuted. It anticipates a coupling nothing has yet experienced, and splitting stays available later on this document's own terms. But if a case ever arises where one capability's tuning demonstrably degrades another sharing its definition, that is the evidence the default asks for, and it will not look like a loop shape recurring.
