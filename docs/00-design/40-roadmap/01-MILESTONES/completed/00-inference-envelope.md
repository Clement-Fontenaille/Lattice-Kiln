# M0 — Characterize the local inference envelope

**State:** done — 2026-08-30
**Findings:** [entry 1](../../../50-findings/01-m0-inference-envelope.md) — **confirms**
**Execution record:** [`M0-inference-envelope.md`](../../../../50-PROGRESS/archives/M0-inference-envelope.md)
**Experiment:** `experiments/M0-inference-envelope/`

## What this milestone was

The project first needs a factual understanding of what the current machine can
run comfortably.

The outcome should describe usable models, quantization choices, context sizes,
model-switching cost, inference latency, GPU/CPU split, and the practical effect
of running inference alongside the development environment.

This milestone exists to prevent later architectural assumptions from depending on
hardware behavior we have not measured.

## Evidence question

What is the real local inference envelope, and how tight is the constraint the
constrained-intelligence thesis assumes?

## What it answered

**Confirms.** The constraint is real, binary, and sharp-edged.

- 7B at Q4/Q5 up to ~16k context, around 40 tok/s.
- **VRAM fit is a hard binary** with a ~10–20× cliff once the model offloads.
- **Per-role model switching is not viable** on the reference host — which removed
  a whole class of architecture that assumed a different model per processor role.

## What it constrains downstream

The envelope numbers are host-specific, and the design set does not currently
state which of its conclusions depend on them. That statement is owed — see
*hardware as a variable* in [`../../00-backlog.md`](../../00-backlog.md).

The no-switching result is why [M15](../15-cross-generation-comparison.md) owns
per-role model assignment rather than any earlier milestone, and why a second GPU
is the gating dependency for a second judgment source.
