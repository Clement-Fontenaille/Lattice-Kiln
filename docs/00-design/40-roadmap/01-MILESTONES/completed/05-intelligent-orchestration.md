# M5 — Intelligent orchestration experiments

**State:** done — 2026-08-31. Follow-up investigation closed 2026-09-02.
**Findings:** [entry 6](../../../50-findings/06-m5-intelligent-orchestration.md) — confirms, narrowly (one addendum) · [entry 7](../../../50-findings/07-m5-followup-investigation.md) — **confirms** (two addenda)
**Execution record:** [`M5-intelligent-orchestration.md`](../../../../50-PROGRESS/archives/M5-intelligent-orchestration.md)
**Specifications:** [`08-orchestrator-contract.md`](../../../../10-technical/08-orchestrator-contract.md), [`09-orchestrator-runtime-boundary.md`](../../../../10-technical/09-orchestrator-runtime-boundary.md)
**Experiment:** `experiments/M5-intelligent-orchestration/`

## What this milestone was

Introduce an LLM-based orchestrator capable of deciding which cognitive operation
appears useful next.

The main objective is not autonomy. It is to study whether natural-language
coordination outperforms a fixed workflow while remaining understandable.

## Evidence question

Does natural-language orchestration beat a fixed workflow while staying
understandable, and where does its overhead start to exceed the benefit of
decomposition?

## What it answered

**Confirms, narrowly.** Orchestrated 7/8 against a monolith's 6/8 and a fixed
chain's 5/8 — but the entire +1 came from **adaptive retry on the hard tasks**, at
roughly 5× the cost. The orchestrator was understandable for *acting* and weak for
*stopping*.

The workflow-suite re-test (entry 6 addendum, six workflow-shaped tasks, N=3)
sharpened rather than changed this: decomposition's benefit is real but
**concentrated on multi-file and multi-concern work**, and is pure overhead
elsewhere at 5–7× the model calls.

## The follow-up investigation

The re-evaluation this milestone owed ran as four experiments and produced
[findings entry 7](../../../50-findings/07-m5-followup-investigation.md) — the
result that reshaped the near-term plan more than any other:

| experiment | what it established |
|---|---|
| attractor census | where a 7B's motion is reliable (emit-the-whole-file survives cross-file indirection) and where it is blind (3/3 implement an impossible O(log n); 0/3 flag it) |
| judge-lab | **no reviewer framing** — neutral, adversarial, structured, K=5 voted — lifts a 7B above "assert the property and approve"; `criteria_first` is actively harmful; a deterministic gate scores 9/10 alone and **drops to 6/10 when the 7B panel is added** |
| loop-lab (bundle D) | test-gated loop + incumbent-protected keeper + escalate-on-stall: 0 regressions against `naive_loop`'s 2, solves the false premise in 0 calls, ~3.4× cheaper |
| super-pipeline | stacking every idea always-on: worse-or-tied on 5/6 tasks, **four stages that changed zero outcomes in 12 runs** |

**Consequence:** on a 7B the judgment seat is deterministic checks + run-the-test +
keep-the-incumbent + escalate. The model is a doer and a failure-explainer, not a
judge. That is what motivated [M6](06-evaluation-task-suite.md) and
[M7](07-static-supervised-workflow.md), and it is why a second judgment source —
a stronger or independent reviewer model — became the gating dependency for any
self-improving loop.

## What it changed

Adaptive retry was promoted from an M5 incidental to a named orchestrator element.
Spec `08` gained a **required stop rationale** and made `declined` distinct from
`blocked`. M2 was hardened in passing.

Two implementation gaps and one constraint were logged rather than fixed: an
unimplemented repetition stopping rule, a planner that over-returns `blocked` on
ordinary "not built yet" objectives, and a 7B implementer degraded by
unlabelled conversational handoff context. All three are in
[`../../00-backlog.md`](../../00-backlog.md).
