# 13 — A live judge against a dead one, on one model

**Subject:** `nemotron-gpu` (NVIDIA Nemotron Nano 9B v2, Q4_K_L, `num_gpu 99`)
**Recorded:** 2026-09-18 / 2026-09-19
**Artifacts:** `experiments/M6-evaluation-suite/results_nemotron/` (judge dead),
`experiments/M6-evaluation-suite/results_nemotron_nothink/` (judge alive),
`experiments/M7-static-workflow/stage_influence_*.jsonl`
**Metric:** `objective_pass` under the 2026-09-18 ruling, floor-adjusted — the six
tasks `baseline` passes are excluded, leaving 28 earned.
**Scope:** six arms, N=1. `think` sweep not yet run.

## How the comparison arose

The 2026-09-18 sweep ran with this model's premise-audit and judge stages
returning the empty string on every call: a reasoning model consumed the
200-token cap inside its thinking block and never reached an answer
(`50-findings/12`, addenda 1 and 2). Setting `think=false` and flooring
`num_predict` at 400 repaired it.

Parse rates, same arms, same model:

| arm | audit, judge dead | audit, judge alive | judge, dead | judge, alive |
|---|---|---|---|---|
| `judge_anchored` | 0/34 | **32/34** | 0/34 | **34/34** |
| `judge_bypass` | 0/34 | **33/34** | 0/34 | **33/34** |
| `judge_caveat` | 0/34 | **33/34** | 0/34 | **34/34** |
| `judge_fullctx` | 0/34 | **34/34** | 0/34 | **34/34** |
| `test_synth` | 0/34 | **34/34** | — | — |

So the two sweeps are the same model on the same arms with the judging stages
off and then on. That was not the intended experiment; it is what the defect
produced.

## Result: the score falls in four arms of six

Earned tasks, out of 28:

| arm | judge dead | judge alive | change |
|---|---|---|---|
| `judge_caveat` | 21 | 13 | **−8** |
| `judge_anchored` | 18 | 14 | **−4** |
| `test_synth` | 17 | 15 | −2 |
| `judge_bypass` | 15 | 13 | −2 |
| `monolith` | 13 | 14 | +1 |
| `judge_fullctx` | 15 | 17 | +2 |

`monolith` makes one model call and has no audit or judge stage. It moves by +1.

## The live judge rejects work the check has already passed

Candidates whose deterministic check was already full, and what the judge said
about them:

| arm | judge dead | judge alive |
|---|---|---|
| `judge_anchored` | 0 of 20 rejected | **15 of 54 rejected (28%)** |
| `judge_bypass` | 0 of 15 rejected | **17 of 55 rejected (31%)** |
| `judge_caveat` | 0 of 18 rejected | **9 of 42 rejected (21%)** |

A dead judge rejects nothing because it returns nothing. A live one rejects
roughly a quarter to a third of candidates that had already satisfied the check.

Each rejection folds an instruction into the next attempt and fires a retry:

| arm | | median calls | `not_met` verdicts | median wall |
|---|---|---|---|---|
| `judge_caveat` | dead | 6.0 | 0/60 | 67.6 s |
| | alive | 8.0 | 46/114 | 70.5 s |
| `judge_anchored` | dead | 4.0 | 0/58 | 57.3 s |
| | alive | 8.0 | 40/120 | 74.7 s |
| `judge_bypass` | dead | 4.0 | 0/62 | 55.0 s |
| | alive | **11.0** | 45/127 | 95.8 s |

The terminal distribution moves accordingly — `judge_caveat` goes from
`answered` 18 / `blocked-no-progress` 6 to `answered` 13 /
`blocked-no-progress` 9.

## Two explanations ruled out

**It is not budget exhaustion.** `TASK_WALL_CAP_S` is 600. Runs at or above
170 s: judge-dead 8–12 per arm, judge-alive 1–2. The condition with a live judge
makes *more* calls and spends *less* wall time per task, because its calls carry
no reasoning tokens. Nothing approaches the cap in either condition.

**It is not damage to the work.** Comparing the check's combined dimension score
before and after, across both conditions and all three arms: **zero runs end
worse than they started.** What changes is how many reach full marks — 18/17/21
improving with the judge dead against 17/16/18 with it alive.

So the retry loop is not breaking code. It is declining to accept code that
passes, retrying, and ending `blocked` where the first attempt would have stood.

