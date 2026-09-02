# Super-pipeline v2 results

_2026-09-02 11:02 - 1 runs_

| task | rep | terminal | base | final | pass | regr | decline_exp | calls | wall | load-bearing |
|---|---|---|---|---|---|---|---|---|---|---|
| wf6_multi | 1 | resolved | 2 | 6/6 | True | False | False | 27 | 147.8 |  |

### wf6_multi detail
| rep | terminal | algo | doc | todo | winner | calls |
|---|---|---|---|---|---|---|
| 1 | resolved | 6/6 | (3, 4) | (2, 3) | b | 27 |

## per-stage cost (mean)

| stage | calls | wall | runs |
|---|---|---|---|
| S0-premise | 3.0 | 9.1s | 1 |
| S1-testspec | 1.0 | 6.3s | 1 |
| S2-implspec | 2.0 | 11.8s | 1 |
| S3-alignment | 1.0 | 3.1s | 1 |
| S4-synth | 3.0 | 33.1s | 1 |
| S5-coding | 12.0 | 63.7s | 1 |
| S6b-l2 | 5.0 | 19.6s | 1 |

## terminals

- resolved: 1

**regressions: 0/1**

## stage load-bearing frequency (how often each signal decided the terminal)

