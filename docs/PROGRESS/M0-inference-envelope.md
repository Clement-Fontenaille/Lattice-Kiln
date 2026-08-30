# M0 — Characterize the Local Inference Envelope

**Milestone:** `40-roadmap/01-milestones.md` → Milestone 0
**Evidence question:** what is the real local inference envelope, and how tight is the constraint the constrained-intelligence thesis assumes?
**State:** WIP

## What "done" looks like

A written description of the envelope covering:

- which models run comfortably, at which quantizations;
- usable context sizes per model and quantization, and where they stop fitting;
- model-switch cost (unload plus load);
- prefill and generation throughput, and latency to first token;
- GPU/CPU offload behaviour and the split actually used;
- the practical effect of running inference alongside the development environment (editor, language servers, build tools).

Plus a findings-log entry giving the verdict against the constrained-intelligence thesis: is the constraint as tight as the design set assumes, tighter, or looser.

All measurements reconstructable from stored structured results and the harness that produced them.

## Where the work lives

- Protocol and harness: `experiments/M0-inference-envelope/`
- Structured results: `experiments/M0-inference-envelope/results/`
- Narrative outcome: appended to this document, then distilled into the findings log.

## Task breakdown

| # | Task | State | Notes |
|---|---|---|---|
| 1 | Inventory the host — CPU, RAM, GPU + VRAM, disk, OS/WSL layout | TODO | Harness can capture most of this automatically. |
| 2 | Choose the inference runtime | BLOCKED | Needs operator input. Candidates: Ollama, llama.cpp, LM Studio. Decision recorded in M1 environment notes, referenced here. |
| 3 | Fix the candidate model set | TODO | Proposal below. Needs task 1 to bound it. |
| 4 | Write the measurement protocol | TODO | `PROTOCOL.md` — metrics, method, repetitions, result schema. Runtime-agnostic where possible. |
| 5 | Build the harness | TODO | Runs the protocol across the matrix, emits one structured record per run. |
| 6 | Run the sweep | BLOCKED | Depends on tasks 2–5 and operator hardware. |
| 7 | Write the envelope description | TODO | Into this document. |
| 8 | Findings-log entry | TODO | Verdict against the constrained-intelligence thesis. |

## Candidate model set (proposal, pending task 1)

A small spread across capability and size, weighted toward coding-capable models:

- one ~3B model (floor case — fast, fits anything);
- one ~7–8B model (expected working default);
- one ~13–14B model (stretch for the working default);
- one larger or mixture-of-experts model if VRAM allows (ceiling case).

Each measured at Q4_K_M and Q8_0 at minimum; add Q5_K_M for the working-default candidates.

Concrete model names to be pinned once the runtime and VRAM are known.

## Metrics the protocol must cover

- Model load time and unload time; combined switch cost.
- Prefill throughput (tokens/sec) at several context fills — e.g. 512, 4k, 16k, 32k, and the model's stated maximum.
- Generation throughput (tokens/sec), steady state.
- Latency to first token.
- Largest context that loads and runs without spilling past VRAM into unacceptable slowdown.
- Offload split actually used (layers on GPU vs CPU) at each configuration.
- Sustained-load behaviour — throughput drift and thermal or memory pressure over a longer run.
- Concurrent-load delta — the same generation measured with the development environment idle vs active (editor plus language server plus a build running).

## Repetition

Each configuration measured enough times to see variance, not once. Exact count set in the protocol against run cost, but no single-run numbers in the final description.

## Log

- 2026-08-30 — milestone decomposed; blockers raised for runtime and host details.
