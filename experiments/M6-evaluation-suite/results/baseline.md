# M6 suite run - arm `baseline` (suite 0.1.0)

_2026-09-02 11:58 - 5 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_cache_decorator | feature/edge-coverage | done | 3/4 | 3/4 | - | False | - | - | 0.0 |
| hf_csv | data/edge-coverage | done | 3/6 | 3/6 | - | False | - | - | 0.0 |
| hf_merge_config | data/edge-coverage | done | 3/6 | 3/6 | - | False | - | - | 0.0 |
| hf_path_sanitize | robustness/edge-coverage | done | 1/8 | 1/8 | - | False | - | - | 0.0 |
| hf_timeout_param | feature/edge-coverage | done | 2/6 | 2/6 | - | False | - | - | 0.0 |

**objective pass 0/5 - regressions 0 - check crashes 0 - decline accuracy 0/0**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| edge-coverage | 5 | 0.44 |
| kway-synth | 1 | 0.50 |
| partial-credit | 2 | 0.31 |
