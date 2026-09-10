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

Curated memory is what survives Collapsing: a claim that was checked, held as a demonstration step, and judged worth keeping as a souvenir (`03`) rather than left to disappear with the episode that produced it — because something outside that episode, a later walk or a fresh processor instance, is expected to need it again.

That expectation is a different question from the one Pertinence (`03`, Weighing claims) already answers. Pertinence asks whether a claim matters to the comparison in front of it, now. Curation asks whether it is likely to matter to a comparison that has not happened yet — which Weighing claims cannot run, because there is no next claim yet to compare against. None of `03`'s three dimensions is stated to look forward this way.

The system should preserve scope, provenance, and reliability when practical. All three now have precise homes in `03`, named exactly that — scope is the one property `03` says cannot be recovered later no matter how the rest of a claim's provenance is kept (`03`, Scope). What `03` does not settle is the cost of attempting it here: under-assessing scope lets a claim silently get used outside where it actually holds (`50-findings/09`'s domain-transfer caveats are this cost already being paid by hand); over-assessing it chases a completeness `03` already says no record of this kind can reach. Managing that tradeoff, for whatever is being curated, is curated memory's job.

Project memory and system memory are conceptually distinct for the reason `30-adaptation-and-evolution/01-project-level-feedback.md` and `02-system-level-feedback.md` already give, not a new one: what evidence justifies a change differs by scope, and a repository convention should not silently become a global processor instruction.

## Expected consequence

Collapsing does more than avoid clutter: it keeps scope-assessment cheap by keeping it rare. Most of a reasoning episode's churn never reaches curated memory at all, so the expensive, necessarily-imperfect work of assessing a claim's scope (`03`, Scope) only has to be spent on what survives to be curated, not on everything a walk tried along the way.

A fresh processor instance beginning from curated knowledge, when it re-derives rather than simply trusts what it is given, is running exactly the check Convergence and Friction (`03`) exist for: independent agreement corroborates, independent disagreement is friction and forces re-evaluation. Independent reassessment was already named as a benefit here; it can now be named as what it actually is.

## Open question

Contradiction before promotion collapses (above); contradiction after promotion is `03`'s qualification and open contract. The rules governing promotion itself, aging, and retirement remain intentionally unresolved and should be refined after observing real project behavior. Scope now has a home (`03`, Scope) and a stated reason it cannot be recovered later; what stays open here is only the cost tradeoff itself — how much assessment effort is worth spending, and how that should vary with what is being curated.
