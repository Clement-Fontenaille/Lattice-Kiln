# M1 — Reproducible Baseline Development Environment

**Milestone:** `40-roadmap/01-milestones.md` → Milestone 1
**Evidence question:** can the baseline be reconstructed from scripts without manual repair, and where does reproducibility actually break?
**State:** TODO

> This decomposition is provisional. It will be firmed up as M0 nears completion, once the inference runtime and host layout are settled.

## What "done" looks like

A scripted setup that stands up the development environment — Windows/WSL layout, local inference runtime, model assets, VS Code, Cline — from a clean machine with no manual repair steps, and a manifest recording what it produced.

The environment is intentionally boring, stable, and observable. Its value is as a fixed reference that later generations improve upon.

## Provisional task breakdown

| # | Task | State | Notes |
|---|---|---|---|
| 1 | Decide native-Windows vs WSL boundary for each component | TODO | Inference runtime placement follows the M0 runtime decision. |
| 2 | Script the OS-level prerequisites | TODO | WSL, drivers/CUDA, base packages. |
| 3 | Script the inference runtime install and model fetch | TODO | Pinned versions, pinned model digests. |
| 4 | Script the editor and Cline setup | TODO | Config checked in, not hand-edited. |
| 5 | Write the environment manifest | TODO | Versions, digests, and reconstruction entry point. Proto-bootstrap artifact. |
| 6 | Clean-machine reconstruction test | TODO | The evidence question. Record every manual repair that proves necessary. |

## Notes

- The manifest from task 5 is the first concrete step toward the bootstrapper concept; keep it declarative.
- Reproducibility breakages found in task 6 are findings — they feed the bootstrapper design document, not just a fix list.
