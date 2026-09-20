"""An experiment declares the cells it needs; the planner says what to run.

    needed - have = run

A declaration names arms, model configurations, judge formats, a task set and a
target rep count. The planner resolves each combination against the **current**
environment -- the arm sources as they are now, the suite version as it is now --
and asks the store what it already holds.

That resolution is the point. If an arm was edited, its `arm_sha` moves, the
resolved cell is a different cell, and prior rows correctly stop matching. The
alternative, which this replaces, was to notice the edit by hand or not at all.

Because a bare "no match" is useless, the planner also reports **near misses**:
store cells differing from a needed cell in exactly one field. That is the
difference between "you have no data" and "you have this data at a different
arm_sha, and here are both hashes" -- which is what a waiver is written against.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from setup_key import Cell, M6, ROOT, suite_version  # noqa: E402
from store import Store  # noqa: E402


def all_tasks() -> list[str]:
    d = json.loads((M6 / "tasks.json").read_text(encoding="utf-8"))
    return [t["id"] for t in d["tasks"]]


def _client_defaults() -> dict:
    """Settings a run would pick up without being told, so a declaration need
    not restate them. Mirrors run_suite._eval_params: the client is what turns
    an unset variable into a default, and the default is part of the setup."""
    import sys as _s
    _s.path.insert(0, str(ROOT / "experiments" / "M4-ephemeral-processors"))
    import ollama_client as _oc
    return {"num_ctx": _oc.DEFAULT_NUM_CTX}


def resolve(decl: dict) -> list[tuple[Cell, int]]:
    """Declaration -> concrete cells bound to the current environment."""
    defaults = _client_defaults()
    tasks = decl.get("tasks") or all_tasks()
    reps = int(decl["reps"])
    out = []
    for arm in decl["arms"]:
        for mname, m in decl["models"].items():
            for fmt in decl["judge_formats"]:
                for task in tasks:
                    out.append((Cell.make(
                        task=task, arm=arm, backend=m["backend"],
                        model=m["model"], judge_format=fmt,
                        params={**defaults, **m.get("params", {})}), reps))
    return out


def near_misses(cell: Cell, summary: dict, limit: int = 3) -> list[str]:
    """The closest store cells, and exactly which fields differ.

    Ranked by how few fields differ, not filtered to one: after an arm edit and
    a fixture bump, every candidate differs in two, and reporting nothing in
    that case is the least useful moment to report nothing. The whole value here
    is naming the fields, because that is what a waiver is written against and
    what tells you whether a re-run is really needed.
    """
    want = cell.as_dict()
    scored = []
    for a in summary.values():
        have = a["cell"]
        if have.get("task") != want["task"] or have.get("arm") != want["arm"]:
            continue                       # a different task or arm is not a near miss
        diff = [k for k in want if want[k] != have.get(k)]
        if diff:
            scored.append((len(diff), diff, have, a))
    scored.sort(key=lambda x: x[0])
    out = []
    for _, diff, have, a in scored[:limit]:
        fields = "; ".join(f"{k}: want {want[k]!r}, store {have.get(k)!r}" for k in diff)
        out.append(f"{a['n_reps']} reps ({'/'.join(a['provenance'])}) differ on -> {fields}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("declaration")
    ap.add_argument("--store", default=None)
    ap.add_argument("--require-recorded", action="store_true",
                    help="refuse rows whose setup was declared at migration "
                         "rather than recorded by the harness")
    ap.add_argument("--no-waivers", action="store_true",
                    help="ignore waivers.json and match on hashes alone")
    ap.add_argument("--explain", action="store_true",
                    help="for cells with no match, show near misses")
    args = ap.parse_args()

    decl = json.loads(Path(args.declaration).read_text(encoding="utf-8"))
    store = Store(Path(args.store) if args.store else None)
    wpath = HERE / "waivers.json"
    waivers = ([] if args.no_waivers or not wpath.is_file()
               else json.loads(wpath.read_text(encoding="utf-8"))["waivers"])
    summary = store.summary()
    cells = resolve(decl)

    print(f"{decl.get('name', 'experiment')}  |  suite {suite_version()}  |  "
          f"target N={decl['reps']}")
    print(f"store holds {len(summary)} cells\n")

    group = defaultdict(lambda: {"need": 0, "have": 0, "cells": 0, "short": []})
    for cell, reps in cells:
        have = min(store.have(cell, args.require_recorded, waivers), reps)
        key = (cell.arm, cell.model, cell.judge_format)
        g = group[key]
        g["cells"] += 1
        g["need"] += reps
        g["have"] += have
        if have < reps:
            g["short"].append(cell)

    print(f"{'arm':18s} {'model':34s} {'format':15s} {'have':>6s} {'need':>6s} {'to run':>7s}")
    total_run = total_need = 0
    for (arm, model, fmt), g in sorted(group.items()):
        run = g["need"] - g["have"]
        total_run += run
        total_need += g["need"]
        print(f"{arm:18s} {model:34s} {fmt:15s} {g['have']:6d} {g['need']:6d} {run:7d}")
    print(f"\n{'TOTAL':18s} {'':34s} {'':15s} "
          f"{total_need-total_run:6d} {total_need:6d} {total_run:7d}")
    pct = 100 * (total_need - total_run) / total_need if total_need else 0
    print(f"\nreusable from the store: {pct:.0f}%")

    if args.explain:
        print("\n--- why cells do not match (one field off) ---")
        shown = 0
        for (arm, model, fmt), g in sorted(group.items()):
            for cell in g["short"][:1]:
                nm = near_misses(cell, summary)
                if nm:
                    print(f"\n{arm} / {model} / {fmt}  (e.g. task {cell.task})")
                    for line in nm:
                        print(f"    {line}")
                    shown += 1
            if shown >= 6:
                break


if __name__ == "__main__":
    main()
