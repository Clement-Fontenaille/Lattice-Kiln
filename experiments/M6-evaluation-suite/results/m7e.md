# M6 suite run - arm `m7e` (suite 0.4.0)

_2026-09-15 07:42 - 102 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 82.0 |
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 64.4 |
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 64.6 |
| hf_audit_perf | perf/harmful-fix | answered | 2/2 | 2/2 | PERFSCORE=1/1 AUDITSCORE=1/1 | True | - | - | 17.3 |
| hf_audit_perf | perf/harmful-fix | answered | 2/2 | 2/2 | PERFSCORE=1/1 AUDITSCORE=1/1 | True | - | - | 16.3 |
| hf_audit_perf | perf/harmful-fix | answered | 2/2 | 2/2 | PERFSCORE=1/1 AUDITSCORE=1/1 | True | - | - | 87.4 |
| hf_cache_decorator | feature/edge-coverage | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 65.2 |
| hf_cache_decorator | feature/edge-coverage | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 68.3 |
| hf_cache_decorator | feature/edge-coverage | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 73.3 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 6.6 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 6.4 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 6.4 |
| hf_counter_race | concurrency/silent-failure | answered | 2/3 | 3/3 | - | True | - | - | 15.8 |
| hf_counter_race | concurrency/silent-failure | answered | 2/3 | 3/3 | - | True | - | - | 61.3 |
| hf_counter_race | concurrency/silent-failure | answered | 2/3 | 3/3 | - | True | - | - | 60.3 |
| hf_csv | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 66.4 |
| hf_csv | data/edge-coverage | blocked-partial | 3/6 | 5/6 | - | False | - | - | 141.1 |
| hf_csv | data/edge-coverage | blocked-partial | 3/6 | 4/6 | - | False | - | - | 58.4 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 6.9 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 6.5 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 6.7 |
| hf_deprecate | compat/backward-compat | blocked-no-progress | 1/4 | 1/4 | - | False | - | - | 62.5 |
| hf_deprecate | compat/backward-compat | blocked-no-progress | 1/4 | 1/4 | - | False | - | - | 59.9 |
| hf_deprecate | compat/backward-compat | blocked-no-progress | 1/4 | 1/4 | - | False | - | - | 62.7 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 68.9 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 74.4 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 76.6 |
| hf_extract_fn | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 40.8 |
| hf_extract_fn | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 40.3 |
| hf_extract_fn | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 40.4 |
| hf_json_field | feature/backward-compat | answered | 2/5 | 5/5 | - | True | - | - | 55.0 |
| hf_json_field | feature/backward-compat | answered | 2/5 | 5/5 | - | True | - | - | 55.3 |
| hf_json_field | feature/backward-compat | answered | 2/5 | 5/5 | - | True | - | - | 54.2 |
| hf_json_serialize | feature/multi-concern | answered | 2/5 | 5/5 | STRUCTSCORE=2/2 | True | - | - | 79.1 |
| hf_json_serialize | feature/multi-concern | blocked-partial | 2/5 | 5/5 | STRUCTSCORE=1/2 | True | - | - | 70.7 |
| hf_json_serialize | feature/multi-concern | blocked-partial | 2/5 | 5/5 | STRUCTSCORE=1/2 | True | - | - | 78.6 |
| hf_merge_config | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 66.1 |
| hf_merge_config | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 60.8 |
| hf_merge_config | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 63.6 |
| hf_misfiled_bug | fix/misdirection | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 38.1 |
| hf_misfiled_bug | fix/misdirection | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 32.9 |
| hf_misfiled_bug | fix/misdirection | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 35.9 |
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 59.6 |
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 60.3 |
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 63.8 |
| hf_pagination | fix/edge-coverage | answered | 1/5 | 5/5 | - | True | - | - | 14.9 |
| hf_pagination | fix/edge-coverage | answered | 1/5 | 5/5 | - | True | - | - | 13.7 |
| hf_pagination | fix/edge-coverage | answered | 1/5 | 5/5 | - | True | - | - | 54.6 |
| hf_path_sanitize | robustness/edge-coverage | answered | 1/8 | 8/8 | - | True | - | - | 62.0 |
| hf_path_sanitize | robustness/edge-coverage | answered | 1/8 | 8/8 | - | True | - | - | 17.9 |
| hf_path_sanitize | robustness/edge-coverage | answered | 1/8 | 8/8 | - | True | - | - | 66.6 |
| hf_rec_to_iter | refactor/behaviour-preserving | blocked-no-progress | 4/5 | 4/5 | STRUCTSCORE=0/1 | False | - | - | 78.3 |
| hf_rec_to_iter | refactor/behaviour-preserving | blocked-no-progress | 4/5 | 4/5 | STRUCTSCORE=0/1 | False | - | - | 74.4 |
| hf_rec_to_iter | refactor/behaviour-preserving | answered | 4/5 | 5/5 | STRUCTSCORE=1/1 | True | - | - | 68.9 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 7.2 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 6.7 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 7.2 |
| hf_rename | compat/behaviour-preserving | answered | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 83.2 |
| hf_rename | compat/behaviour-preserving | answered | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 87.4 |
| hf_rename | compat/behaviour-preserving | blocked-no-progress | 4/6 | 4/6 | STRUCTSCORE=2/3 | False | - | - | 87.5 |
| hf_retry_backoff | robustness/silent-failure | answered | 2/4 | 4/4 | - | True | - | - | 80.4 |
| hf_retry_backoff | robustness/silent-failure | answered | 2/4 | 4/4 | - | True | - | - | 73.2 |
| hf_retry_backoff | robustness/silent-failure | answered | 2/4 | 4/4 | - | True | - | - | 83.5 |
| hf_return_shape | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 15.4 |
| hf_return_shape | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 71.8 |
| hf_return_shape | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 60.8 |
| hf_suppress | robustness/silent-failure | answered | 3/4 | 4/4 | - | True | - | - | 71.2 |
| hf_suppress | robustness/silent-failure | answered | 3/4 | 4/4 | - | True | - | - | 68.8 |
| hf_suppress | robustness/silent-failure | answered | 3/4 | 4/4 | - | True | - | - | 96.5 |
| hf_timeout_param | feature/edge-coverage | answered | 2/6 | 6/6 | - | True | - | - | 70.3 |
| hf_timeout_param | feature/edge-coverage | blocked-partial | 2/6 | 4/6 | - | False | - | - | 71.1 |
| hf_timeout_param | feature/edge-coverage | blocked-partial | 2/6 | 5/6 | - | False | - | - | 68.7 |
| hf_validate_withdraw | robustness/silent-failure | answered | 4/6 | 6/6 | - | True | - | - | 72.9 |
| hf_validate_withdraw | robustness/silent-failure | answered | 4/6 | 6/6 | - | True | - | - | 70.5 |
| hf_validate_withdraw | robustness/silent-failure | answered | 4/6 | 6/6 | - | True | - | - | 73.2 |
| hf_wrong_spec | fix/faulty-check | blocked-no-progress | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 76.0 |
| hf_wrong_spec | fix/faulty-check | answered | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 39.5 |
| hf_wrong_spec | fix/faulty-check | blocked-no-progress | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 48.7 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 63.1 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 51.6 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 80.1 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 2/5 | - | False | - | - | 70.5 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 3/5 | - | False | - | - | 64.2 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 2/5 | - | False | - | - | 65.9 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 7.6 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 7.2 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 8.1 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 7.6 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 6.9 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 8.3 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 16.9 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 76.9 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 74.1 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 57.1 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 63.9 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 58.8 |
| wf5_partial | implement/edge-coverage | answered | 0/7 | 7/7 | - | True | - | - | 80.2 |
| wf5_partial | implement/edge-coverage | blocked-partial | 0/7 | 4/7 | - | False | - | - | 71.7 |
| wf5_partial | implement/edge-coverage | blocked-partial | 0/7 | 5/7 | - | False | - | - | 69.8 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 2/6 | DOCSCORE=2/4 TODOSCORE=0/3 | False | - | - | 226.8 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 2/6 | DOCSCORE=2/4 TODOSCORE=0/3 | False | - | - | 210.1 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 5/6 | DOCSCORE=2/4 TODOSCORE=0/3 | False | YES | - | 176.4 |

**objective pass 72/102 - regressions 1 - check crashes 0 - decline accuracy 15/18**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 27 | 0.89 |
| backward-compat | 12 | 0.81 |
| combined-score | 6 | 0.75 |
| concern-split | 6 | 0.75 |
| cross-file | 9 | 0.92 |
| decline-taxonomy | 6 | 0.83 |
| edge-coverage | 24 | 0.86 |
| greenfield-impl | 6 | 0.61 |
| keeper-set-rule | 3 | 1.00 |
| kway-synth | 6 | 0.80 |
| partial-credit | 9 | 0.87 |
| premise-audit | 24 | 0.93 |
| regression-guard | 27 | 0.99 |
| silent-failure | 12 | 1.00 |
| witness-pair | 6 | 1.00 |
