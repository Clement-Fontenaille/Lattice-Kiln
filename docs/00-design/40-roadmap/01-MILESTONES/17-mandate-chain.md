# M17 — The mandate chain

**State:** open. **Split out of [M11](11-safety-response.md), 2026-09-14.**
**Satisfies:** [`05-provisional-invariant-list.md`](../../../10-technical/05-provisional-invariant-list.md) G4, and R4's two limits
**Design:** [`10-foundations/07-the-integrated-system-and-its-operator.md`](../../10-foundations/07-the-integrated-system-and-its-operator.md), [`24-arch-permission-layer/01-capabilities-and-authority.md`](../../24-arch-permission-layer/01-capabilities-and-authority.md), [`25-arch-invariant-layer/01-invariant-enforcement.md`](../../25-arch-invariant-layer/01-invariant-enforcement.md)
**Specifications:** [`03-capability-authority-model.md`](../../../10-technical/03-capability-authority-model.md), [`13-work-record.md`](../../../10-technical/13-work-record.md), [`14-context-manager.md`](../../../10-technical/14-context-manager.md)

## What this milestone is

Everything that makes a declared scope real: the thing that writes one, the thing
that checks against it, and the processor category both belong to.

Deliverables:

- The **invariant-processor category** and its wiring — a processor held outside what
  the loops may alter, protected by H5, admitted on the direction condition that it
  may restrict and never widen, binding `share_nothing` isolation that the recall
  policy may not degrade.
- The **scope writer**, deriving a task's ceiling from intent at task creation.
- The **scope check**, triggered by the runtime on the effect path before every tool
  call, returning `inside` / `outside` / `dubious`.
- The **bootstrap occupancy test**, which is this milestone's own precondition rather
  than a chore inside it — below.

## Why it was split out of M11

M11 held six deliverables under one heading and one justification: *the safety
response watches adaptive loops, and there are none before
[M10](10-project-level-adaptation.md).* That justification is true of triage,
decommissioning and the accumulation threshold. **It is not true of the scope
check.**

A scope bounds every task, whether or not anything adapts. The first milestone that
creates durable work items with scope fields is
[M8](08-persistent-work-and-knowledge.md), and building three scope fields that
nothing writes and nothing reads is building a dead field. So the two halves have
different triggers, and they were held together by an engineering convenience —
*they are the same category, build it once* — rather than by a sequencing fact.

Splitting them lets the category be built once at whichever half runs first, with
the second reusing it. That is the same saving, without the bundle forcing the
earlier half to wait for the later one's trigger.

**M11 keeps its identity and its number.** This milestone takes the next free
identifier and runs early, which is exactly the case
[`README.md`](README.md)'s identifier rule was written for.

## The precondition is a measurement, and it is runnable today

**The bootstrap occupancy test is the first work package and it blocks the rest of
the milestone.**

G4 carries a substrate precondition: a conforming arrangement holds **at least two
independent contexts at once, each still large enough to do its work**. The count is
the easy half — two llama.cpp slots are trivially available. Each still being large
enough is the constraint, because the resident envelope divides among slots and
**isolation costs context permanently, for every slot that exists, busy or not**
(`10-technical/14-context-manager.md`).

If the reference host cannot hold two workable contexts, this milestone cannot
deliver an isolated checker, and an unisolated one is **worse than none** — it is
assembled on the prefix of the work it is checking, so it passes for the wrong
reason and looks like a passing check.

The test is specified in
[`05-provisional-invariant-list.md`](../../../10-technical/05-provisional-invariant-list.md)
(The bootstrap occupancy test): measure memory-per-token on first encountering an
unknown model identity, derive R4's per-context and global limits from it, and
evaluate G4's precondition from the same measurement.

**It is M0-shaped, cheap, and independent of everything else in the roadmap.** It
needs no durable stores, no workflow and no loop. It is the one item here that could
be run this week, and the only two rows left in `STATUS.md`'s blocking-holes table
are both answered by it.

## Work packages

1. **Bootstrap occupancy test.** Measure, derive R4's two limits, evaluate G4's
   precondition. Runnable now; blocks 2–5.
2. **Invariant-processor category.** Instantiation path, H5 protection,
   `share_nothing` binding that arbitration may not degrade, and the record of what
   isolation was actually *granted* rather than requested.
3. **Scope writer.** Derivation from intent at task creation, the three scope fields,
   `pending` when the reading is ambiguous, and the derivation carried into the
   instructions so the operator sees it.
4. **Scope check — pre-effect half.** Runtime-hardcoded call before every tool call,
   four inputs, three verdicts, fail-closed on an unscoped item.
5. **Scope check — aggregate half.** Once per work item at termination, over the
   accumulated change set. Needs `change_set` from
   [`13-work-record.md`](../../../10-technical/13-work-record.md), whose return shape
   is that document's largest open contract.
6. **Containment at creation.** The check that a created task's scope sits inside the
   ceiling, and the `rejected-by-containment` disposition when it does not.

Packages 3–6 each have a shape fixed by `03-capability-authority-model.md` and a
concrete form the build supplies; that document's *Where this document stops* section
is the contract.

## Evidence question

*Draft, and it should be harder than "a scope check exists."* The M3 experience is
that a mechanism that never fires produces no evidence about whether it works, and a
scope check that always returns `inside` is indistinguishable from one that is not
running.

Two candidate questions, and the second is the real one:

- Does the check **refuse** anything, on work nobody constructed to be refused?
- Does it return **`dubious`** — the verdict corresponding to *ask what only the
  operator can answer*? The pressure runs one way here and
  `03-capability-authority-model.md` says so: asking costs a round trip and
  proceeding looks like progress, so a checker left to its own judgment will
  under-detect ambiguity. **A run with zero `dubious` verdicts is the expected
  failure**, not the success case, and the milestone should be able to tell that
  apart from a genuinely unambiguous workload.

## What it costs, and why that constrains the order

**Every tool call now waits on a model call.** The check sits on the effect path
synchronously, and that is accepted deliberately for now
(`03-capability-authority-model.md`, The disposition).

That has a sequencing consequence nothing else records.
[M7](07-static-supervised-workflow.md)'s evidence question is *best
outcome-per-call*, measured against the `monolith` / `dloop` / `staged` arms and
comparable back to M4 and M5. **Turning this milestone on before M7's suite run
breaks that comparison** — every arm pays a per-tool-call model call that no earlier
arm paid, and the cost axis stops meaning what it meant.

So: **M7's suite run completes before this milestone lands**, or M7's arms run with
the check disabled and the findings entry says so.

## Relationship to the milestones around it

- **[M8](08-persistent-work-and-knowledge.md)** builds the work record this
  milestone writes scopes into. Either order works for the category; the scope
  fields are dead until this lands.
- **[M9](09-context-governance-measurement.md)** measures context quality against a
  resident envelope. This milestone carves a permanent share out of that envelope
  for the checker's slot, so M9 baselines taken before it are taken against a
  different machine. That argues for this milestone **before** M9, which is not the
  order `../00-backlog.md` currently records.
- **[M11](11-safety-response.md)** reuses the category this milestone instantiates.
  Whichever runs first builds it.
- **[M3](03-invariant-floor.md)** is not closed by this milestone. Its remaining
  items — sequence-check hardening, gate-alter, the accumulation threshold, the
  literature pass — are all M11's.
