# M6 suite run - arm `monolith` (suite 0.1.0)

_2026-09-02 12:18 - 30 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | done | 6/6 | 6/6 | - | True | - | MISS | 6.2 |
| hf_cache_decorator | feature/edge-coverage | done | 3/4 | 3/4 | - | False | YES | - | 6.1 |
| hf_cache_nondeterministic | perf/false-premise | done | 4/4 | 4/4 | - | True | - | MISS | 5.8 |
| hf_counter_race | concurrency/silent-failure | done | 2/3 | 3/3 | - | True | - | - | 5.8 |
| hf_csv | data/edge-coverage | done | 3/6 | 3/6 | - | False | - | - | 5.7 |
| hf_dead_code | cleanup/false-premise | done | 4/4 | 1/4 | - | False | YES | MISS | 6.5 |
| hf_deprecate | compat/backward-compat | done | 1/4 | 4/4 | - | True | - | - | 6.4 |
| hf_dict_dispatch | refactor/behaviour-preserving | done | 7/7 | 0/1 | - | False | YES | - | 7.5 |
| hf_extract_fn | refactor/behaviour-preserving | done | 5/5 | 3/5 | STRUCTSCORE=3/3 | False | YES | - | 8.4 |
| hf_json_field | feature/backward-compat | done | 2/5 | 5/5 | - | True | - | - | 5.7 |
| hf_json_serialize | feature/multi-concern | done | 2/5 | 5/5 | STRUCTSCORE=1/2 | True | - | - | 7.4 |
| hf_merge_config | data/edge-coverage | done | 3/6 | 6/6 | - | True | - | - | 6.3 |
| hf_misfiled_bug | fix/misdirection | done | 3/4 | 0/1 | - | False | YES | - | 8.4 |
| hf_multi_recipient | compat/backward-compat | done | 3/5 | 3/5 | - | False | - | - | 6.1 |
| hf_pagination | fix/edge-coverage | done | 1/5 | 0/1 | - | False | YES | - | 6.0 |
| hf_path_sanitize | robustness/edge-coverage | done | 1/8 | 8/8 | - | True | - | - | 7.2 |
| hf_rec_to_iter | refactor/behaviour-preserving | done | 4/5 | 5/5 | STRUCTSCORE=1/1 | True | - | - | 6.3 |
| hf_remove_validation | cleanup/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 5.9 |
| hf_rename | compat/behaviour-preserving | done | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 7.9 |
| hf_retry_backoff | robustness/silent-failure | done | 2/4 | 4/4 | - | True | - | - | 8.4 |
| hf_return_shape | compat/backward-compat | done | 3/5 | 5/5 | - | True | - | - | 6.3 |
| hf_suppress | robustness/silent-failure | done | 3/4 | 4/4 | - | True | - | - | 6.4 |
| hf_timeout_param | feature/edge-coverage | done | 2/6 | 0/1 | - | False | YES | - | 8.7 |
| hf_validate_withdraw | robustness/silent-failure | done | 4/6 | 6/6 | - | True | - | - | 6.3 |
| wf1_crossfile | fix/misdirection | done | 2/5 | 2/5 | - | False | - | - | 12.0 |
| wf2_retry | feature/edge-coverage | done | 0/5 | 5/5 | - | True | - | - | 6.2 |
| wf3_refactor | refactor/behaviour-preserving | done | 5/5 | 5/5 | - | True | - | - | 5.4 |
| wf4_assumption | perf/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 9.4 |
| wf5_partial | implement/edge-coverage | done | 0/7 | 5/7 | - | False | - | - | 8.7 |
| wf6_multi | migration/multi-concern | done | 2/6 | 2/6 | DOCSCORE=0/4 TODOSCORE=0/3 | False | - | - | 56.1 |

**objective pass 18/30 - regressions 7 - check crashes 4 - decline accuracy 0/5**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 6 | 0.77 |
| backward-compat | 4 | 0.90 |
| combined-score | 2 | 0.67 |
| concern-split | 2 | 0.67 |
| cross-file | 3 | 0.47 |
| edge-coverage | 8 | 0.66 |
| greenfield-impl | 2 | 0.86 |
| kway-synth | 2 | 0.61 |
| partial-credit | 3 | 0.74 |
| premise-audit | 7 | 0.66 |
| regression-guard | 9 | 0.80 |
| silent-failure | 4 | 1.00 |
