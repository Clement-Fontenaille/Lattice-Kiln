# M14 — Meta-evaluation

**State:** open
**Was:** M12, before rework 2
**Design:** [`03-meta-level-feedback.md`](../../27-arch-adaptation-and-evolution/03-meta-level-feedback.md), [`08-recursive-symmetry-without-dogma.md`](../../27-arch-adaptation-and-evolution/08-recursive-symmetry-without-dogma.md)

## What this milestone is

Introduce explicit evaluation of the improvement process.

Measure whether benchmarks, promotion criteria, and feedback mechanisms actually
distinguish **transferable** improvements from local or metric-specific gains.

## Why this does not recurse forever

The obvious objection to a level that evaluates the evaluator is that it invites
another level above it. It does not, and the reason is structural rather than a
matter of taste:

- The level is **bounded by construction**. It asks *one generic question* — does
  self-tuning produce trustworthy improvement — not a meta-question per parameter.
- It **terminates on the invariant layer and the frozen baselines**, which are
  non-self-tuned anchors by definition. There is nothing above them to evaluate,
  because they are not adaptive.

This is the concrete form of the recursive-symmetry position: the symmetry is a
useful observation about the levels, not a licence to keep generating them.

## Scope, not a new kind of agent

As with [M10](10-project-level-adaptation.md) and
[M12](12-system-level-candidate-tuning.md): the levels differ in scope, evidence,
and promotion criteria, not necessarily in which processor performs them.

## What it inherits

The evaluation suite ([M6](completed/06-evaluation-task-suite.md)) is explicitly
*not* a meta-evaluation instrument — it scores single-repository task outcomes.
Whether the suite stays discriminating as models improve is deferred to this
milestone and [M15](15-cross-generation-comparison.md), and it is the first thing
that will need answering here.
