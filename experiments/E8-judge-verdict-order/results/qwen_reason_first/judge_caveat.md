# M6 suite run - arm `judge_caveat` (suite 0.4.1)

_2026-09-23 01:55 - 8 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 6.5 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 8.2 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 8.4 |
| hf_return_shape | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 12.6 |
| hf_return_shape | compat/backward-compat | blocked-no-progress | 3/5 | 3/5 | - | False | - | - | 78.8 |
| hf_return_shape | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 17.9 |
| hf_return_shape | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 16.5 |
| hf_return_shape | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 18.0 |

**objective pass 7/8 - regressions 0 - check crashes 0 - decline accuracy 3/3**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| backward-compat | 5 | 0.92 |
| premise-audit | 3 | 1.00 |
| regression-guard | 8 | 0.95 |
