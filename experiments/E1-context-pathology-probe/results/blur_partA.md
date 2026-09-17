# E1 Part A — the anecdote, checked

Generated 2026-09-17T11:20:33.459064+00:00.

Source: `experiments\M5-intelligent-orchestration\pipeline_lab\results\results.json` (M5 pipeline_lab, 6 wf tasks x 2 reps).

| task | rep | core | doc | todo | low | objective_pass | pattern |
|---|---|---|---|---|---|---|---|
| wf1_crossfile | 1 | 1.0 | None | None | None | True | incomplete |
| wf1_crossfile | 2 | 1.0 | None | None | None | True | incomplete |
| wf2_retry | 1 | 0.0 | None | None | None | False | incomplete |
| wf2_retry | 2 | 0.0 | None | None | None | False | incomplete |
| wf3_refactor | 1 | 1.0 | None | None | None | True | incomplete |
| wf3_refactor | 2 | 1.0 | None | None | None | True | incomplete |
| wf4_assumption | 1 | 1.0 | None | None | None | True | incomplete |
| wf4_assumption | 2 | 1.0 | None | None | None | True | incomplete |
| wf5_partial | 1 | 0.0 | None | None | None | False | incomplete |
| wf5_partial | 2 | 0.714 | None | None | None | False | incomplete |
| wf6_multi | 1 | 1.0 | [3, 4] | [2, 3] | 0.708 | True | mixed |
| wf6_multi | 2 | 1.0 | [4, 4] | [3, 3] | 1.0 | True | both_hold |

## Does the anecdote reproduce here?

**No — not in this file.** In the pipeline_lab arm `wf6_multi` scores doc [3, 4]/[4, 4] and todo [2, 3]/[3, 3] — well, not dropped. The 0/4, 0/3 figure belongs to a different arm; see Part B.

Only `wf6_multi` carries doc/todo dimensions at all in this file. The other five `wf*` tasks have `doc: null, todo: null`, so **the direction cannot be compared across tasks here** — there is nothing to compare against.
