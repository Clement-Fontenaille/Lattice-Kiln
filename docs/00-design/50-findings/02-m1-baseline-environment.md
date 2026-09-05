# Entry 2 — Milestone 1: Reproducible baseline development environment

**Date:** 2026-08-30

**Evidence question:** can the baseline be reconstructed from scripts without
manual repair, and where does reproducibility actually break?

**What the evidence said.**

The environment — WSL2 + CUDA toolchain, llama.cpp built from source, Ollama
(native Windows), the pinned Qwen2.5-Coder model set, VS Code + Cline — is now
described by a declarative manifest (`experiments/M1-baseline-environment/manifest.json`,
schema `m1-manifest/0`) and stood up by an ordered, idempotent provisioning
orchestrator (`provision/provision.ps1`, six steps). `provision.ps1 -VerifyOnly`
passes green on the reference host: every component present at the pinned
version, GGUF digests verified against `models.json`, Cline configured to the
baseline (model / 16k context / 60 s timeout, auto-approval effectively off,
telemetry off).

It has **not** been run from scratch on a clean machine — verify-mode confirms
the host matches the manifest, not that the scripts built it from nothing. No
second machine is available now; a controlled clean-environment replay is owed
and tracked (`STATUS.md` → Post-MVP rework backlog).

Where reproducibility needs a human or a host-specific workaround (the
substantive finding):

1. **Driver + WSL bootstrap is not scriptable.** The NVIDIA Windows driver with
   WSL GPU support and `wsl --install -d Ubuntu-24.04` are operator actions; the
   scripts verify them, they do not install them.
2. **One privileged step.** `sudo apt-get install build-essential
   nvidia-cuda-toolkit jq` inside WSL — isolated to step 10, reported, never
   silent, but needs an interactive password.
3. **Stale WSL distro registration.** Registered as `Ubuntu-22.04`, actually
   running 24.04. Every `wsl -d` call hard-codes the misleading name; a clean
   install of `Ubuntu-24.04` would not match without editing the scripts.
4. **Tool-specific config formats.** Cline stores config as JSON under
   `~/.cline/data/`, but `globalState.json` mixes settings with host-specific
   state (workspace paths, commit hashes, migration records) and has no published
   schema — the committed template is a curated capture. An already-configured
   Cline is not auto-reconciled to the baseline; two toggles were manual. (This
   finding took three passes to get right — first "not scriptable", then wrong
   location — a caution that reverse-engineering a tool's storage deserves
   evidence, not assumption.)
5. **pip fragility on this WSL.** `python3-venv` absent, bare `pip3` had a broken
   SSL path; the working form `python3 -m pip --user --break-system-packages` is
   baked in but is a host-specific workaround.
6. **Write-ordering hazards.** Step 50 must run with VS Code closed or Cline
   overwrites the templates. The orchestrator enforces this; a naive script
   would not.

**Verdict: inconclusive** — on the literal question (reconstruction without
manual repair), because the definitive clean-machine run has not happened. What
*is* established: the scripted surface verifies green and is complete, and the
manual surface is fully enumerated (six items above). That enumeration is the
useful output — it is the concrete input to the bootstrapper.

**Touches.**

- Open questions: `40-roadmap/02-open-questions-register.md` → Bootstrapping
  ("Which parts belong in scripts vs. declarative config vs. local knowledge?" —
  M1 gives a first partition; "How portable across machines?" — untested).
- The eventual bootstrapper design document: the manifest is the proto-artifact;
  findings 1–6 are its backlog.
- Milestone sequence: no reordering. M1 is closed on "scripts complete + verified
  in place + breaks enumerated"; the clean-environment replay is deferred to the
  post-MVP rework, alongside the hardware-as-a-variable item.

**Runs.** `experiments/M1-baseline-environment/` — `manifest.json`,
`provision/` (orchestrator + six steps + `config/cline/` templates),
`run-reports/*.json` (schema `m1-provision-run/0`, git-ignored locally; the
green `-VerifyOnly` run of 2026-08-30 is the reference).
