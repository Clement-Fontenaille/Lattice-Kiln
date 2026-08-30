# Status

_Updated: 2026-08-30_

## Where we are

**MVP target:** Milestones 0 through 5 — a local assistant using ephemeral role-specific processors under a language-model orchestrator, on measured hardware, fully observable, on a safety floor.

**Current milestone:** M1 — Reproducible baseline development environment.

**State:** M0 complete — the local inference envelope is measured and written up
(`M0-inference-envelope.md`), with findings-log entry 1 (verdict: *confirms* the
constrained-intelligence thesis; the constraint is VRAM-fit as a hard binary with
a ~10–20× offload cliff, working default = 7B Q4/Q5 at ≤16k context, model-switch
cost 17–30 s). M2's spec doc (`10-technical/02-observability-event-model.md`, v0)
is written ahead per the execution-cadence backlog (current + 1). Execution now
moves to M1: turn the M0 `setup/` scripts into a clean-machine-reconstructable
baseline with a manifest.

## Milestone board

| Milestone | State | Decomposed |
|---|---|---|
| M0 — Local inference envelope | **DONE** (2026-08-30) — findings-log entry 1 | yes — `M0-inference-envelope.md` |
| M1 — Reproducible baseline environment | **WIP** — `setup/` scripts from M0 are its seed | `M1-baseline-environment.md` (being firmed up) |
| M2 — Observability foundation | TODO — spec v0 written ahead | `M2-observability-foundation.md` |
| M3 — Invariant floor (reduced form for MVP) | TODO | no |
| M4 — Ephemeral processor experiments | TODO | no |
| M5 — Intelligent orchestration experiments | TODO | no |

## Immediate next actions

1. Firm up `M1-baseline-environment.md` from provisional, folding in the M0
   runtime decisions (Ollama native Windows; llama.cpp CUDA built in WSL via apt
   `nvidia-cuda-toolkit`) and the `setup/` scripts already in the repo.
2. Consolidate `experiments/M0-inference-envelope/setup/` into an environment
   provisioning set with pinned versions/digests and an entry point.
3. Write the environment manifest (proto-bootstrap artifact) and run the
   clean-ish reconstruction test — recording every manual repair as a finding.

## Blockers

- None. M0's runtime-install blockers are resolved (Ollama native + llama.cpp
  built from source in WSL via apt `nvidia-cuda-toolkit`; see
  `experiments/M0-inference-envelope/setup/README.md`).

## Post-MVP rework backlog (end of M5)

- **Hardware as a variable.** M0 and M1 were characterised against one host.
  Define the replayable procedure to re-bootstrap the environment and
  re-characterise the inference envelope on different hardware, and identify what
  in the design set is allowed to depend on host-specific envelope numbers. See
  `40-roadmap/02-open-questions-register.md` → Bootstrapping, and findings-log
  entry 1.

## Recently done

- **M0 executed and closed** — harness bugs fixed on first live run, Ollama
  matrix swept (staged), llama.cpp cross-check, concurrent/drift passes, envelope
  description + findings-log entry 1. Commits `b587993`..`6400fa3` and the
  write-up commit.
- Conceptual integration pass (review notes 02–03) — committed `b098e91`.
- Execution cadence, findings log, technical-spec kickoff, milestone rework — committed `b098e91`.
