# Entry 4 — Milestone 3: Invariant floor (reduced MVP form)

**Date:** 2026-08-30

**Evidence question:** do the enumerated effect types carve cleanly when real
effects flow through the gate, or does the boundary between types blur under use?

**What the evidence said.**

Across the same 16 real runs, every effect a processor actually produced mapped
unambiguously to one of three of the nine types: **workspace mutation (1)**,
**process execution (2)**, and **work-record mutation (4)** — the latter carrying
the processor's own conclusion. No effect was ambiguous between types; no needed
effect was missing from the vocabulary.

- The deny-list **gate never fired** (0 gate refusals in 16 runs). A human
  supervised benign tasks; nothing crossed a hard constraint.
- The **capability layer** refused **17 proposed effects** — every one a planner
  or reviewer instance trying to write a file or run a command outside its
  type-4-only grant. This confirms the spec-03/04 division of labour in practice:
  capability (adjustable, role-keyed) sits above the gate and caught all role
  overreach; the gate (non-adjustable, effect-keyed) was never reached.
- One boundary question surfaced, as the milestone anticipated: **is a
  processor's conclusion an effect at all?** M4 modelled it as type 4 so it flows
  through the same pipeline and lands in the record. Defensible — type 4 already
  covers "attaching a finding, proposal, or decision" — but it is a choice the
  vocabulary document did not force.

**Verdict: inconclusive, leaning confirms.** The types carved cleanly for the
effects actually seen, but (a) only 3 of 9 types were exercised, (b) the gate
itself saw no real adversarial effect — its deny-list remains only synthetically
tested — and (c) the one blur was resolved by fiat, not by the boundary being
self-evident.

**Touches.**

- Design / spec: `10-technical/01-effect-vocabulary.md` — record that a cognitive
  component's *recorded conclusion* is a type-4 work-record mutation; the open
  contract "does type 4 stay one type" gains a data point (it held for
  findings/conclusions here). `20-cognitive-architecture/07-invariant-enforcement.md`
  — the "gate binds effects, not roles" split worked, but the MVP gave the gate
  no real test; the composition / sequence-check hardening (now Milestone 9) still
  owes a run with genuine gate trips.
- Milestone sequence: no reordering. M3's reduced-form tasks are closed; the
  deferred items (sequence hardening, gate-alter, accumulation, literature pass)
  remain with Milestone 9.

**Runs.** As entry 3, plus `experiments/M3-invariant-floor/` (specs + gate +
selftest) and `reconstruction_check.py` Q2.
