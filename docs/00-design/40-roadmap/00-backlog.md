# Backlog

_Updated: 2026-09-15 — structure and maintenance rules: [`README.md`](README.md)._

> **Motto:** Every phase should make the next design decision easier.

## P0 — Ongoing spec / architectural rework

**Every row here blocks P1.** A gap that blocks nothing is written into the
document it concerns as an open contract, not parked here
([`README.md`](README.md) — what an item carries).

**Nothing in this band blocks M7 any more.** The specification inventory is
discharged, the handoff contract is closed, and decomposition turned out to need no
specification of its own — creating a task is effect 4a, the formulation rides on it,
and how a model expresses a split is a build decision. What is left below blocks later
work, and the rows say which.

**P0 is empty.** Every row has closed, and the last two closed on assignment and on a
cascade rather than on new design: the scope check and the scope writer got an owner —
now [M17](01-MILESTONES/17-mandate-chain.md), split out of M11 on 2026-09-14 — and
M9's stale self-citation is corrected against what `10-foundations/04` now holds.

**Closed since the last revision of this band**, each in the document that owns it
rather than here: the structured role-to-role handoff; the reversibility-class carrier,
now a placeholder that every tool call is irreversible so every one gets the pre-effect
check; five of the seven gaps the trajectory walk found; writing sub-objectives, which
needed nothing specified; the duplicate task—artifact edge set, resolved by removing the
work record's `attachments`; and G4's substrate precondition, which stopped being an
unscheduled measurement when the **bootstrap occupancy test** became a requirement
(`05-provisional-invariant-list.md`).

**What emptied this band was mostly a question rather than work.** Asking *is this
design or implementation?* of each row dissolved three of them: the scope check's
remaining shape, writing sub-objectives, and the reversibility-class carrier were build
decisions that existing contracts already covered. Worth keeping in view the next time
an open contract looks blocking.

## P1 — Work in progress

**[M7 — Static supervised workflow](01-MILESTONES/completed/07-static-supervised-workflow.md)
— closed 2026-09-14.** All five steps done; findings-log entry 10. Back half only, as
scoped; the front half stays an open contract in
[`11-static-workflow.md`](../../10-technical/11-static-workflow.md) and is M9-gated.

**[M8 — Persistent work and knowledge](01-MILESTONES/08-persistent-work-and-knowledge.md)
is next.** Six work packages, named in that file. Packages 1–3 are the three
specification documents written on 2026-09-13 and are independent of each other;
package 4 is the wiring between them and is the one most likely to be
underestimated.

## P2 — Short term work to address next

- **E0 — suite construct validation. Promoted by findings-log entry 10.**
  [`03-research-and-evaluation/`](03-research-and-evaluation/) → E0. M7 and `dloop`
  both scored 24/30 while **four tasks flipped between them**, none touched by the
  stages M7 added — so a four-task churn is available from variance alone at N=1. The
  suite discriminates designs that differ in kind and not designs that differ by a
  task, and nothing had measured that before. Possibly answerable from runs already
  recorded.
- **Repetition is no longer optional for small-effect comparisons.** Same source. Any
  arm comparison whose expected effect is one or two tasks needs N > 1 before it means
  anything. This does not apply retroactively to M4/M5/M6's large effects.
- **Next milestone after M7 — decided, 2026-09-10.**
  [M8 — Persistent work and knowledge](01-MILESTONES/08-persistent-work-and-knowledge.md),
  then [M9 — Context governance measurement](01-MILESTONES/09-context-governance-measurement.md)
  as the framework that measures M8's corpus sweep (E6). This does not resolve
  whether M9 is also needed earlier as a prerequisite for M7's front half — that
  is M7's own open scope decision (P1 step 1), independent of this ordering.
- **The bootstrap occupancy test — runnable now, and nothing schedules it.**
  It is [M17](01-MILESTONES/17-mandate-chain.md)'s first work package and blocks the
  rest of that milestone, but it depends on nothing: no durable stores, no workflow,
  no loop. It answers **both** remaining rows of `STATUS.md`'s blocking-holes table
  in one run, and it decides whether a scope check is providable on this host at all.
  M0-shaped and cheap.
- **Two ordering questions the M11 split opened (2026-09-14).** Both are decisions,
  not research, and neither is taken.

  **M17 against M7's suite run.** The scope check puts a model call in front of every
  tool call. M7's evidence question is *outcome-per-call*, comparable back to M4 and
  M5. Turning M17 on before M7 runs breaks that axis. *Proposed: M7's run completes
  first, or M7's arms run with the check off and the findings entry says so.*

  **M17 against M9.** M17 carves a permanent share of the resident envelope for the
  checker's slot. M9 measures Overload against that envelope, so a baseline taken
  before M17 is taken on a different machine than a reading taken after.
  *Proposed: M17 between M8 and M9, which is not the order the row above records.*
