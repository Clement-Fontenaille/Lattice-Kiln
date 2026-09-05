# Entry 5 — Milestone 4: Ephemeral processor experiments

**Date:** 2026-08-30

**Evidence question:** do ephemeral roles, fresh context, and independent review
beat a monolithic agent on a small task set?

**What the evidence said.**

Setup: `qwen2.5-coder:7b-instruct-q4_K_M` (the M0 working default), naive context
assembly (spec `07`), a **fixed planner → implementer → reviewer chain with no
revision loop**, versus a single monolithic implementer. 4 synthetic tasks
(implement-from-stub, bug-fix-behind-a-failing-test, false-premise, context
-starvation), 2 repetitions, both arms, objective pass/fail per task.

- **Objective pass rate: monolith 6/8, ephemeral 5/8.** An earlier single-rep
  pass ran 3/4 vs 4/4. Across every pass the ephemeral split **never clearly won**
  — it matched or trailed.
- **Cost: ephemeral spent 3× the model calls** (24 vs 8) and **~3× wall-clock**
  (mean ~23 s vs ~7 s per task).
- **False-premise task: both arms, every repetition, correctly declined** and left
  the pre-existing passing tests green. A clean positive for the design claim
  that the correct response to a task may be *not to execute it*
  (`20-cognitive-architecture/01-work-intent-and-task-model.md`) — independent of
  the ephemeral question.
- **Context starvation** (a helper in a file naive assembly does not surface) hurt
  both arms (monolith 1/2, ephemeral 0/2). **No processor ever emitted a context
  request** (0 / 16 runs) — the "ask for missing context" affordance is specified
  and wired but went entirely unused.
- **Independent review**: the reviewer's verdict tracked the objective outcome in
  6/8 ephemeral runs (2 false approvals on the starvation task). But with no
  revision loop in the reduced MVP form, even a correct "needs-change" changed
  nothing — review was **recorded, not consumed**.

**Verdict: inconclusive, leaning weakens** (against "ephemeral roles improve
reasoning quality", `40-roadmap/03-research-and-evaluation-agenda.md`). At this
scale, with deliberately poor context and a non-looping chain, role separation
added latency and cost with no measurable quality gain. It does **not** refute the
hypothesis: N is tiny, variance is high (the trivial task flipped pass/fail
between runs), context assembly is intentionally weak, and the chain has no
feedback edge. The likely missing piece is the reviewer→implementer revision loop
plus better context — not the role split itself.

**Touches.**

- Design: `20-cognitive-architecture/02-processors.md` — record that a
  *non-looping* planner→implementer→reviewer chain did not beat a monolith on
  small tasks, and that independent review with no revision loop is inert.
  `10-foundations/04-context-as-governed-resource.md` — the "processor can request
  missing context" behaviour needs to be prompted or required, not merely
  available (0/16 uptake); it also gave the naive baseline a concrete cost
  (task_4).
- Specification: feeds the **orchestrator contract** (Milestone 5) — a real
  orchestrator is where the reviewer's "needs-change" would route back — and
  **Milestone 7** (naive context measurably cost the starvation task).
- Milestone sequence: no reordering now. The end-of-Milestone-5 rework should
  weigh adding a revision loop to the ephemeral arm before re-running this
  comparison at larger N.

**Runs.** `experiments/M4-ephemeral-processors/` — `fixture/` (task set, schema
`m4-tasks/0`), `harness.py`, `results/results.json` + `results/summary.md`,
`reconstruction_check.py`; per-run records under `runs/` (schema `m2-run/0`,
git-ignored; the 2026-08-30 N=2 set is the reference).
