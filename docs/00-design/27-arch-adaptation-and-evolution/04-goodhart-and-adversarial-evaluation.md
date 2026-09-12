# Goodhart Risk and Adversarial Evaluation

## TL;DR

Any metric that becomes an optimization target can stop representing what we actually care about.

> **Motto:** Never let success be defined by the component trying to win.

## Motivation

A system can increase task success by making tasks trivial. It can reduce correction rate by avoiding ambitious changes. It can improve benchmark scores by specializing to the benchmark. It can shorten reasoning by becoming prematurely confident.

All of these may look like improvement under a narrow metric.

## Adversarial stance

Evaluation should actively look for ways a candidate improvement could be misleading.

A reviewer should not merely ask whether a new strategy performs well. It should ask what useful behavior may have been sacrificed to obtain that performance.

## Independent signals

Objective tests, human acceptance, regression behavior, resource usage, transfer to unseen work, and independent evaluators provide different views of system quality.

No single signal is assumed to be sufficient.

## Evaluator independence as a configuration dimension

Independent evaluation loses much of its value when the evaluator and the optimizer share the same underlying model: what results is correlated blind spots rather than genuine independence.

This is not a defect requiring an immediate architectural fix. It is a dimension for experiments to probe once model diversity and evaluation infrastructure actually exist. Which model performs planning, implementation, or evaluation is one more thing feedback can rearrange, informed by evidence about which pairings produce genuinely independent judgment.

It belongs naturally around the system-level tuning milestone rather than earlier, because comparing model assignments requires multiple models to compare.

The exception is any role whose entire purpose is to watch a loop for drift. There, independence is a structural requirement rather than an experimental variable, and it is settled where the invariant layer is settled.

## Frozen baselines

Candidate changes should be compared against reproducible baselines whenever possible.

This prevents the system from silently redefining its own previous state or moving the measurement target during optimization.

The same reasoning extends past benchmarks. If a baseline must be frozen so that measurement stays meaningful, the goals the measurement serves must be frozen for the same reason and more strongly — a system that can revise what it is for can satisfy any metric by redefinition. That generalization is the invariant layer, which holds goals and hard constraints outside the reach of every feedback loop rather than only outside the reach of a single comparison.

**What a frozen baseline does not freeze.** It fixes the task. It does not fix the knowledge the system reads while solving that task, and that record is a product of the system rather than something found: every artifact in it exists because some policy, some model and some configuration caused a crossing that produced it (`23-arch-context-management/02-context-as-experimental-surface.md`). So the same frozen suite, run by the same configuration against two different accumulated corpora, is not the same measurement.

This does not defeat frozen baselines. It bounds what they establish, and the remedy is the one `10-foundations/03` already prescribes for a single claim under the name Scope: record the conditions as they accumulate rather than reconstruct them afterwards, which `26-arch-observability` now does. A comparison then at least knows which lineage it is reading, even when it cannot neutralise it.

## Open question

There will never be a perfect metric for developer value. The goal is therefore not to eliminate Goodhart risk but to make misalignment observable, contestable, and difficult to hide.
