# M6 suite run - arm `judge_caveat` (suite 0.4.1)

_2026-09-21 23:54 - 8 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_csv | data/edge-coverage | blocked-no-progress | 3/6 | 3/6 | - | False | - | - | 175.5 |
| hf_csv | data/edge-coverage | blocked-partial | 3/6 | 4/6 | - | False | - | - | 247.1 |
| hf_csv | data/edge-coverage | blocked-no-progress | 3/6 | 3/6 | - | False | - | - | 731.3 |
| hf_csv | data/edge-coverage | blocked-no-progress | 3/6 | 3/6 | - | False | - | - | 667.4 |
| hf_csv | data/edge-coverage | blocked-no-progress | 3/6 | 3/6 | - | False | - | - | 596.2 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | False | - | - | 215.4 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | False | - | - | 199.9 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | False | - | - | 149.1 |

**objective pass 0/8 - regressions 0 - check crashes 0 - decline accuracy 0/0**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 3 | 1.00 |
| edge-coverage | 5 | 0.53 |
| kway-synth | 5 | 0.53 |
| partial-credit | 5 | 0.53 |
| regression-guard | 3 | 1.00 |
