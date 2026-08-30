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

## How the implementation boundary will be decided

Context governance could plausibly live in a dedicated subsystem, a specialized processor role, the orchestrator, or some hybrid.

This set deliberately does not choose. The boundary is left to be discovered per generation, per project, or per hardware profile, by the same mechanism that governs every other system-level weakness: if recurring evidence shows that generalist processors or the orchestrator assemble context poorly, system-level feedback may commission a context-curator role as a candidate change, evaluated and promoted or discarded like any other.

Choosing now would settle by intuition what should be settled by evidence, and would settle it identically for every environment the system might run in.

## A naive default is still required

Deferring the design does not defer the need for a starting behavior.

The system needs some unglamorous, possibly poor, context-assembly behavior on day one. Without it there is no baseline against which a proposed curator's benefit could be measured, and the commissioning decision becomes unevidenced.

The first milestone concerned with context is therefore not "design context governance." It is "establish the naive default and enough measurement to make the commissioning decision answerable."

## Open question

How context quality should be measured independently of final task success, since without that measurement the commissioning decision above cannot be made on evidence.

Whether a context curator, once commissioned, becomes a bottleneck or a source of systematic blindness — and how that would be detected.
