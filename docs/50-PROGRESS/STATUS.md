# Status

_Updated: 2026-09-05_

> **This file is Claude's working memory across sessions**, maintained by Claude
> and restructured freely as the work moves. It is written for a cold start —
> dense, pointer-heavy, and not an introduction to the project.
>
> **It is not a document of record.** What was learned lives in
> `00-design/50-findings/`; what the project holds lives in the design set; what it
> intends lives in `40-roadmap/01-MILESTONES/`; what order, and what is owed, lives
> in `40-roadmap/00-backlog.md`. Where this file disagrees with any of them, they
> are right and this one is stale.
>
> Nothing should exist only here. A note that is load-bearing has been filed in the
> wrong place.

## Where we are

**MVP slice (M0–M5) complete.** Plus M6. Findings entries 1–9.

**Current milestone: M7 — Static supervised workflow**, in execution, kept open on
strategy. Neither of its deliverables exists yet: the spec
(`10-technical/11-static-workflow.md`) and the execution record
(`50-PROGRESS/M7-static-workflow.md`) are both owed.

**M3 is open**, not done. It was crossed in a reduced form for the MVP and stays
open until the M11 items land.

For milestone state, read `40-roadmap/01-MILESTONES/README.md` — it carries both
tables and is the source. For what to do next, read `40-roadmap/00-backlog.md`.

**One dependency worth knowing before starting M7:** the suite run (backlog P1
step 4) needs **E0, suite construct validation** (P2) for the comparison to be
interpretable. M7's evidence question is stated against a ruler nobody has
validated. E0 may be answerable from runs already recorded.

## What the completed milestones established

One line each; the detail is in `00-design/50-findings/` and in each milestone's
file under `40-roadmap/01-MILESTONES/completed/`.

- **M0** — 7B Q4/Q5 ≤16k at ~40 tok/s; VRAM fit is a hard binary with a ~10–20×
  offload cliff; per-role model switching not viable.
- **M1** — baseline scripted and green in place; clean-machine replay never run.
- **M2** — 40 real runs reconstructable for unplanned questions, **but only where
  the effect envelope carries structured outcome rather than prose**.
- **M4** — a non-looping role chain did not beat a monolith (5/8 vs 6/8) at ~3×
  cost; review with no revision edge was inert.
- **M5** — LLM orchestration 7/8 vs 6/8 vs 5/8, the +1 entirely adaptive retry, at
  ~5× cost. Understandable for acting, weak for stopping.
- **M5 follow-up** — a 7B does the doing, not the judging. No reviewer framing
  beats an approval bias; a deterministic gate scores 9/10 alone and **6/10 with a
  7B panel added**.
- **M6** — dloop 24/30 with 0 regressions; monolith 18/30 with 7 regressions;
  staged 19/30, worse than the plain spine because premise-audit-as-gate
  false-declines ~20%.

## Changes to how the project is run — 2026-09-05

A large session of process work. Four changes, each with its reasoning in the
document that owns it.

**Milestones split, numbers frozen.** `40-roadmap/01-milestones.md` became
`40-roadmap/01-MILESTONES/`, one file per milestone, completed under `completed/`.
A milestone's number is now a **stable identifier** — allocated on creation, never
reordered. Rework 2's renumbering had been applied in one file and declared
everywhere else, so "Milestone 9" meant two different milestones depending on the
document; every live reference was corrected. `50-findings/` and
`50-PROGRESS/archives/` keep their original numbers by rule — read them through the
mapping table in the milestones README.

**Backlog created.** `40-roadmap/00-backlog.md`, four bands: **P0** ongoing
spec/architectural rework (every row blocks P1), **P1** work in progress, **P2**
short term, **P3** unscheduled and externally blocked. It carries planning and
dependencies only — no rationale, and **no inventory of completed work**. Rules in
`40-roadmap/README.md`. Sequencing content moved out of `00-project` entirely.

**Specification now runs ahead; execution does not.** The just-in-time rule is
gone. A contract may be written for any milestone; what waits is *building*, behind
two gates — the spec is in shape, and findings that invalidate a contract have been
cascaded. Gate 2 is the point: an unwritten contract cannot be contradicted, so a
finding that undermines it collides with nothing. Every document is authoritative,
there are no maturity tiers, and revision grounds in findings only
(`10-technical/00-specification-conventions.md` → authority and revision).

**Prose discipline** added to `00-project/02-documentation-philosophy.md`. Authority
in this set is grounded in auditable argumentation, so extended phrasing is a defect
rather than a taste question. The `Motto` line is the sanctioned exception.

Five non-blocking gaps were moved out of the backlog and written as **open
contracts** on specs 02, 07 and 10, per the rule that a gap blocking nothing belongs
in the document it concerns.

**"The project mantra"** was referenced in three places and defined nowhere. The
references were removed. `70-THINKING/04-praxis.md` was opened as a new thread and
is **not** a replacement for it.

## Blockers

None on execution. The M2 recorder, M3 floor, M4 runtime, and M5 orchestrator are
built and exercised on real runs; Ollama and llama.cpp are in place
(`experiments/M0-inference-envelope/setup/README.md`).

The standing external dependency is a **second judgment source** — a stronger or
independent reviewer model, needing the planned second GPU. It gates M12 onward.

## Open decisions waiting on the operator

- **M7 scope** — back half only, or back half plus front half. The front half pulls
  M9 in front of it. Proposed: back half now, front half as an open contract.
- **Naming theme** — `00-design/90-notes/04-naming-theme` is marked *Decided* and
  has never been applied anywhere. Apply or downgrade.
- **Praxis before or after M7** — two execution gates rest on positions that thread
  has not taken.

## Repository

**Not under version control as of this writing.** No `.git`, no backup.
`.gitignore` and `.gitattributes` are in place and correct. Six milestones of
experimental record — 62 drift runs, 39×3 census probes, 4 arms × 30 suite tasks —
exist in one copy.

The first commit will contain the 2026-09-05 process work already merged into the
baseline; the pre-change state is not recoverable, which is why the section above
records what changed rather than leaving it to a diff.
