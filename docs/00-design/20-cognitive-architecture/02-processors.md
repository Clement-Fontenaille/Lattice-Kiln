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

These examples are not a taxonomy, and no list written now is expected to be complete. The set of roles is itself a subject of system-level feedback: where recurring evidence shows a weakness no existing role is shaped to address, a new role may be commissioned and evaluated like any other candidate change.

The role vocabulary is therefore expected to grow through evidence rather than to be enumerated in advance. Two consequences follow. Roles fixed outside that mechanism — such as those belonging to invariant enforcement — are deliberate exceptions and are specified where the invariant layer is specified, not here. And because the vocabulary is open, operational constraint cannot be expressed in terms of it; that is why the invariant gate binds effects rather than roles.

## Independence

Independent processors should sometimes receive conclusions without inheriting the full reasoning history that produced them.

This allows adversarial reassessment and reduces the risk that one early mistake dominates every later step.

## Discussion

Processors may participate in short discussions mediated by the orchestrator.

A processor may challenge another processor's conclusion or request a new investigation.

The system should treat disagreement as potentially useful evidence rather than as a failure to converge quickly.

## First evidence (Milestone 4)

A small experiment (findings-log entry 5) compared a monolithic implementer
against a fixed planner → implementer → reviewer chain **with no revision loop**,
on a 7B model with deliberately naive context. The ephemeral split did not beat
the monolith on objective task success (5/8 vs 6/8; an earlier pass 4/4 vs 3/4)
and cost roughly 3× the model calls and wall-clock. Independent review often
identified failures correctly but, lacking a feedback edge back to the
implementer, was recorded and then ignored.

This weakens — it does not refute — the "ephemeral roles improve reasoning
quality" hypothesis at small scale. The reading the evidence supports: the value,
if any, is unlikely to come from role separation alone; it needs the
reviewer→implementer revision loop and better context assembly. One separate
positive did hold cleanly: both arms reliably **declined** a task built on a
false premise rather than implementing it.

## Open question

We still need to learn how specialized roles should be, how much context they should share, and whether model diversity provides enough benefit to justify additional runtime complexity.

Milestone 4 adds a specific form of this: does a planner → implementer → reviewer
chain need a revision loop before role separation pays for its overhead, and is
that better studied under the Milestone 5 orchestrator than as a fixed chain?
