# M6 suite run - arm `dloop` (suite 0.1.0)

_2026-09-14 09:00 - 25 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| wf1_crossfile | fix/misdirection | resolved | 2/5 | 5/5 | - | True | - | - | 163.0 |
| wf1_crossfile | fix/misdirection | resolved | 2/5 | 5/5 | - | True | - | - | 4.4 |
| wf1_crossfile | fix/misdirection | resolved | 2/5 | 5/5 | - | True | - | - | 23.2 |
| wf1_crossfile | fix/misdirection | escalate | 2/5 | 2/5 | - | False | - | - | 29.4 |
| wf1_crossfile | fix/misdirection | resolved | 2/5 | 5/5 | - | True | - | - | 4.4 |
| wf2_retry | feature/edge-coverage | resolved | 0/5 | 5/5 | - | True | - | - | 5.8 |
| wf2_retry | feature/edge-coverage | resolved | 0/5 | 5/5 | - | True | - | - | 5.4 |
| wf2_retry | feature/edge-coverage | resolved | 0/5 | 5/5 | - | True | - | - | 5.1 |
| wf2_retry | feature/edge-coverage | needs-change | 0/5 | 3/5 | - | False | - | - | 16.7 |
| wf2_retry | feature/edge-coverage | resolved | 0/5 | 5/5 | - | True | - | - | 11.4 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 0.2 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 0.2 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 0.2 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 0.2 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 0.2 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 0.2 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 0.2 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 0.2 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 0.2 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 0.2 |
| wf5_partial | implement/edge-coverage | needs-change | 0/7 | 5/7 | - | False | - | - | 23.6 |
| wf5_partial | implement/edge-coverage | needs-change | 0/7 | 5/7 | - | False | - | - | 23.3 |
| wf5_partial | implement/edge-coverage | resolved | 0/7 | 7/7 | - | True | - | - | 8.5 |
| wf5_partial | implement/edge-coverage | needs-change | 0/7 | 5/7 | - | False | - | - | 26.9 |
| wf5_partial | implement/edge-coverage | resolved | 0/7 | 7/7 | - | True | - | - | 9.4 |

**objective pass 20/25 - regressions 0 - check crashes 0 - decline accuracy 5/5**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 5 | 1.00 |
| cross-file | 5 | 0.88 |
| edge-coverage | 5 | 0.92 |
| greenfield-impl | 10 | 0.87 |
| kway-synth | 5 | 0.83 |
| partial-credit | 5 | 0.83 |
| premise-audit | 10 | 0.94 |
