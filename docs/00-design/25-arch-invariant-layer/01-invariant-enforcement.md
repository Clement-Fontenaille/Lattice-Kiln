# Invariant Enforcement and Safety Response

## TL;DR

The invariant layer requires a mechanism beneath the capability model that checks proposed effects against it. This document states what that mechanism's structure must be. It deliberately does not yet specify how it operates.

> **Motto:** The gate binds effects, not roles.

## Status of this document

This document is bounded on purpose.

The structural claims below — where the gate sits, what it binds, what the triage role may and may not do, and how a decommission is signalled — follow from the invariant layer's definition and are stable enough to record now.

The operational specifics are not recorded here: the escalation protocol, threshold definitions, the representation of the failure signal, and what human intervention actually looks like in practice. Those are precisely where existing work on corrigibility, scalable oversight, and interruptibility has both results and known failure modes, and this project should inherit them rather than rediscover them empirically. They remain deferred until that reading pass — scheduled as a Milestone 11 deliverable — is done.

## What sits here, and what the floor is

This document holds four mechanisms. They share one property and nothing else: **none of them is adjustable by what it constrains.**

- **The gate** — deterministic, mechanical, over the line or not.
- **Triage** — the invariant processor that assesses and routes a trip.
- **The scope check** — the invariant processor that compares work against its mandate (`24-arch-permission-layer`).
- **The capability engine** — the mechanism that applies capability policy to a requested operation.

**The floor is the gate, not this collection and not the invariant layer.** Those are three different things and the word has been doing double duty. `10-foundations/06`'s **invariant layer** is *content*: the small, explicit set of goals, resource ceilings and hard constraints every loop may read and none may write. The **floor** is the gate — the deterministic point nothing argues past. This document is the *enforcement* architecture, which is where the mechanisms live. A layer of statements, a floor that stops things, and the machinery in between.

**Each mechanism is fixed while its content is adjustable, and by a different party each time.** That pattern recurs and is worth stating once rather than rediscovering per occupant.

| mechanism | fixed | content, and who sets it |
|---|---|---|
| gate | the check | the invariant list — humans, out of band |
| scope check | that it runs, and that it only narrows | the mandate — whoever asked for the work, per task |
| capability engine | that it applies | capability policy — system-level feedback |
| triage | its routing authority and its limits | what trips, which is the gate's |

Confusing the two halves is the failure to watch for in both directions. Treating a mechanism as adjustable removes the floor; treating content as fixed freezes something that has to move — a mandate differs per task, and capability policy is meant to be revised as roles are added.

## The gate is not a role

The enforcement mechanism is not a processor, not a role, and not anything invoked and reasoned with.

A reasoning component is persuadable by construction, and persuadability is precisely the failure mode this mechanism exists to close off.

It should be a deterministic runtime check: narrow, mechanical, over the line or not. It should not be smart, because smart is another word for persuadable.

That is a statement about **the gate**, not about everything this layer may contain. The layer also fixes roles that do reason — triage, below, and the scope check — and Invariant processors sets out the condition under which that is safe rather than contradictory: they may restrict and never widen, so persuading one achieves nothing. The gate remains the thing that is not smart.

## The gate binds effects, not roles

The system's vocabulary of roles is deliberately open-ended. System-level feedback may commission actors that did not exist when the invariant list was written.

A mechanism keyed to roles would therefore be permanently incomplete by design. It would have to anticipate a vocabulary the architecture has explicitly refused to fix.

Effects are the opposite. Filesystem mutation, process execution, network access, memory writes, configuration promotion, and processor invocation form a bounded set that the runtime already represents in order to execute anything at all.

Binding the gate to that set is what allows role commissioning to stay aggressive without weakening the floor. A newly commissioned role inherits no exemption. It can only ever request effects the runtime already knows how to check.

This is also how the invariant layer stays small. It needs no clause per role, per loop, or per generation — only a statement about what may never become true, expressed in the one vocabulary the runtime can verify without reasoning.

## What the gate may see is wider than what it evaluates

Binding the gate to effects says what it is keyed to. It must not be read as saying that effects are the only thing it may look at, and the project has made that mistake once: `10-foundations/02` excluded reads from the gate's reach on the grounds that gating every read would recreate a rigid workflow engine, and its 2026-09-11 Qualification withdraws that half.

The argument above is the reason. It binds to effects because effects are "a bounded set that the runtime already represents in order to execute anything at all." A read is equally something the runtime represents in order to execute anything at all. Nothing in the effect-binding argument excludes it; the exclusion was a separate and weaker claim sitting next to it.

So the gate's input domain is runtime-mediated operations, and typed effects are not the subset that change the world outside the system — every runtime-mediated operation does that. A read leaves an access record, makes a store do work and compete for its capacity, spends metered quota, and is sometimes a state transition outright (dequeuing a queue item, marking a message read, firing a watcher). `10-foundations/02`'s Qualification withdraws that basis along with the exclusion itself.

