# E0 — Is the evaluation suite measuring one coherent thing?

**Status:** **partially answered 2026-09-14** from runs already recorded — three defects found, see below. The item-analysis half has still not been run.
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

## Partial result, 2026-09-14 — three defects found without a new run

Prompted by an operator question about what the M7 arm's decline rule actually rests
on. All three are computable from data already recorded, which is what this sheet
predicted.

### 1. `objective_pass` does not measure whether the objective was met

*(Restated 2026-09-14, same day. This first read "the headline metric discards the
dimensions the checks print", which implied an oversight. It is not one.)*

`wf6_multi/test_task.py` says so in its own docstring:

```
DOCSCORE c/d   - documentation attended to (quality signal, does not gate)
TODOSCORE e/f  - TODO gardening (quality signal, does not gate)
```

**The author declared it.** `SUBTESTS` gates; the structural dimensions are quality
signals and deliberately do not reach the exit code. Four checks are built this way.

So the defect is not in the checks. It is that the harness computes
`objective_pass = (exit_code == 0)` and every downstream reader — the arm comparison
tables, `50-findings/08`, `50-findings/10`, this project's own prose — has taken it to
mean *the task was done*. It means **the gating dimension passed**.

The concrete cost: `hf_dict_dispatch` finishing at `STRUCTSCORE 0/3`, a refactor not
performed at all, is counted as a pass by every arm comparison published so far.

Two repairs are available and they are not the same. Fold the structural dimensions
into the exit code, which changes what the suite gates on. Or rename the metric and
report the dimensions alongside it, which changes nothing about the suite and
everything about how its numbers read. **Neither has been chosen**, and the second is
the cheaper one to get wrong quietly.


### 2. The baseline scores 8/30 by doing nothing

The `baseline` arm makes no model call and changes no file.

| | tasks | reading |
|---|---|---|
| false-premise | `wf4_assumption`, `hf_already_optimal`, `hf_dead_code`, `hf_remove_validation`, `hf_cache_nondeterministic` | correct — doing nothing *is* the answer |
| **work demanded** | `wf3_refactor`, `hf_extract_fn`, `hf_dict_dispatch` | **the metric cannot see the work** |

So the suite's dynamic range is **22 tasks, not 30**, with a floor of 8 that no arm
earned. Reading 24/30 against 18/30 is reading 16 against 10 of what was in play, and
the relative gap between arms is therefore **larger** than the totals suggest, not
smaller.

### 3. `wf3_refactor` has no structural dimension at all

Its objective asks for a shared helper to be extracted. Its check verifies only the
returned prices, and its own comments show what the author guarded against:

```
# staff must stay exact - a shared helper that rounds would break this
# clearance must stay rounded - a shared helper without rounding breaks this
```

**The check catches a badly-done refactor and cannot catch an absent one.** The
untouched source passes 5/5, and so does a correct refactor. Doing the work and not
doing it are the same score.

This is the instructive form of the defect: the author protected against the error
they imagined — the wrong refactor — and not against the null action.

*Checked and withdrawn:* `hf_deprecate` carries the same `L2-structural` tag with no
structural dimension, but its check has an explicit discriminator subtest
(`old_parse matches new_parse`) that a warning-only deprecation fails. Its coverage is
adequate; only the separate score line is missing. One task in thirty, not two.

### The remedy, and what it is not

Operator ruling, 2026-09-14. **The repair for defect 3 is in the objective, not in the
checking apparatus.** Restate the task until its completion has a mechanical witness:

> the two functions become one, **or** each body reduces to a call into a third
> function carrying the shared logic

An AST walk decides that. Two admissible outcomes rather than one, so it says what
finished looks like without prescribing the method.

**Do not close the gap with a judge or a test-writer.** For the judge half this
project has the measurement already: `50-findings/07` scored a deterministic core at
9/10 with zero model calls and 6/10 once a 7B checklist and panel were added. A judge
also relocates the unverifiability rather than removing it. *The test-writer half does
not follow from that and is deliberately left open* — writing a check and judging an
artifact are different operations, and three suite tasks already carry `kway-synth`
for it.

The general form is carried as a **granularity** criterion in
`00-design/22-arch-cognition/08-decomposition.md`, independent of that account's
capacity criterion, and as an authoring rule in
`10-technical/10-evaluation-task-suite.md`.

Note that defects 1 and 3 need **different** repairs. `hf_extract_fn` and
`hf_dict_dispatch` already have a witness — `STRUCTSCORE` — that the metric throws
away; folding the structural dimensions into the exit code fixes those and does
nothing for `wf3_refactor`, which has no witness to fold.

### The cheap test this yields, and why it is not sufficient

**Necessary:** for every task, does the **untouched source** fail the check? Where it
passes while the objective demands work, some part of the demand has no witness. One
pass over the recorded `baseline` results, no run needed.

**Not sufficient**, and the gap matters. Take a demand with three clauses where two
are witnessed and the third is not. The untouched source fails — on the strength of
the first two — so this test reports nothing wrong, and the third clause stays
silently unwitnessed.

**The sufficient form is per clause, not per task:** *for each clause of the demand,
is there a dimension that moves when that clause alone is done?* That is more
expensive, because it obliges the author to name a witness clause by clause.

`wf6_multi` already does exactly that — `SUBTESTS` for `topo_sort`, `DOCSCORE` for the
docstrings and `NOTES.md`, `TODOSCORE` for the TODO gardening — and so does
`hf_json_serialize`. **The practice exists in this suite and is not a rule**, which is
the same shape as the defect it is meant to catch: it holds by the author's care and
nothing would report its absence.


### What this does to the sheet's own question

*Is the suite measuring one coherent thing?* Partly answered, and negatively: it is
measuring subtests, while printing structural scores that look like they count. That
is two instruments reported as one — the exact failure mode named at the top of this
sheet, arrived at from the metric rather than from item analysis.

**The remedy is not obviously a rebuild.** Folding the structural dimensions into the
exit code is a one-line change per check and would restore what the suite already
measures. Whether the M4/M5/M6/M7 comparisons should be re-scored against it is a
separate decision, and it is the one with consequences.

## Cost

Lowest of anything here. Analysis over existing data.
