# Capabilities and Authority

## TL;DR

Knowing how to request an action is not the same as being authorized to make that action real.

> **Motto:** Capability enables proposals; authority governs effects.

## Motivation

The system needs flexibility to introduce new processor roles without hardcoding every role into the runtime.

A capability model provides a stable way to describe what kinds of operations a processor may request.

## Capability concept

Capabilities may cover areas such as workspace access, repository inspection, file modification, process execution, task manipulation, processor invocation, memory proposals, or system experimentation.

Capabilities describe available operations, not a guaranteed right to perform arbitrary effects.

**On that list.** It was written before the effect vocabulary existed, and it is one of three overlapping lists `10-technical/01-effect-vocabulary.md` later reconciled into nine types. It should be read as the areas a policy concerns itself with, not as the enumeration — the enumeration is the effect vocabulary's, and a capability policy is expressed over that. Two of the areas have since acquired owners worth naming: memory proposals are proposals to `21-arch-knowledge-model`, which only a thinking processor makes (`22-arch-cognition/04-thinking.md`), and task manipulation is work-record mutation against `28-arch-work-record`.

## Reads, and where the permissive default lives

A read is not a typed effect, and it is still something an actor may or may not be allowed to perform. `10-foundations/02`'s 2026-09-11 Qualification withdrew the claim that reads are outside what may be checked, and `25-arch-invariant-layer` now carries reads in the gate's input domain — but the question of what *ordinarily* happens to a read is a policy question, which makes it this document's.

The default is permissive: reads pass unless a rule names them. That is a configuration this model expresses, not a property of reads, and it is stated as a default precisely so that it can be changed without anything structural having to move.

What granularity a rule may use to name a class of reads — by path, by crossing type, by volume against a ceiling — is unresolved, and is the same open question `10-foundations/02` holds from the foundational side.

## Authority

The runtime remains responsible for interpreting a requested operation under the current policy.

A reviewer may be allowed to inspect files but not modify them. An implementer may be allowed to propose and perform bounded workspace changes. A system-level optimizer may be able to create candidate configurations without being able to promote them into the trusted baseline.

## Why the distinction matters

Without this separation, role definitions become entangled with runtime security and system governance.

With it, roles can evolve experimentally while operational boundaries remain explicit.

## What this model does not provide

Capability and authority govern what a given actor may request under current policy, and that policy is legitimately adjustable as the system learns.

They are therefore not a floor. A separate, non-adjustable check sits beneath them, testing whether an effect is permissible at all rather than whether this actor is presently authorized to request it. An effect must pass both, and passing capability gating is not evidence of passing that check.

The two also differ in what they are keyed to. Capabilities are described per role, which works because policy can be revised as roles are added. The invariant check cannot be keyed to roles at all, since the role vocabulary is deliberately open-ended; it binds effects instead.

Neither of them answers a third question, and it is worth naming here so that this model is not asked to carry it. **Whether an effect is worth what it forecloses** is not a permission question. An effect can be requestable by this actor, permissible in general, and still a bad idea in this particular situation — most obviously when it is irreversible by nature, which `10-foundations/02` says cannot be refused on reversibility grounds alone without refusing the work itself. That judgment is reasoning-based, belongs to `22-arch-cognition/04-thinking.md`, and happens while the proposal is being formed rather than as a stage in the gating path. `25-arch-invariant-layer` sets out why it must sit upstream rather than inside the pipeline.

So: this model asks whether the actor may request it, the invariant gate asks whether it may happen at all, and thinking asks whether it should. Three questions, three owners, and only the first two are gates.

## A fourth question, which this model does not yet answer

There is one more, and the three-question framing above made it harder to see by looking complete. **Is this within what was asked for?**

`10-foundations/07` names this document as the destination for it — "scope declared and checked belongs with the capability and authority model" — and nothing here currently implements it. The failure mode that commitment exists to prevent is stated there precisely: work beyond the mandate it was given, "including where each step past it is locally justified by the last."

That is not a capability question and capability cannot be stretched to cover it, because the two are keyed to different things. A **capability** is keyed to the actor, set by policy, and evaluated per effect: an implementer may perform bounded workspace changes. A **declared scope** is keyed to the work item, declared per task, and evaluated against what was actually touched. Every step of a drift past the mandate can sit inside capability while the aggregate sits outside the mandate, and a per-effect check keyed to the actor will see nothing wrong at any point.

