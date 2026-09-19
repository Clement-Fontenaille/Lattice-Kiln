# M6 suite run - arm `judge_staged` (suite 0.4.0)

_2026-09-19 12:09 - 7 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 19.5 |
| wf2_retry | feature/edge-coverage | answered | 0/5 | 5/5 | - | True | - | - | 133.6 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 78.1 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 80.4 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 100.6 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 9.1 |
| wf5_partial | implement/edge-coverage | answered | 0/7 | 7/7 | - | True | - | - | 163.4 |

**objective pass 6/7 - regressions 0 - check crashes 0 - decline accuracy 1/1**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 3 | 1.00 |
| cross-file | 1 | 1.00 |
| edge-coverage | 1 | 1.00 |
| greenfield-impl | 2 | 1.00 |
| kway-synth | 1 | 1.00 |
| partial-credit | 1 | 1.00 |
| premise-audit | 2 | 1.00 |
| witness-pair | 2 | 1.00 |
