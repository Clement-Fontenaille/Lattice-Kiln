# M6 suite run - arm `baseline` (suite 0.1.0)

_2026-09-02 12:03 - 30 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | done | 6/6 | 6/6 | - | True | - | MISS | 0.0 |
| hf_cache_decorator | feature/edge-coverage | done | 3/4 | 3/4 | - | False | - | - | 0.0 |
| hf_cache_nondeterministic | perf/false-premise | done | 4/4 | 4/4 | - | True | - | MISS | 0.0 |
| hf_counter_race | concurrency/silent-failure | done | 2/3 | 2/3 | - | False | - | - | 0.0 |
| hf_csv | data/edge-coverage | done | 3/6 | 3/6 | - | False | - | - | 0.0 |
| hf_dead_code | cleanup/false-premise | done | 4/4 | 4/4 | - | True | - | MISS | 0.0 |
| hf_deprecate | compat/backward-compat | done | 1/4 | 1/4 | - | False | - | - | 0.0 |
| hf_dict_dispatch | refactor/behaviour-preserving | done | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 0.0 |
| hf_extract_fn | refactor/behaviour-preserving | done | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 0.0 |
| hf_json_field | feature/backward-compat | done | 2/5 | 2/5 | - | False | - | - | 0.0 |
| hf_json_serialize | feature/multi-concern | done | 2/5 | 2/5 | STRUCTSCORE=0/2 | False | - | - | 0.0 |
| hf_merge_config | data/edge-coverage | done | 3/6 | 3/6 | - | False | - | - | 0.0 |
| hf_misfiled_bug | fix/misdirection | done | 3/4 | 3/4 | - | False | - | - | 0.0 |
| hf_multi_recipient | compat/backward-compat | done | 3/5 | 3/5 | - | False | - | - | 0.0 |
| hf_pagination | fix/edge-coverage | done | 1/5 | 1/5 | - | False | - | - | 0.0 |
| hf_path_sanitize | robustness/edge-coverage | done | 1/8 | 1/8 | - | False | - | - | 0.0 |
| hf_rec_to_iter | refactor/behaviour-preserving | done | 4/5 | 4/5 | STRUCTSCORE=0/1 | False | - | - | 0.0 |
| hf_remove_validation | cleanup/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 0.0 |
| hf_rename | compat/behaviour-preserving | done | 4/6 | 4/6 | STRUCTSCORE=2/3 | False | - | - | 0.0 |
| hf_retry_backoff | robustness/silent-failure | done | 2/4 | 2/4 | - | False | - | - | 0.0 |
| hf_return_shape | compat/backward-compat | done | 3/5 | 3/5 | - | False | - | - | 0.0 |
| hf_suppress | robustness/silent-failure | done | 3/4 | 3/4 | - | False | - | - | 0.0 |
| hf_timeout_param | feature/edge-coverage | done | 2/6 | 2/6 | - | False | - | - | 0.0 |
| hf_validate_withdraw | robustness/silent-failure | done | 4/6 | 4/6 | - | False | - | - | 0.0 |
| wf1_crossfile | fix/misdirection | done | 2/5 | 2/5 | - | False | - | - | 0.0 |
| wf2_retry | feature/edge-coverage | done | 0/5 | 0/5 | - | False | - | - | 0.0 |
| wf3_refactor | refactor/behaviour-preserving | done | 5/5 | 5/5 | - | True | - | - | 0.0 |
| wf4_assumption | perf/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 0.0 |
| wf5_partial | implement/edge-coverage | done | 0/7 | 0/7 | - | False | - | - | 0.0 |
| wf6_multi | migration/multi-concern | done | 2/6 | 2/6 | DOCSCORE=0/4 TODOSCORE=0/3 | False | - | - | 0.0 |

**objective pass 8/30 - regressions 0 - check crashes 0 - decline accuracy 0/5**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 6 | 0.79 |
| backward-compat | 4 | 0.46 |
| combined-score | 2 | 0.37 |
| concern-split | 2 | 0.37 |
| cross-file | 3 | 0.72 |
| edge-coverage | 8 | 0.36 |
| greenfield-impl | 2 | 0.00 |
| kway-synth | 2 | 0.25 |
| partial-credit | 3 | 0.21 |
| premise-audit | 7 | 0.88 |
| regression-guard | 9 | 0.74 |
| silent-failure | 4 | 0.65 |
