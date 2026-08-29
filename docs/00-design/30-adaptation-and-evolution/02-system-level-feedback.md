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

## Candidate changes

System-level changes should normally create candidate system variants.

They should not silently rewrite the trusted running configuration.

This keeps experimentation distinct from promotion.

## Evidence requirement

A system-level change should be justified by behavior across enough tasks or projects to support the claim that the issue is systemic.

The exact threshold is an empirical matter.

## Open question

The project must eventually determine how system-level feedback distinguishes a genuine general weakness from overfitting to one benchmark, one repository type, or one model family.
