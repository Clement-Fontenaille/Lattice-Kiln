# Backlog

_Updated: 2026-09-28 — structure and maintenance rules: [`README.md`](README.md)._

> **Motto:** Every phase should make the next design decision easier.

## P0 — Ongoing spec / architectural rework

**Every row here blocks P1.** A gap that blocks nothing is written into the
document it concerns as an open contract, not parked here
([`README.md`](README.md) — what an item carries).

- **The adapter has no owner.** The serialisation a model is asked to speak in — chat
  template, role markers, thinking delimiters, tool-call syntax, tool-result wire
  format — is a design surface with consequences, and no milestone holds it.
  `26-arch-observability` and the runtime band both stop at "the model".

  **It is named in the code and nowhere in the design set.**
  `processor.adapter_fingerprint()` hashes it, `params.adapter` keys it,
  `ollama_client`'s four recovery layers repair what it mangles — and the string
  `adapter` occurs **zero times** across `10-foundations/`, the `2*-arch-*` band and
  `10-technical/`. Defining the term where the design set can see it is the owner's
  first act.

  **Why it blocks rather than waits.** A defect here is indistinguishable from a model
  limit unless something names the layer, so the debt is paid in misattributed
  results. Measured: Nemotron Nano 9B v2 scored 5/31 under another model's chat
  template and 17/31 under its own, twelve tasks flipping to pass and none to fail,
  and read as the weaker model for a week
  (`experiments/M6-evaluation-suite/modelfiles/Modelfile.nemotron9-native`; owed a
  findings entry). `50-findings/12` rests on that misconfiguration.

  **Blocks P1's last package.** M8 package 6 is the E6 corpus sweep on a rented H100,
  where the chat template is ours to supply and Ollama does not exist.
  `M4-ephemeral-processors/backends.py` is verified on the request and parse paths and
  has never run against a live non-Ollama server; the official templates for all three
  models are in `evalkit_store/model_contracts/`.

  **Decide:** a new milestone or a package inside an existing one. Either way the
  owner also inherits the seam (`backends.py` against a live `llama-server --jinja`),
  the per-model template choice, and the question of what belongs in the setup key —
  because `params.adapter` today fingerprints *our* protocol text, which is identical
  across models, while the model-side renderer rides invisibly on the model tag.

## P1 — Work in progress

**M7's front half is still unwritten** — the back half is what closed. It stays an
open contract in [`11-static-workflow.md`](../../10-technical/11-static-workflow.md)
and is M9-gated.

**[M8 — Persistent work and knowledge](01-MILESTONES/08-persistent-work-and-knowledge.md)
is next.** Six work packages, named in that file. Packages 1–3 are the three
specification documents written on 2026-09-13 and are independent of each other;
package 4 is the wiring between them and is the one most likely to be
underestimated.

## P2 — Short term work to address next

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

**Added 2026-09-27, from the model sweep.** Two queue documents ran this work for
four days — one of outsourceable development, one of research — and are **deleted**,
their open items merged here rather than kept as a parallel list. Nothing in them was
load-bearing that is not below.

- **Re-read everything that leaned on the 9B.** Its whole column measured a model
  under the wrong chat template (P0 above). The rows stay valid as *this model under
  this harness* and are worthless as capability. `50-findings/12` needs an addendum,
  and the "609–2635 tokens to escape the thinking block" figure was measured under a
  template that is not the one opening `<think>`.
- **The suite's ladder is two instruments, not one** (`50-findings/17`). Every arm
  from `dloop` upward feeds the implementer the failing subtest **names**; only
  `baseline`, `monolith` and `monolith_recovery` do not. The 6/34 → 27/34 figure
  spans that boundary and no arm crosses it. `monolith_test` — written, never run —
  is the arm that would separate model-chosen probing from harness-driven.
- **The judge fails at aggregation, not at judging** (`50-findings/18`). 89% right per
  condition, 67% per verdict, because the rule is `all(yes)` and the audit stage
  chooses how many conditions to write. The remedy is unjustified from current data:
  relaxing to "at most one no" cuts false rejects 33% → 9%, but the false-accept
  column has n=7. **What would settle it is enough failing attempts**, which no
  current arm produces in quantity.
- **Three arms written and never executed:** `monolith_test`, `author`,
  `author_judge`. Each needs a single-task smoke test before it joins a sweep. The
  `author` pair also grants the audit stage authority its own prompt currently denies
  it, which is a role change and not a flag. **Their reading is gated** on an
  instrument for stages with no mechanical check, which does not exist —
  `03-research-and-evaluation/00-questions.md`, *How is a stage graded when no
  mechanical check exists?*
