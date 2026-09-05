# M6 — Evaluation task suite

**State:** done — 2026-09-03
**Findings:** [entry 8](../../../50-findings/08-m6-evaluation-task-suite.md) — **confirms**
**Execution record:** [`M6-evaluation-task-suite.md`](../../../../50-PROGRESS/archives/M6-evaluation-task-suite.md)
**Specification:** [`10-evaluation-task-suite.md`](../../../../10-technical/10-evaluation-task-suite.md)
**Experiment:** `experiments/M6-evaluation-suite/`

## What this milestone was

Everything downstream — the static workflow ([M7](../07-static-supervised-workflow.md))
and every adaptive loop after it — is judged by running it against tasks. The MVP
used a 4-then-6-task fixture that was too small and too synthetic to separate arms
at N ≤ 3, and it missed whole classes of common request.

This milestone built a proper suite and the conceptual treatment behind it:

- A **taxonomy of dev-request shapes** (fix, feature, refactor, perf, migration,
  robustness, API/contract change, dependency, cleanup) crossed with a **trap
  taxonomy** (misdirection, backward-compat, behaviour-preserving, edge coverage,
  false premise / push-back, silent-failure).
- **20–30 tasks**, each with a realistic request; a deterministic partial-credit
  check; an explicit *correct vs plausible-wrong* discriminator the check
  enforces; a `stresses:` tag naming which pipeline capability it exercises; and a
  `decline_correct` flag where pushing back is the right move.
- A **pre-existing passing test** per task, so the regression guard is exercised
  suite-wide.
- A **conceptual document** — how the project evaluates — so later milestones
  consume one shared method instead of each reinventing it.

`experiments/M5-intelligent-orchestration/fixture_workflow/` (wf1–wf6) was folded
in as the seed.

## Evidence question

Does a trap-structured task suite separate pipeline variants that a toy fixture
cannot, and does it surface failure modes the MVP fixture missed?

## What it answered

**Confirms, decisively.** The 30-task suite separated three arms that the 6-task
fixture had left inside noise:

| arm | score | regressions | notes |
|---|---|---|---|
| **dloop** | **24/30** | **0** | 5/5 correct declines, 1–4 calls/task |
| monolith | 18/30 | 7 | plus 4 crashes |
| staged (the M7 candidate) | 19/30 | — | *worse* than plain dloop |

Two calibration facts fell out, and both changed M7's design:

- **The spine is dloop.** Confirmed at scale, not just at N ≤ 3.
- **Premise audit must be advisory, not a gate.** As a hard decline gate it
  false-declined roughly 20% of the suite (`hf_csv`, `hf_json_field`, …), which is
  the entire reason the staged arm underperformed the simpler one.
- **Concern-split fires conditionally.** It took `wf6` from 2/6 to 6/6 but cost
  252 s and helps around two tasks in thirty.

The staged arm losing to the plain spine is the useful result here. It is the
second time in this project that stacking machinery made things worse — the
super-pipeline was the first — and it is why M7's stages must each record whether
they changed the terminal.

## What is owed against it

The suite is now a **ruler**, and no one has checked that it measures one coherent
thing. Construct validation — difficulty distribution, item–total correlation,
dimensionality — is experiment E0 in
[`../../08-next-experiments.md`](../../08-next-experiments.md), it is possibly
answerable from runs already recorded, and it gates most of what follows.
