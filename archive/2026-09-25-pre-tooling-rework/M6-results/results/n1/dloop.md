# M6 suite run - arm `dloop` (suite 0.1.0)

_2026-09-02 12:25 - 30 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 0.2 |
| hf_cache_decorator | feature/edge-coverage | resolved | 3/4 | 4/4 | - | True | - | - | 12.5 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 0.2 |
| hf_counter_race | concurrency/silent-failure | resolved | 2/3 | 3/3 | - | True | - | - | 7.3 |
| hf_csv | data/edge-coverage | resolved | 3/6 | 6/6 | - | True | - | - | 7.2 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 0.2 |
| hf_deprecate | compat/backward-compat | resolved | 1/4 | 4/4 | - | True | - | - | 7.0 |
| hf_dict_dispatch | refactor/behaviour-preserving | escalate | 7/7 | 7/7 | STRUCTSCORE=0/3 | True | - | - | 15.6 |
| hf_extract_fn | refactor/behaviour-preserving | resolved | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 21.1 |
| hf_json_field | feature/backward-compat | resolved | 2/5 | 5/5 | - | True | - | - | 6.1 |
| hf_json_serialize | feature/multi-concern | needs-change | 2/5 | 5/5 | STRUCTSCORE=1/2 | True | - | - | 51.4 |
| hf_merge_config | data/edge-coverage | resolved | 3/6 | 6/6 | - | True | - | - | 7.1 |
| hf_misfiled_bug | fix/misdirection | escalate | 3/4 | 3/4 | - | False | - | - | 14.4 |
| hf_multi_recipient | compat/backward-compat | escalate | 3/5 | 3/5 | - | False | - | - | 14.6 |
| hf_pagination | fix/edge-coverage | resolved | 1/5 | 5/5 | - | True | - | - | 7.9 |
| hf_path_sanitize | robustness/edge-coverage | resolved | 1/8 | 8/8 | - | True | - | - | 7.7 |
| hf_rec_to_iter | refactor/behaviour-preserving | escalate | 4/5 | 4/5 | STRUCTSCORE=0/1 | False | - | - | 17.5 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 0.5 |
| hf_rename | compat/behaviour-preserving | resolved | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 8.5 |
| hf_retry_backoff | robustness/silent-failure | resolved | 2/4 | 4/4 | - | True | - | - | 8.9 |
| hf_return_shape | compat/backward-compat | resolved | 3/5 | 5/5 | - | True | - | - | 6.4 |
| hf_suppress | robustness/silent-failure | resolved | 3/4 | 4/4 | - | True | - | - | 6.5 |
| hf_timeout_param | feature/edge-coverage | needs-change | 2/6 | 5/6 | - | False | - | - | 25.2 |
| hf_validate_withdraw | robustness/silent-failure | resolved | 4/6 | 6/6 | - | True | - | - | 6.8 |
| wf1_crossfile | fix/misdirection | resolved | 2/5 | 5/5 | - | True | - | - | 5.2 |
| wf2_retry | feature/edge-coverage | needs-change | 0/5 | 3/5 | - | False | - | - | 17.9 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 0.2 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 0.2 |
| wf5_partial | implement/edge-coverage | resolved | 0/7 | 7/7 | - | True | - | - | 8.9 |
| wf6_multi | migration/multi-concern | escalate | 2/6 | 2/6 | DOCSCORE=0/4 TODOSCORE=0/3 | False | - | - | 113.2 |

**objective pass 24/30 - regressions 0 - check crashes 0 - decline accuracy 5/5**

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 6 | 0.97 |
| backward-compat | 4 | 0.90 |
| combined-score | 2 | 0.67 |
| concern-split | 2 | 0.67 |
| cross-file | 3 | 0.92 |
| edge-coverage | 8 | 0.93 |
| greenfield-impl | 2 | 0.80 |
| kway-synth | 2 | 1.00 |
| partial-credit | 3 | 1.00 |
| premise-audit | 7 | 0.96 |
| regression-guard | 9 | 0.96 |
| silent-failure | 4 | 1.00 |
