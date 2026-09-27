# M6 suite run - arm `monolith_recovery` (suite 0.4.1)

_2026-09-26 23:35 - 34 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | done | 6/6 | 6/6 | - | True | - | MISS | 32.2 |
| hf_audit_perf | perf/harmful-fix | error:TypeError("chat() got an unexpected keyword argument 'top_p'") | 2/2 | 2/2 | PERFSCORE=0/1 AUDITSCORE=1/1 | None | - | - | 377.3 |
| hf_cache_decorator | feature/edge-coverage | error:TypeError("chat() got an unexpected keyword argument 'top_p'") | 3/4 | 3/4 | - | None | - | - | 222.3 |
| hf_cache_nondeterministic | perf/false-premise | done | 4/4 | 4/4 | - | True | - | MISS | 44.1 |
| hf_counter_race | concurrency/silent-failure | done | 2/3 | 2/3 | - | False | - | - | 64.1 |
| hf_csv | data/edge-coverage | done | 3/6 | 3/6 | - | False | - | - | 431.5 |
| hf_dead_code | cleanup/false-premise | done | 4/4 | 4/4 | - | True | - | MISS | 67.2 |
| hf_deprecate | compat/backward-compat | done | 1/4 | 1/4 | - | False | - | - | 86.3 |
| hf_dict_dispatch | refactor/behaviour-preserving | error:TypeError("chat() got an unexpected keyword argument 'top_p'") | 7/7 | 7/7 | STRUCTSCORE=0/3 | None | - | - | 343.5 |
| hf_extract_fn | refactor/behaviour-preserving | done | 5/5 | 5/5 | STRUCTSCORE=1/3 | False | - | - | 166.3 |
| hf_json_field | feature/backward-compat | done | 2/5 | 2/5 | - | False | - | - | 231.2 |
| hf_json_serialize | feature/multi-concern | error:OllamaError('request to http://localhost:11434 failed: HTTP 500: {"error":"XML syntax error on line 5: element \\u | 2/5 | 2/5 | STRUCTSCORE=0/2 | None | - | - | 304.7 |
| hf_merge_config | data/edge-coverage | done | 3/6 | 3/6 | - | False | - | - | 427.7 |
| hf_misfiled_bug | fix/misdirection | done | 3/4 | 3/4 | - | False | - | - | 57.0 |
| hf_multi_recipient | compat/backward-compat | done | 3/5 | 0/1 | - | False | YES | - | 61.8 |
| hf_pagination | fix/edge-coverage | error:TypeError("chat() got an unexpected keyword argument 'top_p'") | 1/5 | 1/5 | - | None | - | - | 498.6 |
| hf_path_sanitize | robustness/edge-coverage | done | 1/8 | 1/8 | - | False | - | - | 114.1 |
| hf_rec_to_iter | refactor/behaviour-preserving | done | 4/5 | 4/5 | STRUCTSCORE=0/1 | False | - | - | 85.3 |
| hf_remove_validation | cleanup/false-premise | error:OllamaError('request to http://localhost:11434 failed: HTTP 500: {"error":"XML syntax error on line 5: element \\u | 5/5 | 5/5 | - | None | - | MISS | 19.2 |
| hf_rename | compat/behaviour-preserving | done | 4/6 | 4/6 | STRUCTSCORE=2/3 | False | - | - | 100.9 |
| hf_retry_backoff | robustness/silent-failure | done | 2/4 | 2/4 | - | False | - | - | 146.6 |
| hf_return_shape | compat/backward-compat | done | 3/5 | 3/5 | - | False | - | - | 233.0 |
| hf_suppress | robustness/silent-failure | error:OllamaError('request to http://localhost:11434 failed: HTTP 500: {"error":"XML syntax error on line 21: element \\ | 3/4 | 3/4 | - | None | - | - | 26.2 |
| hf_timeout_param | feature/edge-coverage | error:TypeError("chat() got an unexpected keyword argument 'top_p'") | 2/6 | 2/6 | - | None | - | - | 437.8 |
| hf_validate_withdraw | robustness/silent-failure | done | 4/6 | 4/6 | - | False | - | - | 186.0 |
| hf_wrong_spec | fix/faulty-check | done | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 214.4 |
| wf1_crossfile | fix/misdirection | error:TypeError("chat() got an unexpected keyword argument 'top_p'") | 2/5 | 2/5 | - | None | - | - | 193.3 |
| wf2_retry | feature/edge-coverage | done | 0/5 | 0/5 | - | False | - | - | 143.0 |
| wf3_refactor | refactor/behaviour-preserving | done | 5/5 | 5/5 | - | True | - | - | 60.0 |
| wf3_refactor_blindview | refactor/behaviour-preserving | done | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 70.1 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | done | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 67.5 |
| wf4_assumption | perf/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 30.1 |
| wf5_partial | implement/edge-coverage | error:TypeError("chat() got an unexpected keyword argument 'top_p'") | 0/7 | 0/7 | - | None | - | - | 798.3 |
| wf6_multi | migration/multi-concern | done | 2/6 | 2/6 | DOCSCORE=0/4 TODOSCORE=0/3 | False | - | - | 373.2 |

**objective pass 5/24 - regressions 1 - check crashes 1 - decline accuracy 0/5**

> **10 of 34 runs did not execute** (the arm raised; `run_ok: false`). They are excluded from every figure above. See `error_trace` in the JSON.

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 7 | 0.82 |
| backward-compat | 4 | 0.31 |
| combined-score | 1 | 0.33 |
| concern-split | 1 | 0.33 |
| cross-file | 2 | 0.88 |
| decline-taxonomy | 1 | 0.67 |
| edge-coverage | 5 | 0.33 |
| greenfield-impl | 1 | 0.00 |
| kway-synth | 1 | 0.50 |
| partial-credit | 2 | 0.31 |
| premise-audit | 6 | 0.90 |
| regression-guard | 6 | 0.56 |
| silent-failure | 3 | 0.61 |
| witness-pair | 2 | 1.00 |
