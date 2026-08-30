# PROGRESS

## What this folder is

The living record of milestone decomposition and execution state. It answers "how far are we, and what happens next" at task granularity.

It is deliberately separate from the roadmap:

| Document | Question it answers | Stability |
|---|---|---|
| `40-roadmap/01-milestones.md` | what each milestone is and why | stable |
| `00-project/04-execution-cadence.md` | how spec, dev, and milestones interrelate | stable |
| `40-roadmap/05-findings-log.md` | what a milestone taught us, on completion | append-only |
| **this folder** | what tasks a milestone breaks into, and their state | changes constantly |

## Structure

- `STATUS.md` — the entry point. Current milestone, blockers, immediate next actions.
- `M<n>-<name>.md` — one document per milestone, holding its task breakdown and state.

A milestone document is written when the milestone becomes *current* or *current + 1*, matching the just-in-time rule in the execution cadence. Milestones further out are not decomposed in advance.

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
