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
| 5 | Build the harness | DONE | `models.json`, `bench-ollama.ps1`, `bench-load-extra.ps1`, `bench-switch.ps1`, `bench-llamacpp.sh`, `aggregate.ps1`. First live run surfaced three measurement bugs (prefill cache contamination, EOS-truncated generation window, `ollama pull` abort) — all fixed. |
| 6 | Run the sweep | DONE | Ollama matrix run staged; 7B Q8 and 14B large-context cells recorded as `skipped` (offload-bound, sub-5 tok/s — see below). llama.cpp cross-check on 7B Q4 validates Ollama; 14B llama.cpp abandoned as intractable to benchmark. `results/summary.md` regenerated. |
| 7 | Write the envelope description | DONE | Below. |
| 8 | Findings-log entry | DONE | `40-roadmap/05-findings-log.md` entry 1 — verdict: **confirms** (constraint is binding and cliff-shaped). |

## Setup and reproduction

`experiments/M0-inference-envelope/setup/` holds the runtime-provisioning scripts
(WSL CUDA llama.cpp build, GGUF fetch) and `setup/README.md` gives the full run
order with the host-specific constants called out. A general cross-host
provisioning system is M1's deliverable; these are its seed.

## Envelope description (2026-08-30)

All numbers from `results/summary.md`, reconstructable from `results/runs/*.json`.
Runtime of record: Ollama 0.33.2. Cross-check: llama.cpp `f1793c1` (CUDA sm_75).

### The shape of it

The host has **one binding constraint, and it is a cliff, not a slope**: a model
that fits entirely in the 8 GB of VRAM runs well; the moment any weights or KV
cache spill to system RAM, generation drops from 40–70 tok/s to 1–5 tok/s. The
FX-8300 makes CPU offload roughly 10–20× slower than the resident case, so there
is no usable middle ground.

### Models and quantizations

| Model / quant | On-disk | Fits 8 GB? | gen tok/s (512 → 32k fill) | Verdict |
|---|---|---|---|---|
| Qwen2.5-Coder-3B Q4_K_M | ~1.9 GB | yes, with room | 73 → 67 | comfortable everywhere on throughput |
| Qwen2.5-Coder-3B Q8_0 | ~3.3 GB | yes | 63 → 53 | comfortable everywhere on throughput |
| Qwen2.5-Coder-7B Q4_K_M | ~4.7 GB | yes to 16k | 52 → 45 (16k), **5.0** (32k) | working default; 32k KV spills |
| Qwen2.5-Coder-7B Q5_K_M | ~5.4 GB | yes to 16k | 45 → 41 (16k), **1.3** (32k) | working default; less 32k headroom than Q4 |
| Qwen2.5-Coder-7B Q8_0 | ~8.1 GB | no | ~4 (even at 512) | out — offload-bound |
| Qwen2.5-Coder-14B Q4_K_M | ~9.0 GB | no | 2.3 (512), 1.4 (4k) | out — offload-bound; llama.cpp could not benchmark it at all |

Comfortable = clears all three PROTOCOL thresholds (gen ≥ 15 tok/s, prompt-eval
≤ 2000 ms at 4k, switch ≤ 5000 ms) at that context fill.

### Usable context

- **3B** at either quant holds 67 tok/s all the way to 32k. It is bounded by
  **prefill latency**, not generation: prompt-eval is 0.2 s at 512, 1.3 s at 4k,
  5.2 s at 16k, 12.8 s at 32k. Interactive to ~4k; usable-with-a-wait beyond.
- **7B Q4/Q5** are fully resident and fast (44–52 tok/s) up to **16k** (prompt-eval
  ~10 s there). At **32k the KV cache pushes total footprint past 8 GB** and the
  cell collapses (5.0 tok/s Q4, 1.3 tok/s Q5; prompt-eval 40–110 s). The 16k→32k
  step is the cliff edge for the working-default model.
- VRAM resident at the top of the usable range: 7B Q4 ~5.2 GB at 16k, 7B Q5
  ~5.9 GB at 16k. The ~2–3 GB of remaining headroom is what the 32k KV cache
  exhausts.

