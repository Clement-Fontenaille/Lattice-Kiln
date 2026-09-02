# M6 evaluation task suite — findings

**Date:** 2026-09-02 (comparison run in progress)
**Evidence question:** does a trap-structured task suite separate pipeline
variants that a toy fixture cannot, and does it surface failure modes the MVP
fixture missed?

## The suite (v0)

30 tasks, `eval-suite-tasks/0`. **11 request shapes** (fix, feature, implement,
refactor, perf, compat, robustness, cleanup, data, dependency-adjacent,
migration, concurrency) × **all 7 traps** (misdirection, backward-compat,
behaviour-preserving, edge-coverage, false-premise, silent-failure,
multi-concern). **5 `decline_correct`** tasks. Each: a realistic request, a
stdlib deterministic check (< 1 s), a documented discriminator subtest, a
pre-existing passing test, `SUBTESTS` (gates) plus non-gating `STRUCTSCORE` /
`DOCSCORE` / `TODOSCORE` where behaviour under-determines the deliverable.

Seed: `fixture_workflow/` wf1–wf6, re-tagged. New: `hf_*` (24).

Baselines (pristine score) span the full range:

| band | tasks |
|---|---|
| 0/n (greenfield) | wf2, wf5, hf_pagination(1/5), hf_path_sanitize(1/8), hf_deprecate(1/4) |
| partial | wf1, wf6, hf_json_field, hf_json_serialize, hf_timeout_param, hf_return_shape, hf_multi_recipient, hf_csv, hf_merge_config, hf_retry_backoff, hf_misfiled_bug, hf_suppress, hf_validate_withdraw, hf_rec_to_iter, hf_rename |
| full SUBTESTS, low STRUCT | wf3, hf_extract_fn, hf_dict_dispatch |
| full (decline tasks) | wf4, hf_already_optimal, hf_dead_code, hf_remove_validation, hf_cache_nondeterministic |

## Comparison arms

- **monolith** — one implementer pass (M4 runtime).
- **dloop** — bundle-D core: incumbent-protected keeper (rejects *any* subtest
  regression, even for a structural gain — the suite caught this rule missing on
  `hf_extract_fn`), test-gated progress, best-of-N, escalate-on-stall.
- **staged** — the Milestone-7 leading candidate: premise audit (K=3,
  multi-part-tolerant) + concern-split-aware dloop core + "refactor with no test
  signal → escalate". *Not* the always-on super-pipeline (data already in
  `pipeline_lab` / findings-log entry 7 addendum).

## Results

_Comparison run (`monolith` → `dloop` → `staged`, N=1) in progress. Results:
`results/{monolith,dloop,staged}.{md,json}`._

<!-- FILL: aggregate table (pass / regressions / decline accuracy / calls per arm),
     stresses-slice deltas, per-trap separation, failure modes the suite surfaced
     that wf1-6 alone did not. -->

## Early signal (from smokes)

- The suite **already caught a keeper bug**: `hf_extract_fn` under `staged`
  shipped `SUBTESTS 4/5 + STRUCTSCORE 3/3` because the combined score rose —
  i.e. it did the refactor but fell into the exact dropped-`try/except` trap the
  task was built for, and the combined-score keeper let the subtest regression
  through. Fixed (keeper now vetoes any subtest regression). A toy fixture
  without a structural dimension + regression guard would not have exposed this.
- **Decline separation works**: `staged`'s premise audit declined wf4 and
  `hf_dead_code` (decline accuracy 2/2 on the smoke); `dloop` and `monolith`
  cannot decline and score these as "resolved, repo untouched" — a visible arm
  difference the MVP fixture (one decline task, wf4) could barely show.
- **Behaviour-preserving separation works**: `dloop` escalates `hf_extract_fn`
  ("did nothing, flag it"); `staged` resolves it (`STRUCTSCORE 3/3`, no
  regression) — the loop_lab wf3 "no-op a refactor" limitation, now visible on a
  second task.