`25-arch-invariant-layer` already states the property that makes this structural rather than an oversight: capability gating evaluates one proposed effect at a time, and a sequence of individually authorized actions can assemble into an outcome no single check was designed to catch. That observation was made about invariant enforcement and applies here unchanged; the line between it and `07`'s commitment had not been drawn.

**It is authority's rather than capability's**, which is why it belongs in this document despite needing something this document does not have. Authority is already the dynamic half — the runtime interpreting a requested operation under current policy — while capability is the static description of what a role may ask for. A mandate is dynamic in the same way, and adjustable per task.

**It is not the invariant layer's**, and the distinction matters. Mandates differ per work item and are set by whoever asked for the work. A mechanism holding something adjustable would not be the invariant layer, whose defining property is that no loop may write to it.

What would have to exist, stated as shape rather than mechanism: a **declared scope carried on the work item** — which makes it `28-arch-work-record`'s to hold, since that actor holds the work item and its formulation — and a **comparison against what was actually touched**, which has to be aggregate over a sequence rather than per effect.

### The shape it takes

**Scope is a task-level property, expressed in natural language.** It cannot be fixed per role, because the same role does differently-bounded work from one task to the next, and it cannot be enumerated in advance, because what a change is allowed to reach is a statement about this piece of work. The artifacts where the boundary matters most are the ones where drift is cheapest and least visible: specification documents, technical documentation, internal APIs.

That natural-language form does not conflict with `10-foundations/07`'s requirement that this become "checkable properties of artifacts and effects, never an inference about intent", and the distinction is worth stating because it is easy to lose. **A stated scope is not an inferred intent.** What `07` forbids is predicting what a person would have wanted; a declared scope was written down by whoever asked for the work, so comparing against it is checking against a record. The judgment lives in the comparison — does this diff fall inside that statement — not in guessing the person.

**The check divides on reversibility, and the two halves sit at opposite ends of a task.**

- **Reversible changes are audited at the end.** Their extent can be compared against the declaration once the work is done, in aggregate, which is the only point at which drift is visible as drift. Auditing late is affordable precisely because the finding still has a remedy: what fell outside can be undone.
- **Irreversible changes are questioned before they happen.** There is no end-of-task remedy, so the check has to precede the effect.

That second placement is the same one already reached from a different direction. `10-foundations/02` requires an irreversible effect to get a risk evaluation before it is proposed, and `25-arch-invariant-layer` explains why such a judgment must sit upstream of the proposal rather than inside the gating path. Scope questioning for an irreversible change lands at exactly that moment, on exactly that argument. Two requirements derived independently, converging on one point in the loop, is a reason to treat that point as real.

**It requires a dedicated processor**, because the comparison is a judgment over natural language and no deterministic check performs it. That processor is *not* commissioned from the open role vocabulary, and `25-arch-invariant-layer` holds the reason: a loop cannot commission its own watcher. It is a fixed role of the same kind as triage, specified where the invariant layer is specified, and its protection is stated there rather than here.

The separation that keeps this coherent: **the mandate is adjustable, the checker is not.** What a given task's scope permits changes with every task and is set by whoever asked for the work, which is why mandate content is not invariant-layer material. That a functioning scope check exists, and cannot be removed or routed around by the loops it constrains, is not adjustable by anything inside the system, which is why the checker is.

## Open question

Capability granularity should be derived from actual needs. Overly coarse capabilities weaken control; overly fine capabilities create administrative complexity and can distract the model from the cognitive objective.

Reads are the first concrete instance of that trade-off rather than a separate question. Naming a class of reads by path, by crossing type, or by volume against a ceiling are granularities with very different administrative costs, and the permissive default above means none of them has to be chosen before there is a reason to.

How a declared scope is expressed and compared, per the section above. `10-foundations/07` requires that it become "checkable properties of artifacts and effects, never an inference about intent" — so a comparison of declared scope against what was touched qualifies, and anything of the form "what the operator would have wanted" does not.

Whether mandate conformance is refused, escalated, or merely recorded when it fails. `07` says the requirement "cannot be enforced by deterministic refusal alone", which rules out treating it like the invariant gate, and leaves what it *is* treated like unanswered.

