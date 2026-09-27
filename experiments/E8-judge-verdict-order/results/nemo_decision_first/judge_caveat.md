# M6 suite run - arm `judge_caveat` (suite 0.4.1)

_2026-09-21 19:37 - 8 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 23.8 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 25.8 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 23.8 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 24.4 |
| hf_misfiled_bug | fix/misdirection | answered | 3/4 | 4/4 | - | True | - | - | 205.2 |
| hf_misfiled_bug | fix/misdirection | answered | 3/4 | 4/4 | - | True | - | - | 179.8 |
| hf_misfiled_bug | fix/misdirection | answered | 3/4 | 4/4 | - | True | - | - | 203.8 |
| hf_misfiled_bug | fix/misdirection | answered | 3/4 | 4/4 | - | True | - | - | 198.5 |

**objective pass 8/8 - regressions 0 - check crashes 0 - decline accuracy 4/4**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| cross-file | 4 | 1.00 |
| premise-audit | 8 | 1.00 |
