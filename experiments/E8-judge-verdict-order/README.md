# E8 — Does the judge decide before it reasons?

**Status:** not run.
**Suite:** 0.4.1 (the counter-semantics fixtures, repaired 2026-09-19).

## The question

The judge's per-condition output opens with a verdict token and justifies it
afterwards:

```
"checked": one line per condition, in order, each "yes" or "no"
```
→ `"yes - the format matches the original exactly"`

So the token is emitted before the reason for it exists. Whether that ordering
changes the verdict is testable by reversing it:

```
"<what you observe in the diff> -> yes"
```

## What prompted it

On `judge_anchored`, `judge_bypass` and `judge_caveat`, a live judge rejected
**21–31% of candidates whose deterministic check had already passed** (15/54,
17/55, 9/42 — `50-findings/13`). Those same three arms are the only ones of
seven carrying a worked example in their JUDGE prompt, and that example's first
entry is self-contradictory:

```
"no - range(retries) with retries=0 skips the loop, then fn() runs once,
      so that one is satisfied"
```

The code described does satisfy the condition. Label says no, prose says yes.

**That is a candidate cause, not a demonstrated one.** Measured across the three
arms, label/prose contradictions appear in **0.6–1.0%** of condition assessments
(4/564, 6/585, 3/517) — far too few to account for a 21–31% rejection rate. The
example is fixed in the `reason_first` variant along with the ordering, so this
experiment tests the pair together, not the example alone.

## Design

| | |
|---|---|
| **arms** | `judge_anchored`, `judge_bypass`, `judge_caveat` — the three sharing the contract and the example |
| **models** | `qwen2.5-coder:7b-instruct-q4_K_M`; `nemotron-gpu` with `LATTICE_THINK=0` |
| **variable** | `LATTICE_JUDGE_FORMAT` = `decision_first` \| `reason_first` |
| **reps** | 1 |
| **runs** | 3 arms × 2 models × 2 formats = **12**, of 34 tasks each |

**`baseline` and `monolith` are reused, not re-run.** Neither has a judge stage,
so neither can move with this variable. They come from
`M6-evaluation-suite/results/` (qwen) and
`M6-evaluation-suite/results_nemotron_nothink/` (Nemotron) and give the floor
and the no-judge reference for each model.

Nemotron runs with reasoning **off** in both format arms. That holds it
comparable to qwen, which has no reasoning channel: measured on the same audit
prompt, both emit ```` ```json ```` and then the object — 8 characters before
the verdict. Neither model deliberates today, in either condition.

## Primary measure

**Rejections of check-passing candidates** — candidates whose deterministic
check was already full and which the judge returned `not_met` on. That is what
the hypothesis is about. Earned score over the 28 non-floor tasks is reported
beside it, but it is the downstream consequence, not the measurement.

## What would falsify it

**The rejection rate does not move between formats.** If `reason_first` rejects
check-passing candidates at the same 21–31%, the ordering is not the cause and
the example correction did not matter either, and the cause lies elsewhere —
most likely in the conditions the audit stage authors, which
`50-findings/13`'s correction already implicates on `hf_audit_perf`.

**A second, cheaper null:** the format is applied but the judge ignores it —
entries still open with the token. `judge_format.apply()` raises if its
replacement target is missing, so an unapplied variant cannot pass silently, but
a *disregarded* one can. Check the recorded `checked` strings before reading any
score.

## Layout

```
E8-judge-verdict-order/
  README.md    this file
  PROTOCOL.md  the steps
  queue.json   12 jobs
  results/     results_<model>_<format>/<arm>.json
```
