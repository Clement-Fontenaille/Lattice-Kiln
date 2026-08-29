# Ephemeral Role-Specific Processors

## TL;DR

Processors are disposable AI reasoning instances defined by purpose rather than by permanent identity.

> **Motto:** Give each mind a job, not a lifetime.

## Motivation

A constrained model performs better when asked to reason about a bounded objective with a focused context.

Separate processor invocations also make it possible to obtain independent assessments rather than one continuously self-confirming chain of thought.

## Processor definition

A processor is defined by natural-language role instructions, an objective, selected context, available capabilities, and interaction expectations.

The role may encourage specific reasoning habits without prescribing a universal step sequence.

Examples may eventually include assessment, investigation, planning, implementation, debugging, criticism, review, context curation, or evaluation.

These examples are not intended to form a fixed taxonomy.

## Independence

Independent processors should sometimes receive conclusions without inheriting the full reasoning history that produced them.

This allows adversarial reassessment and reduces the risk that one early mistake dominates every later step.

## Discussion

Processors may participate in short discussions mediated by the orchestrator.

A processor may challenge another processor's conclusion or request a new investigation.

The system should treat disagreement as potentially useful evidence rather than as a failure to converge quickly.

## Open question

We still need to learn how specialized roles should be, how much context they should share, and whether model diversity provides enough benefit to justify additional runtime complexity.
