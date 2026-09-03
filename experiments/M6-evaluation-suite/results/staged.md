# M6 suite run - arm `staged` (suite 0.1.0)

_2026-09-02 12:37 - 30 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 10.0 |
| hf_cache_decorator | feature/edge-coverage | escalate | 3/4 | 3/4 | - | False | - | - | 22.6 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 9.0 |
| hf_counter_race | concurrency/silent-failure | resolved | 2/3 | 3/3 | - | True | - | - | 16.5 |
| hf_csv | data/edge-coverage | declined | 3/6 | 3/6 | - | False | - | - | 9.6 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 8.8 |
| hf_deprecate | compat/backward-compat | resolved | 1/4 | 4/4 | - | True | - | - | 15.3 |
| hf_dict_dispatch | refactor/behaviour-preserving | escalate | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 23.7 |
| hf_extract_fn | refactor/behaviour-preserving | escalate | 5/5 | 5/5 | STRUCTSCORE=1/3 | True | - | - | 26.0 |
| hf_json_field | feature/backward-compat | declined | 2/5 | 2/5 | - | False | - | - | 9.1 |
| hf_json_serialize | feature/multi-concern | declined | 2/5 | 2/5 | STRUCTSCORE=0/2 | False | - | - | 9.4 |
| hf_merge_config | data/edge-coverage | declined | 3/6 | 3/6 | - | False | - | - | 9.8 |
| hf_misfiled_bug | fix/misdirection | escalate | 3/4 | 3/4 | - | False | - | - | 21.0 |
| hf_multi_recipient | compat/backward-compat | escalate | 3/5 | 3/5 | - | False | - | - | 26.0 |
| hf_pagination | fix/edge-coverage | resolved | 1/5 | 5/5 | - | True | - | - | 14.2 |
| hf_path_sanitize | robustness/edge-coverage | declined | 1/8 | 1/8 | - | False | - | - | 9.1 |
| hf_rec_to_iter | refactor/behaviour-preserving | escalate | 4/5 | 4/5 | STRUCTSCORE=0/1 | False | - | - | 25.9 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 9.5 |
| hf_rename | compat/behaviour-preserving | resolved | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 16.8 |
| hf_retry_backoff | robustness/silent-failure | resolved | 2/4 | 4/4 | - | True | - | - | 17.8 |
| hf_return_shape | compat/backward-compat | resolved | 3/5 | 5/5 | - | True | - | - | 21.8 |
| hf_suppress | robustness/silent-failure | declined | 3/4 | 3/4 | - | False | - | - | 9.5 |
| hf_timeout_param | feature/edge-coverage | escalate | 2/6 | 2/6 | - | False | - | - | 28.4 |
| hf_validate_withdraw | robustness/silent-failure | resolved | 4/6 | 6/6 | - | True | - | - | 14.5 |
| wf1_crossfile | fix/misdirection | resolved | 2/5 | 5/5 | - | True | - | - | 14.3 |
| wf2_retry | feature/edge-coverage | resolved | 0/5 | 5/5 | - | True | - | - | 14.3 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 9.5 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 9.2 |
| wf5_partial | implement/edge-coverage | resolved | 0/7 | 7/7 | - | True | - | - | 25.8 |
| wf6_multi | migration/multi-concern | needs-change | 2/6 | 6/6 | DOCSCORE=0/4 TODOSCORE=3/3 | True | - | - | 252.2 |

**objective pass 19/30 - regressions 0 - check crashes 0 - decline accuracy 5/5**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 6 | 0.97 |
| backward-compat | 4 | 0.75 |
| combined-score | 2 | 0.70 |
| concern-split | 2 | 0.70 |
| cross-file | 3 | 0.92 |
| edge-coverage | 8 | 0.65 |
| greenfield-impl | 2 | 1.00 |
| kway-synth | 2 | 0.75 |
| partial-credit | 3 | 0.54 |
| premise-audit | 7 | 0.96 |
| regression-guard | 9 | 0.86 |
| silent-failure | 4 | 0.94 |
