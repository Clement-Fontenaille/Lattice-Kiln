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

## Where the work lives

`experiments/M1-baseline-environment/` — `manifest.json` (declarative state),
`provision/provision.ps1` (orchestrator + run report), `provision/steps/00..50`,
`provision/config/cline-settings.json`, `run-reports/` (git-ignored).

## Task breakdown

| # | Task | State | Notes |
|---|---|---|---|
| 1 | Native-Windows vs WSL boundary per component | DONE | Recorded in `README.md` + `manifest.json`. Ollama native; llama.cpp WSL; VS Code + Cline native. |
| 2 | Script the OS-level prerequisites | DONE | `steps/00-wsl.ps1` (WSL2 + distro + GPU passthrough), `steps/10-wsl-prereqs.sh` (apt build-essential/jq/nvidia-cuda-toolkit + pip cmake/ninja). Idempotent; the one `sudo` is isolated and reported, never silent. |
| 3 | Script the inference runtime install + model fetch | DONE | `steps/20-llamacpp.sh` wraps the M0 build + GGUF-fetch scripts and verifies pinned digests; `steps/30-ollama.ps1` installs/verifies Ollama + server; `steps/40-models.ps1` ensures the working-default tags (`-FullModelMatrix` for all ~32 GB). |
| 4 | Script the editor + Cline setup | PARTIAL | `steps/50-editor-cline.ps1` installs/verifies VS Code + the Cline extension and checks for a configured `providers.json`. Cline config is file-based JSON (`providers.json` / `global-settings.json` under the extension's globalStorage) but the schema is undocumented and UI-first (see finding 1). Path to done: capture those files from a once-configured instance, commit as templates under `provision/config/`, have step 50 copy them. Until then the step reports the exact manual steps as `WARN`. |
| 5 | Write the environment manifest | DONE (v0) | `manifest.json`, schema `m1-manifest/0`. Component list, native/WSL placement, pinned versions, model digests, reconstruction entry point, known manual steps. |
| 6 | Clean-ish reconstruction test | PARTIAL | `provision.ps1 -VerifyOnly` passes green against the current host (`OK_WITH_WARN`, the warn = the Cline manual step). A genuine clean-machine run is still owed — verify-mode confirms the checker agrees, not that the scripts built it from nothing. |
| 7 | Findings-log entry | TODO | After a real clean-machine attempt. Running list below. |

## Findings so far (feed the bootstrapper doc, not just a fix list)

1. **Cline configuration is file-based but UI-first — scriptable only via an
   undocumented format.** (Corrected from an earlier, wrong "not scriptable".)
   Evidence, from `saoudrizwan.claude-dev-4.1.16/next/dist/extension.js` and
   [docs.cline.bot/getting-started/config](https://docs.cline.bot/getting-started/config):
   - `contributes.configuration` exposes only `cline.rollout.bundleOverride`, so
     VS Code `settings.json` / `code --…` cannot set the provider or model.
   - Cline persists provider/model/global config to plain JSON:
     `providers.json` (empty shape `{ "version": 1, "providers": {} }`),
     `global-settings.json`, `cline_mcp_settings.json`. VS Code extension
     location: `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\`.
     Path overrides shipped in the bundle: `CLINE_PROVIDER_SETTINGS_PATH`,
     `CLINE_GLOBAL_SETTINGS_PATH`, `CLINE_MCP_SETTINGS_PATH`, `CLINE_DATA_DIR`.
   - Ollama provider fields: `ollamaBaseUrl`, `planModeOllamaModelId` /
     `actModeOllamaModelId`, `ollamaApiOptionsCtxNum`, `ollamaThink`.
   - Caveats: the file schemas are undocumented and zod-validated on load (a bad
     pre-seed is rejected or migrated); API keys go to OS-encrypted VS Code
     SecretStorage, **not** these files — irrelevant for our keyless local Ollama
     provider, but the file-only path does not generalize; the files are created
     on first configure, so pre-seeding before first launch is untested; the docs
     present the settings UI and `cline config` (CLI) as the configuration
     methods, not file editing.
   - Baseline approach: configure Cline once via the UI, commit the resulting
     `providers.json` + `global-settings.json` as templates under
     `provision/config/`, and have step 50 copy them into place (or point
     `CLINE_*_SETTINGS_PATH` at the committed copies). Until a template is
     captured, step 50 reports the exact manual steps as a `WARN`.
   - Whether a more config-as-code-friendly agent frontend (e.g. Continue.dev,
     which is `config.yaml`-first and documented) should replace Cline is a
     design question for the post-MVP rework, not an M1 change — the milestone
     names Cline explicitly. Registered in `STATUS.md` → Post-MVP rework backlog.
2. **Stale WSL distro registration.** The distro registered as `Ubuntu-22.04` is
   actually Ubuntu 24.04.4. Every `wsl -d` call hard-codes the misleading name;
   a fresh machine that installs `Ubuntu-24.04` cleanly would not match. The
   provision scripts and manifest use the registered name and flag the mismatch.
3. **pip on this WSL is fragile.** `python3-venv` is absent and bare `pip3` hit a
   broken SSL path; the working invocation is
   `/usr/bin/python3 -m pip install --user --break-system-packages`. Baked into
   `steps/10` and the manifest.
4. **Verify-mode cannot prove reconstruction.** It confirms the environment
   matches the manifest, not that these scripts produced it. Task 6 still needs a
   near-clean host (or a fresh WSL distro + a VM/second machine for the Windows
   side).

## Notes

- Reproducibility breakages found in task 6 are findings — they feed the
  bootstrapper design document, not just a fix list.
- Keep the driver thin. M0's `setup/README.md` deliberately has human checkpoints
  (validate cheap before large pulls); M1 may automate more, but a breakage that
  needs a human is a finding to record, not a failure to hide.
- The manifest should record model/quant and the offload expectation per model,
  since M2's event model will want that and M0 showed it predicts latency 10–20×.
