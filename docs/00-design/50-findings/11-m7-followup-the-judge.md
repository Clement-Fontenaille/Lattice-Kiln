# 11 — M7 follow-up: the independent judge

**Milestone:** [M7](../40-roadmap/01-MILESTONES/completed/07-static-supervised-workflow.md), after closure
**Opened:** 2026-09-14
**Verdict:** **confirms entry 7 and narrows it, with one genuinely new result.**
**Status:** every figure below is **N=1**. An N=5 pass over eight arms is in flight,
and the whole of entry 10's finding 6 is about why that distinction matters.
**Artifacts:** `experiments/M7-static-workflow/` — `ARMS.md` names the arms;
`score_judge.py`, `score_self_report.py`, `analyse_objection.py`, `derive_m7d.py`

## The question

`50-findings/07` measured a 7B panel added to a deterministic gate and found it made
things **worse** — 9/10 alone, 6/10 with the panel — concluding that a 7B does the
doing and cannot do the judging, and that the gap is not a prompt away.

**That panel shared the context of the work it judged.** The operator's hypothesis was
that sharing the context was the variable rather than the judging, and that enough
differentiated roles now exist to give a judge a meaningfully different context.

## 1. Independence removes the approval bias. That is the new result and it is real.

| | approval rate |
|---|---|
| the **worker** on its own work | **96%** |
| the **judge** on the worker's work | **64%** |

The worker's verdict is mandatory in its control block and recorded on every run ever
made, and the workflow discards it. Scored for the first time here, it is worthless:
it says `answered` on 96% of tasks and its precision sits **+3 points above a constant
yes** — 82% against a 79% base rate on `m7`, +1 on `m7b`, +0 on `m7c`. A forecaster
who says *no rain* every day in a desert is right 95% of the time, and that figure
describes the desert.

The independent judge does not do that. **So entry 7's verdict needs splitting: no
*framing* beats the approval bias, and *context independence* does.** That was not
known.

## 2. And it does not produce accuracy. It replaces bias with noise.

| population | agreement | best constant | gap |
|---|---|---|---|
| all tasks | 53% | 53% | **0 points** |
| **non-empty diffs** | **63%** | **79%** | **−16 points** |

On the population that requires judgement, the judge is **worse than always saying
`met`**. And the number a workflow would act on — precision on `not_met` over
non-empty diffs — is **0 of 2**.

### The trap, named before the run and sprung exactly

From `PREDICTION-M7C.md`: *if the only thing it reliably detects is that the diff is
empty, it is not judging, it is detecting emptiness, which `len()` does for nothing.*

It returned `unsound_request` on **13 of 13 empty diffs**. Not a tendency — every one.
Five of those happened to be false-premise tasks, so it *caught 5 of 5* where the
premise audit caught 2 of 5. **Without splitting the populations that would have been
reported as the judge's triumph.**

## 3. Two failure modes, opposite, which is why the total lands near chance

**False `met` — topic matching in place of verification.** Its own words: *the diff
adds a retries parameter to Client.call and implements retry logic, which meets the
request*; *the change imports the csv module and uses it to properly parse*. It reads
the change's apparent purpose and concludes. It never asks whether the code works,
because it cannot run anything, so it substitutes *on the right topic* for *does the
right thing*. The suite's largest stress tag is `edge-coverage` — nine tasks where the
topical answer is obvious and the correct one is in the details.

**False `not_met` — misreading code.** *The diff does not handle the case where the
withdrawal amount is exactly equal to the account balance.* Specific, checkable, and
wrong. This is entry 7's second failure mode reproduced exactly, and **context
independence does not touch it.**

## 4. The judge could not have been detecting premises, structurally

On an empty diff it receives the literal string `(no change to any .py file)`. On a
non-empty one it receives a unified diff with **three lines of context** — never the
unchanged parts of a modified file, never an untouched file, never the check.

Establishing that `_legacy_export` *has* callers requires reading another file. **No
information about the premise reaches the judge at all.** Its 13 of 13 cannot be
detection; it is a prior.

## 5. The note does not move the verdict where it could matter, and might where it does

The first reading of this was wrong. A marginal comparison — `unsound_request` on 43%
of tasks with a note against 44% without — was presented as refuting an echo. It
refutes nothing: it averages two populations.

| task level | with a note | without |
|---|---|---|
| **empty diff** | 9/9 = **100%** | 4/4 = **100%** |
| non-empty diff | 1/14 = 7% | 0/5 = 0% |

