# M1 — Reproducible Baseline Development Environment

**Milestone:** `40-roadmap/01-milestones.md` → Milestone 1
**Evidence question:** can the baseline be reconstructed from scripts without manual repair, and where does reproducibility actually break?
**State:** WIP

## What "done" looks like

A scripted setup that stands up the development environment — Windows/WSL layout,
local inference runtime, model assets, VS Code, Cline — from a mostly-clean
machine with no undocumented manual repair steps, plus a **manifest** recording
what it produced (versions, digests, entry point). The manifest is the first
concrete step toward the bootstrapper concept and stays declarative.

The environment is intentionally boring, stable, and observable. Its value is as
a fixed reference that later generations improve upon.

Scope note: this milestone targets **one host**. Hardware as a variable —
re-bootstrapping and re-characterising on a different machine — is explicitly
deferred to the post-MVP (end-of-M5) rework (`STATUS.md` → Post-MVP rework
backlog; `40-roadmap/02-open-questions-register.md` → Bootstrapping).

## Inherited from M0

M0 already produced and committed the hard-won parts, under
`experiments/M0-inference-envelope/setup/`:

- `build-llamacpp-wsl.sh` — llama.cpp CUDA build in WSL (apt `nvidia-cuda-toolkit`
  + pip cmake/ninja, pinned commit, `sm_75`).
- `fetch-ggufs-wsl.sh` — GGUF fetch with digests pinned in `harness/models.json`.
- `README.md` — run order and the host-specific constants table.
- `harness/detect-host.ps1` — host inventory → `host.json`.

M0 also settled the **native-vs-WSL boundary** (task 1 below): Ollama runs
native on Windows; llama.cpp runs in WSL because the host has no native CUDA
toolchain and no prebuilt Linux CUDA binary exists. M1 records this as a
decision, it does not re-litigate it.

## Task breakdown

| # | Task | State | Notes |
|---|---|---|---|
| 1 | Native-Windows vs WSL boundary per component | DONE (M0) | Ollama → native Windows. llama.cpp → WSL. VS Code + Cline → native Windows. Editor/LSP/build tools → per project. Record in the manifest. |
| 2 | Script the OS-level prerequisites | TODO | WSL distro presence, NVIDIA driver + WSL GPU passthrough check, base packages (`jq`, build-essential, `nvidia-cuda-toolkit`). Idempotent; fail loudly on the one privileged step. |
| 3 | Script the inference runtime install + model fetch | TODO | Ollama install (or verify) + server-up check; llama.cpp build via the M0 script; `ollama pull` the pinned matrix; GGUF fetch. Pinned versions, pinned digests. |
| 4 | Script the editor + Cline setup | TODO | VS Code + Cline install/verify; config checked in, not hand-edited. Point Cline at the local Ollama endpoint and the working-default model (7B Q4_K_M / Q5_K_M, per M0). |
| 5 | Write the environment manifest | TODO | One declarative file: component list, native/WSL placement, pinned versions, model digests, reconstruction entry point. Proto-bootstrap artifact. |
| 6 | Clean-ish reconstruction test | TODO | The evidence question. Run the scripts against as-clean-a-state as practical; record **every** manual repair that proves necessary as a finding. |
| 7 | Findings-log entry | TODO | Verdict: can the baseline be reconstructed without manual repair, and where does reproducibility break. |

## Notes

- Reproducibility breakages found in task 6 are findings — they feed the
  bootstrapper design document, not just a fix list.
- Keep the driver thin. M0's `setup/README.md` deliberately has human checkpoints
  (validate cheap before large pulls); M1 may automate more, but a breakage that
  needs a human is a finding to record, not a failure to hide.
- The manifest should record model/quant and the offload expectation per model,
  since M2's event model will want that and M0 showed it predicts latency 10–20×.