- **Settings never settled.** Sampling is `0.6 / 0.95` for all three models because
  both Nemotron cards document it for tool calling; qwen inherited it for
  comparability and its own documentation has never been read. The v1→v2 protocol
  rework produced 16/34 both ways and earns no claim — keeping it on clarity grounds
  is defensible, saying it helped is not.
- **Does recovery earn its place, and one defect in the way.** `monolith_recovery`
  beat `monolith` on the 4B and lost on the 9B, both at n=1. The floor it must beat is
  the naive retry, which is now general and journalled, so the comparison is available
  from rows already collected. **Blocked by a live bug first:** `chat()` takes no
  `top_p` while the recovery path passes sampling overrides including it, so a remedy
  carrying one raises `TypeError` — killing precisely the attempts the arm exists to
  evaluate, 8 times on the 9B.
- **`E5`'s fifth convergence criterion, never audited.** Every candidate skill must
  name something it blocked or be marked as not yet observed to block anything. None
  of S1–S8 is **termination**, though it is the prerequisite to all of them and is
  exactly what failed.
- **About twenty analysis scripts resolve a path ending `results/`,** which moved to
  `archive/2026-09-25-pre-tooling-rework/` on 2026-09-27. Mostly correct rather than
  broken — they read the pre-rework corpus, which moved with them — but each needs
  repointing at the archive or at `results_matrix_*`, and saying which.

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

- **Deliberation between agents — parked, 2026-09-14.** Dueling advocates belong with
  the deliberation mechanisms as a body of work, not as one more arm bolted onto M7.
  No milestone holds it; it takes the next free identifier. **Four results in
  `50-findings/11` constrain the design before it is drawn** — read them first; the
  load-bearing one is that verdicts do not work at 7B while falsifiable input/output
  claims might, which is the same move `test_synth` and the keeper already make.
  Prior material: `01-MILESTONES/completed/07-…` (Strategies still to explore), and
  M15's reviewer-independence question, which asks the same of two *different* models
  and is gated on the second GPU.

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
- **Concurrent dispatch, unowned and unused (2026-09-27).** `OLLAMA_NUM_PARALLEL=3`
  is set and `evalkit_pool` exists with a claim protocol, but every sweep runs one
  `run_suite` at a time and `run_suite` walks its tasks sequentially. On this host it
  would buy little — a 9B at 16k leaves 811 MiB of 8192 free, so the slots are
  unusable for the model that needs them most — but on the H100 the memory ceiling
  disappears and serial dispatch becomes the binding constraint on every sweep.
  Turning it on means two writers on the store, whose rep-collision guard currently
  only warns. Belongs with the owner of the model-facing contract, P0.
- **Hardware as a variable.** A replayable re-bootstrap and envelope
  re-characterisation, plus a statement of what in the design set depends on
  host-specific numbers. Owner: the bootstrapper design, at the latest M16.
- **Editor-agent frontend choice.** Owner: the bootstrapper design.
- **Experiments E0–E7.** One sheet each in
  [`03-research-and-evaluation/`](03-research-and-evaluation/); that folder's README
  holds the current structure. **E0 is answered (2026-09-17) and its result is not
  yet carried:** the suite is *not* unidimensional — parallel analysis retains two
  factors — and folding the structural dimensions into the gate **changes arm
  ordering**. E4's interpretation has to account for that and does not.
- **An operator population, and with it the system+user ceiling
  (2026-09-22).** `70-THINKING/02` names four ceilings and the fourth — the
  grain an operator-plus-system pair reaches together — has never been
  measured. It is step 6 of the evaluation arc and the terminal quantity the
  other three layers are proxies for. Measuring it means varying the operator,
  which needs a population, and `70-THINKING/01-use-cases.md` §2 is empty. The
  sheet that would have done it, `E5-population-spread`, was dissolved on
  2026-09-22 into a blindness requirement on every layer — correct for what it
  fixed, and it left step 6 without a sheet. **No owner. The largest unowned
  gap in the evaluation programme.**
- **A compiled-language fixture family (2026-09-23).** `E3` direction 3's
  worked example is a buffer overflow that does not appear under ICC and
  segfaults under GCC at the next `free`, with a sanitiser build as the
  held-out check. Every M6 fixture is Python, where undefined behaviour, heap
  metadata and toolchain-dependent manifestation do not exist. This is new
  ground with a build step inside the check, not an extension of the existing
  suite. No owner.
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
