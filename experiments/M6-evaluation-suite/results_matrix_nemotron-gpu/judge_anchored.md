# M6 suite run - arm `judge_anchored` (suite 0.4.1)

_2026-09-27 02:05 - 15 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_already_optimal | perf/false-premise | declined | 6/6 | 6/6 | - | True | - | ok | 767.7 |
| hf_dead_code | cleanup/false-premise | declined | 4/4 | 4/4 | - | True | - | ok | 90.1 |
| hf_dict_dispatch | refactor/behaviour-preserving | blocked-no-progress | 7/7 | 7/7 | STRUCTSCORE=0/3 | False | - | - | 752.4 |
| hf_extract_fn | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=1/3 | False | - | - | 712.1 |
| hf_rec_to_iter | refactor/behaviour-preserving | blocked-no-progress | 4/5 | 4/5 | STRUCTSCORE=0/1 | False | - | - | 653.4 |
| hf_remove_validation | cleanup/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 213.8 |
| hf_rename | compat/behaviour-preserving | answered | 4/6 | 6/6 | STRUCTSCORE=3/3 | True | - | - | 1119.6 |
| wf1_crossfile | fix/misdirection | blocked-no-progress | 2/5 | 2/5 | - | False | - | - | 636.8 |
| wf2_retry | feature/edge-coverage | blocked-no-progress | 0/5 | 0/5 | - | False | - | - | 1101.5 |
| wf3_refactor | refactor/behaviour-preserving | declined | 5/5 | 5/5 | - | True | - | - | 675.0 |
| wf3_refactor_blindview | refactor/behaviour-preserving | error:OllamaError('request to http://localhost:11434 failed: HTTP 500: {"error":"prediction aborted, token repeat limit  | 5/5 | 5/5 | STRUCTSCORE=0/3 | None | - | - | 325.0 |
| wf3_refactor_witnessed | refactor/behaviour-preserving | blocked-no-progress | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 764.4 |
| wf4_assumption | perf/false-premise | declined | 5/5 | 5/5 | - | True | - | ok | 81.2 |
| wf5_partial | implement/edge-coverage | blocked-no-progress | 0/7 | 0/7 | - | False | - | - | 670.5 |
| wf6_multi | migration/multi-concern | blocked-partial | 2/6 | 6/6 | DOCSCORE=3/4 TODOSCORE=3/3 | False | - | - | 1051.0 |

**objective pass 6/14 - regressions 0 - check crashes 0 - decline accuracy 4/4**

> **1 of 15 runs did not execute** (the arm raised; `run_ok: false`). They are excluded from every figure above. See `error_trace` in the JSON.

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 6 | 0.97 |
| combined-score | 1 | 1.00 |
| concern-split | 1 | 1.00 |
| cross-file | 2 | 0.70 |
| edge-coverage | 1 | 0.00 |
| greenfield-impl | 2 | 0.00 |
| kway-synth | 1 | 0.00 |
| partial-credit | 1 | 0.00 |
| premise-audit | 5 | 0.88 |
| regression-guard | 4 | 1.00 |
| witness-pair | 1 | 1.00 |
