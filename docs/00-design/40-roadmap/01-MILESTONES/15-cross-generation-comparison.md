# M15 — Cross-generation comparison

**State:** open
**Was:** M13, before rework 2

## What this milestone is

Compare models, strategies, and system generations under controlled conditions.

Use this milestone to decide whether the project is producing **cumulative system
capability** rather than merely increasing architectural complexity.

## What it owns

**Per-role model assignment** — which model plans, which implements, which
evaluates — is one of the dimensions compared here rather than at any earlier
milestone. [M0](completed/00-inference-envelope.md) established that per-role
model switching is not viable on the reference host, so the question is
unanswerable until a second resident model exists.

**Reviewer independence.** Whether two models are independent enough to provide
genuine adversarial evaluation, rather than merely correlated judgment, is a
question this milestone can begin to answer. It matters more than it looks: the
whole self-improving tier is gated on a second judgment source, and a second model
that is merely *correlated* with the first supplies the appearance of one without
the substance.

**Competing orchestrators**, and whether a stronger orchestrator model changes the
M5 result, are deferred here from
[`08-orchestrator-contract.md`](../../../10-technical/08-orchestrator-contract.md).

## Relationship to the capability sweep

Experiment E4 in [`../08-next-experiments.md`](../08-next-experiments.md) — the
existing suite across models, varying **size and tuning, not size alone** — is a
scaled-down early instance of this milestone's question, runnable long before the
milestone itself. Its warning applies here too: a size-only design cannot separate
a capability effect from a tuning artifact.
