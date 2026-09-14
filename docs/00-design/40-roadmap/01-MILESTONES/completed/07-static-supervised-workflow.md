# M7 — Static supervised workflow

**State:** **complete, 2026-09-14.**
**Findings:** [entry 10](../../../50-findings/10-m7-static-workflow.md) — confirms narrowly
**Execution record:** [`M7-static-workflow.md`](../../../../50-PROGRESS/M7-static-workflow.md)
**Artifacts:** `experiments/M7-static-workflow/`;
`experiments/M6-evaluation-suite/results/m7.{json,md}`

## What it answered

24/30 on the suite, 1 regression, 5/5 decline accuracy. The same score as `dloop`,
with four tasks flipped between them and none of the four touched by the stages M7
added — so the headline result is about the **instrument** rather than the workflow:
the suite at N=1 cannot resolve a one-or-two-task difference.

Making the premise audit **advisory** is the one clean confirmation: `staged`'s seven
false declines became one, and that one was predicted in advance as inherited from
`dloop`.

The run also found that the incumbent-protected keeper **protects a subtest count
rather than the set of passing checks**, which no earlier arm could find because no
earlier arm made enough progress to have something to trade.

**Specification:** [`10-technical/11-static-workflow.md`](../../../../10-technical/11-static-workflow.md) — v0, back half only; front half carried as an open contract there
**Depends on:** [M6](06-evaluation-task-suite.md) (the ruler), [M3](../03-invariant-floor.md) (the floor it sits on)
**Evaluated against:** [`10-evaluation-task-suite.md`](../../../../10-technical/10-evaluation-task-suite.md)

## What this milestone is

The M5 follow-up established the near-term deliverable: a **supervised local
assistant on 7–8B**, not a self-improving loop. It also produced a **leading
candidate** for the shape — but this milestone is deliberately kept open about
strategy, because the evidence behind that candidate was 6 tasks at low N, and the
[M6](06-evaluation-task-suite.md) suite exists precisely to test these
choices at scale.

This milestone turns the chosen strategy into a specified, observable component on
the M3 floor: the flow, the per-stage contract, the firing rules, the escalation
payload, and per-stage outcome-influence observability.

## Evidence question

On the M6 suite, which workflow strategy gives the best outcome-per-call against
the plain monolith and the always-on super-pipeline, and does the chosen one
degrade safely — no regressions, honest escalation — on the tasks it cannot do?

## What M6 already settled

Three facts arrived from the suite before this milestone started building, and
they narrow it considerably:

- **The spine is `dloop`** — test-gated iteration, incumbent-protected keeper,
  escalate-on-stall. 24/30, **0 regressions**, 5/5 correct declines, at 1–4
  calls/task.
- **Premise audit must be advisory, not a hard decline gate.** As a gate it
  false-declined roughly 20% of the suite (`hf_csv`, `hf_json_field`, …) and drove
  the staged arm *below* the plain spine.
- **Concern-split fires conditionally**, on genuine multi-concern objectives. It
  took `wf6` from 2/6 to 6/6 but cost 252 s and helps around two tasks in thirty.

Also **dropped** on evidence, from the super-pipeline: dual implementation specs,
the alignment check, and blind test synthesis as built — four stages that changed
zero outcomes in twelve runs.

And **fixed before reuse**: no plan injected into the implementer context; plain
framing for greenfield; no lone model probe may flip a terminal.

## The proposed front half

`dloop` is the back half and is settled. The front half is a **proposal, not a
position**: convergence before implementation, with a **task-scaled artifact** —
standardise the step, vary the artifact by task, and escalate the artifact on
failure to converge rather than classifying its form upfront.

Origin: [`70-THINKING/01-use-cases.md`](../../../../70-THINKING/01-use-cases.md) P8.
It is exploratory material and nothing load-bearing rests on it yet.

Three things it needs before it can be specified:

1. **A cheap detector for *not converged***, which doubles as the escalation
   trigger.
2. **A decision on what the cheapest artifact is *for*.**
3. **An answer to the fact that convergence closes on nothing.** `dloop` closes on
   a test; nothing validates the artifact.

