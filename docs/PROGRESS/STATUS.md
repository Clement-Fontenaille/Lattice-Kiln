# Status

_Updated: 2026-08-30_

## Where we are

**MVP target:** Milestones 0 through 5 — a local assistant using ephemeral role-specific processors under a language-model orchestrator, on measured hardware, fully observable, on a safety floor.

**Current milestone:** M2 — Observability foundation.

**State:** M0 and M1 complete (findings-log entries 1 and 2). M0: local inference
envelope measured — VRAM-fit is a hard binary with a ~10–20× offload cliff,
working default 7B Q4/Q5 at ≤16k, switch cost 17–30 s. M1: baseline environment
scripted (`experiments/M1-baseline-environment/` — manifest + 6-step provisioning
orchestrator), verifies green in place; the definitive clean-machine replay is
deferred to the post-MVP rework. M2's spec doc
(`10-technical/02-observability-event-model.md`, v0) is written; execution now
moves to M2.

## Milestone board

| Milestone | State | Decomposed |
|---|---|---|
| M0 — Local inference envelope | **DONE** (2026-08-30) — findings-log entry 1 | yes — `M0-inference-envelope.md` |
| M1 — Reproducible baseline environment | **DONE** (2026-08-30) — findings-log entry 2 (verdict inconclusive; clean-machine replay owed) | yes — `M1-baseline-environment.md` |
| M2 — Observability foundation | **WIP** — spec v0 written; recorder next | `M2-observability-foundation.md` |
| M3 — Invariant floor (reduced form for MVP) | TODO | no |
| M4 — Ephemeral processor experiments | TODO | no |
| M5 — Intelligent orchestration experiments | TODO | no |

## Immediate next actions

1. M2 task 2 — decide the record store shape (JSONL per run, illustrative).
2. M2 tasks 3–5 — concrete record schemas for invocation identity + lineage, the
   realized-effect record, and the safety-intervention outcome category, as
   illustrative artifacts under `experiments/M2-observability-foundation/`.
3. M2 task 6 — a minimal standalone recorder emitting the four record kinds, with
   a self-test on a synthetic run (per-actor / per-intent history reconstructs).
   Wiring it into a real run and the reconstruction check (task 7) wait for M4.

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
- **Editor-agent frontend choice.** M1 names Cline. M1 finding 1: Cline's config
  is file-based JSON but the schema is undocumented and UI-first, so the baseline
  needs a one-time manual capture step. Weigh a `config.yaml`-first, documented
  alternative (e.g. Continue.dev) at the rework. Not an M1 change — Cline stays
  for the MVP, worked around by capture-and-replay of its settings JSON. The
  project runs its own orchestrator loop from M5 on, so this frontend is MVP
  scaffolding, not a long-term dependency.

## Recently done

- **M1 executed and closed** — `experiments/M1-baseline-environment/`: declarative
  manifest + `provision.ps1` (6 idempotent steps: WSL/GPU, apt+pip prereqs,
  llama.cpp+GGUF via M0 scripts, Ollama, models, VS Code+Cline). Full
  `-VerifyOnly` run green. Cline config located (`~/.cline/data/`), templates
  captured + curated. Findings-log entry 2.
- **M0 executed and closed** — harness bugs fixed on first live run, Ollama
  matrix swept (staged), llama.cpp cross-check, concurrent/drift passes, envelope
  description + findings-log entry 1.
- Conceptual integration pass (review notes 02–03) — committed `b098e91`.
- Execution cadence, findings log, technical-spec kickoff, milestone rework — committed `b098e91`.
