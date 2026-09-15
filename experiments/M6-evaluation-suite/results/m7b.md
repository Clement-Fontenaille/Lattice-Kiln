# M6 suite run - arm `m7b` (suite 0.4.0)

_2026-09-15 02:46 - 114 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 69.3 |
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 28.5 |
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 273.4 |
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 28.0 |
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 29.2 |
| hf_cache_decorator | feature/edge-coverage | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 40.7 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 3.6 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 13.3 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 29.6 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 9.5 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 29.4 |
| hf_counter_race | concurrency/silent-failure | answered | 2/3 | 3/3 | - | True | - | - | 10.3 |
| hf_csv | data/edge-coverage | blocked-partial | 3/6 | 5/6 | - | False | - | - | 62.4 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 3.6 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 4.8 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 30.1 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 9.3 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 6.9 |
| hf_deprecate | compat/backward-compat | blocked-no-progress | 1/4 | 1/4 | - | False | - | - | 39.6 |
| hf_deprecate | compat/backward-compat | blocked-no-progress | 1/4 | 1/4 | - | False | - | - | 60.9 |
| hf_deprecate | compat/backward-compat | blocked-no-progress | 1/4 | 1/4 | - | False | - | - | 65.1 |
| hf_deprecate | compat/backward-compat | blocked-no-progress | 1/4 | 1/4 | - | False | - | - | 63.1 |
| hf_deprecate | compat/backward-compat | blocked-no-progress | 1/4 | 1/4 | - | False | - | - | 84.5 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 69.2 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 134.8 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 108.7 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 100.2 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 108.3 |
| hf_extract_fn | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 29.0 |
| hf_extract_fn | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 35.4 |
| hf_extract_fn | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 45.3 |
| hf_extract_fn | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 43.5 |
| hf_extract_fn | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 47.6 |
| hf_json_field | feature/backward-compat | answered | 2/5 | 5/5 | - | True | - | - | 41.1 |
| hf_json_field | feature/backward-compat | answered | 2/5 | 5/5 | - | True | - | - | 83.9 |
| hf_json_field | feature/backward-compat | answered | 2/5 | 5/5 | - | True | - | - | 81.6 |
| hf_json_field | feature/backward-compat | answered | 2/5 | 5/5 | - | True | - | - | 54.9 |
| hf_json_field | feature/backward-compat | answered | 2/5 | 5/5 | - | True | - | - | 14.8 |
| hf_json_serialize | feature/multi-concern | blocked-no-progress | 2/5 | 2/5 | STRUCTSCORE=0/2 | False | - | - | 83.0 |
| hf_merge_config | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 73.5 |
| hf_misfiled_bug | fix/misdirection | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 25.5 |
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 56.2 |
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 220.9 |
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 181.9 |
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 105.3 |
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 71.4 |
| hf_pagination | fix/edge-coverage | answered | 1/5 | 5/5 | - | True | - | - | 9.6 |
| hf_path_sanitize | robustness/edge-coverage | answered | 1/8 | 8/8 | - | True | - | - | 14.1 |
| hf_rec_to_iter | refactor/behaviour-preserving | answered | 4/5 | 5/5 | STRUCTSCORE=1/1 | True | - | - | 73.9 |
| hf_rec_to_iter | refactor/behaviour-preserving | blocked-no-progress | 4/5 | 4/5 | STRUCTSCORE=0/1 | False | - | - | 191.0 |
| hf_rec_to_iter | refactor/behaviour-preserving | answered | 4/5 | 5/5 | STRUCTSCORE=1/1 | True | - | - | 140.1 |
| hf_rec_to_iter | refactor/behaviour-preserving | answered | 4/5 | 5/5 | STRUCTSCORE=1/1 | True | - | - | 142.1 |
| hf_rec_to_iter | refactor/behaviour-preserving | blocked-no-progress | 4/5 | 4/5 | STRUCTSCORE=0/1 | False | - | - | 239.8 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 3.9 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 5.1 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 28.2 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 9.2 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 16.7 |
| hf_rename | compat/behaviour-preserving | answered | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 83.7 |
| hf_rename | compat/behaviour-preserving | answered | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 95.5 |
| hf_rename | compat/behaviour-preserving | blocked-no-progress | 4/6 | 4/6 | STRUCTSCORE=2/3 | False | - | - | 147.3 |
| hf_rename | compat/behaviour-preserving | answered | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 152.8 |
| hf_rename | compat/behaviour-preserving | answered | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 229.6 |
| hf_retry_backoff | robustness/silent-failure | answered | 2/4 | 4/4 | - | True | - | - | 61.5 |
| hf_return_shape | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 53.1 |
| hf_return_shape | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 105.4 |
| hf_return_shape | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 69.8 |
| hf_return_shape | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 68.6 |
| hf_return_shape | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 89.3 |
| hf_suppress | robustness/silent-failure | answered | 3/4 | 4/4 | - | True | - | - | 68.5 |
| hf_timeout_param | feature/edge-coverage | blocked-partial | 2/6 | 5/6 | - | False | - | - | 94.1 |
| hf_timeout_param | feature/edge-coverage | answered | 2/6 | 6/6 | - | True | - | - | 117.3 |
| hf_timeout_param | feature/edge-coverage | blocked-partial | 2/6 | 5/6 | - | False | - | - | 104.2 |
| hf_validate_withdraw | robustness/silent-failure | answered | 4/6 | 6/6 | - | True | - | - | 89.0 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 9.3 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 69.1 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 8.8 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 7.9 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 8.0 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 2/5 | - | False | - | - | 64.9 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 2/5 | - | False | - | - | 73.9 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 3/5 | - | False | - | - | 65.3 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 2/5 | - | False | - | - | 71.6 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 2/5 | - | False | - | - | 68.9 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 73.1 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 85.4 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 81.2 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 6.0 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 5.2 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 155.9 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 7.8 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 179.1 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 6.0 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 100.4 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 11.0 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 11.4 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 118.9 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 11.1 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 10.5 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 3.6 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 5.2 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 4.4 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 6.4 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 59.1 |
| wf5_partial | implement/edge-coverage | blocked-partial | 0/7 | 5/7 | - | False | - | - | 65.4 |
| wf5_partial | implement/edge-coverage | blocked-partial | 0/7 | 5/7 | - | False | - | - | 69.5 |
| wf5_partial | implement/edge-coverage | blocked-partial | 0/7 | 5/7 | - | False | - | - | 77.5 |
| wf5_partial | implement/edge-coverage | blocked-partial | 0/7 | 3/7 | - | False | - | - | 137.2 |
| wf5_partial | implement/edge-coverage | answered | 0/7 | 7/7 | - | True | - | - | 93.3 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 2/6 | DOCSCORE=2/4 TODOSCORE=2/3 | False | - | - | 257.2 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 6/6 | DOCSCORE=3/4 TODOSCORE=3/3 | True | - | - | 450.4 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 6/6 | DOCSCORE=0/4 TODOSCORE=2/3 | True | - | - | 508.7 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 2/6 | DOCSCORE=2/4 TODOSCORE=0/3 | False | - | - | 435.2 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 6/6 | DOCSCORE=3/4 TODOSCORE=2/3 | True | - | - | 438.3 |

**objective pass 84/114 - regressions 0 - check crashes 0 - decline accuracy 25/25**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 40 | 0.89 |
| backward-compat | 20 | 0.81 |
| combined-score | 6 | 0.68 |
| concern-split | 6 | 0.68 |
| cross-file | 11 | 0.98 |
| edge-coverage | 14 | 0.75 |
| greenfield-impl | 10 | 0.58 |
| kway-synth | 6 | 0.73 |
| partial-credit | 7 | 0.77 |
| premise-audit | 31 | 0.99 |
| regression-guard | 37 | 0.99 |
| silent-failure | 4 | 1.00 |
| witness-pair | 11 | 1.00 |
