# M1 — Reproducible Baseline Development Environment

Milestone 1. Turns the M0 setup scripts into a scripted, manifest-backed baseline
that a mostly-clean machine can be brought to without undocumented manual repair.

**Evidence question:** can the baseline be reconstructed from scripts without
manual repair, and where does reproducibility actually break?

Decomposition and task state: `docs/PROGRESS/M1-baseline-environment.md`.

## Layout

```
manifest.json            declarative known-good state — components, native/WSL
                         placement, pinned versions, model digests, entry point
provision/
  provision.ps1          Windows-side orchestrator: runs each step, records a
                         run report, never hides a manual repair
  steps/                 ordered, individually runnable steps
  config/                checked-in tool config (not hand-edited on the host)
run-reports/             output of provision.ps1 runs (git-ignored except .keep)
```

## Native vs WSL boundary (decided at M0)

| Component | Placement | Why |
|---|---|---|
| Ollama (runtime of record) | native Windows | first-class Windows build; drives Cline and the assistant |
| llama.cpp (fidelity spot-check) | WSL Ubuntu | host has no native CUDA toolchain; no prebuilt Linux CUDA binary — built from source |
| VS Code + Cline | native Windows | edits the repo on the Windows filesystem |
| editor LSPs / build tools | per project | not part of the baseline itself |

## Relationship to M0

`provision/steps/` reuses, not duplicates:

- `../../M0-inference-envelope/setup/build-llamacpp-wsl.sh`
- `../../M0-inference-envelope/setup/fetch-ggufs-wsl.sh`
- `../../M0-inference-envelope/harness/detect-host.ps1`
- pinned model set + GGUF digests in `../../M0-inference-envelope/harness/models.json`

## Scope

One host. Re-bootstrapping / re-characterising on different hardware is deferred
to the post-MVP rework (`docs/PROGRESS/STATUS.md` → Post-MVP rework backlog).
