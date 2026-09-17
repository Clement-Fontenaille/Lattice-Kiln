# E7 — Which scenarios flipped between the M4 and M5 arms?

**Sheet:** [`docs/00-design/40-roadmap/03-research-and-evaluation/E7-paired-reanalysis.md`](../../docs/00-design/40-roadmap/03-research-and-evaluation/E7-paired-reanalysis.md)
**Status:** not run.
**Needs:** nothing built, no new runs, no decisions. Analysis over committed data.

## Why this one first

M4 reported 5/8 against 6/8. M5 reported 7/8, 6/8, 5/8. Those totals give a
magnitude. **Which tasks flipped gives a condition**, and a condition is
actionable where a total is not.

Pairing on task id also removes task-difficulty variance, which is the largest
noise source in a suite this small.

## What the data actually is (verified 2026-09-17)

| | file | rows | arms | tasks | reps |
|---|---|---|---|---|---|
| **M4** | `experiments/M4-ephemeral-processors/results/results.json` | 16 | `monolith`, `ephemeral` | 4 | 2 |
| **M5** | `experiments/M5-intelligent-orchestration/results/results.json` | 24 | `monolith`, `ephemeral`, `orchestrated` | 4 | 2 |

Both files carry the **same schema** and the **same four task ids**
(`task_1_stringcalc`, `task_2_median`, `task_3_nobug`, `task_4_starve`), so the
join is exact and needs no fuzzy matching.

`4 tasks × 2 reps = 8 attempts per arm`, which is where the `/8` in both
milestones' headline numbers comes from.

## One correction to the sheet

The sheet says to *"read the `stresses` slice for whether flips cluster by
capability tag."* **`stresses` does not exist in M4/M5 records** — it is an M6
suite field. These records carry `kind` instead. The protocol uses `kind` and
records that the tag-based clustering question cannot be answered from this
data.

## Layout

```
E7-paired-reanalysis/
  README.md      this file
  PROTOCOL.md    the steps — follow it literally
  flip_table.py  the analysis (written by step 2)
  results/       committed output
```
