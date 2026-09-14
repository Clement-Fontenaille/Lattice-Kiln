"""Paired per-task analysis at N>1.

At N=1 a task is pass or fail. At N=5 it has a rate, and the rate is what
separates "this arm is better here" from "this task is noisy".

    python analyse_n5.py              # every arm present
    python analyse_n5.py dloop m7     # the pair, with the noise classification
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

RES = Path(__file__).resolve().parent.parent / "M6-evaluation-suite" / "results"
ORDER = ["monolith", "dloop", "staged", "m7"]
# the four that flipped between dloop and m7 at N=1 (findings entry 10, finding 2)
N1_FLIPS = ["hf_multi_recipient", "wf2_retry", "hf_cache_decorator", "wf5_partial"]


def load(arm):
    p = RES / f"{arm}.json"
    if not p.is_file():
        return None
    rows = json.loads(p.read_text(encoding="utf-8"))
    by = defaultdict(list)
    for r in rows:
        by[r["task"]].append(r)
    return by


def rate(rows):
    return sum(r["objective_pass"] for r in rows), len(rows)


def main():
    want = sys.argv[1:] or ORDER
    arms = {a: load(a) for a in want}
    arms = {a: v for a, v in arms.items() if v}
    if not arms:
        print("no results yet")
        return

    print("## Totals (per rep, so a mean and a spread rather than one number)\n")
    print("| arm | reps | mean pass /30 | min | max | regressions | decline | wall/rep |")
    print("|---|---|---|---|---|---|---|---|")
    for a, by in arms.items():
        nreps = max(len(v) for v in by.values())
        per_rep, regr, dec_ok, dec_n, wall = [], 0, 0, 0, 0.0
        for rep in range(1, nreps + 1):
            rows = [v[rep - 1] for v in by.values() if len(v) >= rep]
            per_rep.append(sum(r["objective_pass"] for r in rows))
        for v in by.values():
            for r in v:
                regr += r["regressed"]
                wall += r["wall_s"]
                if r["decline_expected"]:
                    dec_n += 1
                    dec_ok += r["declined_correctly"]
        m = statistics.mean(per_rep)
        print(f"| `{a}` | {nreps} | **{m:.1f}** | {min(per_rep)} | {max(per_rep)} | "
              f"{regr} | {dec_ok}/{dec_n} | {wall/60/nreps:.1f} min |")

    if len(want) == 2 and all(a in arms for a in want):
        a, b = want
        A, B = arms[a], arms[b]
        shared = sorted(set(A) & set(B))

        stable_both, noisy, arm_effect = [], [], []
        for t in shared:
            pa, na = rate(A[t])
            pb, nb = rate(B[t])
            fa, fb = pa / na, pb / nb
            if fa in (0.0, 1.0) and fb in (0.0, 1.0) and fa == fb:
                stable_both.append(t)
            elif fa in (0.0, 1.0) and fb in (0.0, 1.0) and fa != fb:
                arm_effect.append((t, pa, na, pb, nb))
            else:
                noisy.append((t, pa, na, pb, nb, abs(fa - fb)))

        print(f"\n## Per-task classification — `{a}` against `{b}`\n")
        print(f"- **stable and identical in both arms:** {len(stable_both)}/{len(shared)}")
        print(f"- **noisy in at least one arm:** {len(noisy)}")
        print(f"- **clean arm effect (0/N one side, N/N the other):** {len(arm_effect)}")

        if arm_effect:
            print(f"\n### Clean arm effects\n")
            print(f"| task | `{a}` | `{b}` |")
            print("|---|---|---|")
            for t, pa, na, pb, nb in arm_effect:
                print(f"| {t} | {pa}/{na} | {pb}/{nb} |")

        if noisy:
            print(f"\n### Noisy tasks, widest gap first\n")
            print(f"| task | `{a}` | `{b}` | gap |")
            print("|---|---|---|---|")
            for t, pa, na, pb, nb, g in sorted(noisy, key=lambda x: -x[5]):
                print(f"| {t} | {pa}/{na} | {pb}/{nb} | {g:.1f} |")

        print(f"\n### The four that flipped at N=1\n")
        print("Finding 2 predicted these are noisy in both arms rather than arm-sensitive.\n")
        print(f"| task | `{a}` | `{b}` | verdict |")
        print("|---|---|---|---|")
        for t in N1_FLIPS:
            if t not in A or t not in B:
                continue
            pa, na = rate(A[t])
            pb, nb = rate(B[t])
            mid = (0 < pa < na) or (0 < pb < nb)
            v = "noisy — prediction holds" if mid else "**NOT noisy — prediction fails**"
            print(f"| {t} | {pa}/{na} | {pb}/{nb} | {v} |")

    # regressions and declines, per arm, per task
    print("\n## Regressions by task\n")
    any_r = False
    for a, by in arms.items():
        for t, v in sorted(by.items()):
            n = sum(r["regressed"] for r in v)
            if n:
                any_r = True
                fails = sorted({f for r in v for f in r["new_fails"]})
                print(f"- `{a}` / **{t}** — {n}/{len(v)} reps; new failures: {fails}")
    if not any_r:
        print("None in any arm.")

    print("\n## Decline behaviour\n")
    for a, by in arms.items():
        bad = []
        for t, v in sorted(by.items()):
            d = sum(r["terminal"] == "declined" for r in v)
            if d and not v[0]["decline_expected"]:
                bad.append(f"{t} {d}/{len(v)}")
            if v[0]["decline_expected"] and d < len(v):
                bad.append(f"{t} MISSED {d}/{len(v)}")
        print(f"- `{a}` — false/missed declines: {', '.join(bad) if bad else 'none'}")


if __name__ == "__main__":
    main()
