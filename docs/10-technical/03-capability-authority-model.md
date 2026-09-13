# Capability and Authority Model

**Traces to:** `00-design/24-arch-permission-layer/01-capabilities-and-authority.md`,
`00-design/25-arch-invariant-layer/01-invariant-enforcement.md`,
`00-design/28-arch-work-record/01-work-record.md`,
`00-design/10-foundations/07-the-integrated-system-and-its-operator.md`,
`00-design/20-arch-runtime.md`,
`00-design/40-roadmap/01-MILESTONES/03-invariant-floor.md` (M3);
binds to `10-technical/01-effect-vocabulary.md`,
`10-technical/04-enforcement-gate.md`,
`10-technical/06-processor-contract.md`.

## TL;DR

This document specifies two checks that are both authority's and are keyed to
different things.

**Capability** is keyed to the **actor**, set by policy, and evaluated per effect:
an actor may *request* an effect only if it holds a grant for that effect type
whose constraints the request satisfies.

**Mandate conformance** is keyed to the **work item**, declared per task, and
evaluated in aggregate: the work actually done must sit inside the boundary the
task was given.

Neither is the floor. Both sit above the invariant gate, which asks whether an
effect is permissible at all.

> **Motto:** Capability enables proposals; authority governs effects; a mandate governs how far they may go together.

## Status of this document

Two halves at different maturities, and the document says which is which rather
than presenting one level of readiness.

**The capability half is v0 and implemented.** It specifies the static-grant form
the MVP needs: grants are authored by the human operator in runtime seed
configuration, fixed per role for the duration of a run, and not proposable by any
cognitive component. The dynamic side — in-system granting, policy that changes as
the system learns — is an open contract deferred to Milestone 12.

**The mandate half is specified and not built.** Nothing in the running system
derives a scope, records one, or checks against one; `11-static-workflow.md`
records that its workflow runs unscoped. What follows fixes the shape so that a
build has something to conform to, and marks every point where the design set
deliberately left the content open.

### What a build of the mandate half needs decided first

The shape below is complete enough to conform to and **not complete enough to
build from**, and the difference is worth stating precisely rather than leaving an
implementer to discover it. Three decisions are structural — each one changes what
software gets written, not merely how it behaves.

1. **The disposition on `outside`** decides where the call site goes. *Halt* puts
   the check on the effect path, synchronously, with a model call in it. *Escalate*
   needs an operator channel and a suspended work item. *Record-and-continue* makes
   it a post-hoc reporter that can run as a separate job against the record. Those
   are three different pieces of software, and the open contract below leaves the
   choice open.
2. **What the comparison consumes** decides whether the checker needs the
   observability store, the workspace, or a prepared summary — and therefore
   whether it is a processor with a live set at all, or a function called with its
   inputs.
3. **The containment check on a transition** is a natural-language judgment that
   `13-work-record.md` makes a precondition of accepting a split or a refinement.
   Read literally, that puts a model call inside the work store's write path, which
   has latency and availability consequences nothing has accepted.

Below those, four smaller gaps that each stop a specific line from being
implementable: no assigner for the reversibility class the pre-effect check keys
on; no definition of which transitions count as *termination*; no consumer for the
`undecidable` verdict; and no checkable form for the self-modifying-scope
exclusion. All four are recorded as open contracts.

What **is** buildable now, and is worth building before any of the above is
settled: the three scope fields and their states on the work item, the recording
and visibility of a derivation, and the fail-closed behaviour on an unscoped item.
Those need no judgment and no model, and the last of them is the single change
that would move the system from *unbounded* to *stopped*.

## Responsibility

Two, and keeping them separate is the point of the document.

- **Capability.** Given an actor and a proposed effect, decide whether that actor
  is **authorized to request** that effect under current policy, and record the
  decision.
- **Mandate conformance.** Given a work item's declared scope and the set of
  changes made under it, decide whether the work stayed **within what was asked
  for**, and record the verdict with its reasoning.

