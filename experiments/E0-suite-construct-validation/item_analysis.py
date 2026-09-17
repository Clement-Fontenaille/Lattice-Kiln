"""E0 — construct validation of the M6 suite.

Implements experiments/E0-suite-construct-validation/PROTOCOL.md parts 1-3.
numpy is used for eigenvalues only; everything else is stdlib.
"""
from __future__ import annotations

import json
import math
import random
import collections
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SUITE = ROOT / "experiments/M6-evaluation-suite"
RESULTS = SUITE / "results"
OUT = Path(__file__).resolve().parent / "results"

# The baseline arm makes no model call and changes no file. It is the
# untouched-source control, not a pipeline attempt, so it is excluded from the
# response matrix in part 3 (reported both ways).
CONTROL_ARM = "baseline"


def as_bool(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        if v == "True":
            return True
        if v == "False":
            return False
    raise ValueError(f"not a boolean: {v!r}")


def load_tasks():
    d = json.loads((SUITE / "tasks.json").read_text(encoding="utf-8"))
    return {t["id"]: t for t in d["tasks"]}


def load_arms():
    arms = {}
    for p in sorted(RESULTS.glob("*.json")):
        arms[p.stem] = json.loads(p.read_text(encoding="utf-8"))
    return arms


# ---------------------------------------------------------------- part 1

def part1_untouched_source(tasks, arms):
    """For every task, does the untouched source fail the check?"""
    rows = []
    for r in arms[CONTROL_ARM]:
        tid = r["task"]
        t = tasks.get(tid)
        if t is None:
            continue
        baseline_passes = as_bool(r["objective_pass"])
        # decline_correct True => doing nothing IS the answer (false-premise task)
        declining_is_correct = bool(t.get("expect", {}).get("decline_correct", False))
        demands_work = not declining_is_correct
        if baseline_passes and demands_work:
            verdict = "DEFECT_no_witness"
        elif baseline_passes and not demands_work:
            verdict = "correct_false_premise"
        elif not baseline_passes and demands_work:
            verdict = "correct_has_witness"
        else:
            verdict = "DEFECT_inverted"
        rows.append({"task": tid, "baseline_passes": baseline_passes,
                     "demands_work": demands_work, "verdict": verdict,
                     "shape": t.get("shape"), "trap": t.get("trap")})
    counts = collections.Counter(r["verdict"] for r in rows)
    return rows, counts


# ---------------------------------------------------------------- part 2

def part2_defect1_cost(arms):
    per_arm, per_task = {}, collections.Counter()
    for arm, rows in arms.items():
        compared = disagree = 0
        gated_pass = folded_pass = 0
        for r in rows:
            struct = r.get("struct") or {}
            if not struct:
                continue
            g = as_bool(r["objective_pass"])
            full = g and all(e == t for e, t in struct.values())
            compared += 1
            gated_pass += int(g)
            folded_pass += int(full)
            if g != full:
                disagree += 1
                per_task[r["task"]] += 1
        if compared:
            per_arm[arm] = {
                "rows_with_struct": compared,
                "gated_pass": gated_pass,
                "folded_pass": folded_pass,
                "gated_rate": round(gated_pass / compared, 3),
                "folded_rate": round(folded_pass / compared, 3),
                "flipped": disagree,
            }
    return per_arm, per_task


# ---------------------------------------------------------------- part 3

def build_matrix(arms, include_control):
    """rows = tasks, cols = (arm, rep) attempts, cell = objective_pass."""
    cells = collections.defaultdict(dict)
    cols = set()
    for arm, rows in arms.items():
        if not include_control and arm == CONTROL_ARM:
            continue
        for r in rows:
            col = (arm, int(r["rep"]))
            cols.add(col)
            cells[r["task"]][col] = as_bool(r["objective_pass"])
    tasks = sorted(cells)
    cols = sorted(cols)
    # keep only fully-observed columns so correlations are computed on a
    # rectangular matrix rather than on shifting support
    full_cols = [c for c in cols if all(c in cells[t] for t in tasks)]
    mat = np.array([[1.0 if cells[t][c] else 0.0 for c in full_cols] for t in tasks])
    return tasks, full_cols, mat


def point_biserial(mat):
    """Per item: correlation with the total over the OTHER items."""
    n_items = mat.shape[0]
    out = []
    totals = mat.sum(axis=0)
    for i in range(n_items):
        rest = totals - mat[i]
        x = mat[i]
        if x.std() == 0 or rest.std() == 0:
            out.append(None)
        else:
            out.append(float(np.corrcoef(x, rest)[0, 1]))
    return out


def parallel_analysis(mat, iters=500, seed=20260917):
    """Observed eigenvalues vs eigenvalues from random data of the same shape."""
    keep = mat[mat.std(axis=1) > 0]
    if keep.shape[0] < 3:
        return None
    obs = np.linalg.eigvalsh(np.corrcoef(keep))[::-1].real
    rng = random.Random(seed)
    n_items, n_subj = keep.shape
    sims = []
    for _ in range(iters):
        r = np.array([[1.0 if rng.random() < keep[i].mean() else 0.0
                       for _ in range(n_subj)] for i in range(n_items)])
        r = r[r.std(axis=1) > 0]
        if r.shape[0] < 3:
            continue
        sims.append(np.linalg.eigvalsh(np.corrcoef(r))[::-1].real[:len(obs)])
    if not sims:
        return None
    width = min(len(s) for s in sims)
    sim = np.percentile(np.array([s[:width] for s in sims]), 95, axis=0)
    obs = obs[:width]
    n_factors = int(np.sum(obs > sim))
    return {"observed": [round(float(v), 3) for v in obs[:10]],
            "random_p95": [round(float(v), 3) for v in sim[:10]],
            "n_factors": n_factors, "n_items_used": int(keep.shape[0])}


def main():
    tasks, arms = load_tasks(), load_arms()
    OUT.mkdir(exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()

    # ---- part 1
    rows1, counts1 = part1_untouched_source(tasks, arms)
    defects = [r for r in rows1 if r["verdict"].startswith("DEFECT")]
    lines = ["# E0 Part 1 — the untouched-source test", "", f"Generated {now}.", "",
             "For every task: does the untouched source fail its check? The `baseline`",
             "arm makes no model call and changes no file, so its rows are that run.", "",
             "| verdict | count |", "|---|---|"]
    for k, v in sorted(counts1.items()):
        lines.append(f"| {k} | {v} |")
    lines += ["", "## Tasks in a defect row", ""]
    if defects:
        lines += ["| task | shape | trap | baseline passes | demands work | verdict |",
                  "|---|---|---|---|---|---|"]
        for r in sorted(defects, key=lambda r: r["task"]):
            lines.append(f"| {r['task']} | {r['shape']} | {r['trap']} | {r['baseline_passes']} "
                         f"| {r['demands_work']} | {r['verdict']} |")
    else:
        lines.append("None.")
    lines += ["", "## What this test cannot do", "",
              "**Necessary, not sufficient.** A task whose demand has three clauses, two",
              "witnessed and one not, fails at baseline on the strength of the first two",
              "and reports nothing wrong here. The sufficient form is per clause."]
    (OUT / "untouched_source.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ---- part 2
    per_arm, per_task = part2_defect1_cost(arms)
    gated_order = sorted(per_arm, key=lambda a: -per_arm[a]["gated_rate"])
    folded_order = sorted(per_arm, key=lambda a: -per_arm[a]["folded_rate"])
    lines = ["# E0 Part 2 — what defect 1 costs", "", f"Generated {now}.", "",
             "`gated` = `objective_pass` as published. `folded` = also requires every",
             "structural dimension in `struct` to be at full marks.", "",
             "| arm | rows with struct | gated | folded | flipped |", "|---|---|---|---|---|"]
    for arm in sorted(per_arm):
        v = per_arm[arm]
        lines.append(f"| {arm} | {v['rows_with_struct']} | {v['gated_pass']} ({v['gated_rate']}) "
                     f"| {v['folded_pass']} ({v['folded_rate']}) | {v['flipped']} |")
    lines += ["", "## Does folding change arm ORDERING?", "",
              f"- gated order: {' > '.join(gated_order)}",
              f"- folded order: {' > '.join(folded_order)}",
              f"- **ordering changes: {gated_order != folded_order}**", "",
              "## Tasks accounting for the disagreements", ""]
    if per_task:
        lines += ["| task | rows flipped |", "|---|---|"]
        for t, c in per_task.most_common():
            lines.append(f"| {t} | {c} |")
    else:
        lines.append("None.")
    lines += ["", "## Coverage limit", "",
              "`struct` is populated on a minority of tasks per arm, so the folded score is",
              "computed on part of the suite and is **not** a corrected headline number.",
              "It is a sensitivity estimate."]
    (OUT / "defect1_cost.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ---- part 3
    report = {"schema": "e0-item/1", "generated": now}
    lines = ["# E0 Part 3 — item analysis", "", f"Generated {now}.", "",
             "## What these numbers can and cannot mean", "",
             "The \"subjects\" here are **scaffolds on one model**, not models of differing",
             "ability. Classical item analysis assumes subjects spanning an ability range.",
             "An item-total correlation computed over pipelines answers *\"does this item",
             "separate pipelines\"*, which is related to but not the same as *\"does this item",
             "measure the construct\"*. E4 is the experiment that would supply real ability",
             "spread; until it runs, every number here is about pipeline discrimination.", ""]

    for include_control in (False, True):
        tag = "with baseline" if include_control else "excluding baseline"
        titems, tcols, mat = build_matrix(arms, include_control)
        if mat.size == 0:
            continue
        diff = mat.mean(axis=1)
        pb = point_biserial(mat)
        pa = parallel_analysis(mat)
        floor = [titems[i] for i, d in enumerate(diff) if d == 0.0]
        ceil = [titems[i] for i, d in enumerate(diff) if d == 1.0]
        neg = [(titems[i], round(v, 3)) for i, v in enumerate(pb) if v is not None and v <= 0]
        report[tag] = {
            "n_items": len(titems), "n_attempts": len(tcols),
            "difficulty": {t: round(float(d), 3) for t, d in zip(titems, diff)},
            "item_total_r": {t: (round(v, 3) if v is not None else None)
                             for t, v in zip(titems, pb)},
            "zero_variance_floor": floor, "zero_variance_ceiling": ceil,
            "non_positive_discrimination": neg,
            "parallel_analysis": pa,
        }
        lines += [f"## Response matrix — {tag}", "",
                  f"- items (tasks): **{len(titems)}**",
                  f"- attempts (arm x rep, fully observed): **{len(tcols)}**", "",
                  "### Difficulty distribution", "",
                  f"- at the **floor** (no attempt passes, zero variance): {len(floor)} — "
                  f"{', '.join(floor) if floor else 'none'}",
                  f"- at the **ceiling** (every attempt passes, zero variance): {len(ceil)} — "
                  f"{', '.join(ceil) if ceil else 'none'}",
                  f"- **discriminating items** (0 < p < 1): {len(titems) - len(floor) - len(ceil)}",
                  "", "### Item-total correlation", "",
                  "Items with correlation <= 0 — where *better* attempts do *worse*. "
                  "The classic broken-check signal.", ""]
        if neg:
            lines += ["| task | r |", "|---|---|"] + [f"| {t} | {v} |" for t, v in sorted(neg, key=lambda x: x[1])]
        else:
            lines.append("None.")
        lines += ["", "### Dimensionality (parallel analysis, 95th percentile)", ""]
        if pa:
            lines += [f"- items with variance used: **{pa['n_items_used']}**",
                      f"- **factors retained: {pa['n_factors']}**", "",
                      "| # | observed | random p95 |", "|---|---|---|"]
            for i, (o, s) in enumerate(zip(pa["observed"], pa["random_p95"]), 1):
                lines.append(f"| {i} | {o} | {s} |")
        else:
            lines.append("Not computable — too few items with variance.")
        lines.append("")

    (OUT / "item_analysis.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT / "item_analysis.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print("part1:", dict(counts1))
    print("part1 defects:", [r["task"] for r in defects])
    print("part2 ordering changes:", gated_order != folded_order)
    print("part2 flipped tasks:", dict(per_task))
    key = "excluding baseline"
    if key in report:
        r = report[key]
        print(f"part3 ({key}): items={r['n_items']} attempts={r['n_attempts']} "
              f"floor={len(r['zero_variance_floor'])} ceiling={len(r['zero_variance_ceiling'])} "
              f"neg_r={len(r['non_positive_discrimination'])} "
              f"factors={(r['parallel_analysis'] or {}).get('n_factors')}")


if __name__ == "__main__":
    main()
