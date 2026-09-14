# Work Record

## TL;DR

The work record holds intent and the work derived from it durably — what was asked, how each work item was formulated, and how the work moved from one to the other — so that ephemeral processors can cooperate on the same work across sessions.

> **Motto:** The goal outlives every formulation of it.

## Status of this document

Draft. Work-record mutation (`10-technical/01-effect-vocabulary.md` type 4) has a schema, a capability policy and exercised runs behind it, and this actor is what owns the record it mutates. States the responsibility, the service, and a general shape — deliberately not a schema or a storage format, which belong to technical specification.


## Motivation

`22-arch-cognition/01-work-intent-and-task-model.md` defines intent, work items, and work units — what each one is, and that a work item is never rewritten, so that redefining work means creating a successor rather than editing. It does not say where any of it lives between invocations.

Meanwhile `10-technical/01-effect-vocabulary.md` makes work-record mutation a typed, gated effect, `10-foundations/02` names "creating a work item" as a proposal that crosses the same way any effect does, and the M3 runs routed real work-record mutations through the gate. Something was already persisting this in practice with no architectural owner.

`21-arch-knowledge-model` is not that owner. It holds `10-foundations/03`'s claims, and a work item is not a claim — it is what claims attach to.

## The actor and its responsibility

- **Hold intent durably.** Its original human-authored content is not amendable from inside the system — `10-technical/01` type 4 excludes it by name, amendable only out of band. This actor therefore protects intent rather than managing it: written once from outside, read thereafter.
- **Hold work items and their current state.** One formulation per item, fixed at creation, directly readable without reconstructing anything. What changes on an item is its state and its conclusion.
- **Hold a work item's declared scope.** `10-foundations/07` requires that work stay within the mandate it was given, and `24-arch-permission-layer` establishes that capability gating structurally cannot check it — a capability is keyed to the actor and evaluated per effect, while a mandate is keyed to the work item and evaluated in aggregate against what was touched. A declared scope is part of what a work item *says*, which puts the declaration here while the check stays with `24`.

  It is **natural-language text, not a structured field**, and this actor holds it without interpreting it — consistent with everything else here, since this actor does not judge whether a work item is well-formed either.

  It is usually **derived rather than stated**: an operator seldom writes a boundary down, and most of one follows from what the task is and how the system is arranged. Deriving the ceiling from intent is an invariant processor's (`25-arch-invariant-layer`); narrowing it for a child is the orchestrator's, done when it formulates the item. This actor records what either produced without deriving anything itself. That makes what this actor holds two things rather than one — the boundary, and what it was derived from — because a derivation nobody can inspect cannot be contested, and an uncontested wrong derivation is ratified rather than caught (`24-arch-permission-layer`, The shape it takes).

  A scope can also be **pending** rather than derived, when the reading was ambiguous enough that the question went to the operator instead (`24-arch-permission-layer`). That is a state a work item can sit in, not an absence of one, and it needs to be distinguishable from a scope nobody got around to deriving — the first is the check working, the second is it not having run. The distinction has teeth, because the second state stops work: the scope check fails closed on an unscoped item.

  A scope held here is **fixed at creation and never edited**, like the formulation it was derived from. That is what closes the widening path without needing a mechanism: there is no mutation of the field to gate, because there is no mutation of the field. Work whose boundary must move gets a successor task with a scope derived afresh, checked against the ceiling like any other.

  Two consequences for what this actor must support. The declaration has to be readable at any point during the task rather than only at its end, since an irreversible change is questioned before it happens. And a scope is **fixed at creation**, so there is no mid-task widening for an audit to catch: what an audit follows instead is the lineage, where a child or a successor carries its own derived scope. An operator's own indication of a boundary, where one is given, is carried as part of it and governs the derived portion.
- **Record every transition** a work item goes through: challenged, deferred, abandoned, executed. The current state and the history of how it was reached are both held, and neither is derived from the other. Splitting and succession are not transitions on an item — both create new items and leave the existing one untouched (`22-arch-cognition/01`).

  Transitions are not all equally free, and two constraints belong to this actor because they are about the shape of the lineage rather than about any judgment.

  **A split's children derive their own scope at creation, contained in the ceiling** rather than in the parent's. A parent's scope focuses that parent; it does not floor everything beneath it, so a child of a narrow parent may legitimately reach wider while staying inside what intent authorised. What makes splitting unable to manufacture mandate is the ceiling and not the parent: the ceiling descends from intent, and intent is not system-writable (`10-technical/01-effect-vocabulary.md` type 4).

  **A successor stays under the intent's ceiling.** Where an item would have been refined, a new item is created with a redefined objective, and its scope is derived at creation like any other. Redefining broadly is the route that widens without anything ever splitting, and what stops it is the ceiling: every task's scope sits inside the one derived from intent, whether it arrived by split, by succession, or by nested invocation (`24-arch-permission-layer`).
