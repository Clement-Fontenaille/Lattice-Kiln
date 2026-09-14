# Status

_Updated: 2026-09-13_

> **Claude's working memory across sessions**, maintained by Claude and restructured
> freely. Written for a cold start: dense, pointer-heavy, not an introduction.
>
> **Not a document of record.** Findings live in `00-design/50-findings/`; what the
> project holds lives in the design set; intent lives in
> `40-roadmap/01-MILESTONES/`; order and debt live in `40-roadmap/00-backlog.md`.
> Where this file disagrees with any of them, they are right and this is stale.
>
> Nothing should exist only here.

## Current batch — instructions of 2026-09-14

Consolidation pass after the type-4/type-5 immutability rulings, then M7 wrap-up,
then M8/M9/M11 for a testable codebase.

- [x] **1. Backlog sweep.** P1/P2/P3 — remove entries the rework made meaningless.
      P0 is already empty.
- [x] **2. Consolidation pass over the new technical specs.** `12`, `13`, `14`,
      `15`, and the heavily-reworked `03`, `07`. Find inconsistencies, answer the
      easy questions, tighten. Cascaded into `01` and `02`, and one fix into
      `00-design/22-arch-cognition/05-curation.md`.
- [ ] **3. Milestone consolidation.** Name the work packages each existing
      milestone needs, check the order still holds, subdivide where it smooths
      execution.
- [x] **4. Research and evaluation becomes a folder.** `03-research-and-evaluation/`
      with `00-questions.md` cataloguing open questions that can become experiments,
      absorbing `08-next-experiments.md`. One sheet per well-circumscribed
      experiment.
- [ ] **5. Wrap up M7.** Follow-up experiments from tests already run stay
      available as experimental work.
- [ ] **6. M8, M9, M11** — a stable codebase to test against.

### Progress notes

_Appended as work lands. Difficulties and deliberate omissions collected here for
the operator's review._

**2 (this batch) — spec consolidation. Done. Six findings, and one of them is the
kind that should have been caught earlier.**

- **The parent-relative containment rule survived in five places** after the ceiling
  ruling replaced it — four in `03` (the delegation bound, the *scope-forbidden*
  paragraph, the "inside its parent's" judgment line, and by implication the
  spawned-set argument), one in `02`, and one in `14` where it was the stated premise
  of an argument the operator had already corrected twice. The replacement text was
  written into `03`'s Containment section and the cascade was never walked out of it.
  **This is the same failure `90-notes/02` F47 records**, one more time: a ruling
  applied where it was discussed and not where it was cited.
- **The work item had no state meaning *live*.** `13` named four transitions —
  challenged, deferred, abandoned, executed — and no initial value, following
  `22-arch-cognition/01`, which does not name one either. But `12` deletes an artifact
  when its task stops being live and `14` ends a live set when its task ends, so both
  were reading a predicate nothing supplied. Fixed by adding `open` and marking
  `abandoned`/`executed` terminal. **Neither document could have found this alone**,
  which is the argument for `15` existing.
- **Trajectory B never promoted anything.** `15`'s promotion path had a step refusing
  deletion "because the claim is promoted" and no step that promoted it — attaching
  (4c) looks sufficient and is not. Inserted as step 11. Found by re-walking, which is
  gap 7 in that document and the first one the re-walk produced.
- **`03`'s type-4 sub-type numbering was off by one** against `01`: grants written as
  `4d (attach)` / `4e (conclude)` where the vocabulary has 4c Attach and 4d Conclude,
  and a `4a..4e` range where only `4a..4d` exist. A capability example that does not
  match the vocabulary it keys to is the kind of error an implementer inherits
  silently.
- **`14`'s live-set entry never absorbed the edge labels.** `70-THINKING/18` settled
  them — `objective`, `derived_scope`, everything else unlabelled — and the normative
  document had no `label` field, so the policy it calls mechanical could not branch on
  the one thing structurally fixed about a task. Added, with the criterion.
- **"There is no sweep" was overstated** and I wrote it. The design set already called
  removal "the sweep" and already called it incremental
  (`22-arch-cognition/05-curation.md`); what the ruling removed was the *schedule*.
  `12` now says so, and the spec set stops using a word that reads as a whole-graph
  pass. While reconciling, `05-curation.md` was found naming an *archived* live-set
  state that `23-arch-context-management/01` and `14` both forbid — fixed there.

**Easy questions answered rather than filed:** which transitions are terminal and
therefore run the aggregate check; how `pending` resolves without a scope ever being
edited (by succession — it never resolves in place); that Elide is runtime bookkeeping
and not a proposed effect; that promotion is effect 5b; that attachment at task
creation is an ungated runtime call while mid-work attachment is 4c. Three of those
came with a new open contract naming what is left.

