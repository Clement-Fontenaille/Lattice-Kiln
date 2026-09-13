# Execution Cadence

## TL;DR

Three activities could each run ahead of the others: writing specification,
writing code, and advancing the milestone sequence. They should not. The milestone
is the unit of progress, and it pulls the other two.

> **Motto:** The milestone pulls the work; spec and dev do not push it.

This document holds the **rules**. The items those rules apply to — what to do
next, in what order, and what is owed — live in
[`../40-roadmap/00-backlog.md`](../40-roadmap/00-backlog.md).

## Three tracks, one pace

**Specification runs ahead; execution does not.** A contract may be written for any
milestone. Where the evidence behind it is thin, the document names the seams and
parks the rest as open contracts.

What must not run ahead is **building**. Two gates:

1. **The spec is in shape.** The responsibility stateable in a sentence, the
   authority bounded, the failure modes visible, every remaining unknown named as
   an open contract.
2. **Findings that invalidate a contract have been cascaded.** Work depending on
   that contract stops until the revision is carried through — design, then
   specification, then any downstream contract that inherited the old shape.

Gate 2 is why contracts are written ahead. An unwritten contract cannot be
contradicted: a finding that undermines it collides with nothing, and work
continues on the invalidated shape.

A contract written ahead is as authoritative as any other
(`10-technical/00-specification-conventions.md` → authority and revision). It has
no findings behind it yet, which makes it cheap to overturn — not optional to
honour.

**Development is thin.** Boring, stable, observable, and scoped to the current
milestone. Do not build for milestones not yet reached. Observability is the one
exception to "only what the current milestone needs": it is a research
requirement, not an operational nicety, and it is deliberately placed early in the
sequence for that reason.

**Milestone progress is the pace-setter.** A milestone is done when its evidence
question is answered — or is shown to be unanswerable with current machinery,
which is itself a finding worth recording. Completed code is not the criterion.

One-line loop: **spec the next milestone, build it thin, answer its evidence
question, record the finding, update design first, repeat.**

## What "done" means for a milestone

Each milestone carries an explicit evidence question. The milestone is complete
when that question has an answer supported by a reconstructable run, or when the
attempt establishes that the question cannot yet be answered and why.

This restates the progress criterion from the project-management principles in
operational terms: a milestone is valuable when it reduces uncertainty, and
"reduces uncertainty" is made concrete by the evidence question.

A milestone crossed in a **reduced form** is not complete. It stays open, with the
deferred items named in its own file, until they land. The invariant floor
([`../40-roadmap/01-MILESTONES/03-invariant-floor.md`](../40-roadmap/01-MILESTONES/03-invariant-floor.md))
is the standing example.

## How milestones are managed

Milestones live one per file in
[`../40-roadmap/01-MILESTONES/`](../40-roadmap/01-MILESTONES/README.md). Three
rules govern them.

**1. A milestone's number is an identifier, not a position.** It is allocated on
creation and never reused, never reordered, never renumbered. A new milestone
takes the next free number whatever position it occupies in the plan.

The failure this guards against is specific. Where a number encodes order, a
resequencing renumbers milestones — and a renumbering applied in one file and
merely *declared* everywhere else leaves the same number meaning two different
milestones depending on which document it appears in, with one reference reading
as a perfectly valid new number while pointing at the wrong milestone. Severing
the number from the position removes the failure mode rather than promising to be
more careful next time.

**2. Order lives in the backlog, nowhere else.** A milestone file must not state
what comes before or after it. It may state a **dependency** — M11 must precede
M12, because a loop cannot commission its own watcher — because a dependency is a
fact about the work rather than a decision about sequence.

**3. A milestone file holds what the milestone is; not its state, and not its
results.** Task breakdown and execution state are in
[`../../50-PROGRESS/`](../../50-PROGRESS/README.md), which changes continuously and
is not part of the design set. What a milestone taught us is in
[`../50-findings/`](../50-findings/README.md), which is append-only.

