# M6 suite run - arm `judge_anchored` (suite 0.4.1)

_2026-09-21 16:09 - 8 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 65.4 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 63.2 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 49.6 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 46.6 |
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 138.5 |
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 114.8 |
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 205.4 |
| hf_multi_recipient | compat/backward-compat | blocked-no-progress | 3/5 | 3/5 | - | False | - | - | 181.8 |

**objective pass 7/8 - regressions 0 - check crashes 0 - decline accuracy 4/4**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| backward-compat | 4 | 0.90 |
| premise-audit | 4 | 1.00 |
| regression-guard | 4 | 0.90 |