**Worth the operator's eye:** `13` now names a work-item state (`open`) that
`22-arch-cognition/01` does not. The spec is ahead of the design set on one word, and
the design set is where that vocabulary belongs.

**A verification gap worth knowing about.** The link checker used throughout this
session only validates markdown links — bracket-text followed by a parenthesised path. It does not see **prose references to section
names** — "`10-technical/01`, What is not an effect" — and renaming a heading breaks
those silently. Renaming `What is not an effect` tonight broke one such reference, found
only by writing a second checker after the fact. Bolded lead-ins are also used as
reference targets in several places, which no heading-based check will ever catch.

**2 — editorial pass. Done, with two judgement calls worth reviewing.**

- I invoked `03`'s append-don't-rewrite rule to justify this and should not have.
  **That rule governs artifacts** — entries in the claim graph the system holds — **not
  design documents**, which are human-authored specification. Operator ruling,
  2026-09-13. The instruction to strip the archaeology was authority enough on its own;
  citing `03` dressed a straightforward editorial decision as a derived one, and I also
  had the rule's scope condition backwards while doing it.
- The line actually taken, which stands: **keep the argument, drop the chronology.**
  "X rather than Y, because Y describes form while what matters is relation" stays;
  "an earlier draft said Y, withdrawn on this date" goes.
- The pass surfaced one real contradiction rather than only prose: `25` said in one
  paragraph that deriving a scope is ordinary cognition rather than part of the check,
  and in the next that deriving from intent belongs to the layer. Left over from the
  scope reassignment. Resolved to the current position — ceiling here, narrowing not.
  Flagging it because it is a design fix inside a pass that was meant to be editorial.
- **Not done:** "expand paragraphs that are too abstruse" was applied only where the
  archaeology removal already touched the text. A deliberate readability pass over the
  documents this session never rewrote — `22-arch-cognition/08`, most of `27` — has
  not been run.
- **Third sweep, closing the pass.** Grep across `00-project/`, `10-foundations/` and
  the `20`–`28` band for self-historical framing. Three fixes: `04-execution-cadence.md`
  explained milestone numbering by confessing a past mistake, now stated as the failure
  mode it guards against; `22-arch-cognition/02`'s open question said "two of those have
  moved since this was written", now three bolded current positions; and the same file's
  *What survives a processor* opened on what the documents above "never said".
  Verification after: 0 broken links, no duplicate headings, and the only remaining grep
  hit is the rule text itself quoting the phrasings it forbids.
- **The fourth fix was mine, and it is the rule's own failure mode.**
  `02-documentation-philosophy.md`'s **Revision policy** still said changes "should
  preserve historical rationale where useful" — written before, left standing while I
  added the no-history rule two sections above it, in the same file, in the same
  session. A document contradicting itself between line 31 and line 91 is exactly what
  "a promoted claim triggers a cascading revision" exists to prevent, and the cascade
  was not walked even one file deep. Recorded as the fifth case in `90-notes/02` F47,
  which now reads four misses out of five rather than three out of four — and this is
  the worst of them, since the dependent was not in another document but on the screen.

**3 — inventory. Done.** Twelve rows: nine existing specs, three documents that did
not exist (`12-knowledge-model`, `13-work-record`, `14-context-manager`).

**4 — technical upgrade. Done, all twelve.** Worth reviewing rather than trusting: this
is a large amount of normative text written in one unsupervised run, which is exactly
the failure mode the inventory existed to make visible. What follows is what to look at
first.

- **`03-capability-authority-model.md` is the largest change**, and the one most worth
  a read. It had zero mentions of scope; it now carries mandate conformance whole —
  the three scope fields, derive-record-contest, don't-derive-under-ambiguity,
  containment across splits *and refinements and nested invocations*, the who-may-write
  table, static instance scope, and the two halves of the check at opposite ends of a
  task. The permissive read default landed here too, because `01` and `04` both name
  this document as where a read policy is expressed and it was not there.
- **`05` gained G4, which the MVP does not satisfy.** Work executes under a declared
  scope and a functioning scope check exists. Nothing today derives, records or checks
  one. I stated it as a goal rather than a hard constraint because its subject is a
  *presence* and there is no proposed effect whose refusal establishes that a check is
  running — and recorded plainly that a system without it is invalid rather than
  degraded. **This is a judgement call an operator may want to overturn**: it puts a
  clause in the enforced floor that the running system fails.
- **`05` also gained R4**, the context ceiling, physical rather than cognitive. It is
  the concrete reason reads must be in the gate's input domain, since what crosses that
  ceiling is an accumulation of reads and never a typed effect.
