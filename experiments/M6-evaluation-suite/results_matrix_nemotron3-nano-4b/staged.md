# M6 suite run - arm `staged` (suite 0.4.1)

_2026-09-25 19:21 - 34 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 18.3 |
| hf_audit_perf | perf/harmful-fix | resolved | 2/2 | 2/2 | PERFSCORE=1/1 AUDITSCORE=1/1 | True | - | - | 37.2 |
| hf_cache_decorator | feature/edge-coverage | escalate | 3/4 | 3/4 | - | False | - | - | 101.2 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 25.2 |
| hf_counter_race | concurrency/silent-failure | escalate | 2/3 | 2/3 | - | False | - | - | 46.6 |
| hf_csv | data/edge-coverage | needs-change | 3/6 | 5/6 | - | False | - | - | 87.7 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 17.7 |
| hf_deprecate | compat/backward-compat | escalate | 1/4 | 1/4 | - | False | - | - | 51.2 |
| hf_dict_dispatch | refactor/behaviour-preserving | escalate | 7/7 | 7/7 | STRUCTSCORE=0/3 | False | - | - | 102.5 |
| hf_extract_fn | refactor/behaviour-preserving | resolved | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 37.6 |
| hf_json_field | feature/backward-compat | resolved | 2/5 | 5/5 | - | True | - | - | 26.8 |
| hf_json_serialize | feature/multi-concern | resolved | 2/5 | 5/5 | STRUCTSCORE=2/2 | True | - | - | 459.8 |
| hf_merge_config | data/edge-coverage | resolved | 3/6 | 6/6 | - | True | - | - | 69.3 |
| hf_misfiled_bug | fix/misdirection | declined | 3/4 | 3/4 | - | False | - | - | 19.6 |
| hf_multi_recipient | compat/backward-compat | escalate | 3/5 | 3/5 | - | False | - | - | 62.9 |
| hf_pagination | fix/edge-coverage | resolved | 1/5 | 5/5 | - | True | - | - | 63.6 |
| hf_path_sanitize | robustness/edge-coverage | resolved | 1/8 | 8/8 | - | True | - | - | 72.1 |
| hf_rec_to_iter | refactor/behaviour-preserving | escalate | 4/5 | 4/5 | STRUCTSCORE=0/1 | False | - | - | 45.0 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 17.4 |
| hf_rename | compat/behaviour-preserving | resolved | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 161.1 |
| hf_retry_backoff | robustness/silent-failure | resolved | 2/4 | 4/4 | - | True | - | - | 76.9 |
| hf_return_shape | compat/backward-compat | resolved | 3/5 | 5/5 | - | True | - | - | 48.4 |
| hf_suppress | robustness/silent-failure | resolved | 3/4 | 4/4 | - | True | - | - | 50.0 |
| hf_timeout_param | feature/edge-coverage | resolved | 2/6 | 6/6 | - | True | - | - | 56.3 |
| hf_validate_withdraw | robustness/silent-failure | resolved | 4/6 | 6/6 | - | True | - | - | 35.2 |
| hf_wrong_spec | fix/faulty-check | escalate | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 36.9 |
| wf1_crossfile | fix/misdirection | resolved | 2/5 | 5/5 | - | True | - | - | 27.5 |
| wf2_retry | feature/edge-coverage | resolved | 0/5 | 5/5 | - | True | - | - | 38.8 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 18.3 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 18.0 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | resolved | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 33.9 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 21.5 |
| wf5_partial | implement/edge-coverage | resolved | 0/7 | 7/7 | - | True | - | - | 36.8 |
| wf6_multi | migration/multi-concern | needs-change | 2/6 | 6/6 | DOCSCORE=4/4 TODOSCORE=3/3 | True | - | - | 466.1 |

**objective pass 24/34 - regressions 0 - check crashes 0 - decline accuracy 5/6**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 9 | 0.89 |
| backward-compat | 4 | 0.71 |
| combined-score | 2 | 1.00 |
| concern-split | 2 | 1.00 |
| cross-file | 3 | 0.92 |
| decline-taxonomy | 2 | 0.83 |
| edge-coverage | 8 | 0.95 |
| greenfield-impl | 2 | 1.00 |
| keeper-set-rule | 1 | 1.00 |
| kway-synth | 2 | 0.92 |
| partial-credit | 3 | 0.94 |
| premise-audit | 8 | 0.93 |
| regression-guard | 9 | 0.96 |
| silent-failure | 4 | 0.92 |
| witness-pair | 2 | 1.00 |
