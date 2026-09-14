"""Dense summary of every arm. Written to be read in a terminal without scrolling.

    python collect.py              # one line per arm
    python collect.py -j           # + judge block
    python collect.py -s           # + synthesised-witness funnel
    python collect.py -t TASK      # one task across every arm
    python collect.py -f           # flags only: what looks wrong

Columns: n=rows, R=reps, T=tasks, pass=mean objective_pass per rep (spread in
brackets), rg=regressions, dec=correct declines / expected, fd=false declines,
min=wall minutes, c/t=model calls per task.

**pass is a mean over reps and the bracket is the spread.** An arm varies by about
three tasks against itself at N=5, so two arms differing by less than that differ by
nothing (`50-findings/10`, finding 2). The bracket is there to stop the mean being
read as a point.
"""
from __future__ import annotations

import json
import statistics as st
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
STAGES = HERE.parent / "M7-static-workflow"
ORDER = ["baseline", "monolith", "dloop", "staged", "m7", "m7b", "m7c", "m7e", "m7f",
         "judge_anchored", "judge_caveat", "judge_bypass", "judge_staged",
         "judge_fullctx", "test_synth", "test_synth_retry"]


def load(arm):
    p = RES / f"{arm}.json"
    if not p.is_file():
        return None
    try:
        r = json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None
    return r or None


def summarise(arm, rows):
    by = defaultdict(list)
    for x in rows:
        by[x["task"]].append(x)
    reps = max(len(v) for v in by.values())
    per = [sum(1 for t in by if len(by[t]) > i and by[t][i]["objective_pass"])
           for i in range(reps)]
    dec = [x for x in rows if x["decline_expected"]]
    fd = sum(1 for x in rows if x["terminal"] == "declined" and not x["decline_expected"])
    return dict(n=len(rows), T=len(by), R=reps, mean=st.mean(per) if per else 0,
                lo=min(per) if per else 0, hi=max(per) if per else 0,
                rg=sum(x["regressed"] for x in rows),
                dok=sum(x["declined_correctly"] for x in dec), dn=len(dec),
                fd=fd, wall=sum(x["wall_s"] for x in rows) / 60)


def stage_recs(arm):
    p = STAGES / f"stage_influence_{arm}.jsonl"
    if not p.is_file():
        return []
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x]


def main():
    a = sys.argv[1:]
    want_j, want_s, want_f = "-j" in a, "-s" in a, "-f" in a
    task = a[a.index("-t") + 1] if "-t" in a else None

    live = [(k, load(k)) for k in ORDER]
    live = [(k, v) for k, v in live if v]

    if task:
        print(f"{task}")
        for k, rows in live:
            r = [x for x in rows if x["task"] == task]
            if not r:
                continue
            p = sum(x["objective_pass"] for x in r)
            tr = Counter(x["terminal"] for x in r).most_common(1)[0][0]
            print(f"  {k:<17} {p}/{len(r)}  {tr:<20} {st.mean([x['wall_s'] for x in r]):.0f}s")
        return

    if not want_f:
        print("arm                 n   T  R  pass          rg  dec   fd   min")
        for k, rows in live:
            s = summarise(k, rows)
            sp = f"[{s['lo']}-{s['hi']}]" if s["hi"] != s["lo"] else ""
            part = "*" if s["n"] < s["T"] * s["R"] else " "
            print(f"{k:<17}{part}{s['n']:>4}{s['T']:>4}{s['R']:>3}  "
                  f"{s['mean']:>4.1f}/{s['T']:<3}{sp:<8}{s['rg']:>2}  "
                  f"{s['dok']}/{s['dn']:<4}{s['fd']:>2}  {s['wall']:>5.0f}")
        print("* = partial")

    if want_j:
        print("\njudge               verdicts                       empty  n")
        for k, _ in live:
            recs = stage_recs(k)
            vs = [(r.get("judge") or {}) for r in recs]
            vs = [v for v in vs if v.get("verdict")]
            if not vs:
                continue
            c = Counter(v["verdict"] for v in vs)
            e = sum(1 for v in vs if v.get("diff_empty"))
            lab = " ".join(f"{n[:5]}={c[n]}" for n in ("met", "not_met", "unsound_request"))
            print(f"{k:<17} {lab:<30} {e:>4}  {len(vs)}")

    if want_s:
        print("\nsynth               parse  runs  discr  verdicts  rounds")
        for k, _ in live:
            recs = [r.get("synth") for r in stage_recs(k) if r.get("synth")]
            if not recs:
                continue
            w = [x for x in recs if x.get("written")]
            ran = [x for x in w if (x.get("on_pristine") or {}).get("ran")]
            d = [x for x in ran if x.get("discriminates")]
            v = sum(1 for x in recs if x.get("verdict"))
            rd = st.mean([x.get("rounds", x.get("tries", 1)) for x in recs])
            print(f"{k:<17} {len(w):>3}/{len(recs):<4} {len(ran):>3}/{len(w) or 1:<4} "
                  f"{len(d):>3}/{len(ran) or 1:<4} {v:>6}    {rd:>5.1f}")

    # flags: only things that look wrong
    msgs = []
    for k, rows in live:
        s = summarise(k, rows)
        err = sum(1 for x in rows if str(x["terminal"]).startswith("error"))
        if err:
            msgs.append(f"{k}: {err} error terminals")
        if s["rg"] and k not in ("monolith",):
            msgs.append(f"{k}: {s['rg']} regressions")
        if s["T"] not in (0,) and s["n"] < s["T"] * s["R"]:
            msgs.append(f"{k}: partial {s['n']}/{s['T']*s['R']}")
    sizes = {s for _, rows in live for s in [len({x['task'] for x in rows})]}
    if len(sizes) > 1:
        msgs.append(f"task counts differ across arms {sorted(sizes)} - suite versions "
                    f"are mixed, so means are not comparable; read a common subset")
    print("\n" + ("\n".join("! " + m for m in msgs) if msgs else "! none"))


if __name__ == "__main__":
    main()
