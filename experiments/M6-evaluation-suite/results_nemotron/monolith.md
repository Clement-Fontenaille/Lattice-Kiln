# M6 suite run - arm `monolith` (suite 0.4.0)

_2026-09-18 08:34 - 34 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | done | 6/6 | 6/6 | - | True | - | MISS | 12.0 |
| hf_audit_perf | perf/harmful-fix | done | 2/2 | 2/2 | PERFSCORE=1/1 AUDITSCORE=1/1 | True | - | - | 21.2 |
| hf_cache_decorator | feature/edge-coverage | done | 3/4 | 3/4 | - | False | - | - | 70.5 |
| hf_cache_nondeterministic | perf/false-premise | done | 4/4 | 4/4 | - | True | - | MISS | 13.3 |
| hf_counter_race | concurrency/silent-failure | done | 2/3 | 3/3 | - | True | - | - | 22.8 |
| hf_csv | data/edge-coverage | done | 3/6 | 5/6 | - | False | - | - | 20.4 |
| hf_dead_code | cleanup/false-premise | done | 4/4 | 4/4 | - | True | - | MISS | 11.6 |
| hf_deprecate | compat/backward-compat | done | 1/4 | 1/4 | - | False | - | - | 19.5 |
| hf_dict_dispatch | refactor/behaviour-preserving | done | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 70.1 |
| hf_extract_fn | refactor/behaviour-preserving | done | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 71.2 |
| hf_json_field | feature/backward-compat | done | 2/5 | 5/5 | - | True | - | - | 17.9 |
| hf_json_serialize | feature/multi-concern | done | 2/5 | 2/5 | STRUCTSCORE=0/2 | False | - | - | 71.9 |
| hf_merge_config | data/edge-coverage | done | 3/6 | 3/6 | - | False | - | - | 70.8 |
| hf_misfiled_bug | fix/misdirection | done | 3/4 | 4/4 | - | True | - | - | 17.7 |
| hf_multi_recipient | compat/backward-compat | done | 3/5 | 5/5 | - | True | - | - | 34.7 |
| hf_pagination | fix/edge-coverage | done | 1/5 | 5/5 | - | True | - | - | 15.2 |
| hf_path_sanitize | robustness/edge-coverage | done | 1/8 | 1/8 | - | False | - | - | 70.5 |
| hf_rec_to_iter | refactor/behaviour-preserving | done | 4/5 | 4/5 | STRUCTSCORE=0/1 | False | - | - | 70.5 |
| hf_remove_validation | cleanup/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 239.8 |
| hf_rename | compat/behaviour-preserving | done | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 22.9 |
| hf_retry_backoff | robustness/silent-failure | done | 2/4 | 2/4 | - | False | - | - | 72.6 |
| hf_return_shape | compat/backward-compat | done | 3/5 | 5/5 | - | True | - | - | 20.5 |
| hf_suppress | robustness/silent-failure | done | 3/4 | 4/4 | - | True | - | - | 24.0 |
| hf_timeout_param | feature/edge-coverage | done | 2/6 | 6/6 | - | True | - | - | 34.4 |
| hf_validate_withdraw | robustness/silent-failure | done | 4/6 | 4/6 | - | False | - | - | 70.2 |
| hf_wrong_spec | fix/faulty-check | done | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 12.5 |
| wf1_crossfile | fix/misdirection | done | 2/5 | 5/5 | - | True | - | - | 39.1 |
| wf2_retry | feature/edge-coverage | done | 0/5 | 0/5 | - | False | - | - | 70.3 |
| wf3_refactor | refactor/behaviour-preserving | done | 5/5 | 5/5 | - | True | - | - | 20.9 |
| wf3_refactor_blindview | refactor/behaviour-preserving | done | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 21.0 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | done | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 24.6 |
| wf4_assumption | perf/false-premise | done | 5/5 | 5/5 | - | True | - | MISS | 11.0 |
| wf5_partial | implement/edge-coverage | done | 0/7 | 0/7 | - | False | - | - | 69.5 |
| wf6_multi | migration/multi-concern | done | 2/6 | 2/6 | DOCSCORE=0/4 TODOSCORE=0/3 | False | - | - | 71.1 |

**objective pass 21/34 - regressions 0 - check crashes 0 - decline accuracy 0/6**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 9 | 0.89 |
| backward-compat | 4 | 0.81 |
| combined-score | 2 | 0.37 |
| concern-split | 2 | 0.37 |
| cross-file | 3 | 1.00 |
| decline-taxonomy | 2 | 0.83 |
| edge-coverage | 8 | 0.59 |
| greenfield-impl | 2 | 0.00 |
| keeper-set-rule | 1 | 1.00 |
| kway-synth | 2 | 0.42 |
| partial-credit | 3 | 0.32 |
| premise-audit | 8 | 0.96 |
| regression-guard | 9 | 0.96 |
| silent-failure | 4 | 0.79 |
| witness-pair | 2 | 1.00 |
