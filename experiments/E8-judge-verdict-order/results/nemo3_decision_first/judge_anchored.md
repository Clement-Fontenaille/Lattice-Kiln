# M6 suite run - arm `judge_anchored` (suite 0.4.1)

_2026-09-22 13:20 - 8 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_path_sanitize | robustness/edge-coverage | blocked-no-progress | 1/8 | 1/8 | - | False | - | - | 118.5 |
| hf_path_sanitize | robustness/edge-coverage | blocked-no-progress | 1/8 | 1/8 | - | False | - | - | 56.8 |
| hf_path_sanitize | robustness/edge-coverage | error:OllamaError('request to http://127.0.0.1:11435 failed: HTTP Error 500: Internal Server Error') | 1/8 | 1/8 | - | None | - | - | 74.2 |
| hf_path_sanitize | robustness/edge-coverage | blocked-no-progress | 1/8 | 1/8 | - | False | - | - | 81.8 |
| hf_path_sanitize | robustness/edge-coverage | blocked-no-progress | 1/8 | 1/8 | - | False | - | - | 166.3 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 185.7 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 135.7 |
| wf3_refactor_blindview | refactor/behaviour-preserving | declined | 5/5 | 5/5 | STRUCTSCORE=0/3 | False | - | - | 163.8 |

**objective pass 0/7 - regressions 0 - check crashes 0 - decline accuracy 0/0**

> **1 of 8 runs did not execute** (the arm raised; `run_ok: false`). They are excluded from every figure above. See `error_trace` in the JSON.

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 3 | 1.00 |
| edge-coverage | 4 | 0.12 |
| partial-credit | 4 | 0.12 |
| witness-pair | 3 | 1.00 |
