# E2 — forecast test result

Generated 2026-09-17T11:23:53.191073+00:00.

Pre-registration: `experiments\E2-grain-versus-quantity\preregistration\ranking-2026-09-17.json` (proxy P1, committed before any Nemotron result was read).

## Sweep coverage — the sweep did not finish

- Nemotron arms present: **baseline, test_synth**
- of which usable (non-degenerate, matched in qwen): **test_synth**

`baseline` makes no model call and cannot diverge by model; it is used only
as a harness sanity check.

- sanity `baseline`: 34 tasks compared, mismatches: **none — harness consistent**

## Divergence by pre-registered band

Band sizes in the pre-registration: high 14, low 14, mid 6.

| band | tasks compared | divergent | rate |
|---|---|---|---|
| high | 14 | 4 | 28.6% |
| mid | 6 | 4 | 66.7% |
| low | 14 | 9 | 64.3% |
| **total** | **34** | **17** | **50.0%** |

## The divergent tasks

| arm | task | band | P1 count | qwen | nemotron | direction |
|---|---|---|---|---|---|---|
| test_synth | hf_rename | high | 6 | pass | fail | qwen_only |
| test_synth | hf_json_serialize | high | 4 | pass | fail | qwen_only |
| test_synth | hf_retry_backoff | high | 4 | pass | fail | qwen_only |
| test_synth | wf3_refactor_witnessed | high | 4 | pass | fail | qwen_only |
| test_synth | hf_audit_perf | mid | 3 | pass | fail | qwen_only |
| test_synth | hf_counter_race | mid | 3 | pass | fail | qwen_only |
| test_synth | hf_return_shape | mid | 3 | pass | fail | qwen_only |
| test_synth | wf2_retry | mid | 3 | fail | pass | nemotron_only |
| test_synth | hf_csv | low | 2 | pass | fail | qwen_only |
| test_synth | hf_json_field | low | 2 | pass | fail | qwen_only |
| test_synth | hf_merge_config | low | 2 | pass | fail | qwen_only |
| test_synth | hf_multi_recipient | low | 2 | pass | fail | qwen_only |
| test_synth | hf_pagination | low | 2 | pass | fail | qwen_only |
| test_synth | hf_path_sanitize | low | 2 | pass | fail | qwen_only |
| test_synth | hf_rec_to_iter | low | 2 | pass | fail | qwen_only |
| test_synth | hf_suppress | low | 2 | pass | fail | qwen_only |
| test_synth | hf_validate_withdraw | low | 2 | pass | fail | qwen_only |

## Confound audit — tasks that cannot show divergence

Two classes of task pass regardless of what the model did, so they cannot
diverge on `objective_pass` no matter how the models differ:

- **false premise** (`expect.decline_correct`): doing nothing is the answer.
- **no witness** (E0 part 1, 2026-09-17): the untouched source passes while
  work is demanded — `wf3_refactor`, `hf_extract_fn`, `hf_dict_dispatch`.

| band | tasks | of which blind | divergence rate, all | divergence rate, sighted only |
|---|---|---|---|---|
| high | 14 | 6 | 28.6% | 50.0% |
| mid | 6 | 1 | 66.7% | 80.0% |
| low | 14 | 2 | 64.3% | 75.0% |

## Reading

- prediction: **qwen<->Nemotron per-task divergence clusters in the HIGH band (count >= 4) rather than distributing across bands in proportion to band size.**
- falsifier: **Divergence distributed across bands in rough proportion to band size (14/6/14), or concentrated in the LOW band.**
- stated power limit: 34 tasks, bands of 14/6/14, N=1 on the Nemotron side against N=3 or N=5 collapsed by strict majority on the qwen side. This design distinguishes strong clustering from clear proportionality and nothing finer. Directional, not decisive.

