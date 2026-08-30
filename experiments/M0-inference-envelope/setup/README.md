# M0 setup — reproducing the inference-envelope measurement

These scripts stand up the two runtimes M0 measures and fetch the model assets,
so the sweep can be re-run on this host or adapted to another. They are the
**seed for Milestone 1** (reproducible baseline environment); M1 is where a
general, cross-host provisioning system belongs. Here the goal is narrower:
capture what was actually done, with the host-specific constants called out.

Re-characterising the envelope is a recurring job — after a hardware change, a
runtime upgrade, or at Milestone 13 (cross-generation comparison). Treat this
directory as the checklist for that.

## Host-specific constants (change per machine)

| Constant | This host | Where it appears |
|---|---|---|
| Ollama install dir (not on PATH) | `%LOCALAPPDATA%\Programs\Ollama` | `harness/bench-ollama.ps1`, `bench-switch.ps1`, `bench-load-extra.ps1` self-locate it |
| GPU compute capability | `sm_75` (RTX 2070 SUPER, Turing) | `build-llamacpp-wsl.sh` → `-DCMAKE_CUDA_ARCHITECTURES` |
| CUDA toolchain | apt `nvidia-cuda-toolkit` (nvcc 12.0) in WSL | `build-llamacpp-wsl.sh` — needs one `sudo apt-get install` |
| WSL distro | `Ubuntu-22.04` (registered name; actually 24.04) | all `wsl.exe -d` invocations |
| Model matrix | Qwen2.5-Coder 3B/7B/14B | `harness/models.json` |

## Run order

All PowerShell from the repo root in Windows PowerShell 5.1; all bash inside WSL.

### 1. Inventory the host
```powershell
powershell -ExecutionPolicy Bypass -File experiments\M0-inference-envelope\harness\detect-host.ps1
```
Writes `results/host.json`. Every run record carries its SHA-256 as `host_ref`.

### 2. Ollama (runtime of record)
Install Ollama for Windows (native). Confirm the server answers on
`http://localhost:11434`. The bench scripts prepend the install dir to `PATH`
themselves if `ollama` is not resolvable.

### 3. llama.cpp with CUDA (fidelity spot-check, in WSL)
One privileged step, then no more sudo:
```bash
sudo apt-get install -y nvidia-cuda-toolkit      # nvcc 12.0; ~1.9 GB
```
Then:
```bash
bash setup/build-llamacpp-wsl.sh
```
This installs `cmake`/`ninja` via `pip --user`, clones llama.cpp (pinned commit
recorded in `~/m0-llamacpp-build.log`), configures with `-DGGML_CUDA=ON
-DCMAKE_CUDA_ARCHITECTURES=75`, builds **`llama-bench`** only (the current tree's
unified `llama` CLI needs sub-impl libs a lean build omits; `llama-bench -o json`
covers the spot-check), and installs it plus its shared libs to `~/.local`.

### 4. Model assets
- **Ollama** pulls its own on first use — `bench-ollama.ps1` does this on demand.
  The full matrix is ~32 GB of pulls (3B q4+q8, 7B q4+q5+q8, 14B q4).
- **llama.cpp** needs GGUFs on disk:
  ```bash
  bash setup/fetch-ggufs-wsl.sh          # -> ~/m0-models, ~14 GB
  ```
  Fetches bartowski Qwen2.5-Coder 7B Q4_K_M and 14B Q4_K_M. Digests are pinned in
  `harness/models.json` (`gguf_sha256`); verify with `sha256sum ~/m0-models/*.gguf`.

### 5. Sweeps
```powershell
# Ollama matrix: model x quant x context-fill, 5 reps/cell, + switch pass
powershell -ExecutionPolicy Bypass -File experiments\M0-inference-envelope\harness\bench-ollama.ps1

# concurrent_delta + sustained_drift (one representative cell)
powershell -ExecutionPolicy Bypass -File experiments\M0-inference-envelope\harness\bench-load-extra.ps1

# switch cost only (use after an interrupted matrix run)
powershell -ExecutionPolicy Bypass -File experiments\M0-inference-envelope\harness\bench-switch.ps1
```
```bash
# llama.cpp spot-check (WSL): pp/tg tok/s + offload split, ngl sweep on 14B
MODELS_DIR=~/m0-models bash experiments/M0-inference-envelope/harness/bench-llamacpp.sh
```
The Ollama matrix is expensive on a VRAM-bound host: quant/fill combinations that
spill to CPU generate at 1–5 tok/s. Staging (let the small models finish, eyeball
`results/summary.md`, then continue) is the intended workflow. `models.14b-tail.json`
is an example of a trimmed re-run.

### 6. Aggregate
```powershell
powershell -ExecutionPolicy Bypass -File experiments\M0-inference-envelope\harness\aggregate.ps1
```
Regenerates `results/summary.md` from `results/runs/*.json`. Do not hand-edit it.

## What is NOT scripted here

- Installing Ollama itself (a GUI/winget install; version is captured per run).
- WSL provisioning (distro install, GPU passthrough) — assumed present.
- A one-command "do everything" driver — deliberately omitted. The steps have
  human checkpoints (validate the cheap path before 32 GB of pulls) that a
  single script would paper over. A real driver is M1's job.
