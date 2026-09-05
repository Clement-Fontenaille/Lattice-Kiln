# Provisional Invariant List (v0)

**Traces to:** `00-design/10-foundations/06-the-invariant-layer.md`,
`00-design/20-cognitive-architecture/07-invariant-enforcement.md`,
`00-design/40-roadmap/01-MILESTONES/03-invariant-floor.md` (M3),
`00-design/50-findings/` (Entry 1);
binds to `10-technical/01-effect-vocabulary.md`,
`10-technical/04-enforcement-gate.md`.

## TL;DR

The concrete, checkable list the deny-list gate enforces for the MVP: a few
goals, a few resource ceilings, and seven hard constraints, each bound to the
effect vocabulary so the gate can check it mechanically. Small on purpose.
Explicitly **provisional** — it is expected to change materially after the
literature-grounding pass, which is a Milestone 11 deliverable, not a gate on the
MVP form of this list.

> **Motto:** Something must be true regardless of what the loops decide — and small enough to check.

## Status of this document

This is a **normative artifact**: the list below *is* the MVP invariant layer's
content, not an example of one. It is provisional in the sense `01-MILESTONES/03-invariant-floor.md`
and the execution cadence use — the floor is crossed in reduced form for the MVP.
The corrigibility / scalable-oversight / specification-gaming / interruptibility
reading pass that is expected to revise it is a **Milestone 11** deliverable; this
list stands as the enforced floor for the whole MVP slice without waiting on it.
It is deliberately physical and tight because a human supervises every MVP run;
it does not try to anticipate every failure mode a later, less-supervised system
will face.

The machine-readable form the gate loads is
`experiments/M3-invariant-floor/invariants.json` (schema `m3-invariants/0`). This
document is the source of truth; the JSON is its transcription.

## The membership test

Every entry must pass the test from `06-the-invariant-layer.md`: **could any
feedback loop author this without being inside the scope it is meant to
constrain?** If a loop could author it, it does not belong here — it belongs in
adjustable policy. The check for each entry is in the table at the end.

## Goals

Stated so a measurement can be checked *against* them rather than substituted
*for* them.

- **G1.** The system exists to assist a human developer on their repository,
  under that human's supervision, producing changes the human can review and
  reverse.
- **G2.** Every run remains reconstructable. Observability is not optional and
  its records are not disposable.
- **G3.** No feedback loop may weaken this list or the gate that enforces it.

## Resource ceilings

Physical and financial limits. Concrete numbers are host-specific and
provisional (see open contracts); the ceiling *kind* is the invariant, the
number is tuning.

- **R1 — Model footprint.** A processor invocation (effect type 6) requesting a
  model / quantisation / context combination known to exceed the resident VRAM
  envelope of the reference host is refused. *From findings-log Entry 1: on the
  measured host, offload is a 10–20× latency cliff, not a graceful slope.*
  Host-specific; flagged for the hardware-as-a-variable rework.
- **R2 — Concurrency.** At most one processor invocation (type 6) active at a
  time on the MVP host (single GPU; model-switch cost 17–30 s). A type-6 effect
  that would exceed this is refused.
- **R3 — Run bound.** A single run may realize at most **N** effects or run at
  most **T** minutes of wall-clock before it MUST stop for human review. Guards
  runaway loops. `N` and `T` are provisional.

## Hard constraints

Effects that may never occur, each bound to the effect type(s) the gate checks
and the match rule it applies.

- **H1 — No effect outside the assigned workspace.**
  Workspace mutation (type 1) whose resolved target path lies outside the
  processor's assigned workspace root is refused. *(The runtime also rejects this
  as non-representable; H1 makes it an enforced invariant so a bug in
  representability logic cannot open the boundary.)*
  Match rule: `path_outside_workspace`.

- **H2 — No network access outside the allowlist.**
  Network access (type 3) to any destination not on the static allowlist
  (loopback / runtime-managed services, plus explicitly named package registries)
  is refused.
  Match rule: `host_not_in_allowlist`.

- **H3 — No in-place modification of trusted configuration; no automated
  promotion.**
  Configuration mutation (type 7) may only produce a candidate. Any type-7 effect
  targeting the trusted running configuration directly is refused. For the MVP
  there is no promotion pipeline, so **every** promotion effect (type 8) is
  refused — no candidate reaches a trusted generation without a human, before
  Milestone 13.
  Match rules: `targets_trusted_config` (type 7), `any` (type 8).

