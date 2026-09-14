# Static Supervised Workflow

**Traces to:** `00-design/40-roadmap/01-MILESTONES/completed/07-static-supervised-workflow.md`, `00-design/22-arch-cognition/02-processors.md`, `00-design/22-arch-cognition/08-decomposition.md`, `00-design/10-foundations/07-the-integrated-system-and-its-operator.md`
**Exercised by:** `experiments/M7-static-workflow/m7_workflow.py`; findings-log entry 10
**Consumes:** `06-processor-contract.md`, `02-observability-event-model.md`, `04-enforcement-gate.md`, `10-evaluation-task-suite.md`
**Evaluated against:** `10-evaluation-task-suite.md`

## TL;DR

A fixed, non-adaptive workflow for supervised local assistance on a 7–8B model: a
test-gated iteration loop with an incumbent-protected keeper, escalate-on-stall, an
advisory premise audit, and a conditionally-firing concern split. The stage sequence
is fixed; only the firing conditions vary.

> **Motto:** Fixed stages, conditional firing, honest escalation.

## Status of this document

**v0 — the back half only.** The loop, its gates, its keeper and its escalation are
specified here because Milestone 6 measured them against alternatives on thirty tasks.

The **front half is deliberately not specified** and is carried as an open contract
below. Convergence-before-implementation is a proposal rather than a position, it
rests on six tasks at low N, and the third of its three prerequisites is
`10-foundations/04`'s context-quality question — which makes Milestone 9 a
prerequisite for *evaluating* it rather than a later measurement chore. Specifying it
now would be specifying against a ruler nobody has.

## Responsibility

Fix the stage sequence, the per-stage contract, the firing rules, the keeper rule,
the escalation payload, and what each stage must record for its influence on the
outcome to be recoverable.

It does **not** define processor structure (`06-processor-contract.md`), effect
typing (`01-effect-vocabulary.md`), what the suite measures
(`10-evaluation-task-suite.md`), or any adaptive strategy — this workflow is static
by construction, and comparing it against an adaptive orchestrator is what the suite
run is for.

## Why static

Milestone 5 found an LLM orchestrator's only gain over a monolith was **adaptive
retry**, at roughly five times the model calls. Milestone 6 then found that
test-gated iteration — the same retry behaviour, without a model deciding when to
retry — reaches 24/30 with **zero regressions** at one to four calls per task.

The adaptive part was doing the work; the deciding was not. A static workflow keeps
the first and drops the second, and the orchestrator returns as a comparison arm
rather than as the spine.

## The stages

Four, in fixed order. Two always fire; two fire on condition.

### 1. Premise audit — always fires, **advisory only**

Reads the objective and the pre-existing state, and emits a classification
(`bugfix` / `feature` / `refactor` / `perf`) plus any premise concern it finds.

**It may not decline.** As a hard gate it false-declined roughly 20% of the suite and
drove the staged arm below the plain spine — the single clearest negative result
Milestone 6 produced. Its output is advisory input to later stages and to the
escalation payload, and nothing terminal may rest on it alone.

MUST record: classification, concerns raised, and whether any later stage consumed
them. A stage whose influence is not recorded cannot be retired on evidence.

### 2. Concern split — fires on condition

Fires only on a genuinely multi-concern objective. On `wf6` it moved 2/6 to 6/6; it
costs around 252 seconds and helps roughly two tasks in thirty.

**The firing rule is the open part**, and it is `00-design/22-arch-cognition/08`'s
question in operational form: the split should be a comparison of demand against what
the assembly can hold, not a classification of task type. v0 uses the premise audit's
classification as a stand-in trigger and records every firing decision with its
inputs, so the rule can be **learned from the suite's `stresses` slice** rather than
hand-set permanently.

**A firing signal that the stage cannot act on is a no-op, and v0 has one**
(findings-log entry 10). M7's build fired on either a syntactic signal — the objective
enumerates its parts — or the audit's `multi_concern` flag, while segmentation was
purely syntactic. When the model signal fired alone the stage fired and had nothing to
split. The two signals agreed on 29 of 30 tasks, so the model half earned nothing a
regular expression did not.

An implementation MUST either give the model signal a way to produce segments, or drop
it. Recording a firing decision the stage could not act on makes the influence record
say a stage fired when nothing happened, which is the one thing that record exists to
prevent.

When it fires, each concern becomes its own pass through stages 3 and 4, and results
recombine by continuation — each pass hands forward what the next needs — rather than
by an explicit join. What a pass hands forward follows the same rule as the retry
loop: into the objective, as a signal (`06-processor-contract.md`, Handoff framing).

### 3. Implement — always fires

