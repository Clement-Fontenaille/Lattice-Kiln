# Milestones

## TL;DR

One file per milestone. The number in a filename is a **stable identifier**, not a
position in a queue: it is allocated when the milestone is created, and it never
changes again. What order the milestones are worked in lives in
[`../00-backlog.md`](../00-backlog.md).

> **Motto:** The number says which milestone; the backlog says when.

## Why this folder replaced a single document

The sequence used to live in one file, `01-milestones.md`, where a milestone's
number was its position. Rework 2 inserted two milestones after M5 and shifted the
old M6–M14 down to M8–M16. The renumbering was applied inside that one file and
declared everywhere else — earlier documents were left alone under a rule that
their numbers "mean the pre-rework-2 number unless dated after 2026-09-02."

That rule failed in the way such rules do. **"Milestone 9" came to mean two
different milestones depending on which file it appeared in** — safety response in
the older documents, context governance measurement in the newer ones — and
`10-technical/05-provisional-invariant-list.md` contained both conventions at
once. One reference read as a perfectly valid new number while pointing at the
wrong milestone, which is worse than a broken link: nothing about it looks wrong.

Splitting the file is the smaller half of the fix. The larger half is severing the
number from the position.

## The identifier rule

**A milestone's number is allocated on creation and never reused, never
reordered, never renumbered.** Rework 2's shift was the last one.

Three consequences worth stating:

- **A new milestone takes the next free number**, whatever position it occupies in
  the plan. If a milestone is inserted before the static supervised workflow
  tomorrow, it is M17 and it runs early. The number is an identity, not a rank.
- **The folder does not sort into execution order.** It sorts by identifier, which
  approximates the order in which milestones were *conceived*. That is the useful
  reading: a low number is old thinking, a high number is recent thinking.
- **Reordering is now a one-file edit.** A rework changes
  [`../00-backlog.md`](../00-backlog.md) and touches no milestone file, no
  specification, and no foundation.

The numbers themselves are the ones rework 2 left behind, frozen as they stand.
They are not a perfect record of creation order — M6 and M7 were conceived last
but were inserted at 6 and 7 — and they are not being corrected, because the
findings entries and experiment directories that cite them are append-only. The
vintage reading holds from here forward, not retroactively.

## Referring to a milestone

In prose, use the number as shorthand and link the file on first use in a
document: *"the literature-grounding pass (M11,
[`11-safety-response.md`](11-safety-response.md))."* The number is the shorthand
that makes discussion possible; the link is what makes it checkable.

Do not write a bare number for a milestone the reader has to look up, and do not
write "the next milestone" or "a later milestone" where a specific one is meant —
those phrasings survive a reordering by saying nothing.

## Where a milestone's content lives

A milestone file holds **what the milestone is, why it exists, and its evidence
question**. Three things it deliberately does not hold:

| | Lives in | Why not here |
|---|---|---|
| Task breakdown and execution state | [`50-PROGRESS/`](../../../50-PROGRESS/README.md) | Changes daily; this file should not. |
| What the milestone taught us | [`50-findings/`](../../50-findings/README.md) | Append-only record; never rewritten. |
| When it runs, and what blocks it | [`../00-backlog.md`](../00-backlog.md) | Sequencing is revised on its own cadence. |

## Open

Ordered by identifier. For priority see [`../00-backlog.md`](../00-backlog.md).

| ID | Milestone | State |
|---|---|---|
| M3 | [Invariant floor](03-invariant-floor.md) | reduced form crossed; full form open |
| **M7** | [**Static supervised workflow**](07-static-supervised-workflow.md) | **in execution** |
| M8 | [Persistent work and knowledge](08-persistent-work-and-knowledge.md) | open |
| M9 | [Context governance measurement](09-context-governance-measurement.md) | open |
| M10 | [Project-level adaptation](10-project-level-adaptation.md) | open |
| M11 | [Safety response mechanisms](11-safety-response.md) | open |
| M12 | [System-level candidate tuning](12-system-level-candidate-tuning.md) | open |
| M13 | [Reproducible generations and promotion](13-reproducible-generations-and-promotion.md) | open |
| M14 | [Meta-evaluation](14-meta-evaluation.md) | open |
| M15 | [Cross-generation comparison](15-cross-generation-comparison.md) | open |
| M16 | [Bootstrap generation closure](16-bootstrap-generation-closure.md) | open |

## Completed

In [`completed/`](completed/). A milestone moves there when its evidence question
has an answer — including an answer of "not yet answerable, and here is why."

| ID | Milestone | Closed | Verdict |
|---|---|---|---|
| M0 | [Local inference envelope](completed/00-inference-envelope.md) | 2026-08-30 | **confirms** |
| M1 | [Reproducible baseline environment](completed/01-baseline-environment.md) | 2026-08-30 | inconclusive |
| M2 | [Observability foundation](completed/02-observability-foundation.md) | 2026-08-30 | **confirms** |
| M4 | [Ephemeral processor experiments](completed/04-ephemeral-processors.md) | 2026-08-30 | inconclusive, leaning weakens |
| M5 | [Intelligent orchestration experiments](completed/05-intelligent-orchestration.md) | 2026-08-31 | confirms, narrowly |
| M6 | [Evaluation task suite](completed/06-evaluation-task-suite.md) | 2026-09-03 | **confirms** |

M3 is absent from both the completed count and this table's spirit: it was crossed
in a reduced form sufficient for the MVP and is **not complete**. It stays open
until the items in [`03-invariant-floor.md`](03-invariant-floor.md) land.

## Reading older documents

Two sets are **never rewritten** and still carry pre-rework-2 numbers:

- [`50-findings/`](../../50-findings/README.md) — append-only by rule.
- [`50-PROGRESS/archives/`](../../../50-PROGRESS/archives/) — retained as the
  execution record of a milestone as it was worked.

The two sequence-rework documents ([`../06-sequence-rework-01.md`](../06-sequence-rework-01.md),
[`../07-sequence-rework-02.md`](../07-sequence-rework-02.md)) are dated decision
records and keep the numbering in force when they were written. Each carries a
banner saying so.

Everywhere else — the design set, the specification set, `STATUS.md` — numbers are
current and were corrected when this folder was created.

**The mapping, for reading anything in those sets:**

| pre-rework-2 | current | milestone |
|---|---|---|
| M0–M5 | M0–M5 | unchanged |
| — | M6 | Evaluation task suite (inserted) |
| — | M7 | Static supervised workflow (inserted) |
| M6 | M8 | Persistent work and knowledge |
| M7 | M9 | Context governance measurement |
| M8 | M10 | Project-level adaptation |
| M9 | M11 | Safety response mechanisms |
| M10 | M12 | System-level candidate tuning |
| M11 | M13 | Reproducible generations and promotion |
| M12 | M14 | Meta-evaluation |
| M13 | M15 | Cross-generation comparison |
| M14 | M16 | Bootstrap generation closure |

## Adding or changing a milestone

Milestones may be added, split, reframed, or dropped **at any time**, and every
change carries the same obligation: record what has not yet been carried
downstream as an item in [`../00-backlog.md`](../00-backlog.md). The rule and its
reasoning are in [`../README.md`](../README.md).

A new milestone takes the next free identifier. Nothing else renumbers.
