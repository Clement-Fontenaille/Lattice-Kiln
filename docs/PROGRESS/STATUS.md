# Status

_Updated: 2026-08-30_

## Where we are

**MVP target:** Milestones 0 through 5 — a local assistant using ephemeral role-specific processors under a language-model orchestrator, on measured hardware, fully observable, on a safety floor.

**Current milestone:** M0 — Characterize the local inference envelope.

**State:** host inventoried, runtime decided (Ollama of record + llama.cpp spot-checks), protocol written, model matrix pinned to Qwen2.5-Coder 3B/7B/14B on the RTX 2070 SUPER's 8 GB, full harness written (parse-clean, untested). The sweep is blocked only on installing the two runtimes and pulling the GGUFs — an M1 step pulled forward.

## Milestone board

| Milestone | State | Decomposed |
|---|---|---|
| M0 — Local inference envelope | WIP — tasks 1–5 of 8 done | yes — `M0-inference-envelope.md` |
| M1 — Reproducible baseline environment | TODO | provisional — `M1-baseline-environment.md` |
| M2 — Observability foundation | TODO | no — decompose when M0 nears completion |
| M3 — Invariant floor (reduced form for MVP) | TODO | no |
| M4 — Ephemeral processor experiments | TODO | no |
| M5 — Intelligent orchestration experiments | TODO | no |

## Immediate next actions

1. Install Ollama (native Windows) — `winget install Ollama.Ollama` or the installer. Confirm `ollama --version` and that `http://localhost:11434` responds.
2. Install a prebuilt CUDA llama.cpp inside WSL Ubuntu-22.04 (no source build — host has no CUDA toolkit). Put `llama-cli` / `llama-bench` on PATH; `apt install jq`.
3. Fetch the Qwen2.5-Coder GGUFs for the llama.cpp spot-check (7B Q4_K_M + Q5_K_M, 14B Q4_K_M) into `experiments/M0-inference-envelope/models/` (git-ignored). Ollama pulls its own on first run.
4. Run `pwsh experiments/M0-inference-envelope/harness/bench-ollama.ps1`, then `wsl bash .../bench-llamacpp.sh`, then `pwsh .../aggregate.ps1`. Expect first-run script fixes — report errors back.
5. Write the envelope description (into `M0-inference-envelope.md`) and the first findings-log entry.

## Blockers

- **Runtime install + model download.** Steps 1–3 above are operator actions on the host. Everything scriptable for M0 is done and committed.

## Recently done

- Conceptual integration pass (review notes 02–03) — committed `b098e91`.
- Carried notes removed — committed `d80d0e8`.
- Execution cadence, findings log, technical-spec kickoff, milestone rework — committed `b098e91`.
