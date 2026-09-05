# M1 — Reproducible baseline development environment

**State:** done — 2026-08-30. One deliverable still owed (clean-machine replay).
**Findings:** [entry 2](../../../50-findings/02-m1-baseline-environment.md) — inconclusive
**Execution record:** [`M1-baseline-environment.md`](../../../../50-PROGRESS/archives/M1-baseline-environment.md)
**Experiment:** `experiments/M1-baseline-environment/`

## What this milestone was

Create the scripted Windows/WSL/local-model/VS Code/Cline development
environment.

The baseline should be intentionally boring, stable, and observable. Its job is to
provide a known reference installation that later generations can improve upon.

## Evidence question

Can the baseline be reconstructed from scripts without manual repair, and where
does reproducibility actually break?

## What it answered

**Inconclusive**, and the reason is the interesting part.

The scripted surface verifies green in place — a full `-VerifyOnly` run over six
idempotent provisioning steps passes. But *verifying green on the machine that was
already provisioned* is not the same test as building from nothing, and six
manual or host-specific breaks were enumerated rather than fixed.

The definitive test — a clean-machine replay — was not run, because it needs a
second controlled machine. Until it runs, this milestone's evidence question has
an honest "we do not know yet" rather than an answer.

## Still owed

- **Clean-machine replay.** Tracked in [`../../00-backlog.md`](../../00-backlog.md);
  gated on hardware, not on effort.
- **Editor-agent frontend choice.** Cline was taken for the MVP without weighing a
  `config.yaml`-first alternative. Owner: the eventual bootstrapper design.

Both are in the backlog rather than holding this milestone open, because neither
blocks anything downstream and the first cannot be scheduled.
