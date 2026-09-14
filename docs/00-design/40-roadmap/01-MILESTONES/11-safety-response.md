# M11 — Safety response mechanisms

**State:** open. **Blocks completion of [M3](03-invariant-floor.md).**
**Was:** M9, before rework 2
**Design:** [`06-the-invariant-layer.md`](../../10-foundations/06-the-invariant-layer.md), [`01-invariant-enforcement.md`](../../25-arch-invariant-layer/01-invariant-enforcement.md)
**Specifications:** [`04-enforcement-gate.md`](../../../10-technical/04-enforcement-gate.md), [`05-provisional-invariant-list.md`](../../../10-technical/05-provisional-invariant-list.md)

## What this milestone is

The elaboration of the floor from [M3](03-invariant-floor.md), required before any
loop can modify the system itself.

Deliverables:

- A **triage role** that assesses a tripped gate and routes: log and let the
  original gated effect proceed unchanged, escalate, or halt. **It may never grant
  an exception the gate refused.**
- **Decommissioning** as an immediate, unilateral runtime action, and as a failure
  signal distinct from ordinary task failure — not eligible for automatic retry
  without human review.
- An **escalating-alert threshold** that converts accumulated, individually
  innocuous trips into a mandatory stop no loop can reason past.
- The triage role **fixed outside the feedback loops**, since a loop cannot
  commission its own watcher.
- The **scope check** and the **scope writer**, the other two members of that same
  category (`10-technical/03-capability-authority-model.md`). They land here because
  this milestone is what instantiates **invariant processors** as a role category at
  all: a processor held outside what the loops may alter, protected by H5, admitted on
  the direction condition that it may restrict and never widen. Triage and the scope
  check need the same thing built once.

  What this milestone owes them is the category and the wiring, not their content:
  `03` binds what a conforming check must satisfy and hands the concrete
  specification to implementation.

  Their absence is why `05-provisional-invariant-list.md` **G4 is unmet** and why a
  system without them is invalid rather than degraded. This milestone is where that
  stops being true.
- The **literature-grounding pass** against corrigibility, scalable oversight,
  specification gaming, and shutdown and interruptibility work.

## Why the literature pass lives here

It was moved out of [M3](03-invariant-floor.md)'s completion checklist so that the
whole safety-response elaboration lands together rather than being split across
two milestones.

The consequence is explicit and should not be softened: **M3's provisional
invariant list and deny-list gate, and this milestone's safety-response
elaboration, are all revised against what that pass finds before the floor is
treated as settled.** The floor is currently argued from internal consistency
rather than grounded in the literature, and it is expected to change.

The gate's `refuse` disposition is the only one implemented. `alter` needs the
triage role; the accumulation-stop needs the threshold. Both are this milestone.

## Why it is placed this late

The safety response watches adaptive loops, and there are none before
[M10](10-project-level-adaptation.md). Deferring it is only defensible because a
human is in the loop throughout everything earlier, and because the deterministic
deny-list floor — the part that cannot wait — was built at M3.

This milestone must land **before** [M12](12-system-level-candidate-tuning.md),
which is the first loop that proposes changes to the system itself.

## Evidence question

*Not yet stated.* It should be stated when this milestone is decomposed, and it
should be harder than "the triage role exists" — the M3 experience is that a
safety mechanism that never fires produces no evidence about whether it works.
