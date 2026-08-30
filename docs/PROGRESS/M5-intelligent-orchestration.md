# M5 — Intelligent Orchestration Experiments

**Milestone:** `40-roadmap/01-milestones.md` → Milestone 5 (last of the MVP slice)
**Evidence question:** does natural-language orchestration beat a fixed workflow
while staying understandable, and where does its overhead start to exceed the
benefit of decomposition?
**State:** decomposing — specs written

## What "done" looks like

Findings-log entry 6, resting on committed reconstructable runs, comparing an
**LLM orchestrator** that decides the next cognitive operation against (a) the M4
fixed planner→implementer→reviewer chain and (b) the monolith, on the same
fixture task set. "Understandable" is a first-class part of the question: the
orchestrator's strategy must be reconstructable from its decision records alone.
An *inconclusive* verdict is acceptable if the runs support it.

Completing M5 also closes the MVP slice (M0–M5) and triggers the **first
scheduled sequence rework** — the batch review of findings-log entries 1–6.

## Deliverables

- Specs (both written this session):
  - `10-technical/08-orchestrator-contract.md` — the orchestrator loop, per-step
    decision record, delegation rules, stopping rules.
  - `10-technical/09-orchestrator-runtime-boundary.md` — the two reasoning→runtime
    crossings and three runtime→reasoning crossings; runtime validation depth
    narrowed to "four properties + deny-list, nothing semantic".
- An **orchestrator** under `experiments/M5-intelligent-orchestration/`: an LLM
  loop (observe → decide next operation → spawn a processor via the M4 runtime →
  integrate → stop-or-continue), capability set `{6, 4}` only, a decision record
  per step, the stopping rules from spec `08`. Reuses — does not fork — the M4
  processor runtime, the M3 gate, the M2 recorder.
- A third harness arm, **`orchestrated`**, alongside M4's `monolith` and
  `ephemeral`. It may route a reviewer's `needs-change` back to a fresh
  implementer (the M4 finding: independent review is inert without a loop).
- The comparison run over the fixture task set (extend it only if 4 tasks prove
  too coarse to separate the arms), then the two checks and the findings entry.

## Task breakdown

| # | Task | State | Notes |
|---|---|---|---|
| 1 | Orchestrator contract spec (`08`) | DONE | v0. Loop + decision record + stopping rules; mediation = route-output-as-input for the MVP. |
| 2 | Orchestrator/runtime boundary spec (`09`) | DONE | v0. Crossings fixed; validation depth = 4 properties + gate, no semantic judgment; call order pinned. |
| 3 | Orchestrator implementation | TODO | LLM loop over the M4 runtime. Decision record = type-4 effect per step. Stopping: objective met / repetition / R3 budget / no-useful-next-op. |
| 4 | `orchestrated` harness arm | TODO | Third arm. Reviewer `needs-change` → new implementer invocation carrying the critique, bounded by the step budget. |
| 5 | Comparison run | TODO | 3 arms × fixture tasks × N. All runs committed. |
| 6 | Understandability check | TODO | Reconstruct the orchestrator's strategy (what it chose each step and why) from decision records alone. |
| 7 | Findings-log entry 6 | TODO | Verdict on NL-orchestration vs fixed workflow; where overhead exceeds benefit. |
| 8 | Trigger end-of-MVP sequence rework | TODO | Batch review of findings 1–6 → milestone-sequence revision (`00-project/04-execution-cadence.md`). |

## Carried-in constraints

- **One resident model** (M0): the orchestrator runs on the same 7B as the
  processors; no per-role model switching. A stronger orchestrator model is a
  Milestone 13 question.
- **Naive context** (spec `07`, M4 finding): the orchestrator's own context is
  "intent + running summary + naive bundle"; M4 showed the naive assembler misses
  files and processors never ask. Expect the orchestrator to inherit that
  weakness.
- **Human supervises every run** (MVP invariant list).
- **M4 result to beat**: monolith 6/8, fixed ephemeral 5/8 at ~3× cost. The bar
  for "orchestration earns its overhead" is set by that.

## Notes

- Just-in-time: `08` and `09` are the last two spec-backlog items for the MVP.
  Nothing beyond Milestone 5 is specified.
- If the orchestrator cannot be made to beat the fixed chain at this scale, that
  is a legitimate finding — it says the benefit needs better context or a
  stronger model, not that NL orchestration is worthless. The end-of-MVP rework
  is where that gets weighed.
