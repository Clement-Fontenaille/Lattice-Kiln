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

## Current batch — instructions of 2026-09-13

Running autonomously. Report to the operator on difficulties and on anything left
untreated.

- [x] **1. Sandbox cleanup.** This file rebuilt as the worklist. `archives/` is one
      file per completed milestone, append-only by rule — nothing to clean.
- [x] **2. Editorial pass, foundations + architecture.** Archaeology stripped,
      redundancy reduced, half-answered questions restated.
- [x] **3. Inventory of changes owed to `10-technical/`.** Written into
      `40-roadmap/00-backlog.md` as **Specification inventory**, one row per document
      plus three that do not exist. Filed there rather than here because the backlog
      owns what is owed; a copy in the sandbox would rot.
- [~] **4. Upgrade `10-technical/` toward a concrete implementation axis.** Partial —
      see below.
- [~] **5. M7.** Step 1 of 4 done.

### Progress notes

_Appended as work lands. Difficulties and deliberate omissions collected here for
the operator's review._

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

**3 — inventory. Done.** Twelve rows: nine existing specs, three documents that do not
exist (`12-knowledge-model`, `13-work-record`, `14-context-manager`). The sharpest
items: `03-capability-authority-model.md` contains **zero** mentions of scope and needs
the whole mandate-conformance dimension; `04-enforcement-gate.md` never mentions reads
at all, so the gate as specified cannot represent one whether or not a rule names it;
`01`'s definition of an effect as "a state-changing operation" no longer discriminates.

**4 — technical upgrade. Partial, and deliberately so.**

- **Done:** `06-processor-contract.md`, because `11-static-workflow.md` would have
  inherited it broken. Six things bind at instantiation rather than five —
  `context_bundle` replaced by a `scope` and a `live_set_id`, with context itself no
  longer bound at all. One open contract closed: context-request servicing is an
  ordinary tool call and no servicing path should be built.
- **Also done:** `01-effect-vocabulary.md` and `04-enforcement-gate.md`, on a narrower
  criterion than "upgrade" — these two carried normative text that the foundations pass
  made **actively false**, and a wrong MUST in a spec propagates into code. `01` now
  defines an effect by footprint rather than by "state-changing operation", and
  separates the three exclusions by *reason* rather than listing them together: only
  cognition and bookkeeping are ungatable, while a read is outside the vocabulary
  because its footprint is untracked. `04` gains an input domain that includes reads,
  the invariant-processor category with its direction condition, and a requirement
  that `check_sequence`'s history carry reads even while the check passes
  unconditionally — because turning it on later against an effects-only history would
  be turning on a check that cannot see the case it exists for.
- **Not done, on purpose:** the remaining six spec documents and the three that do not
  exist. Each is a substantial rewrite, several are ordered behind each other (`01`
  before `04` before `05`; a knowledge-model spec before `07`'s rewrite), and none
  blocks M7. Writing them all in one unsupervised run would produce a great deal of
  normative text nobody had reviewed, which is the failure mode the inventory exists to
  avoid. **This is the main thing left.**

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
  `06` now binds a `scope` and `24-arch-permission-layer` requires one, but nothing
  derives, checks or enforces it. That is honest rather than accidental, and it is
  recorded as an open contract in `11`.

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

**Owed to specification** — six rows in `00-backlog.md` P0, all created by that pass.
These are task 3's inventory input.

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

## Repository

Under version control. `main`, not pushed to `origin` as of this writing.
