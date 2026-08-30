# M2 — Observability Foundation

**Milestone:** `40-roadmap/01-milestones.md` → Milestone 2
**Evidence question:** can a run be reconstructed well enough to answer a question we have not thought to ask yet?
**State:** COMPLETE (2026-08-30) — findings-log entry 3

## What "done" looks like

An AI-assisted run can be reconstructed after the fact well enough that a later
analyst — or a later milestone's experiment — can relate what happened to a
hypothesis about the system, not merely narrate the sequence of events.

Three requirements are load-bearing and must not be traded for a simpler format
(`40-roadmap/01-milestones.md` M2, `20-cognitive-architecture/06-observability.md`):

1. Reconstruction detects **composed and drifting behaviour across sequences** of
   effects, not only single effects reviewed in isolation.
2. The event model represents a **safety intervention as its own outcome
   category**, distinct from ordinary task failure, traceable, and not eligible
   for automatic retry without human review.
3. Recorded behaviour is **relatable to hypotheses** about the system (e.g.
   comparing two context policies, two orchestrator versions), not only to a
   narrative.

Storage may stay simple. What must be reconstructable may not.

## Deliverables

- `10-technical/02-observability-event-model.md` — the v0 contract. Pins
  invocation identity, the realized-effect record, the safety-intervention
  outcome category, and per-actor / per-intent sequence reconstructability.
  Expected to carry many open contracts; the schema emerges from the first
  experiments (M4/M5).
- A minimal recorder wired into whatever runs during M4, emitting the event
  model's records to a simple store (files/JSONL is fine).
- A reconstruction check: pose a question *not* designed into the schema and show
  it can be answered from stored records alone.

## Task breakdown

| # | Task | State | Notes |
|---|---|---|---|
| 1 | Write `02-observability-event-model.md` v0 | DONE | Binds to `01-effect-vocabulary.md`. Four mandatory event kinds + open contracts. |
| 2 | Decide the record store shape | DONE | JSONL, one file per run (`runs/<run_id>/events.jsonl` + `run.json`), per-run monotonic `seq` for total order. Illustrative; see `experiments/M2-observability-foundation/README.md`. |
| 3 | Invocation identity + lineage | DONE | `event_model.RunRecorder.invocation()` — `invocation_id`, `parent_invocation_id`, `intent_ref`, `role`, `model_identity` (incl. `offloaded`). `reconstruct.per_intent()` / `intent_lineage()` walk the tree. Self-tested. |
| 4 | Realized-effect record | DONE | `.realized_effect()` — typed by the 9-effect vocabulary, `envelope` carries the representable/permitted/attributable/reversible fields, `outcome`. Plus `.proposed_effect()` (kind 4). |
| 5 | Safety-intervention outcome category | DONE | `.safety_intervention()` — distinct `kind`, `retry_eligible=False` always, `human_review_ref` null until attached. Self-test asserts it is never folded into a generic effect/failure. |
| 6 | Minimal recorder | DONE (standalone) | `event_model.py`, stdlib only, runs under Windows Python and WSL python3. Loud on write failure (no silent gap). Wiring into a real processor run is an M4 step. |
| 7 | Reconstruction check | DONE | `experiments/M4-ephemeral-processors/reconstruction_check.py` poses two questions the schema was not shaped around (reviewer verdict vs objective outcome; role behind each refused effect) and answers both from `events.jsonl` alone across 16 real M4 runs. |
| 8 | Findings-log entry | DONE | Entry 3. Verdict **confirms** — with the caveat that reconstruction is only as good as the structured content the effect envelope carries (a free-text-only conclusion broke one query until `verdict` was added). |

## State

The event model and recorder are **built and self-tested**. M2's evidence
question is answered provisionally against a synthetic run; it is formally closed
at M4 when the recorder is wired into a real processor run and an unplanned
question is answered from that. Per the execution cadence, observability is
deliberately ahead of the milestone that consumes it.

## Carried from M0 (findings-log entry 1)

- The event model **must record model + quant per invocation and whether
  inference was offloaded** — on the measured host that flag predicts latency by
  10–20×, so any performance hypothesis needs it.
- Per-role model switching is not viable on the MVP host; the recorder should not
  assume a model changes between invocations, but should not forbid recording it
  either.

## Notes

- Just-in-time: write only the contracts M2 and M3 need. M3 (the gate) consumes
  the realized-effect record and the sequence-reconstruction guarantee, so those
  parts must be firm; retention, redaction, and summarisation stay open.
- Sequence evaluation window/grouping is an open contract owned by
  `20-cognitive-architecture/07-invariant-enforcement.md`; the event model only
  guarantees the ordered history exists and is queryable per actor and per intent.
