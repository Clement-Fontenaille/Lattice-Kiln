# Backlog

_Updated: 2026-09-13 — structure and maintenance rules: [`README.md`](README.md)._

> **Motto:** Every phase should make the next design decision easier.

## P0 — Ongoing spec / architectural rework

**Every row here blocks P1.** A gap that blocks nothing is written into the
document it concerns as an open contract, not parked here
([`README.md`](README.md) → what an item carries).

**The specification inventory is discharged.** The architecture pass of
2026-09-11/13 owed the specification layer twelve documents: nine rewrites and
three that did not exist. All twelve are written. `10-technical/` now holds a
specification counterpart for every actor in the architecture band, and the
cross-layer claims — reads in the gate's input domain, the dead context bundle,
the live set as an index, mandate conformance, the turn input as the recorded unit
— are carried on both sides.

What remains below is what that pass did **not** cover.

| Item | Target | Source | Blocks |
|---|---|---|---|
| **Decomposition has no specification counterpart** | new document, or within [`11-static-workflow.md`](../../10-technical/11-static-workflow.md). That document specifies concern-split as one conditional stage of one workflow, which is not the same as specifying decomposition: fork/join versus continuation, what a recombination step consumes, and how a split's parts are evaluated against the composite are all untouched | [`22-arch-cognition/08`](../22-arch-cognition/08-decomposition.md) | P1 step 2 — concern-split is a decomposition |
| **Structured role-to-role handoff** | open contract on [`07`](../../10-technical/07-naive-context-assembly.md) and [`08`](../../10-technical/08-orchestrator-contract.md). The requirement is normative on both — prior-step output is structured, never appended as narration — and the structure itself is unspecified. Now sharper than before: the handoff arrives as a **crossing** rather than as a bundle field, so the question is what the handoff read looks like | findings 6, 7 | P1 step 3 |
| **Who assigns a reversibility class, and how it is carried** | [`01-effect-vocabulary.md`](../../10-technical/01-effect-vocabulary.md) open contract. [`10-foundations/02`](../10-foundations/02-reasoning-vs-runtime.md) argues the proposing side — an effect irreversible by nature still needs a risk evaluation before it is proposed, reasoning-based rather than a static type property or a runtime check. Not reconciled with a concrete carrier. Sharpened by the scope check, whose pre-effect half fires **on exactly this classification** | [`10-foundations/02`](../10-foundations/02-reasoning-vs-runtime.md); [`03-capability-authority-model.md`](../../10-technical/03-capability-authority-model.md) | P1 — the irreversible half of the scope check has no trigger without it |
| **M9 self-cites a phrase that no longer stands alone** | [M9](01-MILESTONES/09-context-governance-measurement.md) quotes [`10-foundations/04`](../10-foundations/04-context-as-governed-resource.md)'s **2026-09-05** "redundancy, not volume" verbatim as an open contract. The second pass superseded and narrowed that claim rather than adding to it, so the citation is stale, not only the implementation | [`10-foundations/04`](../10-foundations/04-context-as-governed-resource.md) | M9 |
| **G4 has no owner** | [`05-provisional-invariant-list.md`](../../10-technical/05-provisional-invariant-list.md) G4 requires a functioning scope check and no milestone builds one. The specification is complete ([`03-capability-authority-model.md`](../../10-technical/03-capability-authority-model.md)); a system without the check is invalid rather than degraded, and what stands in for it today is the human in the loop | [`10-foundations/07`](../10-foundations/07-the-integrated-system-and-its-operator.md) | Nothing yet — it should |

## P1 — Work in progress

**[M7 — Static supervised workflow](01-MILESTONES/07-static-supervised-workflow.md)**

1. **Decision pending — scope.** Back half only, or back half plus front half. The
   front half depends on [M9](01-MILESTONES/09-context-governance-measurement.md);
   the back half has no open dependency. *Proposed: back half now, front half
   recorded as an open contract.*
2. **Specify** — P0 row 1, scoped by the decision above.
3. **Build** — after the spec. Needs the handoff-framing row in P0.
4. **Run against the M6 suite** — needs E0 (P2) for the comparison to be
   interpretable.
5. **Findings entry.**

## P2 — Short term work to address next

- **E0 — suite construct validation.**
  [`08-next-experiments.md`](08-next-experiments.md) → E0. Blocks interpretation of
  P1 step 4. Possibly answerable from runs already recorded.
