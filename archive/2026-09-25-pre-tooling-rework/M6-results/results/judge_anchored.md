# M6 suite run - arm `judge_anchored` (suite 0.4.1)

_2026-09-23 23:26 - 10 runs_

| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |
|---|---|---|---|---|---|---|---|---|---|
| wf2_retry | feature/edge-coverage | error:OllamaError('empty response and no tool calls, truncated at num_predict=8192 (done_reason=length, 32043 chars of t | 0/5 | 3/5 | - | None | - | - | 213.0 |
| wf2_retry | feature/edge-coverage | error:OllamaError('empty response and no tool calls, truncated at num_predict=8192 (done_reason=length, 26457 chars of t | 0/5 | 3/5 | - | None | - | - | 393.9 |
| wf2_retry | feature/edge-coverage | answered | 0/5 | 5/5 | - | True | - | - | 284.7 |
| wf2_retry | feature/edge-coverage | error:OllamaError('empty response and no tool calls, truncated at num_predict=8192 (done_reason=length, 26393 chars of t | 0/5 | 3/5 | - | None | - | - | 700.9 |
| wf2_retry | feature/edge-coverage | answered | 0/5 | 5/5 | - | True | - | - | 645.7 |
| wf2_retry | feature/edge-coverage | answered | 0/5 | 5/5 | - | True | - | - | 445.6 |
| wf2_retry | feature/edge-coverage | answered | 0/5 | 5/5 | - | True | - | - | 230.2 |
| wf2_retry | feature/edge-coverage | answered | 0/5 | 5/5 | - | True | - | - | 289.5 |
| wf2_retry | feature/edge-coverage | error:OllamaError('empty response and no tool calls, truncated at num_predict=8192 (done_reason=length, 25148 chars of t | 0/5 | 3/5 | - | None | - | - | 125.1 |
| wf2_retry | feature/edge-coverage | answered | 0/5 | 5/5 | - | True | - | - | 40.4 |

**objective pass 6/6 - regressions 0 - check crashes 0 - decline accuracy 0/0**

> **4 of 10 runs did not execute** (the arm raised; `run_ok: false`). They are excluded from every figure above. See `error_trace` in the JSON.

## `stresses` slices (mean final SUBTESTS fraction)

| capability | n | mean |
|---|---|---|
| edge-coverage | 6 | 1.00 |
| greenfield-impl | 6 | 1.00 |
