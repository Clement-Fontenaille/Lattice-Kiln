"""E8: what changes when the judge states its reasons before its verdict.

    python analyse.py                 # all three measures, join self-validated
    python analyse.py --validate      # only the join's accuracy against truth
    python analyse.py --unresolved    # what could not be attributed, and why

Three measures, reported together because the first one alone misleads.

1. REJECTIONS OF CHECK-PASSING CANDIDATES (PROTOCOL.md's primary measure).
   A candidate whose deterministic check was already full (`check_full`) and
   whose verdict is nonetheless `not_met`. Rate over check-passing candidates,
   not over reps: a rep may put several candidates to the judge, and a format
   that changes how many survive to be judged would otherwise move the
   denominator for a reason unrelated to the verdict.

2. CORRECT CHOICE (added 2026-09-22). Measure 1 counts every `not_met` on
   check-passing work as a defect, and some rejections are right -- the
   deterministic check is not the whole truth, since structural dimensions are
   non-gating (E0 defect 1). So this asks the question measure 1 only appears
   to: per rep, did the judge's FINAL verdict match what was actually
   delivered?

       normal task        truth = objective_pass (gate AND every structural
                          dimension). Correct = `met` when true, `not_met`
                          when false.
       false-premise task the right call is to refuse the work outright, so
                          correct = `unsound_request`.

   It splits measure 1's single number into false rejection and false
   acceptance, which move in opposite directions under this variable and are
   not interchangeable.

3. THE EMPTY-DIFF SPLIT (added 2026-09-22, corrected same day). judge_caveat
   is the only arm whose JUDGE prompt carries a block about how to weigh the
   per-condition tokens, and that block names one case explicitly: an empty
   diff, where every condition reads "no" whether the engineer failed or
   correctly refused. Splitting on `diff_empty` tests whether the arm's effect
   lands where its prompt says it should.

   The first version of this split reported a rejection RATE and was therefore
   uninterpretable -- it did not say whether rejecting an empty diff is right.
   It is not one question but two, and they have opposite answers:

       decline_expected  the request was unsound and doing nothing was the
                         correct engineering move. `not_met` punishes a correct
                         refusal and is WRONG; `unsound_request` is right.
       otherwise         the check passes only because the baseline already
                         did. The conditions really are unmet, so `not_met` is
                         DEFENSIBLE.

   Pooled, the two look identical and a correct 100% sits beside a wrong 100%.
   Split, nemotron's empty-diff rejections turn out to be entirely the second
   kind and are not a failure at all, while qwen's are largely the first.

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
evidence of the formats AGREEING and manufactured differences. It put
nemotron's judge_bypass at +22.7 points where the answer is +4.3.

A 0.5s tolerance plus call-count agreement fixes both, and `--validate` proves
it rather than asserting it: the records that carry real stamps have them held
back, and the join is asked to recover them. At 2026-09-22: 94.2% resolved, 0
wrong, 100.00% accurate among resolved.

That check runs on every invocation. The join is the only thing making the
older rows usable, and a change to the suite, the store or the workflows could
break it silently.

UNRESOLVED RECORDS ARE NOT A RESIDUAL
-------------------------------------
About a third of unstamped records do not resolve, far above the 5.8% seen on
stamped ones, because the file also holds runs from M7 experiments that predate
the store entirely. Those are correctly excluded. But the loss is uneven, and
one cell is destroyed by it: judge_anchored / qwen / decision_first resolves 9
reps out of 170 stored, because those rows were migrated from older M7 runs by
`seed_from_existing.py` and their stage records do not correspond. Cells under
the floors below are withheld rather than printed, because a rate on 31
candidates formats exactly like a rate on 400.
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
MIN_CANDIDATES = 50      # measure 1
MIN_REPS = 40            # measure 2, normal tasks
MIN_DECLINE = 15         # measure 2, false-premise tasks
MIN_SPLIT = 15           # measure 3


def short(model: str) -> str:
    return "nemo" if "nemo" in model else "qwen"


def ci(hits: int, n: int) -> tuple[float, float]:
    p = hits / n
    se = math.sqrt(p * (1 - p) / n)
    return 100 * max(0.0, p - 1.96 * se), 100 * min(1.0, p + 1.96 * se)


def store_index() -> dict:
    """(arm, task, rep, terminal) -> candidate store rows, tagged with setup."""
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
            r["_model"], r["_fmt"] = e["model"], e["judge_format"]
            out[(e["arm"], r["task"], int(r["rep"]), r.get("terminal"))].append(r)
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


def join(index: dict, arm: str, d: dict) -> dict | None:
    """The store row for a stage record, or None when not certain.

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
          if r.get("wall_s") is not None and abs(r["wall_s"] - w) <= WALL_TOL_S
          and (r.get("llm_calls") is None or c is None or r["llm_calls"] == c)]
    if len({(r["_model"], r["_fmt"]) for r in ok}) != 1:
        return None
    return ok[0]


