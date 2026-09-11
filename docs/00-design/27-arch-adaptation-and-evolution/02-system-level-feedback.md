# System-Level Feedback

## TL;DR

When failures recur across work, the system should be able to question its own workflow rather than storing more project notes.

> **Motto:** Repeated local pain may reveal a global design flaw.

## Motivation

Some weaknesses are not repository-specific.

A processor may routinely miss dependencies. The orchestrator may over-investigate trivial work. A context policy may consistently omit tests. A reviewer may identify defects only after expensive implementation cycles.

These patterns belong to system-level analysis.

## Object of adaptation

System-level feedback may propose changes to processor definitions, orchestrator instructions, delegation behavior, context policy, review strategy, evaluation roles, or other cognitive workflow configuration.

It may also propose a role that does not yet exist.

## Commissioning new roles

The system's vocabulary of cognitive roles is not fixed at design time. If recurring evidence shows a weakness that no existing role is shaped to address, system-level feedback may commission a new one — a context curator, a diagnostic specialist for a recurring class of test failure, a dependency analyst.

This requires no machinery beyond what is already defined. Proposing a role is a cognitive act: cheap, reversible, and non-authoritative. Instantiating it with real capabilities is a runtime effect, gated by the existing capability and authority split. Its justification and promotion follow the existing experiment and candidate-system path. Its lineage is recorded like any other promoted change.

The default assumption should nonetheless remain reuse of an existing role at a new scope. A new role is warranted when evidence shows an existing role genuinely cannot serve the need, not merely because a familiar pattern has recurred at a new level.

Role commissioning does not weaken the invariant layer. A commissioned role inherits no exemption from enforcement, because the enforcement gate binds effects rather than roles.

## Candidate changes

System-level changes should normally create candidate system variants.

They should not silently rewrite the trusted running configuration.

This keeps experimentation distinct from promotion.

## Scope, not identity

This level is distinct from project-level and meta-level feedback in what it may change and what evidence it requires. It is not necessarily distinct in which processor performs it. The separation belongs to invocation — scope, context, and objective — and does not imply three separate kinds of agent.

## Evidence requirement

A system-level change should be justified by behavior across enough tasks or projects to support the claim that the issue is systemic.

The exact threshold is an empirical matter.

## Open question

The project must eventually determine how system-level feedback distinguishes a genuine general weakness from overfitting to one benchmark, one repository type, or one model family.

Commissioning a role changes the system's cognitive shape more than tuning an existing one does, and probably deserves a higher evidence bar. What distinguishes the two thresholds is unresolved.
