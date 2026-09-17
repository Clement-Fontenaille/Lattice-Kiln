"""E7 — paired re-analysis of M4 vs M5 on the shared 4-task fixture.

Implements experiments/E7-paired-reanalysis/PROTOCOL.md. Stdlib only.
Run from anywhere: paths resolve against the repository root.
"""
from __future__ import annotations

import json
import collections
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
M4 = ROOT / "experiments/M4-ephemeral-processors/results/results.json"
M5 = ROOT / "experiments/M5-intelligent-orchestration/results/results.json"
OUT = Path(__file__).resolve().parent / "results"

# Published headline numbers, taken from the milestones' own summary.md files
# (M4-ephemeral-processors/results/summary.md, M5-intelligent-orchestration/
# results/summary.md), which name the arm for each number. The E7 sheet quotes
# the same totals as bare figures -- "M4 reported 5/8 against 6/8" -- without
# saying which arm scored which, so the sheet alone cannot source this table.
PUBLISHED = {
    "m4": {"monolith": (6, 8), "ephemeral": (5, 8)},
    "m5": {"monolith": (6, 8), "ephemeral": (5, 8), "orchestrated": (7, 8)},
}


def as_bool(v):
    """Booleans are stored as strings in some rows. bool('False') is True, so
    guessing here would silently invert the analysis."""
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        if v == "True":
            return True
        if v == "False":
            return False
    raise ValueError(f"not a boolean: {v!r}")


