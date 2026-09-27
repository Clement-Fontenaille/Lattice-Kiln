# 17 — The ladder has two instruments, not one

*2026-09-27. Queue B items B9 and B10. Source reading and a store read; no new
runs.*

---

## The claim this examines

The project's central figure is an arm ladder measured on the 4B:

    baseline 6/34 -> monolith 14 -> monolith_recovery 18 -> dloop 21
      -> m7 / test_synth / judge_anchored 23 -> staged 24
      -> judge_caveat / judge_fullctx 26 -> judge_bypass 27

read as: processor design lifts a small model from 6/34 to 27/34.

## B10 — What each arm's worker could see of the gate

Every arm from `dloop` upward embeds a loop that scores the workspace and feeds
**the failing subtest names** back into the implementer's prompt. In
`m6_arms.py:102-106`:

```python
hint = best["s"]["fails"]
...
step = (f"{seg}\n\nCurrent state still fails:\n{hint}\n"
        "Output the whole corrected file(s).")
```

`fails` is `"\n".join(_FAIL.findall(out)[:12])` — up to twelve failing subtest
labels, verbatim, from the command that grades the run.

**This is not confined to `dloop`.** The string `Current state still fails`
appears in every one of these files:

    m6_arms.py                    (dloop, staged)
    m7_workflow.py    m7b  m7c  m7e  m7f
    judge_anchored  judge_caveat  judge_bypass  judge_fullctx  judge_staged
    test_synth      test_synth_retry

The whole M7 family inherits the dloop core. The arms that do **not** put
failure names in front of the model are exactly three:

    baseline, monolith, monolith_recovery

**So the ladder splits at `dloop`:**

| | arms | range |
|---|---|---|
| the worker never sees the gate | baseline, monolith, monolith_recovery | 6 → 18 |
| the worker is handed failing subtest names each round | everything else | 21 → 27 |

The step from 18 to 21 is where the instrument changes, and no arm spans the
boundary. Every comparison across it confounds *processor design* with *access
to the answer key*.

**What this does not say.** It does not say the upper arms are worthless or
that their differences are fake — `judge_bypass` 27 against `judge_anchored` 23
is a within-instrument comparison and stands. It says the 6→27 figure is not a
single measurement, and nothing written down said so.

**What it makes newly important.** `monolith_test` (Queue A11) was queued to
separate model-chosen probing from harness-driven probing. It is now also the
only arm that would put a *deliberate*, *counted*, *capped* probe next to
`monolith`'s none and `dloop`'s unconditional-every-round — the first clean
reading of what gate access is worth.

## B9 — Does `judge_fullctx` judge, or echo the worker?

**Not answerable from what is on disk.** Three routes were tried and all three
measure an artifact.

**1. `score_correlation.py`, the existing instrument, joins wrongly.**
`{r["task"]: r for r in rows}` collapses 170 result rows to 34 — last rep wins
— and `worker_verdicts()` keys on the objective's first 90 characters, which
collapses the same way. Per-rep judge verdicts are compared against one
arbitrary rep's outcome. Its output (`judge_fullctx` 74% vs check, 54% vs
worker, "tracking: the check") is not interpretable, and the arms have very
different rep counts, which alone moves that number.

**2. Re-joining on `(task, rep)` pools models and sweeps.**
`stage_influence_*.jsonl` is append-only across every sweep ever run.
`judge_caveat` holds 1446 records over **170 distinct `(task, rep)` keys** — up
to 13 per key — spanning three models plus 458 records with no model recorded.
`results/judge_caveat.json` is one sweep. The join matches qwen judge verdicts
to nemotron check outcomes.

**3. Restricting to model-tagged populations leaves nothing.** `judge_fullctx`
has **zero** of 286 records carrying a model, so it has no clean population at
all. `judge_caveat` and `judge_bypass` are tagged on the E8 runs, but those
result files hold 2–8 rows against 170 stage records — interrupted runs — and
the join yields n ≤ 8 per cell.

**The fix is plumbing, not analysis.** `run_suite` already computes a cell id
and exports it as `LATTICE_CELL`; the stage records do not carry it. With the
cell on the record the join is exact and carries model, protocol and sampling
with it. Queued as A14.

**Until then, no claim about any judge's accuracy is licensed** — including the
ones in this repository. The corrected-join numbers computed on the way to this
conclusion showed every judge scoring *below* a constant predictor, and that
figure is as contaminated as the one it corrects. It is recorded here only so
nobody recomputes it and believes it.

