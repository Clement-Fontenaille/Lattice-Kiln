# E0 — Is the evaluation suite measuring one coherent thing?

**Sheet:** [`docs/00-design/40-roadmap/03-research-and-evaluation/E0-suite-construct-validation.md`](../../docs/00-design/40-roadmap/03-research-and-evaluation/E0-suite-construct-validation.md)
**Status:** partially answered 2026-09-14 — three defects found without a new run.
The item-analysis half has still not been run.
**Gates:** E4, and the interpretation of every arm comparison on the M6 suite.

## What is already answered

Three defects, all found from recorded data:

1. **`objective_pass` does not mean the objective was met.** It means the gating
   dimension passed. Structural dimensions (`DOCSCORE`, `TODOSCORE`, `STRUCTSCORE`,
   `PERFSCORE`…) are declared quality signals that deliberately do not gate.
   Cost: `hf_dict_dispatch` at `STRUCTSCORE 0/3` — a refactor not performed at all —
   counts as a pass in every arm comparison published so far.
2. **The baseline scores 8/30 by doing nothing.** Dynamic range is 22 tasks, not 30.
3. **`wf3_refactor` has no structural dimension at all** — doing the work and not
   doing it score the same.

## What is not answered

- **The item analysis**: difficulty distribution, item–total correlation,
  dimensionality. This is the half the sheet was opened for.
- **The untouched-source test**, stated in the sheet as *necessary but not
  sufficient*: for every task, does the untouched source fail the check?
- **The defect-1 repair decision**: fold structural dimensions into the exit code
  (changes what the suite gates on), or rename the metric and report dimensions
  alongside (changes nothing about the suite, everything about how its numbers
  read). **Neither has been chosen**, and the sheet warns the second is the
  cheaper one to get wrong quietly.

## What the data is (verified 2026-09-17)

`experiments/M6-evaluation-suite/results/<arm>.json` — 18 arms, one JSON array
each, 30–34 tasks, 1–5 reps.

Per-row fields that matter here:

| field | meaning |
|---|---|
| `task` | task id, joins to `tasks.json` |
| `objective_pass` | the gating boolean — **string `'True'`/`'False'` in some rows** |
| `struct` | dict of per-requirement dimensions, e.g. `{"PERFSCORE": [0,1], "AUDITSCORE": [1,1]}` — `[earned, total]` |
| `baseline_sub` / `final_sub` | `[passed, total]` subtests before/after |
| `stresses` | capability tags, the sheet's candidate clustering |
| `shape`, `trap`, `worker_view` | task taxonomy |

**Good news for cost:** `struct` is already structured data. The per-requirement
analysis needs **no log parsing** — the dimensions are sitting in the results JSON.

**Bad news for power:** `struct` is populated on only ~6–10 tasks per arm. Whatever
the per-requirement analysis says, it says it about a third of the suite at most.

## Layout

```
E0-suite-construct-validation/
  README.md       this file
  PROTOCOL.md     the steps
  item_analysis.py
  results/
```