def attribute(index: dict, records: list[dict]):
    """Yield (stage record, model short name, judge format, store row or None).

    A stamped record needs no store row for measures 1 and 3, so its row may be
    None there; measure 2 requires one and skips what it cannot get.
    """
    how = collections.Counter()
    for d in records:
        row = join(index, d["_arm"], d)
        if d.get("judge_format") and d.get("model"):
            model, fmt, how_ = d["model"], d["judge_format"], "stamped"
        elif row is not None:
            model, fmt, how_ = row["_model"], row["_fmt"], "joined"
        else:
            how["unresolved"] += 1
            continue
        how[how_] += 1
        yield d, short(model), fmt, row
    yield None, None, None, how


def collect(index, records):
    rej = collections.defaultdict(lambda: {"full": 0, "rej": 0, "reps": 0})
    split = collections.defaultdict(
        lambda: {"n": 0, "not_met": 0, "unsound": 0})
    corr = collections.defaultdict(collections.Counter)
    how = None
    for d, m, fmt, row in attribute(index, records):
        if d is None:
            how = row
            break
        k = (d["_arm"], m, fmt)
        rej[k]["reps"] += 1
        for c in (d.get("judge_candidates") or []):
            if not c.get("check_full"):
                continue
            rej[k]["full"] += 1
            bad = c.get("verdict") == "not_met"
            rej[k]["rej"] += bad
            # The split needs the task's ground truth, which only the store row
            # carries; a stamped record with no matching row is skipped here and
            # still counted in measure 1.
            if row is not None and c.get("diff_empty"):
                sk = k + (bool(row.get("decline_expected")),)
                split[sk]["n"] += 1
                split[sk]["not_met"] += bad
                split[sk]["unsound"] += (c.get("verdict") == "unsound_request")

        # measure 2 needs ground truth, which only the store row carries
        if row is None or not row.get("run_ok"):
            continue
        v = (d.get("judge") or {}).get("verdict")
        if v is None:
            corr[k]["unparseable"] += 1
            continue
        if row.get("decline_expected"):
            corr[k]["decline_n"] += 1
            corr[k]["decline_right"] += (v == "unsound_request")
        else:
            good = bool(row.get("objective_pass"))
            corr[k]["n"] += 1
            corr[k]["truth_good"] += good
            if good and v == "met":
                corr[k]["correct_accept"] += 1
            elif good:
                corr[k]["FALSE_REJECT"] += 1
            elif v == "not_met":
                corr[k]["correct_reject"] += 1
            else:
                corr[k]["FALSE_ACCEPT"] += 1
    return rej, corr, split, how


def validate(index, records) -> bool:
    truth = [d for d in records if d.get("judge_format") and d.get("model")]
    right = wrong = unres = 0
    for d in truth:
        row = join(index, d["_arm"], d)
        if row is None:
            unres += 1
        elif (row["_model"], row["_fmt"]) == (d["model"], d["judge_format"]):
            right += 1
        else:
            wrong += 1
    if not truth:
        print("no stamped records: the join cannot be validated, so nothing "
              "below this line is trustworthy")
        return False
    acc = 100 * right / (right + wrong) if (right + wrong) else 0.0
    print(f"join validated on {len(truth)} stamped records: "
          f"{100*right/len(truth):.1f}% resolved, {wrong} wrong, "
          f"{acc:.2f}% accurate among resolved")
    if wrong:
        print("  *** the join is producing WRONG attributions; nothing below "
              "is usable ***")
    return wrong == 0


def delta(label, cells, key, fmt_row):
    print()
    print(f"{label}:")
    for m in ("qwen", "nemo"):
        for arm in ARMS:
            a, b = cells.get((arm, m, FORMATS[0])), cells.get((arm, m, FORMATS[1]))
            line = fmt_row(arm, m, a, b)
            if line:
                print("  " + line)


