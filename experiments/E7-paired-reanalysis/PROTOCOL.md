# E7 Protocol — paired re-analysis of M4 vs M5

Follow these steps in order. Every path is relative to the repository root
(`C:\Users\Fontenaille\Desktop\Lattice-Kiln`). Nothing here runs a model, calls
a network, or modifies any existing file. If a step's stated precondition is not
true, **stop and record why** rather than improvising.

---

## Step 0 — Preconditions (2 minutes)

Check all three. If any fails, stop.

```bash
python -c "import json; d=json.load(open('experiments/M4-ephemeral-processors/results/results.json')); print(len(d))"
# expect: 16

python -c "import json; d=json.load(open('experiments/M5-intelligent-orchestration/results/results.json')); print(len(d))"
# expect: 24

python -c "
import json
a={r['task'] for r in json.load(open('experiments/M4-ephemeral-processors/results/results.json'))}
b={r['task'] for r in json.load(open('experiments/M5-intelligent-orchestration/results/results.json'))}
print('identical task sets:', a==b, sorted(a))
"
# expect: identical task sets: True ['task_1_stringcalc','task_2_median','task_3_nobug','task_4_starve']
```

If the task sets are **not** identical, the pairing is invalid. Stop and record
the difference — that is itself a finding about the two milestones' comparability.

---

## Step 1 — Fix the definitions before looking at anything

These are decided now, in writing, so the analysis cannot be tuned to its own
result.

**Unit of observation:** one `(task, arm, rep)` attempt.

**Outcome variable:** `objective_pass`, read as a boolean. Note this is the
**gating** metric and carries E0's defect 1 — it means *"the gating dimension
passed"*, not *"the task was done"*. M4/M5 records have no structural dimensions
to fold in, so the defect cannot be repaired here; it is **recorded as a
limitation**, not worked around.

**What counts as a flip.** For an arm present in both milestones (`monolith`,
`ephemeral`), compare per `(task, rep)`:

| M4 | M5 | label |
|---|---|---|
| False | True | `gained` |
| True | False | `lost` |
| True | True | `stable_pass` |
| False | False | `stable_fail` |

**Tie-break when reps disagree.** Report per-rep. Do **not** average reps into a
rate and then compare rates — that reintroduces the aggregation this experiment
exists to avoid. If the two reps of one `(task, arm)` cell disagree within a
single milestone, label that cell `unstable` and report it separately; an
unstable cell cannot be read as a flip.

**The `orchestrated` arm exists only in M5.** It has no M4 counterpart, so it
cannot flip. It is reported as a standalone column against M5's other two arms,
never as a flip.

---

## Step 2 — Write the analysis script

Create `experiments/E7-paired-reanalysis/flip_table.py`. It must:

1. Load both JSON files (stdlib `json` only — no pandas, no new dependency).
2. Index each as `{(task, arm, rep): objective_pass}`. Note `objective_pass` is
   stored as the **string** `'True'`/`'False'` in some rows and as a real boolean
   in others — normalise with an explicit helper, do not rely on truthiness
   (`bool('False')` is `True`, which would silently invert results).
3. For each `(task, arm, rep)` present in both milestones, emit the flip label
   from Step 1's table.
4. Detect and label `unstable` cells (reps disagreeing within one milestone).
5. Write `results/flip_table.json` and a human-readable `results/flip_table.md`.

Sanity assertion the script must make and fail loudly on: the per-arm M4 and M5
pass totals it recomputes must equal the milestones' published headline numbers
(M4: 5/8 and 6/8; M5: 7/8, 6/8, 5/8). **If they do not match, the published
numbers and this data disagree** — that is a finding, and a bigger one than the
flip table. Stop and record it.

---

## Step 3 — Output schema

`results/flip_table.json`:

```json
{
  "schema": "e7-flip/1",
  "generated": "ISO-8601",
  "sources": {
    "m4": "experiments/M4-ephemeral-processors/results/results.json",
    "m5": "experiments/M5-intelligent-orchestration/results/results.json"
  },
  "headline_check": {
    "m4": {"monolith": "5/8", "ephemeral": "6/8"},
    "m5": {"monolith": "7/8", "ephemeral": "6/8", "orchestrated": "5/8"},
    "matches_published": true
  },
  "cells": [
    {"task": "task_1_stringcalc", "arm": "monolith", "rep": 1,
     "m4_pass": true, "m5_pass": true, "label": "stable_pass", "kind": "implement"}
  ],
  "summary": {"gained": 0, "lost": 0, "stable_pass": 0, "stable_fail": 0, "unstable": 0},
  "limitations": [
    "objective_pass is the gating metric only (E0 defect 1); no structural dimensions exist in M4/M5 records",
    "stresses tags absent from M4/M5 records; kind used instead; tag-clustering question unanswerable here",
    "4 tasks x 2 reps per arm: any pattern is directional, not decisive"
  ]
}
```

`results/flip_table.md` — the same content as a table a human can read without
running anything.

---

## Step 4 — Read the result against what was predicted

The sheet states what a null means. Apply it **as written**, before looking for
alternatives:

- **No flips** (every cell `stable_pass` or `stable_fail`): a real finding. The
  arms differ in cost and not in what they can do — close to what M4 already
  concluded, and it strengthens it.
- **Flips concentrated on one task**: that task is the condition. Name it and
  read its fixture (`experiments/M4-ephemeral-processors/fixture/<task>/`) for
  what distinguishes it.
- **Flips scattered with no pattern**: report as scattered. Do **not** search for
  a post-hoc grouping that makes them look ordered — with 8 attempts per arm,
  something will always look like a pattern.

---

## Step 5 — Record it

1. Commit `flip_table.py`, `results/flip_table.json`, `results/flip_table.md`.
2. Update the sheet
   (`docs/00-design/40-roadmap/03-research-and-evaluation/E7-paired-reanalysis.md`):
   set **Status** to run, with the date, and add a short result section — the
   flip counts and the one-line reading. Do not rewrite the sheet's existing
   framing; append.
3. If the headline-number check in Step 2 failed, that goes in
   `docs/00-design/50-findings/` as its own entry, not buried in this sheet.

## Done when

`results/flip_table.md` exists, its recomputed headline numbers match the
published ones (or the mismatch is recorded as a finding), and the sheet's status
line says run.