## Relation to the existing measurement

`50-findings/07` recorded a deterministic gate at 9/10 alone and 6/10 once a 7B
checklist and panel were added. This is the same direction, measured
differently: the same model on the same arms, with the judging stages off and
then on, and the rejection rate of already-passing candidates stated directly.

## What is not established here

- **N=1 per arm.** No rep-to-rep variance is available on either side.
- **Six arms of sixteen.** `judge_staged` was partial when these figures were
  taken; `m7`, `m7b`, `m7c`, `m7e`, `m7f`, `dloop`, `staged` and
  `test_synth_retry` had not run in the repaired condition.
- **The two conditions differ in a second way.** `nothink` also removes
  reasoning from the implementer call. `monolith` isolates that at +1 of 28,
  which is one task, but it is one arm at N=1 and does not bound the effect
  tightly.
- **`judge_fullctx` moves the other way** (+2), and `judge_caveat`'s −8 is the
  largest single movement in either direction. Nothing here explains why those
  two arms behave differently from the rest.
- The `think` sweep, which would separate reasoning from judging on this model,
  has not run.

## Correction, 2026-09-19 — "rejects passing work" is the wrong summary

The section above counts rejections of check-passing candidates and reports
21–31%. Reading what the judge actually wrote on each one splits those 41
rejections into three kinds, and the judge is not the faulty component in any of
them.

| kind | count |
|---|---|
| 1. the judge is right and the check is blind | **19** |
| 2. the audit authored a condition the judge cannot observe | **11** |
| 3. the objective is underspecified and the judge picked a reading | **11** |

### 1. The judge is right and the check is blind (19)

All nineteen are `wf3_refactor` and `wf3_refactor_blindview`. The judge writes:

```
checked: ["no - no change made", "no - no change made", ... ×5]
said:    "Implement the shared helper function to replace duplicated logic
          in both staff_price and clearance_price."
```

`check_comb` is 5 — full marks — because that check tests only the returned
prices and the untouched source passes 5/5. This is E0's defect 3, and **the
judge detects it.** Counting these as the judge rejecting good work inverts what
happened.

### 2. The audit authored a condition the judge cannot observe (11)

`hf_audit_perf`, whose objective is *"transfer() in ledger.py is slow because of
the audit_log write. Make transfers faster."* The audit stage turned that into:

> "The total time taken for 1000 transfers is reduced by at least 40%"

The judge then reports exactly what its input supports:

```
"yes - _audit_line now uses f-string for O(n) construction"   <- the fix landed
"no  - the diff does not provide timing data"                 <- and cannot
said: "Measure and compare execution time of 1000 transfers..."
```

The candidate had replaced O(n²) concatenation with an f-string; the judge says
so itself. It is being asked for a runtime measurement, and it is shown a static
diff. The instruction repeats across rounds 0, 1, 2 and 3 because no code change
can satisfy it through that channel.

**The defect is upstream of the judge**: a condition was written whose witness
does not exist in what the judge is given. That is the same authoring rule E0
states for tasks — completion needs a mechanical witness — applied to a stage
that generates conditions at runtime.

### 3. The objective is underspecified and the judge picked a reading (11)

`wf2_retry` and `hf_retry_backoff`. The judge asks for a counter to reflect total
attempts:

> "Update the calls attribute to increment by the total number of attempts made."

**Both attributes are real.** `Client.__init__` sets `self.calls = 0` and
`call()` increments it; `Sender.__init__` sets `self.attempts = 0` and `_try()`
increments it. Neither objective says what the counter should mean once retries
exist — whether `calls` counts invocations of `call()` or attempts of `fn()` is
open — and the check tests neither reading. The judge chose one; the implementer
chose the other.

### What the score drop therefore means

`objective_pass` *is* the check. The judge is stricter than the check. Measuring
a stricter pipeline with the weaker criterion shows a fall, and 19 of the 41
disagreements are cases where the stricter reading is the correct one.

So the measured result stands — four arms of six score lower with the judge
live, and the retry counts double — while the reading changes: **this is not
evidence that the judge is wrong. It is evidence that the judge and the check
disagree, that the check is not ground truth, and that one stage in the pipeline
(the audit) can author conditions nothing downstream can verify.**

What would separate the remaining question — whether the judge's strictness is
worth its cost — is scoring these runs against something neither stage produced.
That does not exist yet.
