# M2 — Observability Foundation

**Milestone:** `40-roadmap/01-milestones.md` → Milestone 2
**Evidence question:** can a run be reconstructed well enough to answer a question we have not thought to ask yet?
**State:** WIP — decomposing

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
| 1 | Write `02-observability-event-model.md` v0 | WIP | Binds to `01-effect-vocabulary.md`. Draft in this batch. |
| 2 | Decide the record store shape | TODO | JSONL per run vs. one growing log. Illustrative only until M4 forces it. |
| 3 | Invocation identity + lineage | TODO | Stable id per processor invocation; parent/intent links so per-actor and per-intent histories reconstruct. |
| 4 | Realized-effect record | TODO | One record per effect the runtime realizes, typed by the effect vocabulary, carrying enough to judge it after the fact. |
| 5 | Safety-intervention outcome category | TODO | Distinct terminal outcome; carries the gate trip and the decommission signal; marked no-auto-retry. |
| 6 | Minimal recorder | TODO | Wire into the M4 processor harness. Thin. |
| 7 | Reconstruction check | TODO | The evidence question. Pick an unplanned question, answer it from records. |
| 8 | Findings-log entry | TODO | Verdict: is unplanned-question reconstruction actually possible with this model. |

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
