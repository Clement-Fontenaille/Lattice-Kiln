# M0 Measurement Protocol

Defines what is measured, how, and in what form results are stored. The harness
scripts implement this document; if they diverge, this document wins.

## Runtimes

- **Ollama** — runtime of record. Every model in the matrix is measured here.
- **llama.cpp** — fidelity spot-check. Only the working-default candidates
  (~7–8B and ~13–14B) are measured here, to cross-check Ollama's numbers and to
  expose the offload split and KV-cache behaviour Ollama hides.

Both are driven headless. Ollama via its HTTP API (`/api/generate`,
`/api/show`). llama.cpp via `llama-bench` plus a scripted `llama-cli` run for
the metrics `llama-bench` does not cover.

## Matrix

`model × quantization × context-fill`.

- **model** — the candidate set fixed in `harness/models.json` (proposal in the
  M0 progress doc; pinned once host VRAM is known).
- **quantization** — `Q4_K_M` and `Q8_0` for all; add `Q5_K_M` for the
  working-default candidates.
- **context-fill** — 512, 4096, 16384, 32768 tokens, and the model's stated
  maximum. Skip any fill the model or the hardware cannot hold; record it as
  `skipped` with a reason, not as a gap.

## Metrics

Per matrix cell:

| Metric | Definition | Method |
|---|---|---|
| `load_ms` | cold load: model not resident → ready to generate | unload all, time first token request minus generation of 1 token |
| `unload_ms` | resident → evicted | Ollama: `keep_alive: 0` then poll `/api/ps`; llama.cpp: process exit |
| `switch_ms` | `unload_ms` of model A + `load_ms` of model B | measured as a pair, adjacent models in the matrix |
| `ttft_ms` | prompt submitted → first token emitted | streaming response, timestamp first chunk |
| `prefill_tok_s` | prompt tokens ÷ (ttft − load), at each context-fill | derived |
| `gen_tok_s` | steady-state generation throughput | generate 256 tokens after a 32-token warmup discard |
| `max_context_ok` | largest context-fill that loads and holds `gen_tok_s` above the floor | sweep fills upward until it fails the floor or OOMs |
| `offload` | GPU layers / total layers, and VRAM resident | llama.cpp: parse `llama.cpp` load log; Ollama: `/api/ps` `size_vram` vs `size` |
| `sustained_drift` | `gen_tok_s` at minute 1 vs minute 10 of continuous generation | one long run per working-default model at Q5_K_M |
| `concurrent_delta` | `gen_tok_s` with dev env idle vs active | active = VS Code open on this repo + one language server + a `cargo`/`npm` build running |

## "Comfortable" thresholds

Used only to classify the envelope, not to gate measurement:

- `gen_tok_s` floor for interactive use: **15 tok/s**.
- `ttft_ms` ceiling for interactive use: **2000 ms** at 4k context.
- `switch_ms` tolerable for orchestration: **5000 ms**.

A model/quant is "comfortable" at a context-fill if it clears all three there.
These numbers are provisional and may be revised in the findings entry.

## Repetition

- Latency and throughput metrics: **5 runs** per cell, report median and
  min–max. Discard the first run of each cell (cache warmup).
- `sustained_drift` and `concurrent_delta`: **2 runs** each (expensive).
- Host inventory: once.

## Result storage

`results/` in this folder. Committed — results are evidence.

- `results/host.json` — one object, from `detect-host.ps1`.
- `results/runs/<runtime>__<model>__<quant>__<fill>__<n>.json` — one object per
  run, schema below.
- `results/summary.md` — generated aggregate table; regenerated, not hand-edited.

### Run record schema

```json
{
  "schema": "m0-run/1",
  "runtime": "ollama | llama.cpp",
  "runtime_version": "string",
  "model": "string",
  "quant": "Q4_K_M | Q5_K_M | Q8_0",
  "context_fill": 4096,
  "repetition": 1,
  "timestamp": "ISO-8601",
  "host_ref": "sha256 of host.json",
  "metrics": {
    "load_ms": 0, "unload_ms": 0, "ttft_ms": 0,
    "prefill_tok_s": 0.0, "gen_tok_s": 0.0,
    "gpu_layers": 0, "total_layers": 0, "vram_resident_mb": 0
  },
  "status": "ok | skipped | oom | error",
  "note": "string"
}
```

Metrics absent for a given runtime (e.g. `gpu_layers` on Ollama when
unavailable) are `null`, not `0`.

## Reconstructability

Every number in the envelope description must trace to run records here, and
every run record carries `host_ref` and `runtime_version`. The harness and this
protocol are committed together so a run can be repeated.
