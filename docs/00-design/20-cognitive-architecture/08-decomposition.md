# Decomposition

## TL;DR

Decomposition is the operation the constrained-intelligence thesis rests on, and
the one whose cost the thesis did not originally account for. This document holds
a candidate account of when splitting pays, marked as a sketch rather than a
settled position.

> **Motto:** Splitting is the easy half.

## Motivation

The thesis asks the system to reduce the amount of simultaneous reasoning each
invocation must perform. That is decomposition, and everything else in this set
assumes it works.

The thesis also now records that decomposition costs unconditionally and pays
conditionally, and that evaluating the composite is where the cost concentrates
(`10-foundations/01`). Neither the orchestrator nor the processor document says
how the decision to split is made. The orchestrator lists decomposition among the
operations it may select and offers no rule for selecting it, which leaves the
architecture's central operation unspecified at exactly the point the evidence
says it matters.

## A candidate account

What varies with the capability of an assembly may be principally the
**granularity at which relevant context can be accounted for** — the coarsest
unit it can integrate correctly, below which it works and above which it produces
fluent output uncorrelated with the truth.

Under that reading there are no separate faculties. Doing, judging, planning and
investigating are the same operation at different grains, and **decomposition is
grain-matching**: split until each unit is one the assembly can hold.

## Status of this account

**A lens, not a theory.** It was assembled to explain observations already in
hand, and it has not yet made a prediction that could fail. It is recorded here
because it is the only account currently on offer that yields a *rule* rather
than a heuristic, and because leaving the architecture's central operation without
any account is worse than holding a provisional one that is labelled as such.

Two things it would need before it is treated as more than that. A definition of
granularity that does not permit any failure to be relabelled "above the ceiling"
after the fact. And a prediction that can lose — the nearest candidate being
whether the same information at a coarser grain outperforms it at a finer one with
quantity held constant, which nobody appears to have tested.

## Its first result

The account's one non-trivial consequence, and the reason to keep it: it predicts
that orchestration overhead exceeds benefit exactly when a unit is split below
what the assembly could already hold.

That matches what has been observed — a fixed chain losing to a single pass, a
splitting stage bought at high cost for narrow benefit (findings entries 5 and 8)
— which the thesis previously had no account for at all. It also matches published
work in which decomposition depth is best left to emerge from failure rather than
being set in advance (entry 9, §4).

This is retrodiction, not confirmation. It earns the account somewhere to be
worked on. It does not establish it.

## What it does not explain

**Recombination.** If the binding cost is rejoining rather than splitting, then a
grain-matching rule addresses the cheaper half of the problem. The account says
nothing about how coarse the recombining step must be, and recombination is coarse
by construction: it requires holding the objective and the parts together.

**Objective preservation.** Parts can meet their own criteria and miss what was
asked, each having acquired a local target in place of the goal. Matching grain
says nothing about preserving intent, and a rule that only matched grain would
produce this failure readily.

Both gaps sit on the same side: the account describes how to cut and is silent on
how to close.

## Consequences if it holds

Stated so that they can be recognised as wrong later.

The orchestrator's decomposition decision becomes a **comparison** — demand
against what the assembly can hold — rather than a classification of task type.
Depth follows from that comparison rather than being configured. And the firing
rule for any heavier stage is conditioned on the same quantity, which would let
redundant stages retire on evidence rather than on judgement.

## Open question

Whether the granularity account survives contact with a prediction that could
fail, and what replaces it if not.

Whether decomposition and recombination are governed by one quantity or two. The
account assumes one; the observed concentration of cost in aggregation is the
reason to doubt it.

Where the decision to split should live. The orchestrator is the obvious owner,
but a rule this consequential being held by a component that is itself tunable
system configuration deserves examination rather than assumption.
