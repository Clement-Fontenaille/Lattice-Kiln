# M6 suite run - arm `judge_anchored` (suite 0.4.1)

_2026-09-23 05:14 - 8 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_merge_config | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 70.2 |
| hf_merge_config | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 61.0 |
| hf_merge_config | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 68.6 |
| hf_merge_config | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 59.5 |
| hf_rename | compat/behaviour-preserving | answered | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 89.1 |
| hf_rename | compat/behaviour-preserving | answered | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 102.1 |
| hf_rename | compat/behaviour-preserving | blocked-no-progress | 4/6 | 4/6 | STRUCTSCORE=2/3 | False | - | - | 78.8 |
| hf_rename | compat/behaviour-preserving | answered | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 83.1 |

**objective pass 7/8 - regressions 0 - check crashes 0 - decline accuracy 0/0**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 4 | 0.92 |
| edge-coverage | 4 | 1.00 |
| regression-guard | 4 | 0.92 |
