# M5 comparison results

_2026-08-31 00:44 - 1 runs_

- **orchestrated**: objective pass 1/1, mean wall 32.8s, 4 model calls total

| task | kind | arm | rep | obj_pass | declined | steps/seq | calls | wall_s |
|---|---|---|---|---|---|---|---|---|
| task_1_stringcalc | implement | orchestrated | 1 | True | False | planner/implementer/reviewer | 4 | 32.8 |

## For the findings entry
- M5: orchestrated vs monolith vs M4 fixed chain - pass rate, cost, and whether
  the orchestrator's per-step choices (spawn_sequence + rationales in the decision
  records) reconstruct into a legible strategy.
- End-of-MVP: this closes M0-M5; trigger the findings 1-6 sequence rework.
