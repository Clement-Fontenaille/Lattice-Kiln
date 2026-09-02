# M6 suite run - arm `baseline` (suite 0.1.0)

_2026-09-02 11:55 - 4 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_deprecate | compat/backward-compat | done | 1/4 | 1/4 | - | False | - | - | 0.0 |
| hf_json_field | feature/backward-compat | done | 2/5 | 2/5 | - | False | - | - | 0.0 |
| hf_multi_recipient | compat/backward-compat | done | 3/5 | 3/5 | - | False | - | - | 0.0 |
| hf_return_shape | compat/backward-compat | done | 3/5 | 3/5 | - | False | - | - | 0.0 |

**objective pass 0/4 - regressions 0 - check crashes 0 - decline accuracy 0/0**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 1 | 0.25 |
| backward-compat | 4 | 0.46 |
| regression-guard | 3 | 0.53 |
