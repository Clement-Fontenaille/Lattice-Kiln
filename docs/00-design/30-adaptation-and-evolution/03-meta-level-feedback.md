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

## Open question

The project must determine which evaluation anchors should remain externally fixed enough to prevent moving goalposts, and which should themselves be evolvable as our understanding of useful performance improves.
