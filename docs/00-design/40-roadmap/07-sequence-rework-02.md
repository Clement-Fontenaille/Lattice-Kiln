# Sequence Rework 2 — after the M5-follow-up investigation

## TL;DR

The second milestone-sequence rework, run against findings-log **entry 7** and its
three addenda (workflow re-test, loop control, super-pipeline). Outcome: **two
milestones inserted after Milestone 5**, and everything from the old "Persistent
work and knowledge" onward shifts down by two.

- **M6 — Evaluation task suite.** The near-term work can only be judged by running
  it against tasks, and the MVP fixture (4→6 synthetic tasks) is too small and
  too narrow to separate arms or to represent common dev requests.
- **M7 — Static supervised workflow.** The investigation established the near-term
  deliverable concretely — a supervised assistant on 7–8B, built as a cheap
  reliable spine with heavy stages fired conditionally — and produced the
  calibration data to specify it.

The old Milestones 6–14 keep their text and become 8–16.

> **Motto:** Build the ruler before the thing it measures; then build only the
> part the evidence asks for.

## Why now

Rework 1 (`06-sequence-rework-01.md`) closed the MVP slice with "no reordering"
and a recalibration: a 7B does the *doing* with scaffolding, not the *judging*;
the deliverable splits into a supervised assistant now and a self-improving loop
later. It named the next task as "a deeper re-evaluation of achievable goals
before M6 executes."

That re-evaluation happened as four experiments (findings-log entry 7):

| experiment | what it established |
|---|---|
| attractor census | where a 7B's motion is reliable (emit-the-whole-file; false-premise blindness; concern-drop under load) and where it is not (any verdict framing) |
| judge-lab | no reviewer framing — neutral, adversarial, structured, K=5 voted — beats an approval bias; execution is the only reliable verification lever; deterministic core alone scores 9/10, the 7B panel drags it to 6/10 |
| loop-lab (bundle D) | a test-gated loop with an incumbent-protected keeper + escalate-on-stall gets 9/12 at 1–3 calls/task, **0 regressions**, solves the false premise for free |
| super-pipeline | stacking every idea, always on: worse-or-tied on 5/6 tasks, one real win (multi-concern, via concern-split + combined-score keeper), two self-inflicted regressions, and **four stages that changed zero outcomes in 12 runs** |

Two things fall out of that and neither fits the existing sequence:

1. **The toy fixture cannot carry the next phase.** Every finding above is
   qualified by "N ≤ 3, 6 tasks, read the transcript not the score." M7 and every
   adaptive milestone after it need a real ruler first.
2. **The static workflow is now specifiable** — the labs produced the flow, the
   conditional-firing rules, and the counterfactual attribution that says which
   stages earn their calls. That is a milestone's worth of work and it is the
   tier-1 deliverable, not a detour on the way to persistence.

## The inserted milestones

### M6 — Evaluation task suite

A taxonomy of dev-request shapes × trap types, 20–30 tasks each with a
deterministic partial-credit check, an explicit correct-vs-plausible-wrong
discriminator, a `stresses:` tag, and (where pushing back is right) a
`decline_correct` flag. Each task also ships a pre-existing passing test so the
regression guard is exercised suite-wide. Plus a conceptual document — how the
project evaluates — so later milestones share one method.

Full spec: `10-technical/10-evaluation-task-suite.md`. Seed:
`experiments/M5-intelligent-orchestration/fixture_workflow/` (wf1–wf6).

**Evidence question:** does a trap-structured suite separate pipeline variants a
toy fixture cannot, and does it surface failure modes the MVP fixture missed?

### M7 — Static supervised workflow

The **leading candidate** from `loop_lab` + `pipeline_lab` is below; M7 keeps the
strategy space open (see `01-milestones.md` → M7 "Strategies still to explore" —
fixed blind K-way synthesis, dueling advocates with executable claims,
cross-model review, task-type-adaptive stage selection, the NL orchestrator
reconsidered on harder tasks). The M6 suite exists to choose among them at scale.

Leading candidate — a specified, observable component on the M3 floor:

- **spine** = d_loop (test-gated iteration, incumbent-protected keeper,
  escalate-on-stall);
- **conditional stages**: premise audit (always — cheap, catches false premises);
  concern-split + combined-score keeper (conjunctive objectives — the multi-
  concern win); "no behavioural signal → escalate" (refactor / no-test tasks);
- **dropped** from the super-pipeline: dual impl-specs, alignment check, blind
  test synthesis as built (zero outcome influence in 12 runs);
- **fixed before reuse**: no plan injected into the implementer context; plain
  framing for greenfield; no lone model probe may flip a terminal;
- **observability**: every stage records whether it changed the terminal, so
  redundant stages retire on evidence.

Static by choice — the M5 orchestrator's only gain was adaptive retry, already in
the spine, at 5–7× cost. The orchestrator returns as a comparison arm.

**Evidence question:** on the M6 suite, does the conditionally-staged static
workflow beat both the plain monolith and the always-on super-pipeline on
outcome-per-call, and does it degrade safely on the tasks it cannot do?

## Milestone number mapping

| was | is | title |
|---|---|---|
| — | **M6** | **Evaluation task suite** (new) |
| — | **M7** | **Static supervised workflow** (new) |
| M6 | M8 | Persistent work and knowledge |
| M7 | M9 | Context governance measurement |
| M8 | M10 | Project-level adaptation |
| M9 | M11 | Safety response mechanisms |
| M10 | M12 | System-level candidate tuning |
| M11 | M13 | Reproducible generations and promotion |
| M12 | M14 | Meta-evaluation |
| M13 | M15 | Cross-generation comparison |
| M14 | M16 | Bootstrap generation closure |

Earlier documents' references to "Milestone _n_" for _n_ ≥ 6 mean the
pre-rework-2 number unless dated after 2026-09-02. `01-milestones.md` internal
cross-references (M3 → the safety/literature pass at M11; the scope-of-feedback
note at M10/M12/M14) are updated in place.

## What did not change

- The project objectives and mantra; the constrained-intelligence thesis; the
  local-model end goal.
- The invariant floor's content, the gate's determinism, the reasoning/runtime
  split, the just-in-time specification rule.
- The **content** of the shifted milestones (M8–M16) — only their numbers.
- The recalibration from rework 1: two deliverable tiers (supervised assistant
  now; self-improving loop gated on a second judgment source / better hardware).
  M7 *is* tier 1, made concrete.
- The post-MVP backlog in `06-sequence-rework-01.md`, including the "second
  judgment source" item — still owned by the goal re-evaluation, now partly
  discharged (the answer: a stronger/independent reviewer model, not 7B prompt
  tuning; hardware path already chosen).

## Next

Execute in order:

1. **M6** — write `10-technical/10-evaluation-task-suite.md` (done as part of this
   rework), then build the suite: fold in wf1–wf6, add the new tasks by trap
   class, wire a runner that reports per-task partial credit + `stresses` slices.
2. **M7** — specify the static workflow (`10-technical/11-static-workflow.md`),
   implement it from the `loop_lab`/`pipeline_lab` parts with the drops and fixes
   above, run it against the M6 suite versus monolith and super-pipeline, write
   the findings entry.