- **Re-analyse M4/M5 as paired comparisons before re-running anything.** The arms ran
  on a shared suite, so which tasks *flipped* between arms may be recoverable from data
  already collected. Paired analysis removes task-difficulty variance entirely and
  which scenarios flipped carries far more signal than 6/8 against 5/8, because it names
  a condition rather than a magnitude — this is the cheapest experimental improvement
  available and it needs no new runs. See
  [`27-arch-adaptation-and-evolution/05`](../27-arch-adaptation-and-evolution/05-experiments-and-candidate-systems.md),
  Resolution before precision.
- **M4/M5 re-test at larger N.** Depends on M8 (durable work records) and M9
  (non-naive assembler). Not a milestone; a task inside whichever lands.

## P3 — Unscheduled / Notes

### Milestones not yet scheduled

| | Dependency |
|---|---|
| [M3 — Invariant floor](01-MILESTONES/03-invariant-floor.md) | **open.** Its remaining items are owned by M11 — not M17, which sits above the gate. Its effect-type coverage comes from M8. |
| [M10 — Project-level adaptation](01-MILESTONES/10-project-level-adaptation.md) | — |
| [M11 — Safety response](01-MILESTONES/11-safety-response.md) | Gates M12. Closes M3. Triage, gate-`alter`, decommissioning, the accumulation threshold, sequence-check hardening, the literature pass |
| [M12 — System-level candidate tuning](01-MILESTONES/12-system-level-candidate-tuning.md) | M11, and a second judgment source. |
| [M13 — Reproducible generations](01-MILESTONES/13-reproducible-generations-and-promotion.md) | Relaxes invariant H3. |
| [M14 — Meta-evaluation](01-MILESTONES/14-meta-evaluation.md) | — |
| [M15 — Cross-generation comparison](01-MILESTONES/15-cross-generation-comparison.md) | A second resident model. |
| [M16 — Bootstrap generation closure](01-MILESTONES/16-bootstrap-generation-closure.md) | — |
| [M17 — The mandate chain](01-MILESTONES/17-mandate-chain.md) | **Runs early**, split out of M11 on 2026-09-14. Instantiates **invariant processors** as a category: the scope writer, the scope check. Satisfies G4. First work package is the bootstrap occupancy test, runnable now |

**M10–M16 get no work packages in this pass, deliberately.** Five of the seven have
no evidence question stated, and naming packages under an unstated evidence question
produces a task list nobody can tell is complete. They also all sit behind either M11
or the second GPU, so the packages would be written against a substrate that will have
moved. The rule this follows is already recorded above: *carry the foundations pass
into each as it is decomposed.*

### Blocked externally

- **A second judgment source.** Needs a stronger or independent reviewer model —
  the planned second GPU. Gates M12 onward.
- **Clean-machine M1 replay.** Needs a second controlled machine.
- **External signal** — [`70-THINKING/01-use-cases.md`](../../70-THINKING/01-use-cases.md)
  §2 is empty. Needs users. `10-foundations/07`'s population obligation is
  uncheckable without it.

### Unscheduled

- **Deliberation between agents — parked deliberately, 2026-09-14.** The operator's
  decision: dueling advocates belong with the deliberation mechanisms as a body of
  work, not as one more arm bolted onto M7, and it is a large piece. No milestone
  holds it yet; it takes the next free identifier when it gets one.

  **The judge investigation is what it inherits** (`50-findings/11`), and four results
  there constrain any deliberation design before it is drawn:

  **A reader's value is the difference between its context and the others', not the
  size of its context.** Two instances of one model over one context share their blind
  spots, so their agreement and their disagreement are both sampling variance. Any
  design putting N agents on the same material is running one measurement N times.

  **The unit of independence is the task, not the exchange.** A model that decides
  about a task repeats itself across every turn about that task — in the M7 run one
  judge said `unsound_request` on all six candidates of a task without changing its
  mind. A deliberation of six turns is not six observations, and a design that reads
  convergence as agreement will read stubbornness as consensus.

  **Verdicts do not work at 7B and executable claims might.** The judge scored below a
  constant on the population that required judgement, and its two failure modes —
  matching a change's topic instead of verifying it, and misreading code outright —
  are both comprehension rather than framing. The dueling-advocates shape avoids this
  by construction: the readers emit **falsifiable input/output claims** and the
  *interpreter* adjudicates, so the model supplies material and the machine decides.
  That is the same move `test_synth` makes and the same one `10-technical/11`'s keeper
  makes.

  **And a judge does earn its place in one situation**, which is the only positive
  result the investigation produced: where the check is satisfied, nothing improved,
  and the premise was not doubted. There the check has said *fine* and the open
  question is whether it asked the right thing — no mechanical instrument can answer
  that, and a reader is the only one left. A deliberation design should be built for
  that case rather than for the general one.

  Prior material: `40-roadmap/01-MILESTONES/completed/07-…`, Strategies still to
  explore; `M15`'s reviewer-independence question, which asks the same thing of two
  *different* models and is gated on the second GPU.

