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
- [ ] **3. Inventory of changes owed to `10-technical/`.**
- [ ] **4. Upgrade `10-technical/` toward a concrete implementation axis.**
- [ ] **5. M7 — close it, or advance it.**

### Progress notes

_Appended as work lands. Difficulties and deliberate omissions collected here for
the operator's review._

**2 — editorial pass. Done, with two judgement calls worth reviewing.**

- `03`'s append-don't-rewrite rule applies to *promoted claims other documents relied
  on*. The audit trail for every correction lives in `90-notes/02` (F1–F46) and in
  git, so removing archaeology from the design documents loses nothing. Line taken:
  **keep the argument, drop the chronology.** "X rather than Y, because Y describes
  form while what matters is relation" stays; "an earlier draft said Y, withdrawn on
  this date" goes.
- The pass surfaced one real contradiction rather than only prose: `25` said in one
  paragraph that deriving a scope is ordinary cognition rather than part of the check,
  and in the next that deriving from intent belongs to the layer. Left over from the
  scope reassignment. Resolved to the current position — ceiling here, narrowing not.
  Flagging it because it is a design fix inside a pass that was meant to be editorial.
- **Not done:** "expand paragraphs that are too abstruse" was applied only where the
  archaeology removal already touched the text. A deliberate readability pass over the
  documents this session never rewrote — `22-arch-cognition/08`, most of `27` — has
  not been run.

## Where we are

**MVP slice M0–M6 complete.** Findings entries 1–9.

**Current milestone: M7 — Static supervised workflow.** Both deliverables owed: the
spec (`10-technical/11-static-workflow.md`) and the execution record
(`50-PROGRESS/M7-static-workflow.md`).

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
