# M6 suite run - arm `judge_fullctx` (suite 0.4.0)

_2026-09-15 00:39 - 170 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 7.5 |
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 47.3 |
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 46.4 |
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 41.2 |
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 46.9 |
| hf_audit_perf | perf/harmful-fix | answered | 2/2 | 2/2 | PERFSCORE=1/1 AUDITSCORE=1/1 | True | - | - | 15.4 |
| hf_audit_perf | perf/harmful-fix | answered | 2/2 | 2/2 | PERFSCORE=1/1 AUDITSCORE=1/1 | True | - | - | 76.8 |
| hf_audit_perf | perf/harmful-fix | answered | 2/2 | 2/2 | PERFSCORE=1/1 AUDITSCORE=1/1 | True | - | - | 60.4 |
| hf_audit_perf | perf/harmful-fix | answered | 2/2 | 2/2 | PERFSCORE=1/1 AUDITSCORE=1/1 | True | - | - | 15.1 |
| hf_audit_perf | perf/harmful-fix | answered | 2/2 | 2/2 | PERFSCORE=1/1 AUDITSCORE=1/1 | True | - | - | 14.9 |
| hf_cache_decorator | feature/edge-coverage | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 65.6 |
| hf_cache_decorator | feature/edge-coverage | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 52.4 |
| hf_cache_decorator | feature/edge-coverage | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 48.5 |
| hf_cache_decorator | feature/edge-coverage | answered | 3/4 | 4/4 | - | True | - | - | 78.4 |
| hf_cache_decorator | feature/edge-coverage | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 52.5 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 6.7 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 6.3 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 6.4 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 6.5 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 5.9 |
| hf_counter_race | concurrency/silent-failure | answered | 2/3 | 3/3 | - | True | - | - | 16.8 |
| hf_counter_race | concurrency/silent-failure | answered | 2/3 | 3/3 | - | True | - | - | 54.7 |
| hf_counter_race | concurrency/silent-failure | answered | 2/3 | 3/3 | - | True | - | - | 46.0 |
| hf_counter_race | concurrency/silent-failure | answered | 2/3 | 3/3 | - | True | - | - | 57.5 |
| hf_counter_race | concurrency/silent-failure | answered | 2/3 | 3/3 | - | True | - | - | 53.8 |
| hf_csv | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 62.6 |
| hf_csv | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 78.4 |
| hf_csv | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 75.7 |
| hf_csv | data/edge-coverage | blocked-partial | 3/6 | 5/6 | - | False | - | - | 96.1 |
| hf_csv | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 52.3 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 6.7 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 6.2 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 6.2 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 6.2 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 6.3 |
| hf_deprecate | compat/backward-compat | answered | 1/4 | 4/4 | - | True | - | - | 53.9 |
| hf_deprecate | compat/backward-compat | blocked-no-progress | 1/4 | 1/4 | - | False | - | - | 45.4 |
| hf_deprecate | compat/backward-compat | blocked-no-progress | 1/4 | 1/4 | - | False | - | - | 47.1 |
| hf_deprecate | compat/backward-compat | blocked-no-progress | 1/4 | 1/4 | - | False | - | - | 43.9 |
| hf_deprecate | compat/backward-compat | blocked-partial | 1/4 | 3/4 | - | False | - | - | 51.6 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 89.2 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 79.1 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 82.8 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 85.4 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 86.2 |
| hf_extract_fn | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 40.5 |
| hf_extract_fn | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 35.7 |
| hf_extract_fn | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 34.9 |
| hf_extract_fn | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 36.6 |
| hf_extract_fn | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 32.2 |
| hf_json_field | feature/backward-compat | answered | 2/5 | 5/5 | - | True | - | - | 47.7 |
| hf_json_field | feature/backward-compat | answered | 2/5 | 5/5 | - | True | - | - | 45.9 |
| hf_json_field | feature/backward-compat | answered | 2/5 | 5/5 | - | True | - | - | 48.6 |
| hf_json_field | feature/backward-compat | answered | 2/5 | 5/5 | - | True | - | - | 44.6 |
| hf_json_field | feature/backward-compat | answered | 2/5 | 5/5 | - | True | - | - | 44.5 |
| hf_json_serialize | feature/multi-concern | answered | 2/5 | 5/5 | STRUCTSCORE=2/2 | True | - | - | 102.2 |
| hf_json_serialize | feature/multi-concern | answered | 2/5 | 5/5 | STRUCTSCORE=2/2 | True | - | - | 107.9 |
| hf_json_serialize | feature/multi-concern | answered | 2/5 | 5/5 | STRUCTSCORE=2/2 | True | - | - | 128.4 |
| hf_json_serialize | feature/multi-concern | answered | 2/5 | 5/5 | STRUCTSCORE=2/2 | True | - | - | 172.6 |
| hf_json_serialize | feature/multi-concern | answered | 2/5 | 5/5 | STRUCTSCORE=2/2 | True | - | - | 107.8 |
| hf_merge_config | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 92.1 |
| hf_merge_config | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 76.5 |
| hf_merge_config | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 83.1 |
| hf_merge_config | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 67.8 |
| hf_merge_config | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 88.9 |
| hf_misfiled_bug | fix/misdirection | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 25.0 |
| hf_misfiled_bug | fix/misdirection | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 41.6 |
| hf_misfiled_bug | fix/misdirection | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 29.5 |
| hf_misfiled_bug | fix/misdirection | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 42.8 |
| hf_misfiled_bug | fix/misdirection | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 25.2 |
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 81.8 |
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 47.4 |
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 59.4 |
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 68.3 |
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 59.2 |
| hf_pagination | fix/edge-coverage | answered | 1/5 | 5/5 | - | True | - | - | 13.1 |
| hf_pagination | fix/edge-coverage | answered | 1/5 | 5/5 | - | True | - | - | 45.5 |
| hf_pagination | fix/edge-coverage | answered | 1/5 | 5/5 | - | True | - | - | 12.2 |
| hf_pagination | fix/edge-coverage | answered | 1/5 | 5/5 | - | True | - | - | 11.7 |
| hf_pagination | fix/edge-coverage | answered | 1/5 | 5/5 | - | True | - | - | 47.8 |
| hf_path_sanitize | robustness/edge-coverage | answered | 1/8 | 8/8 | - | True | - | - | 76.6 |
| hf_path_sanitize | robustness/edge-coverage | answered | 1/8 | 8/8 | - | True | - | - | 15.8 |
| hf_path_sanitize | robustness/edge-coverage | answered | 1/8 | 8/8 | - | True | - | - | 17.2 |
| hf_path_sanitize | robustness/edge-coverage | answered | 1/8 | 8/8 | - | True | - | - | 84.0 |
| hf_path_sanitize | robustness/edge-coverage | answered | 1/8 | 8/8 | - | True | - | - | 16.5 |
| hf_rec_to_iter | refactor/behaviour-preserving | blocked-no-progress | 4/5 | 4/5 | STRUCTSCORE=0/1 | False | - | - | 107.8 |
| hf_rec_to_iter | refactor/behaviour-preserving | blocked-no-progress | 4/5 | 4/5 | STRUCTSCORE=0/1 | False | - | - | 98.4 |
| hf_rec_to_iter | refactor/behaviour-preserving | answered | 4/5 | 5/5 | STRUCTSCORE=1/1 | True | - | - | 91.7 |
| hf_rec_to_iter | refactor/behaviour-preserving | answered | 4/5 | 5/5 | STRUCTSCORE=1/1 | True | - | - | 92.7 |
| hf_rec_to_iter | refactor/behaviour-preserving | blocked-no-progress | 4/5 | 4/5 | STRUCTSCORE=0/1 | False | - | - | 102.8 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 7.4 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 7.2 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 6.9 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 7.0 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 6.7 |
| hf_rename | compat/behaviour-preserving | answered | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 58.7 |
| hf_rename | compat/behaviour-preserving | answered | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 49.7 |
| hf_rename | compat/behaviour-preserving | blocked-no-progress | 4/6 | 4/6 | STRUCTSCORE=2/3 | False | - | - | 74.1 |
| hf_rename | compat/behaviour-preserving | blocked-no-progress | 4/6 | 4/6 | STRUCTSCORE=2/3 | False | - | - | 68.6 |
| hf_rename | compat/behaviour-preserving | answered | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 67.2 |
| hf_retry_backoff | robustness/silent-failure | answered | 2/4 | 4/4 | - | True | - | - | 67.1 |
| hf_retry_backoff | robustness/silent-failure | answered | 2/4 | 4/4 | - | True | - | - | 116.3 |
| hf_retry_backoff | robustness/silent-failure | answered | 2/4 | 4/4 | - | True | - | - | 121.3 |
| hf_retry_backoff | robustness/silent-failure | answered | 2/4 | 4/4 | - | True | - | - | 105.2 |
| hf_retry_backoff | robustness/silent-failure | answered | 2/4 | 4/4 | - | True | - | - | 59.7 |
| hf_return_shape | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 86.7 |
| hf_return_shape | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 56.9 |
| hf_return_shape | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 71.0 |
| hf_return_shape | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 54.7 |
| hf_return_shape | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 67.7 |
| hf_suppress | robustness/silent-failure | answered | 3/4 | 4/4 | - | True | - | - | 101.7 |
| hf_suppress | robustness/silent-failure | answered | 3/4 | 4/4 | - | True | - | - | 87.8 |
| hf_suppress | robustness/silent-failure | answered | 3/4 | 4/4 | - | True | - | - | 46.8 |
| hf_suppress | robustness/silent-failure | answered | 3/4 | 4/4 | - | True | - | - | 13.9 |
| hf_suppress | robustness/silent-failure | answered | 3/4 | 4/4 | - | True | - | - | 57.7 |
| hf_timeout_param | feature/edge-coverage | answered | 2/6 | 6/6 | - | True | - | - | 85.2 |
| hf_timeout_param | feature/edge-coverage | blocked-partial | 2/6 | 5/6 | - | False | - | - | 83.4 |
| hf_timeout_param | feature/edge-coverage | blocked-partial | 2/6 | 5/6 | - | False | - | - | 82.6 |
| hf_timeout_param | feature/edge-coverage | blocked-partial | 2/6 | 4/6 | - | False | - | - | 83.8 |
| hf_timeout_param | feature/edge-coverage | blocked-partial | 2/6 | 5/6 | - | False | - | - | 90.3 |
| hf_validate_withdraw | robustness/silent-failure | answered | 4/6 | 6/6 | - | True | - | - | 105.2 |
| hf_validate_withdraw | robustness/silent-failure | answered | 4/6 | 6/6 | - | True | - | - | 89.8 |
| hf_validate_withdraw | robustness/silent-failure | answered | 4/6 | 6/6 | - | True | - | - | 87.6 |
| hf_validate_withdraw | robustness/silent-failure | answered | 4/6 | 6/6 | - | True | - | - | 94.8 |
| hf_validate_withdraw | robustness/silent-failure | answered | 4/6 | 6/6 | - | True | - | - | 98.2 |
| hf_wrong_spec | fix/faulty-check | answered | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 104.7 |
| hf_wrong_spec | fix/faulty-check | answered | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 58.3 |
| hf_wrong_spec | fix/faulty-check | blocked-no-progress | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 57.3 |
| hf_wrong_spec | fix/faulty-check | blocked-no-progress | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 49.3 |
| hf_wrong_spec | fix/faulty-check | blocked-no-progress | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 47.7 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 13.4 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 11.6 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 42.0 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 45.7 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 41.4 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 3/5 | - | False | - | - | 79.2 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 2/5 | - | False | - | - | 95.2 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 3/5 | - | False | - | - | 88.8 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 3/5 | - | False | - | - | 78.1 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 2/5 | - | False | - | - | 82.3 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 9.1 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 105.1 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 67.4 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 7.8 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 82.2 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 7.3 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 97.9 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 131.5 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 83.8 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 7.2 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 149.9 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 17.2 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 116.6 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 14.3 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 15.3 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 7.1 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 6.5 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 6.5 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 6.7 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 6.7 |
| wf5_partial | implement/edge-coverage | blocked-partial | 0/7 | 5/7 | - | False | - | - | 101.4 |
| wf5_partial | implement/edge-coverage | blocked-partial | 0/7 | 5/7 | - | False | - | - | 52.0 |
| wf5_partial | implement/edge-coverage | blocked-partial | 0/7 | 1/7 | - | False | - | - | 136.6 |
| wf5_partial | implement/edge-coverage | blocked-partial | 0/7 | 5/7 | - | False | - | - | 91.7 |
| wf5_partial | implement/edge-coverage | blocked-partial | 0/7 | 5/7 | - | False | - | - | 67.6 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 2/6 | DOCSCORE=2/4 TODOSCORE=0/3 | False | - | - | 219.5 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 2/6 | DOCSCORE=2/4 TODOSCORE=0/3 | False | - | - | 282.5 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 2/6 | DOCSCORE=2/4 TODOSCORE=0/3 | False | - | - | 393.0 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 6/6 | DOCSCORE=2/4 TODOSCORE=2/3 | True | - | - | 241.1 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 5/6 | DOCSCORE=3/4 TODOSCORE=2/3 | False | YES | - | 263.7 |

**objective pass 123/170 - regressions 1 - check crashes 0 - decline accuracy 25/30**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 45 | 0.92 |
| backward-compat | 20 | 0.88 |
| combined-score | 10 | 0.78 |
| concern-split | 10 | 0.78 |
| cross-file | 15 | 0.92 |
| decline-taxonomy | 10 | 0.83 |
| edge-coverage | 40 | 0.89 |
| greenfield-impl | 10 | 0.56 |
| keeper-set-rule | 5 | 1.00 |
| kway-synth | 10 | 0.78 |
| partial-credit | 15 | 0.86 |
| premise-audit | 40 | 0.93 |
| regression-guard | 45 | 0.99 |
| silent-failure | 20 | 1.00 |
| witness-pair | 10 | 1.00 |
