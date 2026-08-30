# M4 — Ephemeral Processor Experiments

Milestone 4. First milestone that runs real model inference. Compares a
monolithic agent against an ephemeral planner → implementer → reviewer split, and
in doing so exercises the M2 recorder and the M3 invariant floor against real
runs.

**Evidence question:** do ephemeral roles, fresh context, and independent review
beat a monolithic agent on a small task set?

Contracts: `docs/10-technical/06-processor-contract.md`,
`docs/10-technical/07-naive-context-assembly.md`.
Decomposition + task state: `docs/PROGRESS/M4-ephemeral-processors.md`.

## Layout

| File | Role |
|---|---|
| `_bridge.py` | `sys.path` wiring to the M2 recorder (`event_model`, `reconstruct`) and the M3 floor (`capabilities`, `gate`, `enforce`). M4 reuses those, does not fork them. |
| `ollama_client.py` | Non-streaming Ollama client (stdlib urllib). Working default per M0: `qwen2.5-coder:7b-instruct-q4_K_M`, `num_ctx` 16384. |
| `context_assembly.py` | Naive context assembly, v0 of spec `07`. Objective + README + file tree + hint/substring file inclusion to a token budget. Deterministic; emits a selection trace. |
| `roles.py` | The tiny fixed role library: `implementer`, `planner`, `reviewer`, plus each role's capability grants and the control-block output protocol. |
| `processor.py` | The processor runtime, spec `06`. One instance = one model call; every proposed effect routed through `enforce.submit_effect`; every event recorded through `RunRecorder`; only gate-passed effects realized. No resume. |
| `placeholder_selftest.py` | Plumbing test: one real model call end-to-end + the synthetic gate-refusal path. Skips if Ollama is down. |
| `fixture/` | The synthetic task-set repo and `tasks.json` (added after plumbing verified). |
| `harness.py` | Arm A (monolith) vs arm B (ephemeral split) over the task set, N repetitions, objective scoring. |
| `runs/` | One directory per run (`run.json` + `events.jsonl`). Git-ignored except `.gitkeep`. |

## Effect model in play

A processor's control block yields:

- `workspace_write` → effect type 1 (workspace mutation), realized as a file write.
- `process_run` → effect type 2 (process execution), realized via `subprocess`.
- the processor's own conclusion → effect type 4 (work-record mutation).

Whether a conclusion is genuinely an "effect" is one of the type-boundary
questions M4 is meant to surface (`docs/PROGRESS/M4` task 9).

## Run the plumbing test

```
python experiments/M4-ephemeral-processors/placeholder_selftest.py
```

## Status

Plumbing built and verified (one real 7B call, ~39 tok/s as M0 predicted; gate
refusal of an observability-record write recorded as a `gate_refusal`
safety-intervention; run reconstructs). Next: the synthetic fixture task set
(4 tasks) and the arm-A/arm-B harness, then the three evidence checks.
