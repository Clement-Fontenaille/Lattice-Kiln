# M6 suite run - arm `judge_caveat` (suite 0.4.1)

_2026-09-22 16:30 - 8 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 122.5 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 4.9 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 4.4 |
| hf_return_shape | compat/backward-compat | blocked-no-progress | 3/5 | 3/5 | - | False | - | - | 223.9 |
| hf_return_shape | compat/backward-compat | blocked-no-progress | 3/5 | 3/5 | - | False | - | - | 200.4 |
| hf_return_shape | compat/backward-compat | blocked-no-progress | 3/5 | 3/5 | - | False | - | - | 174.7 |
| hf_return_shape | compat/backward-compat | blocked-no-progress | 3/5 | 3/5 | - | False | - | - | 117.0 |
| hf_return_shape | compat/backward-compat | blocked-no-progress | 3/5 | 3/5 | - | False | - | - | 134.2 |

**objective pass 3/8 - regressions 0 - check crashes 0 - decline accuracy 3/3**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| backward-compat | 5 | 0.60 |
| premise-audit | 3 | 1.00 |
| regression-guard | 8 | 0.75 |
