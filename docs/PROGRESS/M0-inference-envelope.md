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
| 1 | Inventory the host — CPU, RAM, GPU + VRAM, disk, OS/WSL layout | DONE | `harness/detect-host.ps1` run; `results/host.json` captured. Summary below. |
| 2 | Choose the inference runtime | DONE | **Both**: Ollama as runtime of record (drives M1 and the assistant), llama.cpp for M0 fidelity spot-checks on the working-default models. |
| 3 | Fix the candidate model set | DONE | Pinned matrix below, bounded by 8 GB VRAM. |
| 4 | Write the measurement protocol | DONE | `experiments/M0-inference-envelope/PROTOCOL.md`. |
| 5 | Build the harness | DONE (untested) | `models.json`, `bench-ollama.ps1`, `bench-llamacpp.sh`, `aggregate.ps1`. All parse; none run against a live runtime yet. |
| 6 | Run the sweep | BLOCKED | Needs Ollama (native) + a prebuilt CUDA llama.cpp (WSL) installed, plus the GGUFs. First run will surface script fixes. |
| 7 | Write the envelope description | TODO | Into this document. |
| 8 | Findings-log entry | TODO | Verdict against the constrained-intelligence thesis. |

## Host summary (2026-08-30)

Full record: `experiments/M0-inference-envelope/results/host.json`.

| | |
|---|---|
| GPU | NVIDIA RTX 2070 SUPER, **8 GB VRAM**, driver 581.80 (Turing; no FP8) |
| CPU | AMD FX-8300 — 2012 Piledriver, 4 modules / 8 threads, 3.3 GHz. Weak single-thread. |
| RAM | 11.9 GB total |
| Disk | 659 GB free on C: |
| OS / WSL | Windows 10 19045; WSL2 Ubuntu-22.04 present, stopped |
| Runtimes | neither Ollama nor llama.cpp installed yet |
| CUDA toolkit | absent — llama.cpp in WSL should use a prebuilt CUDA binary, not a source build |

The envelope is tight on two axes at once: 8 GB VRAM caps model size, and the
FX-8300 makes any CPU offload expensive. The measurements that matter most are
therefore the partial-offload cases (14B) and the concurrent-load delta.

## Pinned model matrix

All Qwen2.5-Coder unless noted — it is the coding-capable line with good small
sizes. Sizes approximate for GGUF.

| Slot | Model | Quants | GPU fit (8 GB) | Purpose |
|---|---|---|---|---|
| Floor | Qwen2.5-Coder-3B | Q4_K_M (~2.0 GB), Q8_0 (~3.3 GB) | full, large context | fast baseline |
| Default | Qwen2.5-Coder-7B | Q4_K_M (~4.7 GB), Q5_K_M (~5.4 GB), Q8_0 (~8.1 GB) | Q4/Q5 full; Q8 expected to spill | expected working default |
| Stretch | Qwen2.5-Coder-14B | Q4_K_M (~9.0 GB) | partial offload — will not fully fit | ceiling: how much does offload cost on this CPU |
| Ceiling (optional) | Qwen3-30B-A3B (MoE) | Q4_K_M (~18 GB) | out — exceeds RAM+VRAM | record as `skipped: insufficient memory` unless a smaller MoE is substituted |

Instruct/base: use the instruct-tuned variants throughout.
Context-fill points per `PROTOCOL.md`: 512 / 4k / 16k / 32k / model max, skipping
what does not fit and recording the skip.

## Metrics, repetition, result schema

All defined in `experiments/M0-inference-envelope/PROTOCOL.md`. That document is
the contract; the harness implements it.

## Log

- 2026-08-30 — milestone decomposed; blockers raised for runtime and host details.
- 2026-08-30 — runtime decided (Both: Ollama of record + llama.cpp spot-checks). Protocol written. Host-detection script written and run: RTX 2070 SUPER 8 GB / FX-8300 / 11.9 GB RAM. Model matrix pinned to Qwen2.5-Coder 3B/7B/14B. Tasks 1–4 done.
- 2026-08-30 — harness written (tasks 5): `models.json`, `bench-ollama.ps1`, `bench-llamacpp.sh`, `aggregate.ps1`. All parse-clean, none run yet. Sweep now blocked only on installing Ollama + a prebuilt CUDA llama.cpp and pulling the GGUFs.
