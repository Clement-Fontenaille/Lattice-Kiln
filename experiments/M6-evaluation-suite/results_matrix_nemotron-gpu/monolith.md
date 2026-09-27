# M6 suite run - arm `monolith` (suite 0.4.1)

_2026-09-26 21:42 - 8 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| hf_audit_perf | perf/harmful-fix | done | 2/2 | 2/2 | PERFSCORE=0/1 AUDITSCORE=1/1 | False | - | - | 56.4 |
| hf_counter_race | concurrency/silent-failure | done | 2/3 | 0/1 | - | False | YES | - | 65.3 |
| hf_json_serialize | feature/multi-concern | done | 2/5 | 2/5 | STRUCTSCORE=0/2 | False | - | - | 188.8 |
| hf_pagination | fix/edge-coverage | done | 1/5 | 1/5 | - | False | - | - | 130.2 |
| hf_retry_backoff | robustness/silent-failure | done | 2/4 | 2/4 | - | False | - | - | 196.5 |
| hf_suppress | robustness/silent-failure | done | 3/4 | 3/4 | - | False | - | - | 75.6 |
| hf_validate_withdraw | robustness/silent-failure | error:OllamaError('request to http://localhost:11434 failed: HTTP 500: {"error":"XML syntax error on line 5: element \\u | 4/6 | 4/6 | - | None | - | - | 68.5 |
| hf_wrong_spec | fix/faulty-check | done | 2/3 | 2/3 | SPECSCORE=4/4 | False | - | MISS | 10.7 |

**objective pass 0/7 - regressions 1 - check crashes 1 - decline accuracy 0/1**

> **1 of 8 runs did not execute** (the arm raised; `run_ok: false`). They are excluded from every figure above. See `error_trace` in the JSON.

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| L2-structural | 1 | 1.00 |
| combined-score | 1 | 0.40 |
| concern-split | 1 | 0.40 |
| decline-taxonomy | 2 | 0.83 |
| edge-coverage | 2 | 0.35 |
| keeper-set-rule | 1 | 1.00 |
| premise-audit | 1 | 0.67 |
| regression-guard | 1 | 0.75 |
| silent-failure | 3 | 0.42 |
