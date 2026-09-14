"""Score the judge against the check, on the two populations separately.

The traps were named in PREDICTION-M7C.md before the run and both are honoured here.

**Empty diffs are scored apart.** On an empty diff `not_met` is trivially right for any
task demanding work, and needs no judgement. If accuracy collapses once they are
removed, the judge is detecting emptiness -- which `len()` does for nothing.

**The base rate is shown beside every precision.** A constant "met" scores the task
pass rate. `score_self_report.py` found the worker sits +3 points above that, which is
the bar, and a raw precision above 80% can still be worthless.

    python score_judge.py m7c
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE.parent / "M6-evaluation-suite" / "results"
SUITE = HERE.parent / "M6-evaluation-suite"


def main():
    arm = sys.argv[1] if len(sys.argv) > 1 else "m7c"
    stage = HERE / f"stage_influence_{arm}.jsonl"
    if not stage.is_file():
        raise SystemExit(f"no stage log for {arm}")
    recs = [json.loads(x) for x in stage.read_text(encoding="utf-8").splitlines() if x]
    rows = {r["task"]: r for r in json.loads((RES / f"{arm}.json").read_text(encoding="utf-8"))}
    tasks = {t["id"]: t for t in json.loads((SUITE / "tasks.json").read_text(encoding="utf-8"))["tasks"]}
    obj2id = {" ".join(t["objective"].split())[:200]: i for i, t in tasks.items()}

    # ---- task-level verdict, against the check
    pop = {"all": [], "nonempty": []}
    for r in recs:
        tid = obj2id.get(r["task_objective"][:200])
        j = r.get("judge") or {}
        if not tid or tid not in rows or not j.get("verdict"):
            continue
        row, t = rows[tid], tasks[tid]
        # ground truth: the check passed -> "met"; a false-premise task the arm
        # correctly declined -> "unsound_request"; otherwise "not_met"
        if t["expect"]["decline_correct"] and row["terminal"] == "declined":
            truth = "unsound_request"
        else:
            truth = "met" if row["objective_pass"] else "not_met"
        entry = (tid, j["verdict"], truth, j.get("diff_empty"))
        pop["all"].append(entry)
        if not j.get("diff_empty"):
            pop["nonempty"].append(entry)

    print(f"## `{arm}` -- the judge's TASK-LEVEL verdict against the check\n")
    for name, rowset in pop.items():
        if not rowset:
            continue
        n = len(rowset)
        agree = sum(1 for _, v, tr, _ in rowset if v == tr)
        base = max(Counter(tr for _, _, tr, _ in rowset).values())
        said = Counter(v for _, v, _, _ in rowset)
        met = [tr for _, v, tr, _ in rowset if v == "met"]
        nm = [tr for _, v, tr, _ in rowset if v == "not_met"]
        label = "all tasks" if name == "all" else "**non-empty diffs only**"
        print(f"### {label} -- n={n}\n")
        print(f"- said: {dict(said)}")
        print(f"- agreement **{agree}/{n} ({100*agree/n:.0f}%)**, against a "
              f"best-constant baseline of {100*base/n:.0f}%")
        if met:
            print(f"- when it said `met`: right {sum(1 for x in met if x=='met')}/{len(met)}")
        if nm:
            print(f"- **when it said `not_met`: right "
                  f"{sum(1 for x in nm if x=='not_met')}/{len(nm)}** "
                  f"-- the number a workflow would act on")
        print()

    # ---- the cases that matter: judge against check, where they disagree
    print("### Where the judge contradicts the check\n")
    print("A judge earns its place only here. Elsewhere it repeats what the check "
          "already knew.\n")
    print("| task | judge | check | judge right? |")
    print("|---|---|---|---|")
    shown = 0
    for tid, v, truth, empty in pop["all"]:
        row = rows[tid]
        check_says = "met" if row["objective_pass"] else "not met"
        if (v == "met") != row["objective_pass"]:
            right = "**yes**" if v == truth else "no"
            print(f"| {tid} | {v} | {check_says} | {right} |")
            shown += 1
    if not shown:
        print("| — | — | — | it never contradicted the check |")

    # ---- candidate-level verdicts, if present
    cand = [v for r in recs for v in r.get("judge_candidates", []) if v.get("verdict")]
    if cand:
        c = Counter(v["verdict"] for v in cand)
        approve = 100 * c["met"] / len(cand)
        print(f"\n### Candidate-level verdicts -- n={len(cand)}\n")
        print(f"- {dict(c)}")
        print(f"- **approval rate {approve:.0f}%**, against the worker's own **96%** "
              f"on its own work (`score_self_report.py`). A judge reproducing the "
              f"worker's bias would measure the same thing twice.")


if __name__ == "__main__":
    main()
