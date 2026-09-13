# M7 — Static supervised workflow

**State:** **in execution.** Kept open on strategy.
**Specification:** [`10-technical/11-static-workflow.md`](../../../10-technical/11-static-workflow.md) — **v0 written, back half only; front half carried as an open contract there**
**Execution record:** `50-PROGRESS/M7-static-workflow.md` — **owed** (moves to `archives/` on completion)
**Depends on:** [M6](completed/06-evaluation-task-suite.md) (the ruler), [M3](03-invariant-floor.md) (the floor it sits on)
**Evaluated against:** [`10-evaluation-task-suite.md`](../../../10-technical/10-evaluation-task-suite.md)

## What this milestone is

The M5 follow-up established the near-term deliverable: a **supervised local
assistant on 7–8B**, not a self-improving loop. It also produced a **leading
candidate** for the shape — but this milestone is deliberately kept open about
strategy, because the evidence behind that candidate was 6 tasks at low N, and the
[M6](completed/06-evaluation-task-suite.md) suite exists precisely to test these
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

Origin: [`70-THINKING/01-use-cases.md`](../../../70-THINKING/01-use-cases.md) P8.
It is exploratory material and nothing load-bearing rests on it yet.

Three things it needs before it can be specified:

1. **A cheap detector for *not converged***, which doubles as the escalation
   trigger.
2. **A decision on what the cheapest artifact is *for*.**
3. **An answer to the fact that convergence closes on nothing.** `dloop` closes on
   a test; nothing validates the artifact.

The third is
[`10-foundations/04`](../../10-foundations/04-context-as-governed-resource.md)'s
context-quality question, which makes **[M9](09-context-governance-measurement.md)
a prerequisite for evaluating this front half** rather than a later measurement
chore. That dependency is the main open sequencing question in
[`../00-backlog.md`](../00-backlog.md).

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
[`10-foundations/07`](../../10-foundations/07-the-integrated-system-and-its-operator.md):

> Ask what only the operator can answer; where the system must decide, yield with
> the reasoning that would let the decision be overturned; never present what the
> operator can only accept.

This is the general form of M5's required stop-rationale, and it applies to the
escalation payload above.

## Work remaining

1. ~~Specify the workflow.~~ **Done** — [`10-technical/11-static-workflow.md`](../../../10-technical/11-static-workflow.md) v0, back half. The front half stays unspecified and is an open contract there, since its third prerequisite is M9.
2. Build it from the `loop_lab` / `m6_arms` parts, with premise-audit-as-advisory,
   conditional concern-split, and the `pipeline_lab` fixes.
3. Run it on the M6 suite against `monolith` / `dloop` / `staged`.
4. Write the findings entry.

Per-stage outcome-influence observability is not step 5. It is a property of
step 2, because the whole point is that **redundant stages retire on evidence** —
and a stage whose influence was never recorded cannot be retired on anything.
