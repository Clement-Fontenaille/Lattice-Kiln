# AI Development System — Technical Specification Set

## Purpose of this set

This set turns the converged concepts in `00-design` into contracts precise enough to implement from: responsibilities, inputs, outputs, authority, failure modes, and the relationships between components, stated without relying on phrases like "the AI handles it."

It does not restate the conceptual motivation. Each specification document traces back to the design document that justifies it, and the design set remains the place to challenge whether a concept should exist at all.

> **Motto:** Specify the seams, not the substance twice.

## Relationship to the design set

The design set is a working hypothesis and expects revision. The specification set inherits that posture — not by holding its contracts more loosely, but by holding all of them revisable on the same terms: **a finding may overturn any point in either set, technical contract through foundational concept.** A specification is not weaker than the concept beneath it; it is exposed to the same evidence.

When an experiment contradicts a specified contract, the correction flows back to the design document first, then forward into the specification. Specifications are not permitted to quietly accumulate semantics the design set never sanctioned — that is the exact failure the documentation philosophy exists to prevent.

## What is ready to specify

A concept is ready when its responsibility, inputs, outputs, authority, failure modes, and relationships can be described concretely.

Which contracts get written, and in what order, is not decided here. The owed contracts sit in P0 of `00-design/40-roadmap/00-backlog.md`; how that band is maintained is in `00-design/40-roadmap/README.md`.

**A contract may be written for any milestone.** Where the evidence is thin, the document names the seams and parks the rest as open contracts — the mechanism this set already requires everywhere. What waits is *building*, not writing: the execution gates are in `00-design/00-project/04-execution-cadence.md`. Writing early is how a later finding gets something to contradict, which is what turns stopping mid-experiment into a decision rather than a loss of nerve.

Writing early does not make a contract weaker. **Every document in this set is authoritative, and every one is revisable on findings** — see `00-specification-conventions.md` → authority and revision. A contract written ahead simply has no findings behind it yet, which makes it cheap to overturn without making it optional to honour.

Milestone numbers in this set are **stable identifiers** — allocated on creation, never reordered. Every reference here was corrected to the current numbering on 2026-09-05; before that date the same number could mean two different milestones depending on the file. See `00-design/40-roadmap/01-MILESTONES/README.md`.

The **effect vocabulary** is specified first because the enforcement gate, the capability model, and observability all bind to it.

Areas deliberately deferred until concepts settle or milestones produce evidence: memory promotion and retirement, context-quality metrics, the operational safety response beyond the deny-list gate, and generation packaging.

## What this set does not decide

Storage formats, programming languages, message schemas, databases, runtime APIs, and wire protocols are out of scope until a contract or an experiment forces the choice. Where a document must name a concrete shape to stay unambiguous, it marks that shape as illustrative rather than normative.

## Conventions

`00-specification-conventions.md` defines document structure, normative language, traceability tags, and the meaning of an open contract. Read it before adding to this set.
