# M6 suite run - arm `monolith` (suite 0.4.1)

_2026-09-25 11:28 - 34 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | done | 6/6 | 6/6 | - | True | - | MISS | 13.1 |
| hf_audit_perf | perf/harmful-fix | done | 2/2 | 0/1 | - | False | YES | - | 17.5 |
| hf_cache_decorator | feature/edge-coverage | done | 3/4 | 0/1 | - | False | YES | - | 322.9 |
| hf_cache_nondeterministic | perf/false-premise | done | 4/4 | 4/4 | - | True | - | MISS | 10.9 |
| hf_counter_race | concurrency/silent-failure | done | 2/3 | 0/1 | - | False | YES | - | 21.8 |
| hf_csv | data/edge-coverage | done | 3/6 | 0/6 | - | False | YES | - | 34.7 |
| hf_dead_code | cleanup/false-premise | done | 4/4 | 4/4 | - | True | - | MISS | 11.2 |
| hf_deprecate | compat/backward-compat | done | 1/4 | 4/4 | - | True | - | - | 32.9 |
| hf_dict_dispatch | refactor/behaviour-preserving | done | 7/7 | 0/1 | - | False | YES | - | 88.5 |
| hf_extract_fn | refactor/behaviour-preserving | done | 5/5 | 5/5 | STRUCTSCORE=2/3 | False | - | - | 58.0 |
| hf_json_field | feature/backward-compat | done | 2/5 | 5/5 | - | True | - | - | 30.8 |
| hf_json_serialize | feature/multi-concern | done | 2/5 | 1/5 | STRUCTSCORE=1/2 | False | YES | - | 55.8 |
| hf_merge_config | data/edge-coverage | done | 3/6 | 4/6 | - | False | - | - | 30.8 |
| hf_misfiled_bug | fix/misdirection | done | 3/4 | 3/4 | - | False | - | - | 14.5 |
| hf_multi_recipient | compat/backward-compat | done | 3/5 | 5/5 | - | True | - | - | 32.3 |
| hf_pagination | fix/edge-coverage | done | 1/5 | 5/5 | - | True | - | - | 41.9 |
| hf_path_sanitize | robustness/edge-coverage | done | 1/8 | 3/8 | - | False | YES | - | 31.7 |
| hf_rec_to_iter | refactor/behaviour-preserving | done | 4/5 | 1/5 | STRUCTSCORE=1/1 | False | YES | - | 50.4 |
| hf_remove_validation | cleanup/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 18.3 |
| hf_rename | compat/behaviour-preserving | done | 4/6 | 0/1 | - | False | YES | - | 56.7 |
| hf_retry_backoff | robustness/silent-failure | done | 2/4 | 2/4 | - | False | - | - | 50.0 |
| hf_return_shape | compat/backward-compat | done | 3/5 | 5/5 | - | True | - | - | 39.8 |
| hf_suppress | robustness/silent-failure | done | 3/4 | 4/4 | - | True | - | - | 45.6 |
| hf_timeout_param | feature/edge-coverage | done | 2/6 | 0/1 | - | False | YES | - | 34.0 |
| hf_validate_withdraw | robustness/silent-failure | done | 4/6 | 6/6 | - | True | - | - | 48.4 |
| hf_wrong_spec | fix/faulty-check | done | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 8.2 |
| wf1_crossfile | fix/misdirection | done | 2/5 | 5/5 | - | True | - | - | 36.4 |
| wf2_retry | feature/edge-coverage | done | 0/5 | 3/5 | - | False | - | - | 31.0 |
| wf3_refactor | refactor/behaviour-preserving | done | 5/5 | 5/5 | - | True | - | - | 37.5 |
| wf3_refactor_blindview | refactor/behaviour-preserving | done | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 25.2 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | done | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 28.4 |
| wf4_assumption | perf/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 7.0 |
| wf5_partial | implement/edge-coverage | done | 0/7 | 1/7 | - | False | - | - | 34.7 |
| wf6_multi | migration/multi-concern | done | 2/6 | 2/6 | DOCSCORE=0/4 TODOSCORE=0/3 | False | - | - | 38.0 |

**objective pass 16/34 - regressions 10 - check crashes 6 - decline accuracy 0/6**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 9 | 0.58 |
| backward-compat | 4 | 1.00 |
| combined-score | 2 | 0.27 |
| concern-split | 2 | 0.27 |
| cross-file | 3 | 0.92 |
| decline-taxonomy | 2 | 0.33 |
| edge-coverage | 8 | 0.39 |
| greenfield-impl | 2 | 0.37 |
| keeper-set-rule | 1 | 0.00 |
| kway-synth | 2 | 0.07 |
| partial-credit | 3 | 0.17 |
| premise-audit | 8 | 0.93 |
| regression-guard | 9 | 0.78 |
| silent-failure | 4 | 0.62 |
| witness-pair | 2 | 1.00 |
