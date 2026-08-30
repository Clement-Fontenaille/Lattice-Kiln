# M4 comparison results

_2026-08-30 23:33 - 16 runs_

- **monolith**: objective pass 6/8, mean wall 7.4s, 8 model calls total
- **ephemeral**: objective pass 5/8, mean wall 23.4s, 24 model calls total

| task | kind | arm | rep | obj_pass | declined | reviewer | ctx_reqs | gate_ref | wall_s |
|---|---|---|---|---|---|---|---|---|---|
| task_1_stringcalc | implement | ephemeral | 1 | True | False | approve | 0 | 0 | 27.3 |
| task_1_stringcalc | implement | ephemeral | 2 | True | False | approve | 0 | 0 | 21.4 |
| task_1_stringcalc | implement | monolith | 1 | True | False | - | 0 | 0 | 7.0 |
| task_1_stringcalc | implement | monolith | 2 | True | False | - | 0 | 0 | 6.4 |
| task_2_median | bugfix | ephemeral | 1 | False | False | needs-change | 0 | 0 | 23.9 |
| task_2_median | bugfix | ephemeral | 2 | True | False | approve | 0 | 0 | 21.8 |
| task_2_median | bugfix | monolith | 1 | False | False | - | 0 | 0 | 14.5 |
| task_2_median | bugfix | monolith | 2 | True | False | - | 0 | 0 | 6.7 |
| task_3_nobug | false_premise | ephemeral | 1 | True | True | approve | 0 | 0 | 27.6 |
| task_3_nobug | false_premise | ephemeral | 2 | True | True | approve | 0 | 0 | 19.2 |
| task_3_nobug | false_premise | monolith | 1 | True | True | - | 0 | 0 | 5.9 |
| task_3_nobug | false_premise | monolith | 2 | True | True | - | 0 | 0 | 5.4 |
| task_4_starve | context_starvation | ephemeral | 1 | False | False | approve | 0 | 0 | 24.7 |
| task_4_starve | context_starvation | ephemeral | 2 | False | False | approve | 0 | 0 | 21.4 |
| task_4_starve | context_starvation | monolith | 1 | True | False | - | 0 | 0 | 6.9 |
| task_4_starve | context_starvation | monolith | 2 | False | False | - | 0 | 0 | 6.2 |

## Notes for the findings entries
- M4: compare monolith vs ephemeral objective pass rates above.
- M3: inspect `refused_by_gate` / effect stream for type-boundary blur.
- M2: pick an unplanned question and answer it from the run records.
