# Loop-lab results (bundle D)

_2026-09-01 00:51 - 36 runs, MAX_ROUNDS=3, STALL_TOL=1_

- **oneshot**: obj pass 6/12, subtests 48/60 (80%), **1 regressions vs baseline**, 12 calls, mean wall 11.8s
- **naive_loop**: obj pass 10/12, subtests 54/54 (100%), **2 regressions vs baseline**, 48 calls, mean wall 24.6s
- **d_loop**: obj pass 9/12, subtests 56/66 (85%), **0 regressions vs baseline**, 14 calls, mean wall 17.6s

| task | arm | rep | base | final | pass | regressed | rounds | calls | terminal | best_src | kept_best | wall |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| wf1_crossfile | d_loop | 1 | 2 | 5/5 | True | False | 1 | 1 | resolved | round0 | False | 4.5 |
| wf1_crossfile | d_loop | 2 | 2 | 5/5 | True | False | 1 | 1 | resolved | round0 | False | 4.3 |
| wf1_crossfile | naive_loop | 1 | 2 | 5/5 | True | False | 1 | 2 | reviewer-approved | last | False | 8.4 |
| wf1_crossfile | naive_loop | 2 | 2 | 5/5 | True | False | 1 | 2 | reviewer-approved | last | False | 8.3 |
| wf1_crossfile | oneshot | 1 | 2 | 5/5 | True | False | 1 | 1 | done | round0 | False | 4.9 |
| wf1_crossfile | oneshot | 2 | 2 | 5/5 | True | False | 1 | 1 | done | round0 | False | 4.0 |
| wf2_retry | d_loop | 1 | 0 | 5/5 | True | False | 2 | 2 | resolved | round1 | False | 11.3 |
| wf2_retry | d_loop | 2 | 0 | 5/5 | True | False | 2 | 2 | resolved | round1 | False | 10.5 |
| wf2_retry | naive_loop | 1 | 0 | 5/5 | True | False | 2 | 4 | reviewer-approved | last | False | 20.2 |
| wf2_retry | naive_loop | 2 | 0 | 5/5 | True | False | 2 | 4 | reviewer-approved | last | False | 18.1 |
| wf2_retry | oneshot | 1 | 0 | 3/5 | False | False | 1 | 1 | done | round0 | False | 5.5 |
| wf2_retry | oneshot | 2 | 0 | 3/5 | False | False | 1 | 1 | done | round0 | False | 4.7 |
| wf3_refactor | d_loop | 1 | 5 | 5/5 | True | False | 0 | 0 | resolved | incumbent | False | 0.3 |
| wf3_refactor | d_loop | 2 | 5 | 5/5 | True | False | 0 | 0 | resolved | incumbent | False | 0.2 |
| wf3_refactor | naive_loop | 1 | 5 | 5/5 | True | False | 4 | 7 | exhausted | last | False | 30.8 |
| wf3_refactor | naive_loop | 2 | 5 | 5/5 | True | False | 1 | 2 | reviewer-approved | last | False | 8.6 |
| wf3_refactor | oneshot | 1 | 5 | 5/5 | True | False | 1 | 1 | done | round0 | False | 5.2 |
| wf3_refactor | oneshot | 2 | 5 | 5/5 | True | False | 1 | 1 | done | round0 | False | 4.7 |
| wf4_assumption | d_loop | 1 | 5 | 5/5 | True | False | 0 | 0 | resolved | incumbent | False | 0.2 |
| wf4_assumption | d_loop | 2 | 5 | 5/5 | True | False | 0 | 0 | resolved | incumbent | False | 0.2 |
| wf4_assumption | naive_loop | 1 | 5 | 5/5 | True | False | 2 | 4 | reviewer-approved | last | False | 19.1 |
| wf4_assumption | naive_loop | 2 | 5 | 5/5 | True | False | 3 | 6 | reviewer-approved | last | False | 23.3 |
| wf4_assumption | oneshot | 1 | 5 | 5/5 | True | False | 1 | 1 | done | round0 | False | 4.1 |
| wf4_assumption | oneshot | 2 | 5 | 5/5 | True | False | 1 | 1 | done | round0 | False | 3.7 |
| wf5_partial | d_loop | 1 | 0 | 5/7 | False | False | 3 | 3 | stalled | round0 | False | 20.6 |
| wf5_partial | d_loop | 2 | 0 | 7/7 | True | False | 1 | 1 | resolved | round0 | False | 7.8 |
| wf5_partial | naive_loop | 1 | 0 | 7/7 | True | False | 1 | 2 | reviewer-approved | last | False | 11.6 |
| wf5_partial | naive_loop | 2 | 0 | 7/7 | True | False | 1 | 2 | reviewer-approved | last | False | 11.4 |
| wf5_partial | oneshot | 1 | 0 | 5/7 | False | False | 1 | 1 | done | round0 | False | 7.3 |
| wf5_partial | oneshot | 2 | 0 | 5/7 | False | False | 1 | 1 | done | round0 | False | 6.4 |
| wf6_multi | d_loop | 1 | 2 | 2/6 | False | False | 2 | 2 | no-improvement | incumbent | True | 76.1 |
| wf6_multi | d_loop | 2 | 2 | 2/6 | False | False | 2 | 2 | no-improvement | incumbent | True | 75.6 |
| wf6_multi | naive_loop | 1 | 2 | 0/0 | False | True | 3 | 6 | reviewer-approved | last | False | 91.9 |
| wf6_multi | naive_loop | 2 | 2 | 0/0 | False | True | 4 | 7 | exhausted | last | False | 43.5 |
| wf6_multi | oneshot | 1 | 2 | 2/6 | False | False | 1 | 1 | done | round0 | False | 54.9 |
| wf6_multi | oneshot | 2 | 2 | 0/0 | False | True | 1 | 1 | done | round0 | False | 36.3 |

## per task (mean final subtests)

| task | oneshot | naive_loop | d_loop | d regressions |
|---|---|---|---|---|
| wf1_crossfile (/5) | 5.0 | 5.0 | 5.0 | 0 |
| wf2_retry (/5) | 3.0 | 5.0 | 5.0 | 0 |
| wf3_refactor (/5) | 5.0 | 5.0 | 5.0 | 0 |
| wf4_assumption (/5) | 5.0 | 5.0 | 5.0 | 0 |
| wf5_partial (/7) | 5.0 | 7.0 | 6.0 | 0 |
| wf6_multi (/6) | 1.0 | 0.0 | 2.0 | 0 |