## Consequence for the queue

`author_judge` (A13) was made to wait on B9 so its judge could be chosen on
evidence. B9 now waits on A14. Either A13 proceeds with `judge_caveat` on the
stated grounds — it keeps the judge on every task, so the briefing effect is not
confounded with judging less — or it waits for a clean read.

The first is better. A13's question is whether an authored brief helps the
worker, and that does not need the judge to be the best one available; it needs
the judge to be the *same* one as in its control.

---

## Addendum, same day — the contract change is keyed, and B9 was partly readable

Prompted by the question "we did change the output contract on tests for all
models recently, right?" — yes, twice: markers to tools, then v1 to v2. Two
things follow, one confirming and one correcting.

**Confirming: the ladder is a single population.** 726 store rows carry
`protocol` and an adapter fingerprint; 6548 predate the params work and carry
neither. But on the 4B every arm in the ladder holds exactly **34 rows at one
adapter, `63b5b222daf4`** — baseline, monolith, monolith_recovery, dloop,
staged, m7, test_synth and all four judges. The matrix re-ran every arm on the
current contract. The B10 split above is not comparing across protocols.

**Correcting: "no claim about any judge's accuracy is licensed" was too
strong.** The gap is per-workflow, not systemic. `judge_caveat_workflow.py:690`
and `:693` already record `model` and `results_subdir` on the stage record;
`judge_fullctx_workflow.py` simply lacks those two lines, as do the `m7*` and
`test_synth` workflows. So `judge_caveat` and `judge_bypass` each have 34
cleanly attributable matrix records, and a single-model single-adapter read was
available without A14:

| arm | n | says met | check pass | vs CHECK | best constant | lift | vs WORKER |
|---|---|---|---|---|---|---|---|
| judge_caveat | 33 | 61% | 79% | 64% | 79% | **-15** | 70% |
| judge_bypass | 29 | 66% | 76% | 62% | 76% | **-14** | 55% |

**Both judges score below a constant predictor** on their own rows, and both say
`met` less often than the check passes — they reject correct work. That is the
failure mode `50-findings/14` names, with a clean number under it for the first
time.

n=33 on one model at n=1 per task settles nothing by itself. What it does is
remove the excuse: the question was answerable, and the earlier conclusion that
it was not came from reading the dirtiest available file instead of the store.

**A14 narrows accordingly.** It is not "add cell ids to a broken pile". It is:
bring `judge_fullctx`, `m7*` and `test_synth` up to what `judge_caveat` already
does, and prefer `LATTICE_CELL` over `results_subdir` because it carries model,
protocol and sampling in one value. The `judge_fullctx` question specifically
stays blocked, because that arm records nothing to attribute its 286 records by.

---

## Addendum — the provenance block this entry should have opened with

Appended 2026-09-27. The header of this entry cites "Queue B items B9 and B10",
which were bullets on a four-day working list, now deleted. **A finding does not
cite a todo list.** This log's own README says findings are not roadmap, and entries
13, 14 and 16 all open with the block below. This entry dropped it, and the queue
reference filled the hole where `Artifacts` belonged. The text above stands as
written; this supplies what was missing.

**Subject:** `nemotron3-nano-4b:latest`, the matrix sweep at `params.adapter`
`63b5b222daf4`, protocol `tools` v2, temperature 0.6 / top_p 0.95, `num_ctx` 16384,
n=1 per task. Plus a source reading over every arm in M6 and M7, which has no model.

**Recorded:** 2026-09-27.

**Artifacts:**
- *the two instruments* — `experiments/M6-evaluation-suite/m6_arms.py` and
  `experiments/M7-static-workflow/*_workflow.py`, grep `Current state still fails`;
  the arms that do NOT match are `baseline`, `monolith`, `monolith_recovery`.
- *the failed join* — `evalkit_store/index.jsonl`,
  `experiments/M7-static-workflow/stage_influence_*.jsonl`,
  `experiments/M6-evaluation-suite/results_matrix_nemotron3-nano-4b/`.
- *the corrected reader* — `experiments/M7-static-workflow/score_correlation_paired.py`,
  written here and superseding `score_correlation.py` for this question.

**Metric:** `objective_pass` per row; judge agreement against the check and against
the worker's own `terminal`, each over the same `(task, rep)` pairs.

**Verdict:** the ladder claim is confounded — established. The judge-versus-worker
question — not answerable from the files as they stood.
