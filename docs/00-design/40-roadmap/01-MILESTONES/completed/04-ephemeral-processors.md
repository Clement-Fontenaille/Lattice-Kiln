# M4 — Ephemeral processor experiments

**State:** done — 2026-08-30
**Findings:** [entry 5](../../../50-findings/05-m4-ephemeral-processors.md) — inconclusive, leaning **weakens**
**Execution record:** [`M4-ephemeral-processors.md`](../../../../50-PROGRESS/archives/M4-ephemeral-processors.md)
**Specifications:** [`06-processor-contract.md`](../../../../10-technical/06-processor-contract.md), [`07-naive-context-assembly.md`](../../../../10-technical/07-naive-context-assembly.md)
**Experiment:** `experiments/M4-ephemeral-processors/`

## What this milestone was

Introduce independent role-specific invocations outside a monolithic coding
conversation.

Use a small set of roles only, to learn whether role separation, fresh context,
independent assessment, and adversarial review provide practical value.

Processors receive deliberately naive context assembly at this stage — some
unglamorous, possibly poor, default. Its job is to be a measurable baseline, not
to be good. [M9](../09-context-governance-measurement.md) is the milestone that
measures against it.

## Evidence question

Do ephemeral roles, fresh context, and independent review beat a monolithic agent
on a small task set?

## What it answered

**Inconclusive, leaning weakens** — the first result that went against the
architecture's expectations.

A non-looping planner→implementer→reviewer chain scored **5/8 against a
monolith's 6/8, at roughly 3× the cost**. Independent review with no revision edge
was inert: the reviewer produced assessments that changed nothing, because nothing
downstream could act on them.

The lean is toward *weakens* rather than *refutes* because N=8 is within noise and
because the missing revision edge is a plausible explanation for the whole
result — a review that cannot cause a revision is not a test of review.

## What it changed

The revision loop was promoted to a first-class element rather than an
implementation detail, and the result set up the two milestones that followed:
[M5](05-intelligent-orchestration.md) added adaptive coordination over the same
runtime, and the M5 follow-up eventually established that the reviewer seat itself
was the problem — not the loop around it.

Design touches: the effect vocabulary (a conclusion is a type-4 effect),
[`02-processors.md`](../../../22-arch-cognition/02-processors.md),
[`04-context-as-governed-resource.md`](../../../10-foundations/04-context-as-governed-resource.md),
[`01-observability.md`](../../../26-arch-observability/01-observability.md).

## Owed re-test

The comparison is N=8 and within noise. A productive re-test needs the revision
loop, a non-naive context assembler ([M9](../09-context-governance-measurement.md)),
and durable work records ([M8](../08-persistent-work-and-knowledge.md)) — so it is
a task inside those milestones rather than a milestone of its own. Tracked in
[`../../00-backlog.md`](../../00-backlog.md).
