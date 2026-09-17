# E0 Part 3 — item analysis

Generated 2026-09-17T11:17:27.829528+00:00.

## What these numbers can and cannot mean

The "subjects" here are **scaffolds on one model**, not models of differing
ability. Classical item analysis assumes subjects spanning an ability range.
An item-total correlation computed over pipelines answers *"does this item
separate pipelines"*, which is related to but not the same as *"does this item
measure the construct"*. E4 is the experiment that would supply real ability
spread; until it runs, every number here is about pipeline discrimination.

## Response matrix — excluding baseline

- items (tasks): **34**
- attempts (arm x rep, fully observed): **41**

### Difficulty distribution

- at the **floor** (no attempt passes, zero variance): 2 — hf_misfiled_bug, hf_wrong_spec
- at the **ceiling** (every attempt passes, zero variance): 9 — hf_already_optimal, hf_cache_nondeterministic, hf_counter_race, hf_dead_code, hf_remove_validation, hf_retry_backoff, hf_validate_withdraw, wf1_crossfile, wf3_refactor
- **discriminating items** (0 < p < 1): 23

### Item-total correlation

Items with correlation <= 0 — where *better* attempts do *worse*. The classic broken-check signal.

| task | r |
|---|---|
| wf3_refactor_blindview | -0.497 |
| hf_deprecate | -0.463 |
| wf2_retry | -0.288 |
| hf_return_shape | -0.144 |
| wf6_multi | -0.092 |
| hf_rename | -0.084 |
| wf5_partial | -0.009 |

### Dimensionality (parallel analysis, 95th percentile)

- items with variance used: **23**
- **factors retained: 2**

| # | observed | random p95 |
|---|---|---|
| 1 | 5.827 | 3.051 |
| 2 | 4.12 | 2.528 |
| 3 | 1.885 | 2.22 |
| 4 | 1.753 | 1.969 |
| 5 | 1.593 | 1.802 |
| 6 | 1.487 | 1.63 |
| 7 | 0.967 | 1.469 |
| 8 | 0.914 | 1.33 |
| 9 | 0.869 | 1.204 |
| 10 | 0.74 | 1.1 |

## Response matrix — with baseline

- items (tasks): **34**
- attempts (arm x rep, fully observed): **42**

### Difficulty distribution

- at the **floor** (no attempt passes, zero variance): 2 — hf_misfiled_bug, hf_wrong_spec
- at the **ceiling** (every attempt passes, zero variance): 5 — hf_already_optimal, hf_cache_nondeterministic, hf_dead_code, hf_remove_validation, wf3_refactor
- **discriminating items** (0 < p < 1): 27

### Item-total correlation

Items with correlation <= 0 — where *better* attempts do *worse*. The classic broken-check signal.

| task | r |
|---|---|
| wf3_refactor_blindview | -0.309 |
| hf_deprecate | -0.26 |
| wf2_retry | -0.144 |

### Dimensionality (parallel analysis, 95th percentile)

- items with variance used: **27**
- **factors retained: 3**

| # | observed | random p95 |
|---|---|---|
| 1 | 8.168 | 3.119 |
| 2 | 4.01 | 2.655 |
| 3 | 3.375 | 2.362 |
| 4 | 1.689 | 2.126 |
| 5 | 1.65 | 1.946 |
| 6 | 1.414 | 1.764 |
| 7 | 1.264 | 1.607 |
| 8 | 0.88 | 1.474 |
| 9 | 0.851 | 1.354 |
| 10 | 0.657 | 1.243 |

