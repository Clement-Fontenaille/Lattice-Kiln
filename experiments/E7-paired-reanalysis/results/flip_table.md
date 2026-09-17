# E7 — M4 vs M5 flip table

Generated 2026-09-17T11:15:24.988809+00:00.

## Headline check

| milestone | arm | published | recomputed | match |
|---|---|---|---|---|
| m4 | monolith | 6/8 | 6/8 | yes |
| m4 | ephemeral | 5/8 | 5/8 | yes |
| m5 | monolith | 6/8 | 6/8 | yes |
| m5 | ephemeral | 5/8 | 5/8 | yes |
| m5 | orchestrated | 7/8 | 7/8 | yes |

**Matches published: True**

## Paired cells (arms present in both milestones)

| task | arm | rep | M4 | M5 | label |
|---|---|---|---|---|---|
| task_1_stringcalc | ephemeral | 1 | pass | pass | stable_pass |
| task_1_stringcalc | ephemeral | 2 | pass | pass | stable_pass |
| task_1_stringcalc | monolith | 1 | pass | pass | stable_pass |
| task_1_stringcalc | monolith | 2 | pass | pass | stable_pass |
| task_2_median | ephemeral | 1 | fail | pass | unstable |
| task_2_median | ephemeral | 2 | pass | fail | unstable |
| task_2_median | monolith | 1 | fail | pass | unstable |
| task_2_median | monolith | 2 | pass | pass | unstable |
| task_3_nobug | ephemeral | 1 | pass | pass | stable_pass |
| task_3_nobug | ephemeral | 2 | pass | pass | stable_pass |
| task_3_nobug | monolith | 1 | pass | pass | stable_pass |
| task_3_nobug | monolith | 2 | pass | pass | stable_pass |
| task_4_starve | ephemeral | 1 | fail | fail | stable_fail |
| task_4_starve | ephemeral | 2 | fail | fail | stable_fail |
| task_4_starve | monolith | 1 | pass | fail | unstable |
| task_4_starve | monolith | 2 | fail | fail | unstable |

## Summary

- **gained**: 0
- **lost**: 0
- **stable_pass**: 8
- **stable_fail**: 2
- **unstable**: 6

Rep-unstable cells — M4: task_2_median/ephemeral, task_2_median/monolith, task_4_starve/monolith
Rep-unstable cells — M5: task_2_median/ephemeral, task_2_median/orchestrated

## M5 within-milestone (arms only in M5: orchestrated)

Passes out of 2 reps.

| task | ephemeral | monolith | orchestrated |
|---|---|---|---|
| task_1_stringcalc | 2/2 | 2/2 | 2/2 |
| task_2_median | 1/2 | 2/2 | 1/2 |
| task_3_nobug | 2/2 | 2/2 | 2/2 |
| task_4_starve | 0/2 | 0/2 | 2/2 |

## Limitations

- objective_pass is the gating metric only (E0 defect 1); M4/M5 records carry no structural dimensions to fold in
- stresses tags absent from M4/M5 records; kind used instead; tag-clustering question unanswerable from this data
- 4 tasks x 2 reps per arm: any pattern is directional, not decisive
- the orchestrated arm exists only in M5 and therefore cannot flip