## Change may happen at any time; the debt must be recorded

**Design positions and milestones may be added, reframed, resequenced, or dropped
at any time.** Waiting for a scheduled rework to write down a change that is
already understood loses the reasoning that produced it, which is the more
expensive loss. What batching still governs is *reordering under findings
pressure* — see below.

**A change is finished when every document that depended on the old version has
been updated, or when the remaining gap is written down.** There is no third
option.

Where it is written down depends on whether it blocks anything. A gap holding up
work in progress is a P0 item in the backlog. A gap that blocks nothing is an
**open contract in the document it concerns** — where the person who needs it is
reading, and where the open-contract lifecycle governs how it closes. A P0 band
holding items that block nothing stops being read as a statement of what is
blocked.

Sequencing and debt do not live in this document, or anywhere else in
`00-project`. A near-term specification list once did; it went stale because the
document around it was not expected to churn. How the backlog is structured is
in
[`../40-roadmap/README.md`](../40-roadmap/README.md); the items are in
[`../40-roadmap/00-backlog.md`](../40-roadmap/00-backlog.md).

## The feedback flow

Findings flow in one direction, in this order:

1. **Design first.** A finding that bears on a concept updates the design
   document, preserving the historical rationale rather than overwriting it, per
   the revision policy.
2. **Then specification.** The corresponding open contracts are revisited. A
   finding may close one, reopen one, or add one.
3. **Then the sequence.** Milestone reordering happens at a rework point — not
   continuously. The exception is a finding that invalidates a foundational
   constraint, which is handled immediately.

Where step 2 or step 3 cannot be done at the time, the gap becomes a P0 item in the
backlog. That is what makes the one-directional flow auditable rather than
aspirational — and it is the cascade gate in operational form: **an open P0 item
against a document the current work depends on means the current work is
blocked.**

Not every finding trips the gate. A finding that adds an open contract, or narrows
one, or bears on a milestone nothing is currently building against, is recorded and
the work continues. The gate is for findings that **invalidate** a contract the
work in progress rests on — where continuing means accumulating output on a shape
already known to be wrong.

The concrete artifact carrying findings is [`../50-findings/`](../50-findings/README.md),
one entry per completed milestone, append-only.

## Scheduled sequence rework

The milestone sequence is reworked in batches, not continuously, so that findings
accumulate into a coherent revision rather than causing drift.

The first rework batch ran after the MVP slice — end of Milestone 5
([`../40-roadmap/06-sequence-rework-01.md`](../40-roadmap/06-sequence-rework-01.md),
outcome: no reordering). The second ran after the M5-follow-up investigation
rather than at any calendar or sequence midpoint
([`../40-roadmap/07-sequence-rework-02.md`](../40-roadmap/07-sequence-rework-02.md),
outcome: two milestones inserted). **A rework is triggered by a body of findings
large enough to revise the sequence coherently, not by a position in the
sequence.**

Between rework points, ad-hoc *reordering* is discouraged; a finding that seems to
demand it is recorded in the backlog and left for the batch unless it touches a
foundational constraint. This is a constraint on reordering only — it is not a
reason to leave any other kind of change unwritten.

## The MVP slice

The minimum viable product was Milestones 0 through 5: a local assistant on
measured hardware, fully observable, sitting on a safety floor, that decomposes
work across ephemeral role-specific processors coordinated by a language-model
orchestrator.

It was chosen to be the smallest slice that is independently useful *and* tests
three core hypotheses at once — that orchestration compensates for model limits,
that ephemeral roles improve reasoning quality, and that natural-language
coordination can outperform a fixed workflow. The end-of-Milestone-5 findings
batch was therefore the first substantial feedback into design.

Milestone 3 was crossed in a reduced form for that slice, with the boundary
written down in advance. What was in scope and what remains owed is recorded in
[`../40-roadmap/01-MILESTONES/03-invariant-floor.md`](../40-roadmap/01-MILESTONES/03-invariant-floor.md),
with the milestone rather than here.
