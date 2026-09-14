"""Paired per-scenario comparison across the M6 suite arms.

`10-evaluation-task-suite.md`: read per scenario rather than as totals. The arms
share a suite, so the pairing is available, and which tasks flip carries more than
a score difference because it names a condition rather than a magnitude.

    python compare_arms.py                    # all arms present
    python compare_arms.py dloop m7           # one pair, with the flip table
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RES = Path(__file__).resolve().parent.parent / "M6-evaluation-suite" / "results"
STAGE = Path(__file__).resolve().parent / "stage_influence.jsonl"
ORDER = ["monolith", "dloop", "staged", "m7"]


def load(arm):
    p = RES / f"{arm}.json"
    if not p.is_file():
        return None
    return {r["task"]: r for r in json.loads(p.read_text(encoding="utf-8"))}


def totals(arm, rows):
    dec = [r for r in rows.values() if r["decline_expected"]]
    return {
        "n": len(rows),
        "pass": sum(r["objective_pass"] for r in rows.values()),
        "regr": sum(r["regressed"] for r in rows.values()),
        "dec_ok": sum(r["declined_correctly"] for r in dec),
        "dec_n": len(dec),
        "false_dec": sum(1 for r in rows.values()
                         if r["terminal"] == "declined" and not r["decline_expected"]),
        "wall": sum(r["wall_s"] for r in rows.values()) / 60,
    }


def main():
    want = sys.argv[1:] or ORDER
    arms = {a: load(a) for a in want}
    arms = {a: r for a, r in arms.items() if r}

    print("## Totals\n")
    print("| arm | n | pass | regressions | decline | false declines | wall |")
    print("|---|---|---|---|---|---|---|")
    for a, rows in arms.items():
        t = totals(a, rows)
        print(f"| `{a}` | {t['n']} | {t['pass']}/{t['n']} | {t['regr']} | "
              f"{t['dec_ok']}/{t['dec_n']} | {t['false_dec']} | {t['wall']:.1f} min |")

    if len(want) == 2 and all(a in arms for a in want):
        a, b = want
        A, B = arms[a], arms[b]
        shared = sorted(set(A) & set(B))
        flips = [(t, A[t]["objective_pass"], B[t]["objective_pass"]) for t in shared
                 if A[t]["objective_pass"] != B[t]["objective_pass"]]
        print(f"\n## Flip table — `{a}` against `{b}` ({len(shared)} shared tasks)\n")
        if not flips:
            print("No flips. The arms agree per task and differ only in aggregate.\n")
        else:
            print(f"| task | stresses | `{a}` | `{b}` | {b} terminal |")
            print("|---|---|---|---|---|")
            for t, pa, pb in flips:
                print(f"| {t} | {','.join(B[t]['stresses'])} | "
                      f"{'pass' if pa else 'fail'} | {'pass' if pb else 'fail'} | "
                      f"{B[t]['terminal']} |")
            gained = [t for t, pa, pb in flips if pb and not pa]
            lost = [t for t, pa, pb in flips if pa and not pb]
            print(f"\n`{b}` gains {len(gained)}, loses {len(lost)}. "
                  f"Net {len(gained) - len(lost):+d}.\n")

    if STAGE.is_file() and "m7" in arms:
        recs = [json.loads(x) for x in STAGE.read_text(encoding="utf-8").splitlines() if x]
        recs = recs[-len(arms["m7"]):]          # last full run only
        fired = sum(r["s2_concern_split"]["fired"] for r in recs)
        agreed = sum(r["s2_concern_split"]["agreed"] for r in recs)
        syn = sum(r["s2_concern_split"]["signal_syntactic"] for r in recs)
        mod = sum(r["s2_concern_split"]["signal_model"] for r in recs)
        parsed = sum(r["s1_premise_audit"]["parsed"] for r in recs)
        conc = sum(r["influence"]["s1_concern_nonempty"] for r in recs)
        used = sum(bool(r["influence"]["s1_concern_consumed_by"]) for r in recs)
        cls_used = sum(bool(r["influence"]["s1_classification_consumed_by"]) for r in recs)
        calls = sum(r["calls"] for r in recs)
        print(f"\n## Stage influence — {len(recs)} tasks\n")
        print(f"- stage 1 parsed cleanly on **{parsed}/{len(recs)}**; "
              f"model calls total **{calls}** ({calls/len(recs):.1f}/task)")
        print(f"- stage 1 `concern` non-empty on **{conc}**, "
              f"**consumed on {used}** (escalation payloads only)")
        print(f"- stage 1 `multi_concern` consumed by the firing rule on **{cls_used}**")
        print(f"- stage 2 fired on **{fired}/{len(recs)}**; signals agreed on "
              f"**{agreed}/{len(recs)}** (syntactic {syn}, model {mod})")


if __name__ == "__main__":
    main()
