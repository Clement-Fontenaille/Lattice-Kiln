# 18 — The judge is 89% right per condition and 67% right per verdict

*2026-09-27. Queue B, following `50-findings/17`. One model (4B), the matrix
sweep at adapter `63b5b222daf4`, three arms with attributable stage records.
No new runs.*

---

## Isolate the attempts first

A judge asked about an empty diff is not judging. Across the three arms with
clean records, **30-41% of rows carried an empty diff** — 14 of 34 for
`judge_anchored`. Every aggregate reported before this excluded nothing and so
mixed the question "did it judge well" with "was there anything to judge".

On attempts only:

| arm | attempts | OK work, judge NO | NOK work, judge YES | bad decisions |
|---|---|---|---|---|
| `judge_anchored` | 20 | 7/17 = **41%** | 1/3 | 8/20 = 40% |
| `judge_caveat` | 22 | 5/20 = **25%** | 1/2 | 6/22 = **27%** |
| `judge_bypass` | 23 | 7/21 = **33%** | 2/2 | 9/23 = 39% |

The false-accept cell is n=2-3 and reads nothing. **The judge's error is
rejecting work that passed**, and that is the whole of it.

## The error is in the aggregation, not the judgement

Pooling the three arms over work that passed the check, n=58 attempts carrying
233 individual condition verdicts:

    per CONDITION   208/233 = 89% marked yes
    per VERDICT      39/58  = 67% met

The verdict rule is `all(yes)`, exactly — **58 of 58 rows** have
`verdict == met` iff no condition is marked no. And **14 of the 19 rejections
are driven by a single `no`**:

    wf5_partial            ["yes","no","yes","yes","yes"]
    hf_rename              ["yes","yes","yes","no","yes"]
    hf_validate_withdraw   ["no","yes","yes","yes","yes"]

## It scales with how many conditions were written

If each condition carries independent error at rate 1-p, an AND rule accepts at
p^n. With p = 0.893 measured above:

| conditions | observed accept | p^n |
|---|---|---|
| 3 | 11/15 = 73% | 71% |
| 4 | 18/27 = 67% | 64% |
| 5 | 10/16 = 62% | 57% |

The fit needs no free parameter. **The judge's verdict-level unreliability is
its condition-level noise, compounded by the number of conditions it was
handed.**

Which means the AUDIT stage sets the judge's false-reject rate, by choosing how
many conditions to write. Its prompt says "2 to 5 short observable conditions"
(`judge_anchored_workflow.py:205`) and nothing in it knows that the fifth
condition costs about five points of accept rate.

## What this does not establish

Alternative aggregation on the same rows:

| rule | false reject (n=58) | false accept (n=7) |
|---|---|---|
| all yes *(current)* | 19/58 = 33% | 4/7 = 57% |
| at most one no | 5/58 = **9%** | 5/7 = 71% |
| majority yes | 5/58 = **9%** | 6/7 = 86% |

Relaxing the rule cuts false rejects by two thirds. **The false-accept column
has n=7 and cannot referee the trade**, so no rule change is justified from this
data — only the mechanism is established, and the measurement that would settle
it is now specified: enough failing attempts to populate the right-hand column.

The 11% per-condition "error" is also assumed, not shown. A condition may be
genuinely unmet while the check passes — `expected` is authored independently of
the check, which is the point of it. What argues against substance is that the
rate scales with *how many* conditions the auditor happened to write; a real
mismatch would not care.

## Consequences

**For A12/A13** (`author`, `author_judge`): those arms feed `expected` to the
worker as a brief. Same artifact, new consumer. The number of conditions is now
known to be a live variable and should be recorded per run, not left to the
auditor's discretion and forgotten.

**For the judge comparison in `50-findings/17`:** `judge_caveat`'s advantage
over `judge_anchored` — 25% against 41% false rejects — may be nothing more than
the caveat making the judge readier to mark a condition yes. That is a
per-condition effect with a per-verdict shadow, and it is measurable in
`checked` directly.

**Dead end recorded:** `why` is empty on all 33 rows, which looked like a judge
returning verdicts without reasoning. It is a schema difference — this arm's
record carries `checked`, `n_conditions`, `instruction` and `scope`, while
`judge_fullctx` carries `why` and `code_bytes`. Nothing was wrong.

---

## Addendum, same day — one judge is structurally immune

`judge_fullctx` uses **no conditions**: no `expected`, no `checked`, no
`n_conditions`. `judge_change(objective, pristine, after)` makes one call and
returns one verdict with a `why`. The `p^n` mechanism above cannot apply to it,
because there is no conjunction to compound.

That makes it the judge for the `author_judge` arm (A13), chosen on structure
rather than on a score — the scores in `50-findings/17` were the ones this
finding disqualifies.

It does not make it a *good* judge. Its accuracy is unmeasured and unmeasurable
retrospectively, for the reason `50-findings/17` gives: it records nothing to
attribute its 286 stage records by. The claim here is narrower — it cannot fail
in the specific way the checklist judges demonstrably do.

---

## Addendum — the provenance block this entry should have opened with

Appended 2026-09-27, for the reason given in `50-findings/17`'s addendum: this
entry's header cites "Queue B", a working list that no longer exists, in the slot
where `Artifacts` belongs. Entries 13, 14 and 16 carry the block below; this one
did not.

**Subject:** `nemotron3-nano-4b:latest`, the matrix sweep at `params.adapter`
`63b5b222daf4`, protocol `tools` v2, temperature 0.6 / top_p 0.95, `num_ctx` 16384,
n=1 per task. Arms `judge_anchored`, `judge_caveat`, `judge_bypass` — the three whose
workflows tag their stage records with `model` and `results_subdir`, which is why
these three and no others.

**Recorded:** 2026-09-27.

**Artifacts:** `experiments/M6-evaluation-suite/results_matrix_nemotron3-nano-4b/`
(the check outcome per `(task, rep)`), and
`experiments/M7-static-workflow/stage_influence_judge_{anchored,caveat,bypass}.jsonl`
filtered to `results_subdir == results_matrix_nemotron3-nano-4b` (the judge's
`checked` array, `n_conditions`, `verdict`, `diff_empty`).

**Metric:** per-condition — entries of `checked` equal to `yes`, over work the check
passed. Per-verdict — `verdict == met` over the same rows. Attempts only:
`diff_empty` false, which excludes 30–41% of rows.

**Verdict:** the mechanism is established — `all(yes)` over n conditions, accept rate
tracking p^n with no free parameter. The remedy is not: the false-accept column has
n=7 and cannot referee a rule change.