What the typed-effect vocabulary enumerates is the set of operations whose **footprint** this project has decided is worth naming and tracking. Footprint is a gradient, so membership is a judgment about where tracking pays rather than a consequence of what the operation is. That is weaker than the original claim and survives contact with it, and it costs the gate nothing it actually used: the set is still bounded, still closed, still checkable without reasoning.

A read is therefore in the domain, and it is there for a stronger reason than before — not because it touches the system's own state while leaving the world alone, but because the only thing separating it from a typed effect is how large its footprint is. Whether any rule fires on one is policy, and the default should be permissive: reads pass unless a rule names them. A permissive default is adjustable; a domain that cannot represent reads is not.

Two things follow. A resource ceiling is expressible: context is a bounded resource (`10-foundations/04`, Overload), ceilings are invariant-layer content (`10-foundations/06`), and a read that would cross one is a read the gate has to be able to see. And the Composition risk below stops having a blind half — a sequence of permitted reads followed by one permitted effect is the shape that section exists to catch, and reads outside the domain are reads outside the sequence.

## Position relative to capability gating

This sits below the capability and authority model rather than within it.

Capability gating asks whether a given actor is authorized to request a given operation under current policy, and that policy is legitimately adjustable. The invariant gate asks a different question — whether the effect is permissible at all — and its answer is not adjustable by anything inside the system.

An effect must pass both. Passing capability gating is not evidence of passing the invariant gate.

## What the gate does not evaluate: whether an effect is worth it

Three different questions can be asked about a proposed effect, and only two of them are gating questions. Keeping them apart is what lets this gate stay mechanical.

- **May this actor request it?** Capability and authority (`24-arch-permission-layer`), under a policy that is legitimately adjustable as the system learns.
- **May it happen at all?** This gate, under constraints no loop may adjust.
- **Is it worth what it forecloses?** Neither of the above. This is a judgment, it is context-dependent, and it has no fixed answer.

The third question is not this layer's, and `10-foundations/02` says why in a form worth repeating precisely: this layer holds effects that may never occur regardless of what any loop concludes, and **a legitimately irreversible effect is by definition not one of those**. Deleting a branch, dropping a database, publishing something — each may be exactly what was asked for. Refusing them on reversibility grounds alone would be refusing to do the work.

So an irreversible effect needs a real evaluation of whether this specific change, in this specific context, is worth what it closes off. That evaluation is reasoning-based and context-grounded, it is weighed the way any other claim is weighed (`10-foundations/03`, Weighing claims), and it belongs to `22-arch-cognition/04-thinking.md`.

**It sits upstream of the proposal, not in the gating pipeline.** This is the load-bearing part. The evaluation happens while the effect is being formed, before it is submitted — not as a fourth stage after capability and before the invariant check. If it were a stage in the pipeline it would be a reasoning component sitting inside the enforcement path, which is precisely the persuadable mechanism The gate is not a role exists to keep out. Judgment before the proposal; mechanism after it.

One consequence for this layer. The gate never has to ask whether an effect was well-considered, and must not try. An irreversible effect that passes is permitted, not endorsed, and an effect proposed without the judgment having been made looks identical to one proposed after it. Whether the judgment happened is a question for the record (`26-arch-observability`), not for the gate.

## Composition risk

Capability gating evaluates one proposed effect at a time.

A sequence of individually authorized actions can in principle assemble into an outcome that no single check was designed to catch. The gate must therefore be able to evaluate sequences, not only isolated requests.

The sequence has to include reads, which is the practical consequence of the input-domain section above. The canonical composed outcome is an accumulation of permitted reads followed by one permitted effect that carries the accumulation somewhere it should not go. A gate evaluating only typed effects sees the carrying step and nothing of what filled it, which is the half that determines whether the step matters.

This makes the reconstruction requirement described under observability more load-bearing than it first appears. Detection of composed or drifting behavior runs against reconstructable history, not against individual requests in the moment.

## The triage role

When the gate trips, most cases will not be malicious — clumsy sequencing, an edge case, a legitimate but unanticipated need.

A triage role assesses and routes: log and let the original, already-gated effect proceed unchanged; escalate; or halt.

It must never have authority to approve an effect the gate rejected. If it could, it would become a second and persuadable version of the mechanism it sits behind.

That constraint turns out to be the general condition for any reasoning role this layer fixes, not a precaution particular to triage — see Invariant processors.

## Why the triage role is fixed rather than commissioned

Role creation otherwise belongs to the feedback loops, which commission against identified need on evidence.

This role is an exception, and not because it fails that test. The mechanism that applies the test cannot reach it.

A loop cannot commission its own watcher. Anything a loop commissions is inside that loop's scope by construction — parameterized by it, tunable by it, revisable by it on its own evidence. A watcher whose parameters the watched loop may propose changes to is not a watcher.

The burden therefore falls to the humans writing the invariant layer, for the same reason that layer is human-authored: not a preference for designing things in advance, but the absence of any other party with standing to do it. The role satisfies the invariant layer's membership test, and its bounds are specified alongside the constraints it enforces.

