"""E8's primary measure: rejections of check-passing candidates, per cell.

    python analyse.py                 # the measure, with the join self-validated
    python analyse.py --validate      # only the join's accuracy against truth
    python analyse.py --unresolved    # what could not be attributed, and why

A rejection is a judge candidate whose deterministic check was already full
(`check_full`) and whose verdict is nonetheless `not_met`. The rate is over
check-passing candidates, not over reps: a rep may put several candidates to
the judge, and a format that changes how many candidates survive to be judged
would otherwise move the denominator for a reason unrelated to the verdict.

WHY THIS NEEDS A JOIN AT ALL
----------------------------
Verdicts live only in `M7-static-workflow/stage_influence_<arm>.jsonl`. That
path is fixed per arm and ignores LATTICE_RESULTS_SUBDIR, and until 2026-09-21
the record named neither the model nor the judge format. Every run of an arm
appended to one file, so E8 -- whose entire variable IS the judge format --
pooled its own measure. Records written after that date carry `model`,
`judge_format`, `results_subdir` and `t_end`, and are used directly. Earlier
ones are attributed by joining to the store.

THE JOIN, AND WHY THE OBVIOUS VERSION IS WORSE THAN USELESS
-----------------------------------------------------------
Key: (arm, task, rep, terminal) plus agreement on wall_s and call count.

The first version required wall_s to match EXACTLY and resolved 60% of records.
That was not merely weak, it was biased: the workflow times itself internally
while run_suite times the whole arm call, so the two differ by 0.0-0.3s almost
always, and exact matching discarded most true pairs. Worse, a key stays
ambiguous precisely when both formats produced the same terminal for the same
task and rep -- the agreement case -- so dropping unresolved records removed
evidence of the formats behaving alike and manufactured differences. It put
nemotron's judge_bypass at +22.7 points when the answer is +4.3.

A 0.5s tolerance fixes both. Validated against the 856 records that carry real
stamps, holding those stamps back and asking the join to recover them:

    94.2% resolved | 0 wrong | 100.00% accurate among resolved

`--validate` re-runs that check. It is not decoration: the join is the only
reason the pre-2026-09-21 rows are usable, and a change to the suite, the store
or the workflows could silently break it. If accuracy is not 100%, no number
below this line can be trusted.

UNRESOLVED RECORDS ARE NOT A RESIDUAL
-------------------------------------
About a third of unstamped records do not resolve, far above the 5.8% seen on
stamped ones, because the file also holds runs from M7 experiments that predate
the store entirely. Those are correctly excluded. But the loss is uneven, and
one cell is destroyed by it: judge_anchored / qwen / decision_first resolves 9
reps out of 170 stored, because those rows were migrated from older M7 runs by
`seed_from_existing.py` and their stage records do not correspond. Cells below
`MIN_CANDIDATES` are withheld rather than printed with a wide interval, because
a rate on 31 candidates formats exactly like a rate on 400.
"""
from __future__ import annotations

import argparse
import collections
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "evalkit"))

from store import Store  # noqa: E402

M7 = ROOT / "experiments" / "M7-static-workflow"
ARMS = ("judge_anchored", "judge_bypass", "judge_caveat")
FORMATS = ("decision_first", "reason_first")
WALL_TOL_S = 0.5
MIN_CANDIDATES = 50


def short(model: str) -> str:
    return "nemo" if "nemo" in model else "qwen"


def store_index() -> dict:
    """(arm, task, rep, terminal) -> candidate store rows."""
    s = Store()
    cells = {}
    with (s.path / "index.jsonl").open(encoding="utf-8") as fh:
        for line in fh:
            e = json.loads(line)
            cells.setdefault(e["cell_id"], e)

    out = collections.defaultdict(list)
    for cid, e in cells.items():
        p = s.rows_dir / f"{cid}.jsonl"
        if not p.is_file():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            out[(e["arm"], r["task"], int(r["rep"]), r.get("terminal"))].append(
                {"model": e["model"], "fmt": e["judge_format"],
                 "wall": r.get("wall_s"), "calls": r.get("llm_calls")})
    return out


def stage_records() -> list[dict]:
    out = []
    for arm in ARMS:
        p = M7 / f"stage_influence_{arm}.jsonl"
        if not p.is_file():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            d = json.loads(line)
            d["_arm"] = arm
            out.append(d)
    return out


def join(index: dict, arm: str, d: dict) -> tuple | None:
    """(model, judge_format) for a stage record, or None when not certain.

    None covers two cases deliberately not distinguished by the caller: no
    store row within tolerance, and several rows within tolerance disagreeing
    about the setup. Both mean "this record cannot be assigned", and guessing
    either way is what the first version of this did.
    """
    cand = index.get((arm, d.get("task"), int(d.get("rep", 0)), d.get("terminal")), [])
    w, c = d.get("wall_s"), d.get("calls")
    if w is None:
        return None
    ok = [r for r in cand
          if r["wall"] is not None and abs(r["wall"] - w) <= WALL_TOL_S
          and (r["calls"] is None or c is None or r["calls"] == c)]
    tags = {(r["model"], r["fmt"]) for r in ok}
    return tags.pop() if len(tags) == 1 else None