Neither decides whether an effect is permissible in principle — that is the gate,
`04-enforcement-gate.md` — and neither realizes effects, which is the runtime's.

## Why one document holds both

A per-effect check keyed to the actor structurally cannot catch drift past a
mandate, and the reason is worth stating in the specification rather than leaving
to the design set. Every individual step of a drift can sit inside capability
while the aggregate sits outside the mandate. An implementer granted bounded
workspace mutation is permitted to edit each of forty files; nothing in the grant
notices that the task was about two of them.

So mandate conformance cannot be expressed by adding constraints to grants. It
needs a different key (the work item), a different evaluation point (aggregate,
not per effect), and a different comparison (natural language, not a constraint
predicate). It stays in this document because it is **authority's** — the dynamic
half, the runtime interpreting a request under current policy — while capability
is the static description of what a role may ask for.

## Narrowing

`01-capabilities-and-authority.md` leaves capability granularity, policy
representation, and the whole of scope expression open. This document narrows to:

- **Grants keyed to the nine effect types**, not to finer sub-operations. A grant
  is `(effect_type, constraints)`. Discarded for the MVP: per-tool or
  per-syscall capabilities (administrative complexity the milestone explicitly
  warns against), and a single coarse "may cause effects" capability (too weak to
  express reviewer-reads-only vs implementer-writes).
- **Static policy.** The grant set for a role is a fixed map in seed
  configuration. Discarded for the MVP: a policy engine that revises grants
  during a run. Revocation is the one dynamic operation kept, because
  decommissioning requires it.
- **Scope as one opaque natural-language field plus its derivation**, carried on
  the work item. Discarded: a structured scope (a path allowlist, a module list, a
  set of artifact identifiers). The design set is explicit that a boundary is a
  statement about *this* piece of work and cannot be enumerated in advance, and
  that the artifacts where drift is cheapest — specifications, internal APIs,
  documentation — are exactly the ones a path list handles worst.

## Inputs

For a capability decision:

- A **proposed effect**, typed `1..9` per `01-effect-vocabulary.md`, carrying its
  four-property envelope (representable, permitted, attributable, reversible).
- An **actor identity**: the invocation's `role` and its bound capability set
  (from the `processor_invocation` effect that instantiated it — effect type 6).
- **Current policy**: for the MVP, the static role→grants map plus any revocations
  applied this run.

For a mandate-conformance decision:

- The work item's **declared scope** and the record of what it was derived from,
  read from the work record (`00-design/28-arch-work-record/01-work-record.md`).
- The **accumulated change set** attributable to that work item — the realized
  effects in its intent lineage, from observability
  (`02-observability-event-model.md`). Attribution needs no new mechanism: every
  effect inherits its work item through the instance that proposed it, which the
  runtime already tracks.
- For the pre-effect half, **one proposed irreversible effect** rather than an
  accumulation.

## Outputs

- A **capability decision**: `permit_request` or `reject_by_capability`, with a
  machine-readable `reason` (which grant was missing, or which constraint the
  request violated).
- A `reject_by_capability` is recorded by observability as a **kind-4
  proposed-effect disposition** (`02-observability-event-model.md`), never as a
  safety intervention — a capability rejection is ordinary policy, not a gate
  trip.
- A **conformance verdict**: `within`, `outside`, or `undecidable`, each carrying
  natural-language reasoning. The verdict MUST be recorded whatever it says.
  `within` is not a null result — its absence and its presence must be
  distinguishable, since a check that did not run and a check that passed look
  identical in a record that only writes failures.

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

### Where a spawned instance's set comes from — an unresolved collision

Two rules in this set contradict each other, and an implementation cannot satisfy
both.

**This document** says a grant set is keyed to the **role** and read from seed
configuration. **`08-orchestrator-contract.md`** says the orchestrator "cannot
grant what it does not hold" and that a spawned processor's capability set is
bounded by the orchestrator's own.

The illustrative sets above break the second rule immediately: the orchestrator
holds types 6 and 4, the implementer it spawns holds 1 and 2, and an orchestrator
that could only pass down a subset of its own grants could never spawn an
implementer at all — which is the entire arrangement.

