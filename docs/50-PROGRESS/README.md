# PROGRESS

## What this folder is

The living record of milestone decomposition and execution state. It answers "how far are we, and what happens next" at task granularity.

It is deliberately separate from the roadmap:

| Document | Question it answers | Stability |
|---|---|---|
| `40-roadmap/01-MILESTONES/` | what each milestone is and why | stable |
| `40-roadmap/00-backlog.md` | every outstanding item, in four priority bands | revised freely |
| `00-project/04-execution-cadence.md` | how spec, dev, milestones, and the backlog are managed | stable |
| `00-design/50-findings/` | what a milestone taught us, on completion | append-only |
| **this folder** | what tasks a milestone breaks into, and their state | changes constantly |

## Structure

- `STATUS.md` — the entry point. Current milestone, blockers, and pointers.
- `M<n>-<name>.md` — one document per milestone, holding its task breakdown and state. The document for the current milestone sits here; on completion it moves to `archives/`.
- `archives/` — the execution records of completed milestones, retained as written.

A milestone document is written when the milestone becomes *current* or *current + 1*. Milestones further out are not decomposed in advance.

This is deliberately stricter than the rule for specifications, which may be written arbitrarily far ahead as placeholders (`00-design/00-project/04-execution-cadence.md`). A contract written early states what the seams are and parks the rest as open contracts, so being early costs nothing. A task breakdown written early states *how the work will be done*, which depends on decisions the milestone before it has not made yet — so being early makes it wrong rather than incomplete.

**Numbering.** The `M<n>` in a filename is the milestone's stable identifier (`00-design/40-roadmap/01-MILESTONES/README.md`). Documents already in `archives/` were written before those numbers were frozen and still carry pre-rework-2 numbering in their bodies — they are historical records and are not rewritten. Read them through the mapping table in the milestones index.

## Task states

- **TODO** — not started.
- **WIP** — in progress.
- **DONE** — complete and verified.
- **BLOCKED** — cannot proceed; the blocker is named.
- **DROPPED** — abandoned; the reason is named.

## Completion

A milestone is complete when its evidence question is answered from a reconstructable run, or when the attempt establishes the question cannot yet be answered and why.

On completion: a findings-log entry is written first, then the milestone document is marked complete and retained for history.

## Not a design surface

Decisions live in the design and specification sets. This folder points at them; it does not hold them. If a task surfaces a real design choice, that choice is recorded where it belongs and referenced here.
