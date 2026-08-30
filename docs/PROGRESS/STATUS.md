# Status

_Updated: 2026-08-30_

## Where we are

**MVP target:** Milestones 0 through 5 — a local assistant using ephemeral role-specific processors under a language-model orchestrator, on measured hardware, fully observable, on a safety floor.

**Current milestone:** M2 — Observability foundation.

**State:** M0 complete — the local inference envelope is measured and written up
(`M0-inference-envelope.md`), with findings-log entry 1 (verdict: *confirms* the
constrained-intelligence thesis; the constraint is VRAM-fit as a hard binary with
a ~10–20× offload cliff, working default = 7B Q4/Q5 at ≤16k context, model-switch
cost 17–30 s). M2 is being decomposed and its spec doc (`10-technical/02-observability-event-model.md`) drafted next, per the execution-cadence backlog.

## Milestone board

| Milestone | State | Decomposed |
|---|---|---|
| M0 — Local inference envelope | **DONE** (2026-08-30) — findings-log entry 1 | yes — `M0-inference-envelope.md` |
| M1 — Reproducible baseline environment | TODO — `setup/` scripts from M0 are its seed | provisional — `M1-baseline-environment.md` |
| M2 — Observability foundation | **WIP** — decomposing now | `M2-observability-foundation.md` |
| M3 — Invariant floor (reduced form for MVP) | TODO | no |
| M4 — Ephemeral processor experiments | TODO | no |
| M5 — Intelligent orchestration experiments | TODO | no |

## Immediate next actions

1. Decompose M2 into tasks — `M2-observability-foundation.md`.
2. Draft `10-technical/02-observability-event-model.md` (v0, many open contracts):
   pin invocation identity, the realized-effect record, the safety-intervention
   outcome category, and per-actor / per-intent sequence reconstructability. It
   binds to the effect vocabulary (`10-technical/01-effect-vocabulary.md`).
3. Carry forward from M0: the event model should record model/quant per
   invocation and whether inference was offloaded (predicts latency 10–20×).

## Blockers

- None. M0's runtime-install blockers are resolved (Ollama native + llama.cpp
  built from source in WSL via apt `nvidia-cuda-toolkit`; see
  `experiments/M0-inference-envelope/setup/README.md`).

## Recently done

- **M0 executed and closed** — harness bugs fixed on first live run, Ollama
  matrix swept (staged), llama.cpp cross-check, concurrent/drift passes, envelope
  description + findings-log entry 1. Commits `b587993`..`6400fa3` and the
  write-up commit.
- Conceptual integration pass (review notes 02–03) — committed `b098e91`.
- Execution cadence, findings log, technical-spec kickoff, milestone rework — committed `b098e91`.
