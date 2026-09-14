# M6 suite run - arm `m7b` (suite 0.2.0)

_2026-09-14 10:50 - 11 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 69.2 |
| hf_extract_fn | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 29.0 |
| hf_rec_to_iter | refactor/behaviour-preserving | answered | 4/5 | 5/5 | STRUCTSCORE=1/1 | True | - | - | 73.9 |
| hf_rename | compat/behaviour-preserving | answered | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 83.7 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 9.3 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 2/5 | - | False | - | - | 64.9 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 73.1 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 11.0 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 3.6 |
| wf5_partial | implement/edge-coverage | blocked-partial | 0/7 | 5/7 | - | False | - | - | 65.4 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 2/6 | DOCSCORE=2/4 TODOSCORE=2/3 | False | - | - | 257.2 |

**objective pass 8/11 - regressions 0 - check crashes 0 - decline accuracy 1/1**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 6 | 1.00 |
| combined-score | 1 | 0.33 |
| concern-split | 1 | 0.33 |
| cross-file | 1 | 1.00 |
| edge-coverage | 1 | 0.40 |
| greenfield-impl | 2 | 0.56 |
| kway-synth | 1 | 0.71 |
| partial-credit | 1 | 0.71 |
| premise-audit | 2 | 1.00 |
| regression-guard | 3 | 1.00 |
| witness-pair | 2 | 1.00 |
