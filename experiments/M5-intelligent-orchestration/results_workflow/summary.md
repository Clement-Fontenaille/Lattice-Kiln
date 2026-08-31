# M5 workflow-suite results

_2026-08-31 02:36 - 54 runs_

- **monolith**: objective pass 10/18, subtests 67/87 (77%), 18 calls, mean wall 11.7s
- **fixed**: objective pass 11/18, subtests 76/87 (87%), 83 calls, mean wall 39.3s
- **orchestrated**: objective pass 12/18, subtests 77/93 (83%), 129 calls, mean wall 54.1s

| task | kind | arm | rep | obj_pass | subtests | declined | calls | wall_s |
|---|---|---|---|---|---|---|---|---|
| wf1_crossfile | cross_file_bug | fixed | 1 | True | 5/5 | False | 3 | 15.0 |
| wf1_crossfile | cross_file_bug | fixed | 2 | True | 5/5 | False | 3 | 12.8 |
| wf1_crossfile | cross_file_bug | fixed | 3 | True | 5/5 | False | 4 | 24.3 |
| wf1_crossfile | cross_file_bug | monolith | 1 | False | 2/5 | False | 1 | 4.6 |
| wf1_crossfile | cross_file_bug | monolith | 2 | True | 5/5 | False | 1 | 4.3 |
| wf1_crossfile | cross_file_bug | monolith | 3 | False | 2/5 | False | 1 | 4.0 |
| wf1_crossfile | cross_file_bug | orchestrated | 1 | True | 5/5 | False | 7 | 27.5 |
| wf1_crossfile | cross_file_bug | orchestrated | 2 | True | 5/5 | False | 5 | 21.5 |
| wf1_crossfile | cross_file_bug | orchestrated | 3 | True | 5/5 | False | 5 | 19.0 |
| wf2_retry | feature_design_choice | fixed | 1 | False | 3/5 | False | 5 | 24.7 |
| wf2_retry | feature_design_choice | fixed | 2 | True | 5/5 | False | 5 | 25.4 |
| wf2_retry | feature_design_choice | fixed | 3 | False | 3/5 | False | 5 | 24.1 |
| wf2_retry | feature_design_choice | monolith | 1 | True | 5/5 | False | 1 | 5.7 |
| wf2_retry | feature_design_choice | monolith | 2 | False | 3/5 | False | 1 | 4.9 |
| wf2_retry | feature_design_choice | monolith | 3 | True | 5/5 | False | 1 | 4.9 |
| wf2_retry | feature_design_choice | orchestrated | 1 | False | 0/5 | False | 12 | 52.4 |
| wf2_retry | feature_design_choice | orchestrated | 2 | False | 0/5 | False | 12 | 51.0 |
| wf2_retry | feature_design_choice | orchestrated | 3 | True | 5/5 | False | 11 | 47.9 |
| wf3_refactor | refactor_trap | fixed | 1 | True | 5/5 | False | 3 | 14.9 |
| wf3_refactor | refactor_trap | fixed | 2 | True | 5/5 | False | 5 | 23.3 |
| wf3_refactor | refactor_trap | fixed | 3 | True | 5/5 | False | 8 | 37.2 |
| wf3_refactor | refactor_trap | monolith | 1 | True | 5/5 | False | 1 | 5.4 |
| wf3_refactor | refactor_trap | monolith | 2 | True | 5/5 | False | 1 | 4.8 |
| wf3_refactor | refactor_trap | monolith | 3 | True | 5/5 | False | 1 | 4.7 |
| wf3_refactor | refactor_trap | orchestrated | 1 | True | 5/5 | False | 5 | 20.7 |
| wf3_refactor | refactor_trap | orchestrated | 2 | True | 5/5 | False | 5 | 18.7 |
| wf3_refactor | refactor_trap | orchestrated | 3 | True | 5/5 | False | 7 | 31.2 |
| wf4_assumption | stale_assumption | fixed | 1 | True | 5/5 | True | 5 | 19.6 |
| wf4_assumption | stale_assumption | fixed | 2 | True | 5/5 | True | 5 | 19.5 |
| wf4_assumption | stale_assumption | fixed | 3 | True | 5/5 | True | 5 | 19.2 |
| wf4_assumption | stale_assumption | monolith | 1 | True | 5/5 | True | 1 | 4.5 |
| wf4_assumption | stale_assumption | monolith | 2 | True | 5/5 | True | 1 | 3.9 |
| wf4_assumption | stale_assumption | monolith | 3 | True | 5/5 | True | 1 | 3.8 |
| wf4_assumption | stale_assumption | orchestrated | 1 | True | 5/5 | False | 1 | 4.1 |
| wf4_assumption | stale_assumption | orchestrated | 2 | True | 5/5 | False | 1 | 2.7 |
| wf4_assumption | stale_assumption | orchestrated | 3 | True | 5/5 | False | 1 | 3.2 |
| wf5_partial | partial_credit | fixed | 1 | False | 4/7 | False | 8 | 51.4 |
| wf5_partial | partial_credit | fixed | 2 | False | 5/7 | False | 3 | 20.2 |
| wf5_partial | partial_credit | fixed | 3 | False | 5/7 | False | 3 | 22.9 |
| wf5_partial | partial_credit | monolith | 1 | False | 5/7 | False | 1 | 7.5 |
| wf5_partial | partial_credit | monolith | 2 | True | 7/7 | False | 1 | 7.3 |
| wf5_partial | partial_credit | monolith | 3 | False | 1/7 | False | 1 | 7.0 |
| wf5_partial | partial_credit | orchestrated | 1 | False | 5/7 | False | 7 | 32.3 |
| wf5_partial | partial_credit | orchestrated | 2 | False | 5/7 | False | 7 | 33.3 |
| wf5_partial | partial_credit | orchestrated | 3 | False | 5/7 | False | 7 | 34.8 |
| wf6_multi | multi_concern | fixed | 1 | False | 0/0 | False | 4 | 82.9 |
| wf6_multi | multi_concern | fixed | 2 | True | 6/6 | False | 3 | 53.7 |
| wf6_multi | multi_concern | fixed | 3 | False | 0/0 | False | 6 | 215.5 |
| wf6_multi | multi_concern | monolith | 1 | False | 0/0 | False | 1 | 38.8 |
| wf6_multi | multi_concern | monolith | 2 | False | 0/0 | False | 1 | 38.4 |
| wf6_multi | multi_concern | monolith | 3 | False | 2/6 | False | 1 | 56.1 |
| wf6_multi | multi_concern | orchestrated | 1 | False | 0/0 | False | 12 | 214.8 |
| wf6_multi | multi_concern | orchestrated | 2 | True | 6/6 | False | 12 | 170.4 |
| wf6_multi | multi_concern | orchestrated | 3 | True | 6/6 | False | 12 | 188.2 |

