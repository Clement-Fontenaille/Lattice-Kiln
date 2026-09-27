"""Does the judge track the check, or track the worker? -- joined per (task, rep).

Supersedes `score_correlation.py` for this question. That script asks the right
question and joins wrongly: `{r["task"]: r for r in rows}` collapses 170 result
rows to 34 (last rep wins), and `worker_verdicts()` keys on the objective's
first 90 characters, which collapses the same way. Per-rep judge verdicts were
then compared against ONE arbitrary rep's check outcome and worker verdict.

That is not a small error. The arms carry different rep counts -- 223 usable
records for `judge_fullctx` against 1374 for `judge_caveat` -- so the arm with
fewer reps suffers less mismatch and scores higher for that reason alone. The
reported 74% vs 50% spread is not interpretable.

The fix needs no new data. `stage_influence_*.jsonl` already carries `rep`, and
it already carries the worker's own verdict as `terminal`, so the fragile join
through intent text is unnecessary.

Three references per arm, over the same rows:

    vs CHECK      is the judge right?
    vs WORKER     is it a copy of the worker's self-report?
    vs CONSTANT   what does always-saying-the-majority-verdict score?

The third is the one that decides whether the first two mean anything. A judge
that cannot beat a constant is not judging, however its agreement reads.

    python score_correlation_paired.py
    python score_correlation_paired.py judge_fullctx judge_caveat
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "evalkit"))
from jsonl_read import load_jsonl  # noqa: E402  (tolerates a partial tail)

HERE = Path(__file__).resolve().parent
SUITE = HERE.parent / "M6-evaluation-suite"
RES = SUITE / "results"

ARMS = ["m7c", "m7e", "m7f", "judge_anchored", "judge_caveat", "judge_bypass",
        "judge_staged", "judge_fullctx"]


def load(arm: str):
    """(check, worker, judge) triples, one per (task, rep) that carries all three."""
    stage = HERE / f"stage_influence_{arm}.jsonl"
    rp = RES / f"{arm}.json"
    if not (stage.is_file() and rp.is_file()):
        return []
    rows = {}
    for r in json.loads(rp.read_text(encoding="utf-8")):
        # `objective_pass` is None when the arm raised: no attempt was made, so
        # neither "passed" nor "failed" is true of it and it cannot be a
        # reference. Dropped rather than coerced.
        if r.get("objective_pass") is None:
            continue
        rows[(r["task"], str(r["rep"]))] = bool(r["objective_pass"])
    out = []
    for rec in load_jsonl(stage):
        key = (rec.get("task"), str(rec.get("rep")))
        if key not in rows:
            continue
        verdict = (rec.get("judge") or {}).get("verdict")
        terminal = rec.get("terminal")
        if not verdict or not terminal:
            continue
        out.append((rows[key], terminal == "answered", verdict == "met"))
    return out


def main() -> None:
    want = [a for a in (sys.argv[1:] or ARMS)]
    print("| arm | n | judge says met | check pass | vs CHECK | best constant | "
          "lift | vs WORKER |")
    print("|---|---|---|---|---|---|---|---|")
    for arm in want:
        tri = load(arm)
        if not tri:
            continue
        n = len(tri)
        chk = sum(c for c, _, _ in tri)
        met = sum(j for _, _, j in tri)
        vs_check = sum((j == c) for c, _, j in tri)
        vs_worker = sum((j == w) for _, w, j in tri)
        # the best a verdict-blind predictor can do on this arm's own rows
        const = max(chk, n - chk)
        c = 100 * vs_check / n
        k = 100 * vs_worker / n
        b = 100 * const / n
        print(f"| `{arm}` | {n} | {100*met/n:.0f}% | {100*chk/n:.0f}% | "
              f"{c:.0f}% | {b:.0f}% | {c-b:+.0f} | {k:.0f}% |")
    print()
    print("**lift** is agreement with the check minus the best constant on the "
          "same rows. It is the only column in which a judge can earn anything.")


if __name__ == "__main__":
    main()
