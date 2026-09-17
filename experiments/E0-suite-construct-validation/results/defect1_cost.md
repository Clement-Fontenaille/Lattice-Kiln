# E0 Part 2 — what defect 1 costs

Generated 2026-09-17T11:17:27.829528+00:00.

`gated` = `objective_pass` as published. `folded` = also requires every
structural dimension in `struct` to be at full marks.

| arm | rows with struct | gated | folded | flipped |
|---|---|---|---|---|
| baseline | 10 | 2 (0.2) | 0 (0.0) | 2 |
| dloop | 30 | 21 (0.7) | 8 (0.267) | 13 |
| judge_anchored | 50 | 33 (0.66) | 17 (0.34) | 16 |
| judge_bypass | 22 | 14 (0.636) | 11 (0.5) | 3 |
| judge_caveat | 30 | 24 (0.8) | 13 (0.433) | 11 |
| judge_fullctx | 50 | 31 (0.62) | 21 (0.42) | 10 |
| judge_staged | 30 | 20 (0.667) | 14 (0.467) | 6 |
| m7 | 30 | 23 (0.767) | 10 (0.333) | 13 |
| m7b | 36 | 25 (0.694) | 12 (0.333) | 13 |
| m7c | 8 | 6 (0.75) | 3 (0.375) | 3 |
| m7e | 30 | 18 (0.6) | 10 (0.333) | 8 |
| m7f | 50 | 33 (0.66) | 19 (0.38) | 14 |
| monolith | 22 | 10 (0.455) | 8 (0.364) | 2 |
| n5_dloop | 30 | 21 (0.7) | 8 (0.267) | 13 |
| n5_m7 | 30 | 23 (0.767) | 10 (0.333) | 13 |
| staged | 30 | 15 (0.5) | 8 (0.267) | 7 |
| test_synth | 50 | 34 (0.68) | 23 (0.46) | 11 |
| test_synth_retry | 42 | 28 (0.667) | 16 (0.381) | 12 |

## Does folding change arm ORDERING?

- gated order: judge_caveat > m7 > n5_m7 > m7c > dloop > n5_dloop > m7b > test_synth > judge_staged > test_synth_retry > judge_anchored > m7f > judge_bypass > judge_fullctx > m7e > staged > monolith > baseline
- folded order: judge_bypass > judge_staged > test_synth > judge_caveat > judge_fullctx > test_synth_retry > m7f > m7c > monolith > judge_anchored > m7 > m7b > m7e > n5_m7 > dloop > n5_dloop > staged > baseline
- **ordering changes: True**

## Tasks accounting for the disagreements

| task | rows flipped |
|---|---|
| hf_dict_dispatch | 64 |
| hf_extract_fn | 57 |
| hf_json_serialize | 27 |
| wf6_multi | 22 |

## Coverage limit

`struct` is populated on a minority of tasks per arm, so the folded score is
computed on part of the suite and is **not** a corrected headline number.
It is a sensitivity estimate.
