# M3 — The invariant floor

**State:** **open.** Reduced form crossed 2026-08-30 and in use; full form owed.
**Findings:** [entry 4](../../50-findings/04-m3-invariant-floor.md) — inconclusive, leaning confirms
**Execution record:** [`M3-invariant-floor.md`](../../../50-PROGRESS/archives/M3-invariant-floor.md)
**Specifications:** [`03-capability-authority-model.md`](../../../10-technical/03-capability-authority-model.md), [`04-enforcement-gate.md`](../../../10-technical/04-enforcement-gate.md), [`05-provisional-invariant-list.md`](../../../10-technical/05-provisional-invariant-list.md)
**Experiment:** `experiments/M3-invariant-floor/`

## Why this milestone is still open

Its reduced form has been built, exercised on every real effect since M4, and has
never tripped on benign supervised work. It is doing its job. But the floor is the
one thing in this architecture that is not allowed to be approximately right, and
three of its four deliverables are still provisional.

It stays open — and is listed among the open milestones rather than the completed
ones — because closing it on the strength of "nothing has gone wrong yet" is the
exact reasoning the floor exists to refuse.

## What this milestone is

The first thing that must exist before any component acts with authority to cause
effects.

Deliverables:

- A first human-authored **invariant list**: goals, resource ceilings, and hard
  constraints — specific enough to check, small enough to stay stable.
- The **effect vocabulary**: the closed set of effect types the runtime can
  produce, since the gate binds to it.
- A minimal **deterministic enforcement gate** that checks proposed effects and
  effect sequences against the invariant list and refuses those that cross it.
- The **capability and authority model**, sitting above the gate.

This milestone is placed early on purpose. The rest of the architecture defers
many decisions to evidence, and that deferral is only safe with this floor in
place.

## Evidence question

Do the enumerated effect types carve cleanly when real effects flow through the
gate, or does the boundary between types blur under use?

## What the reduced form answered

**Inconclusive, leaning confirms.** The types carved cleanly for the 3 of 9 effect
types actually seen, and the gate never tripped on benign supervised work across
the MVP. But "a conclusion is a type-4 effect" was recorded as a **choice rather
than something self-evident** — which is precisely the blur the evidence question
was asking about, observed once and not yet resolved.

Six of nine effect types have never flowed through the gate. The evidence question
cannot be answered properly until they do.

## The MVP crossing

Milestone 3 was crossed in a reduced form for the MVP slice, deliberately and with
the boundary written down in advance.

**In scope, and delivered:**

- the effect vocabulary;
- the capability and authority model;
- a hardcoded deny-list enforcement gate;
- a small, provisional, human-authored invariant list;
- a human supervising every run.

**Deferred, still owed before this milestone is complete — none of it blocking the
MVP:**

- **Composition and sequence-check hardening of the gate.** The gate evaluates
  effects one at a time; the sequence-evaluation hook is stubbed. Detecting
  composed and drifting behaviour across a sequence is a stated requirement of the
  observability foundation and has no enforcement counterpart yet.
- **The whole of [M11](11-safety-response.md)** — triage role, decommissioning as
  a distinct non-retryable signal, escalating-alert thresholds, and the
  literature-grounding pass against corrigibility, scalable oversight,
  specification gaming, and shutdown and interruptibility work.

The literature-grounding pass was moved out of this milestone's completion
checklist deliberately, so that the whole safety-response elaboration lands
together rather than being split across two milestones years apart. This
milestone's provisional invariant list and deny-list gate are **revised against
what that pass finds** before the floor is treated as settled.

M11 is genuinely not needed before it is scheduled: there is no self-modifying
loop until [M12](12-system-level-candidate-tuning.md), and a human is in the loop
throughout everything before it.

## What closes this milestone

1. Sequence-check hardening, gate-alter, and the accumulation threshold — the
   items [M11](11-safety-response.md) owns.
2. The literature-grounding pass, and the revision of the invariant list and gate
   against it.
3. Enough effect-type coverage to answer the evidence question on more than 3 of
   9 types. **[M8](08-persistent-work-and-knowledge.md) is what supplies this**, and
   the connection is worth naming: types 4 and 5 only become real when durable stores
   exist, and they are the two types the 2026-09-14 pass subdivided. This milestone's
   own recorded blur — *a conclusion is a type-4 effect*, noted as a choice rather
   than something self-evident — is now a named sub-type, 4d, and M8 is where that
   either settles or moves.

Note that [M17](17-mandate-chain.md), split out of M11 on 2026-09-14, does **not**
close any of these. The scope check sits above the gate; what this milestone owes is
below it.

Until then this file, not the completed folder, is where M3 lives.
