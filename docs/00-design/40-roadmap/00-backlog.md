# Backlog

_Updated: 2026-09-11 — structure and maintenance rules: [`README.md`](README.md)._

> **Motto:** Every phase should make the next design decision easier.

## P0 — Ongoing spec / architectural rework

**Every row here blocks P1.** A gap that blocks nothing is written into the
document it concerns as an open contract, not parked here
([`README.md`](README.md) → what an item carries).

| Item | Target | Source | Blocks |
|---|---|---|---|
| Static workflow contract | `10-technical/11-static-workflow.md` — **owed** | [M7](01-MILESTONES/07-static-supervised-workflow.md) | P1 step 2 onward |
| Two-mode interaction requirement | [`08-orchestrator-contract.md`](../../10-technical/08-orchestrator-contract.md), spec 11 | [`10-foundations/07`](../10-foundations/07-the-integrated-system-and-its-operator.md) | P1 step 2 — an input to spec 11, not a follow-up edit |
| Decomposition has no specification counterpart | new, or within spec 11 | [`22-arch-cognition/08`](../22-arch-cognition/08-decomposition.md) | P1 step 2 — concern-split is a decomposition |
| Structured role-to-role handoff | open contract on [`07`](../../10-technical/07-naive-context-assembly.md) and [`08`](../../10-technical/08-orchestrator-contract.md) — close it | findings 6, 7 | P1 step 3 |
| `02` rework not carried into cognition, runtime, or the invariant layer | [`22-arch-cognition/02`](../22-arch-cognition/02-processors.md), [`03`](../22-arch-cognition/03-orchestrator.md), [`20-arch-runtime.md`](../20-arch-runtime.md), [`25-arch-invariant-layer/01`](../25-arch-invariant-layer/01-invariant-enforcement.md) — **partly carried 2026-09-11**: reads-vs-effects landed in [`20-arch-runtime.md`](../20-arch-runtime.md)'s new §The path an invocation takes, which states that a read is capability-gated only while an effect also passes the invariant gate. Thinking, Feedback, and reversibility risk-evaluation are still owed, and the two cognition documents have received none of it | [`10-foundations/02`](../10-foundations/02-reasoning-vs-runtime.md), 2026-09-10 pass (Thinking, Feedback, reads-vs-effects, reversibility risk-evaluation) | M8's decomposition into P1 — cannot specify the ingesting processor without it |
| `03` rework not carried into observability or cognition | [`26-arch-observability/01`](../26-arch-observability/01-observability.md), [`22-arch-cognition/02`](../22-arch-cognition/02-processors.md); candidate structure for the handoff row above | [`10-foundations/03`](../10-foundations/03-evidence-belief-and-provenance.md), 2026-09-10 pass (Mode of acquisition, Weighing claims, Friction/Convergence, Scope, Provenance as a DAG, souvenir) | P1 step 3, as the answer the handoff row is missing; M8's decomposition |
| `04` rework — two passes; carried into architecture, not yet into specification | [`23-arch-context-management/01`](../23-arch-context-management/01-context-manager.md) — **carried 2026-09-11**: the actor now states register / track / recall, with knowledge-base retrieval as an ordinary model-initiated tool call rather than a servicing path of its own, and the recall policy named as a required-but-unspecified responsibility. [`21-arch-knowledge-model/01`](../21-arch-knowledge-model/01-knowledge-model.md) — **carried the same day**, taking the query-surface half (breadth, depth, matching mode). What remains owed is the specification side: [`10-technical/07-naive-context-assembly.md`](../../10-technical/07-naive-context-assembly.md), and [M9](01-MILESTONES/09-context-governance-measurement.md) itself (both self-cite the **2026-09-05** phrase "redundancy, not volume" verbatim as an open contract feeding this row — that phrase no longer stands alone in `04`, so the citation itself is stale, not only the implementation) — owed | [`10-foundations/04`](../10-foundations/04-context-as-governed-resource.md): **2026-09-05** pass ("too much is a relation, not a property"); **2026-09-10/11** pass (the shape of a context — an artifact is what a crossing into conversation, `01`'s fourth location, produces from the external world, the knowledge base, or the model's own weights; a context is the set of artifacts currently live, judged on coverage vs. integration; four-way failure modes on that basis — Insufficiency, Redundancy, Uselessness, Overload; the live-context tracking requirement; a track/decide obligation named per mode; the objective-validity boundary — already-satisfied, false-premise, under-specified — named as a processor judgment context assembly feeds but does not make; context selection reframed as a forced choice over an index of not-yet-taken crossings, needing arbitration, distinct from and not inheriting this project's self-judgment-unreliability evidence) — the second pass supersedes and narrows the first's redundancy claim rather than merely adding to it | M9's context-quality metric — M9's own file claims this is already tracked here; it was not, until now |
| `05` rework not carried into cognition or observability | [`22-arch-cognition/02`](../22-arch-cognition/02-processors.md) (ephemeral processors), possibly [`26-arch-observability/01`](../26-arch-observability/01-observability.md) — owed | [`10-foundations/05`](../10-foundations/05-ephemeral-conversation-curated-memory.md), 2026-09-10 pass (Collapsing, Curated memory rebuilt, Scope handed to `03`) | M8's decomposition into P1 — this is M8's own subject document |

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
