# Meta-Level Feedback

## TL;DR

The meta loop does not merely improve the improver. It evaluates whether our way of discovering improvement is trustworthy.

> **Motto:** Audit the mechanism that decides what "better" means.

## Motivation

A feedback system can optimize the wrong metric, reward superficial behavior, overfit benchmarks, or repeatedly propose changes that appear beneficial only inside one running instance.

The meta level exists to detect these failures.

## Object of evaluation

The meta loop observes the system-level adaptation process itself.

It asks whether experiments are meaningful, metrics remain aligned with developer value, candidate improvements transfer to independent instances, regressions are detected, and promotion decisions remain reproducible.

## Expected outputs

The meta level may propose changes to benchmark composition, evaluation procedures, experiment design, repetition requirements, promotion criteria, regression testing, or the architecture of the feedback loop.

## Deliberate boundary

The meta loop is not expected to recursively spawn an infinite hierarchy of meta-meta systems.

Its purpose is pragmatic: increase confidence that system evolution is real rather than self-confirming.

Three things keep the boundary from being merely asserted.

The loop asks one generic question — whether the system's self-tuning produces trustworthy improvement in aggregate — rather than a separate meta-question per tunable parameter. A mechanism that can propose changes to a processor's instructions can equally propose changes to its own thresholds; that is self-application of an existing mechanism to a new object, not grounds for a dedicated overseer per parameter.

The chain terminates on something not self-tuned. Frozen baselines and the invariant layer sit outside every loop being judged, which is what prevents the tower from quietly moving its own goalposts.

That termination is less complete than it reads, and the gap should be visible here rather than only where it was found. A frozen baseline fixes the task; it does not fix the accumulated record the system consults while performing it, and that record is an output of the system (`04-goodhart-and-adversarial-evaluation.md`, What a frozen baseline does not freeze). The invariant layer is genuinely outside every loop. The evidence this level reads is not, and no anchor currently available makes it so. What is available is knowing which lineage produced it, which `26-arch-observability` records.

This bears directly on one of the questions above. "Whether candidate improvements transfer to independent instances" is precisely the transfer measurement `23-arch-context-management/02-context-as-experimental-surface.md` defines — a policy evaluated on a corpus it did not shape. That is the sharpest tool this level has, because it is the one comparison whose result is not underwritten by the conditions being audited.

And this level is distinct from the others in scope and evidence requirements rather than necessarily in which processor performs it. The separation belongs to invocation, not to agent identity.

## Open question

The project must determine which evaluation anchors should remain externally fixed enough to prevent moving goalposts, and which should themselves be evolvable as our understanding of useful performance improves.
