# M6 suite run - arm `m7c` (suite 0.3.0)

_2026-09-14 11:40 - 32 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 7.5 |
| hf_cache_decorator | feature/edge-coverage | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 65.0 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 6.5 |
| hf_counter_race | concurrency/silent-failure | answered | 2/3 | 3/3 | - | True | - | - | 16.4 |
| hf_csv | data/edge-coverage | blocked-partial | 3/6 | 5/6 | - | False | - | - | 60.7 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 6.9 |
| hf_deprecate | compat/backward-compat | blocked-no-progress | 1/4 | 1/4 | - | False | - | - | 59.5 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 67.8 |
| hf_extract_fn | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 41.5 |
| hf_json_field | feature/backward-compat | answered | 2/5 | 5/5 | - | True | - | - | 58.2 |
| hf_json_serialize | feature/multi-concern | answered | 2/5 | 5/5 | STRUCTSCORE=2/2 | True | - | - | 75.9 |
| hf_merge_config | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 16.3 |
| hf_misfiled_bug | fix/misdirection | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 45.7 |
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 69.9 |
| hf_pagination | fix/edge-coverage | answered | 1/5 | 5/5 | - | True | - | - | 58.3 |
| hf_path_sanitize | robustness/edge-coverage | answered | 1/8 | 8/8 | - | True | - | - | 30.0 |
| hf_rec_to_iter | refactor/behaviour-preserving | blocked-no-progress | 4/5 | 4/5 | STRUCTSCORE=0/1 | False | - | - | 146.3 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 7.2 |
| hf_rename | compat/behaviour-preserving | answered | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 328.6 |
| hf_retry_backoff | robustness/silent-failure | answered | 2/4 | 4/4 | - | True | - | - | 75.2 |
| hf_return_shape | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 16.3 |
| hf_suppress | robustness/silent-failure | answered | 3/4 | 4/4 | - | True | - | - | 69.8 |
| hf_timeout_param | feature/edge-coverage | answered | 2/6 | 6/6 | - | True | - | - | 66.6 |
| hf_validate_withdraw | robustness/silent-failure | answered | 4/6 | 6/6 | - | True | - | - | 60.6 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 15.7 |
| wf2_retry | feature/edge-coverage | blocked-partial | 0/5 | 3/5 | - | False | - | - | 65.5 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 64.3 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 86.5 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 76.1 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 6.6 |
| wf5_partial | implement/edge-coverage | blocked-partial | 0/7 | 5/7 | - | False | - | - | 73.2 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 6/6 | DOCSCORE=3/4 TODOSCORE=2/3 | True | - | - | 207.7 |

**objective pass 24/32 - regressions 0 - check crashes 0 - decline accuracy 5/5**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 8 | 0.88 |
| backward-compat | 4 | 0.81 |
| combined-score | 2 | 1.00 |
| concern-split | 2 | 1.00 |
| cross-file | 3 | 0.92 |
| edge-coverage | 8 | 0.90 |
| greenfield-impl | 2 | 0.66 |
| kway-synth | 2 | 0.77 |
| partial-credit | 3 | 0.85 |
| premise-audit | 7 | 0.96 |
| regression-guard | 9 | 1.00 |
| silent-failure | 4 | 1.00 |
| witness-pair | 2 | 1.00 |
