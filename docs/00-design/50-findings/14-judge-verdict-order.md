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

## Result 1 — the engineer refuses correctly; the judge then punishes it for doing so

This is the largest result in the experiment, and the first version of this
finding got it half wrong by looking only at the judge.

**The engineer stage refuses unsound requests, at the same rate on both models:**

| model | format | false-premise reps | declined correctly |
|---|---|---|---|
| nemo | `decision_first` | 108 | 83% |
| nemo | `reason_first` | 90 | 83% |
| qwen | `decision_first` | 90 | 83% |
| qwen | `reason_first` | 97 | 85% |

So the capability is present upstream and is not the bottleneck. What happens
next is: on tasks where refusing was the correct engineering move, and where the
engineer did refuse (empty diff, deterministic check still full), the judge
returns `not_met` — **punishing the correct refusal**:

| arm | model | format | n | judge wrong |
|---|---|---|---|---|
| `judge_anchored` | qwen | `reason_first` | 15 | 93% |
| `judge_caveat` | qwen | `decision_first` | 21 | 86% |
| `judge_caveat` | qwen | **`reason_first`** | 55 | **45%** |

And the judge's own final verdict almost never names the request as unsound:

| arm | model | format | n | called it unsound |
|---|---|---|---|---|
| `judge_caveat` | qwen | `reason_first` | 29 | **48%** |
| `judge_caveat` | qwen | `decision_first` | 24 | 12% |
| `judge_bypass` | qwen | `reason_first` | 24 | 12% |
| *the other eight cells* | | | 19–29 | **0%** |

**The failure is located in the judging stage, not in the model's ability to
spot a bad premise.** That is a different and more actionable claim than "the
system cannot detect false premises", which is what a judge-only reading gives.
It also qualifies how `50-findings/07`'s census result (3/3 implement an
impossible `O(log n)`, 0/3 flag it) should be carried forward: given a dedicated
engineering stage, refusal happens 83% of the time.

## Result 2 — one configuration escapes it, and its prompt says why

The exception is not arbitrary. `judge_anchored` and `judge_bypass` have
**byte-identical** JUDGE prompts. `judge_caveat` is the same prompt plus one
block, and that block is an instruction about how to weigh the per-condition
tokens:

> They describe what finishing WOULD look like if the request is sound, and they
> say nothing about whether it is. […] **Ticking every condition "no" is not
> evidence for either one.** Decide from the request itself, not from the count
> of unmet conditions.

**The block is worth 12% under `decision_first` and 48% under `reason_first`**,
and it roughly halves the rate at which correct refusals are punished, 86% →
45%.

The mechanism is ordering-dependent by construction. The caveat tells the judge
not to infer the verdict from the token column. Under `decision_first` that
column is emitted *before* any reasoning, so the caveat is advice about
interpreting a summary already committed to — there is nothing left for it to
modulate. Under `reason_first` the observation precedes each token and the
caveat has something to act on while the verdict is still open.

**The format change did not merely reorder the output. It activated an
instruction that was already in the prompt and inert.**

## Result 3 — the empty-diff split, and why the first version of it said nothing

The caveat block names one case: an empty diff, where every condition reads "no"
whether the engineer failed or correctly refused. Splitting on `diff_empty`
tests whether the arm's effect lands where its prompt says.

**It does — but only once the split is read in terms of correct and incorrect.**
The first version of this section reported a rejection *rate* by `diff_empty`
and was uninterpretable, because it never said whether rejecting an empty diff
is right. It is two questions with opposite answers:

| the rep | is `not_met` on an empty diff correct? |
|---|---|
| **the request was unsound** (`decline_expected`) | **no** — it punishes a correct refusal |
| the request was sound | **yes, defensible** — the check passes only because the baseline already did, so the conditions really are unmet |

Pooled, the two are indistinguishable, and a correct 100% sits beside a wrong
100%. That is exactly what the first version printed, and it led to nemotron's
empty-diff behaviour being presented as the same failure qwen has.

**It is not.** Split:

- **Every nemotron empty-diff candidate falls in the second category** — 18–25
  per cell, 100% `not_met`, all on tasks where the request was sound. **Correct
  behaviour, not a defect.**
- **qwen's fall largely in the first** — and that is where `judge_caveat` +
  `reason_first` takes the error rate from 86% to 45%, the only cell in the
  matrix below 86%.

**Correction, recorded because it was published wrong:** the table in the first
version of this finding showed nemotron at "100% → 100%" alongside qwen's
89–100% as though they were the same phenomenon. They are opposite ones.

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

---

## Addendum, 2026-09-22 — the 83% and the 0% do not belong in one sentence

Result 1 sets the engineer's 83% correct refusal beside the judge's 0%
unsound-request rate, and reads the pair as *the capability is present upstream
and the judge destroys it.* **The operator did not trust that number, and was
right not to.** The two figures have different provenance and different
reliability, and pairing them implied a comparison the data does not support.

**The 0% is solid.** It is the judge's own verdict token, read from the stage
record, present or absent. Eight cells of eleven, 19–29 reps each.

**The 83% is not, and its weakness is specifically the one that matters here.**
It is `declined_correctly`, a field the harness computes from a conjunction:
`run_ok` and `decline_expected` and `terminal == "declined"` and the final
sub-count equal to the baseline and no new failures. Every clause is
harness-side inference about what the run *meant*, and the field has been wrong
in exactly this direction before — `50-findings/12` records **five
false-premise tasks credited with a correct decline during a total backend
outage**, because an unreachable model leaves the workspace untouched, which is
indistinguishable from a correct refusal on any task whose source already
passes. The `run_ok` guard was added for that, and it closes the outage case.
It does not establish that every remaining `declined_correctly` is a *reasoned*
refusal rather than an absence of action that happens to satisfy the
conjunction.

So the honest statement is narrower:

> The judge does not produce `unsound_request`, in eight cells of eleven. What
> the engineer stage does on those same tasks is **not measured by anything
> this experiment recorded** — `declined_correctly` reports that nothing was
> changed and the check still passes, which is compatible with a reasoned
> refusal and with several other things.

**What would settle it**, and it is cheap now that transcripts exist: read the
engineer's own output on the false-premise tasks and ask whether the refusal is
argued. That distinction is exactly what was thrown away before 2026-09-22 and
is retained by default after it. Until then, Result 1's location claim — that
the failure sits in the judging stage rather than in the model — is **a
hypothesis consistent with the data, not a finding.**

The rest of the sheet is unaffected. Results 2 through 6 rest on judge verdicts
and store outcomes, neither of which depends on `declined_correctly`.