- **Next milestone after M7 — decided, 2026-09-10.**
  [M8 — Persistent work and knowledge](01-MILESTONES/08-persistent-work-and-knowledge.md),
  then [M9 — Context governance measurement](01-MILESTONES/09-context-governance-measurement.md)
  as the framework that measures M8's corpus sweep (E6). This does not resolve
  whether M9 is also needed earlier as a prerequisite for M7's front half — that
  is M7's own open scope decision (P1 step 1), independent of this ordering.
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
| [M3 — Invariant floor](01-MILESTONES/03-invariant-floor.md) | **open.** Its remaining items are owned by M11. |
| [M10 — Project-level adaptation](01-MILESTONES/10-project-level-adaptation.md) | — |
| [M11 — Safety response](01-MILESTONES/11-safety-response.md) | Gates M12. Closes M3. |
| [M12 — System-level candidate tuning](01-MILESTONES/12-system-level-candidate-tuning.md) | M11, and a second judgment source. |
| [M13 — Reproducible generations](01-MILESTONES/13-reproducible-generations-and-promotion.md) | Relaxes invariant H3. |
| [M14 — Meta-evaluation](01-MILESTONES/14-meta-evaluation.md) | — |
| [M15 — Cross-generation comparison](01-MILESTONES/15-cross-generation-comparison.md) | A second resident model. |
| [M16 — Bootstrap generation closure](01-MILESTONES/16-bootstrap-generation-closure.md) | — |

### Blocked externally

- **A second judgment source.** Needs a stronger or independent reviewer model —
  the planned second GPU. Gates M12 onward.
- **Clean-machine M1 replay.** Needs a second controlled machine.
- **External signal** — [`70-THINKING/01-use-cases.md`](../../70-THINKING/01-use-cases.md)
  §2 is empty. Needs users. `10-foundations/07`'s population obligation is
  uncheckable without it.

### Unscheduled

- **Hardware as a variable.** A replayable re-bootstrap and envelope
  re-characterisation, plus a statement of what in the design set depends on
  host-specific numbers. Owner: the bootstrapper design, at the latest M16.
- **Editor-agent frontend choice.** Owner: the bootstrapper design.
- **Experiments E1–E5 and E-corpus.**
  [`08-next-experiments.md`](08-next-experiments.md). E4 gated on E0.
- **Repetition stop unimplemented.** [`08-orchestrator-contract.md`](../../10-technical/08-orchestrator-contract.md)
  requires it; `run_orchestrated` does not implement it. A defect against a
  written contract, not an open question — owner is whatever milestone next drives
  the orchestrator.
- **`Exercised by` lines absent across [`10-technical/`](../../10-technical/README.md).**
  Mechanical rollout of a 2026-09-05 convention; recoverable from the findings
  entries.
- **Prose discipline predates the set it governs.**
  [`02-documentation-philosophy.md`](../00-project/02-documentation-philosophy.md)
  → prose discipline was added 2026-09-05. Documents written before it have not
  been read against it. Debt created by that change, recorded here because a design
  document has no open-contract section to hold it.
- **2026-09-10 foundations pass predates M10–M16's framing.** `03`, `02`, `01`,
  and `05` gained Mode of acquisition, Weighing claims, Friction and Convergence,
  Thinking, Feedback, Scope, and Collapsing; every later milestone implicitly
  assumes a knowledge and reasoning substrate and was written before any of it
  existed in named form. Not blocking — none of their own evidence questions
  depend on the new vocabulary yet — so not P0. Carry into each as it is
  decomposed, the way M8 and M9 already were on 2026-09-10.
- **`10-technical/` only partly checked against the 2026-09-10 foundations pass.**
  Two files were checked directly: `01-effect-vocabulary.md` (found real friction —
  `02`'s Feedback section had claimed local reads cross the boundary as effects;
  the vocabulary already excludes reads by name; `02` was corrected, and the
  vocabulary's reversibility-assignment open contract now cites `02`'s risk-
  evaluation answer) and `09-orchestrator-runtime-boundary.md` (consistent as
  found, no change needed). `00-06-08` and `10` have not been checked. This is
  the exact failure this document's own history names twice — the spec set
  looking correct while describing an older design — so treat as live debt, not
  a closed audit.
- **Naming theme decided and never applied.** `00-design/90-notes/04-naming-theme`
  (no file extension) is marked **Decided** with propagation owed. Zero occurrences
  in the set across the whole MVP. Needs applying or downgrading to *considered,
  not adopted* — a standing decision nothing honours misleads a cold reader.
- **No repository README.** Nothing at the repo root states what this is or where
  to start. First file anyone opens.
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
  items are not. Given its own folder rather than folded into `21` because a claim
  there is append-only and superseded while a work item is mutable by design. Its
  number sits above `27`'s only because the lower ones were taken.
