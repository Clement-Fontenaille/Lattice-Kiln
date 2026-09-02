# M6 suite run - arm `baseline` (suite 0.1.0)

_2026-09-02 11:37 - 4 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | done | 6/6 | 6/6 | - | True | - | MISS | 0.0 |
| hf_cache_nondeterministic | perf/false-premise | done | 4/4 | 4/4 | - | True | - | MISS | 0.0 |
| hf_dead_code | cleanup/false-premise | done | 4/4 | 4/4 | - | True | - | MISS | 0.0 |
| hf_remove_validation | cleanup/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 0.0 |

**objective pass 4/4 - regressions 0 - check crashes 0 - decline accuracy 0/4**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| cross-file | 1 | 1.00 |
| premise-audit | 4 | 1.00 |
| regression-guard | 1 | 1.00 |