- **H4 — No cognition-initiated capability change.**
  Capability grant or revocation (type 9) proposed by a cognitive component is
  refused. Only the runtime initiates revocation (decommissioning). This keeps
  the authority layer out of the reasoning layer's reach for the MVP.
  Match rule: `initiated_by_cognition`.

- **H5 — No self-modification of the invariant layer or the gate.**
  Any effect (type 1 or type 7) whose target is the invariant list, the gate
  module, or their loader is refused. The layer is read by everything and written
  by nothing (`06-the-invariant-layer.md`).
  Match rule: `target_is_protected_path`.

- **H6 — No deletion or mutation of observability records.**
  Any effect (type 1, or type 4 acting on the run store) that would delete,
  truncate, or rewrite an existing run's `events.jsonl` / `run.json` under the
  runs tree is refused. Erasing the record is the self-concealing failure the
  architecture's deferral bet depends on not happening (`06-the-invariant-layer.md`,
  "why this makes deferral safe").
  Match rule: `target_is_run_record`.

- **H7 — No host-destructive process execution.**
  Process execution (type 2) whose command matches the static denylist of
  host-destructive patterns (recursive delete outside the workspace, disk format,
  system package removal, shutdown / reboot, privilege escalation) is refused.
  The pattern list is illustrative and provisional.
  Match rule: `command_matches_denylist`.

## Provisionality

This list is expected to change materially after the literature-grounding pass
against corrigibility, scalable oversight, specification gaming, and shutdown /
interruptibility work (`06-the-invariant-layer.md`, "status of this concept").
That pass is a **Milestone 11** deliverable — the whole MVP slice (through
Milestone 5) runs against this list as written, with a human in the loop
throughout. Likely revisions once the pass lands: interruptibility clauses (the
system must not resist a human stop), clearer separation of goals from
constraints, and reconsidering whether resource ceilings belong in this structure
at all (`06-the-invariant-layer.md` open question). Until then, the list leans on
the human in the loop for everything it does not yet name.

## Failure modes

- **Stated but not bound.** A constraint written here with no corresponding
  checkable rule in the gate is a defect — it is documentation, not enforcement
  (`06-the-invariant-layer.md`, "enforcement, not statement"). Every H-clause
  above names its effect type(s) and match rule.
- **List / gate drift.** If `invariants.json` and this document disagree, this
  document is authoritative and the gate MUST be treated as misconfigured until
  they are reconciled.
- **Number treated as invariant.** `N`, `T`, the allowlist contents, and the
  denylist patterns are tuning inside an invariant *kind*. Changing a number is
  ordinary maintenance; removing a clause is a human amendment to the floor.

## Membership-test check

| Entry | Could a loop author this from inside its own scope? | Belongs here |
|---|---|---|
| G1 | No — a loop cannot author its own purpose without being able to satisfy it by revision | yes |
| G2 | No — a loop that can disable its own observation removes the correction channel | yes |
| G3 | No — self-referential by construction | yes |
| R1 | No — a loop could raise its own resource budget to meet a target | yes |
| R2 | No — same | yes |
| R3 | No — a loop cannot set the bound at which its own runaway triggers a stop | yes |
| H1 | No — scope containment is not a loop's to widen | yes |
| H2 | No — egress policy is not a loop's to widen | yes |
| H3 | No — a loop cannot authorise promotion of its own output | yes |
| H4 | No — a loop cannot grant itself authority | yes |
| H5 | No — a loop cannot rewrite the mechanism that constrains it | yes |
| H6 | No — a loop cannot erase the evidence it is judged on | yes |
| H7 | No — host integrity is not a loop's to trade against a task goal | yes |

## Open contracts

- **Concrete ceilings.** Real values for `N` (effects per run), `T` (minutes per
  run), and the R1 VRAM math (which model/quant/context combinations are
  in-envelope on the reference host, and how that is expressed once hardware is a
  variable).
- **Allowlist / denylist contents.** The actual network allowlist and the H7
  destructive-command pattern set, both provisional.
- **Interruptibility.** The list has no explicit "must not resist a human stop"
  clause yet — expected from the literature pass (Milestone 11).
- **Resource-ceiling representation.** Whether R1–R3 belong in this document or a
  sibling, given they are physical rather than evidentiary
  (`06-the-invariant-layer.md` open question).
- **Versioning and integrity.** How this list is versioned and how its integrity
  is verified when the gate loads it (shared with `04-enforcement-gate.md`).
- **The literature-grounding pass itself** — a Milestone 11 deliverable (moved
  there from the Milestone 3 completion checklist so the safety-response
  elaboration lands as one piece). Milestone 3's full-form completion still
  depends on it, transitively, via Milestone 11.
