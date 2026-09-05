# M2 — Observability foundation

**State:** done — 2026-08-30
**Findings:** [entry 3](../../../50-findings/03-m2-observability-foundation.md) — **confirms**
**Execution record:** [`M2-observability-foundation.md`](../../../../50-PROGRESS/archives/M2-observability-foundation.md)
**Specification:** [`02-observability-event-model.md`](../../../../10-technical/02-observability-event-model.md)
**Experiment:** `experiments/M2-observability-foundation/`

## What this milestone was

Ensure that important AI-assisted work can be reconstructed well enough for later
analysis: invocation identity, model and configuration, context, outputs, tool
activity, repository effects, objective verification, and human correction where
available.

Three requirements were load-bearing and were not to be traded away for a simpler
format:

- Reconstruction must be good enough to detect **composed and drifting behavior
  across sequences** of effects, not only to review effects one at a time.
- The event model must represent a **safety intervention as an outcome category
  distinct from ordinary task failure** — traceable, and not eligible for
  automatic retry without human review.
- Recorded behavior must be relatable to **hypotheses about the system**, not only
  to a narrative of what happened.

The storage format could stay simple. What must be reconstructable could not.

## Evidence question

Can a run be reconstructed well enough to answer a question we have not thought to
ask yet?

## What it answered

**Confirms, with a condition that turned out to matter more than the result.**

Forty real runs were reconstructable, including for questions never designed into
the schema — but only **when the effect envelope carries structured outcome
rather than prose**. Cross-record joins are the mechanism by which an unplanned
question gets answered, and a free-text outcome field cannot be joined on.

That condition is not yet enforced by the specification. It is the *observability
envelope contract* item in [`../../00-backlog.md`](../../00-backlog.md), and it
was reinforced independently by [M5](05-intelligent-orchestration.md).

## Why this milestone was placed early

Observability is the one exception to the "build only what the current milestone
needs" rule. It is a research requirement rather than an operational nicety: every
later milestone's evidence question is answered by reading records this milestone
made possible.
