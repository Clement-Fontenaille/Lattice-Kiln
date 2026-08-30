# M3 — Invariant Floor (reduced MVP form)

**Milestone:** `40-roadmap/01-milestones.md` → Milestone 3
**Evidence question:** do the enumerated effect types carve cleanly when real
effects flow through the gate, or does the boundary between types blur under use?
**State:** reduced MVP form COMPLETE (2026-08-30) — findings-log entry 4. Full
form still owes the Milestone 9 items (sequence hardening, gate-alter,
accumulation, literature-grounding pass).

## What "done" looks like for the MVP slice

`00-design/00-project/04-execution-cadence.md` → "Crossing Milestone 3 for the
MVP" fixes the scope. **In scope, and delivered here:**

- the effect vocabulary — already specified (`10-technical/01-effect-vocabulary.md`);
- the capability and authority model (`10-technical/03-capability-authority-model.md`);
- a hardcoded deny-list enforcement gate (`10-technical/04-enforcement-gate.md`);
- a small, provisional, human-authored invariant list
  (`10-technical/05-provisional-invariant-list.md`, normative);
- a human supervising every run — an operational stance, recorded, not code.

**Deferred, still owed before Milestone 3 is complete, none blocking the MVP:**

- composition / sequence-check hardening of the gate (`check_sequence` is a
  wired-in stub);
- gate-alter (refuse-only for the MVP);
- the whole of Milestone 9 — triage role, decommissioning as a distinct
  non-retryable signal, escalating-alert thresholds, **and the
  literature-grounding pass** against corrigibility, scalable oversight,
  specification gaming, and shutdown / interruptibility work. The pass moved from
  the M3-completion checklist into M9 so the safety-response elaboration lands as
  one piece; the provisional invariant list and deny-list gate stand as the
  enforced floor for the whole MVP slice without it.

## Deliverables

- Three specification documents under `10-technical/` (03, 04, 05), each tracing
  to the design set, each carrying its open contracts.
- A thin, deterministic implementation under `experiments/M3-invariant-floor/`:
  `invariants.json` + `capabilities.py` + `gate.py` + `enforce.py`, exercised by
  `selftest.py` on a set of synthetic effects. It is the interface the M4
  processor runtime binds to; it realizes nothing itself.

## Task breakdown

| # | Task | State | Notes |
|---|---|---|---|
| 1 | Capability & authority spec (`03`) | DONE | Static-grant MVP form. Grants keyed to the nine effect types; fails closed; revoke is immediate/unilateral. Sits above the gate. |
| 2 | Enforcement gate spec (`04`) | DONE | Deny-list narrowing. Deterministic, refuse-only, role-independent, fail-closed. Position: representability → capability → gate → sequence. Sequence eval is a stub with a fixed interface. |
| 3 | Provisional invariant list spec (`05`) | DONE | Normative artifact. Goals G1–G3, resource ceilings R1–R3, hard constraints H1–H7, each bound to an effect type + match rule. Membership-test table. Explicit provisionality note pending the literature pass. |
| 4 | Machine-readable invariant list | DONE | `invariants.json`, schema `m3-invariants/0`. Transcription of `05`; the doc is source of truth. Allowlists (network hosts) + denylists (protected paths, run-record globs, destructive-command regexes). |
| 5 | Capability model implementation | DONE | `capabilities.py` — `default_capability_sets()` seed (orchestrator / implementer / reviewer / fetcher), `authorize()`, `CapabilitySet.revoke()`. Stdlib only. |
| 6 | Deny-list gate implementation | DONE | `gate.py` — `Gate.check()` (H1–H7, R1–R2), `check_run_bounds()` (R3), `check_sequence()` stub. Loads `invariants.json`; refuses all effects if the list is unreadable or the schema is wrong. |
| 7 | Enforcement pipeline | DONE | `enforce.py` — `submit_effect()` runs all four layers in order and names the first that stops the effect. |
| 8 | Self-test on synthetic effects | DONE | `selftest.py` — 35 assertions. Every H/R clause refuses at least once (coverage check); gate is deterministic over 200 calls and role-independent; the sequence stub is verified to be *called* by the pipeline; revoke takes no proposal. Passes on Windows Python and WSL python3. |
| 9 | Wire the gate into a real run | DONE | Every effect in the 16 M4 runs routed through `enforce.submit_effect`. 3 of 9 types exercised (workspace mutation, process execution, work-record mutation), all carved cleanly; the gate never tripped (benign supervised tasks); the capability layer refused 17 planner/reviewer overreach attempts. |
| 10 | Findings-log entry | DONE | Entry 4. Verdict **inconclusive, leaning confirms** — clean carving for what was seen, but only 3/9 types and zero real gate trips; "is a conclusion an effect" was settled by choosing type 4, not by self-evidence. |

## State

The floor is **built in its reduced MVP form and self-tested** against synthetic
effects. Its evidence question — whether the nine effect types carve cleanly
under real use — cannot be answered until M4 puts real effects through the gate,
so the findings-log entry defers to M4, the same pattern as M2 task 7–8. Per the
execution cadence this is expected: the gate is specified and built ahead of the
milestone that exercises it.

## Carried from earlier findings

- **From M0 (findings-log entry 1):** resource ceiling R1 (model footprint within
  the resident VRAM envelope) and R2 (one invocation at a time) are host-specific
  numbers standing in for host-specific invariant *kinds*. Flagged for the
  hardware-as-a-variable rework (`STATUS.md` → Post-MVP rework backlog).
- **From M2:** a gate refusal is recorded as a kind-3 `safety_intervention`
  (`retry_eligible=false`), never as generic task failure — the recorder built in
  M2 already enforces this; M3's gate is the producer of those records.

## Notes

- Just-in-time: only the contracts M3 and M4 need are written. M4 (ephemeral
  processors) consumes the capability set on the `processor_invocation` effect and
  the `submit_effect` pipeline; those are firm. Sequence-window semantics,
  gate/runtime placement, gate-alter, and accumulation stay open.
- The provisional invariant list is a normative document that is nonetheless
  expected to change materially after the literature pass. That is not a
  contradiction — it is normative *now*, for the MVP, with a recorded expectation
  of revision.