- **Experiments packaged as artifacts, air-gapped hosts included
  (2026-09-15).** An experiment's preparation should assume the repo travels as
  an archive to a machine with no network access, runs there, and produces
  artifacts that are repatriated for investigation and only then pushed to the
  forge — not that a forge push is itself how an experiment is packaged.
  Related to the raw-output/`.gitignore` question parked the same day
  (M6/M7 `runs_*/` churn from repeated sweeps) and to "Hardware as a variable"
  below, but distinct from both: this is about an experiment's own portability,
  not the host's. **Blocks the E6 corpus sweep's rented-H100 run**
  (`experiments/M8-persistent-work-and-knowledge/e6_corpus_sweep.py`,
  M8/`08-persistent-work-and-knowledge.md` package 6) — the operator's own
  framing, 2026-09-15: pipeline consolidation is a prerequisite for that sweep,
  not a parallel concern. No owner yet.
- **Hardware as a variable.** A replayable re-bootstrap and envelope
  re-characterisation, plus a statement of what in the design set depends on
  host-specific numbers. Owner: the bootstrapper design, at the latest M16.
- **Editor-agent frontend choice.** Owner: the bootstrapper design.
- **Experiments E1–E5 and E-corpus.**
  One sheet each in [`03-research-and-evaluation/`](03-research-and-evaluation/).
  E4 gated on E0.
- **Repetition stop unimplemented.** [`08-orchestrator-contract.md`](../../10-technical/08-orchestrator-contract.md)
  requires it; `run_orchestrated` does not implement it. A defect against a
  written contract, not an open question — owner is whatever milestone next drives
  the orchestrator.
- **`Exercised by` lines absent across [`10-technical/`](../../10-technical/README.md).**
  Mechanical rollout of a 2026-09-05 convention; recoverable from the findings
  entries.
- **Prose discipline: two folders never read against it.**
  [`02-documentation-philosophy.md`](../00-project/02-documentation-philosophy.md)
  → prose discipline was added 2026-09-05. `00-project/`, `10-foundations/`, the
  architecture band and `10-technical/` have since been rewritten or swept.
  `40-roadmap/` and `70-THINKING/` have not, and `70-THINKING/` is not governed by
  it in any case.
- **2026-09-10 foundations pass predates M10–M16's framing.** `03`, `02`, `01`,
  and `05` gained Mode of acquisition, Weighing claims, Friction and Convergence,
  Thinking, Feedback, Scope, and Collapsing; every later milestone implicitly
  assumes a knowledge and reasoning substrate and was written before any of it
  existed in named form. Not blocking — none of their own evidence questions
  depend on the new vocabulary yet — so not P0. Carry into each as it is
  decomposed, the way M8 and M9 already were on 2026-09-10.
- **Naming theme decided and never applied.** `00-design/90-notes/04-naming-theme`
  (no file extension) is marked **Decided** with propagation owed. Zero occurrences
  in the set across the whole MVP. Needs applying or downgrading to *considered,
  not adopted* — a standing decision nothing honours misleads a cold reader.
- **Praxis thread open.** [`70-THINKING/04-praxis.md`](../../70-THINKING/04-praxis.md).
  Two execution gates — *spec in shape*, *finding is critical* — rest on positions
  it has not taken. Both currently operate on human judgment, which holds while a
  human runs every session and does not hold at
  [M12](01-MILESTONES/12-system-level-candidate-tuning.md).
- **Architecture folder reorg (2026-09-11).** `20-cognitive-architecture` split by
  concern, since only its actors (task representation, processors, orchestrator,
  decomposition) are reasoning/coordinating — the rest were resources or
  constraints, not actors. New layout: `20-arch-runtime.md` (single file, entry
  point), `21-arch-knowledge-model`, `22-arch-cognition`, `23-arch-context-management`,
  `24-arch-permission-layer`, `25-arch-invariant-layer`, `26-arch-observability`.
  `30-adaptation-and-evolution` renumbered into the same band as
  `27-arch-adaptation-and-evolution`, leaving a deliberate gap at `30`. Every
  cross-reference in `00-design/`, `10-technical/`, and `70-THINKING/` was updated
  to match. **Exception, by design:** `50-findings/*.md` and
  `50-PROGRESS/archives/*.md` are append-only and still cite the pre-reorg paths
  (e.g. `20-cognitive-architecture/06-observability.md`) — a reader following one of
  those citations needs this mapping, since the target moved but the citation,
  correctly, did not.
- **`28-arch-work-record` added (2026-09-11).** The consolidation pass after the
  reorg found that work-record mutation (`10-technical/01` type 4) had a schema, a
  capability policy, and exercised M3 runs behind it, while no actor in the band
  held the record it mutates: `22-arch-cognition/01` defines intent and work items
  without storing them, and `21-arch-knowledge-model` holds claims, which work
  items are not. Given its own folder rather than folded into `21` because a work
  item is not a claim, and because its current state must be readable directly on every
  orchestrator loop step rather than by walking a provenance graph. *(The original
  reason — a claim is append-only while a work item is mutable — no longer holds: a
  work item's formulation and scope are fixed at creation too.)* Its number sits above
  `27`'s only because the lower ones were taken.