The reading that makes the configuration coherent, stated so that a decision has
something to accept or reject rather than as a settled position: **delegation is
bounded by the `roles` constraint on the type-6 grant, not by a subset relation
over effect types.** An orchestrator may instantiate the roles its own grant
names, and each instance then holds what seed configuration gives that role. What
`08`'s rule is reaching for is separately stated there and is the part that
survives either way — an orchestrator MUST NOT use a processor to accomplish what
it is itself **forbidden** to do, which is a statement about forbidden effects
rather than about unheld grants.

Until this is decided, an implementation MUST record which reading it took, because
the two produce different capability sets for the same configuration.

### The rule the prohibition was reaching for, and what it can actually check

`08-orchestrator-contract.md` also forbids the orchestrator to "use a processor to
accomplish what it is itself forbidden to do". That statement collapses three
different senses of *forbidden*, and separating them leaves less than it appears
to.

**Gate-forbidden.** Its own example — instructing an implementer to edit the
invariant list — is refused at the implementer's own gate check, since H5 binds the
effect and not the proposer. The rule adds nothing here, and its illustration is
its weakest case.

**Capability-forbidden.** Delegating what one cannot do oneself is what an
orchestrator is *for*, which is the collision above. The distinction the rule never
drew: **"cannot propose" is not "must not happen under my mandate."** An empty
type-1 grant is a statement about an actor's hands, not about its remit.

**Scope-forbidden.** Already normative, and already checkable: a child's scope is
contained in its parent's, and the accumulated change set under a lineage is
audited against the declaration.

What is left once those three are removed is **purpose** — laundering an intention
through a delegate — and purpose is not observable from an effect stream. A rule
keyed to why an invocation was issued is an inference about intent, which
`10-foundations/07` forbids on exactly the grounds that make it unusable here: it
cannot be shown wrong. So the prohibition is not implementable as stated, and
nothing checkable is lost by replacing it with the containment and aggregate checks
that already exist.

**One real laundering route survives, and it is not about purpose.** A ceiling
expressed as a per-actor grant constraint is not the same as a system-wide
invariant, even when both carry the same number. `max_concurrent: 1` on an
orchestrator's type-6 grant bounds that actor; a child also holding type 6 can
spawn under its own separate allowance, and total concurrency exceeds one while
every actor individually conforms. What catches this is R2 in the invariant list,
which is keyed to the system rather than to a grant — so the capability constraint
is a **redundant shadow** of the real ceiling. An implementation that builds the
constraint and not the clause has the hole and will pass its own tests.

## Reads

A read is not a typed effect and is still something an actor may or may not be
allowed to perform (`01-effect-vocabulary.md`, Reads specifically). What
ordinarily happens to one is a policy question, which makes it this document's.

- The **default is permissive**: a read passes unless a rule names it.
- That default MUST be expressible as a **rule in policy**, not as a property of
  the vocabulary or a branch in the gate. The distinction is operational rather
  than stylistic: as a rule, holding a policy about some class of reads is a
  configuration change; as a vocabulary exclusion it would be a design-set change.
- A policy that names a class of reads binds them the same way a grant binds an
  effect type: the read is refused if the rule matches, permitted otherwise.

At what granularity a rule may name a class of reads — by path, by crossing type,
by volume against a ceiling — is open, and the permissive default is what makes it
possible to leave open. Nothing has to choose a granularity until there is a rule
that needs one.

## Mandate conformance

### What a scope is

**Natural-language text carried on the work item**, not a structured field. The
work record holds it and does not interpret it
(`00-design/28-arch-work-record/01-work-record.md`).

A work item MUST carry, as distinct parts:

- the **boundary** itself;
- **what it was derived from** — the reasoning that produced it;
- its **state**: `derived`, `stated` (the operator gave one), or `pending` (the
  reading was ambiguous and the question went to the operator).

