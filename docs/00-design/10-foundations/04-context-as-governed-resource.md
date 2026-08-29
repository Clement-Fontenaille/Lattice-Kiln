# Context as a Governed Resource

## TL;DR

Context should be intentionally assembled for a purpose, measured as a resource, and evaluated as part of system behavior.

> **Motto:** Relevant context beats maximal context.

## Motivation

The local-model constraint makes indiscriminate context accumulation expensive and often counterproductive.

The project therefore treats context as an explicit artifact produced for a specific invocation rather than as a transparent dump of everything known.

## Expected behavior

A processor should receive enough information to pursue its objective, but should not automatically inherit the full repository, the full project history, every previous processor conversation, and all persistent memory.

A processor should be able to identify missing context and request more when necessary.

## Context governance

Context governance is the broader responsibility of deciding what information becomes available, what remains hidden unless requested, what is summarized, what source material is preferred, and how context budget is allocated among competing needs.

This responsibility may eventually involve both deterministic retrieval mechanisms and AI-assisted selection.

## Why this deserves first-class treatment

If the orchestrator itself receives unlimited context, the system simply relocates the working-memory problem.

If context is too aggressively filtered, the system becomes confidently incomplete.

The quality of context selection is therefore a major determinant of the whole architecture's effectiveness.

## Open question

We do not yet know whether context governance should remain a dedicated subsystem, a specialized processor role, part of orchestration, or a hybrid of all three. The concept is settled; the implementation boundary is not.