def report_rejections(rej):
    print("1. REJECTIONS OF CHECK-PASSING CANDIDATES   (PROTOCOL.md primary)")
    print()
    print(f"{'arm':16s} {'model':5s} {'format':15s} {'reps':>5} {'cand':>5} "
          f"{'rate':>7}  95% CI")
    print("-" * 72)
    withheld = []
    for k in sorted(rej):
        v = rej[k]
        if v["full"] < MIN_CANDIDATES:
            withheld.append((k, v))
            continue
        lo, hi = ci(v["rej"], v["full"])
        print(f"{k[0]:16s} {k[1]:5s} {k[2]:15s} {v['reps']:5d} {v['full']:5d} "
              f"{100*v['rej']/v['full']:6.1f}%  [{lo:4.1f}, {hi:4.1f}]")
    for k, v in withheld:
        print(f"withheld: {k[0]} / {k[1]} / {k[2]} -- {v['full']} candidates "
              f"from {v['reps']} rep(s), under the {MIN_CANDIDATES} floor")

    def row(arm, m, a, b):
        if not (a and b and a["full"] >= MIN_CANDIDATES
                and b["full"] >= MIN_CANDIDATES):
            return None
        ra, rb = 100*a["rej"]/a["full"], 100*b["rej"]/b["full"]
        la, ha = ci(a["rej"], a["full"])
        lb, hb = ci(b["rej"], b["full"])
        sep = ha < lb or hb < la
        return (f"{m:5s} {arm:16s} {ra:5.1f}% -> {rb:5.1f}%  "
                f"delta {rb-ra:+5.1f} pts   "
                f"CIs {'SEPARATE' if sep else 'overlap'}")
    delta("decision_first -> reason_first", rej, None, row)


def report_correctness(corr):
    print("2. CORRECT CHOICE   (did the final verdict match what was delivered?)")
    print()
    print("normal tasks -- truth is objective_pass: the gate AND every "
          "structural dimension")
    print(f"{'arm':16s} {'model':5s} {'format':15s} {'n':>4} {'good':>5} "
          f"{'correct':>8} {'false rej':>10} {'false acc':>10} {'unparsed':>9}")
    print("-" * 88)
    for k in sorted(corr):
        c = corr[k]
        if c["n"] < MIN_REPS:
            continue
        n = c["n"]
        ok = c["correct_accept"] + c["correct_reject"]
        tot = n + c["decline_n"] + c["unparseable"]
        print(f"{k[0]:16s} {k[1]:5s} {k[2]:15s} {n:4d} {c['truth_good']:5d} "
              f"{100*ok/n:7.0f}% {100*c['FALSE_REJECT']/n:9.0f}% "
              f"{100*c['FALSE_ACCEPT']/n:9.0f}% "
              f"{100*c['unparseable']/tot if tot else 0:8.0f}%")
    print()
    print("false-premise tasks -- the right call is `unsound_request`")
    print(f"{'arm':16s} {'model':5s} {'format':15s} {'n':>4} {'right':>7}")
    print("-" * 56)
    for k in sorted(corr):
        c = corr[k]
        if c["decline_n"] < MIN_DECLINE:
            continue
        print(f"{k[0]:16s} {k[1]:5s} {k[2]:15s} {c['decline_n']:4d} "
              f"{100*c['decline_right']/c['decline_n']:6.0f}%")


def report_split(split):
    print("3. THE EMPTY-DIFF SPLIT   (was rejecting the empty diff correct?)")
    print()
    print("The judge_caveat prompt names this case: on an empty diff every")
    print("condition reads 'no' whether the engineer failed or correctly refused.")
    print()
    print("A. THE REQUEST WAS UNSOUND -- doing nothing was the right move.")
    print("   `not_met` punishes a correct refusal. Lower is better.")
    print(f"{'arm':16s} {'model':5s} {'format':15s} {'n':>4} {'not_met':>8} "
          f"{'unsound':>8} {'judge wrong':>12}")
    print("-" * 74)
    any_a = False
    for k in sorted(split):
        if not k[3]:
            continue
        c = split[k]
        n = c["n"]
        if n < MIN_SPLIT:
            continue
        any_a = True
        print(f"{k[0]:16s} {k[1]:5s} {k[2]:15s} {n:4d} {c['not_met']:8d} "
              f"{c['unsound']:8d} {100*c['not_met']/n:11.0f}%")
    if not any_a:
        print("(no cell reaches the floor)")
    print()
    print("B. THE REQUEST WAS SOUND -- the check passes only because the baseline")
    print("   already did, so the conditions really are unmet and `not_met` is")
    print("   defensible. A high rate here is NOT a defect.")
    print(f"{'arm':16s} {'model':5s} {'format':15s} {'n':>4} {'not_met':>8}")
    print("-" * 58)
    for k in sorted(split):
        if k[3]:
            continue
        c = split[k]
        n = c["n"]
        if n < MIN_SPLIT:
            continue
        print(f"{k[0]:16s} {k[1]:5s} {k[2]:15s} {n:4d} "
              f"{100*c['not_met']/n:7.0f}%")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--unresolved", action="store_true")
    args = ap.parse_args()

    index, records = store_index(), stage_records()
    ok = validate(index, records)
    if args.validate:
        return

    rej, corr, split, how = collect(index, records)
    print("attribution: " + ", ".join(f"{k} {v}" for k, v in sorted(how.items())))
    print()
    report_rejections(rej)
    print("\n" + "=" * 88 + "\n")
    report_correctness(corr)
    print("\n" + "=" * 88 + "\n")
    report_split(split)

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
