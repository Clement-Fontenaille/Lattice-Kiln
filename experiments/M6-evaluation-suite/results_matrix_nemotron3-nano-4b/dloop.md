# M6 suite run - arm `dloop` (suite 0.4.1)

_2026-09-25 18:38 - 34 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 0.2 |
| hf_audit_perf | perf/harmful-fix | resolved | 2/2 | 2/2 | PERFSCORE=1/1 AUDITSCORE=1/1 | True | - | - | 20.4 |
| hf_cache_decorator | feature/edge-coverage | escalate | 3/4 | 3/4 | - | False | - | - | 121.9 |
| hf_cache_nondeterministic | perf/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 0.3 |
| hf_counter_race | concurrency/silent-failure | resolved | 2/3 | 3/3 | - | True | - | - | 17.0 |
| hf_csv | data/edge-coverage | needs-change | 3/6 | 5/6 | - | False | - | - | 51.8 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 0.2 |
| hf_deprecate | compat/backward-compat | resolved | 1/4 | 4/4 | - | True | - | - | 16.8 |
| hf_dict_dispatch | refactor/behaviour-preserving | escalate | 7/7 | 7/7 | STRUCTSCORE=0/3 | False | - | - | 167.4 |
| hf_extract_fn | refactor/behaviour-preserving | resolved | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 26.9 |
| hf_json_field | feature/backward-compat | resolved | 2/5 | 5/5 | - | True | - | - | 28.6 |
| hf_json_serialize | feature/multi-concern | escalate | 2/5 | 2/5 | STRUCTSCORE=0/2 | False | - | - | 44.1 |
| hf_merge_config | data/edge-coverage | needs-change | 3/6 | 5/6 | - | False | - | - | 71.8 |
| hf_misfiled_bug | fix/misdirection | escalate | 3/4 | 3/4 | - | False | - | - | 36.6 |
| hf_multi_recipient | compat/backward-compat | resolved | 3/5 | 5/5 | - | True | - | - | 13.5 |
| hf_pagination | fix/edge-coverage | resolved | 1/5 | 5/5 | - | True | - | - | 14.7 |
| hf_path_sanitize | robustness/edge-coverage | error:OllamaError('request to http://localhost:11434 failed: HTTP 500: {"error":"XML syntax error on line 36: element \\ | 1/8 | 1/8 | - | None | - | - | 21.0 |
| hf_rec_to_iter | refactor/behaviour-preserving | resolved | 4/5 | 5/5 | STRUCTSCORE=1/1 | True | - | - | 33.5 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 0.2 |
| hf_rename | compat/behaviour-preserving | resolved | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 42.9 |
| hf_retry_backoff | robustness/silent-failure | resolved | 2/4 | 4/4 | - | True | - | - | 48.8 |
| hf_return_shape | compat/backward-compat | resolved | 3/5 | 5/5 | - | True | - | - | 30.1 |
| hf_suppress | robustness/silent-failure | resolved | 3/4 | 4/4 | - | True | - | - | 15.5 |
| hf_timeout_param | feature/edge-coverage | escalate | 2/6 | 2/6 | - | False | - | - | 64.0 |
| hf_validate_withdraw | robustness/silent-failure | resolved | 4/6 | 6/6 | - | True | - | - | 17.8 |
| hf_wrong_spec | fix/faulty-check | escalate | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 12.9 |
| wf1_crossfile | fix/misdirection | resolved | 2/5 | 5/5 | - | True | - | - | 13.8 |
| wf2_retry | feature/edge-coverage | needs-change | 0/5 | 3/5 | - | False | - | - | 166.9 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 0.2 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 0.3 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | resolved | 5/5 | 5/5 | STRUCTSCORE=3/3 | True | - | - | 17.5 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 0.2 |
| wf5_partial | implement/edge-coverage | needs-change | 0/7 | 1/7 | - | False | - | - | 109.0 |
| wf6_multi | migration/multi-concern | needs-change | 2/6 | 6/6 | DOCSCORE=1/4 TODOSCORE=3/3 | False | - | - | 91.8 |

**objective pass 21/33 - regressions 0 - check crashes 0 - decline accuracy 5/6**

> **1 of 34 runs did not execute** (the arm raised; `run_ok: false`). They are excluded from every figure above. See `error_trace` in the JSON.

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 9 | 1.00 |
| backward-compat | 4 | 1.00 |
| combined-score | 2 | 0.70 |
| concern-split | 2 | 0.70 |
| cross-file | 3 | 0.92 |
| decline-taxonomy | 2 | 0.83 |
| edge-coverage | 7 | 0.76 |
| greenfield-impl | 2 | 0.37 |
| keeper-set-rule | 1 | 1.00 |
| kway-synth | 2 | 0.49 |
| partial-credit | 2 | 0.49 |
| premise-audit | 8 | 0.93 |
| regression-guard | 9 | 1.00 |
| silent-failure | 4 | 1.00 |
| witness-pair | 2 | 1.00 |
