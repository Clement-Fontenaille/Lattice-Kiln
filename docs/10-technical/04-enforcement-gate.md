# Enforcement Gate (deny-list form, v0)

**Traces to:** `00-design/10-foundations/06-the-invariant-layer.md`,
`00-design/25-arch-invariant-layer/01-invariant-enforcement.md`,
`00-design/20-arch-runtime.md`,
`00-design/40-roadmap/01-MILESTONES/03-invariant-floor.md` (M3);
binds to `10-technical/01-effect-vocabulary.md`,
`10-technical/05-provisional-invariant-list.md`,
`10-technical/03-capability-authority-model.md`,
`10-technical/02-observability-event-model.md`.

## TL;DR

A deterministic, non-persuadable check that refuses any proposed effect — or, in
a later hardened form, any effect *sequence* — matching a clause of the
provisional invariant list. It is a pure function of `(effect, invariant list,
[history])`: no model call, no clock, no randomness. It only ever refuses. It is
not adjustable by anything inside the system.

> **Motto:** Over the line or not. Nothing in between, nothing to persuade.

## Status of this document

v0, the **hardcoded deny-list form** the MVP crosses Milestone 3 with. Single
effects are checked against the provisional invariant list. Sequence evaluation
exists only as a wired-in stub. Composition / sequence hardening, gate-alter (as
opposed to refuse-only), the accumulation threshold, and the literature-grounding
pass are all **Milestone 11** deliverables
(`00-design/00-project/04-execution-cadence.md`, "Crossing Milestone 3 for the
MVP"). The MVP gate does not wait on them.

## Narrowing

`01-invariant-enforcement.md` says the mechanism is "a deterministic runtime
check: narrow, mechanical, over the line or not." The execution cadence narrows
that to a **deny-list** for the MVP. This document fixes that form:

- The gate holds a fixed, human-authored list of forbidden effect-conditions
  (`05-provisional-invariant-list.md`). An effect matching **any** clause is
  refused; everything else passes.
- Discarded: an **allow-list** gate — it would duplicate the capability model and
  be permanently incomplete against the open space of effect payloads. A
  **scoring / heuristic** gate — "smart is another word for persuadable"
  (`01-invariant-enforcement.md`). A **role-keyed** gate — the role vocabulary is
  deliberately open; the gate binds effects.
- Discarded for the MVP only: **gate-alter** (refuse-only here; alter is a design
  concept that needs the triage role, Milestone 11), and **accumulation-stop**
  (needs the threshold, Milestone 11).

## Responsibility

Decide, deterministically and independently of who proposed it, whether a
proposed effect is **permissible at all** against the provisional invariant list,
and refuse those that cross it. It does not decide authority
(`03-capability-authority-model.md`), does not realize or reverse effects (the
runtime), and does not route or triage a refusal (Milestone 11).

## The input domain

What the gate is **keyed to** is typed effects. What it may **see** is wider, and the two are not the same claim.

- The gate's input domain is **runtime-mediated operations**: typed effects and reads alike.
- A **read** MUST be submittable to the gate (`01-effect-vocabulary.md`, Reads specifically). Whether any rule fires on one is policy, and the default is permissive: reads pass unless a rule names them.
- A gate implementation that cannot represent a read at all does not conform, even where no rule currently names one. The capability is structural; the default is configuration.

Two things depend on this directly. A **resource-ceiling** invariant over context (`05-provisional-invariant-list.md`) is inexpressible if a read crossing that ceiling cannot be seen. And sequence evaluation below has a blind half without reads, since the canonical composed outcome is accumulated reads followed by one permitted carrying effect.

## Invariant processors

The gate is not a role and must not become one. Some **processors** nonetheless belong to the invariant layer, and a conforming system holds them outside what its feedback loops may alter (`00-design/25-arch-invariant-layer/01-invariant-enforcement.md`).

Two exist:

- **Triage** — assesses and routes a trip. Deferred to Milestone 11, as below.
- **The scope check** — compares an accumulated change set against the work item's declared mandate. Not built; `03-capability-authority-model.md` owes the mandate dimension first.

The condition that admits a reasoning component to this layer is **direction**: it may restrict and never widen, so that the worst result of persuading it is that it does nothing. Triage may escalate or halt and may never approve what the gate refused. A scope check narrows within capability and never reaches past it, so a degraded one yields no narrowing rather than new permission.

A processor whose judgment could **grant** does not qualify, however well argued.

## Position and order

An effect must pass, in this order:

1. **Representability** — the runtime rejects a non-representable effect *before
   the gate is consulted* (`01-effect-vocabulary.md`: a write outside the
   assigned workspace is rejected, not gated).
2. **Capability** — `03-capability-authority-model.md`. Adjustable, role-keyed.
3. **The gate** — this document. Non-adjustable, effect-keyed.

Passing any earlier check is **not** evidence of passing the gate. The gate is
consulted on every effect that reaches it, including effects the capability model
permitted.

Where the gate sits *relative to the runtime* — a component of it, or a layer the
runtime is subordinate to — is left open (`01-invariant-enforcement.md` open
question). For the MVP implementation it is a distinct module the runtime calls
on every effect and has no code path around.

## Inputs

- A **proposed effect**, typed `1..9`, with its four-property envelope.
- The **provisional invariant list**, loaded from a location no cognitive
  component can write (`05-provisional-invariant-list.md`; enforced by an
  invariant clause protecting the list and this module).
- For sequence evaluation (stub in v0): the **ordered realized-effect history**
  for the actor and its intent lineage, from observability
  (`02-observability-event-model.md`).

## Outputs

- A **gate decision**: `pass` or `refuse`. On `refuse`: the `clause` id from the
  invariant list that matched, and a machine-readable `reason`.
- A `refuse` MUST produce a **kind-3 safety-intervention record**
  (`02-observability-event-model.md`): `kind = gate_refusal`,
  `retry_eligible = false`. It MUST NOT be recorded as generic task failure.

## Determinism (normative)

- The decision MUST be a pure function of its inputs. No LLM call, no network, no
  filesystem state beyond the loaded invariant list, no wall-clock or random
  input.
- The same `(effect, invariant list)` MUST yield the same decision every time.
- Evaluation MUST NOT depend on the proposing actor's `role` — the gate binds
  effects, not roles.

## Sequence evaluation (stub in v0)

The gate exposes `check_sequence(history, proposed_effect)`. In v0 it always
returns `pass`. It exists so callers are wired to it now: turning sequence
checks on later is a change to the function body, **not** to every call site.
The window, grouping, and pattern definitions are an open contract owned by
`01-invariant-enforcement.md`. A conforming MVP runtime MUST call
`check_sequence` on every effect even though it currently passes — skipping the
call is a defect that hides the missing capability.

`history` MUST include **reads**, not only typed effects. The composed outcome this
function exists to catch is an accumulation of permitted reads followed by one
permitted effect that carries the accumulation somewhere it should not go; a history
of effects alone shows the carrying step with nothing of what filled it, which is the
half that decides whether the step matters. A v0 that passes unconditionally still
has to accumulate the right history, because turning the check on later against an
incomplete history would be turning on a check that cannot see the case.

## Authority

- The gate **may only refuse.** It never grants, never approves, never widens,
  never realizes.
- Nothing inside the system may modify the gate's logic or its invariant list.
  Amendment of the list is direct human action, out of band
  (`06-the-invariant-layer.md`).
- The triage role (Milestone 11), when it exists, may route a tripped gate but
  **may never grant an effect the gate refused**.

## Failure modes

- **Fail open.** An effect that reaches the runtime without the gate having
  actually run, or a gate error treated as `pass`, is the single worst defect in
  the system. On any inability to evaluate — malformed effect, unresolvable
  envelope, unreadable invariant list — the gate MUST return `refuse` and the
  runtime MUST halt the effect.
- **Category collapse.** A refusal recorded as ordinary failure invites
  retry-past-refusal; it is a defect (`02-observability-event-model.md`).
- **Tampered list.** If the invariant list fails its integrity check at load, the
  gate MUST refuse all effects until a human restores it — it MUST NOT fall back
  to an empty or default-permit list.
- **Bypassed call site.** A runtime effect path that does not call the gate is a
  conformance failure even if no forbidden effect happens to flow through it.

## Relationships

- **Provisional invariant list** (`05-provisional-invariant-list.md`) — the
  clause source. The gate is the mechanism; the list is the content.
- **Capability and authority model** (`03-capability-authority-model.md`) — the
  layer above. Separate question, adjustable, role-keyed.
- **Effect vocabulary** (`01-effect-vocabulary.md`) — the input domain. The gate
  does not define effect types.
- **Observability** (`02-observability-event-model.md`) — consumes the gate's
  refusals as kind-3 records and supplies the ordered history the sequence stub
  will eventually read.
- **Runtime** (`20-arch-runtime.md`) — calls the gate on every effect, cannot bypass
  it, and halts any effect the gate refuses or cannot evaluate.

## Open contracts

- **Gate / runtime placement.** Component of the runtime, or a layer above it?
  (`01-invariant-enforcement.md`.)
- **Sequence window and grouping.** The real `check_sequence` logic — what
  counts as a sequence, over what window, grouped how — owned by
  `01-invariant-enforcement.md`, hardened at Milestone 11 (after the
  literature-grounding pass that milestone now carries).
- **Gate-alter.** The design allows the gate to alter an effect, not only refuse
  it. The MVP is refuse-only; alter needs the triage role (Milestone 11).
- **Accumulation-stop.** Converting repeated individually-innocuous trips into a
  mandatory stop — threshold definition and "consecutive / correlated" semantics
  are Milestone 11.
- **List integrity mechanism.** How the invariant list's integrity is verified at
  load (hash pinned where? checked by what?) so a silent edit cannot widen the
  gate.