The three states are not decoration. `pending` and *absent* MUST be
distinguishable: the first is the check working as designed, the second is the
check not having run, and they call for opposite responses.

### Deriving one

Most scopes are implicit. An operator rarely writes a boundary down, and most of
one follows from what the task is and how the system is arranged — a request to
add an output format to a CLI reaches the interface specification and its
functional tests, and not the web API documentation, without anyone saying so.

- Where the operator **states** a boundary, that statement governs, and the
  derivation fills only what was left unsaid.
- A derived scope MUST be recorded **with its derivation**, and MUST be visible to
  the operator. This is not hygiene. A derivation nobody sees cannot be contested,
  and an uncontested wrong derivation is ratified rather than caught — the
  end-of-task check then compares the work against a boundary that was already too
  wide, which turns drift into something legitimate one step earlier than the
  check was built to notice.
- Under **genuine ambiguity the system MUST NOT derive**. It sets the scope
  `pending` and asks, and the asking has a required form: it names the candidate
  readings rather than posing an open question or handing over a confident
  boundary for validation (`00-design/10-foundations/07`, the two modes). A short
  list of readings asks the operator the one thing only they can settle.

What counts as enough doubt to stop is **not set**, and the pressure runs one way:
asking costs a round trip and proceeding looks like progress, so a check left to
its own judgment will under-detect ambiguity. Recorded as an open contract below
rather than given a number here.

This derivation does not violate `10-foundations/07`'s requirement that scope
become "checkable properties of artifacts and effects, never an inference about
intent". What that forbids is inference about **a person** — "what the operator
would have wanted" is a psychological prediction, unbounded and unfalsifiable.
Inferring that a CLI output format reaches the CLI surface is an inference about
**the work and the structure of the system**: checkable by anyone who knows the
codebase, and demonstrably wrong when it is wrong.

### Containment

One rule, three places it applies. **A mandate descends and never widens on the
way down.**

- A **split**'s children inherit the parent's scope and MAY narrow it. A proposed
  child whose boundary is not contained in its parent's is not a split; it is a new
  root task, and a new root needs intent, which only arrives from outside
  (`01-effect-vocabulary.md` type 4 excludes an intent record's original content
  from system amendment).
- A **refinement** changes a work item's formulation and not its intent, so a
  re-derived scope may move underneath the intent's scope and MUST NOT push past
  it.
- A **nested invocation** — a processor invoking another — passes down a scope
  contained in its own and MAY narrow it.

Implementations MUST check containment on all three, not only on splits. The split
route is the obvious one, and refinement reaches the same place without anything
ever splitting.

Deciding whether a proposed child's boundary sits inside its parent's is itself a
natural-language judgment. This rule does not reduce the amount of judgment
required; it puts all of it in one check instead of leaving a path around it.

### Who may write a scope

| Party | May | Why |
|---|---|---|
| The operator | Anything, without bound | Scope descends from intent, and intent is amended out of band |
| An **invariant processor**, deriving from intent | Write the ceiling | Assigning this to the orchestrator is circular — the actor bounded by the intent's scope would be the one writing it |
| The orchestrator | Narrow only | It formulates work items under a ceiling set above it. Narrowing is safe unprotected: it makes the check stricter, and declining to narrow leaves the inherited boundary standing |
| Anything working *under* a task | Nothing | Including the scope check, which is **read-only** on the scope: it compares and reports, never rewrites |

The general form, because it generalizes past scope: **a scope may be derived for
work one is not doing, and may not be widened for work one is doing.** The
constrained party and the constraining party cannot be the same one.

Scope is nonetheless held on the work item like any other field, and needs no
special protection there. Widening it is a work-record mutation, which is an
effect, which the check sees — modifying the scope is inside the current scope or
it is not. What that costs is a **default rather than a mechanism**: a scope
permitting its own modification MUST be excluded unless explicitly granted.

### An instance's scope is static

Instantiation binds a scope alongside role, objective, live set and capability set
(`06-processor-contract.md`). For the instance's life:

