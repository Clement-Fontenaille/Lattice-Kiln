# Decomposition

## TL;DR

Decomposition is the operation the constrained-intelligence thesis rests on, and
the one whose cost the thesis does not account for. This document holds
a candidate account of when splitting pays, marked as a sketch rather than a
settled position.

> **Motto:** Splitting is the easy half.

## Motivation

The thesis asks the system to reduce the amount of simultaneous reasoning each
invocation must perform. That is decomposition, and everything else in this set
assumes it works.

The thesis records that decomposition costs unconditionally and pays conditionally,
and that evaluating the composite is where the cost concentrates
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
— which the thesis has no account for on its own. It also matches published
work in which decomposition depth is best left to emerge from failure rather than
being set in advance (entry 9, §4).

This is retrodiction, not confirmation. It earns the account somewhere to be
worked on. It does not establish it.

## What it does not explain

**Recombination.** If the binding cost is rejoining rather than splitting, then a
grain-matching rule addresses the cheaper half of the problem. The account says
nothing about how coarse the recombining step must be, and recombination is coarse
by construction: it requires holding the objective and the parts together.

There are two shapes for how split work comes back together, and the coarseness above
falls differently under each. **Fork/join** — parts run independently of each other,
then an explicit step rejoins them, and that step is where the cost concentrates. **Continuation** is the alternative: instead of forking
into parts unaware of each other and reconciling afterward, each step hands off to
the next as an evolving single thread, carrying forward what the next step needs
directly — there is no separate join, because nothing was split into independent
branches to begin with. This does not make recombination's cost disappear; it
relocates it, folded into every handoff instead of concentrated at the end, and
whether that is cheaper is exactly as untested as the rest of this account.

**A preference, not a decision.** Continuation is the standing preference for this
project, named here precisely so it does not lose by default to fork/join's silent
assumption above rather than by argument. Nothing in this account yet justifies
preferring one over the other — both stay on the table until evidence or a sharper
argument decides between them.

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

## A second criterion: the mechanical witness

Operator ruling, 2026-09-14. The account above splits on **capacity** — until each
unit is one the assembly can hold. This is a second criterion, independent of it, and
it constrains **formulation** rather than size.

**A task is well-formed when its completion has a mechanical witness.** Where no
statement of the objective admits one, the task is at the wrong granularity, and the
response is to restate or split it.

The case that produced this is `wf3_refactor` in the evaluation suite. Its objective
reads *remove the duplication by extracting a shared helper, without changing what
either function returns*. Nothing mechanical observes that. The untouched source
passes every check and so does a correct refactor, so doing the work and not doing it
are the same observation
(`40-roadmap/03-research-and-evaluation/E0-suite-construct-validation.md`).

Restated, it has a witness immediately:

> the two functions become one, **or** each body reduces to a call into a third
> function carrying the shared logic.

That is an inspection of two function bodies. No model, no judgement.

Note the shape: **two admissible outcomes rather than one imposed.** It says what
*finished* looks like without prescribing how to get there. A criterion admitting only
one implementation has stopped being a completion test and become a specification of
method.

### Three refinements, same day

**The unit is the demand, not the check.** An earlier wording put the fault on the
check and qualified it with *clearly*, which did no work. Coverage is binary: either a
clause of the demand has a witness or it has not. Stated as the operator put it:

> A demand that is not the subject of a witness defeats the arm every time.

**Witness, not test.** A `test_task.py` case is one kind of witness. An AST walk
asking whether two function bodies reduced to calls is another; reading the source for
docstrings is a third. Saying *test* excludes by vocabulary half the repairs
available, including the one proposed for `wf3_refactor` above.

**What is defeated is the terminal, not the work.** An arm working on an unwitnessed
clause may do the job perfectly. What it cannot do is report. On `wf3_refactor` an arm
that refactors correctly reports `declined`, and an arm that does nothing reports
`declined` — the artifact may be fine either way, the self-assessment is worthless
either way. For a system whose value is honest escalation, that is the expensive loss.

**And nothing inside the system can check it.** Detecting an unwitnessed clause means
comparing a natural-language demand against what a check measures. This is a criterion
applied by a person when the work is formulated. A suite, or a task store, cannot
audit itself on it, and an implementation must not be built as though it could.


### The response to a missing witness is not a judge

Two reasons, and the first is measured rather than argued.

**This project has already tested adding one.** `50-findings/07`, the Milestone 5
follow-up, found the deterministic core alone scoring **9/10 with zero model calls**,
and a 7B checklist-and-panel added on top dropping it to **6/10**. The checklist
codified false premises as requirements and the panel emitted confident, wrong
`not_met` verdicts on correct code. Its verdict: a 7B does the *doing* with
scaffolding and **cannot do the *judging*, and the gap is not a prompt away.** The
panel's one demonstrated use was explaining a *known* failing test line — a reporting
aid, not a decision aid.

**And structurally, a judge relocates the unverifiability rather than removing it.**
Something now has to establish that the judge was right, and that is the question
that was already unanswerable.

### What is not settled

**Whether a test-writer is redundant in the same way.** The judge result does not
transfer: writing a check and judging an artifact are different operations, and `07`
found the panel useful precisely for explaining a *known* failure. Three suite tasks
carry the `kway-synth` tag for this, and blind K-way synthesis is listed among
Milestone 7's unexplored strategies. Open, and flagged as open by the operator who
gave the ruling.

### Against the account above

The capacity criterion and this one can disagree. Two units can be identical in what
an assembly can hold and opposite in whether their completion is observable.

That bears on the open question below — *whether decomposition is governed by one
quantity or two* — by naming a candidate second one on the **splitting** side, where
the existing doubt was on the recombination side.

## Open question

Whether the granularity account survives contact with a prediction that could
fail, and what replaces it if not.

Whether decomposition executes as fork/join or as continuation (What it does not
explain, Recombination, above) is unresolved and untested. Nothing in the account
itself depends on which; the recombination gap reads differently under each, and
the standing preference for continuation is not yet an argued position.

Whether decomposition and recombination are governed by one quantity or two. The
account assumes one; the observed concentration of cost in aggregation is the
reason to doubt it.

Where the decision to split should live. The orchestrator is the obvious owner,
but a rule this consequential being held by a component that is itself tunable
system configuration deserves examination rather than assumption.

What counts as the *failure* that triggers a split. The external work says depth
is best left to emerge from failed attempts (entry 9, §4) — but the same work
reports that a model judging whether its own attempt succeeded is unreliable and
biased toward "done." So the trigger cannot be the executor's self-report, and
what replaces it is unspecified. This is the same gap `10-foundations/01` names
from the other side.