- **`12`, `13`, `14` written from nothing.** The three load-bearing narrowings, each of
  which could have gone the other way: mode of acquisition on the provenance *edge*
  rather than on the claim (F6 says a multi-parent claim is the case that occurs);
  current work state and transition log both held and neither derived from the other
  (the orchestrator's per-loop-step read must not replay anything); the live set holding
  references and no content, with a retrieval registering an event and no content at
  all.
- **`07` stopped producing a bundle** and is now a seeding heuristic plus the degenerate
  recall policy. The seeding half is the caller's, not the context manager's — the
  context manager never initiates a crossing — which is a re-founding rather than an
  edit, and it makes live-set seeding a visible open contract instead of a question a
  bundle made look answered.
- **`09`'s "exactly two things cross" was wrong in both directions.** Going out,
  processor invocation is effect type 6 and was double-counted, while the read was
  missing entirely. Coming back, the assembled context was a request/response object
  that no longer exists.
- **`02` went from four record kinds to eight**, adding the turn input, knowledge-state
  transitions, work transitions, and the conditions in force. One narrowing worth
  flagging: reads and typed effects share **one** record kind rather than getting one
  each, so the gate reads a single ordered history. Two kinds would invite an
  implementation to build the query over effects alone, which is the blindness the
  requirement exists to remove.
- **`10` gained the reading rules**: paired over aggregate, resolution before precision,
  what repetition is actually for, the within-arm versus between-arm regime diagnostic,
  and expected effect size declared before the run.

**Not done inside task 4:** nothing was written for **decomposition**, which has no
specification counterpart and was not in my own inventory — `11-static-workflow.md`
specifies concern-split as one conditional stage of one workflow, which is not the same
thing. It is now a P0 row.

**5 — M7. Step 1 of 4 done, and the other three are not mine to do alone.**

- **Done:** `10-technical/11-static-workflow.md` v0. Back half only, per the recorded
  proposal in Open decisions below — the loop, its gates, the incumbent-protected
  keeper, escalate-on-stall, premise audit as advisory, concern split as conditional.
  Everything in it comes from M6 evidence rather than from argument.
- **The front half is an open contract in that document**, not a gap. It rests on six
  tasks at low N and its third prerequisite is `10-foundations/04`'s context-quality
  question, which makes **M9 a prerequisite for evaluating it**. Specifying it now
  would be specifying against a ruler nobody has.
- **Steps 2–4 are build-and-run**, not writing: build from the `loop_lab` / `m6_arms`
  parts, run against the suite, write the findings entry. Step 3 still needs **E0**
  (suite construct validation) for the comparison to be interpretable — the dependency
  named under Where we are.
- One thing I flagged in the spec rather than fixing: **the workflow runs unscoped.**
  `06` binds a `scope` and `24-arch-permission-layer` requires one, but nothing
  derives, checks or enforces it. That is honest rather than accidental, recorded as
  an open contract in `11`, and it is now also `05`'s G4 and a P0 row — the
  specification side is complete and the build side has no owner.

## Where we are

**MVP slice M0–M6 complete.** Findings entries 1–9.

**Current milestone: M7 — Static supervised workflow.** The spec
(`10-technical/11-static-workflow.md`) is written, back half only. The execution record
(`50-PROGRESS/M7-static-workflow.md`) is still owed, and steps 2–4 are build-and-run.

**M3 open**, crossed in reduced form for the MVP, stays open until the M11 items land.

Milestone state: `40-roadmap/01-MILESTONES/README.md`. What to do next:
`40-roadmap/00-backlog.md`.

**Dependency before M7's suite run:** backlog P1 step 4 needs **E0, suite construct
validation** (P2) for the comparison to be interpretable. E0 may be answerable from
runs already recorded.

## What the completed milestones established

One line each; detail in `00-design/50-findings/` and in
`40-roadmap/01-MILESTONES/completed/`.

- **M0** — 7B Q4/Q5 ≤16k at ~40 tok/s; VRAM fit is a hard binary with a ~10–20×
  offload cliff; per-role model switching not viable.
- **M1** — baseline scripted and green; clean-machine replay never run.
- **M2** — 40 real runs reconstructable for unplanned questions, **but only where the
  effect envelope carries structured outcome rather than prose**.
- **M4** — a non-looping role chain did not beat a monolith (5/8 vs 6/8) at ~3× cost;
  review with no revision edge was inert. Both arms reliably **declined** a
  false-premise task.
- **M5** — LLM orchestration 7/8 vs 6/8 vs 5/8, the +1 entirely adaptive retry, at ~5×
  cost. Understandable for acting, weak for stopping; **declined** and **blocked**
  collapsed into one outcome.
- **M5 follow-up** — a 7B does the doing, not the judging. No reviewer framing beats an
  approval bias; a deterministic gate scores 9/10 alone and **6/10 with a 7B panel
  added**.
- **M6** — dloop 24/30 with 0 regressions; monolith 18/30 with 7 regressions; staged
  19/30, worse than the plain spine because premise-audit-as-gate false-declines ~20%.

## Design-set state after the 2026-09-11/13 architecture pass

The architecture band is consolidated and the three foundations reworks (`02`, `03`,
`05`) are carried. Justification record: `90-notes/02` F1–F46, `90-notes/03` for the
context-management refoundation.

**Deliberately open**, not gaps: the recall policy's content; the criterion for
deliberate remembrance; live-set seeding; who assigns `03`'s labels and by what
method; how scope is concretely inscribed; fork/join versus continuation; whether the
thinking family is one role or several; whether scope derivation and scope checking
are one role or two.

**The specification layer is carried.** All twelve documents the pass owed
`10-technical/` are written, so every actor in the architecture band has a
specification counterpart. `00-backlog.md` P0 now holds only what the pass did not
cover: decomposition, the handoff structure, the reversibility-class carrier, M9's
stale self-citation, and G4's missing owner.

**A specification's open contract is not a design-set gap.** The list above is what the
design set deliberately holds open; the specs carry their own open contracts against
it, and the two are not the same list. The one that is both, and the most consequential
of the new ones: **what the scope comparison actually consumes** — a raw change set, a
summary, a diff — which is the largest unknown in the mandate half and has no answer on
either side.

## Where the spec set still needs answers

**P0 is empty as of 2026-09-14.** Every row closed, and most of them closed by asking
whether they were design or implementation rather than by new design. The scope check
and the scope writer are M11 deliverables alongside triage, all three being invariant
processors, so the category is instantiated once.


The holes have a fixed location by convention: **every specification document ends
with `## Open contracts`**, and that is where a hole is written down rather than
guessed. There are **123 entries across the fifteen documents**.

Most are waiting on something that has not happened yet, which is the correct state
rather than debt. **Two stop something now, and both are measurements rather than
decisions** — which is a different position from the last reading of this table.

| Where | The question | What it stops |
|---|---|---|
| `05` G4 / `14` | How does the resident envelope divide across contexts? | Whether a scope check is providable at all |
| `14-context-manager` | Can a turn input's KV footprint be estimated before composing it? | R4 reports a crash instead of refusing |

**The same instrument answers both.** `05`'s bootstrap occupancy test measures
memory-per-token on first encountering an unknown model identity and derives R4's two
limits and G4's substrate precondition from one run. It is M0-shaped, cheap, and
nothing is scheduled to run it.

**Eight rows left this table since the last reading**, and it is worth recording how,
because only one of them was closed by new design. The root set, the meaning of
*promoted*, and the removal trigger were settled by the operator's rulings on
promotion-as-inscription and incremental removal. The `outside` disposition, what the
comparison reads, what triggers a ceiling derivation, and how a derived scope reaches
the operator were settled by asking whether each was design or implementation — and
`03` now carries an explicit section saying where the specification stops and what a
build owes. Decomposition was closed by finding it needed **no mechanism of its own**:
it is task creation, which already had a contract.

**One item needs neither a run nor a decision.** Re-analysing M4 and M5 as paired
comparisons — now E7 in `40-roadmap/03-research-and-evaluation/`, the only sheet
there needing no run, no build and no population.

**Everything else waits on a run, a milestone, or the second GPU.** Storage shapes
and schemas in `02` wait on real volume; gate-alter, accumulation-stop and
interruptibility wait on M11; competing orchestrators and model diversity wait on
hardware.

## Blockers

None on execution. M2 recorder, M3 floor, M4 runtime, M5 orchestrator are built and
exercised on real runs; Ollama and llama.cpp in place.

Standing external dependency: a **second judgment source** — a stronger or independent
reviewer model, needing the planned second GPU. Gates M12 onward.

## Open decisions waiting on the operator

- **M7 scope** — back half only, or back half plus front half. The front half pulls M9
  in front of it. Proposed: back half now, front half as an open contract.
- **Naming theme** — `00-design/90-notes/04-naming-theme` is marked *Decided* and has
  never been applied. Apply or downgrade.
- **Praxis before or after M7** — two execution gates rest on positions
  `70-THINKING/04-praxis.md` has not taken.
- **The isolation measurement.** G4's substrate precondition — two independent
  contexts, each large enough to work in — is verifiable at startup and has never
  been measured on the reference host. It is M0-shaped and cheap. Nothing is
  scheduled to run it, and it gates whether a scope check is providable at all.

## Repository

Under version control. `main`, not pushed to `origin` as of this writing.
