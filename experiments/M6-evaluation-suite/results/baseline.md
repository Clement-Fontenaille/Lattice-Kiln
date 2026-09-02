# M6 suite run - arm `baseline` (suite 0.1.0)

_2026-09-02 11:34 - 10 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_dict_dispatch | refactor/behaviour-preserving | done | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 0.0 |
| hf_extract_fn | refactor/behaviour-preserving | done | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 0.0 |
| hf_rec_to_iter | refactor/behaviour-preserving | done | 4/5 | 4/5 | STRUCTSCORE=0/1 | False | - | - | 0.0 |
| hf_rename | compat/behaviour-preserving | done | 4/6 | 4/6 | STRUCTSCORE=2/3 | False | - | - | 0.0 |
| wf1_crossfile | fix/misdirection | done | 2/5 | 2/5 | - | False | - | - | 0.0 |
| wf2_retry | feature/edge-coverage | done | 0/5 | 0/5 | - | False | - | - | 0.0 |
| wf3_refactor | refactor/behaviour-preserving | done | 5/5 | 5/5 | - | True | - | - | 0.0 |
| wf4_assumption | perf/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 0.0 |
| wf5_partial | implement/edge-coverage | done | 0/7 | 0/7 | - | False | - | - | 0.0 |
| wf6_multi | migration/multi-concern | done | 2/6 | 2/6 | DOCSCORE=0/4 TODOSCORE=0/3 | False | - | - | 0.0 |

**objective pass 4/10 · regressions 0 · check crashes 0 · decline accuracy 0/1**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 5 | 0.89 |
| combined-score | 1 | 0.33 |
| concern-split | 1 | 0.33 |
| cross-file | 1 | 0.40 |
| edge-coverage | 1 | 0.00 |
| greenfield-impl | 2 | 0.00 |
| kway-synth | 1 | 0.00 |
| partial-credit | 1 | 0.00 |
| premise-audit | 2 | 0.70 |
| regression-guard | 3 | 0.89 |
