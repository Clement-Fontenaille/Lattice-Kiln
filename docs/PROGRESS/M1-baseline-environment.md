# M1 — Reproducible Baseline Development Environment

**Milestone:** `40-roadmap/01-milestones.md` → Milestone 1
**Evidence question:** can the baseline be reconstructed from scripts without manual repair, and where does reproducibility actually break?
**State:** DONE (2026-08-30) — closed on "scripts complete + verified in place + manual surface enumerated". Findings-log entry 2. The definitive clean-machine replay is deferred to the post-MVP rework (no second machine available now).

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
| 4 | Script the editor + Cline setup | DONE | `steps/50-editor-cline.ps1` installs/verifies VS Code + Cline, and copies the committed templates `provision/config/cline/{providers,global-settings,globalState}.json` into `%USERPROFILE%\.cline\data\` when Cline is unconfigured (refuses to write under a running VS Code). Templates were captured from a UI-configured instance and curated (host-specific and cruft keys stripped; auto-approval/telemetry/auto-update set to baseline values). See finding 1 + `provision/config/cline/README.md`. |
| 5 | Write the environment manifest | DONE (v0) | `manifest.json`, schema `m1-manifest/0`. Component list, native/WSL placement, pinned versions, model digests, reconstruction entry point, known manual steps. |
| 6 | Clean-ish reconstruction test | PARTIAL (closed) | `provision.ps1 -VerifyOnly` passes green against the reference host (`overall: OK`, 6/6 steps, zero WARN). A genuine clean-machine run is still owed — no second machine now — and is deferred to the post-MVP rework (`STATUS.md`). Verify-mode confirms the host matches the manifest, not that the scripts built it from nothing. |
| 7 | Findings-log entry | DONE | `40-roadmap/05-findings-log.md` entry 2. Verdict: **inconclusive** on reconstruction-without-repair (clean run not done), but the manual surface is fully enumerated (6 items) — that enumeration is the bootstrapper backlog. |

## Findings so far (feed the bootstrapper doc, not just a fix list)

1. **Cline configuration is file-based at a documented location; scriptable with
   one curation step.** (This is the third and settled version — earlier notes
   wrongly said "not scriptable", then wrongly located the files in VS Code
   globalStorage.) Evidence: `saoudrizwan.claude-dev-4.1.16` (`next` bundle,
   confirmed active via `state.vscdb` `cline.rollout.bundle:"next"`),
   [docs.cline.bot/getting-started/config](https://docs.cline.bot/getting-started/config),
   and the live files on this host.
   - `contributes.configuration` exposes only `cline.rollout.bundleOverride` —
     VS Code `settings.json` / `code --…` cannot configure Cline. That part of
     the original instinct held.
   - The `next` bundle stores everything under **`%USERPROFILE%\.cline\data\`**
     (relocatable via `CLINE_DATA_DIR`), NOT VS Code globalStorage:
     - `settings/providers.json` — provider registry. Our `ollama` block
       (`model`, `baseUrl`, `timeout`). Also carries a `sapaicore` entry from a
       Cline migration — cruft.
     - `settings/global-settings.json` — `autoUpdateEnabled`, `telemetryOptOut`.
     - `globalState.json` — the effective settings: `{plan,act}ModeApiProvider`,
       `{plan,act}ModeOllamaModelId`, `ollamaBaseUrl`, `ollamaApiOptionsCtxNum`
       (a string, e.g. `"16384"`), `requestTimeoutMs`, `autoApprovalSettings`,
       `telemetrySetting` — **mixed with host-specific state**: `workspaceRoots`
       (absolute path + git commit hash), `primaryRootIndex`, a legacy-MCP
       migration path, `lastShownAnnouncementId`, other-provider cruft.
   - So it IS scriptable, but a committed template must be **curated**: keep the
     config keys, strip the host-specific and cruft keys. Done:
     `provision/config/cline/{providers,global-settings,globalState}.json` +
     `README.md`. `steps/50` copies them into `~/.cline/data\` when Cline is not
     yet configured, and **refuses to write while VS Code is running** (Cline
     would overwrite on next save).
   - Remaining caveats: no published schema for hand-authoring `globalState.json`
     (the template is a curated capture, validated only by Cline accepting it on
     load); API-keyed providers would also need VS Code SecretStorage (a file
     won't do) — moot for keyless local Ollama.
   - Cline defaults that the baseline overrides in the template: auto-approval
     (Cline default `enabled: true` with reads / safe commands / MCP approved →
     baseline `false`, a human approves every run), telemetry (`enabled` →
     `disabled`), auto-update (`true` → `false`, a baseline is pinned).
   - Whether a `config.yaml`-first frontend (e.g. Continue.dev) should replace
     Cline is a post-MVP rework question, not an M1 change — the milestone names
     Cline. Registered in `STATUS.md` → Post-MVP rework backlog.
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
