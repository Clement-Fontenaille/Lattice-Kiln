# M6 suite run - arm `judge_anchored` (suite 0.4.1)

_2026-09-25 13:20 - 34 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 18.1 |
| hf_audit_perf | perf/harmful-fix | answered | 2/2 | 2/2 | PERFSCORE=1/1 AUDITSCORE=1/1 | True | - | - | 172.1 |
| hf_cache_decorator | feature/edge-coverage | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 241.6 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 14.6 |
| hf_counter_race | concurrency/silent-failure | answered | 2/3 | 3/3 | - | True | - | - | 34.1 |
| hf_csv | data/edge-coverage | answered | 3/6 | 6/6 | - | True | - | - | 181.5 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 14.0 |
| hf_deprecate | compat/backward-compat | blocked-no-progress | 1/4 | 1/4 | - | False | - | - | 143.6 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | False | - | - | 137.3 |
| hf_extract_fn | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 243.5 |
| hf_json_field | feature/backward-compat | answered | 2/5 | 5/5 | - | True | - | - | 34.7 |
| hf_json_serialize | feature/multi-concern | answered | 2/5 | 5/5 | STRUCTSCORE=2/2 | True | - | - | 190.3 |
| hf_merge_config | data/edge-coverage | blocked-partial | 3/6 | 5/6 | - | False | - | - | 602.9 |
| hf_misfiled_bug | fix/misdirection | blocked-no-progress | 3/4 | 3/4 | - | False | - | - | 92.2 |
| hf_multi_recipient | compat/backward-compat | answered | 3/5 | 5/5 | - | True | - | - | 185.5 |
| hf_pagination | fix/edge-coverage | answered | 1/5 | 5/5 | - | True | - | - | 143.5 |
| hf_path_sanitize | robustness/edge-coverage | answered | 1/8 | 8/8 | - | True | - | - | 205.1 |
| hf_rec_to_iter | refactor/behaviour-preserving | answered | 4/5 | 5/5 | STRUCTSCORE=1/1 | True | - | - | 43.8 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 18.7 |
| hf_rename | compat/behaviour-preserving | answered | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 463.2 |
| hf_retry_backoff | robustness/silent-failure | blocked-no-progress | 2/4 | 2/4 | - | False | - | - | 371.5 |
| hf_return_shape | compat/backward-compat | blocked-no-progress | 3/5 | 3/5 | - | False | - | - | 110.3 |
| hf_suppress | robustness/silent-failure | answered | 3/4 | 4/4 | - | True | - | - | 413.7 |
| hf_timeout_param | feature/edge-coverage | blocked-partial | 2/6 | 5/6 | - | False | - | - | 120.9 |
| hf_validate_withdraw | robustness/silent-failure | answered | 4/6 | 6/6 | - | True | - | - | 39.2 |
| hf_wrong_spec | fix/faulty-check | blocked-no-progress | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 59.2 |
| wf1_crossfile | fix/misdirection | answered | 2/5 | 5/5 | - | True | - | - | 114.1 |
| wf2_retry | feature/edge-coverage | answered | 0/5 | 5/5 | - | True | - | - | 98.7 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 155.4 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 18.7 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | answered | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 644.8 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 18.4 |
| wf5_partial | implement/edge-coverage | answered | 0/7 | 7/7 | - | True | - | - | 142.7 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 5/6 | DOCSCORE=4/4 TODOSCORE=3/3 | False | YES | - | 416.5 |

**objective pass 23/34 - regressions 1 - check crashes 0 - decline accuracy 5/6**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 9 | 0.92 |
| backward-compat | 4 | 0.71 |
| combined-score | 2 | 0.92 |
| concern-split | 2 | 0.92 |
| cross-file | 3 | 0.92 |
| decline-taxonomy | 2 | 0.83 |
| edge-coverage | 8 | 0.86 |
| greenfield-impl | 2 | 1.00 |
| keeper-set-rule | 1 | 1.00 |
| kway-synth | 2 | 1.00 |
| partial-credit | 3 | 1.00 |
| premise-audit | 8 | 0.93 |
| regression-guard | 9 | 0.96 |
| silent-failure | 4 | 0.88 |
| witness-pair | 2 | 1.00 |
