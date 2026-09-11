# Invariant Enforcement and Safety Response

## TL;DR

The invariant layer requires a mechanism beneath the capability model that checks proposed effects against it. This document states what that mechanism's structure must be. It deliberately does not yet specify how it operates.

> **Motto:** The gate binds effects, not roles.

## Status of this document

This document is bounded on purpose.

The structural claims below — where the gate sits, what it binds, what the triage role may and may not do, and how a decommission is signalled — follow from the invariant layer's definition and are stable enough to record now.

The operational specifics are not recorded here: the escalation protocol, threshold definitions, the representation of the failure signal, and what human intervention actually looks like in practice. Those are precisely where existing work on corrigibility, scalable oversight, and interruptibility has both results and known failure modes, and this project should inherit them rather than rediscover them empirically. They remain deferred until that reading pass — scheduled as a Milestone 11 deliverable — is done.

## The gate is not a role

The enforcement mechanism is not a processor, not a role, and not anything invoked and reasoned with.

A reasoning component is persuadable by construction, and persuadability is precisely the failure mode this mechanism exists to close off.

It should be a deterministic runtime check: narrow, mechanical, over the line or not. It should not be smart, because smart is another word for persuadable.

## The gate binds effects, not roles

The system's vocabulary of roles is deliberately open-ended. System-level feedback may commission actors that did not exist when the invariant list was written.

A mechanism keyed to roles would therefore be permanently incomplete by design. It would have to anticipate a vocabulary the architecture has explicitly refused to fix.

Effects are the opposite. Filesystem mutation, process execution, network access, memory writes, configuration promotion, and processor invocation form a bounded set that the runtime already represents in order to execute anything at all.

Binding the gate to that set is what allows role commissioning to stay aggressive without weakening the floor. A newly commissioned role inherits no exemption. It can only ever request effects the runtime already knows how to check.

This is also how the invariant layer stays small. It needs no clause per role, per loop, or per generation — only a statement about what may never become true, expressed in the one vocabulary the runtime can verify without reasoning.

## What the gate may see is wider than what it evaluates

Binding the gate to effects says what it is keyed to. It must not be read as saying that effects are the only thing it may look at, and the project has made that mistake once: `10-foundations/02` excluded reads from the gate's reach on the grounds that gating every read would recreate a rigid workflow engine, and its 2026-09-11 Qualification withdraws that half.

The argument above is the reason. It binds to effects because effects are "a bounded set that the runtime already represents in order to execute anything at all." A read is equally something the runtime represents in order to execute anything at all. Nothing in the effect-binding argument excludes it; the exclusion was a separate and weaker claim sitting next to it.

So the gate's input domain is runtime-mediated operations, of which typed effects are the subset that change the world outside the system. A read is in the domain. Whether any rule fires on one is policy, and the default should be permissive — reads pass unless a rule names them — because the cost concern that motivated the exclusion is real even though the conclusion drawn from it was not. A permissive default is adjustable; a domain that cannot represent reads is not.

Two things follow. A resource ceiling is expressible: context is a bounded resource (`10-foundations/04`, Overload), ceilings are invariant-layer content (`10-foundations/06`), and a read that would cross one is a read the gate has to be able to see. And the Composition risk below stops having a blind half — a sequence of permitted reads followed by one permitted effect is the shape that section exists to catch, and reads outside the domain are reads outside the sequence.

## Position relative to capability gating

This sits below the capability and authority model rather than within it.

Capability gating asks whether a given actor is authorized to request a given operation under current policy, and that policy is legitimately adjustable. The invariant gate asks a different question — whether the effect is permissible at all — and its answer is not adjustable by anything inside the system.

An effect must pass both. Passing capability gating is not evidence of passing the invariant gate.

## Composition risk

Capability gating evaluates one proposed effect at a time.

A sequence of individually authorized actions can in principle assemble into an outcome that no single check was designed to catch. The gate must therefore be able to evaluate sequences, not only isolated requests.

The sequence has to include reads, which is the practical consequence of the input-domain section above. The canonical composed outcome is an accumulation of permitted reads followed by one permitted effect that carries the accumulation somewhere it should not go. A gate evaluating only typed effects sees the carrying step and nothing of what filled it, which is the half that determines whether the step matters.

This makes the reconstruction requirement described under observability more load-bearing than it first appears. Detection of composed or drifting behavior runs against reconstructable history, not against individual requests in the moment.

## The triage role

When the gate trips, most cases will not be malicious — clumsy sequencing, an edge case, a legitimate but unanticipated need.

A triage role assesses and routes: log and let the original, already-gated effect proceed unchanged; escalate; or halt.

It must never have authority to approve an effect the gate rejected. If it could, it would become a second and persuadable version of the mechanism it sits behind.

## Why the triage role is fixed rather than commissioned

Role creation otherwise belongs to the feedback loops, which commission against identified need on evidence.

This role is an exception, and not because it fails that test. The mechanism that applies the test cannot reach it.

A loop cannot commission its own watcher. Anything a loop commissions is inside that loop's scope by construction — parameterized by it, tunable by it, revisable by it on its own evidence. A watcher whose parameters the watched loop may propose changes to is not a watcher.

The burden therefore falls to the humans writing the invariant layer, for the same reason that layer is human-authored: not a preference for designing things in advance, but the absence of any other party with standing to do it. The role satisfies the invariant layer's membership test, and its bounds are specified alongside the constraints it enforces.

Non-shared model or lineage with the loops it watches follows from this as a consequence rather than standing as the primary argument. The correlated-blind-spot concern raised for evaluation independence applies with more force here, since the failure being guarded against is a loop's own drift — but the structural point stands even where blind spots are not at issue.

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
