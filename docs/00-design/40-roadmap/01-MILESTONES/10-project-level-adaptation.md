# M10 — Project-level adaptation

**State:** open
**Was:** M8, before rework 2
**Design:** [`01-project-level-feedback.md`](../../30-adaptation-and-evolution/01-project-level-feedback.md)

## What this milestone is

Use observed project work to improve project-local knowledge.

The key test is whether later work in the same repository improves **without
polluting global system behavior**.

## Evidence question

*Not yet stated.* The bar recorded at rework 1:

> Second-pass work in the same repository improves without polluting global
> behaviour, on even a handful of tasks.

## Scope, not a new kind of agent

This is a *scope* of feedback. The same holds for
[M12](12-system-level-candidate-tuning.md) and [M14](14-meta-evaluation.md): the
levels differ in scope, evidence, and promotion criteria — **not necessarily in
which processor performs them.**

That distinction is load-bearing. Reading the three levels as three agents invents
an org chart the architecture never asked for, and the recursive-symmetry document
([`08-recursive-symmetry-without-dogma.md`](../../30-adaptation-and-evolution/08-recursive-symmetry-without-dogma.md))
exists to keep the symmetry from hardening into dogma.

## The first loop

This is the first milestone where the system changes its own behaviour on the
basis of its own observations, however narrowly. The floor
([M3](03-invariant-floor.md)) and the observability foundation
([M2](completed/02-observability-foundation.md)) were both placed early so that
this milestone could be reached without either being retrofitted.

It is still not a *self-modifying* loop — project-local knowledge is not system
configuration. That line is crossed at
[M12](12-system-level-candidate-tuning.md).