Non-shared model or lineage with the loops it watches follows from this as a consequence rather than standing as the primary argument. The correlated-blind-spot concern raised for evaluation independence applies with more force here, since the failure being guarded against is a loop's own drift — but the structural point stands even where blind spots are not at issue.

## Invariant processors

The gate is not a role. Some **processors** nonetheless belong to this layer, and there are now two: triage, above, and a **scope check** — `10-foundations/07` requires that work stay within the mandate it was given, and `24-arch-permission-layer` establishes that no deterministic check can carry it, since a mandate is stated in natural language at task level and comparing it against what was touched is a judgment.

That sits uneasily next to The gate is not a role, and the discomfort is worth working through rather than waving at, because a reasoning component placed in this layer is exactly the persuadability this layer exists to close off.

**The resolution is direction, and this layer already relies on it without having generalized it.** Triage is permitted to reason because of a constraint stated for it specifically: it must never have authority to approve an effect the gate rejected. Persuading triage gets you an escalation or a halt — outcomes that are never the failure. Persuading it to permit something is not available, because permitting is not among the things it can do.

Stated generally: **an invariant processor may reason only where it can restrict and never widen, so that the worst result of persuading it is that it does nothing.**

The scope check satisfies that, and the reason is worth being precise about. A scope narrows within capability; it never reaches past it. An effect still passes capability gating and still passes the gate, whatever the scope says. So a scope check that is lax, confused, or talked into generosity degrades to *no scope check* — which is where this project stands today — and it cannot open anything capability had closed. Its failure mode is uselessness, not permission.

That is what makes membership safe here and would not make it safe for an arbitrary role. A processor whose judgment could grant would not qualify however well argued, since the whole layer's value is that no argument reaches it.

Two things follow that are easy to get wrong. **The gate itself stays deterministic**: nothing here softens The gate is not a role, and an invariant processor is not a smarter gate but a separate occupant of the same layer. And **deriving a scope is ordinary cognition rather than part of the check** — the derivation is a proposal, recorded with its reasoning and contestable (`24-arch-permission-layer`), while what this layer fixes is that a check runs at all and that it can only narrow.

Beyond direction, membership needs the ordinary test: a loop able to remove one, retune it, or route around it is inside the scope that role constrains, so a loop cannot be the party that commissions it — the test stated in `10-foundations/06` and applied to triage above.

**Everything else follows from membership and is not restated per role.** That system-level feedback may not delete one or reshape the path around it, that a system lacking one is not valid — these are properties of belonging to a layer every loop may read and none may write, not separate stipulations attached to particular occupants. Enumerating them role by role would be worse than redundant: it would imply that a future invariant processor arriving without its own enumeration is unprotected.

What this layer does *not* hold is the mandates themselves. A task's scope is set by whoever asked for the work and differs with every task, which is exactly the adjustability this layer exists to be free of. The checker is fixed; what it checks against is not.

**"Functioning" needs a test, and this part does not follow from membership.** Membership means a role cannot be removed. It says nothing about whether the role still works, and a scope check that passes everything is indistinguishable by inspection from one that catches things — the same collapse `22-arch-cognition/05-curation.md` records for an over-generous curator, with the symptom again an absence rather than an error. The answer available here and not there is a **predefined scenario with a planted violation**, which a functioning occupant must catch: an out-of-scope change for the scope check, a boundary-exceeding sequence for triage. That places the test at the extraction level of `27-arch-adaptation-and-evolution/03`'s evidence gradient, which is where a check on something the loops must not influence belongs anyway.

## Decommissioning is immediate and unilateral

A role attempting to exceed its authorized bounds should have its capabilities revoked by the runtime at once — no proposal, no evaluation step, no waiting for human review before authority is pulled.

This is the grant and revoke primitive the capability model already implies, exercised in the direction opposite to normal operation.

## Decommissioning is a distinct failure signal

If a loop commissioned a role and that role is decommissioned mid-task, the loop must be able to tell that its objective failed because of a safety intervention rather than through ordinary task failure such as bad output, timeout, or low quality.

Collapsing these into one generic incomplete result is dangerous. A loop that cannot tell the difference may retry with a rephrased proposal, which is the boundary-probing pattern this mechanism exists to prevent rather than to invite.

This requires its own outcome category in the observability and provenance model: traceable, and explicitly not eligible for automatic retry without human review.

## Accumulation

A single trip may be innocuous. A pattern of repeated and individually innocuous trips — from the same role, the same loop, or a correlated set — may not be.

Some threshold must convert accumulated alerts into a mandatory stop that no loop can reason its way past. This guards against drift by repetition rather than only drift by single large action.

The threshold belongs in the invariant layer rather than being tunable by what it watches. It satisfies the membership test for the same reason the triage role does.

## Open question

Where exactly the gate sits relative to the runtime — whether it is a component of the runtime, or a layer the runtime is itself subordinate to.

What "consecutive" or "correlated" means precisely for alert accumulation: same role, same loop, same category of violation, or some combination.

What the human-facing escalation protocol looks like in practice — who is notified, what state the system is frozen into, and what is required before resumption.
