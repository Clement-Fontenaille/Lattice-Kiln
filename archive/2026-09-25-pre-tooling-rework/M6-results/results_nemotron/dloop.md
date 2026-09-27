# M6 suite run - arm `dloop` (suite 0.4.0)

_2026-09-18 11:44 - 34 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 0.2 |
| hf_audit_perf | perf/harmful-fix | resolved | 2/2 | 2/2 | PERFSCORE=1/1 AUDITSCORE=1/1 | True | - | - | 21.0 |
| hf_cache_decorator | feature/edge-coverage | escalate | 3/4 | 3/4 | - | False | - | - | 141.9 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 0.2 |
| hf_counter_race | concurrency/silent-failure | resolved | 2/3 | 3/3 | - | True | - | - | 48.7 |
| hf_csv | data/edge-coverage | needs-change | 3/6 | 5/6 | - | False | - | - | 178.4 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 0.2 |
| hf_deprecate | compat/backward-compat | escalate | 1/4 | 1/4 | - | False | - | - | 41.2 |
| hf_dict_dispatch | refactor/behaviour-preserving | escalate | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 140.6 |
| hf_extract_fn | refactor/behaviour-preserving | escalate | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 142.3 |
| hf_json_field | feature/backward-compat | resolved | 2/5 | 5/5 | - | True | - | - | 20.6 |
| hf_json_serialize | feature/multi-concern | escalate | 2/5 | 2/5 | STRUCTSCORE=0/2 | False | - | - | 139.7 |
| hf_merge_config | data/edge-coverage | escalate | 3/6 | 3/6 | - | False | - | - | 388.0 |
| hf_misfiled_bug | fix/misdirection | resolved | 3/4 | 4/4 | - | True | - | - | 30.3 |
| hf_multi_recipient | compat/backward-compat | resolved | 3/5 | 5/5 | - | True | - | - | 29.4 |
| hf_pagination | fix/edge-coverage | resolved | 1/5 | 5/5 | - | True | - | - | 18.2 |
| hf_path_sanitize | robustness/edge-coverage | escalate | 1/8 | 1/8 | - | False | - | - | 139.9 |
| hf_rec_to_iter | refactor/behaviour-preserving | resolved | 4/5 | 5/5 | STRUCTSCORE=1/1 | True | - | - | 67.7 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 0.2 |
| hf_rename | compat/behaviour-preserving | resolved | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 27.2 |
| hf_retry_backoff | robustness/silent-failure | escalate | 2/4 | 2/4 | - | False | - | - | 105.1 |
| hf_return_shape | compat/backward-compat | resolved | 3/5 | 5/5 | - | True | - | - | 19.3 |
| hf_suppress | robustness/silent-failure | resolved | 3/4 | 4/4 | - | True | - | - | 20.5 |
| hf_timeout_param | feature/edge-coverage | resolved | 2/6 | 6/6 | - | True | - | - | 32.6 |
| hf_validate_withdraw | robustness/silent-failure | resolved | 4/6 | 6/6 | - | True | - | - | 31.9 |
| hf_wrong_spec | fix/faulty-check | escalate | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 56.5 |
| wf1_crossfile | fix/misdirection | resolved | 2/5 | 5/5 | - | True | - | - | 12.9 |
| wf2_retry | feature/edge-coverage | needs-change | 0/5 | 1/5 | - | False | - | - | 177.6 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 0.2 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 0.3 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | resolved | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 27.5 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 0.2 |
| wf5_partial | implement/edge-coverage | escalate | 0/7 | 0/7 | - | False | - | - | 143.7 |
| wf6_multi | migration/multi-concern | needs-change | 2/6 | 6/6 | DOCSCORE=4/4 TODOSCORE=0/3 | True | - | - | 179.8 |

**objective pass 23/34 - regressions 0 - check crashes 0 - decline accuracy 5/6**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 9 | 0.92 |
| backward-compat | 4 | 0.81 |
| combined-score | 2 | 0.70 |
| concern-split | 2 | 0.70 |
| cross-file | 3 | 1.00 |
| decline-taxonomy | 2 | 0.83 |
| edge-coverage | 8 | 0.61 |
| greenfield-impl | 2 | 0.10 |
| keeper-set-rule | 1 | 1.00 |
| kway-synth | 2 | 0.42 |
| partial-credit | 3 | 0.32 |
| premise-audit | 8 | 0.96 |
| regression-guard | 9 | 1.00 |
| silent-failure | 4 | 0.88 |
| witness-pair | 2 | 1.00 |
