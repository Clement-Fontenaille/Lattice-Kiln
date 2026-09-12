# Project-Level Feedback

## TL;DR

The first adaptive loop should make the system better at one project without pretending that project-specific lessons are universal.

> **Motto:** Learn the repository before changing the machine.

## Motivation

Repeated work in the same repository reveals conventions, architecture, dependencies, recurring failures, terminology, and local expectations.

For constrained models, preserving this knowledge can reduce repeated rediscovery and improve context selection.

## Scope

Project-level feedback primarily changes project-local knowledge and project-local guidance.

It should not casually rewrite global processor roles or system policies.

This scope is distinct from system-level and meta-level feedback in what it may change and what evidence it requires. It is not necessarily distinct in which processor performs it. The separation between the three levels belongs to invocation — scope, context, and objective — and does not imply three separate kinds of agent.

## Expected outputs

The loop may produce architectural notes, conventions, dependency knowledge, validated assumptions, project-specific warnings, useful retrieval hints, or summaries of recurring patterns.

The output should remain attributable to evidence from the project.

## Evaluation

The project loop should eventually be judged by whether later work in the same project becomes more correct, efficient, or easier to verify.

A large knowledge base is not itself evidence of success.

## Open question

The most important unresolved issue is memory quality: how to promote useful knowledge while preventing stale, redundant, or speculative entries from becoming a new source of context pollution.

Much of that question now has machinery behind it, and what remains open is narrower than this phrasing suggests. Promotion is not a side effect of a loop running — it is a proposal made by a thinking processor (`22-arch-cognition/04-thinking.md`) and checked like any other. The default for everything not promoted is removal, by reachability rather than by judgment (`22-arch-cognition/05-curation.md`), so a knowledge base does not accumulate simply because work happened. And "context pollution" has precise names: `10-foundations/04`'s Redundancy — duplicated material — and Uselessness — material that is irrelevant without duplicating anything — which are different failure modes needing different responses.

Two things genuinely stay open here. The criterion for keeping something nothing has yet cited, which `05-curation.md` leaves as a parameter because no dimension in `10-foundations/03` looks forward. And retention *within* memory over time, which is named there and not addressed.
