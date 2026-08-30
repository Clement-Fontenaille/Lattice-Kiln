# AI Development System — Technical Specification Set

## Purpose of this set

This set turns the converged concepts in `00-design` into contracts precise enough to implement from: responsibilities, inputs, outputs, authority, failure modes, and the relationships between components, stated without relying on phrases like "the AI handles it."

It does not restate the conceptual motivation. Each specification document traces back to the design document that justifies it, and the design set remains the place to challenge whether a concept should exist at all.

> **Motto:** Specify the seams, not the substance twice.

## Relationship to the design set

The design set is a working hypothesis and expects revision. The specification set inherits that posture: a specification is only as settled as the concept beneath it, and several concepts are explicitly not ready to specify yet.

When an experiment contradicts a specified contract, the correction flows back to the design document first, then forward into the specification. Specifications are not permitted to quietly accumulate semantics the design set never sanctioned — that is the exact failure the documentation philosophy exists to prevent.

## What is ready to specify

A concept is ready when its responsibility, inputs, outputs, authority, failure modes, and relationships can be described concretely.

Which contracts get written, and in what order, is not decided here. It follows the milestone sequence: the backlog is always the contracts the current and next milestone need, and the ordered near-term list lives in `00-design/00-project/04-execution-cadence.md`. A specification document must not be written for a milestone beyond the next one.

The **effect vocabulary** is specified first because the enforcement gate, the capability model, and observability all bind to it.

Areas deliberately deferred until concepts settle or milestones produce evidence: memory promotion and retirement, context-quality metrics, the operational safety response beyond the deny-list gate, and generation packaging.

## What this set does not decide

Storage formats, programming languages, message schemas, databases, runtime APIs, and wire protocols are out of scope until a contract or an experiment forces the choice. Where a document must name a concrete shape to stay unambiguous, it marks that shape as illustrative rather than normative.

## Conventions

`00-specification-conventions.md` defines document structure, normative language, traceability tags, and the meaning of an open contract. Read it before adding to this set.
