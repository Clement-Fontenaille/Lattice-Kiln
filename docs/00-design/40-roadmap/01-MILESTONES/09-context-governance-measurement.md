# M9 — Context governance measurement

**State:** open. Possibly a prerequisite for evaluating M7's front half — see
[`../00-backlog.md`](../00-backlog.md).
**Was:** M7, before rework 2
**Baseline it measures against:** [`07-naive-context-assembly.md`](../../../10-technical/07-naive-context-assembly.md)

## What this milestone is

The goal is **not** to design good context governance. It is to establish the
naive default from [M4](completed/04-ephemeral-processors.md) as a measurable
baseline, and to develop **metrics for context quality that are independent of
final task success**.

Without those metrics, a later decision to commission a context-curator role
cannot be made on evidence. This milestone produces the evidence base; it does not
pick the mechanism.

## Why the independence matters

A context-quality metric scored by task outcome is a failure predictor wearing
another name. If context quality can only be recognised after the task succeeded
or failed, it cannot be used to *decide* anything during assembly — and the
curator role it is supposed to justify would be evaluated by the same signal that
already evaluates everything else.

This is the same construct problem experiment E1 in
[`../08-next-experiments.md`](../08-next-experiments.md) attacks from the probe
side: label by **construction**, not by outcome.

## Evidence question

*Not yet stated.* The bar recorded at rework 1:

> The naive assembler's observed failures — the wrong-file writes on `wf1`, the
> missed helper on `wf4`/`wf6` — are quantifiable, and a less-naive assembler
> moves the metric.

## Why it may need to move earlier

[M7](07-static-supervised-workflow.md)'s proposed front half is convergence before
implementation, and its unresolved problem is that **convergence closes on
nothing** — `dloop` closes on a test, but nothing validates the artifact the
convergence step produces. Validating that artifact is a context-quality question,
which is this milestone's subject.

If M7's front half is pursued, this milestone becomes a prerequisite rather than a
later measurement chore. If M7 ships with the settled back half only, it does not.
That decision is open and is tracked in [`../00-backlog.md`](../00-backlog.md).

## Related foundations

Two positions were added to
[`04-context-as-governed-resource.md`](../../10-foundations/04-context-as-governed-resource.md)
in the 2026-09-05 design pass and have not yet flowed into this milestone's
framing or into the specification set:

- *Too much is a relation, not a property.*
- *What makes context costly is redundancy, not volume.*

Both bear directly on what a context-quality metric should measure. Carrying them
down is listed as un-carried work in [`../00-backlog.md`](../00-backlog.md).
