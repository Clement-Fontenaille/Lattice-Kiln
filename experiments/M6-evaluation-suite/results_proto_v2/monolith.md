# M6 suite run - arm `monolith` (suite 0.4.1)

_2026-09-25 11:27 - 34 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | done | 6/6 | 6/6 | - | True | - | MISS | 11.8 |
| hf_audit_perf | perf/harmful-fix | done | 2/2 | 0/1 | - | False | YES | - | 42.6 |
| hf_cache_decorator | feature/edge-coverage | done | 3/4 | 3/4 | - | False | - | - | 143.3 |
| hf_cache_nondeterministic | perf/false-premise | done | 4/4 | 4/4 | - | True | - | MISS | 14.0 |
| hf_counter_race | concurrency/silent-failure | done | 2/3 | 0/1 | - | False | YES | - | 34.1 |
| hf_csv | data/edge-coverage | done | 3/6 | 0/6 | - | False | YES | - | 80.7 |
| hf_dead_code | cleanup/false-premise | done | 4/4 | 4/4 | - | True | - | MISS | 9.3 |
| hf_deprecate | compat/backward-compat | done | 1/4 | 0/1 | - | False | YES | - | 31.8 |
| hf_dict_dispatch | refactor/behaviour-preserving | done | 7/7 | 0/1 | - | False | YES | - | 84.5 |
| hf_extract_fn | refactor/behaviour-preserving | done | 5/5 | 3/5 | STRUCTSCORE=3/3 | False | YES | - | 62.4 |
| hf_json_field | feature/backward-compat | done | 2/5 | 5/5 | - | True | - | - | 27.4 |
| hf_json_serialize | feature/multi-concern | done | 2/5 | 0/1 | - | False | YES | - | 52.0 |
| hf_merge_config | data/edge-coverage | done | 3/6 | 6/6 | - | True | - | - | 34.8 |
| hf_misfiled_bug | fix/misdirection | done | 3/4 | 0/1 | - | False | YES | - | 32.5 |
| hf_multi_recipient | compat/backward-compat | done | 3/5 | 5/5 | - | True | - | - | 30.9 |
| hf_pagination | fix/edge-coverage | done | 1/5 | 5/5 | - | True | - | - | 29.8 |
| hf_path_sanitize | robustness/edge-coverage | done | 1/8 | 8/8 | - | True | - | - | 60.3 |
| hf_rec_to_iter | refactor/behaviour-preserving | done | 4/5 | 5/5 | STRUCTSCORE=1/1 | True | - | - | 49.1 |
| hf_remove_validation | cleanup/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 20.8 |
| hf_rename | compat/behaviour-preserving | done | 4/6 | 4/6 | STRUCTSCORE=2/3 | False | - | - | 58.4 |
| hf_retry_backoff | robustness/silent-failure | done | 2/4 | 2/4 | - | False | YES | - | 50.7 |
| hf_return_shape | compat/backward-compat | done | 3/5 | 0/1 | - | False | YES | - | 39.7 |
| hf_suppress | robustness/silent-failure | done | 3/4 | 3/4 | - | False | YES | - | 34.0 |
| hf_timeout_param | feature/edge-coverage | done | 2/6 | 0/1 | - | False | YES | - | 60.4 |
| hf_validate_withdraw | robustness/silent-failure | done | 4/6 | 6/6 | - | True | - | - | 42.1 |
| hf_wrong_spec | fix/faulty-check | done | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 8.7 |
| wf1_crossfile | fix/misdirection | done | 2/5 | 5/5 | - | True | - | - | 38.4 |
| wf2_retry | feature/edge-coverage | done | 0/5 | 3/5 | - | False | - | - | 51.6 |
| wf3_refactor | refactor/behaviour-preserving | done | 5/5 | 5/5 | - | True | - | - | 18.0 |
| wf3_refactor_blindview | refactor/behaviour-preserving | done | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 25.6 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | done | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 28.6 |
| wf4_assumption | perf/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 5.0 |
| wf5_partial | implement/edge-coverage | done | 0/7 | 0/7 | - | False | - | - | 30.0 |
| wf6_multi | migration/multi-concern | done | 2/6 | 5/6 | DOCSCORE=4/4 TODOSCORE=3/3 | False | YES | - | 48.9 |

**objective pass 16/34 - regressions 13 - check crashes 8 - decline accuracy 0/6**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 9 | 0.59 |
| backward-compat | 4 | 0.50 |
| combined-score | 2 | 0.42 |
| concern-split | 2 | 0.42 |
| cross-file | 3 | 0.67 |
| decline-taxonomy | 2 | 0.33 |
| edge-coverage | 8 | 0.61 |
| greenfield-impl | 2 | 0.30 |
| keeper-set-rule | 1 | 0.00 |
| kway-synth | 2 | 0.00 |
| partial-credit | 3 | 0.33 |
| premise-audit | 8 | 0.83 |
| regression-guard | 9 | 0.67 |
| silent-failure | 4 | 0.56 |
| witness-pair | 2 | 1.00 |
