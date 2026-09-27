# M6 suite run - arm `judge_bypass` (suite 0.4.1)

_2026-09-21 16:20 - 2 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 105.6 |
| hf_multi_recipient | compat/backward-compat | blocked-no-progress | 3/5 | 3/5 | - | False | - | - | 102.5 |

**objective pass 1/2 - regressions 0 - check crashes 0 - decline accuracy 0/0**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| backward-compat | 2 | 0.80 |
| regression-guard | 2 | 0.80 |