- A running instance **MUST NOT** widen its own scope.
- A change to the work item's scope — re-derivation after a refinement or split,
  or an operator amendment — **MUST NOT** reach instances already running. It
  applies from the next invocation.
- An instance that finds it must reach further **MUST stop and report** — a
  recorded conclusion, or a proposed transition on the work item — and something
  else decides.

The reason is not defence against a concurrent attacker. It is that the instance
reporting a boundary problem must not be the one that benefits from the answer. If
a running instance's scope updated live, the report would cost nothing and change
nothing: the instance would simply continue under the new boundary, which is the
locally-justified-step drift `10-foundations/07` names, reached by an honest route
instead of a dishonest one. Static scope is what gives "requires a new mandate"
operational force — a new mandate means a new invocation.

The same uniform rule covers an operator amending a mandate mid-run. Waiting for
re-instantiation is not obviously required there and is adopted anyway, because
distinguishing an operator amendment from a system widening *at the moment of
application* would put a judgment inside the path rather than at its edges. It is
affordable because processors are ephemeral and re-instantiation is cheap.

### Where the check runs

The check divides on reversibility, and the two halves sit at opposite ends of a
task.

**Reversible changes are audited at the end**, once, as an accumulated set against
the declaration. This is the only point at which drift is visible *as* drift
rather than as a series of individually unremarkable steps, and auditing late is
affordable precisely because the finding still has a remedy: what fell outside can
be undone.

**Irreversible changes are questioned before they happen**, one at a time. There
is no end-of-task remedy, so the check must precede the effect. That placement
coincides with the risk evaluation `10-foundations/02` requires before an
irreversible effect is proposed — two requirements derived independently landing
on the same point in the loop.

So, normatively:

- An implementation MUST run the aggregate check once per work item at
  termination, and MUST run the per-effect check before realizing any effect
  classed irreversible.
- It MUST NOT run the aggregate check per effect. That is the difference between
  one judgment per task and one per effect, which is the difference between a
  check worth running and one nobody will.
- The check **fails closed on an unscoped item**. Work stops. Nothing separate has
  to watch for scopes going missing, which removes a mechanism rather than adding
  one.

### How the checker is invoked

**The runtime hardcodes the call.** Every tool call passes through the runtime,
which holds the specification's required call sites and makes the invariant-layer
calls at each of them. The scope check is therefore **triggered by the runtime**,
not requested by any cognitive component, and there is no path by which the
triggering instance can decline to trigger it.

This settles two things that looked open.

**The checker is not spawned by the loop.** It is not a type-6 invocation the
orchestrator issues, which would put the constrained party in charge of summoning
its own constrainer. The trigger sits with the runtime for the same reason the gate
call does.

**It still has a live set and a turn input like anything else.** Being triggered by
the runtime settles *who calls*, not *what the checker sees*. It reaches
`14-context-manager.md` for its material, and it is a processor reasoning over
natural language, not a function handed a payload.

What follows from that is a requirement on how its material is assembled. The
checker is a **judge**, so it binds `share_nothing`: it inherits no prefix carrying
the reasoning it is meant to assess (`14-context-manager.md`, The isolation
preference). This is not a preference the policy may trade away under capacity
pressure. A check assembled on the prefix of the work it is checking passes for the
wrong reason, which is worse than not running, because it looks like a passing
check. Where `share_nothing` cannot be provided, the check **has not run**, and the
fail-closed rule below applies.

### The checker is an invariant processor

The comparison is a judgment over natural language and no deterministic check
performs it, so the checker is a processor. It is an **invariant processor**
(`04-enforcement-gate.md`, Invariant processors), not one drawn from the open role
vocabulary: a loop able to remove or retune it would be inside the scope it
constrains.

It qualifies for that layer on the **direction** condition, and the reasoning is
specific to scope rather than a general licence for reasoning components. **A scope
only ever narrows within capability and never reaches past it.** An effect still
passes capability and still passes the gate whatever the scope says. So a scope
check that is lax, degraded, or talked into generosity yields *no narrowing* —
which is where this project stands today, running unscoped — rather than new
permission. Its failure mode is uselessness, not permission.

