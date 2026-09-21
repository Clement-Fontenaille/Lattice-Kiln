# 14 — When the judge states its reasons before its verdict

**Subject:** `qwen2.5-coder:7b-instruct-q4_K_M` and `nemotron-gpu` (NVIDIA
Nemotron Nano 9B v2, `num_gpu 99`, `think=false`, `min_predict 400`), both at
`num_ctx` 8192
**Recorded:** 2026-09-20 / 2026-09-22
**Artifacts:** `experiments/E8-judge-verdict-order/` (declaration, `analyse.py`),
`experiments/M7-static-workflow/stage_influence_judge_*.jsonl`, `evalkit_store/`
**Variable:** `LATTICE_JUDGE_FORMAT` — `decision_first`, each `checked` entry
opening with the verdict token ("yes - <reason>"), against `reason_first`, each
entry ending with it ("<what you observe> -> yes"). Nothing else differs; the
transformation is an exact string replacement that raises if its target is
absent.
**Scope:** 3 arms × 2 models × 2 formats, 1,513 reps in the pool, 1,885 stage
records attributed. Reps per reported cell: 115–206.
**Verdict:** **confirms**, with the effect model-specific and the mechanism
identified.

## What was being asked

`50-findings/11` recorded that the judge rejects work whose deterministic check
has already passed, at 21–31% across three arms. `judge_format.py` named a
candidate cause: those three arms are the only ones carrying a worked example in
their JUDGE prompt, and that example's first entry labels `no` a condition its
own prose says is satisfied. The label/prose contradiction appears in 0.6–1.0%
of condition assessments, too rare to explain the rate — so it was a cause to
test, not a demonstrated one. E8 tests the more general form: does committing to
a verdict before writing the reason for it change the verdict?

## Result 1 — the judge does not refuse unsound requests, in eight cells of eleven

The suite contains tasks whose correct outcome is to refuse the work. On those,
the right verdict is `unsound_request`:

| arm | model | format | n | right |
|---|---|---|---|---|
| `judge_caveat` | qwen | `reason_first` | 29 | **48%** |
| `judge_caveat` | qwen | `decision_first` | 24 | 12% |
| `judge_bypass` | qwen | `reason_first` | 24 | 12% |
| *the other eight cells* | | | 19–29 | **0%** |

Zero. Not low — zero, in eight of eleven cells, across both models and all three
arms. This is a **capability floor, not a format effect**, and it is the largest
single result in the experiment. The judge stage as currently built does not
detect false premises; it evaluates conditions and reports whether they are met.

It also bears on `50-findings/07`'s census result (3/3 implement an impossible
`O(log n)`; 0/3 flag it): the failure survives being moved into a dedicated
judging seat with the conditions laid out explicitly.

## Result 2 — one configuration escapes it, and its prompt says why

The exception is not arbitrary. `judge_anchored` and `judge_bypass` have
**byte-identical** JUDGE prompts. `judge_caveat` is the same prompt plus one
block, and that block is an instruction about how to weigh the per-condition
tokens:

> They describe what finishing WOULD look like if the request is sound, and they
> say nothing about whether it is. […] **Ticking every condition "no" is not
> evidence for either one.** Decide from the request itself, not from the count
> of unmet conditions.

**The block is worth 12% under `decision_first` and 48% under `reason_first`.**

The mechanism is ordering-dependent by construction. The caveat tells the judge
not to infer the verdict from the token column. Under `decision_first` that
column is emitted *before* any reasoning, so the caveat is advice about
interpreting a summary already committed to — there is nothing left for it to
modulate. Under `reason_first` the observation precedes each token and the
caveat has something to act on while the verdict is still open.

**The format change did not merely reorder the output. It activated an
instruction that was already in the prompt and inert.**

## Result 3 — the effect lands exactly where the block says it should

The caveat block names one case: an empty diff, where every condition reads "no"
whether the engineer failed or correctly refused. Rejection rate among
check-passing candidates, split on `diff_empty`:

| arm | model | empty: dec → rsn | non-empty: dec → rsn |
|---|---|---|---|
| `judge_caveat` | qwen | **89% → 46%** | 58% → 28% |
| `judge_bypass` | qwen | 100% → – | 46% → 34% |
| `judge_anchored` | qwen | – → 95% | 94%* → 32% |
| `judge_caveat` | nemo | 100% → 100% | 18% → 32% |
| `judge_bypass` | nemo | 100% → 100% | 18% → 22% |
| `judge_anchored` | nemo | 100% → 100% | 18% → 18% |

`judge_caveat` / qwen / `reason_first` is the **only cell in the matrix** where
empty-diff rejection falls below 89%. Every other cell sits at 95–100%
regardless of arm, model or format. The prediction was made from the prompt text
before the split was computed, and it holds.

(*`judge_anchored` / qwen / `decision_first` rests on 31 candidates from 9 reps
— see Limits.)

## Result 4 — on qwen, the format trades one error for the other

Counting rejections alone is misleading, because some rejections are correct.
Per rep, against what was actually delivered (`objective_pass`: the gate **and**
every structural dimension):

| arm | model | format | n | correct | false rej | false acc |
|---|---|---|---|---|---|---|
| `judge_caveat` | qwen | decision | 122 | 52% | **42%** | 7% |
| `judge_caveat` | qwen | reason | 115 | **64%** | **20%** | 16% |
| `judge_bypass` | qwen | decision | 134 | 60% | 34% | 5% |
| `judge_bypass` | qwen | reason | 116 | 68% | 24% | 8% |
| `judge_anchored` | qwen | reason | 114 | 68% | 23% | 9% |
| `judge_caveat` | nemo | decision | 136 | 76% | 12% | 12% |
| `judge_caveat` | nemo | reason | 134 | 75% | 18% | 7% |
| `judge_bypass` | nemo | decision | 136 | 76% | 13% | 10% |
| `judge_bypass` | nemo | reason | 134 | 75% | 16% | 8% |
| `judge_anchored` | nemo | decision | 130 | 75% | 12% | 13% |
| `judge_anchored` | nemo | reason | 133 | 74% | 19% | 8% |

