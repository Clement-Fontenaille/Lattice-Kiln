# M12 — System-level candidate tuning

**State:** open. **Gated on [M11](11-safety-response.md)** and on a second
judgment source.
**Was:** M10, before rework 2
**Design:** [`02-system-level-feedback.md`](../../30-adaptation-and-evolution/02-system-level-feedback.md), [`05-experiments-and-candidate-systems.md`](../../30-adaptation-and-evolution/05-experiments-and-candidate-systems.md)

## What this milestone is

Use recurring evidence across tasks or projects to propose changes to processors,
orchestration, context policy, and evaluation behavior.

Valid categories of change include processor definitions, orchestrator
instructions, delegation behavior, context policy, review and evaluation
strategy — **and proposing a processor role that does not yet exist**.

Role commissioning likely carries a higher evidence bar than role tuning;
establishing that threshold is part of this milestone.

**Changes remain candidates until independently evaluated.**

## The first self-modifying loop

This is where the system begins proposing changes to itself, and it is therefore
the first milestone where the invariant floor is doing work no human is
duplicating. Two hard preconditions:

- **[M11](11-safety-response.md) must be complete.** A loop that modifies the
  system cannot commission its own watcher.
- **A second judgment source must exist.** The M5 follow-up established that no 7B
  reviewer framing beats an approval bias, and that adding a 7B panel to a
  deterministic gate makes it *worse* (9/10 → 6/10). A tuning loop whose evaluation
  is not above noise will confidently promote noise.

The second precondition is the harder one. It needs a human, an automated check,
or a stronger/independent reviewer model — the last enabled by the planned second
GPU. That moved the second-GPU path from "nice to have" to the gating dependency
for this whole tier. See [`../00-backlog.md`](../00-backlog.md).

## The Goodhart exposure

This is the milestone where a system that adapts its own evaluation criteria could
satisfy its own measurements by redefining what is being measured. The invariant
layer and the frozen baselines are the structural answer
([`04-goodhart-and-adversarial-evaluation.md`](../../30-adaptation-and-evolution/04-goodhart-and-adversarial-evaluation.md)),
and [M14](14-meta-evaluation.md) is where whether they worked gets asked.

## Scope, not a new kind of agent

As with [M10](10-project-level-adaptation.md) and [M14](14-meta-evaluation.md):
the levels differ in scope, evidence, and promotion criteria, not necessarily in
which processor performs them.
