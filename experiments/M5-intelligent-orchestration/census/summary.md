# Attractor census - raw observation table
_model qwen2.5-coder:7b-instruct-q4_K_M, temp 0.4, 117 calls, 9.9 min_

Booleans shown as hits/samples. Read the transcripts in `runs/` for the actual motion - this table only says where to look.

## doer

| probe | file_blocks | terminal_state | past_done_hits | hedge_hits | refusal_hits | touches_pricing | touches_orders_only | mentions_round | did_binary_search | mentions_sorted_precond | all_three_concerns | kept_todo_2019 | gen_tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fix_indirection__bare | 0.3 | answered:3 | 2.0 | 0.0 | 0.0 | 1/3 | 0/3 | - | - | - | - | - | 100.3 |
| fix_indirection__plan_prose | 1.3 | answered:3 | 1.3 | 0.0 | 0.0 | 3/3 | 0/3 | - | - | - | - | - | 99.7 |
| fix_indirection__critique_prose | 1.3 | answered:3 | 1.3 | 0.0 | 0.0 | 3/3 | 0/3 | - | - | - | - | - | 103.7 |
| fix_indirection__here_is_file | 1.0 | answered:3 | 1.7 | 0.0 | 0.0 | 3/3 | 0/3 | - | - | - | - | - | 104.3 |
| fix_local__bare | 0.7 | answered:3 | 1.0 | 0.0 | 0.0 | 2/3 | 0/3 | - | - | - | - | - | 82.3 |
| fix_local__here_is_file | 1.0 | answered:3 | 1.0 | 0.0 | 0.0 | 3/3 | 0/3 | - | - | - | - | - | 90.3 |
| refactor_trap__bare | 1.0 | answered:3 | 0.3 | 0.0 | 0.0 | - | - | 3/3 | - | - | - | - | 163.0 |
| refactor_trap__plan_prose | 0.3 | answered:3 | 0.0 | 0.0 | 0.0 | - | - | 3/3 | - | - | - | - | 151.7 |
| refactor_trap__here_is_file | 0.3 | answered:3 | 0.3 | 0.0 | 0.0 | - | - | 3/3 | - | - | - | - | 166.0 |
| false_premise__bare | 1.0 | answered:3 | 0.3 | 0.0 | 0.0 | - | - | - | 3/3 | 0/3 | - | - | 190.3 |
| false_premise__here_is_file | 0.7 | answered:3 | 1.0 | 0.0 | 0.0 | - | - | - | 3/3 | 0/3 | - | - | 166.7 |
| implement_fresh__bare | 0.7 | answered:3 | 1.0 | 0.0 | 0.0 | - | - | - | - | - | - | - | 326.0 |
| implement_fresh__here_is_file | 1.0 | answered:3 | 1.7 | 0.0 | 0.0 | - | - | - | - | - | - | - | 307.7 |
| feature_choice__bare | 0.3 | answered:3 | 1.0 | 0.0 | 0.0 | - | - | - | - | - | - | - | 188.3 |
| feature_choice__here_is_file | 0.7 | answered:3 | 1.7 | 0.0 | 0.0 | - | - | - | - | - | - | - | 198.0 |
| multi_concern__bare | 0.0 | answered:3 | 2.3 | 0.0 | 0.3 | - | - | - | - | - | 1/3 | - | 517.0 |
| multi_concern__one_concern_algo | 0.0 | answered:3 | 1.7 | 0.0 | 0.0 | - | - | - | - | - | 0/3 | - | 272.7 |
| multi_concern__one_concern_docs | 0.0 | answered:3 | 1.0 | 0.0 | 0.7 | - | - | - | - | - | 1/3 | - | 438.3 |
| multi_concern__one_concern_todo | 0.0 | answered:3 | 1.0 | 0.0 | 0.0 | - | - | - | - | - | 0/3 | - | 116.3 |

## judge

| probe | verdict | numbered_items | pass_token | hedge_hits | mentions_round | mentions_qty | mentions_exact_or_staff | gen_tok |
|---|---|---|---|---|---|---|---|---|
| review_wf3_correct__is_correct | approve:3 | 0.0 | 0/3 | 0.0 | 1/3 | - | 3/3 | 124.7 |
| review_wf3_correct__predict_failure | approve:3 | 0.0 | 3/3 | 0.0 | 0/3 | - | 1/3 | 66.3 |
| review_wf3_correct__criteria_first | approve:3 | 4.3 | 0/3 | 0.0 | 3/3 | - | 3/3 | 284.7 |
| review_wf3_correct__strongest_reason | approve:3 | 0.0 | 0/3 | 0.0 | 2/3 | - | 3/3 | 131.3 |
| review_wf3_correct__adversarial_anon | approve:3 | 0.0 | 0/3 | 0.0 | 3/3 | - | 3/3 | 153.3 |
| review_wf3_broken__is_correct | approve:3 | 0.0 | 0/3 | 0.0 | 0/3 | - | 3/3 | 121.0 |
| review_wf3_broken__predict_failure | approve:3 | 0.0 | 3/3 | 0.0 | 1/3 | - | 1/3 | 63.3 |
| review_wf3_broken__criteria_first | approve:3 | 6.3 | 0/3 | 0.0 | 3/3 | - | 3/3 | 296.0 |
| review_wf3_broken__strongest_reason | approve:1 | 0.0 | 0/3 | 0.0 | 1/3 | - | 2/3 | 64.3 |
| review_wf1_correct__is_correct | approve:2,needs-change:1 | 0.0 | 0/3 | 0.3 | - | 0/3 | - | 140.3 |
| review_wf1_correct__predict_failure | approve:2,needs-change:1 | 0.0 | 3/3 | 0.0 | - | 0/3 | - | 70.7 |
| review_wf1_correct__criteria_first | needs-change:2,approve:1 | 4.0 | 0/3 | 0.0 | - | 2/3 | - | 277.0 |
| review_wf1_empty__is_correct | needs-change:2,approve:1 | 0.0 | 0/3 | 0.0 | - | 2/3 | - | 144.3 |
| review_wf1_empty__predict_failure | needs-change:2,approve:1 | 0.0 | 3/3 | 0.0 | - | 0/3 | - | 88.0 |

## plan

| probe | terminal_state | numbered_items | refusal_hits | mentions_sorted_precond | all_three_concerns | touches_orders_only | gen_tok |
|---|---|---|---|---|---|---|---|
| plan_false_premise__plan_bare | answered:3 | 5.7 | 0.0 | 2/3 | - | - | 140.0 |
| plan_false_premise__whats_missing | answered:3 | 3.0 | 0.0 | 2/3 | - | - | 249.7 |
| plan_multi__plan_bare | answered:3 | 5.0 | 0.0 | - | 3/3 | - | 162.7 |
| plan_multi__whats_missing | answered:1 | 1.0 | 0.0 | - | 1/3 | - | 141.0 |
| plan_indirection__plan_bare | answered:3 | 2.3 | 0.0 | - | - | 0/3 | 111.3 |
| plan_indirection__whats_missing | answered:3 | 1.3 | 0.0 | - | - | 0/3 | 215.3 |
