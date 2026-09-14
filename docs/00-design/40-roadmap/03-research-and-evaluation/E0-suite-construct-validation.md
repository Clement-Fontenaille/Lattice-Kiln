# E0 — Is the evaluation suite measuring one coherent thing?

**Status:** not run. Possibly answerable from runs already recorded.
**Gates:** E4, and the interpretation of every arm comparison on the M6 suite.

## The question

The Milestone 6 suite is used as a ruler by everything downstream. Nothing has checked
that it is one. An instrument that is a list of unrelated tasks rather than indicators
of a common thing produces scores that cannot be compared across arms, and the failure
is invisible from the scores themselves.

## What would falsify a coherent suite

Standard item analysis, decided before looking:

- **Difficulty distribution** — items clustered at ceiling or floor discriminate
  nothing.
- **Item—total correlation** — an item that does not correlate with the rest is
  measuring something else.
- **Dimensionality** — if the suite resolves into several unrelated factors, it is
  several instruments reported as one.

## Design

No new runs if the recorded ones suffice. The suite has been run by `monolith`,
`dloop` and `staged` across thirty tasks, which is the data item analysis needs.

Read per scenario rather than per arm: this asks about the **items**, not about which
arm won.

## What a null means

A suite that fails item analysis is not thereby worthless — it may be several
coherent sub-instruments. Splitting it and reporting per cluster is the likely
remedy, not rebuilding it, and `10-technical/10-evaluation-task-suite.md`'s `stresses`
tags are the candidate clustering.

## Cost

Lowest of anything here. Analysis over existing data.
