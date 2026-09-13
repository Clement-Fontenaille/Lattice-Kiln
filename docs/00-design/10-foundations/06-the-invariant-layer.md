# The Invariant Layer

## TL;DR

Every adaptive mechanism in this system — role commissioning, context governance, memory curation, model assignment, project-level, system-level, and meta-level feedback — is designed to change itself based on evidence. The invariant layer is the part that is structurally exempt from that change: a small, explicit set of goals, resource ceilings, and **inescapable constraints** that every loop may read and none may write.

It is human-authored and human-amended only, and it is enforced rather than merely stated.

> **Motto:** Something must be true regardless of what the loops decide.

## Motivation

Evidence is only meaningful relative to a standard of what the system is for.

If that standard is itself a tunable parameter, the system can satisfy its own measurements by quietly redefining what is being measured.

This is the Goodhart risk already named in this set, but that treatment scopes frozen baselines to evaluation benchmarks. The generalization is that the goals and hard limits themselves must be frozen relative to every feedback loop, including system-level and meta-level feedback.

This is where alignment risk in this architecture concentrates. It is not located in any single processor's output. It is located in the possibility that the system's own optimization process has no floor it cannot optimize away.

## What the layer contains

Goals — what the system is for, stated well enough that a measurement can be checked against them rather than substituted for them.

Resource ceilings — compute, cost, concurrency, and other physical or financial limits.

Inescapable constraints — what the system may not get out from under, regardless of what any loop concludes.

The layer should be small. Its value comes from being stable and checkable, not from being comprehensive.

**Inescapable, not hard**, and the distinction carries weight. *Hard* would describe the **form** of a constraint — a bright line, mechanically checkable, binary. What defines membership here is a **relation to the system**: it cannot evade this. Those come apart. A scope check comparing a natural-language mandate against a diff is not a bright line and is entirely inescapable, since the system can neither remove it, route around it, nor argue past it.

Reading membership as a matter of form would imply that enforcement must be mechanical, and that would be wrong in a way that propagates: it would exclude any reasoning component from this layer, when what actually makes one safe to fix here is **direction** — it may restrict and never widen, so persuading it achieves nothing (`25-arch-invariant-layer`, Invariant processors).

The other two terms were already defined this way. A goal a loop could rewrite is not a goal but a preference; a ceiling the system can raise is not a ceiling. Inescapability, not crispness, is what the three have in common.

None of this widens the layer. What qualifies is decided by The membership test below; this settles what membership *means*, not what passes.

## Read by everything, written by nothing

Every loop may read the layer, and should. A loop that cannot see what it is optimizing toward, or what it may not touch, is optimizing blind.

No loop may write to it. Amendment happens through direct human action, outside the candidate, evidence, and promotion pipeline entirely — never as a system proposal, regardless of how well evidenced that proposal is.

This is a categorical difference rather than a matter of degree. System-level feedback decides what may exist. The invariant layer decides what may never be true.

## The membership test

A necessary condition for belonging in this layer: **could any loop author this without being inside the scope it is meant to constrain?**

If it could not, it belongs here. A loop cannot author its own goals without being able to satisfy them by revision. A loop cannot commission its own watcher, because anything it commissions is parameterized by it. A loop cannot set the threshold at which its own behavior triggers intervention.

The test is necessary rather than sufficient. It identifies what is disqualified from being tunable. It does not determine which specific goals and ceilings should be written, which remains a human question closer to drafting a constitution than to proposing a configuration change.

## Enforcement, not statement

This set already describes foundational constraints as a matter of decision discipline. That description is aspirational — a statement of what the project intends to hold to.

This layer differs in kind. It requires a deterministic mechanism that checks proposed effects against it and refuses those that cross the line. A constraint that exists only as documentation is a constraint the system can violate without anything noticing.

**This layer is content; the floor is the mechanism.** The distinction is worth holding because one word has been carrying both. What this document defines — goals, resource ceilings, inescapable constraints — is a set of statements. The **floor** is the gate that enforces them: the deterministic point nothing argues past. `25-arch-invariant-layer` holds that gate along with the other mechanisms no loop may adjust, and sets out the pattern they share, which is that each is fixed while the content it applies is set by someone outside the loops it constrains.

## Why this makes deferral safe

Much of this documentation set defers deliberately. Context governance is left to be discovered rather than designed. The vocabulary of roles is left open-ended. Memory policy, model assignment, and evaluation thresholds are all left to be resolved by evidence.

Read alone, that is a permissive posture. It is not.

Every deferral in this set is a bet that a bad outcome will be observable and correctable. That bet is sound only where the failure can be neither catastrophic nor self-concealing. The invariant layer is what makes such failures non-catastrophic; observability is what makes them non-self-concealing. Together they are the precondition for the rest of the architecture's willingness to leave things open.

The floor and the deferral are therefore one position rather than two.

The gain is sharpest at the meta level. With a floor, the meta loop asks only whether the system's self-tuning produces trustworthy improvement. Without one, it would also have to ask whether the system is still pursuing the right goals at all — a question no amount of evidence answers, because the evidence is generated under the goals being questioned.

## Status of this concept

The argument above is architectural. It reasons from this set's internal consistency and is not grounded in prior work.

Schemes of this general shape have been studied, and both their partial successes and their known failure modes exist in the literature on corrigibility, scalable oversight, specification gaming, and shutdown and interruptibility problems. A deliberate reading pass against that work is required before this concept is treated as settled, and the design is expected to change in response to what that pass finds. That pass is scheduled as a Milestone 11 deliverable — grouped with the rest of the safety-response elaboration rather than gating the floor's first, provisional form.

The claimed benefits are the most likely part to need revision, because they are the part that is argued rather than evidenced.

## Open question

What actually belongs in the invariant list — specific enough to be checkable, stable enough not to need frequent revision, without being so narrow that it fails to anticipate real failure modes.

Whether a single invariant layer serves all system generations and branches, or whether branches may reasonably hold different invariants — and if so, what must remain invariant across all of them regardless.

How resource ceilings are represented in the same structure as behavioral constraints, given that they are physical and financial rather than evidentiary in nature.
