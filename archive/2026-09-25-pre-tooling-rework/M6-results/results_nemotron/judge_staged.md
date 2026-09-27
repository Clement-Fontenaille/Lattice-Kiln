# M6 suite run - arm `judge_staged` (suite 0.4.0)

_2026-09-18 18:51 - 34 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 23.2 |
| hf_audit_perf | perf/harmful-fix | answered | 2/2 | 2/2 | PERFSCORE=1/1 AUDITSCORE=1/1 | True | - | - | 37.9 |
| hf_cache_decorator | feature/edge-coverage | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 194.9 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 23.4 |
| hf_counter_race | concurrency/silent-failure | answered | 2/3 | 3/3 | - | True | - | - | 46.3 |
| hf_csv | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 172.7 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 22.8 |
| hf_deprecate | compat/backward-compat | blocked-no-progress | 1/4 | 1/4 | - | False | - | - | 78.4 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 560.5 |
| hf_extract_fn | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 236.1 |
| hf_json_field | feature/backward-compat | answered | 2/5 | 5/5 | - | True | - | - | 37.5 |
| hf_json_serialize | feature/multi-concern | blocked-partial | 2/5 | 5/5 | STRUCTSCORE=0/2 | True | - | - | 570.6 |
| hf_merge_config | data/edge-coverage | blocked-no-progress | 3/6 | 3/6 | - | False | - | - | 226.2 |
| hf_misfiled_bug | fix/misdirection | answered | 3/4 | 4/4 | - | True | - | - | 32.2 |
| hf_multi_recipient | compat/backward-compat | blocked-no-progress | 3/5 | 3/5 | - | False | - | - | 155.0 |
| hf_pagination | fix/edge-coverage | answered | 1/5 | 5/5 | - | True | - | - | 32.8 |
| hf_path_sanitize | robustness/edge-coverage | blocked-no-progress | 1/8 | 1/8 | - | False | - | - | 233.2 |
| hf_rec_to_iter | refactor/behaviour-preserving | answered | 4/5 | 5/5 | STRUCTSCORE=1/1 | True | - | - | 93.6 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 23.9 |
| hf_rename | compat/behaviour-preserving | answered | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 53.3 |
| hf_retry_backoff | robustness/silent-failure | blocked-no-progress | 2/4 | 2/4 | - | False | - | - | 237.1 |
| hf_return_shape | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 61.8 |
| hf_suppress | robustness/silent-failure | answered | 3/4 | 4/4 | - | True | - | - | 109.0 |
| hf_timeout_param | feature/edge-coverage | answered | 2/6 | 6/6 | - | True | - | - | 131.0 |
| hf_validate_withdraw | robustness/silent-failure | answered | 4/6 | 6/6 | - | True | - | - | 55.6 |
| hf_wrong_spec | fix/faulty-check | blocked-no-progress | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 80.9 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 41.8 |
| wf2_retry | feature/edge-coverage | answered | 0/5 | 5/5 | - | True | - | - | 158.5 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 23.7 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 22.8 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 41.9 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 23.8 |
| wf5_partial | implement/edge-coverage | blocked-no-progress | 0/7 | 0/7 | - | False | - | - | 234.6 |
| wf6_multi | migration/multi-concern | answered | 2/6 | 6/6 | DOCSCORE=4/4 TODOSCORE=3/3 | True | - | - | 661.3 |

**objective pass 25/34 - regressions 0 - check crashes 0 - decline accuracy 5/6**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 9 | 0.92 |
| backward-compat | 4 | 0.71 |
| combined-score | 2 | 1.00 |
| concern-split | 2 | 1.00 |
| cross-file | 3 | 1.00 |
| decline-taxonomy | 2 | 0.83 |
| edge-coverage | 8 | 0.73 |
| greenfield-impl | 2 | 0.50 |
| keeper-set-rule | 1 | 1.00 |
| kway-synth | 2 | 0.50 |
| partial-credit | 3 | 0.38 |
| premise-audit | 8 | 0.96 |
| regression-guard | 9 | 0.96 |
| silent-failure | 4 | 0.88 |
| witness-pair | 2 | 1.00 |
