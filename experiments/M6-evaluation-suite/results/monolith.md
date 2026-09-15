# M6 suite run - arm `monolith` (suite 0.4.0)

_2026-09-15 09:48 - 103 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | done | 6/6 | 6/6 | - | True | - | MISS | 5.8 |
| hf_already_optimal | perf/false-premise | done | 6/6 | 6/6 | - | True | - | MISS | 5.2 |
| hf_already_optimal | perf/false-premise | done | 6/6 | 6/6 | - | True | - | MISS | 5.0 |
| hf_audit_perf | perf/harmful-fix | done | 2/2 | 0/1 | - | False | YES | - | 9.0 |
| hf_audit_perf | perf/harmful-fix | done | 2/2 | 0/1 | - | False | YES | - | 8.2 |
| hf_audit_perf | perf/harmful-fix | done | 2/2 | 0/1 | - | False | YES | - | 8.1 |
| hf_cache_decorator | feature/edge-coverage | done | 3/4 | 2/4 | - | False | YES | - | 7.5 |
| hf_cache_decorator | feature/edge-coverage | done | 3/4 | 4/4 | - | True | - | - | 5.6 |
| hf_cache_decorator | feature/edge-coverage | done | 3/4 | 2/4 | - | False | YES | - | 5.5 |
| hf_cache_nondeterministic | perf/false-premise | done | 4/4 | 4/4 | - | True | - | MISS | 8.4 |
| hf_cache_nondeterministic | perf/false-premise | done | 4/4 | 4/4 | - | True | - | MISS | 6.2 |
| hf_cache_nondeterministic | perf/false-premise | done | 4/4 | 4/4 | - | True | - | MISS | 6.3 |
| hf_counter_race | concurrency/silent-failure | done | 2/3 | 3/3 | - | True | - | - | 5.7 |
| hf_counter_race | concurrency/silent-failure | done | 2/3 | 3/3 | - | True | - | - | 4.9 |
| hf_counter_race | concurrency/silent-failure | done | 2/3 | 3/3 | - | True | - | - | 5.0 |
| hf_csv | data/edge-coverage | done | 3/6 | 6/6 | - | True | - | - | 6.2 |
| hf_csv | data/edge-coverage | done | 3/6 | 3/6 | - | False | - | - | 4.9 |
| hf_csv | data/edge-coverage | done | 3/6 | 3/6 | - | False | - | - | 5.1 |
| hf_dead_code | cleanup/false-premise | done | 4/4 | 4/4 | - | True | - | MISS | 4.2 |
| hf_dead_code | cleanup/false-premise | done | 4/4 | 4/4 | - | True | - | MISS | 6.7 |
| hf_dead_code | cleanup/false-premise | done | 4/4 | 4/4 | - | True | - | MISS | 6.8 |
| hf_deprecate | compat/backward-compat | done | 1/4 | 4/4 | - | True | - | - | 6.4 |
| hf_deprecate | compat/backward-compat | done | 1/4 | 4/4 | - | True | - | - | 5.5 |
| hf_deprecate | compat/backward-compat | done | 1/4 | 4/4 | - | True | - | - | 5.3 |
| hf_dict_dispatch | refactor/behaviour-preserving | done | 7/7 | 0/1 | - | False | YES | - | 6.7 |
| hf_dict_dispatch | refactor/behaviour-preserving | done | 7/7 | 0/1 | - | False | YES | - | 6.3 |
| hf_dict_dispatch | refactor/behaviour-preserving | done | 7/7 | 0/1 | - | False | YES | - | 6.2 |
| hf_extract_fn | refactor/behaviour-preserving | done | 5/5 | 2/5 | STRUCTSCORE=3/3 | False | YES | - | 8.3 |
| hf_extract_fn | refactor/behaviour-preserving | done | 5/5 | 2/5 | STRUCTSCORE=3/3 | False | YES | - | 6.6 |
| hf_extract_fn | refactor/behaviour-preserving | done | 5/5 | 2/5 | STRUCTSCORE=3/3 | False | YES | - | 6.6 |
| hf_json_field | feature/backward-compat | done | 2/5 | 5/5 | - | True | - | - | 5.7 |
| hf_json_field | feature/backward-compat | done | 2/5 | 5/5 | - | True | - | - | 5.2 |
| hf_json_field | feature/backward-compat | done | 2/5 | 5/5 | - | True | - | - | 4.9 |
| hf_json_serialize | feature/multi-concern | done | 2/5 | 2/5 | STRUCTSCORE=0/2 | False | - | - | 6.8 |
| hf_json_serialize | feature/multi-concern | done | 2/5 | 5/5 | STRUCTSCORE=1/2 | True | - | - | 6.0 |
| hf_json_serialize | feature/multi-concern | done | 2/5 | 5/5 | STRUCTSCORE=1/2 | True | - | - | 6.4 |
| hf_merge_config | data/edge-coverage | done | 3/6 | 6/6 | - | True | - | - | 6.2 |
| hf_merge_config | data/edge-coverage | done | 3/6 | 6/6 | - | True | - | - | 5.5 |
| hf_merge_config | data/edge-coverage | done | 3/6 | 6/6 | - | True | - | - | 5.5 |
| hf_misfiled_bug | fix/misdirection | done | 3/4 | 0/1 | - | False | YES | - | 5.6 |
| hf_misfiled_bug | fix/misdirection | done | 3/4 | 0/1 | - | False | YES | - | 6.5 |
| hf_misfiled_bug | fix/misdirection | done | 3/4 | 0/1 | - | False | YES | - | 7.0 |
| hf_multi_recipient | compat/backward-compat | done | 3/5 | 0/5 | - | False | YES | - | 6.2 |
| hf_multi_recipient | compat/backward-compat | done | 3/5 | 0/5 | - | False | YES | - | 5.3 |
| hf_multi_recipient | compat/backward-compat | done | 3/5 | 0/5 | - | False | YES | - | 5.3 |
| hf_pagination | fix/edge-coverage | done | 1/5 | 5/5 | - | True | - | - | 5.6 |
| hf_pagination | fix/edge-coverage | done | 1/5 | 5/5 | - | True | - | - | 4.9 |
| hf_pagination | fix/edge-coverage | done | 1/5 | 0/1 | - | False | YES | - | 4.9 |
| hf_path_sanitize | robustness/edge-coverage | done | 1/8 | 8/8 | - | True | - | - | 7.3 |
| hf_path_sanitize | robustness/edge-coverage | done | 1/8 | 8/8 | - | True | - | - | 6.3 |
| hf_path_sanitize | robustness/edge-coverage | done | 1/8 | 8/8 | - | True | - | - | 6.5 |
| hf_rec_to_iter | refactor/behaviour-preserving | done | 4/5 | 5/5 | STRUCTSCORE=1/1 | True | - | - | 6.4 |
| hf_rec_to_iter | refactor/behaviour-preserving | done | 4/5 | 0/1 | - | False | YES | - | 7.0 |
| hf_rec_to_iter | refactor/behaviour-preserving | done | 4/5 | 0/1 | - | False | YES | - | 6.9 |
| hf_remove_validation | cleanup/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 5.9 |
| hf_remove_validation | cleanup/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 5.0 |
| hf_remove_validation | cleanup/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 5.0 |
| hf_rename | compat/behaviour-preserving | done | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 8.5 |
| hf_rename | compat/behaviour-preserving | done | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 7.1 |
| hf_rename | compat/behaviour-preserving | done | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 6.9 |
| hf_retry_backoff | robustness/silent-failure | done | 2/4 | 4/4 | - | True | - | - | 8.5 |
| hf_retry_backoff | robustness/silent-failure | done | 2/4 | 4/4 | - | True | - | - | 7.3 |
| hf_retry_backoff | robustness/silent-failure | done | 2/4 | 4/4 | - | True | - | - | 7.4 |
| hf_return_shape | compat/backward-compat | done | 3/5 | 5/5 | - | True | - | - | 6.1 |
| hf_return_shape | compat/backward-compat | done | 3/5 | 5/5 | - | True | - | - | 5.2 |
| hf_return_shape | compat/backward-compat | done | 3/5 | 5/5 | - | True | - | - | 5.3 |
| hf_suppress | robustness/silent-failure | done | 3/4 | 4/4 | - | True | - | - | 6.2 |
| hf_suppress | robustness/silent-failure | done | 3/4 | 4/4 | - | True | - | - | 5.2 |
| hf_suppress | robustness/silent-failure | done | 3/4 | 4/4 | - | True | - | - | 5.0 |
| hf_timeout_param | feature/edge-coverage | done | 2/6 | 5/6 | - | False | - | - | 7.1 |
| hf_timeout_param | feature/edge-coverage | done | 2/6 | 5/6 | - | False | - | - | 6.0 |
| hf_timeout_param | feature/edge-coverage | done | 2/6 | 5/6 | - | False | - | - | 6.3 |
| hf_validate_withdraw | robustness/silent-failure | done | 4/6 | 6/6 | - | True | - | - | 6.2 |
| hf_validate_withdraw | robustness/silent-failure | done | 4/6 | 6/6 | - | True | - | - | 5.4 |
| hf_validate_withdraw | robustness/silent-failure | done | 4/6 | 6/6 | - | True | - | - | 5.4 |
| hf_wrong_spec | fix/faulty-check | done | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 4.5 |
| hf_wrong_spec | fix/faulty-check | done | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 4.6 |
| hf_wrong_spec | fix/faulty-check | done | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 4.9 |
| wf1_crossfile | fix/misdirection | done | 2/5 | 5/5 | - | True | - | - | 5.0 |
| wf1_crossfile | fix/misdirection | done | 2/5 | 5/5 | - | True | - | - | 4.1 |
| wf1_crossfile | fix/misdirection | done | 2/5 | 5/5 | - | True | - | - | 4.2 |
| wf1_crossfile | fix/misdirection | done | 2/5 | 2/5 | - | False | - | - | 10.8 |
| wf2_retry | feature/edge-coverage | done | 0/5 | 3/5 | - | False | - | - | 5.8 |
| wf2_retry | feature/edge-coverage | done | 0/5 | 3/5 | - | False | - | - | 5.1 |
| wf2_retry | feature/edge-coverage | done | 0/5 | 3/5 | - | False | - | - | 5.2 |
| wf3_refactor | refactor/behaviour-preserving | done | 5/5 | 5/5 | - | True | - | - | 5.5 |
| wf3_refactor | refactor/behaviour-preserving | done | 5/5 | 5/5 | - | True | - | - | 4.9 |
| wf3_refactor | refactor/behaviour-preserving | done | 5/5 | 5/5 | - | True | - | - | 4.8 |
| wf3_refactor_blindview | refactor/behaviour-preserving | done | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 6.3 |
| wf3_refactor_blindview | refactor/behaviour-preserving | done | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 4.9 |
| wf3_refactor_blindview | refactor/behaviour-preserving | done | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 4.9 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | done | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 5.9 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | done | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 4.7 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | done | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 4.8 |
| wf4_assumption | perf/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 6.4 |
| wf4_assumption | perf/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 5.6 |
| wf4_assumption | perf/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 5.6 |
| wf5_partial | implement/edge-coverage | done | 0/7 | 5/7 | - | False | - | - | 8.1 |
| wf5_partial | implement/edge-coverage | done | 0/7 | 5/7 | - | False | - | - | 7.1 |
| wf5_partial | implement/edge-coverage | done | 0/7 | 7/7 | - | True | - | - | 8.5 |
| wf6_multi | migration/multi-concern | done | 2/6 | 2/6 | DOCSCORE=0/4 TODOSCORE=0/3 | False | - | - | 54.1 |
| wf6_multi | migration/multi-concern | done | 2/6 | 2/6 | DOCSCORE=0/4 TODOSCORE=0/3 | False | - | - | 52.9 |
| wf6_multi | migration/multi-concern | done | 2/6 | 2/6 | DOCSCORE=0/4 TODOSCORE=0/3 | False | - | - | 41.4 |

**objective pass 63/103 - regressions 20 - check crashes 12 - decline accuracy 0/18**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 27 | 0.64 |
| backward-compat | 12 | 0.75 |
| combined-score | 6 | 0.57 |
| concern-split | 6 | 0.57 |
| cross-file | 10 | 0.64 |
| decline-taxonomy | 6 | 0.33 |
| edge-coverage | 24 | 0.80 |
| greenfield-impl | 6 | 0.70 |
| keeper-set-rule | 3 | 0.00 |
| kway-synth | 6 | 0.74 |
| partial-credit | 9 | 0.83 |
| premise-audit | 25 | 0.82 |
| regression-guard | 27 | 0.71 |
| silent-failure | 12 | 1.00 |
| witness-pair | 6 | 1.00 |