The separation that keeps this coherent: **the mandate is adjustable, the checker
is not.** What a task's scope permits changes with every task and is set by
whoever asked for the work, which is why mandate content is not invariant-layer
material. That a functioning scope check exists and cannot be removed or routed
around is not adjustable by anything inside the system, which is why the checker
is.

## Authority

- The capability model **may refuse a request**. It may never realize an effect,
  never widen a grant, and never substitute for the gate.
- The scope check **may only restrict.** It may report `outside`, and it may not
  permit anything the other checks refused. It is read-only on the scope itself.
- **Grant** and **revoke** are the same primitive in opposite directions (effect
  type 9). For the MVP:
  - Grants are established only from seed configuration authored by the human
    operator. No in-system actor may grant a capability to another — a type-9
    effect proposed by a cognitive component is refused by the gate
    (`04-enforcement-gate.md`; provisional invariant list clause on
    cognition-initiated capability change).
  - **Revocation MUST be realizable immediately and unilaterally by the
    runtime** — no proposal, no evaluation step, no wait for human review
    (`01-invariant-enforcement.md`, decommissioning). After revocation the
    actor's set is empty and every subsequent request from it fails closed.
  - **Revocation targets a running instance, not a role.** Decommissioning is a
    response to what one actor did, and emptying a role's seed entry would silently
    disarm every future instance of it — a configuration change wearing an
    intervention's clothes. An implementation MUST be able to revoke one
    `invocation_id` without touching the seed map.

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
- **A system ceiling implemented only as a grant constraint.** A per-actor
  constraint bounds one actor; a system ceiling bounds the system. Where both carry
  the same number — `max_concurrent: 1` against R2 — implementing only the
  constraint leaves a route open through delegation, since each actor conforms
  separately while the total does not. The constraint is a convenience; the
  invariant clause is the enforcement.
- **Unscoped work proceeding.** A work item reaching execution with no scope in
  any of the three states is a defect. The check fails closed; a path that runs
  anyway has removed the only thing standing between the system and unbounded
  work.
- **`pending` read as `derived`.** Collapsing "we asked and are waiting" into "we
  decided" converts a correctly-detected ambiguity into a silently chosen reading.
  The states MUST stay distinct in the record and in the check's input.
- **An unrecorded derivation.** A scope with no recorded reasoning is
  uncontestable, and an uncontestable derivation is ratified rather than checked.
  Recording it is normative above for this reason.
- **A conformance verdict recorded only on failure.** Then a check that never ran
  and a check that passed are the same absence, and the system cannot tell an
  unscoped run from a clean one afterwards.
- **Scope drift through refinement.** An implementation that checks containment on
  splits and not on refinements has left the route open that splitting alone did
  not close.

## Relationships

- **Effect vocabulary** (`01-effect-vocabulary.md`) — supplies the effect-type
  domain this model expresses permissions over. It owns the actor-and-policy
  dimension the vocabulary deliberately omits, including the read default.
- **Enforcement gate** (`04-enforcement-gate.md`) — sits *below* the capability
  model and asks the non-adjustable question. An effect must pass capability
  **and** gate; order is representability (runtime) → capability → gate. That
  document also holds the invariant-processor category the scope check belongs to.
- **Work record** (`13-work-record.md`, owed; `00-design/28-arch-work-record/`) —
  holds the declared scope, its derivation, its state, and the transitions that
  change it. This document owns the check; that one owns the declaration.
- **Processor contract** (`06-processor-contract.md`) — binds a scope at
  instantiation and forbids an instance widening its own.
- **Observability** (`02-observability-event-model.md`) — records every
  capability decision as a kind-4 disposition, and must carry conformance verdicts
  and scope transitions for the aggregate check to have an input.
- **Runtime** (`20-arch-runtime.md`) — holds the seed grant map, applies revocations,
  and calls this model; it does not let a cognitive component reach the map.

## Open contracts

