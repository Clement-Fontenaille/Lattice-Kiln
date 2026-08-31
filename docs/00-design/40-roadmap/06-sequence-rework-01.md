# Sequence Rework 1 — after the MVP slice (end of Milestone 5)

## TL;DR

The first scheduled milestone-sequence rework, run against findings-log entries
1–6. Outcome: **the sequence holds — no milestone is reordered.** The MVP slice
(M0–M5) built and exercised the full stack (measured hardware → reproducible
environment → observability → enforced invariant floor → ephemeral processors →
LLM orchestrator), and every core hypothesis got a *narrow* answer at a *high*
cost. The adjustments are to framing and backlog, not order.

> **Motto:** The floor is real; every gain above it is still narrow and expensive.

## When and why

The execution cadence schedules the first sequence rework here, so findings
accumulate into one coherent revision rather than causing drift
(`00-project/04-execution-cadence.md`). This document is that revision. It does
not restate the findings — see `05-findings-log.md` entries 1–6.

## What the MVP established

| Milestone | Left standing |
|---|---|
| M0 | The inference envelope: 7B Q4/Q5 ≤16k, ~40 tok/s, VRAM-fit a hard binary with a ~10–20× offload cliff; per-role model switching not viable. |
| M1 | A scripted baseline environment that verifies green in place; the clean-machine replay is owed. |
| M2 | An append-only event model + recorder that made 40 real runs reconstructable, including for questions never designed into the schema. |
| M3 (reduced) | A deterministic deny-list gate + capability model + provisional invariant list; every real effect routed through it; effect types carved cleanly for the 3/9 seen. |
| M4 | A processor runtime; monolith vs a fixed planner→implementer→reviewer chain — the chain did not beat the monolith. |
| M5 | An LLM orchestrator over that runtime — 7/8 vs monolith 6/8 vs fixed chain 5/8, the win entirely from adaptive retry, at ~5× cost. |

## Findings 1–6, one line each

1. **M0 — confirms.** The constrained-intelligence constraint is real, binary, and
   sharp-edged.
2. **M1 — inconclusive.** Scripted surface verifies green; six manual/host-specific
   breaks enumerated; clean-machine replay not done.
3. **M2 — confirms.** Runs answer unplanned questions by cross-record join —
   provided the effect envelope carries structured outcome, not prose.
4. **M3 — inconclusive, leaning confirms.** Types carved cleanly for what was
   seen; gate never tripped on benign supervised work; "a conclusion is a type-4
   effect" was a choice, not self-evident.
5. **M4 — inconclusive, leaning weakens.** A non-looping role split did not beat a
   monolith; independent review with no revision edge was inert.
6. **M5 — confirms, narrowly.** NL orchestration beat both, by +1/8, entirely via
   adaptive retry, at ~5× cost; understandable for acting, weak for stopping.

## Sequence decisions

**1. No reordering of M6–M14.** Every entry recorded "no reorder". The sequence
articulates: each milestone could be built from what the previous ones produced.
The later entries stay deliberately loose.

**2. The re-test of M4/M5 at larger N is folded into later milestones, not a new
one.** The M4/M5 comparisons are N=8 and within noise. The productive re-test
needs (a) the reviewer→implementer revision loop as a first-class element — now
in `10-technical/08-orchestrator-contract.md` — (b) a non-naive context assembler,
which is exactly what Milestone 7 exists to make measurable, and (c) durable work
records (Milestone 6). Re-running the comparison is therefore a task inside M7/M8,
tracked in the backlog below, not a milestone insertion.

A first pass of this re-test was run at M5 close (findings-log entry 6
addendum): six workflow-shaped tasks, tuned role prompts, the fixed loop given a
fair iteration budget, N=3. It sharpens the picture rather than changing the
sequence — **decomposition's benefit is real but concentrated on multi-file and
multi-concern work** (cross-file bug: monolith 3.0/5 vs decomposed 5/5;
multi-concern: monolith 2/6 algo and 0/4 docs and 0/3 TODO vs decomposed 6/6,
2/4, 3/3), pure overhead elsewhere, at 5–7× the model calls. It also surfaced two
implementation gaps now recorded on spec `08` (an unimplemented repetition
stopping rule; a planner that over-blocks) and a constraint on `07` (a 7B
implementer is degraded by conversational handoff context). The full M7/M8
re-test should raise N, add a degraded-context monolith arm, and vary task size.

**3. Adaptive retry is promoted from an M5 incidental to a named orchestrator
element.** Done in spec `08` (the decision record and terminal states). No
sequence effect; recorded here so the promotion is traceable.

**4. M3 full-form completion is unchanged.** The reduced form is done
(findings-log entry 4). Milestone 9 still owes: composition/sequence-check
hardening, gate-alter, the accumulation threshold, and the literature-grounding
pass (moved into M9 by the earlier scoping decision). No reordering.

**5. The post-MVP backlog is confirmed and consolidated** (below).

## Consolidated post-MVP backlog

Carried forward from the findings, to be scheduled by the milestone that needs
each — not a separate track.

- **Hardware as a variable** (entries 1, 2). A replayable procedure to
  re-bootstrap the environment and re-characterise the inference envelope on
  different hardware, and a statement of what in the design set may depend on
  host-specific envelope numbers. Owner: the eventual bootstrapper design + M11.
- **Clean-machine M1 replay** (entry 2). The definitive test that the scripts
  build the baseline from nothing. Owner: whenever a second controlled machine is
  available.
- **Observability envelope contract** (entries 3, 6). The effect envelope must
  carry structured outcome (verdict, terminal reason), not free text, because
  cross-record joins are how unplanned questions get answered. Owner:
  `10-technical/02-observability-event-model.md` open contracts, sharpened by M6.
- **Orchestrator stopping semantics** (entry 6). `declined` distinct from
  `blocked`, each with a required reason; a rationale required on stop decisions.
  In spec `08` now; validate at the M4/M5 re-test.
- **Editor-agent frontend choice** (entry 2). Cline stays for the MVP; weigh a
  documented `config.yaml`-first alternative at the rework. Owner: bootstrapper
  design.
- **M9 debt** (entry 4). Sequence-check hardening, gate-alter, accumulation
  threshold, literature-grounding pass — all in Milestone 9 as planned.

## What did not change

- The MVP definition, the milestone motivations, the invariant layer's content
  and the gate's determinism, the reasoning/runtime split, the just-in-time
  specification rule. None of the findings touched a foundational constraint.

## Next

Milestone 6 — persistent work and knowledge. First milestone past the MVP slice;
its evidence question is not yet written (it is now *current + 1* and may be
decomposed).
