# M4 — Ephemeral Processor Experiments

**Milestone:** `40-roadmap/01-milestones.md` → Milestone 4
**Evidence question:** do ephemeral roles, fresh context, and independent review
beat a monolithic agent on a small task set?
**State:** decomposing — specs written, experiment design needs operator input

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
| 3 | Decide the task set | **TODO — operator input** | Size, source, and objective-checkability. See "Open decision". |
| 4 | Processor runtime | TODO | Ollama client (7B Q4/Q5 ≤16k, per M0), effect → `enforce.submit_effect`, event → `event_model.RunRecorder`. Ephemeral: one model context per instance, no carry-over. |
| 5 | Role library | TODO | `implementer` (also the monolith); `planner`, `reviewer`. Free-text role instructions per `06`. |
| 6 | Naive context assembler | TODO | Implements `07`: objective + README + tree + hint/substring file inclusion to budget, with trace. Deterministic. |
| 7 | Comparison harness + run the set | TODO | Arm A vs arm B, N reps. Objective score + reasoning-quality signals. All runs committed. |
| 8 | M2 reconstruction check | TODO | Unplanned question answered from stored records alone → findings-log entry 3. |
| 9 | M3 effect-carving check | TODO | Real effect stream through the gate; note any type blur → findings-log entry 4. |
| 10 | M4 findings-log entry | TODO | Verdict on the ephemeral-vs-monolith hypothesis → entry 5. |

## Open decision — the task set (needs operator input)

The milestone says "a small task set" and "a small set of roles only." Before
building arm B, the task set has to be pinned. Candidate shape:

- **6–10 tasks**, each a self-contained change in a small throwaway repo (or a
  fixture repo committed under the experiment dir), each with an **objective
  pass/fail**: a test that must go green, a lint that must stay clean, a build
  that must succeed.
- Mix of: a straightforward implementation, a bug fix behind a failing test, a
  task with a **false premise** (to see whether either arm correctly `declines`),
  a small refactor, a task needing a second file the naive assembler will
  probably miss (to exercise context starvation).
- Kept deliberately small because the host runs one 7B model at ~40 tok/s and
  each ephemeral task is 3 model calls vs the monolith's 1.

Operator questions:
1. Throwaway synthetic repo, or a real small repo you want to point at?
2. Is 6–10 tasks / N=3 repetitions an acceptable inference budget on this host,
   or should the first pass be smaller (e.g. 4 tasks, N=2)?
3. Any task types you specifically want represented or excluded?

## Notes

- Just-in-time: `06` and `07` are written because M4 needs them; the orchestrator
  contract (M5) is **not** written yet — a fixed harness plays caller for M4.
- The runtime reuses, not reimplements, `experiments/M2-observability-foundation/`
  and `experiments/M3-invariant-floor/`. If either needs a change to be usable
  from a real run, that change is a finding for its milestone.
- A human supervises every run (MVP invariant list, operational stance).
