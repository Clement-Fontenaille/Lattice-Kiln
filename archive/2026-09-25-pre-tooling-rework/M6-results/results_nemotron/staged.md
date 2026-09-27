# M6 suite run - arm `staged` (suite 0.4.0)

_2026-09-18 16:17 - 34 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 20.6 |
| hf_audit_perf | perf/harmful-fix | resolved | 2/2 | 2/2 | PERFSCORE=1/1 AUDITSCORE=1/1 | True | - | - | 45.8 |
| hf_cache_decorator | feature/edge-coverage | escalate | 3/4 | 3/4 | - | False | - | - | 161.4 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 21.2 |
| hf_counter_race | concurrency/silent-failure | resolved | 2/3 | 3/3 | - | True | - | - | 48.2 |
| hf_csv | data/edge-coverage | needs-change | 3/6 | 5/6 | - | False | - | - | 427.4 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 20.1 |
| hf_deprecate | compat/backward-compat | resolved | 1/4 | 4/4 | - | True | - | - | 52.6 |
| hf_dict_dispatch | refactor/behaviour-preserving | escalate | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 165.1 |
| hf_extract_fn | refactor/behaviour-preserving | escalate | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 160.5 |
| hf_json_field | feature/backward-compat | resolved | 2/5 | 5/5 | - | True | - | - | 39.1 |
| hf_json_serialize | feature/multi-concern | needs-change | 2/5 | 5/5 | STRUCTSCORE=0/2 | True | - | - | 382.4 |
| hf_merge_config | data/edge-coverage | escalate | 3/6 | 3/6 | - | False | - | - | 162.0 |
| hf_misfiled_bug | fix/misdirection | resolved | 3/4 | 4/4 | - | True | - | - | 54.8 |
| hf_multi_recipient | compat/backward-compat | escalate | 3/5 | 3/5 | - | False | - | - | 70.9 |
| hf_pagination | fix/edge-coverage | resolved | 1/5 | 5/5 | - | True | - | - | 43.1 |
| hf_path_sanitize | robustness/edge-coverage | escalate | 1/8 | 1/8 | - | False | - | - | 162.5 |
| hf_rec_to_iter | refactor/behaviour-preserving | resolved | 4/5 | 5/5 | STRUCTSCORE=1/1 | True | - | - | 156.9 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 20.2 |
| hf_rename | compat/behaviour-preserving | resolved | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 54.7 |
| hf_retry_backoff | robustness/silent-failure | escalate | 2/4 | 2/4 | - | False | - | - | 163.6 |
| hf_return_shape | compat/backward-compat | resolved | 3/5 | 5/5 | - | True | - | - | 47.5 |
| hf_suppress | robustness/silent-failure | resolved | 3/4 | 4/4 | - | True | - | - | 89.1 |
| hf_timeout_param | feature/edge-coverage | resolved | 2/6 | 6/6 | - | True | - | - | 52.5 |
| hf_validate_withdraw | robustness/silent-failure | resolved | 4/6 | 6/6 | - | True | - | - | 58.4 |
| hf_wrong_spec | fix/faulty-check | escalate | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 58.5 |
| wf1_crossfile | fix/misdirection | resolved | 2/5 | 5/5 | - | True | - | - | 50.2 |
| wf2_retry | feature/edge-coverage | resolved | 0/5 | 5/5 | - | True | - | - | 187.0 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 20.2 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 20.1 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | resolved | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 48.5 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 19.7 |
| wf5_partial | implement/edge-coverage | resolved | 0/7 | 7/7 | - | True | - | - | 55.8 |
| wf6_multi | migration/multi-concern | escalate | 2/6 | 2/6 | DOCSCORE=0/4 TODOSCORE=0/3 | False | - | - | 443.4 |

**objective pass 25/34 - regressions 0 - check crashes 0 - decline accuracy 5/6**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 9 | 1.00 |
| backward-compat | 4 | 0.90 |
| combined-score | 2 | 0.67 |
| concern-split | 2 | 0.67 |
| cross-file | 3 | 1.00 |
| decline-taxonomy | 2 | 0.83 |
| edge-coverage | 8 | 0.71 |
| greenfield-impl | 2 | 1.00 |
| keeper-set-rule | 1 | 1.00 |
| kway-synth | 2 | 0.92 |
| partial-credit | 3 | 0.65 |
| premise-audit | 8 | 0.96 |
| regression-guard | 9 | 0.96 |
| silent-failure | 4 | 0.88 |
| witness-pair | 2 | 1.00 |