One implementer instance per pass (`06-processor-contract.md`).

Three constraints carried from Milestone 6, each fixing an observed failure:

- **No plan is injected into the implementer's turn input.** Injected plans measurably
  hurt. What the retry loop hands forward instead is the failing check's own output,
  folded into the objective (`06-processor-contract.md`, Handoff framing) — a signal
  rather than a model's account of one. The premise audit's concerns are model prose
  addressed to the operator and reach the escalation payload only, never an
  implementer's objective.
- **Plain framing for greenfield.** Elaborate framing helps only where there is
  pre-existing code to respect.
- **No lone model probe may flip a terminal state.** A single model's opinion is not
  a terminal outcome; only the test gate and the escalation rule produce one.

### 4. Test gate and keeper — always fires

The loop. Run the objective check. On failure, iterate: a fresh implementer instance
with the failure recorded, bounded by the stall rule below.

**Incumbent-protected keeper.** A new attempt replaces the incumbent only if it
strictly improves the objective check **and no check that was passing has begun to
fail**. A tie keeps the incumbent. This is the rule to preserve if any other is traded
away.

**The second clause is a correction, and it is load-bearing** (findings-log entry 10).
An implementation that compares *how many* checks pass rather than *which* ones will
accept a change that fixes three and breaks one, because the count went up. That is
what M7 did on `wf6_multi`: subtests 2/6 → 5/6 while `topo cycle`, green at the start,
went red. The keeper saw 5 >= 2 and accepted.

**Do not read the earlier arms' zero regressions as evidence the count rule is safe.**
Three arms scored zero on that task for three unrelated reasons: `monolith` and `dloop`
changed nothing, so nothing could regress; `staged` fixed **every** subtest, so the set
of failures was empty and nothing could enter it. Only M7 finished in a partial
position, which is the only place the rule is actually asked to choose. **A rule is
only tested where it has to decide.** Compare sets.

### If a model verdict is ever admitted, it is task-level and never candidate-level

Both the keeper and the terminal read *the dimensions*, so "add the judge as another
dimension" is ambiguous between two designs. The difference is not cosmetic.

**Task-level.** The verdict is taken once, after the loop, and enters only the
completeness test. The keeper never sees it.

**Candidate-level.** The verdict is taken per attempt and enters the
candidate-against-incumbent comparison.

**Only the first is admissible**, on three grounds, and the third is the one that
settles it.

It **cannot fabricate a success.** A task-level verdict can withhold `answered` and
turn it into an escalation; it never causes a candidate to be accepted. That is the
direction condition `03-capability-authority-model.md` admits invariant processors on —
may restrict, never widen — so a degraded judge yields unnecessary escalation rather
than a false pass. A candidate-level verdict has the opposite property: a change that
fixes nothing but which the judge calls `met` raises the combined score by one and is
kept, on the judge's word alone. That is approval bias entering through the keeper,
and approval bias at 7B is what `50-findings/07` measured.

It **costs one call instead of up to twelve**, since a per-candidate verdict needs a
judge call per attempt.

And it **keeps the keeper mechanical.** The keeper's rule is deterministic and so are
the dimensions it compares, because they come from the check: the same candidate always
produces the same decision. Putting a model verdict into that comparison ends it. The
same candidate could be kept on one run and discarded on the next, the arm's trajectory
stops being reproducible, and no run can be replayed or explained afterwards.

**That last property is also what makes a task-level verdict measurable without being
deployed.** Since it changes no candidate, the trajectory is identical with and without
it, and the terminal can be recomputed from a recorded verdict — which is how m7d is
derived from m7c's log rather than run
(`experiments/M7-static-workflow/derive_m7d.py`). A candidate-level verdict cannot be
derived at all: there is no single trajectory to recompute.


**Escalate on stall.** Stall is a bounded, mechanical condition: no strict improvement
across *N* consecutive attempts, or the call budget is reached. v0 sets N = 2 and a
budget of 4 calls, both from Milestone 6's observed 1–4 call range.

**The budget is per pass, not per task**, and the distinction only appears once stage
2 fires. M6's 1–4 range was measured on `dloop`, which never splits; a three-concern
objective under a per-*task* budget of four would give each concern barely one
attempt, which is worse than not splitting. A task-level cap belongs alongside it to
stop a many-concern objective running away — M7's build used 12, and one task reached
11 calls and 43% of that arm's entire wall clock.

Neither number is derived from anything, and both are recorded per run so the suite
can move them.

Escalation is not failure. It is a terminal outcome with its own payload, below.

## Terminal states

Three, from `06-processor-contract.md`, kept distinct in the record:

- `answered` — the objective check passes and the keeper holds a passing artifact.
- `declined` — the work was refused on inspection. Milestone 4 found both arms
  reliably declined a false-premise task; that behaviour must survive.
- `blocked` — stalled or out of budget.

`declined` and `blocked` **MUST NOT** collapse into one outcome. Milestone 5 recorded
an orchestrator resolving both to a generic `blocked`, losing a distinction the
simpler arms had made, and that collapse is what this constraint exists to prevent.

## The escalation payload

Bound by the two-mode requirement (`00-design/10-foundations/07`): *ask what only the
operator can answer; where the system must decide, yield with the reasoning that
would let the decision be overturned; never present what the operator can only
accept.*

So an escalation is **a precise, answerable question**, not a dump. It MUST carry:

- the objective, verbatim;
- what was attempted, and what the check reported on each attempt;
- the premise audit's concerns, whether or not any stage consumed them;
- the specific question the operator is being asked, phrased so a short answer
  unblocks the work;
- for any decision the workflow took on the operator's behalf, the reasoning that
  would let it be overturned.

A payload that presents a conclusion for acceptance rather than a question for
answering does not satisfy this, however complete it is.

## Observability

Per-stage outcome influence is a property of the build rather than a later addition,
because the point of a static workflow is that **redundant stages retire on
evidence** — and a stage whose influence was never recorded cannot be retired on
anything. Four stages changed zero outcomes across twelve runs of the
super-pipeline, and that was only knowable because their outputs were recorded.

Each stage MUST emit, via `02-observability-event-model.md`:

- whether it fired, and on what condition;
- what it produced;
- whether any later stage consumed that output;
- its cost in calls and wall-clock.

The third is the one that is easy to omit and the one that makes retirement
possible.

**The record measures consumption and cannot measure value** (findings-log entry 10,
finding 6). A stage whose output is read on eight tasks may still be wrong on nine of
the eleven it produced — the M7 premise audit was, at 18% precision — and nothing in
this record says so.

So the third field answers *was this output used?* and never *was it worth using?*
**Reading consumption as value is a mistake this record invites rather than prevents**,
and the M7 run made it. A stage may be retired on a consumption count of zero; it may
never be **kept** on a non-zero one without a separate measurement of whether its
output was right.


## What this competes against

The suite run (`10-evaluation-task-suite.md`) compares this workflow against
`monolith`, `dloop` and `staged`. Read **per scenario** rather than as totals: which
tasks flip between arms carries far more than a score difference, and the arms share
a suite, so the pairing is available
(`00-design/27-arch-adaptation-and-evolution/05-experiments-and-candidate-systems.md`).

**One run per arm was adequate for the differences M6 was reporting and is not
adequate here** (findings-log entry 10). M7 and `dloop` both scored 24/30 while four
tasks flipped between them — two gained, two lost — and none of the four was a task
the added stages touched. A four-task churn is available from run-to-run variance
alone at N=1, so any comparison whose expected effect is one or two tasks needs
repetition before it means anything.

The large effects stay readable at N=1: the monolith's seven regressions and
`staged`'s seven false declines are not noise. The suite discriminates designs that
differ in kind and not designs that differ by a task.

## Open contracts

- **The front half.** Convergence before implementation, with a task-scaled artifact.
  Three things block specification: a cheap detector for *not converged* that doubles
  as the escalation trigger; a decision on what the cheapest artifact is *for*; and
  the fact that convergence closes on nothing, where the loop closes on a test.
  The third is `10-foundations/04`'s context-quality question, so **Milestone 9 gates
  evaluating this**, not merely measuring it afterwards.
- **The concern-split firing rule.** v0 triggers on the premise audit's
  classification, which `00-design/22-arch-cognition/08` argues is the wrong shape —
  demand against capacity, not task type. The suite's `stresses` slice is the
  intended source for a better rule.
- **Stall thresholds.** N = 2 and a 4-call budget are observed ranges, not derived
  values.
- **The `ground_notest` hole.** Three of ten on tasks with no test to gate on. Two
  candidate verifiers are named and neither is specified: blind K-way test synthesis
  that tolerates partial code, and dueling advocates emitting falsifiable claims that
  the interpreter adjudicates.
- **Scope checking is not wired in.** The specification side is complete —
  `03-capability-authority-model.md` carries mandate conformance whole,
  `13-work-record.md` holds the declaration, `06-processor-contract.md` binds a
  `scope` — and nothing here derives, checks or enforces one. This workflow runs
  unscoped, which `05-provisional-invariant-list.md` G4 classes as an invalidity
  rather than a shortfall. What stands in for it is that a human supervises every
  run of it.
