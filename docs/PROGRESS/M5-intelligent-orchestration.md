# M5 — Intelligent Orchestration Experiments

**Milestone:** `40-roadmap/01-milestones.md` → Milestone 5 (last of the MVP slice)
**Evidence question:** does natural-language orchestration beat a fixed workflow
while staying understandable, and where does its overhead start to exceed the
benefit of decomposition?
**State:** COMPLETE (2026-08-31) — findings-log entry 6. Verdict **confirms,
narrowly**: orchestrated 7/8 vs monolith 6/8 vs fixed chain 5/8, the win entirely
from adaptive retry, at ~5× cost. MVP slice (M0–M5) closed;
`40-roadmap/06-sequence-rework-01.md` written.

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
| 3 | Orchestrator implementation | DONE | `orchestrator.py` — `run_orchestrated()` loop over the M4 runtime; decision record (type-4) per step routed through the M3 floor; spawns via unmodified `run_processor`; stops on objective-met / repetition / step budget / no-useful-next-op; synthesis record on close. |
| 4 | `orchestrated` harness arm | DONE | `compare.py` — third arm alongside M4's `monolith` and `ephemeral` (both reused verbatim). The orchestrator spawned a second implementer on tasks the first attempt failed (the M4-finding revision loop). |
| 5 | Comparison run | DONE | 3 arms × 4 tasks × N=2 = 24 runs. `results/results.json` + `summary.md`. Orchestrated 7/8, monolith 6/8, fixed chain 5/8; ~5× calls, ~4.5× wall for orchestrated. |
| 6 | Understandability check | DONE | `strategy_check.py` — every run's strategy (op per step + spawn rationale) reconstructs from decision records alone, matching the invocation lineage. Gap: 7/8 stop decisions carried no rationale. |
| 7 | Findings-log entry 6 | DONE | Verdict **confirms, narrowly**. Overhead exceeds benefit on any task a single pass can solve; the +1/8 win is adaptive retry on the hard tasks. |
| 8 | End-of-MVP sequence rework | DONE | `40-roadmap/06-sequence-rework-01.md` — no reordering; backlog consolidated; M4/M5 re-test folded into M7/M8. |

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
