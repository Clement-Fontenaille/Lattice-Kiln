"""Does the judge track the check, or track the worker?

Every judge arm so far has been scored against the check. That says whether it is
right. It does not say **what it is a copy of**, and that is the question
`50-findings/11` finding 6 turns on: a judge holding the worker's context is predicted
to become a second sample of the worker rather than an independent reading.

The worker's own verdict is recorded on every run as a type-4 effect and is worthless
alone -- it says `answered` on 96% of tasks, +3 points over a constant. But as a
*reference series* it is exactly what a correlated judge would converge on.

So for each arm, three numbers over the same tasks:

    agreement with the CHECK     is it right?
    agreement with the WORKER    is it a copy of the worker?
    the gap between them         which one is it tracking?

A judge that is genuinely independent should sit above chance against the check and
near chance against the worker. One that has become a second sample should do the
reverse, and the diff-only arms give the baseline for how much of the agreement is
just both being usually correct on easy tasks.

    python score_correlation.py                 # every arm with a judge
    python score_correlation.py m7c judge_fullctx
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUITE = HERE.parent / "M6-evaluation-suite"
RES = SUITE / "results"

ARMS = {
    "m7c": ("runs_m7c", "juge-critique — diff only, 3 lines of context"),
    "m7e": ("runs_m7e", "juge-instruction — same context, different register"),
    "m7f": ("runs_m7f", "juge-orienté — same context, oriented"),
    "judge_anchored": ("runs_judge_anchored", "juge-ancré — conditions written before"),
    "judge_caveat": ("runs_judge_caveat", "juge-caveat"),
    "judge_bypass": ("runs_judge_bypass", "juge-bypass"),
    "judge_staged": ("runs_judge_staged", "juge-étagé"),
    "judge_fullctx": ("runs_judge_fullctx", "juge-contexte-complet — the worker's material"),
}


def worker_verdicts(runs_dir):
    """last terminal_state per run, keyed by the run's intent text"""
    out = {}
    for rj in sorted(glob.glob(str(HERE / runs_dir / "*" / "run.json"))):
        run = json.loads(Path(rj).read_text(encoding="utf-8"))
        ev = Path(rj).with_name("events.jsonl")
        if not ev.is_file():
            continue
        last = None
        for line in ev.read_text(encoding="utf-8").splitlines():
            e = json.loads(line)
            if e.get("kind") == "realized_effect" and e.get("effect_type") == 4:
                ts = (e.get("envelope") or {}).get("terminal_state")
                if ts:
                    last = ts
        if last:
            out[" ".join(run.get("intent_text", "").split())[:90]] = last
    return out


def main():
    want = sys.argv[1:] or list(ARMS)
    tasks = json.loads((SUITE / "tasks.json").read_text(encoding="utf-8"))["tasks"]
    obj = {t["id"]: " ".join(t["objective"].split()) for t in tasks}

    print("| arm | n | vs CHECK | vs WORKER | tracking |")
    print("|---|---|---|---|---|")
    for arm in want:
        if arm not in ARMS:
            continue
        runs_dir, label = ARMS[arm]
        stage = HERE / f"stage_influence_{arm}.jsonl"
        rp = RES / f"{arm}.json"
        if not (stage.is_file() and rp.is_file()):
            continue
        recs = [json.loads(x) for x in stage.read_text(encoding="utf-8").splitlines() if x]
        rows = {r["task"]: r for r in json.loads(rp.read_text(encoding="utf-8"))}
        wv = worker_verdicts(runs_dir)
        o2i = {v[:200]: k for k, v in obj.items()}

        n = vs_check = vs_worker = 0
        for r in recs:
            tid = o2i.get(r["task_objective"][:200])
            j = r.get("judge") or {}
            v = j.get("verdict")
            if not tid or tid not in rows or not v:
                continue
            w = wv.get(obj[tid][:90])
            if w is None:
                continue
            n += 1
            # both reduced to "is it done?" so the two series are comparable
            vs_check += (v == "met") == rows[tid]["objective_pass"]
            vs_worker += (v == "met") == (w == "answered")
        if not n:
            continue
        c, k = 100 * vs_check / n, 100 * vs_worker / n
        if abs(c - k) < 6:
            track = "neither clearly"
        else:
            track = "**the worker**" if k > c else "the check"
        print(f"| `{arm}` {label} | {n} | {c:.0f}% | {k:.0f}% | {track} |")

    print()
    print("**Read the gap, not the levels.** The worker says `answered` on 96% of "
          "tasks, so agreeing with it is easy for any arm that mostly says `met`. What "
          "separates a second sample from an independent reading is whether the arm "
          "agrees with the worker *more* than it agrees with the check — and how that "
          "gap moves when the judge is handed the worker's own material.")


if __name__ == "__main__":
    main()
