# Documentation Philosophy

## TL;DR

The conceptual documentation exists to make future implementation less ambiguous, not to make current ideas look finished.

> **Motto:** Capture convergence without freezing discovery.

## Why the architecture is documented extensively

The project contains several abstractions that interact in subtle ways: work representation, orchestration, ephemeral processors, context governance, persistent knowledge, evaluation, feedback loops, experimentation, system generations, and bootstrapping.

If these ideas remain only conversational, later implementation will silently fill conceptual gaps with accidental technical decisions.

The documentation therefore aims to expose those gaps before they become code.

## Why the documents are split by theme

Each important conceptual decision should be independently reviewable.

A future discussion about context selection should not require reopening the full project charter. A challenge to the role of the orchestrator should not automatically invalidate the feedback architecture. A revision to the meta-evaluation concept should remain traceable as a local conceptual change unless it genuinely has broader consequences.

This modularity is intended to make conceptual iteration efficient.

## Which layer states what

The split by theme has a second axis that had been practised without being written down, and stating it is what keeps the layers independently reviewable rather than merely separately filed.

**Foundations name functions and constraints.** What has to be true, what distinctions must be kept, what a thing is *for*. Long-term memory, context as a governed resource, the reasoning/runtime boundary.

**Architecture names actors and arrangements.** Who holds what, what service each provides, how they interact. A knowledge model, a context manager, a live set that points rather than copies.

**Technical specification names formats and contracts.** Schemas, effect types, interfaces.

The failure to watch for runs downward: a foundations document naming a particular solution shape. It spends a decision it did not need to make, it is wrong as soon as the architecture changes even though the function it was describing did not, and it quietly removes architecture's freedom to choose differently.

A concrete instance, since the rule is easier to apply against one. Foundationally, a tool's response is discussion material: it arrives, it is live, and it does not enter long-term memory by arriving — promotion is a separate act. Architecturally, the context manager holds no copy and points into a store where everything already sits from the moment it arrives. Both are true. The foundational documents briefly said the second, which made a storage arrangement look like a claim about what the system *knows*, and blurred the distinction between storing something and having decided it was worth keeping.

Citing across layers is not the problem and is expected — a foundations document may cite an architecture document for evidence or for where a question went. Importing its solution shape is.

## What a mature conceptual document should provide

A document should make the motivation for an abstraction explicit, state what problem it is expected to solve, identify the boundaries of the idea, describe how it relates to neighboring concepts, and preserve the unresolved questions that prevent immediate technical specification.

The goal is not to eliminate uncertainty prematurely. The goal is to locate it precisely.

## When a concept is ready for technical specification

A concept is ready to cross into technical design when its responsibility, inputs, outputs, authority, failure modes, and relationships to other components can be described without relying on vague phrases such as "the AI handles it."

Even then, the technical specification should remain traceable back to the conceptual motivation that justified it.

## Prose discipline

Design and specification documents are authoritative. They are read to determine what is required and what is claimed.

State the claim, its basis, and its consequence. Emphasis and figurative phrasing are available where something must stand out; used as the default register they stop marking anything.

This is not a matter of taste. Authority in this set is grounded in auditable argumentation — each step checkable against a finding, a design position, or a prior contract. Extended phrasing obscures which sentences carry the argument and which are ornament, and an argument whose steps cannot be located cannot be audited.

The same applies to a document's scope. A document argues its own subject; borrowing weight from an adjacent one blurs which set a claim belongs to and puts its correctness beyond the reach of the people reviewing that document.

The `Motto` line is the exception, and the reason the convention exists. It carries vision or intent in compressed form, in a designated place where it cannot be mistaken for a step in the argument. Ornament in the body obscures the reasoning; ornament in a slot reserved for it does not. Use one wherever it earns its line.

## Revision policy

Conceptual documents are living artifacts.

Changes should preserve historical rationale where useful, especially when a concept is narrowed, renamed, or removed because experiments contradicted an earlier assumption.

Removing an elegant abstraction is considered progress when evidence shows that the abstraction does not provide useful leverage.
