# Ephemeral Conversation and Curated Memory

## TL;DR

Temporary discussion supports reasoning. Persistent memory should be deliberate.

> **Motto:** Conversation is working memory; knowledge is a published result.

## Motivation

Long-lived agent conversations accumulate stale assumptions, irrelevant history, and unexamined conclusions.

The project instead favors short-lived processor instances and bounded discussions whose useful results can be promoted into persistent knowledge.

## Ephemeral interaction

A processor may discuss a question with the orchestrator, ask for additional evidence, receive another processor's challenge, or revise its conclusion.

That conversational history is useful while the reasoning episode is active.

It does not automatically deserve long-term persistence.

## Collapsing

An attempted argument (`10-foundations/03-evidence-belief-and-provenance.md`) that gets superseded before it is ever promoted does not need the treatment a promoted claim gets when it is corrected. Qualification and the open-contract convention (`03`, Friction and re-evaluation) exist because a promoted claim may already have been relied on elsewhere, and erasing that history would hide from a later reader that something once stood, was used, and changed. An ephemeral revision within the same active reasoning episode has no such history to protect — nothing outside the episode has cited it, built on it, or could be misled by its disappearance. It **collapses**: the superseded step and the conclusion that replaced it resolve to the settled state alone, with no visible trail, because none is owed.

This is what "revise its conclusion," above, actually means for something that never left working memory. The line it draws is the one `03` does not: not every attempted argument a walk forms belongs in Provenance. Most of a reasoning episode's internal churn collapses before it would ever reach that question; only what survives to be checked, held, and used by something else earns a souvenir instead of disappearing.

## Curated memory

Persistent memory should contain information expected to remain useful beyond the current interaction.

The system should preserve scope, provenance, confidence, and evidence when practical.

Project memory and system memory are conceptually distinct because a repository convention should not silently become a global processor instruction.

## Expected consequence

Fresh processor instances can begin from curated knowledge rather than inherited conversational baggage.

This supports both constrained context and independent reassessment.

## Open question

Contradiction before promotion collapses (above); contradiction after promotion is `03`'s qualification and open contract. The rules governing promotion itself, aging, and retirement remain intentionally unresolved and should be refined after observing real project behavior.
