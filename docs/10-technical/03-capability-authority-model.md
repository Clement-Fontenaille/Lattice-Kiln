# Capability and Authority Model

**Traces to:** `00-design/20-cognitive-architecture/04-capabilities-and-authority.md`,
`00-design/20-cognitive-architecture/07-invariant-enforcement.md`,
`00-design/20-cognitive-architecture/05-runtime.md`,
`00-design/40-roadmap/01-MILESTONES/03-invariant-floor.md` (M3);
binds to `10-technical/01-effect-vocabulary.md`.

## TL;DR

An actor may **request** an effect only if it holds a capability grant for that
effect type whose constraints the request satisfies. This is the adjustable,
role-keyed layer. It sits *above* the invariant gate and answers a different
question — *is this actor allowed to ask?* — not *is this effect permissible at
all?* An effect must pass both.

> **Motto:** Capability enables proposals; authority governs effects; neither is the floor.

## Status of this document

v0 for the MVP slice. It specifies the static-grant form the MVP needs: grants
are authored by the human operator in runtime seed configuration, fixed per role
for the duration of a run, and not proposable by any cognitive component. The
dynamic side — in-system granting, policy that changes as the system learns —
is named as an open contract and deferred until there is a feedback loop that
would exercise it (Milestone 12).

## Responsibility

Given an actor and a proposed effect, decide whether that actor is **authorized
to request** that effect under current policy, and record the decision. It does
not decide whether the effect is permissible in principle (that is the gate,
`10-technical/04-enforcement-gate.md`), and it does not realize effects (that is
the runtime).

## Narrowing

`04-capabilities-and-authority.md` leaves capability granularity and the
representation of policy open. This document narrows the MVP form to:

- **Grants keyed to the nine effect types**, not to finer sub-operations. A grant
  is `(effect_type, constraints)`. Discarded for the MVP: per-tool or
  per-syscall capabilities (administrative complexity the milestone explicitly
  warns against), and a single coarse "may cause effects" capability (too weak to
  express reviewer-reads-only vs implementer-writes).
- **Static policy.** The grant set for a role is a fixed map in seed
  configuration. Discarded for the MVP: a policy engine that revises grants
  during a run. Revocation is the one dynamic operation kept, because
  decommissioning requires it.

## Inputs

- A **proposed effect**, typed `1..9` per `01-effect-vocabulary.md`, carrying its
  four-property envelope (representable, permitted, attributable, reversible).
- An **actor identity**: the invocation's `role` and its bound capability set
  (from the `processor_invocation` effect that instantiated it — effect type 6).
- **Current policy**: for the MVP, the static role→grants map plus any revocations
  applied this run.

## Outputs

- A **capability decision**: `permit_request` or `reject_by_capability`, with a
  machine-readable `reason` (which grant was missing, or which constraint the
  request violated).
- A `reject_by_capability` is recorded by observability as a **kind-4
  proposed-effect disposition** (`02-observability-event-model.md`), never as a
  safety intervention — a capability rejection is ordinary policy, not a gate
  trip.

## The capability set

Illustrative shape (`10-technical` conventions — intent, not a fixed format):

```
CapabilitySet := { effect_type -> Constraints }

# examples
implementer := {
  1 (workspace_mutation):  { path_within: "<assigned_workspace_root>" },
  2 (process_execution):   { command_allowlist: ["build", "test", "lint", "fmt"] },
  4 (work_record_mutation): { }        # unconstrained within the run's work items
}
reviewer := {
  # reads only — no effect grants at all
}
orchestrator := {
  6 (processor_invocation): { max_concurrent: 1, roles: ["implementer", "reviewer"] },
  4 (work_record_mutation): { }
}
```

Rules:

- An effect type absent from the set means **the actor may not request that
  type** — the model fails closed. An actor with an empty set may request
  nothing.
- Constraints are conjunctive: every constraint on the grant must hold for the
  request to be permitted.
- The constraint vocabulary (`path_within`, `command_allowlist`,
  `destination_class`, `max_concurrent`, …) is illustrative for the MVP and is an
  open contract.

## Authority

- The capability model **may refuse a request**. It may never realize an effect,
  never widen a grant, and never substitute for the gate.
- **Grant** and **revoke** are the same primitive in opposite directions (effect
  type 9). For the MVP:
  - Grants are established only from seed configuration authored by the human
    operator. No in-system actor may grant a capability to another — a type-9
    effect proposed by a cognitive component is refused by the gate
    (`04-enforcement-gate.md`; provisional invariant list clause on
    cognition-initiated capability change).
  - **Revocation MUST be realizable immediately and unilaterally by the
    runtime** — no proposal, no evaluation step, no wait for human review
    (`07-invariant-enforcement.md`, decommissioning). After revocation the
    actor's set is empty and every subsequent request from it fails closed.

## Failure modes

- **Unknown effect type.** A request typed outside `1..9` is malformed; reject
  and report — it is not a capability question.
- **Missing capability set.** An actor with no resolvable grant set is treated as
  holding the empty set (fail closed), and the condition is reported — a run
  where an actor's authority cannot be established is not trustworthy.
- **Ambiguous or unresolvable constraint.** A constraint that cannot be
  evaluated (e.g. `path_within` with no assigned workspace root) fails closed and
  is reported, never assumed satisfied.
- **Silent widening.** A code path that permits a request without a matching
  grant is a defect, even if the gate would have caught the effect anyway —
  passing the gate is not evidence of passing capability.

## Relationships

- **Effect vocabulary** (`01-effect-vocabulary.md`) — supplies the effect-type
  domain this model expresses permissions over. It owns the actor-and-policy
  dimension the vocabulary deliberately omits.
- **Enforcement gate** (`04-enforcement-gate.md`) — sits *below* this model and
  asks the non-adjustable question. An effect must pass capability **and** gate;
  order is representability (runtime) → capability → gate.
- **Observability** (`02-observability-event-model.md`) — records every
  capability decision as a kind-4 disposition.
- **Runtime** (`05-runtime.md`) — holds the seed grant map, applies revocations,
  and calls this model; it does not let a cognitive component reach the map.

## Open contracts

- **Grant authority once loops exist.** Who may issue a type-9 grant when
  system-level feedback (Milestone 12) can commission roles? For the MVP the
  answer is "only the human, out of band"; that will not hold later.
- **Constraint language.** The illustrative constraint keys need a real,
  checkable grammar (path globs, command matching semantics, destination
  classes). Deferred until M4 shows which constraints real effects need.
- **Policy dynamism.** When does policy stop being a static map? What triggers a
  grant change mid-run, if ever, and how is that itself gated?
- **Granularity review.** `04-capabilities-and-authority.md`'s open question —
  effect-type granularity is the MVP choice; M4 evidence may show a type (likely
  2, process execution, or 4, work-record mutation) needs to be split for
  authority purposes even though the vocabulary keeps it whole.
- **Destination classes for type 3.** Whether network access grants distinguish
  registry / known-service / arbitrary host at the capability level or leave all
  host policy to the gate's allowlist.
