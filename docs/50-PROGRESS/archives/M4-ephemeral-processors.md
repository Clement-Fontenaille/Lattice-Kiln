# M4 — Ephemeral Processor Experiments

**Milestone:** `40-roadmap/01-milestones.md` → Milestone 4
**Evidence question:** do ephemeral roles, fresh context, and independent review
beat a monolithic agent on a small task set?
**State:** COMPLETE (2026-08-30) — findings-log entries 3 (M2), 4 (M3), 5 (M4).
Verdict on the M4 question: **inconclusive, leaning weakens** — a non-looping
planner→implementer→reviewer chain did not beat a monolith (5/8 vs 6/8) at ~3×
the cost.

## Why this milestone carries three findings-log entries

M4 is the first milestone where anything real runs. It is where the machinery
built ahead of it gets exercised and where three evidence questions get answered
from reconstructable runs:

| From | Question | How M4 answers it |
|---|---|---|
| M2 | Can a run be reconstructed to answer a question nobody designed the schema for? | Wire the M2 recorder into the M4 runtime; after the runs, pose an unplanned question and answer it from stored records alone. |
| M3 | Do the nine effect types carve cleanly when real effects flow through the gate? | Every M4 effect goes through `experiments/M3-invariant-floor/enforce.py`; inspect the real effect stream for type-boundary blur. |
| M4 | Do ephemeral roles + fresh context + independent review beat a monolith? | Two arms, same model, same task set, same budget; compare on objective task outcome and on reasoning-quality signals. |

## What "done" looks like

Findings-log entries 3 (M2), 4 (M3), and 5 (M4), each resting on committed,
reconstructable runs under `experiments/M4-ephemeral-processors/`. A verdict of
*inconclusive* on any of the three is an acceptable outcome if the runs support
it (`03-research-and-evaluation-agenda.md`, evaluation posture).

## Deliverables

- Specs (both written this session):
  - `10-technical/06-processor-contract.md` — processor input/output envelope +
    lifecycle, bound to effect type 6 and the kind-1 record.
  - `10-technical/07-naive-context-assembly.md` — the deliberately simple v0
    context baseline for Milestone 7.
- A thin **processor runtime** under `experiments/M4-ephemeral-processors/`:
  binds a role + capability set, calls naive assembly, calls the working-default
  model via Ollama, routes **every** effect through the M3 enforcement pipeline,
  records **every** event through the M2 `RunRecorder`. Realizes only the effects
  the gate passes; a human reviews every run (MVP invariant).
- A tiny **role library**: monolithic `implementer`; ephemeral split
  `planner` → `implementer` → `reviewer` (`review` mode, conclusion-only).
- A small **task set** (see open decision below).
- The **comparison harness**: arm A (monolith) vs arm B (ephemeral split), same
  model / budget / tasks, N repetitions, objective scoring (build / test / lint)
  plus recorded reasoning-quality signals.

## Task breakdown

| # | Task | State | Notes |
|---|---|---|---|
| 1 | Processor contract spec (`06`) | DONE | v0. Five-part input envelope, output envelope, lifecycle, no-resume. |
| 2 | Naive context assembly spec (`07`) | DONE | v0. Normative: stays simple, emits a selection trace. M7 replaces (not accretes). |
| 3 | Decide the task set | DONE | Operator: synthetic fixture repo, 4 tasks × N=2. `fixture/` — implement-from-stub, bug-fix, false-premise, context-starvation; `tasks.json` schema `m4-tasks/0`. |
| 4 | Processor runtime | DONE | `processor.py` — `run_processor()`: one model call, control-block parse, every effect → `enforce.submit_effect`, every event → `RunRecorder`, realize only gate-passed. Conclusion recorded as effect type 4. Caller owns run lifecycle (no processor self-close). |
| 5 | Role library | DONE | `roles.py` — `implementer` / `planner` / `reviewer`, per-role capability grants, `<<<FILE>>>` + `<<<CONTROL>>>` output protocol (JSON kept free of file bodies after a `"""`-in-JSON parse failure). |
| 6 | Naive context assembler | DONE | `context_assembly.py` — objective + README + tree + hint/substring inclusion to an 8k-token budget, deterministic, selection trace. |
| 7 | Comparison harness + run the set | DONE | `harness.py` — arm A vs arm B, 4×2, `results/results.json` + `results/summary.md` committed; per-run records under `runs/`. |
| 8 | M2 reconstruction check | DONE | `reconstruction_check.py` — two unplanned questions answered from records alone → findings-log entry 3. |
| 9 | M3 effect-carving check | DONE | Effect stream inspected via the same script (Q2) → findings-log entry 4. 3/9 types, all clean; gate never tripped. |
| 10 | M4 findings-log entry | DONE | Entry 5 — verdict inconclusive, leaning weakens. |

## Task set (resolved)

Operator decision: **synthetic fixture repo, 4 tasks × N=2**, build the runtime
first against a placeholder. Delivered as `experiments/M4-ephemeral-processors/fixture/`
(`task_1_stringcalc` implement-from-stub, `task_2_median` bug-fix-behind-a-failing
-test, `task_3_nobug` false-premise, `task_4_starve` context-starvation), scored
by a stdlib `python test_task.py` check (no pytest dependency on the host).

## Notes

- Just-in-time: `06` and `07` are written because M4 needs them; the orchestrator
  contract (M5) is **not** written yet — a fixed harness plays caller for M4.
- The runtime reuses, not reimplements, `experiments/M2-observability-foundation/`
  and `experiments/M3-invariant-floor/`. If either needs a change to be usable
  from a real run, that change is a finding for its milestone.
- A human supervises every run (MVP invariant list, operational stance).
