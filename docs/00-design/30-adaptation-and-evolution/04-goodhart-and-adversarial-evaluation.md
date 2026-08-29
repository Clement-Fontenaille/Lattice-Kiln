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

## Frozen baselines

Candidate changes should be compared against reproducible baselines whenever possible.

This prevents the system from silently redefining its own previous state or moving the measurement target during optimization.

## Open question

There will never be a perfect metric for developer value. The goal is therefore not to eliminate Goodhart risk but to make misalignment observable, contestable, and difficult to hide.
