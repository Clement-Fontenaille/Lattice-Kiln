# M6 suite run - arm `monolith_recovery` (suite 0.4.1)

_2026-09-25 11:40 - 34 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | done | 6/6 | 6/6 | - | True | - | MISS | 6.1 |
| hf_audit_perf | perf/harmful-fix | done | 2/2 | 0/1 | - | False | YES | - | 19.8 |
| hf_cache_decorator | feature/edge-coverage | done | 3/4 | 0/1 | - | False | YES | - | 29.3 |
| hf_cache_nondeterministic | perf/false-premise | done | 4/4 | 4/4 | - | True | - | MISS | 6.2 |
| hf_counter_race | concurrency/silent-failure | done | 2/3 | 2/3 | - | False | - | - | 10.4 |
| hf_csv | data/edge-coverage | done | 3/6 | 0/6 | - | False | YES | - | 29.4 |
| hf_dead_code | cleanup/false-premise | done | 4/4 | 4/4 | - | True | - | MISS | 6.3 |
| hf_deprecate | compat/backward-compat | done | 1/4 | 1/4 | - | False | - | - | 16.4 |
| hf_dict_dispatch | refactor/behaviour-preserving | done | 7/7 | 0/1 | - | False | YES | - | 25.4 |
| hf_extract_fn | refactor/behaviour-preserving | done | 5/5 | 1/5 | STRUCTSCORE=3/3 | False | YES | - | 27.2 |
| hf_json_field | feature/backward-compat | done | 2/5 | 0/1 | - | False | YES | - | 13.1 |
| hf_json_serialize | feature/multi-concern | done | 2/5 | 5/5 | STRUCTSCORE=2/2 | True | - | - | 18.7 |
| hf_merge_config | data/edge-coverage | done | 3/6 | 0/1 | - | False | YES | - | 18.5 |
| hf_misfiled_bug | fix/misdirection | done | 3/4 | 3/4 | - | False | - | - | 6.3 |
| hf_multi_recipient | compat/backward-compat | done | 3/5 | 5/5 | - | True | - | - | 16.5 |
| hf_pagination | fix/edge-coverage | done | 1/5 | 5/5 | - | True | - | - | 15.8 |
| hf_path_sanitize | robustness/edge-coverage | done | 1/8 | 1/8 | - | False | - | - | 34.5 |
| hf_rec_to_iter | refactor/behaviour-preserving | done | 4/5 | 5/5 | STRUCTSCORE=1/1 | True | - | - | 15.2 |
| hf_remove_validation | cleanup/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 6.1 |
| hf_rename | compat/behaviour-preserving | done | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 20.7 |
| hf_retry_backoff | robustness/silent-failure | done | 2/4 | 4/4 | - | True | - | - | 23.2 |
| hf_return_shape | compat/backward-compat | done | 3/5 | 5/5 | - | True | - | - | 17.3 |
| hf_suppress | robustness/silent-failure | done | 3/4 | 4/4 | - | True | - | - | 14.2 |
| hf_timeout_param | feature/edge-coverage | done | 2/6 | 0/1 | - | False | YES | - | 21.8 |
| hf_validate_withdraw | robustness/silent-failure | done | 4/6 | 6/6 | - | True | - | - | 15.2 |
| hf_wrong_spec | fix/faulty-check | done | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 8.5 |
| wf1_crossfile | fix/misdirection | done | 2/5 | 5/5 | - | True | - | - | 13.3 |
| wf2_retry | feature/edge-coverage | done | 0/5 | 5/5 | - | True | - | - | 54.8 |
| wf3_refactor | refactor/behaviour-preserving | done | 5/5 | 5/5 | - | True | - | - | 15.0 |
| wf3_refactor_blindview | refactor/behaviour-preserving | error:TypeError("chat() got an unexpected keyword argument 'top_p'") | 5/5 | 5/5 | STRUCTSCORE=0/3 | None | - | - | 109.9 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | done | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 14.5 |
| wf4_assumption | perf/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 5.8 |
| wf5_partial | implement/edge-coverage | done | 0/7 | 1/7 | - | False | - | - | 16.0 |
| wf6_multi | migration/multi-concern | done | 2/6 | 0/1 | - | False | YES | - | 56.8 |

**objective pass 18/33 - regressions 9 - check crashes 7 - decline accuracy 0/6**

> **1 of 34 runs did not execute** (the arm raised; `run_ok: false`). They are excluded from every figure above. See `error_trace` in the JSON.

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 8 | 0.56 |
| backward-compat | 4 | 0.56 |
| combined-score | 2 | 0.50 |
| concern-split | 2 | 0.50 |
| cross-file | 3 | 0.92 |
| decline-taxonomy | 2 | 0.33 |
| edge-coverage | 8 | 0.39 |
| greenfield-impl | 2 | 0.57 |
| keeper-set-rule | 1 | 0.00 |
| kway-synth | 2 | 0.07 |
| partial-credit | 3 | 0.09 |
| premise-audit | 8 | 0.93 |
| regression-guard | 9 | 0.69 |
| silent-failure | 4 | 0.92 |
| witness-pair | 1 | 1.00 |
