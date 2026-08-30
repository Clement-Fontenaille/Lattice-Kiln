# M5 comparison results

_2026-08-31 00:55 - 24 runs_

- **monolith**: objective pass 6/8, mean wall 5.7s, 8 model calls total
- **ephemeral**: objective pass 5/8, mean wall 20.9s, 24 model calls total
- **orchestrated**: objective pass 7/8, mean wall 25.5s, 40 model calls total

| task | kind | arm | rep | obj_pass | declined | steps/seq | calls | wall_s |
|---|---|---|---|---|---|---|---|---|
| task_1_stringcalc | implement | ephemeral | 1 | True | False | - | 3 | 19.8 |
| task_1_stringcalc | implement | ephemeral | 2 | True | False | - | 3 | 20.2 |
| task_1_stringcalc | implement | monolith | 1 | True | False | - | 1 | 5.3 |
| task_1_stringcalc | implement | monolith | 2 | True | False | - | 1 | 5.0 |
| task_1_stringcalc | implement | orchestrated | 1 | True | False | planner/implementer | 5 | 23.2 |
| task_1_stringcalc | implement | orchestrated | 2 | True | False | planner/implementer | 5 | 22.7 |
| task_2_median | bugfix | ephemeral | 1 | True | False | - | 3 | 19.9 |
| task_2_median | bugfix | ephemeral | 2 | False | False | - | 3 | 17.8 |
| task_2_median | bugfix | monolith | 1 | True | False | - | 1 | 5.4 |
| task_2_median | bugfix | monolith | 2 | True | False | - | 1 | 5.0 |
| task_2_median | bugfix | orchestrated | 1 | True | False | planner/implementer/implementer | 7 | 39.7 |
| task_2_median | bugfix | orchestrated | 2 | False | False | planner/implementer/implementer | 7 | 35.5 |
| task_3_nobug | false_premise | ephemeral | 1 | True | True | - | 3 | 25.4 |
| task_3_nobug | false_premise | ephemeral | 2 | True | True | - | 3 | 27.0 |
| task_3_nobug | false_premise | monolith | 1 | True | True | - | 1 | 9.9 |
| task_3_nobug | false_premise | monolith | 2 | True | True | - | 1 | 4.2 |
| task_3_nobug | false_premise | orchestrated | 1 | True | False | 1 | 1 | 3.9 |
| task_3_nobug | false_premise | orchestrated | 2 | True | False | 1 | 1 | 3.5 |
| task_4_starve | context_starvation | ephemeral | 1 | False | False | - | 3 | 19.0 |
| task_4_starve | context_starvation | ephemeral | 2 | False | False | - | 3 | 18.4 |
| task_4_starve | context_starvation | monolith | 1 | False | False | - | 1 | 5.5 |
| task_4_starve | context_starvation | monolith | 2 | False | False | - | 1 | 4.9 |
| task_4_starve | context_starvation | orchestrated | 1 | True | False | planner/implementer/implementer | 7 | 35.8 |
| task_4_starve | context_starvation | orchestrated | 2 | True | False | planner/implementer/implementer | 7 | 39.3 |

## For the findings entry
- M5: orchestrated vs monolith vs M4 fixed chain - pass rate, cost, and whether
  the orchestrator's per-step choices (spawn_sequence + rationales in the decision
  records) reconstruct into a legible strategy.
- End-of-MVP: this closes M0-M5; trigger the findings 1-6 sequence rework.
