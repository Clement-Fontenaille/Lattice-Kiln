# M6 suite run - arm `test_synth` (suite 0.3.0)

_2026-09-14 12:47 - 33 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 39.2 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 15.8 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 51.3 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 66.1 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 79.9 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 3/5 | - | False | - | - | 76.7 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 3/5 | - | False | - | - | 84.6 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 3/5 | - | False | - | - | 194.2 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 2/5 | - | False | - | - | 82.2 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 3/5 | - | False | - | - | 74.4 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 12.8 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 65.3 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 12.8 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 84.0 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 67.5 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 95.7 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 14.8 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 68.2 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 102.8 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 14.5 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 86.0 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 128.6 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 17.6 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 73.7 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 16.3 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 9.5 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 9.0 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 10.1 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 19.3 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 9.2 |
| wf5_partial | implement/edge-coverage | answered | 0/7 | 7/7 | - | True | - | - | 65.3 |
| wf5_partial | implement/edge-coverage | answered | 0/7 | 7/7 | - | True | - | - | 73.5 |
| wf5_partial | implement/edge-coverage | blocked-partial | 0/7 | 5/7 | - | False | - | - | 96.0 |

**objective pass 22/33 - regressions 0 - check crashes 0 - decline accuracy 5/5**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 15 | 1.00 |
| cross-file | 5 | 1.00 |
| edge-coverage | 5 | 0.56 |
| greenfield-impl | 8 | 0.69 |
| kway-synth | 3 | 0.90 |
| partial-credit | 3 | 0.90 |
| premise-audit | 10 | 1.00 |
| witness-pair | 10 | 1.00 |