def load(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    meta = {}
    for r in rows:
        key = (r["task"], r["arm"], int(r["rep"]))
        out[key] = as_bool(r["objective_pass"])
        meta[key] = {"kind": r.get("kind")}
    return out, meta


def headline(passes):
    """Per-arm (passed, attempted), recomputed from rows."""
    agg = collections.defaultdict(lambda: [0, 0])
    for (task, arm, rep), ok in passes.items():
        agg[arm][1] += 1
        if ok:
            agg[arm][0] += 1
    return {arm: tuple(v) for arm, v in agg.items()}


def unstable_cells(passes):
    """(task, arm) cells whose reps disagree within one milestone."""
    byc = collections.defaultdict(list)
    for (task, arm, rep), ok in passes.items():
        byc[(task, arm)].append(ok)
    return {c for c, v in byc.items() if len(set(v)) > 1}


def main():
    m4, m4meta = load(M4)
    m5, _ = load(M5)

    h4, h5 = headline(m4), headline(m5)
    checks = []
    matches = True
    for label, got, want in (("m4", h4, PUBLISHED["m4"]), ("m5", h5, PUBLISHED["m5"])):
        for arm, expected in want.items():
            actual = got.get(arm)
            ok = actual == expected
            matches &= ok
            checks.append({
                "milestone": label, "arm": arm,
                "published": f"{expected[0]}/{expected[1]}",
                "recomputed": f"{actual[0]}/{actual[1]}" if actual else None,
                "match": ok,
            })

    u4, u5 = unstable_cells(m4), unstable_cells(m5)

    cells = []
    counts = collections.Counter()
    for key in sorted(set(m4) & set(m5)):
        task, arm, rep = key
        a, b = m4[key], m5[key]
        if (task, arm) in u4 or (task, arm) in u5:
            label = "unstable"
        elif a and not b:
            label = "lost"
        elif b and not a:
            label = "gained"
        elif a and b:
            label = "stable_pass"
        else:
            label = "stable_fail"
        counts[label] += 1
        cells.append({
            "task": task, "arm": arm, "rep": rep,
            "m4_pass": a, "m5_pass": b, "label": label,
            "kind": m4meta[key]["kind"],
        })

    m5_only = sorted({arm for (_, arm, _) in m5} - {arm for (_, arm, _) in m4})

    # Arms only in M5 cannot flip, so they are reported standalone: per task,
    # how the M5-only arm scored against the two shared arms in the same run.
    standalone = []
    for arm in m5_only:
        for task in sorted({t for (t, a, _) in m5 if a == arm}):
            row = {"task": task, "arm": arm}
            for other in sorted({a for (_, a, _) in m5}):
                reps = [m5[(task, other, r)] for r in (1, 2) if (task, other, r) in m5]
                row[other] = f"{sum(reps)}/{len(reps)}" if reps else None
            standalone.append(row)

    doc = {
        "schema": "e7-flip/1",
        "generated": datetime.now(timezone.utc).isoformat(),
        "sources": {"m4": str(M4.relative_to(ROOT)), "m5": str(M5.relative_to(ROOT))},
        "headline_check": {"checks": checks, "matches_published": matches},
        "arms_only_in_m5": m5_only,
        "m5_within_milestone": standalone,
        "cells": cells,
        "summary": dict(counts),
        "unstable_cells": {
            "m4": sorted(f"{t}/{a}" for t, a in u4),
            "m5": sorted(f"{t}/{a}" for t, a in u5),
        },
        "limitations": [
            "objective_pass is the gating metric only (E0 defect 1); M4/M5 records carry no structural dimensions to fold in",
            "stresses tags absent from M4/M5 records; kind used instead; tag-clustering question unanswerable from this data",
            "4 tasks x 2 reps per arm: any pattern is directional, not decisive",
            "the orchestrated arm exists only in M5 and therefore cannot flip",
        ],
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "flip_table.json").write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")

    lines = ["# E7 — M4 vs M5 flip table", "",
             f"Generated {doc['generated']}.", "",
             "## Headline check", "",
             "| milestone | arm | published | recomputed | match |",
             "|---|---|---|---|---|"]
    for c in checks:
        lines.append(f"| {c['milestone']} | {c['arm']} | {c['published']} | {c['recomputed']} | {'yes' if c['match'] else '**NO**'} |")
    lines += ["", f"**Matches published: {matches}**", "",
              "## Paired cells (arms present in both milestones)", "",
              "| task | arm | rep | M4 | M5 | label |", "|---|---|---|---|---|---|"]
    for c in cells:
        lines.append(f"| {c['task']} | {c['arm']} | {c['rep']} | {'pass' if c['m4_pass'] else 'fail'} | "
                     f"{'pass' if c['m5_pass'] else 'fail'} | {c['label']} |")
    lines += ["", "## Summary", ""]
    for k in ("gained", "lost", "stable_pass", "stable_fail", "unstable"):
        lines.append(f"- **{k}**: {counts.get(k, 0)}")
    lines += ["",
              f"Rep-unstable cells — M4: {', '.join(f'{t}/{a}' for t, a in sorted(u4)) or 'none'}",
              f"Rep-unstable cells — M5: {', '.join(f'{t}/{a}' for t, a in sorted(u5)) or 'none'}",
              ""]
    if standalone:
        arms = sorted({a for (_, a, _) in m5})
        lines += [f"## M5 within-milestone (arms only in M5: {', '.join(m5_only)})", "",
                  "Passes out of 2 reps.", "",
                  "| task | " + " | ".join(arms) + " |",
                  "|---|" + "---|" * len(arms)]
        seen = set()
        for row in standalone:
            if row["task"] in seen:
                continue
            seen.add(row["task"])
            lines.append(f"| {row['task']} | " + " | ".join(str(row.get(a)) for a in arms) + " |")
        lines.append("")
    lines += ["## Limitations", ""] + [f"- {x}" for x in doc["limitations"]]
    (OUT / "flip_table.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"headline matches published: {matches}")
    for c in checks:
        if not c["match"]:
            print(f"  MISMATCH {c['milestone']}/{c['arm']}: published {c['published']}, recomputed {c['recomputed']}")
    print("summary:", dict(counts))
    print("unstable cells m4:", sorted(u4), "m5:", sorted(u5))


if __name__ == "__main__":
    main()