The note contributes **nothing** where the prior is absolute. At candidate level, on
non-empty diffs, **17% (15 of 85) against 5% (2 of 40)** — suggestive, small, and the
only place a note effect appears. A reading worth testing rather than asserting: the
note may not replace the examination but bias the reading of what is examined.
`judge_staged` asks the same task twice, without and with the note, which is the only
design separating *the note moved this* from *both track the same case*.

## 6. What the operator established, and it reframes the whole line

**A judge's value is the difference between its context and the worker's, not the size
of its context.**

Offered the fix *give it the full original source so it can verify*, the operator
refused it: a judge holding essentially the worker's context is independent in the
strict sense, and its judgement then measures **the model's noise level** rather than
the work. Two instances of one model, same context, same question, share their blind
spots — their agreement and their disagreement are both sampling variance. M15 already
names this for two different models; with one model the correlation is maximal by
construction.

So finding 4's diagnosis was right about the symptom and wrong about the remedy. The
judge sees **too little of the same thing**. Completing it would make it a second
sample of the worker. What is needed is a **different** thing.

This reclassifies what is in flight. `test_synth` is the interesting arm not because
its output is executed but because **its verdict depends on no reading of the worker's
code at all** — the model supplies an instrument and the interpreter judges.
`judge_anchored`'s expectation is written before the work exists, which is a different
context by timing. `m7c`, `m7e`, `m7f` and `judge_caveat` vary framing over a context
of the same nature, and on this account should not be expected to move.

## 7. The decline mechanism covers one cell of a matrix

Every false-premise task in the suite shares a property nobody had noticed: **the
check already passes at baseline.** So declining requires no reasoning — it falls out
of *the check passes and nothing improved it*. The 5/5 decline accuracy reported all
through M7 **measures the keeper's no-op detection, not premise judgement.**

Worse, the rule cannot express the other cases. It requires the check to **pass**, so
it can say *there is nothing to do* and never *there is something to do and it must
not be done*.

Suite 0.4.0 adds the two missing cells, and one of them pays a second debt:

- **`hf_audit_perf`** — a real speedup exists and a harmful one does too. Deleting the
  audit call raises the combined score from 3 to 4 while `AUDITSCORE` goes from
  passing to failing and the subtest count never moves. **The first task that
  discriminates a set-comparing keeper from a count-comparing one** — the rule `m7b`
  implements had never been put in front of a case where it decides.
- **`hf_wrong_spec`** — the check itself is wrong. `objective_pass` is false for every
  arm by construction, and **no current arm can be right**: the correct terminal is
  `declined` and the mechanical rule cannot produce it.

## 8. A use for the premise audit that its precision does not disqualify

Its precision is around 20% over the suite, so it cannot decide anything. Asked only
*which of two cases is this*, within the subpopulation where the check is satisfied
and nothing improved, it separated them perfectly on the `m7c` run: a concern on all
five false premises, silence on both real-work tasks.

**It routes without deciding.** A judge is worth calling when the check is satisfied,
nothing improved, **and the premise was not doubted** — because that is the case where
the check may not measure what was asked, and the judge is then the only instrument
left rather than a duplicate of the check.

That is the only positive argument for a judge this investigation produced, and it is
the operator's. An earlier version of the bypass rule skipped the judge on the first
two conditions alone, which would have removed it from exactly that case —
`wf3_refactor_blindview`, where the decline is measurably wrong.

## What was corrected, and the pattern

Four claims of mine were wrong, and one mistake produced three of them.

- *The `wf6_multi` regression showed the keeper's count rule failing.* It was an
  artifact of a broken label extractor; `m7` has zero regressions across 150 runs.
- *The audit catches 2 of 5 false premises.* One run. Another gives 5 of 5, by raising
  a concern on 72% of tasks instead of 37% — louder, not better.
- *The anchor recreated entry 7's checklist failure.* One observation, two variables.
- *There is no echo.* A marginal comparison across two populations.

**Reading a single run as a measurement** — in a project whose own entry 10 finding 2
established that an unchanged arm varies by three tasks against itself. It applies to
the stages inside an arm exactly as it applies to the arm's score.

## What this does not settle

Whether a judge helps. None of these has authority, by design, so none can help or
harm. What is settled is whether a verdict is **worth** authority — and on the
evidence in hand, not yet, for reasons that are the model's rather than the framing's.

`50-findings/07`'s verdict therefore stands wider than it was written: not *this
framing fails* but **framing is not the variable**. What would lift the ceiling is a
second judgment source, already the recorded gating dependency for M12 onward — or not
asking the model to read at all, which is what a mechanical witness does and what
`test_synth` tests.
