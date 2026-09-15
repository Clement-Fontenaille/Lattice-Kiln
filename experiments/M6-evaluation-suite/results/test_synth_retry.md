# M6 suite run - arm `test_synth_retry` (suite 0.4.0)

_2026-09-15 04:00 - 124 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 60.8 |
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 8.5 |
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 9.9 |
| hf_audit_perf | perf/harmful-fix | blocked-no-progress | 2/2 | 2/2 | PERFSCORE=0/1 AUDITSCORE=1/1 | False | - | - | 78.1 |
| hf_audit_perf | perf/harmful-fix | blocked-no-progress | 2/2 | 2/2 | PERFSCORE=0/1 AUDITSCORE=1/1 | False | - | - | 87.1 |
| hf_audit_perf | perf/harmful-fix | answered | 2/2 | 2/2 | PERFSCORE=1/1 AUDITSCORE=1/1 | True | - | - | 17.2 |
| hf_cache_decorator | feature/edge-coverage | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 64.0 |
| hf_cache_decorator | feature/edge-coverage | answered | 3/4 | 4/4 | - | True | - | - | 85.5 |
| hf_cache_decorator | feature/edge-coverage | answered | 3/4 | 4/4 | - | True | - | - | 84.2 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 8.7 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 9.1 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 8.2 |
| hf_counter_race | concurrency/silent-failure | answered | 2/3 | 3/3 | - | True | - | - | 57.9 |
| hf_counter_race | concurrency/silent-failure | answered | 2/3 | 3/3 | - | True | - | - | 55.0 |
| hf_counter_race | concurrency/silent-failure | answered | 2/3 | 3/3 | - | True | - | - | 16.0 |
| hf_csv | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 86.6 |
| hf_csv | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 80.1 |
| hf_csv | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 78.5 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 9.5 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 7.1 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 8.0 |
| hf_deprecate | compat/backward-compat | blocked-no-progress | 1/4 | 1/4 | - | False | - | - | 64.8 |
| hf_deprecate | compat/backward-compat | blocked-no-progress | 1/4 | 1/4 | - | False | - | - | 110.8 |
| hf_deprecate | compat/backward-compat | blocked-no-progress | 1/4 | 1/4 | - | False | - | - | 66.4 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 106.8 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 96.2 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 93.2 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 91.8 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 95.5 |
| hf_extract_fn | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 66.5 |
| hf_extract_fn | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 41.9 |
| hf_extract_fn | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 53.0 |
| hf_extract_fn | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 41.3 |
| hf_extract_fn | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 45.7 |
| hf_json_field | feature/backward-compat | answered | 2/5 | 5/5 | - | True | - | - | 16.0 |
| hf_json_field | feature/backward-compat | answered | 2/5 | 5/5 | - | True | - | - | 47.8 |
| hf_json_field | feature/backward-compat | answered | 2/5 | 5/5 | - | True | - | - | 46.5 |
| hf_json_serialize | feature/multi-concern | answered | 2/5 | 5/5 | STRUCTSCORE=2/2 | True | - | - | 102.7 |
| hf_json_serialize | feature/multi-concern | answered | 2/5 | 5/5 | STRUCTSCORE=2/2 | True | - | - | 95.9 |
| hf_json_serialize | feature/multi-concern | answered | 2/5 | 5/5 | STRUCTSCORE=2/2 | True | - | - | 100.0 |
| hf_merge_config | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 91.4 |
| hf_merge_config | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 88.1 |
| hf_merge_config | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 87.6 |
| hf_misfiled_bug | fix/misdirection | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 42.0 |
| hf_misfiled_bug | fix/misdirection | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 43.7 |
| hf_misfiled_bug | fix/misdirection | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 31.0 |
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 116.4 |
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 69.5 |
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 370.5 |
| hf_pagination | fix/edge-coverage | answered | 1/5 | 5/5 | - | True | - | - | 14.9 |
| hf_pagination | fix/edge-coverage | answered | 1/5 | 5/5 | - | True | - | - | 15.2 |
| hf_pagination | fix/edge-coverage | answered | 1/5 | 5/5 | - | True | - | - | 15.7 |
| hf_path_sanitize | robustness/edge-coverage | answered | 1/8 | 8/8 | - | True | - | - | 22.7 |
| hf_path_sanitize | robustness/edge-coverage | answered | 1/8 | 8/8 | - | True | - | - | 19.6 |
| hf_path_sanitize | robustness/edge-coverage | answered | 1/8 | 8/8 | - | True | - | - | 18.7 |
| hf_rec_to_iter | refactor/behaviour-preserving | answered | 4/5 | 5/5 | STRUCTSCORE=1/1 | True | - | - | 110.1 |
| hf_rec_to_iter | refactor/behaviour-preserving | answered | 4/5 | 5/5 | STRUCTSCORE=1/1 | True | - | - | 115.7 |
| hf_rec_to_iter | refactor/behaviour-preserving | answered | 4/5 | 5/5 | STRUCTSCORE=1/1 | True | - | - | 83.6 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 7.8 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 11.9 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 13.3 |
| hf_rename | compat/behaviour-preserving | blocked-no-progress | 4/6 | 4/6 | STRUCTSCORE=2/3 | False | - | - | 96.0 |
| hf_rename | compat/behaviour-preserving | answered | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 95.3 |
| hf_rename | compat/behaviour-preserving | answered | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 92.4 |
| hf_rename | compat/behaviour-preserving | answered | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 60.1 |
| hf_rename | compat/behaviour-preserving | answered | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 106.6 |
| hf_retry_backoff | robustness/silent-failure | answered | 2/4 | 4/4 | - | True | - | - | 116.5 |
| hf_retry_backoff | robustness/silent-failure | answered | 2/4 | 4/4 | - | True | - | - | 23.1 |
| hf_retry_backoff | robustness/silent-failure | answered | 2/4 | 4/4 | - | True | - | - | 102.0 |
| hf_return_shape | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 202.0 |
| hf_return_shape | compat/backward-compat | blocked-no-progress | 3/5 | 3/5 | - | False | - | - | 82.1 |
| hf_return_shape | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 22.4 |
| hf_suppress | robustness/silent-failure | answered | 3/4 | 4/4 | - | True | - | - | 63.1 |
| hf_suppress | robustness/silent-failure | answered | 3/4 | 4/4 | - | True | - | - | 102.2 |
| hf_suppress | robustness/silent-failure | answered | 3/4 | 4/4 | - | True | - | - | 112.9 |
| hf_timeout_param | feature/edge-coverage | blocked-partial | 2/6 | 5/6 | - | False | - | - | 118.0 |
| hf_timeout_param | feature/edge-coverage | blocked-partial | 2/6 | 5/6 | - | False | - | - | 94.6 |
| hf_timeout_param | feature/edge-coverage | blocked-partial | 2/6 | 5/6 | - | False | - | - | 104.5 |
| hf_validate_withdraw | robustness/silent-failure | answered | 4/6 | 6/6 | - | True | - | - | 101.4 |
| hf_validate_withdraw | robustness/silent-failure | answered | 4/6 | 6/6 | - | True | - | - | 102.9 |
| hf_validate_withdraw | robustness/silent-failure | answered | 4/6 | 6/6 | - | True | - | - | 94.6 |
| hf_wrong_spec | fix/faulty-check | answered | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 37.8 |
| hf_wrong_spec | fix/faulty-check | blocked-no-progress | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 21.8 |
| hf_wrong_spec | fix/faulty-check | answered | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 20.5 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 28.3 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 54.8 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 74.3 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 72.2 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 72.0 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 2/5 | - | False | - | - | 152.1 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 3/5 | - | False | - | - | 121.5 |
| wf2_retry | feature/edge-coverage | answered | 0/5 | 5/5 | - | True | - | - | 101.6 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 3/5 | - | False | - | - | 106.6 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 3/5 | - | False | - | - | 120.2 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 143.2 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 19.2 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 17.1 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 131.3 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 313.0 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 51.2 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 41.9 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 43.9 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 328.7 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 310.1 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 49.7 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 394.9 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 64.3 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 46.8 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 56.7 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 24.3 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 13.2 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 20.6 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 17.1 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 27.4 |
| wf5_partial | implement/edge-coverage | blocked-partial | 0/7 | 5/7 | - | False | - | - | 169.5 |
| wf5_partial | implement/edge-coverage | blocked-partial | 0/7 | 5/7 | - | False | - | - | 137.8 |
| wf5_partial | implement/edge-coverage | blocked-partial | 0/7 | 5/7 | - | False | - | - | 121.8 |
| wf5_partial | implement/edge-coverage | blocked-partial | 0/7 | 2/7 | - | False | - | - | 96.5 |
| wf5_partial | implement/edge-coverage | blocked-partial | 0/7 | 5/7 | - | False | - | - | 156.2 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 2/6 | DOCSCORE=2/4 TODOSCORE=0/3 | False | - | - | 509.3 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 6/6 | DOCSCORE=2/4 TODOSCORE=2/3 | True | - | - | 252.7 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 2/6 | DOCSCORE=2/4 TODOSCORE=2/3 | False | - | - | 321.9 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 6/6 | DOCSCORE=3/4 TODOSCORE=3/3 | True | - | - | 536.6 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 5/6 | DOCSCORE=2/4 TODOSCORE=0/3 | False | YES | - | 469.7 |

**objective pass 90/124 - regressions 1 - check crashes 0 - decline accuracy 17/20**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 39 | 0.93 |
| backward-compat | 12 | 0.78 |
| combined-score | 8 | 0.81 |
| concern-split | 8 | 0.81 |
| cross-file | 11 | 0.93 |
| decline-taxonomy | 6 | 0.83 |
| edge-coverage | 26 | 0.90 |
| greenfield-impl | 10 | 0.63 |
| keeper-set-rule | 3 | 1.00 |
| kway-synth | 8 | 0.77 |
| partial-credit | 11 | 0.83 |
| premise-audit | 28 | 0.94 |
| regression-guard | 33 | 0.98 |
| silent-failure | 12 | 1.00 |
| witness-pair | 10 | 1.00 |