- **Hold a processor's recorded conclusion** — answered, blocked, or declined, with its reasoning. `10-technical/01` classes this as a work-record mutation rather than a memory write, a boundary the M4 runs found carved cleanly once chosen but not self-evident beforehand. Keeping *declined* distinct from *blocked* is load-bearing rather than cosmetic: Milestone 5 recorded an orchestrator collapsing "the task rests on a false premise" and "I cannot find a next step" into one generic outcome, losing a distinction the simpler Milestone 4 arms had made.

Whether three verdicts suffice is open, and the doubt has the same shape as the failure they were introduced to prevent. `22-arch-cognition/01-work-intent-and-task-model.md` names two distinct reasons to refuse execution — the task rests on a false premise, and the request has already been satisfied — and both currently land on *declined* while calling for entirely different follow-ups. That may be this vocabulary reproducing Milestone 5's collapse one level down. Resolving it belongs with the processor contract rather than here; what this actor owes is only that whatever verdicts exist stay distinguishable in the record. Whether an instance judges objective validity at all is that instance's strategy (`10-foundations/04`, The objective itself is not a given); being able to record the verdict once it does is not.

What this actor does not do is decide anything about the work. Whether a work item should be split is the orchestrator's call, and the harder question of where that decision ought to live is `22-arch-cognition/08`'s open question, not this actor's; it records a split once something else has decided and realized one. It likewise does not judge whether a work item is well-formed or whether a recorded conclusion is correct.

## Service provided to the rest of the system

- **Intent lineage.** Given any work item, the chain back to the intent it descends from. `10-technical/01` already requires realized effects to be reconstructable "per intent lineage" and nothing in this band supplied that chain; this actor is what knows it.
- **Current state of work.** What items exist, how each is formulated, what state it is in, and its lineage links in both directions.
- **Transition history**, for one item or for a whole lineage.

## General shape and a naive default

The same restraint `21-arch-knowledge-model` and `23-arch-context-management` commit to: the filesystem, no database, no index, until evidence says the naive version is the actual bottleneck. And the same reading of that restraint — it sequences the work rather than doubting that a real store will eventually be needed, so this actor's service surface is the part that has to survive the change, and a caller must never learn that a work item is a file.

One structured record per work item, holding its current formulation and state as directly readable fields, with an append-only transition log kept alongside it rather than inside it.

That shape is the reason this is a separate actor rather than a region of `21-arch-knowledge-model`, and the reason is the **write discipline** rather than any cost of reading. A claim there is append-only and superseded rather than edited; a work item is rewritten in place every time the work changes. Holding a mutable current view and an immutable record of how it changed asks two incompatible things of one store, and collapsing them would force one of them to give. This is the storage side of the ownership argument above: a work item is not a claim, so it is not held where claims are held.

Intent is a third kind of record again, and the simplest: written from outside the system and never rewritten by it, so it needs no transition log at all.

## Interactions

- **`22-arch-cognition/01-work-intent-and-task-model.md`** owns the vocabulary this actor persists — intent, work item, work unit — and this actor adds no concepts to it.
- **`22-arch-cognition/03-orchestrator.md`** reads current work state on every loop step and proposes the transitions that change it, including its own per-step decision record.
- **`20-arch-runtime.md`** gates and realizes a work-record mutation; this actor persists what the runtime realized, not what was merely proposed.
- **`21-arch-knowledge-model`** is not referenced by this actor at all. What crossed under a task is that task's live set (`23-arch-context-management`), which is the one task—artifact relation; this actor holds the work.
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

Whether one lineage relation suffices for every shape creation produces. A child, a successor and a merge result all descend from existing work by the same edge, differing in fan-out and fan-in rather than in kind, and what separates decomposition from redefinition is the parent's state rather than the edge. Nothing has exercised this.

Whether an abandoned work item is retained or removed. Retention is the cheaper assumption and keeps "why was this dropped" answerable, but nothing here establishes that it is required.
