# Roadmap

## TL;DR

What the project intends to do, in what order, and what it owes. Three kinds of
document: milestones (what each piece of work *is*), the backlog (what order, and
what is outstanding), and the registers that keep the open questions honest.

> **Motto:** Identity is stable; order is a claim; debt is written down.

## What is in this space

| | Holds | Stability |
|---|---|---|
| [`00-backlog.md`](00-backlog.md) | every outstanding item, in four priority bands | revised freely |
| [`01-MILESTONES/`](01-MILESTONES/README.md) | one file per milestone: what it is, its evidence question | stable |
| [`02-open-questions-register.md`](02-open-questions-register.md) | questions the design set has not answered | grows |
| [`03-research-and-evaluation-agenda.md`](03-research-and-evaluation-agenda.md) | the hypotheses and how each would be falsified | revised on findings |
| [`04-long-term-perspectives.md`](04-long-term-perspectives.md) | directions beyond the current sequence | loose |
| [`06-sequence-rework-01.md`](06-sequence-rework-01.md), [`07-sequence-rework-02.md`](07-sequence-rework-02.md) | dated records of past resequencing decisions | never rewritten |
| [`08-next-experiments.md`](08-next-experiments.md) | experiments ranked by information per unit of cost | revised freely |

Neighbouring spaces: [`../50-findings/`](../50-findings/README.md) records what a
milestone taught us and is append-only;
[`../../50-PROGRESS/`](../../50-PROGRESS/README.md) records task-level execution
state and changes daily. Neither is roadmap — the roadmap states intent, findings
state what happened, progress states where the work is right now.

## Milestones: identity and position are separate

A milestone's number is a **stable identifier**, allocated on creation and never
reused, reordered, or renumbered. Its **position** — when it gets worked — lives
in the backlog and nowhere else.

The full rule, and the mapping needed to read documents written before the numbers
were frozen, is in [`01-MILESTONES/README.md`](01-MILESTONES/README.md).

A milestone file must not state what comes before or after it. It may state a
**dependency** — M11 must precede M12, because a loop cannot commission its own
watcher — because a dependency is a fact about the work rather than a decision
about sequence.

## How the backlog works

### Four bands

| | Holds |
|---|---|
| **P0** | Ongoing specification and architectural rework. Contracts owed, and design positions not yet carried into the documents that depend on them. |
| **P1** | Work in progress. Normally the current milestone, decomposed far enough to act on. |
| **P2** | Short-term work to address next. |
| **P3** | Unscheduled, externally blocked, and notes. |

**P0 is a gate, not a queue.** Every row in it blocks P1, and it is checked before
moving rather than worked through in order. That is the whole reason the band sits
above work in progress.

**A gap that blocks nothing does not go in P0.** It is written into the document it
concerns as an **open contract**
([`../../10-technical/00-specification-conventions.md`](../../10-technical/00-specification-conventions.md)),
where whoever next opens that document will read it, and where the open-contract
lifecycle already governs how it closes. Parked in the backlog it would be read by
nobody who needed it, and a P0 band holding a dozen non-blocking rows stops being
read as a statement of what is blocked — which is the only thing it is for.

Three kinds of gap are *not* open contracts and belong in P3 instead:

- a **defect against a contract already written** — a decision was made and the
  code does not honour it;
- **mechanical rollout** of a convention;
- **anything owed against a design document.** Open contracts are a specification
  convention; design documents have no such section. Non-blocking design debt has
  no home but P3.

The third is a known asymmetry, not a considered position. Whether the design set
should gain an equivalent mechanism is open.

Within a band, order carries no claim. Between bands it does.

### What an item carries

**Planning and dependencies. Nothing else.** What the work is, which document or
milestone owns it, what it blocks, and what blocks it.

Not rationale, not evidence, not results, and in particular **not an inventory of
what has been done**. Completed work is recorded in
[`../50-findings/`](../50-findings/README.md) and in the milestone files; a backlog
that also summarises it becomes a second, diverging record of the project's
history, and the version in the backlog is always the stale one.

An item that seems to need a paragraph of justification is usually an item whose
reasoning belongs in the document that owns it — cite that document instead. If it
also blocks nothing, that is the second signal it should be an open contract there
rather than a row here.

### When an item enters

When it is understood well enough to state, whether or not it is scheduled — and
in particular when a change is made upstream that has not been carried downstream.

### When an item leaves

When it is done. **Not when it is decided that it does not matter much** — that
decision is itself a change, and it gets recorded as one.

### The banding is a claim, not a schedule

The standing rule from [`08-next-experiments.md`](08-next-experiments.md) applies
here too: working only from the top band confirms the ordering without ever risking
it, and the ordering then becomes an unexamined premise.

## Change may happen at any time; the debt gets recorded

Design positions and milestones may be added, reframed, resequenced, or dropped at
any time. Waiting for a scheduled rework to write down a change that is already
understood loses the reasoning that produced it, which is the more expensive loss.
What batching still governs is *reordering under findings pressure* — see
[`../00-project/04-execution-cadence.md`](../00-project/04-execution-cadence.md).

**The obligation attached to every change: a change is finished when every
document that depended on the old version has been updated, or when the remaining
gap is an item in the backlog.** There is no third option, and "it is obvious to
whoever made the change" is not one — it is obvious for about a week.

This exists because it has failed twice. Rework 2's renumbering was applied in one
file and declared everywhere else, and the same number came to mean two different
milestones depending on which document it appeared in. The 2026-09-05 design pass
promoted positions out of the thinking set into foundations, cognitive
architecture, and the research agenda, and never reached the specification set —
which then spent weeks describing an older version of the design with nothing
recording that it did.

Neither failure was a broken link. Both were documents that looked correct.

## What does not belong in the backlog

- **Rules.** They belong here, or in the execution cadence. A list that
  accumulates its own instructions stops being read as a list.
- **Anything the milestone files or the findings already hold.** The backlog
  points; it does not restate.
- **Speculative improvements.** Every item is something outstanding — work owed,
  or a known inconsistency. A list that also holds ideas cannot be read as a
  statement of debt.
