# Entry 8 — Milestone 6: Evaluation task suite

**Date:** 2026-09-03

**Evidence question:** does a trap-structured task suite separate pipeline
variants that a toy fixture cannot, and does it surface failure modes the MVP
fixture missed?

**What the evidence said.**

A 30-task suite (`experiments/M6-evaluation-suite/`, schema `eval-suite-tasks/0`)
— 11 request shapes × all 7 traps (misdirection, backward-compat,
behaviour-preserving, edge-coverage, false-premise, silent-failure,
multi-concern), 5 `decline_correct`, each with a deterministic partial-credit
check, a documented discriminator subtest, a pre-existing passing test, and
non-gating `STRUCTSCORE`/`DOCSCORE`/`TODOSCORE` where behaviour under-determines
the deliverable. wf1–wf6 folded in as the seed. Three arms, N=1: **monolith**
(one implementer pass), **dloop** (bundle-D: incumbent-protected keeper,
test-gated progress, escalate-on-stall), **staged** (the Milestone-7 leading
candidate: premise audit K=3 + concern-split-aware dloop + refactor→escalate).

| arm | objective pass | regressions | check crashes | decline accuracy |
|---|---|---|---|---|
| monolith | 18/30 | 7 | 4 | 0/5 |
| **dloop** | **24/30** | **0** | **0** | **5/5** |
| staged | 19/30 | 0 | 0 | 5/5 |

The 6-task fixture put these arms within noise (entry 6 addendum: 10 / 11 / 12).
The 30-task suite is decisive, and it surfaced four failure modes the fixture
could not:

1. **The monolith regresses or crashes ~1 task in 3** (7 + 4 of 30) — it fixes
   one thing and breaks another (`hf_dead_code` 4/4→1/4, `hf_dict_dispatch`
   7/7→crash, `hf_extract_fn` 5/5→3/5 dropping the `try/except` trap, …). The
   fixture showed this on one task (wf6). Strongest single argument for the
   incumbent-protected keeper.
2. **Premise audit as a hard decline gate over-declines ~20 %** — `staged`
   declined 11 tasks, only 5 correctly; it false-declined `hf_csv`,
   `hf_json_field`, `hf_json_serialize`, `hf_merge_config`, `hf_path_sanitize`,
   `hf_suppress`. The census established the planner stance *catches* false
   premises; this establishes it also *false-positives* them, so as a unilateral
   gate it is net-negative. This is the load-bearing input to Milestone 7.
3. **Concern-split earns its cost only narrowly** — `staged` took `wf6_multi`
   2/6 → 6/6 SUBTESTS + 3/3 TODO (docs still 0/4) where `dloop` escalates and the
   monolith no-ops, but at 252 s for that one task, and only 2 suite tasks are
   genuine multi-concern → conditional firing, not always-on.
4. **`STRUCTSCORE` + regression-guard together separate** clean-refactor /
   broke-it / didn't-do-it — invisible on the fixture (wf3 alone, no structural
   score).

`stresses` slices separated capability rather than aggregate: cross-file
(monolith 0.47 vs dloop 0.92 — retry-with-failing-lines rescues indirection),
edge-coverage (0.66 / 0.93 / 0.65), silent-failure (~1.0 everywhere — "add a
guard" tasks the 7B does in any arm).

**Verdict: confirms** (the suite is fit for purpose — research-and-evaluation
agenda: "a milestone closes when its evidence question is answerable from a
reconstructable run"). A trap-structured suite separates arms a toy fixture
cannot and exposes safety-relevant failure modes (regression rate, false
decline). **`dloop` is confirmed as the Milestone-7 spine; `staged` as built is
not an improvement**, and the reason is specific: the premise audit must be
advisory, not a gate.

**Touches.**

- Milestone 7 (`01-milestones.md`): the leading-candidate description gains a
  hard constraint — premise audit is advisory / unanimous+pattern-gated, never a
  unilateral hard decline; concern-split fires conditionally on genuine
  multi-concern objectives, not always. The `stresses`-slice deltas are the
  calibration data for which stage runs for which task class.
- Design: `20-cognitive-architecture/01-work-intent-and-task-model.md` — "the
  correct response may be to decline" holds, but *deciding to decline* is itself
  a high-error judgment on a 7B and must not be unilateral.
- `10-technical/10-evaluation-task-suite.md` — v0 validated at N=1; the open
  contract on suite size can note that 30 tasks separated three arms cleanly.
- Milestone sequence: no reordering. M6 closes; M7 executes next against this
  suite.

**Runs.** `experiments/M6-evaluation-suite/` — `tasks.json`, `suite/` (30 task
dirs), `run_suite.py`, `suite_lint.py`, `m6_arms.py`, `results/{monolith,dloop,
staged}.{md,json}`, `FINDINGS.md`. Per-run records under `runs/` (git-ignored;
the 2026-09-02 three-arm N=1 set is the reference).
