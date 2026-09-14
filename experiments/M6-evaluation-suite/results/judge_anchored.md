# M6 suite run - arm `judge_anchored` (suite 0.3.0)

_2026-09-14 11:59 - 3 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 7.8 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 3/5 | - | False | - | - | 107.3 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 133.3 |

**objective pass 1/3 - regressions 0 - check crashes 0 - decline accuracy 1/1**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 1 | 1.00 |
| edge-coverage | 1 | 0.60 |
| greenfield-impl | 1 | 0.60 |
| premise-audit | 1 | 1.00 |
| witness-pair | 1 | 1.00 |
