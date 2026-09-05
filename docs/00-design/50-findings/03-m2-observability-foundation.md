# Entry 3 — Milestone 2: Observability foundation

**Date:** 2026-08-30

**Evidence question:** can a run be reconstructed well enough to answer a question
we have not thought to ask yet?

**What the evidence said.**

The M2 recorder (`experiments/M2-observability-foundation/event_model.py`, schemas
`m2-run/0` / `m2-event/0`) was wired into the M4 processor runtime and recorded
**16 real runs** (4 tasks × 2 arms × 2 repetitions). Reconstruction was then
tested with questions the schema was not shaped around
(`experiments/M4-ephemeral-processors/reconstruction_check.py`), answered from
`events.jsonl` alone:

- **Q1 — did the independent reviewer's verdict agree with the objective
  outcome?** Answering it joins the reviewer's conclusion record (a type-4
  realized effect) with the harness root's final objective-check record (a type-2
  realized effect). Neither record references the other; the join is ad hoc.
  Answerable — it surfaced 2/8 ephemeral runs where the reviewer approved a run
  that objectively failed.
- **Q2 — for every refused proposed effect, which role proposed it, which layer
  stopped it, and did the run still pass?** Join across `invocation.role` ×
  `proposed_effect.disposition` × the final check. Answerable — all 17 refusals
  were capability-layer planner/reviewer overreach; several of those runs still
  reached their objective.

Per-actor and per-intent lineage reconstructed cleanly (harness root → planner /
implementer / reviewer as children under one `intent_ref`). The
safety-intervention category stayed distinct: the plumbing test's synthetic
`gate_refusal` was recorded as its own kind with `retry_eligible=False`, never
folded into task failure.

One real gap: the first recorded pass stored the processor's conclusion with only
a free-text `summary`, so "did the reviewer approve?" degraded to string
-sniffing. Adding a structured `verdict` to the type-4 effect envelope fixed it.

**Verdict: confirms** — a run is reconstructable well enough to answer questions
nobody designed the schema for, **provided the effect envelope carries the
structured result and not just prose**. The reconstruction is exactly as good as
what the envelope was told to hold.

**Touches.**

- Design: `20-cognitive-architecture/06-observability.md` — the reconstruction
  requirement holds up in practice; add that the recorded form of an effect must
  carry its *structured* outcome, since ad-hoc cross-record joins are how
  unplanned questions get answered.
- Specification open contracts (`10-technical/02-observability-event-model.md`):
  **the four-property / envelope carrier** contract is load-bearing — sharpen it,
  do not close it. **Hypothesis linkage** — Q1/Q2 were answered by hand-written
  joins; a first-class `experiment_id` / run-tag would have made them one-liners.
  Still deferred, now with a concrete motivating case.
- Milestone sequence: no reordering. M2 tasks 7–8 are now closed by this entry.

**Runs.** `experiments/M4-ephemeral-processors/results/results.json` (committed),
`reconstruction_check.py`, per-run records under
`experiments/M4-ephemeral-processors/runs/` (schema `m2-run/0`, git-ignored; the
2026-08-30 N=2 set is the reference). Recorder + synthetic self-test:
`experiments/M2-observability-foundation/`.