def attribute(index: dict, records: list[dict]) -> tuple[dict, collections.Counter]:
    t = collections.defaultdict(lambda: {"full": 0, "rej": 0, "reps": 0})
    how = collections.Counter()
    for d in records:
        if d.get("judge_format") and d.get("model"):
            tag, how_ = (d["model"], d["judge_format"]), "stamped"
        else:
            tag = join(index, d["_arm"], d)
            how_ = "joined" if tag else "unresolved"
        how[how_] += 1
        if tag is None:
            continue
        k = (d["_arm"], short(tag[0]), tag[1])
        t[k]["reps"] += 1
        for c in (d.get("judge_candidates") or []):
            if c.get("check_full"):
                t[k]["full"] += 1
                if c.get("verdict") == "not_met":
                    t[k]["rej"] += 1
    return t, how


def ci(rej: int, n: int) -> tuple[float, float]:
    p = rej / n
    se = math.sqrt(p * (1 - p) / n)
    return 100 * max(0.0, p - 1.96 * se), 100 * min(1.0, p + 1.96 * se)


def validate(index: dict, records: list[dict]) -> bool:
    """Hold back the real stamps and ask the join to recover them."""
    truth = [d for d in records if d.get("judge_format") and d.get("model")]
    right = wrong = unres = 0
    for d in truth:
        got = join(index, d["_arm"], d)
        if got is None:
            unres += 1
        elif got == (d["model"], d["judge_format"]):
            right += 1
        else:
            wrong += 1
    n = len(truth)
    if not n:
        print("no stamped records: the join cannot be validated, so nothing below"
              " this line is trustworthy")
        return False
    acc = 100 * right / (right + wrong) if (right + wrong) else 0.0
    print(f"join validated on {n} stamped records: {100*right/n:.1f}% resolved, "
          f"{wrong} wrong, {acc:.2f}% accurate among resolved")
    if wrong:
        print("  *** the join is producing WRONG attributions; the measure below"
              " is not usable ***")
    return wrong == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--unresolved", action="store_true")
    args = ap.parse_args()

    index, records = store_index(), stage_records()
    ok = validate(index, records)
    if args.validate:
        return
    print()

    t, how = attribute(index, records)
    print(f"attribution: " + ", ".join(f"{k} {v}" for k, v in sorted(how.items())))
    print()

    print(f"{'arm':16s} {'model':5s} {'format':15s} {'reps':>5} {'cand':>5} "
          f"{'rate':>7}  95% CI")
    print("-" * 72)
    withheld = []
    for k in sorted(t):
        v = t[k]
        if v["full"] < MIN_CANDIDATES:
            withheld.append((k, v))
            continue
        lo, hi = ci(v["rej"], v["full"])
        print(f"{k[0]:16s} {k[1]:5s} {k[2]:15s} {v['reps']:5d} {v['full']:5d} "
              f"{100*v['rej']/v['full']:6.1f}%  [{lo:4.1f}, {hi:4.1f}]")
    if withheld:
        print()
        for k, v in withheld:
            print(f"withheld: {k[0]} / {k[1]} / {k[2]} -- {v['full']} candidates "
                  f"from {v['reps']} rep(s), under the {MIN_CANDIDATES} floor")

    print()
    print("decision_first -> reason_first, same arm and model:")
    for m in ("qwen", "nemo"):
        for arm in ARMS:
            a, b = t.get((arm, m, FORMATS[0])), t.get((arm, m, FORMATS[1]))
            if not (a and b and a["full"] >= MIN_CANDIDATES
                    and b["full"] >= MIN_CANDIDATES):
                continue
            ra, rb = 100*a["rej"]/a["full"], 100*b["rej"]/b["full"]
            la, ha = ci(a["rej"], a["full"])
            lb, hb = ci(b["rej"], b["full"])
            sep = ha < lb or hb < la
            print(f"  {m:5s} {arm:16s} {ra:5.1f}% -> {rb:5.1f}%  "
                  f"delta {rb-ra:+5.1f} pts   "
                  f"CIs {'SEPARATE' if sep else 'overlap'}")

    if args.unresolved:
        print()
        miss = collections.Counter()
        for d in records:
            if d.get("judge_format") and d.get("model"):
                continue
            if join(index, d["_arm"], d) is None:
                miss[(d["_arm"], d.get("terminal"))] += 1
        print("unresolved unstamped records, by arm and terminal:")
        for k, n in miss.most_common(15):
            print(f"  {n:4d}  {k[0]:16s} {k[1]}")

    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
