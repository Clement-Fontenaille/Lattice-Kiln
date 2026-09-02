# M6 suite run - arm `monolith` (suite 0.1.0)

_2026-09-02 12:14 - 5 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| wf1_crossfile | fix/misdirection | done | 2/5 | 2/5 | - | False | - | - | 12.0 |
| wf2_retry | feature/edge-coverage | done | 0/5 | 5/5 | - | True | - | - | 6.2 |
| wf3_refactor | refactor/behaviour-preserving | done | 5/5 | 5/5 | - | True | - | - | 5.4 |
| wf4_assumption | perf/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 9.4 |
| wf5_partial | implement/edge-coverage | done | 0/7 | 5/7 | - | False | - | - | 8.7 |

**objective pass 3/5 - regressions 0 - check crashes 0 - decline accuracy 0/1**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 1 | 1.00 |
| cross-file | 1 | 0.40 |
| edge-coverage | 1 | 1.00 |
| greenfield-impl | 2 | 0.86 |
| kway-synth | 1 | 0.71 |
| partial-credit | 1 | 0.71 |
| premise-audit | 2 | 0.70 |
