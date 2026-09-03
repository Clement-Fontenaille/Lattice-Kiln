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

## Results (3-arm comparison, N=1, 2026-09-02)

| arm | objective pass | regressions | check crashes | decline accuracy | total wall |
|---|---|---|---|---|---|
| monolith | 18/30 | **7** | **4** | **0/5** | 260 s |
| **dloop** | **24/30** | **0** | **0** | **5/5** | 406 s |
| staged | 19/30 | 0 | 0 | 5/5 | 710 s |

Where the 6-task toy fixture put the arms within noise (M5: 10 / 11 / 12), the
30-task suite is decisive.

### 1. The monolith regresses or crashes ~1 task in 3

7 regressions + 4 check-crashes in 30. It "fixes" one thing and breaks another:
`hf_dead_code` 4/4 → 1/4 (removed the live function), `hf_dict_dispatch` 7/7 →
crash, `hf_misfiled_bug` 3/4 → crash (rewrote `rect_area`), `hf_pagination` /
`hf_timeout_param` → crash, `hf_extract_fn` 5/5 → 3/5 (dropped the `try/except`),
`hf_cache_decorator` (corruption). The MVP fixture showed this on **one** task
(wf6). The strongest single argument for the incumbent-protected keeper.

### 2. `dloop` — the cheap loop — wins outright

24/30, **zero regressions, zero crashes, 5/5 declines**, at 1–4 calls/task. The
incumbent-in-keeper-pool + test-gated progress captures nearly all the achievable
value. Its 6 non-passes: 4 honest `escalate`s (`hf_dict_dispatch`,
`hf_rec_to_iter`, `hf_misfiled_bug` cross-file, `hf_multi_recipient`,
`wf6_multi`), 2 partial (`hf_timeout_param` 5/6, `wf2_retry` 3/5).

### 3. `staged` (the M7 leading candidate) is a **regression vs plain `dloop`**

19/30 vs 24/30. Cause: the **premise audit as a hard decline gate over-declines**.
It declined 11 tasks; only 5 were correct. False declines of real work:
`hf_csv`, `hf_json_field`, `hf_json_serialize`, `hf_merge_config`,
`hf_path_sanitize`, `hf_suppress` — all legitimate tasks the K=3 audit majority
-voted "unsound". This is the census finding's other half: the planner/analyst
stance catches false premises **and** false-positives them; as a hard gate it
throws away ~20 % of the suite.

**M7 consequence:** premise audit must be **advisory** (surface for human) or
gated on *unanimous* unsound + a recognised impossibility pattern — never a
unilateral hard decline.

### 4. Concern-split earns its cost, narrowly

`staged` got `wf6_multi` 2/6 → **6/6 SUBTESTS + TODOSCORE 3/3** (DOCSCORE still
0/4) — the concern-split lever, where `dloop` escalates and the monolith no-ops.
But it cost **252 s** for that one task, and only 2 suite tasks are genuine
multi-concern. Conditional firing, not always-on.

### 5. `stresses` slices separate capability, not just aggregate

| slice | monolith | dloop | staged | reads as |
|---|---|---|---|---|
| cross-file | 0.47 | 0.92 | 0.92 | the retry-with-failing-lines rescues indirection the monolith botches |
| edge-coverage | 0.66 | 0.93 | 0.65 | dloop's iteration lands the edges; staged's over-decline tanks it |
| partial-credit | 0.74 | 1.00 | 0.54 | same |
| L2-structural (SUBTESTS) | 0.77 | 0.97 | 0.97 | the keeper protects behaviour during a refactor; the monolith doesn't |
| silent-failure | 1.00 | 1.00 | 0.94 | "add a guard" tasks — the 7B does these fine in any arm |

## Verdict

**The evidence question is answered: yes.** A trap-structured 30-task suite
separates arms a 6-task fixture cannot, and it surfaced four failure modes the
fixture missed: the monolith's ~30 % regression/crash rate, premise-audit-as-gate
false-declining ~20 % of legit work, the concern-split cost/benefit ratio, and
`STRUCTSCORE` + regression-guard distinguishing clean-refactor / broke-it /
didn't-do-it. `dloop` is confirmed as the M7 spine; `staged` as built is not an
improvement and tells M7 exactly what to change.
