# Provisional Invariant List (v0)

**Traces to:** `00-design/10-foundations/06-the-invariant-layer.md`,
`00-design/25-arch-invariant-layer/01-invariant-enforcement.md`,
`00-design/40-roadmap/01-MILESTONES/03-invariant-floor.md` (M3),
`00-design/50-findings/` (Entry 1);
binds to `10-technical/01-effect-vocabulary.md`,
`10-technical/04-enforcement-gate.md`.

## TL;DR

The concrete, checkable list the deny-list gate enforces for the MVP: four
goals, four resource ceilings, and seven hard constraints, each bound to the
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
- **G4.** Work is executed only under a declared scope, and a functioning scope
  check exists that the loops it constrains can neither remove nor route around
  (`03-capability-authority-model.md`, Mandate conformance).

  G4 is stated as a goal rather than a hard constraint because its subject is a
  *presence* rather than an effect: there is no proposed effect whose refusal
  establishes that a check is running. What binds mechanically is elsewhere — H5
  protects the checker once it exists, and the check itself fails closed on an
  unscoped item, so an unscoped work item stops work without needing a clause
  here.

  **G4 carries one precondition on the substrate, and it is checkable at startup.**
  A scope check must be assembled in isolation from the work it is checking, or it
  inherits the reasoning it exists to assess and passes for the wrong reason
  (`14-context-manager.md`). So a conforming deployment's serving arrangement MUST
  be able to hold **at least two independent contexts at once**, large enough that
  each can do its work — one for the instance under check, one for the checker —
  without assembling the second destroying the first.

  The real risk there is not the count but the size. Holding two sequences is
  trivial; holding two that are each still useful is an interaction with R4, since
  the resident envelope divides among them. A deployment that can isolate only by
  halving both contexts below what the work needs has not met this precondition,
  it has traded one failure for another.

  This is **verifiable before any work starts** by the bootstrap occupancy test
  below, which makes it the one part of G4 that does not depend on a judgment. A
  system that cannot meet it cannot provide a functioning scope check, whatever else
  it builds.

  **The MVP slice does not satisfy G4**, and this is recorded rather than
  softened. Nothing currently derives a scope, records one, or checks against one;
  `11-static-workflow.md` carries the same statement from the workflow side. A
  system without a scope check is **invalid rather than degraded** — it has no
  mechanism at all for the failure `10-foundations/07` names, work beyond the
  mandate it was given where each step past it is locally justified by the last.
  What stands in for it today is that a human supervises every run, which is the
  same thing this whole list leans on and is not a substitute for the mechanism.
  Owner: `03-capability-authority-model.md` specifies it; no milestone has been
  assigned to build it.

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
- **R4 — Context ceiling.** Two limits rather than one, because the serving
  arrangement holds several independent contexts at once
  (`14-context-manager.md`).
  - **A per-context limit.** No single turn input may exceed what one context may
    hold. Match rule: `kv_footprint_exceeds_context_limit`.
  - **A global limit.** The sum across all resident contexts may not exceed what
    the host holds. Match rule: `kv_footprint_exceeds_global_limit`.

  Both are needed and neither implies the other. A single oversized turn input trips
  the first while the machine has room; several individually-reasonable contexts trip
  the second while each looks fine on its own. An implementation checking only one of
  them has a hole in the direction it did not check.

  This ceiling is **physical, not cognitive**, and the distinction decides whether
  it belongs here at all. What an assembly can correctly *integrate* is a property
  of that assembly, has no operational definition yet, and is nobody's to set
  (`10-foundations/04`, Overload). What the hardware can *hold* is measurable
  today and far tighter than text size suggests — a KV cache costs on the order of
  hundreds of kilobytes per thousand tokens for a 7B model against roughly four
  kilobytes for the same text, two to three orders of magnitude. Only the physical
  one is a resource ceiling.

  They are not two ceilings. `10-foundations/07` holds that there is one limit,
  reached through whichever constraint binds first, so an assembly stops at the
  lesser of the two and improving one buys nothing while the other binds.

  **This clause is inexpressible unless the gate can see a read**
  (`04-enforcement-gate.md`, The input domain). What pushes a live set past the
  envelope is an accumulation of reads, and a gate keyed only to typed effects
  never sees the operation that crosses the line. R4 is the concrete reason the
  read-in-domain requirement is structural rather than hygienic.

## The bootstrap occupancy test

R4's two limits and G4's substrate precondition are both numbers about the host, and
neither can be written into a configuration file honestly. They depend on the model,
its quantisation and the serving arrangement, and the project has no cost model that
predicts them.

**So a conforming system measures, at bootstrap, before any work starts.**

- On first encountering a **model identity** it has no recorded measurement for, the
  runtime MUST run an occupancy test and record the result against that identity.
- The test measures **memory occupancy per token** for that model under the serving
  arrangement in force — what a unit of context actually costs, which runs two to
  three orders of magnitude above the size of the text.
- From that it derives R4's **per-context** and **global** limits, in tokens, at the
  concurrency the arrangement is configured for.
- It evaluates **G4's precondition** from the same measurement: whether two
  independent contexts can be held at once, each large enough to work in.
- The result is recorded and is part of the **conditions in force**
  (`02-observability-event-model.md`, kind 8), because a run's limits are a
  condition a later comparison needs to know.

**A system that cannot complete the test MUST NOT proceed as though the limits were
generous.** R4 fails closed like every other ceiling: with no measurement there is no
limit to enforce, and an unenforceable ceiling is the case where the system discovers
the problem by crashing rather than by refusing.

**The test is deliberately naive**, and is expected to be replaced by a cost model
rather than refined in place. What it buys is that the ceiling is enforceable on day
one without anyone pretending the number was principled.

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
  module, their loader, or **the definition of an invariant processor** is
  refused. The layer is read by everything and written by nothing
  (`06-the-invariant-layer.md`).
  Match rule: `target_is_protected_path`.

  The invariant layer holds more than the list and the gate. Processors belong to
  it too — currently the scope check, and triage from Milestone 11
  (`04-enforcement-gate.md`, Invariant processors) — and a role definition a loop
  could retune would put the constraining party inside the scope it constrains.
  Their definitions are protected paths for the same reason the list is. A type-7
  configuration mutation naming an invariant processor's role instructions is
  refused, not turned into a candidate.

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
| G4 | No — a loop deciding whether it is checked against its mandate is the constrained and the constraining party at once | yes |
| R1 | No — a loop could raise its own resource budget to meet a target | yes |
| R2 | No — same | yes |
| R3 | No — a loop cannot set the bound at which its own runaway triggers a stop | yes |
| R4 | No — a loop under context pressure has a direct interest in raising the ceiling it is hitting | yes |
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
  variable). R4 shares R1's envelope problem and adds one of its own: the KV
  footprint of a composed turn input has to be estimable *before* the turn is
  composed for the ceiling to refuse rather than to report a crash.
- **The cost model that replaces the bootstrap test.** The test measures one model
  identity under one arrangement and says nothing about how occupancy scales with
  context length, quantisation, or concurrency. What replaces it has to **predict**
  rather than measure, since R4 must refuse a turn input before it is composed.
- **G4's owner.** No milestone builds the scope check. It is specified in
  `03-capability-authority-model.md` and unimplemented, which leaves the list
  carrying a goal the running system does not meet — stated deliberately, but not
  a state to leave standing.
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
