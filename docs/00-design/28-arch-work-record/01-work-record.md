# Work Record

## TL;DR

The work record holds intent and the work derived from it durably — what was asked, how it is currently formulated, and every transition between the two — so that ephemeral processors can cooperate on the same work across sessions.

> **Motto:** The goal outlives every formulation of it.

## Status of this document

Draft. Work-record mutation (`10-technical/01-effect-vocabulary.md` type 4) has a schema, a capability policy and exercised runs behind it, and this actor is what owns the record it mutates. States the responsibility, the service, and a general shape — deliberately not a schema or a storage format, which belong to technical specification.


## Motivation

`22-arch-cognition/01-work-intent-and-task-model.md` defines intent, work items, and work units — what each one is, and that a work item is deliberately revisable rather than fixed. It does not say where any of it lives between invocations.

Meanwhile `10-technical/01-effect-vocabulary.md` makes work-record mutation a typed, gated effect, `10-foundations/02` names "creating a work item" as a proposal that crosses the same way any effect does, and the M3 runs routed real work-record mutations through the gate. Something was already persisting this in practice with no architectural owner.

`21-arch-knowledge-model` is not that owner. It holds `10-foundations/03`'s claims, and a work item is not a claim — it is what claims attach to.

## The actor and its responsibility

- **Hold intent durably.** Its original human-authored content is not amendable from inside the system — `10-technical/01` type 4 excludes it by name, amendable only out of band. This actor therefore protects intent rather than managing it: written once from outside, read thereafter.
- **Hold work items and their current state.** One current formulation per item, directly readable without reconstructing anything.
- **Hold a work item's declared scope.** `10-foundations/07` requires that work stay within the mandate it was given, and `24-arch-permission-layer` establishes that capability gating structurally cannot check it — a capability is keyed to the actor and evaluated per effect, while a mandate is keyed to the work item and evaluated in aggregate against what was touched. A declared scope is part of what a work item *says*, which puts the declaration here while the check stays with `24`.

  It is **natural-language text, not a structured field**, and this actor holds it without interpreting it — consistent with everything else here, since this actor does not judge whether a work item is well-formed either.

  It is usually **derived rather than stated**: an operator seldom writes a boundary down, and most of one follows from what the task is and how the system is arranged. Deriving the ceiling from intent is an invariant processor's (`25-arch-invariant-layer`); narrowing it for a child is the orchestrator's, done when it formulates the item. This actor records what either produced without deriving anything itself. That makes what this actor holds two things rather than one — the boundary, and what it was derived from — because a derivation nobody can inspect cannot be contested, and an uncontested wrong derivation is ratified rather than caught (`24-arch-permission-layer`, The shape it takes).

  A scope can also be **pending** rather than derived, when the reading was ambiguous enough that the question went to the operator instead (`24-arch-permission-layer`). That is a state a work item can sit in, not an absence of one, and it needs to be distinguishable from a scope nobody got around to deriving — the first is the check working, the second is it not having run. The distinction has teeth, because the second state stops work: the scope check fails closed on an unscoped item.

  Note that a scope held here is mutable like the rest of a work item, and that is not a hole. Widening it is a work-record mutation, which is an effect, which the scope check sees — so a mandate can only widen within what the current mandate already permits, and a scope permitting its own modification is excluded by default (`24-arch-permission-layer`, Four things this does not need). This actor needs no special protection for the field, which is why it holds it like any other.

  Three consequences for what this actor must support. The declaration has to be readable at any point during the task rather than only at its end, since an irreversible change is questioned before it happens. It has to sit in the transition history like anything else — both because a mandate widened mid-task is what an audit needs to see rather than find silently already true, and because a work item that is refined, split or merged has its scope legitimately re-derived, and those two look identical unless the history distinguishes them. And an operator's own indication of a boundary, where one is given, is carried as part of it and governs the derived portion.
- **Record every transition** a work item goes through: refined, challenged, split, merged, deferred, abandoned, executed. The current state and the history of how it was reached are both held, and neither is derived from the other.

  Transitions are not all equally free, and two constraints belong to this actor because they are about the shape of the lineage rather than about any judgment.

  **A split's children inherit the parent's scope and may narrow it, never widen it.** A proposed child whose boundary is not contained in its parent's is not a split; it is a new root, and a new root needs intent, which only arrives from outside (`10-technical/01-effect-vocabulary.md` type 4 excludes an intent record's original content from system amendment). Without that, splitting would be a way to manufacture mandate — widen the boundary in the child, act under the child.

  **A refinement stays under its item's intent.** Scope derives from a work item's formulation, so refining the formulation broadly and re-deriving would widen the scope without anything ever splitting. What bounds it is that a refinement changes the formulation and not the intent: the re-derived scope may move around underneath the intent's scope and may not push past it. The two constraints together are one rule seen from two sides — mandate descends and never widens on the way, whether the step down is a split, a refinement, or a nested invocation (`24-arch-permission-layer`, Who may modify a task's scope).