On qwen, `reason_first` **halves false rejections and doubles false
acceptances**. Net correct call rate rises 12 points on `judge_caveat` and 8 on
`judge_bypass`. It converts a strongly over-rejecting judge into a mildly
over-accepting one — a shift in where the judge errs, not a pure gain, and worth
stating that way because which error is cheaper depends on what the gate does
downstream.

## Result 5 — on nemotron, judgment is unchanged and validity is transformed

Correct call rate is flat at 74–76% in all six nemotron cells. But the format
does something else entirely there:

| model | format | verdicts that failed to parse |
|---|---|---|
| nemo | `decision_first` | 17%, 18%, 21% |
| nemo | `reason_first` | 1%, 1%, 6% |
| qwen | either | 0–7% |

**`reason_first` nearly eliminates nemotron's unparseable verdicts.** An
unparseable verdict is a rep whose judge stage produced nothing usable, so this
is a substantial reliability gain even though judgment quality among parsed
verdicts does not move.

It also qualifies the row above it: nemotron's `decision_first` correctness is
computed on the 79–83% that parsed, its `reason_first` correctness on 94–99%. The
flat 75% is measured on a *more complete* sample under `reason_first`, which
makes "unchanged" a slight understatement.

**Correction, recorded because it was stated wrongly in session:** this was
reported as "no effect on nemotron". That was wrong. The format has a large
effect on nemotron's output validity and none on its judgment.

## Result 6 — the two models are differently biased judges before any intervention

| | qwen | nemotron |
|---|---|---|
| correct call rate | 52–68% | 74–76% |
| false rejection, `decision_first` | 34–42% | 12–13% |
| `unsound_request` as share of final verdicts | 6.6% | **0.4%** |
| per-candidate `met` vs `not_met` | 1,337 / 1,615 | 2,143 / 1,306 |

**Nemotron is the better judge on this suite**, and it is the less responsive to
the scaffold. qwen over-rejects; nemotron is closer to balanced. The 16× gap in
willingness to use `unsound_request` is a model-level disposition, which is why
the caveat block — whose whole purpose is to license that verdict — has nothing
to unlock on nemotron.

The manipulation is not failing to reach it: nemotron complies with the
requested `checked` format in **95%** of entries. It reorders its output and
keeps its verdicts.

## What this means

**The lift is real and it is model-specific.** Measured at the processor /
effective-ceiling layer (`70-THINKING/02`'s vocabulary), one output-contract
change buys 8–12 points of judge accuracy and 36 points of false-premise
detection on qwen, and buys output validity but no accuracy on nemotron. **A
scaffold tuned on one model is mis-tuned for the other**, in both directions:
`reason_first` is clearly right for qwen and is, for nemotron, a fix for a
different defect than the one it was introduced to address.

**An instruction's position in the output contract determines whether it can
execute at all.** The caveat block was in the `judge_caveat` prompt for its
entire history and was doing nothing, because the format gave it nothing to act
on. That is not a prompt-quality issue and would not have been found by
rewriting the block. It is worth generalising as a hypothesis: *an instruction
about how to weigh evidence cannot function in a contract that emits the
conclusion first.*

**A candidate reading for `70-THINKING/02`, flagged as candidate.** That
document records that no reviewer framing — neutral, adversarial, structured,
K=5 — lifts the judge, and attributes the null to those interventions varying
**stance**, which does not change granularity. E8 varied neither stance nor
input, and did lift the judge. One reading is that `reason_first` splits the
judging operation into observe-then-decide — granularity reduction applied to
the judge's *own output* rather than to its input. That is consistent with the
document's account and is **not established by this experiment**, which was not
designed to test it.

## Limits

- **`judge_anchored` / qwen / `decision_first` is absent.** It resolves 9 reps of
  170 stored, because those rows were migrated from older M7 runs whose stage
  records do not correspond. Its apparent −55.5 point delta is not reportable and
  is withheld by `analyse.py`'s floor.
- **False-premise cells are 19–29 reps.** 48% against 0% is solid; 12% against
  0% is not.
- **The empty-diff split for `judge_caveat` / qwen rests on 28 and 56
  candidates.** Enough for an 89-vs-46 gap, not enough to quote a number.
- **One arm, one prompt block.** The mechanism predicts that other
  reason-dependent instructions behave the same way. Untested.
- **Attribution.** 1,885 of 2,450 stage records attributed; 565 unresolved,
  mostly M7-era runs predating the store. The join that recovers the
  pre-2026-09-21 records is validated against 856 stamped ones at 100% accuracy
  among resolved, and `analyse.py` re-runs that check on every invocation.

## Methodology note

The instrument defects found while producing this are recorded in the commit
history and in `analyse.py`'s header, and one is worth surfacing here because it
nearly produced a false finding: stage records did not carry the experiment's own
independent variable, and the first join written to recover it dropped exactly
the cases where the two formats **agreed**, which manufactured differences. It
put nemotron's `judge_bypass` at +22.7 points where the answer is +4.3.

What caught it was an accident of timing — the stamping fix landed mid-sweep,
leaving 856 records with ground truth to validate the join against. Without that
overlap the biased numbers would have been reported. **An instrument needs a
channel that can tell you it is lying, and that channel has to be built before
the measurement rather than recovered from a lucky overlap.**