### wf6_multi secondary concerns (mean over reps)
| arm | algo subtests | doc score | todo score |
|---|---|---|---|
| monolith | 2.0/6 | 0.0/4 | 0.0/3 |
| fixed | 6.0/6 | 2.0/4 | 3.0/3 |
| orchestrated | 6.0/6 | 1.5/4 | 2.5/3 |

## Cost/benefit ledger (fixed vs monolith, mean over reps)

| task | mono subtests | fixed subtests | d subtests | mono calls | fixed calls | d calls | verdict |
|---|---|---|---|---|---|---|---|
| wf1_crossfile | 3.0/5 | 5.0/5 | +2.0 | 1 | 3 | +2.3 | fixed helps |
| wf2_retry | 4.3/5 | 3.7/5 | -0.7 | 1 | 5 | +4.0 | fixed worse |
| wf3_refactor | 5.0/5 | 5.0/5 | +0.0 | 1 | 5 | +4.3 | no gain |
| wf4_assumption | 5.0/5 | 5.0/5 | +0.0 | 1 | 5 | +4.0 | no gain |
| wf5_partial | 4.3/7 | 4.7/7 | +0.3 | 1 | 5 | +3.7 | no gain |
| wf6_multi | 0.7/6 | 2.0/6 | +1.3 | 1 | 4 | +3.3 | fixed helps |
