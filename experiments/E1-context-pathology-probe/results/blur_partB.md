# E1 Part B — does it hold across the M6 corpus?

Generated 2026-09-17T11:20:33.459064+00:00.

Rows are M6 results carrying a low-salience dimension (`DOCSCORE`/`TODOSCORE`).
**Tasks carrying any such dimension: 1 — wf6_multi**

Rows analysed: **69** across 18 arms.

## Pattern distribution

`blur` = core >= 0.8 and low < 0.5 (the claim). `both_drop` = both below threshold (ordinary global failure, NOT the claim). `inverse` = periphery holds while core drops.

| pattern | rows | share |
|---|---|---|
| both_drop | 36 | 52.2% |
| mixed | 19 | 27.5% |
| blur | 10 | 14.5% |
| both_hold | 4 | 5.8% |

## The motivating anecdote, located

- `monolith` rep1: {'DOCSCORE': [0, 4], 'TODOSCORE': [0, 3]}, core `final_sub` = 0.333, objective_pass = False → **both_drop**
- `monolith` rep2: {'DOCSCORE': [0, 4], 'TODOSCORE': [0, 3]}, core `final_sub` = 0.333, objective_pass = False → **both_drop**
- `monolith` rep3: {'DOCSCORE': [0, 4], 'TODOSCORE': [0, 3]}, core `final_sub` = 0.333, objective_pass = False → **both_drop**

The 0/4 and 0/3 figures reproduce exactly. **What does not reproduce is the reading**: the core did not hold. `final_sub` is 2/6 and `objective_pass` is False in every monolith rep. That is `both_drop` — global failure — not selective omission.

## Per-arm pattern counts

| arm | rows | blur | both_drop | both_hold | inverse | mixed |
|---|---|---|---|---|---|---|
| baseline | 1 | 0 | 1 | 0 | 0 | 0 |
| dloop | 5 | 0 | 5 | 0 | 0 | 0 |
| judge_anchored | 5 | 2 | 1 | 0 | 0 | 2 |
| judge_bypass | 2 | 1 | 1 | 0 | 0 | 0 |
| judge_caveat | 3 | 1 | 0 | 0 | 0 | 2 |
| judge_fullctx | 5 | 0 | 3 | 0 | 0 | 2 |
| judge_staged | 3 | 0 | 1 | 1 | 0 | 1 |
| m7 | 5 | 1 | 3 | 0 | 0 | 1 |
| m7b | 5 | 1 | 1 | 1 | 0 | 2 |
| m7c | 1 | 0 | 0 | 0 | 0 | 1 |
| m7e | 3 | 1 | 2 | 0 | 0 | 0 |
| m7f | 5 | 1 | 3 | 1 | 0 | 0 |
| monolith | 3 | 0 | 3 | 0 | 0 | 0 |
| n5_dloop | 5 | 0 | 5 | 0 | 0 | 0 |
| n5_m7 | 5 | 1 | 3 | 0 | 0 | 1 |
| staged | 3 | 0 | 1 | 0 | 0 | 2 |
| test_synth | 5 | 0 | 2 | 0 | 0 | 3 |
| test_synth_retry | 5 | 1 | 1 | 1 | 0 | 2 |

## Load proxies vs the core-minus-low gap

Correlation of `gap` with each proxy, reported separately (never averaged into one index, which would hide disagreement).

| proxy | n | correlation with gap |
|---|---|---|
| L1 requirement count | 69 | no variance |
| L3 context budget | 69 | -0.076 |
| L2 worker view | 69 | {'full': 47, None: 22} |

## Reading, against the rule fixed in the protocol

- `blur` rows: **10 (14.5%)**
- `both_drop` rows: **36 (52.2%)**
- `inverse` rows: **0**

## Limitations, required by the protocol

1. Only **1 tasks** in the whole 34-task suite carry a low-salience dimension. Everything above describes those tasks, not the suite.
2. **No controlled load axis exists.** L1 confounds 'more to do' with 'more to hold'; L3 confounds context budget with scaffold generation. This is observational.
3. L2 (worker view) has no variance in these rows and is not computable.
4. Arms differ in scaffold, not in load, so any correlation is between scaffold-associated quantities, not a dose-response.
