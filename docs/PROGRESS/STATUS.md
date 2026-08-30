# Status

_Updated: 2026-08-30_

## Where we are

**MVP target:** Milestones 0 through 5 — a local assistant using ephemeral role-specific processors under a language-model orchestrator, on measured hardware, fully observable, on a safety floor.

**Current milestone:** M0 — Characterize the local inference envelope.

**State:** host inventoried, runtime decided (Ollama of record + llama.cpp spot-checks), protocol written, model matrix pinned to Qwen2.5-Coder 3B/7B/14B on the RTX 2070 SUPER's 8 GB. Bench scripts are the next build step; the sweep is blocked only on installing the two runtimes (an M1 step pulled forward).

## Milestone board

| Milestone | State | Decomposed |
|---|---|---|
| M0 — Local inference envelope | WIP — tasks 1–4 of 8 done | yes — `M0-inference-envelope.md` |
| M1 — Reproducible baseline environment | TODO | provisional — `M1-baseline-environment.md` |
| M2 — Observability foundation | TODO | no — decompose when M0 nears completion |
| M3 — Invariant floor (reduced form for MVP) | TODO | no |
| M4 — Ephemeral processor experiments | TODO | no |
| M5 — Intelligent orchestration experiments | TODO | no |

## Immediate next actions

1. Write the M0 bench scripts — `bench-ollama.ps1` (all matrix cells) and `bench-llamacpp.sh` (7B/14B spot-checks), plus `models.json` and an aggregator.
2. Install the runtimes: Ollama (native Windows), and a prebuilt CUDA llama.cpp in WSL Ubuntu-22.04. Pull the Qwen2.5-Coder GGUFs.
3. Run the model × quantization × context sweep.
4. Write the envelope description and the first findings-log entry.

## Blockers

- **Runtime install.** Ollama and llama.cpp are not yet on the host. Step 2 above — an M1 install task pulled forward because M0 needs it. Everything else for M0 is unblocked.

## Recently done

- Conceptual integration pass (review notes 02–03) — committed `b098e91`.
- Carried notes removed — committed `d80d0e8`.
- Execution cadence, findings log, technical-spec kickoff, milestone rework — committed `b098e91`.
