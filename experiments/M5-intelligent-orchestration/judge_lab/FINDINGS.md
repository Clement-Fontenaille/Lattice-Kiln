# Judge-lab — findings

**Date:** 2026-09-01
**Model:** `qwen2.5-coder:7b-instruct-q4_K_M`, 10 scenarios, 4 pipelines, ~10 min.
**Question:** can the 7B judge be rescued — by voting down the noise, by
per-clause structure, by execution grounding — enough for a feedback loop's
evaluation to sit above noise?

Scenarios (`scenarios.py`): correct / broken pairs over wf1 (cross-file),
wf2 (retry off-by-one), wf3 (refactor trap), wf4 (false premise — the *correct*
verdict is approve-the-unchanged-linear-scan), wf5 (dropped seconds unit). Each
carries a known-correct verdict. Transcripts: `runs/<scenario>.md`. Table:
`results.md`.

## Pipelines

| | what it is |
|---|---|
| **baseline** | the M5 reviewer: one call, objective + claim + files, "is it met?", K=3, majority |
| **vote** | same reviewer, K=5 @ temp 0.5, majority — "vote down the noise" |
| **ground_notest** | deterministic prechecks (parse / import / claim-vs-diff) + a model-generated checklist + one reviewer call **per checklist clause**, test output withheld — isolates the LLM structural lift for the no-tests case |
| **ground** | as `ground_notest`, but each clause call is handed the **real `test_task.py` output** as ground truth |

## Result

| pipeline | correct | note |
|---|---|---|
| baseline | **4/10** | approves 8/10 — approve-biased |
| vote | **4/10** | **verdict-identical to baseline on all 10 rows** |
| ground_notest | **3/10** | *worse* than baseline; adds escalate/false-reject noise |
| ground | **6/10** (+2 escalate) | only pipeline above baseline; the lift is the test, not the model |

Deterministic core alone — parse + import + "claim asserts a change but files are
byte-identical" + "trust the `test_task.py` exit/subtests" — scores **9/10** with
zero model calls (the 10th, wf4, needs the planner stance; see below). **Adding
the 7B checklist+panel to that core drops it to 6/10.**

## Mechanisms

**1. Voting is dead here — the errors are systematic, not random.** `vote` (K=5,
higher temp) returned the identical verdict to `baseline` (K=3) on every one of
the 10 scenarios. The 7B reviewer is not noisy around the right answer; it is
confidently and repeatably wrong in one direction (toward approval). Self
-consistency only helps zero-mean noise.

**2. The checklist step codifies false premises as requirements.** For wf4
("rewrite `find()` to O(log n)", where the linear scan is correct and the task
should be declined), the model-generated checklist was:

> 1. Implement a binary search algorithm in `search.find()`.
> 2. Ensure the method correctly identifies the target … **in a sorted array**.
> 3. The method must execute in **O(log n)** time complexity.

The panel then checked the (correct) linear scan against these, returned
`not_met` on 1–3, and the aggregate rejected it — **overriding a 5/5 passing
test**. The checklist does not extract intent; it elaborates the objective's
surface into a spec, false premises included. This is the census `criteria_first`
pathology, confirmed and generalised.

**3. The panel is a decent failure *explainer*, not a judge.** Given the real
failing line `staff messy input unrounded: got 1.25 want 1.2536` (wf3_trap,
`ground`), the panel attached that exact line as evidence to 4/5 clauses and
correctly returned `needs-change` — the one clean win over baseline that used the
model. Withhold the test (`ground_notest`) and the same scenario collapses to
5×`unsure` → escalate: "the submission does not provide any test output to
verify…". It knows it cannot evaluate `staff_price(1.567)` by reading code, and
says so.

**4. The panel emits confident-wrong `not_met` on correct code.** wf2_correct
(passes 5/5): the panel rejected "when `retries=0`, make a single attempt" with
"it retries up to `retries + 1` times, which is 3 times when `retries=0`" — the
7B miscounts `range(0 + 1)`. So the panel does not merely over-escalate; it
actively contradicts a green test on arithmetic it gets wrong.

**5. wf4 defeats every pipeline** (baseline, vote, ground_notest, ground all
MISS). The doer implements the false premise (census: 3/3), the judge checklist
codifies it, the panel enforces it. The **only** stance in either experiment that
caught it is the **planner** (census `plan_false_premise`: 2/3 flagged the
unsorted precondition).

## Consequence: the judgment seat on a 7B

Not "tune the reviewer prompt". The composition that the evidence supports:

1. **Deterministic gate first** — does it parse, import, and change anything the
   claim says it changed; then **run the test and trust the result**. This is the
   9/10.
2. **No test? Escalate to a human.** Do not let the model stand in — `ground_notest`
   is 3/10 and its failures are confident, not hedged.
3. **The model's role near judgment is narrow and post-hoc:** given a *known*
   failing test line, draft the explanation and the retry hint. Never let a model
   `not_met` override a green test.
4. **Premise-soundness is a planner-pass concern**, upstream of implementation —
   the one place the 7B's critical read is live.

This is the M5 recalibration made concrete: a 7B does the *doing* with scaffolding
and cannot do the *judging*, and the gap is not a prompt away. It is the input to
whether the self-improving loop waits on a second resident model (a
reasoning-distill reviewer, enabled by the planned second GPU) or on the model
tier improving.
