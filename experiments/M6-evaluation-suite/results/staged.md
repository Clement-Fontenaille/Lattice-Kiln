# M6 suite run - arm `staged` (suite 0.4.0)

_2026-09-15 03:31 - 102 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 10.0 |
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 26.5 |
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 15.8 |
| hf_audit_perf | perf/harmful-fix | declined | 2/2 | 2/2 | PERFSCORE=0/1 AUDITSCORE=1/1 | False | - | - | 13.9 |
| hf_audit_perf | perf/harmful-fix | declined | 2/2 | 2/2 | PERFSCORE=0/1 AUDITSCORE=1/1 | False | - | - | 26.5 |
| hf_audit_perf | perf/harmful-fix | resolved | 2/2 | 2/2 | PERFSCORE=1/1 AUDITSCORE=1/1 | True | - | - | 30.3 |
| hf_cache_decorator | feature/edge-coverage | escalate | 3/4 | 3/4 | - | False | - | - | 22.6 |
| hf_cache_decorator | feature/edge-coverage | escalate | 3/4 | 3/4 | - | False | - | - | 34.5 |
| hf_cache_decorator | feature/edge-coverage | escalate | 3/4 | 3/4 | - | False | - | - | 38.5 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 9.0 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 15.6 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 15.3 |
| hf_counter_race | concurrency/silent-failure | resolved | 2/3 | 3/3 | - | True | - | - | 16.5 |
| hf_counter_race | concurrency/silent-failure | resolved | 2/3 | 3/3 | - | True | - | - | 26.4 |
| hf_counter_race | concurrency/silent-failure | resolved | 2/3 | 3/3 | - | True | - | - | 27.6 |
| hf_csv | data/edge-coverage | declined | 3/6 | 3/6 | - | False | - | - | 9.6 |
| hf_csv | data/edge-coverage | declined | 3/6 | 3/6 | - | False | - | - | 18.2 |
| hf_csv | data/edge-coverage | declined | 3/6 | 3/6 | - | False | - | - | 16.4 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 8.8 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 14.7 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 17.7 |
| hf_deprecate | compat/backward-compat | resolved | 1/4 | 4/4 | - | True | - | - | 15.3 |
| hf_deprecate | compat/backward-compat | resolved | 1/4 | 4/4 | - | True | - | - | 29.3 |
| hf_deprecate | compat/backward-compat | resolved | 1/4 | 4/4 | - | True | - | - | 26.7 |
| hf_dict_dispatch | refactor/behaviour-preserving | escalate | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 23.7 |
| hf_dict_dispatch | refactor/behaviour-preserving | escalate | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 35.6 |
| hf_dict_dispatch | refactor/behaviour-preserving | escalate | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 43.7 |
| hf_extract_fn | refactor/behaviour-preserving | escalate | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 26.0 |
| hf_extract_fn | refactor/behaviour-preserving | resolved | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 37.4 |
| hf_extract_fn | refactor/behaviour-preserving | escalate | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 37.7 |
| hf_json_field | feature/backward-compat | declined | 2/5 | 2/5 | - | False | - | - | 9.1 |
| hf_json_field | feature/backward-compat | declined | 2/5 | 2/5 | - | False | - | - | 15.3 |
| hf_json_field | feature/backward-compat | resolved | 2/5 | 5/5 | - | True | - | - | 28.5 |
| hf_json_serialize | feature/multi-concern | declined | 2/5 | 2/5 | STRUCTSCORE=0/2 | False | - | - | 9.4 |
| hf_json_serialize | feature/multi-concern | declined | 2/5 | 2/5 | STRUCTSCORE=0/2 | False | - | - | 17.6 |
| hf_json_serialize | feature/multi-concern | declined | 2/5 | 2/5 | STRUCTSCORE=0/2 | False | - | - | 19.5 |
| hf_merge_config | data/edge-coverage | declined | 3/6 | 3/6 | - | False | - | - | 9.8 |
| hf_merge_config | data/edge-coverage | declined | 3/6 | 3/6 | - | False | - | - | 18.0 |
| hf_merge_config | data/edge-coverage | declined | 3/6 | 3/6 | - | False | - | - | 27.0 |
| hf_misfiled_bug | fix/misdirection | escalate | 3/4 | 3/4 | - | False | - | - | 21.0 |
| hf_misfiled_bug | fix/misdirection | declined | 3/4 | 3/4 | - | False | - | - | 14.9 |
| hf_misfiled_bug | fix/misdirection | declined | 3/4 | 3/4 | - | False | - | - | 18.2 |
| hf_multi_recipient | compat/backward-compat | escalate | 3/5 | 3/5 | - | False | - | - | 26.0 |
| hf_multi_recipient | compat/backward-compat | escalate | 3/5 | 3/5 | - | False | - | - | 44.7 |
| hf_multi_recipient | compat/backward-compat | escalate | 3/5 | 3/5 | - | False | - | - | 44.3 |
| hf_pagination | fix/edge-coverage | resolved | 1/5 | 5/5 | - | True | - | - | 14.2 |
| hf_pagination | fix/edge-coverage | resolved | 1/5 | 5/5 | - | True | - | - | 23.5 |
| hf_pagination | fix/edge-coverage | resolved | 1/5 | 5/5 | - | True | - | - | 31.1 |
| hf_path_sanitize | robustness/edge-coverage | declined | 1/8 | 1/8 | - | False | - | - | 9.1 |
| hf_path_sanitize | robustness/edge-coverage | declined | 1/8 | 1/8 | - | False | - | - | 18.6 |
| hf_path_sanitize | robustness/edge-coverage | declined | 1/8 | 1/8 | - | False | - | - | 20.3 |
| hf_rec_to_iter | refactor/behaviour-preserving | escalate | 4/5 | 4/5 | STRUCTSCORE=0/1 | False | - | - | 25.9 |
| hf_rec_to_iter | refactor/behaviour-preserving | escalate | 4/5 | 4/5 | STRUCTSCORE=0/1 | False | - | - | 53.4 |
| hf_rec_to_iter | refactor/behaviour-preserving | escalate | 4/5 | 4/5 | STRUCTSCORE=0/1 | False | - | - | 34.4 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 9.5 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 14.5 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 15.1 |
| hf_rename | compat/behaviour-preserving | resolved | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 16.8 |
| hf_rename | compat/behaviour-preserving | resolved | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 28.4 |
| hf_rename | compat/behaviour-preserving | resolved | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 22.7 |
| hf_retry_backoff | robustness/silent-failure | resolved | 2/4 | 4/4 | - | True | - | - | 17.8 |
| hf_retry_backoff | robustness/silent-failure | resolved | 2/4 | 4/4 | - | True | - | - | 28.9 |
| hf_retry_backoff | robustness/silent-failure | resolved | 2/4 | 4/4 | - | True | - | - | 35.2 |
| hf_return_shape | compat/backward-compat | resolved | 3/5 | 5/5 | - | True | - | - | 21.8 |
| hf_return_shape | compat/backward-compat | resolved | 3/5 | 5/5 | - | True | - | - | 36.9 |
| hf_return_shape | compat/backward-compat | resolved | 3/5 | 5/5 | - | True | - | - | 33.1 |
| hf_suppress | robustness/silent-failure | declined | 3/4 | 3/4 | - | False | - | - | 9.5 |
| hf_suppress | robustness/silent-failure | declined | 3/4 | 3/4 | - | False | - | - | 19.0 |
| hf_suppress | robustness/silent-failure | declined | 3/4 | 3/4 | - | False | - | - | 15.8 |
| hf_timeout_param | feature/edge-coverage | escalate | 2/6 | 2/6 | - | False | - | - | 28.4 |
| hf_timeout_param | feature/edge-coverage | escalate | 2/6 | 2/6 | - | False | - | - | 53.9 |
| hf_timeout_param | feature/edge-coverage | needs-change | 2/6 | 5/6 | - | False | - | - | 49.0 |
| hf_validate_withdraw | robustness/silent-failure | resolved | 4/6 | 6/6 | - | True | - | - | 14.5 |
| hf_validate_withdraw | robustness/silent-failure | resolved | 4/6 | 6/6 | - | True | - | - | 31.4 |
| hf_validate_withdraw | robustness/silent-failure | resolved | 4/6 | 6/6 | - | True | - | - | 26.4 |
| hf_wrong_spec | fix/faulty-check | declined | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | ok | 14.3 |
| hf_wrong_spec | fix/faulty-check | escalate | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 38.4 |
| hf_wrong_spec | fix/faulty-check | escalate | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 40.6 |
| wf1_crossfile | fix/misdirection | resolved | 2/5 | 5/5 | - | True | - | - | 14.3 |
| wf1_crossfile | fix/misdirection | resolved | 2/5 | 5/5 | - | True | - | - | 33.7 |
| wf1_crossfile | fix/misdirection | resolved | 2/5 | 5/5 | - | True | - | - | 38.7 |
| wf2_retry | feature/edge-coverage | resolved | 0/5 | 5/5 | - | True | - | - | 14.3 |
| wf2_retry | feature/edge-coverage | resolved | 0/5 | 5/5 | - | True | - | - | 30.6 |
| wf2_retry | feature/edge-coverage | resolved | 0/5 | 5/5 | - | True | - | - | 26.0 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 9.5 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 29.2 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 17.0 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 13.4 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 17.5 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 12.5 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | resolved | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 22.3 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | resolved | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 15.4 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | resolved | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 15.9 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 9.2 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 17.8 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 21.3 |
| wf5_partial | implement/edge-coverage | resolved | 0/7 | 7/7 | - | True | - | - | 25.8 |
| wf5_partial | implement/edge-coverage | needs-change | 0/7 | 4/7 | - | False | - | - | 66.3 |
| wf5_partial | implement/edge-coverage | needs-change | 0/7 | 5/7 | - | False | - | - | 56.1 |
| wf6_multi | migration/multi-concern | needs-change | 2/6 | 6/6 | DOCSCORE=0/4 TODOSCORE=3/3 | True | - | - | 252.2 |
| wf6_multi | migration/multi-concern | escalate | 2/6 | 2/6 | DOCSCORE=0/4 TODOSCORE=0/3 | False | - | - | 323.8 |
| wf6_multi | migration/multi-concern | needs-change | 2/6 | 6/6 | DOCSCORE=0/4 TODOSCORE=3/3 | True | - | - | 302.4 |

**objective pass 59/102 - regressions 0 - check crashes 0 - decline accuracy 16/18**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 27 | 0.98 |
| backward-compat | 12 | 0.80 |
| combined-score | 6 | 0.59 |
| concern-split | 6 | 0.59 |
| cross-file | 9 | 0.92 |
| decline-taxonomy | 6 | 0.83 |
| edge-coverage | 24 | 0.67 |
| greenfield-impl | 6 | 0.88 |
| keeper-set-rule | 3 | 1.00 |
| kway-synth | 6 | 0.63 |
| partial-credit | 9 | 0.46 |
| premise-audit | 24 | 0.93 |
| regression-guard | 27 | 0.88 |
| silent-failure | 12 | 0.94 |
| witness-pair | 6 | 1.00 |