### Latency to first token / prefill

Prefill throughput is 2300–3000 tok/s for the 3B, ~1400–1520 tok/s for resident
7B, and falls to 100–600 tok/s (3B unaffected; 7B/14B offloaded) once spill
begins. Time-to-first-token at 4k context: ~1.3 s (3B), ~2.1 s (7B) — the 7B just
misses the 2 s ceiling. At 16k it is 5–10 s; at 32k, tens of seconds to minutes.

### Model-switch cost

Unload is cheap (**86–228 ms**). The cost is the cold load of the incoming
model: **3B ~17–18 s, 7B ~30 s, 14B ~54 s** (warm disk cache; the very first
load of a model from cold disk was ~77 s). `switch_ms` is therefore 17–30 s for
the pairs measured — **3–6× over the 5 s orchestration threshold**. Switching
7B → 14B crashed the Ollama inference subprocess (`CUDA error: shared object
initialization failed`); 14B loads are marginal even in isolation.

Implication for orchestration: per-role **model** switching is expensive here.
Role differentiation by prompt within one resident model is strongly preferred;
an orchestrator that swaps models pays 20–30 s each time.

### GPU / CPU offload

Ollama reports `size_vram == size` for every resident cell (3B both quants; 7B
Q4/Q5 up to 16k) — i.e. **100% GPU, no offload** in the usable envelope. Every
"out" case is offload-bound. llama.cpp confirms the resident 7B numbers
(prefill 1540 vs Ollama 1544 at 512; gen 55 vs 52) — agreement within 7%,
validating Ollama as runtime of record. The intended llama.cpp `-ngl` sweep on
14B to trace the offload-cost curve **could not be run**: `llama-bench` did not
complete a single iteration in 180 s even at `-ngl 0 -p 128 -n 32`, because the
9 GB mmap page-in over WSL2 disk plus FX-8300 dequant is itself the bottleneck.
That failure is a data point: 14B is not merely slow here, it is impractical to
even measure.

### Running alongside the development environment

`concurrent_delta`, 7B Q5 at 4k, against 8 synthetic CPU workers + RAM churn
standing in for editor + language server + build: **idle 44.0 → concurrent 42.5
tok/s, −3.4%**. A fully-resident model barely feels host CPU pressure, because
generation runs on the GPU. (For an offloaded model the question is moot — it is
already unusable.) So: the dev environment is not a meaningful tax **as long as
the model fits**.

### Sustained generation

`sustained_drift`, 7B Q5 at 4k, 11 minutes continuous: **first-minute median
44.4 → last-minute median 39.5 tok/s, −11%**. Mild, monotonic — consistent with
GPU thermal / clock settling under sustained load. A long session loses ~10% off
its opening rate.

### Deviations from PROTOCOL taken during the run

- 14B Q4 recorded at 3 repetitions, not 5 (offload-bound, minutes per rep).
- 7B Q8 measured at 512/4096 only; 16k/32k recorded `skipped` (both measured
  fills already < 5 tok/s — out of envelope, larger fills add no information).
- 14B Q4 measured at 512/4096 only; 16k/32k recorded `skipped` (same reason).
- llama.cpp spot-check: 7B Q5_K_M deferred (one quant cross-checks throughput);
  14B `-ngl` sweep recorded `skipped` (intractable, see above).
- `gen_tok_s` is a whole-response average (Ollama exposes no per-token timing);
  the generation prompt is a fixed long-form task run to `num_predict` = 320 so
  the average sits in steady state.

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
- 2026-08-30 — sweep executed. First live run surfaced and fixed three harness bugs (prefill KV-cache contamination, EOS-truncated generation window, `ollama pull` aborting under `ErrorActionPreference=Stop`). Added `bench-load-extra.ps1` (concurrent_delta + sustained_drift) and `bench-switch.ps1`. llama.cpp CUDA built from source in WSL via apt `nvidia-cuda-toolkit` (no prebuilt Linux CUDA binary exists); spot-check runs on `llama-bench -o json`. Setup scripts promoted to `setup/`. Envelope description written above; findings-log entry 1 written. **Tasks 6–8 done — M0 complete.**
