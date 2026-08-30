# M0 — Inference Envelope Measurement

Harness for Milestone 0. Measures what this host can actually run, per
`PROTOCOL.md`.

## Layout

```
PROTOCOL.md              the measurement contract
harness/
  detect-host.ps1        task 1 - host inventory  -> results/host.json
  models.json            the pinned model matrix           (pending)
  bench-ollama.ps1       full matrix via Ollama            (pending)
  bench-llamacpp.sh      7B/14B spot-checks via llama.cpp  (pending)
  aggregate.ps1          results/runs/*.json -> results/summary.md   (pending)
results/
  host.json              committed - host of record
  runs/*.json            committed - one record per run
  summary.md             generated aggregate
```

## Order of operations

1. `pwsh harness/detect-host.ps1` — already run; `results/host.json` is committed.
2. Install runtimes (see the M1 progress doc): Ollama on native Windows; a
   prebuilt CUDA `llama.cpp` inside WSL Ubuntu-22.04 (no source build — the host
   has no CUDA toolkit). Pull the Qwen2.5-Coder GGUFs named in `models.json`.
3. `pwsh harness/bench-ollama.ps1` — runs every matrix cell, writes
   `results/runs/ollama__*.json`.
4. `wsl bash harness/bench-llamacpp.sh` — 7B and 14B only, writes
   `results/runs/llama.cpp__*.json`.
5. `pwsh harness/aggregate.ps1` — builds `results/summary.md`.
6. The envelope description and the findings-log entry are written from the
   summary, back in the progress and roadmap docs.

## Notes

- Model files are git-ignored (`*.gguf`). Only `models.json` records which ones
  and at what digest.
- `results/` is committed — the runs are the evidence M0 exists to produce.
- Re-running overwrites `results/runs/*.json` for the same cell; prior runs live
  in git history.
