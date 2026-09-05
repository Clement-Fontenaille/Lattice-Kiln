# Sequence Rework 1 — after the MVP slice (end of Milestone 5)

> **Numbering banner.** This is a dated decision record and keeps the milestone
> numbering that was in force when it was written — **before rework 2**. Read
> every "Milestone _n_" here for _n_ ≥ 6 through the mapping table in
> [`01-MILESTONES/README.md`](01-MILESTONES/README.md). In particular: "M6" here
> is persistent work and knowledge (now M8), "M7" is context governance
> measurement (now M9), and "Milestone 9" is safety response (now M11).
>
> Numbers are now stable identifiers and no future document will need a banner
> like this one. The live backlog is [`00-backlog.md`](00-backlog.md); the items
> below are preserved as the record of what was carried forward at the time.

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
not restate the findings — see `../50-findings/` entries 1–6.

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
- **Repetition stopping rule + planner over-blocking** (entry 6 addendum). Spec
  `08` requires a repetition stop; `run_orchestrated` does not implement it, and
  an orchestrator spawned the planner 4–6× consecutively. The tuned planner also
  over-returns `blocked` on ordinary "not built yet" objectives. Owner: whatever
  milestone next drives the orchestrator (M7/M8 re-test).
- **Role-to-role handoff framing** (entry 6 addendum; refined by entry 7). A 7B
  implementer stops emitting effects when its context carries *unlabelled*
  conversational text; a plan or critique in a **named, structured section** is
  tolerated (census). Prior-step output must be structured, not appended as raw
  narration. Owner: `10-technical/07`, exercised at M7.
- **Second judgment source** (entry 7). No 7B reviewer framing — neutral,
  adversarial, structured, or voted — beats "assert the property and approve";
  the deterministic gate + run-the-test scores 9/10 where a test exists, the 7B
  panel drags it to 6/10. The self-improving tier's evaluation edge therefore
  needs a human, an automated check, or a stronger/reasoning reviewer model — the
  last enabled by the planned second GPU. This moves the second-GPU path from
  "nice to have" to the gating dependency for tier 2. Owner: the goal
  re-evaluation, then M8/M10.
- **Editor-agent frontend choice** (entry 2). Cline stays for the MVP; weigh a
  documented `config.yaml`-first alternative at the rework. Owner: bootstrapper
  design.
- **M9 debt** (entry 4). Sequence-check hardening, gate-alter, accumulation
  threshold, literature-grounding pass — all in Milestone 9 as planned.

## What did not change

- The MVP definition, the milestone motivations, the invariant layer's content
  and the gate's determinism, the reasoning/runtime split, the just-in-time
  specification rule. None of the findings touched a foundational constraint.
- The project objectives. The constrained-intelligence thesis and the
  local-model end goal stand unchanged.

## Recalibrated expectations (post-MVP)

The MVP evidence did not change the objectives, but it moved the **expected
benefit** down, and that shift is worth recording so a later reader is not
surprised by it.

**The finding driving the recalibration.** A constrained local model (7B-class,
the size that fits the common 8 GB hardware) does the *doing* — implement, fix,
refactor — acceptably with scaffolding, and role decomposition demonstrably helps
on multi-file and multi-concern work (findings-log entry 6 addendum). But it does
not do the *judging* reliably: the reviewer role, even tuned, hallucinates
acceptance criteria and mis-evaluates correct code. A feedback loop is only
beneficial if its evaluation is well above noise; on current 7B it is not. This
is the correlated-blind-spot / Goodhart risk the design already names, now
observed rather than anticipated.

**Consequence for the goal, not the goal itself.** The deliverable separates into
two tiers:

1. **A supervised local assistant on 7–8B** — achievable now. Observability, the
   safety floor, a reproducible environment, ephemeral roles where they help, a
   human in the evaluation seat. A real, shippable outcome.
2. **A local self-improving loop** — gated on either a higher hardware tier
   (14B-class resident, ~16 GB VRAM, where judgment starts becoming viable) or on
   small models improving into that capability over time. The architecture is
   model-agnostic by construction so it rides that curve; the scaffolding —
   observability, safety, orchestration — is the slow, model-independent part and
   building it now is the bet that pays off when the model catches up.

**"Promising signal on 7B" is a legitimate milestone outcome.** The next phases
(M6+) are not justified as scaffolding alone. Each should also be a genuine
attempt to get a real result on 7B, with a bar beyond "the code exists":

- **M6** — a processor that reuses a stored finding/decision from an earlier run
  measurably beats one starting cold.
- **M7** — the naive assembler's observed failures (wrong-file writes on wf1, the
  missed helper on wf4/wf6) are quantifiable, and a less-naive assembler moves
  the metric.
- **M8** — second-pass work in the same repository improves without polluting
  global behaviour, on even a handful of tasks.

A milestone that lands "mechanism sound, no signal yet at 7B" is a weaker but
still honest finding. The M5 method applies: at 7B / low N, read the transcript
*mechanism*, not the aggregate score.

## Next

**A deeper re-evaluation of achievable goals**, against these rework notes and the
six MVP findings together, *before* M6 is executed in earnest. It should restate,
concretely and per adaptive milestone (M6–M14), what "success on constrained
hardware today" looks like versus what waits on better models or hardware, and
whether any later milestone's framing needs revising in light of the evaluation
ceiling. That re-evaluation is the first task of the post-MVP phase; M6's
evidence question and decomposition follow from it.