The third is
[`10-foundations/04`](../../../10-foundations/04-context-as-governed-resource.md)'s
context-quality question, which makes **[M9](../09-context-governance-measurement.md)
a prerequisite for evaluating this front half** rather than a later measurement
chore. That dependency is the main open sequencing question in
[`../00-backlog.md`](../../00-backlog.md).

## Strategies still to explore, not foreclosed

- **Blind K-way test synthesis, fixed.** It was inert in the super-pipeline only
  because its suites crashed on an unfinished implementation before emitting a
  check line. A version that tolerates partial code, or runs after the first
  coding pass, may be the missing verifier for no-test tasks — the `ground_notest`
  3/10 hole.
- **Dueling advocates with executable claims.** Two context-diverse readers (one
  sees only the diff, one only the pre-change file plus the objective) emit
  *falsifiable* input/output claims; the interpreter, not a third model,
  adjudicates. Attacks the same no-test hole from the other side.
- **Cross-model / stronger-model review.** Once a second resident model is
  available (the planned second GPU), the reviewer is a different model — the one
  intervention the judge-lab said could lift evaluation above the approval bias.
  This may change how much verification machinery the workflow needs at all.
- **Task-type-adaptive stage selection.** The premise audit already classifies
  bugfix / feature / refactor / perf; the conditional-firing rules can be *learned
  from M6 `stresses`-slice data* rather than hand-set.
- **The natural-language orchestrator, reconsidered.** M5 showed its only gain was
  adaptive retry — already in the spine — at 5–7× cost, on toy tasks. Whether it
  earns its cost on the harder M6 tasks (multi-file, migration, multi-concern) is
  an open question the suite can now answer. It returns at minimum as a comparison
  arm.
- **Human-in-the-loop shape.** The escalation payload — a precise, human-answerable
  question rather than a dump — is itself a design surface.

## The interaction requirement

Every handoff in this milestone is bound by the two-mode requirement from
[`10-foundations/07`](../../../10-foundations/07-the-integrated-system-and-its-operator.md):

> Ask what only the operator can answer; where the system must decide, yield with
> the reasoning that would let the decision be overturned; never present what the
> operator can only accept.

This is the general form of M5's required stop-rationale, and it applies to the
escalation payload above.

## Work remaining — none

1. ~~Specify the workflow.~~ [`10-technical/11-static-workflow.md`](../../../../10-technical/11-static-workflow.md) v0, back half. The front half stays unspecified and is an open contract there, since its third prerequisite is M9.
2. ~~Build it from the `loop_lab` / `m6_arms` parts, with premise-audit-as-advisory,
   conditional concern-split, and the `pipeline_lab` fixes.~~
   `experiments/M7-static-workflow/m7_workflow.py`.
3. ~~Run it on the M6 suite against `monolith` / `dloop` / `staged`.~~ 24/30.
4. ~~Write the findings entry.~~ [Entry 10](../../../50-findings/10-m7-static-workflow.md).

**Building it found two defects in the specification**, which is what step 2 was for:
the per-task call budget of 4 cannot survive a concern split, since that figure was
measured on an arm that never splits; and the keeper rule as written compares subtest
counts while the claim it carries is about the set of passing checks. Both are
corrected in the specification and recorded in entry 10.

Step 3 needs **E0** ([`../03-research-and-evaluation/E0-suite-construct-validation.md`](../../03-research-and-evaluation/E0-suite-construct-validation.md))
for the comparison to be interpretable, and E0 is possibly answerable from runs
already recorded.

**Step 3 also has a deadline nothing else records.**
[M17](../17-mandate-chain.md) puts a model call in front of every tool call, and this
milestone's evidence question is **outcome-per-call**, measured against arms that are
comparable back to M4 and M5. Once the scope check is on the effect path, every arm
pays a cost no earlier arm paid and the axis stops meaning what it meant. So this
run completes before M17 lands, or it runs with the check disabled and the findings
entry says which.

Per-stage outcome-influence observability is not step 5. It is a property of
step 2, because the whole point is that **redundant stages retire on evidence** —
and a stage whose influence was never recorded cannot be retired on anything.
