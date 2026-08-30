# Status

_Updated: 2026-08-30_

## Where we are

**MVP target:** Milestones 0 through 5 — a local assistant using ephemeral role-specific processors under a language-model orchestrator, on measured hardware, fully observable, on a safety floor.

**Current milestone:** M0 — Characterize the local inference envelope.

**State:** just started. Task breakdown drafted in `M0-inference-envelope.md`. The measurement protocol and harness are the next build step. Two decisions need the operator's input before the sweep can run (see blockers).

## Milestone board

| Milestone | State | Decomposed |
|---|---|---|
| M0 — Local inference envelope | WIP | yes — `M0-inference-envelope.md` |
| M1 — Reproducible baseline environment | TODO | provisional — `M1-baseline-environment.md` |
| M2 — Observability foundation | TODO | no — decompose when M0 nears completion |
| M3 — Invariant floor (reduced form for MVP) | TODO | no |
| M4 — Ephemeral processor experiments | TODO | no |
| M5 — Intelligent orchestration experiments | TODO | no |

## Immediate next actions

1. Resolve the two M0 blockers below.
2. Write the M0 measurement protocol (`experiments/M0-inference-envelope/PROTOCOL.md`).
3. Build the harness that runs the protocol and emits structured results.
4. Run the model × quantization × context sweep.
5. Write the envelope description and the first findings-log entry.

## Blockers needing operator input

- **Inference runtime.** Which local runtime to measure against and build M1 on — Ollama, llama.cpp directly, LM Studio, or another. This shapes the harness and the model-switch-cost measurement.
- **Host and execution target.** GPU model and VRAM, system RAM, and whether inference runs under native Windows or WSL. This sets the model and quantization matrix. The harness can auto-detect some of this, but the matrix needs to be bounded before the sweep.

## Recently done

- Conceptual integration pass (review notes 02–03) — committed `b098e91`.
- Carried notes removed — committed `d80d0e8`.
- Execution cadence, findings log, technical-spec kickoff, milestone rework — committed `b098e91`.
