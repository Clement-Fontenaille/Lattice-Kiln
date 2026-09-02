# Super-pipeline v2 results

_2026-09-02 11:21 - 12 runs_

| task | rep | terminal | base | final | pass | regr | decline_exp | calls | wall | load-bearing |
|---|---|---|---|---|---|---|---|---|---|---|
| wf1_crossfile | 1 | needs-change | 2 | 5/5 | True | False | False | 22 | 105.8 | l2_violated |
| wf1_crossfile | 2 | resolved | 2 | 5/5 | True | False | False | 17 | 92.2 |  |
| wf2_retry | 1 | needs-change | 0 | 0/5 | False | False | False | 16 | 74.2 |  |
| wf2_retry | 2 | needs-change | 0 | 0/5 | False | False | False | 16 | 69.7 |  |
| wf3_refactor | 1 | escalate | 5 | 5/5 | True | False | False | 17 | 68.3 |  |
| wf3_refactor | 2 | escalate | 5 | 5/5 | True | False | False | 12 | 58.9 |  |
| wf4_assumption | 1 | declined | 5 | 5/5 | True | False | True | 3 | 9.0 | premise_unsound |
| wf4_assumption | 2 | declined | 5 | 5/5 | True | False | True | 3 | 9.0 | premise_unsound |
| wf5_partial | 1 | needs-change | 0 | 0/7 | False | False | False | 16 | 82.8 |  |
| wf5_partial | 2 | needs-change | 0 | 5/7 | False | False | False | 16 | 89.8 | l1_provided_fail |
| wf6_multi | 1 | needs-change | 2 | 6/6 | True | False | False | 28 | 247.8 | l2_violated |
| wf6_multi | 2 | resolved | 2 | 6/6 | True | False | False | 29 | 222.6 |  |

### wf6_multi detail
| rep | terminal | algo | doc | todo | winner | calls |
|---|---|---|---|---|---|---|
| 1 | needs-change | 6/6 | (3, 4) | (2, 3) | b | 28 |
| 2 | resolved | 6/6 | (4, 4) | (3, 3) | a | 29 |

## per-stage cost (mean)

| stage | calls | wall | runs |
|---|---|---|---|
| S0-premise | 3.0 | 8.9s | 12 |
| S1-testspec | 1.0 | 7.5s | 10 |
| S2-implspec | 2.0 | 8.9s | 10 |
| S3-alignment | 1.0 | 3.0s | 10 |
| S4-synth | 3.0 | 29.4s | 10 |
| S5-coding | 3.7 | 35.4s | 10 |
| S6b-l2 | 5.2 | 17.8s | 10 |

## terminals

- needs-change: 6
- resolved: 2
- escalate: 2
- declined: 2

**regressions: 0/12**

## stage load-bearing frequency (how often each signal decided the terminal)

- l2_violated: 2
- premise_unsound: 2
- l1_provided_fail: 1
