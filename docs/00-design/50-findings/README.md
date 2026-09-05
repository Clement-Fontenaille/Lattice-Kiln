# Findings

## TL;DR

One entry per completed milestone, recording what its evidence question actually
answered and what that answer touches. This is the empirical counterpart to the
research and evaluation agenda.

> **Motto:** A milestone closes when it has taught us something, and this is where we write down what.

## Why this is its own space

Findings are not roadmap. The roadmap states what the project intends to do and in
what order; findings state what happened when it did. They are consumed by the
roadmap at rework points, but they are not part of it — and keeping them there
made the sequencing documents answerable to a record that only grows.

The distinction matters for stability. Roadmap documents are revised. **Entries
here are appended, never rewritten.** If a later milestone contradicts an earlier
finding, that contradiction is a new entry referencing the old one, not an edit to
it.

## How this log is used

The execution cadence routes findings design-first: an entry is written when a
milestone completes, and its consequences then flow into the relevant design
document, then into the specification's open contracts, then — at a scheduled
rework point — into the milestone sequence itself.

Entries are cited elsewhere by number — *"findings-log entry 5"* — and that
reference is stable regardless of which file an entry lives in.

## Entry format

Each entry provides:

- **Milestone** — number and name.
- **Evidence question** — copied from the milestone, so the entry stands alone.
- **What the evidence said** — the observed result, in plain terms.
- **Verdict** — against the relevant hypothesis in the research and evaluation
  agenda, one of: confirms, weakens, refutes, inconclusive. "Inconclusive" is a
  legitimate and useful outcome.
- **Touches** — which design documents and which specification open contracts this
  finding bears on.
- **Runs** — reference to the reconstructable observability run or runs the
  finding rests on.

An entry may carry **addenda** — later work within the same investigation,
appended under the entry rather than given a number of their own.

## Two kinds of entry

**Milestone entries** are the default and follow the format above.

**Field entries** record external work the design set has come to rest on:
published research, industry telemetry, vendor documentation. They share the
numbering and the append-only rule, and differ where the format cannot apply —
there is no evidence question of ours, no reconstructable run, and no verdict.
In their place they carry **per-claim reliability**, **what in the design set
depends on the claim**, and a **re-verify-by date**, because external claims age
and a foundation citing one should not be the last place that ageing becomes
visible.

## Entries

| # | subject | date | verdict | file |
|---|---|---|---|---|
| 1 | M0 — local inference envelope | 2026-08-30 | **confirms** | [`01-m0-inference-envelope.md`](01-m0-inference-envelope.md) |
| 2 | M1 — reproducible baseline environment | 2026-08-30 | inconclusive | [`02-m1-baseline-environment.md`](02-m1-baseline-environment.md) |
| 3 | M2 — observability foundation | 2026-08-30 | **confirms** | [`03-m2-observability-foundation.md`](03-m2-observability-foundation.md) |
| 4 | M3 — invariant floor (reduced form) | 2026-08-30 | inconclusive, leaning confirms | [`04-m3-invariant-floor.md`](04-m3-invariant-floor.md) |
| 5 | M4 — ephemeral processor experiments | 2026-08-30 | inconclusive, leaning **weakens** | [`05-m4-ephemeral-processors.md`](05-m4-ephemeral-processors.md) |
| 6 | M5 — intelligent orchestration | 2026-08-31 | confirms, narrowly | [`06-m5-intelligent-orchestration.md`](06-m5-intelligent-orchestration.md) |
| 7 | M5 follow-up — census, judge-lab, loop-lab, pipeline-lab | 2026-09-01 | **confirms** | [`07-m5-followup-investigation.md`](07-m5-followup-investigation.md) |
| 8 | M6 — evaluation task suite | 2026-09-03 | **confirms** | [`08-m6-evaluation-task-suite.md`](08-m6-evaluation-task-suite.md) |
| 9 | *field entry* — external evidence the design set rests on | 2026-09-05 | — (re-verify by 2027-03-05) | [`09-field-evidence-2026-09.md`](09-field-evidence-2026-09.md) |

Entry 6 carries one addendum (workflow-suite re-test). Entry 7 carries two
(loop control; super-pipeline).
