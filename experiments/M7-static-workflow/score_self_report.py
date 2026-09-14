"""Score the worker's own verdict on its own work. Costs nothing: already recorded.

The implementer's control block is mandatory and carries
`terminal_state: answered | blocked | declined` plus a prose `summary`. The runtime
records it as a **type-4 work-record mutation**, which is what
`10-technical/01-effect-vocabulary.md` says a processor's own recorded conclusion is.

The workflow then **discards it** -- `_pass` calls the implementer without capturing
the result -- because no lone model probe may produce a terminal
(`11-static-workflow.md`).

But discarding it for decisions is not a reason to leave it unscored. **It is the
cheapest possible judge**: the worker already answers the question the independent
judge is being built to answer, at zero extra calls, on every run ever made.

**A judge has to beat this to be worth anything**, and nothing had checked what this
is worth.

    python score_self_report.py                 # every arm with recorded runs
"""
from __future__ import annotations

import glob
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE.parent / "M6-evaluation-suite" / "results"
ARMS = {"m7": "runs", "m7b": "runs_m7b", "m7c": "runs_m7c",
        "m7e": "runs_m7e", "m7f": "runs_m7f"}


def truth_by_objective(arm):
    """task outcome, keyed by the first 90 chars of the objective (what run.json keeps)"""
    p = RES / f"{arm}.json"
    if not p.is_file():
        return {}
    tasks = json.loads((HERE.parent / "M6-evaluation-suite" / "tasks.json")
                       .read_text(encoding="utf-8"))["tasks"]
    obj = {t["id"]: " ".join(t["objective"].split()) for t in tasks}
    out = {}
    for r in json.loads(p.read_text(encoding="utf-8")):
        if r["task"] in obj:
            out[obj[r["task"]][:90]] = r
    return out


def self_reports(runs_dir):
    """last terminal_state per run, with the run's intent text"""
    out = []
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
            out.append((" ".join(run.get("intent_text", "").split())[:90], last))
    return out


def main():
    for arm, d in ARMS.items():
        reports = self_reports(d)
        if not reports:
            continue
        truth = truth_by_objective(arm)
        rows = [(t, r, truth[k]) for k, r in reports if (t := k) and k in truth]
        if not rows:
            print(f"### `{arm}` -- {len(reports)} self-reports, none matched to an "
                  f"outcome (the results file may be from a different suite version)\n")
            continue

        said = Counter(r for _, r, _ in rows)
        # the worker claims success; did the check agree?
        claims = [(r, tr["objective_pass"]) for _, r, tr in rows]
        said_ok = [p for v, p in claims if v == "answered"]
        said_not = [p for v, p in claims if v != "answered"]

        print(f"### `{arm}` -- {len(rows)} tasks with a self-report\n")
        print(f"- what it said: {dict(said)}")
        if said_ok:
            print(f"- said **answered** {len(said_ok)}x, and the check agreed "
                  f"**{sum(said_ok)}/{len(said_ok)}** "
                  f"({100*sum(said_ok)/len(said_ok):.0f}% precision on success)")
        if said_not:
            print(f"- said **not answered** {len(said_not)}x, and the check "
                  f"nonetheless passed {sum(said_not)}/{len(said_not)}")
        agree = sum(1 for v, p in claims if (v == "answered") == p)
        print(f"- overall agreement with the check: {agree}/{len(claims)} "
              f"({100*agree/len(claims):.0f}%)")
        # The comparison that matters: a predictor that always says `answered`
        # scores exactly the task pass rate. Anything at that level carries no
        # information, however high it looks.
        base = 100 * sum(p for _, p in claims) / len(claims)
        prec = 100 * sum(said_ok) / len(said_ok) if said_ok else 0
        rate = 100 * len(said_ok) / len(claims)
        print(f"- says `answered` on **{rate:.0f}%** of tasks")
        print(f"- **precision {prec:.0f}% against a base rate of {base:.0f}% "
              f"-- {prec-base:+.0f} points**")
        print()

    print("---\n")
    print("**Read the success-precision line, not the agreement line.** Agreement is "
          "inflated by every task where the worker said `answered` and was right for "
          "easy reasons. What a workflow would act on is: *when this says it is done, "
          "is it?* -- and that is the number an independent judge must beat while "
          "costing an extra call per candidate.")


if __name__ == "__main__":
    main()
