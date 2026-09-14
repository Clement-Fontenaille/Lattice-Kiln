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
- The **literature-grounding pass** against corrigibility, scalable oversight,
  specification gaming, and shutdown and interruptibility work.

## What moved out, and why

The **scope check** and the **scope writer** were deliverables here until 2026-09-14.
They are now [M17](17-mandate-chain.md).

They were here because this milestone instantiates **invariant processors** as a role
category, and triage is one — so all three needed the same thing built once. That
saving is real and survives the split: whichever of the two milestones runs first
builds the category, and the other reuses it.

What does not survive is the sequencing. *Why it is placed this late*, below, argues
that the safety response watches adaptive loops and there are none before
[M10](10-project-level-adaptation.md). **That argument does not cover a scope check**,
which bounds every task whether or not anything adapts, and which
[M8](08-persistent-work-and-knowledge.md) makes necessary the moment durable work
items carry scope fields. Keeping them bundled would have held the earlier half to the
later half's trigger for no reason but shared machinery.

G4 is therefore satisfied by M17 and not here.

## Work packages

1. **Triage role.** Assesses a tripped gate and routes: log-and-proceed, escalate, or
   halt. Reuses M17's invariant-processor category, or builds it if M17 has not run.
2. **Gate `alter` disposition.** The only one of the gate's dispositions still
   unimplemented apart from the threshold; it is what triage acts through.
3. **Decommissioning.** Immediate, unilateral runtime revocation targeting a running
   `invocation_id` rather than a role, plus its distinct non-retryable failure signal.
4. **Escalating-alert threshold.** Converts accumulated individually-innocuous trips
   into a mandatory stop. Needs the sequence-check hardening M3 also owes.
5. **Sequence-check hardening.** The gate evaluates effects one at a time and the
   sequence hook is stubbed. Closes M3 item 1 alongside 2 and 4.
6. **Literature-grounding pass**, and the revision of the invariant list and the gate
   against what it finds.

Package 6 revises what packages 1–5 built, which is deliberate and is the reason the
pass was moved here from [M3](03-invariant-floor.md) — see below. An implementation
order that treats 6 as a final sign-off rather than as a revision trigger has missed
the point of moving it.

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

The shape to aim for, borrowed from [M17](17-mandate-chain.md)'s draft: ask what the
mechanism does on work **nobody constructed to trip it**. A triage role evaluated
only on deliberately-tripping cases has been shown to route correctly and has said
nothing about whether it fires when it should, or stays quiet when it should not.
