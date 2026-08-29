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

## What a mature conceptual document should provide

A document should make the motivation for an abstraction explicit, state what problem it is expected to solve, identify the boundaries of the idea, describe how it relates to neighboring concepts, and preserve the unresolved questions that prevent immediate technical specification.

The goal is not to eliminate uncertainty prematurely. The goal is to locate it precisely.

## When a concept is ready for technical specification

A concept is ready to cross into technical design when its responsibility, inputs, outputs, authority, failure modes, and relationships to other components can be described without relying on vague phrases such as "the AI handles it."

Even then, the technical specification should remain traceable back to the conceptual motivation that justified it.

## Revision policy

Conceptual documents are living artifacts.

Changes should preserve historical rationale where useful, especially when a concept is narrowed, renamed, or removed because experiments contradicted an earlier assumption.

Removing an elegant abstraction is considered progress when evidence shows that the abstraction does not provide useful leverage.