- **What happens when conformance fails.** `10-foundations/07` says the
  requirement "cannot be enforced by deterministic refusal alone", which rules out
  treating it like the gate, and leaves what it *is* treated like unanswered. The
  direction condition narrows the space usefully: an invariant processor may only
  restrict, so the available dispositions are halt, escalate to the operator, or
  record-and-continue. Which one, and whether it differs between the aggregate and
  pre-effect halves, is not decided — and it decides the call site, per What a
  build needs decided first.
- **How a scope is expressed and compared.** Free text is what the design set
  fixes; what the comparison actually consumes — the raw change set, a summary of
  it, a diff — is not. This is the single largest unknown in the mandate half.
- **What invokes the containment check, and where it sits.** `13-work-record.md`
  makes a passing containment check a precondition of accepting a split or a
  refinement, and the check is a natural-language judgment. So either a model call
  sits inside the work store's write path, or containment is checked before the
  transition is proposed and the store trusts a verdict it is handed, or transitions
  are accepted provisionally and reconciled. None of the three is argued.
- **Who assigns a reversibility class, and when.** The pre-effect check is
  normatively required "before realizing any effect classed irreversible", and
  nothing assigns that class — `01-effect-vocabulary.md` holds the question open,
  and `10-foundations/02` argues the proposing side without naming a carrier. As
  written, half this check has a predicate that does not exist.
- **What counts as termination.** The aggregate check runs "once per work item at
  termination". `13-work-record.md` names seven transitions and does not say which
  are terminal. Whether the check runs on *abandoned* and *deferred*, and whether a
  work item refined after execution is re-checked, is undefined.
- **What `undecidable` means operationally.** It is a permitted verdict with no
  stated consequence. Whether it is treated as `outside`, as a request to escalate,
  or as a distinct state the work item can sit in, is not decided.
- **How the self-modifying-scope exclusion is checked.** "A scope permitting its
  own modification MUST be excluded unless explicitly granted" reads like a
  mechanical default and is not one: whether a natural-language boundary permits
  modifying itself is the same judgment the rest of the check makes. Either it is
  a flag alongside the boundary, or it is another question put to the checker.
- **What isolating the checker costs.** How it is invoked is settled, and that it
  binds `share_nothing` is settled. What is not known is the price: a dedicated
  sequence takes a permanent share of the resident envelope whether or not it is
  busy, and nobody has measured how the envelope divides on the reference host.
  That figure decides how many judging processors the arrangement can afford at
  once (`14-context-manager.md`).
- **The doubt threshold for asking.** What counts as enough ambiguity to set a
  scope `pending` rather than deriving. Unset, with a known bias toward
  under-detection.
- **The orchestrator's own scope.** It reads work state across items rather than
  operating under one. The natural reading is that it holds the **intent's** scope
  with work items inheriting narrowed versions, which is consistent with mandate
  descending from intent but is not argued anywhere.
- **Whether derivation and checking are one role or two.** Both are invariant
  processors; nothing establishes that they are the same one.
- **Grant authority once loops exist.** Who may issue a type-9 grant when
  system-level feedback (Milestone 12) can commission roles? For the MVP the
  answer is "only the human, out of band"; that will not hold later.
- **Constraint language.** The illustrative constraint keys need a real,
  checkable grammar (path globs, command matching semantics, destination
  classes). Deferred until real effects show which constraints they need.
- **Policy dynamism.** When does policy stop being a static map? What triggers a
  grant change mid-run, if ever, and how is that itself gated?
- **Granularity review.** Effect-type granularity is the MVP choice; evidence may
  show a type (likely 2, process execution, or 4, work-record mutation) needs to be
  split for authority purposes even though the vocabulary keeps it whole.
- **Read granularity.** At what granularity a rule may name a class of reads — by
  path, by crossing type, by volume against a ceiling. Open on the foundational
  side too (`10-foundations/02`).
- **Destination classes for type 3.** Whether network access grants distinguish
  registry / known-service / arbitrary host at the capability level or leave all
  host policy to the gate's allowlist.