- **Hold the attachment edges** between a work item and the claims attached to it — a finding, a proposal, a decision. The claim's content lives in `21-arch-knowledge-model`; this actor holds a reference plus its own metadata, the same way `23-arch-context-management` does for a retrieved claim. Two actors point into one claim store; neither copies it.
- **Hold a processor's recorded conclusion** — answered, blocked, or declined, with its reasoning. `10-technical/01` classes this as a work-record mutation rather than a memory write, a boundary the M4 runs found carved cleanly once chosen but not self-evident beforehand. Keeping *declined* distinct from *blocked* is load-bearing rather than cosmetic: Milestone 5 recorded an orchestrator collapsing "the task rests on a false premise" and "I cannot find a next step" into one generic outcome, losing a distinction the simpler Milestone 4 arms had made.

Whether three verdicts suffice is open, and the doubt has the same shape as the failure they were introduced to prevent. `22-arch-cognition/01-work-intent-and-task-model.md` names two distinct reasons to refuse execution — the task rests on a false premise, and the request has already been satisfied — and both currently land on *declined* while calling for entirely different follow-ups. That may be this vocabulary reproducing Milestone 5's collapse one level down. Resolving it belongs with the processor contract rather than here; what this actor owes is only that whatever verdicts exist stay distinguishable in the record. Whether an instance judges objective validity at all is that instance's strategy (`10-foundations/04`, The objective itself is not a given); being able to record the verdict once it does is not.

What this actor does not do is decide anything about the work. Whether a work item should be split is the orchestrator's call, and the harder question of where that decision ought to live is `22-arch-cognition/08`'s open question, not this actor's; it records a split once something else has decided and realized one. It likewise does not judge whether a work item is well-formed or whether a recorded conclusion is correct.

## Service provided to the rest of the system

- **Intent lineage.** Given any work item, the chain back to the intent it descends from. `10-technical/01` already requires realized effects to be reconstructable "per intent lineage" and nothing in this band supplied that chain; this actor is what knows it.
- **Current state of work.** What items exist, how each is currently formulated, what state it is in, and its parent and child links.
- **Transition history**, for one item or for a whole lineage.
- **Attached-claim references** for a work item, resolvable against `21-arch-knowledge-model`.

## General shape and a naive default

The same restraint `21-arch-knowledge-model` and `23-arch-context-management` commit to: the filesystem, no database, no index, until evidence says the naive version is the actual bottleneck. And the same reading of that restraint — it sequences the work rather than doubting that a real store will eventually be needed, so this actor's service surface is the part that has to survive the change, and a caller must never learn that a work item is a file.

One structured record per work item, holding its current formulation and state as directly readable fields, with an append-only transition log kept alongside it rather than inside it.

That shape is the reason this is a separate actor rather than a region of `21-arch-knowledge-model`. A claim there is append-only and superseded rather than edited, so its current truth sits at the end of a chain. A work item's current state has to be readable without walking anything, because the orchestrator interprets current work on every loop step (`22-arch-cognition/03`, Responsibility). Holding both a mutable current view and an immutable record of how it changed is a different write discipline from `21`'s, and collapsing the two would force one of them to give.

Intent is a third kind of record again, and the simplest: written from outside the system and never rewritten by it, so it needs no transition log at all.

## Interactions

- **`22-arch-cognition/01-work-intent-and-task-model.md`** owns the vocabulary this actor persists — intent, work item, work unit — and this actor adds no concepts to it.
- **`22-arch-cognition/03-orchestrator.md`** reads current work state on every loop step and proposes the transitions that change it, including its own per-step decision record.
- **`20-arch-runtime.md`** gates and realizes a work-record mutation; this actor persists what the runtime realized, not what was merely proposed.
- **`21-arch-knowledge-model`** holds the claims this actor's attachment edges point at. Separate stores, one direction of reference.
- **`23-arch-context-management`** registers a work item reaching a processor as an artifact, a crossing like any other. This actor is queried; it never pushes into a context.
- **`26-arch-observability`** keeps its own copy of work-record events, for the same retention and compression reasons it does not read `21` or `23` directly.
- **`25-arch-invariant-layer`** needs a decommission to be distinguishable from ordinary task failure. The half of that which is a processor's recorded conclusion lands here; the event-history half is `26`'s.

## Relationships

- **`22-arch-cognition/01-work-intent-and-task-model.md`** — owns the model this actor realizes.
- **`21-arch-knowledge-model`** — a separate store this actor references and never copies.
- **`26-arch-observability`** — a separate store that keeps its own copy of what happens here.
- **`20-arch-runtime.md`** — realizes the effects this actor persists.

## Open question

Whether work units need first-class persistent representation at all, or remain an emergent orchestration concept. `22-arch-cognition/01` left this open and nothing here closes it; the answer decides whether this actor holds two kinds of record or three.

Whether split and merge are one primitive exercised in two directions or two genuinely different transitions. This matters for what the parent and child links have to be able to express.

Whether an abandoned work item is retained or removed. Retention is the cheaper assumption and keeps "why was this dropped" answerable, but nothing here establishes that it is required.
