"""Re-run named tasks across every arm of a results tree, after a fixture change.

Why this exists (2026-09-19): `wf2_retry`'s `Client.calls` and
`hf_retry_backoff`'s `Sender.attempts` are asserted by their checks -- `calls`
must equal the number of fn() ATTEMPTS, 1/2/3/1 across the four cases that test
it -- but **no stage of the workflow is ever shown `test_task.py`**
(`_py_files()` excludes it). So the semantics were settled by the check and
invisible to the implementer, the audit and the judge alike.

On `judge_anchored`, `judge_bypass` and `judge_caveat` the judge rejected
check-passing candidates over exactly this, writing "no - calls attribute
increments by 1 per attempt, not total attempts" -- a sentence that describes
the required behaviour and labels it a failure. Those runs measured the gap in
the fixture, not the pipeline.

The fixtures now state the semantics in the source, which every stage does see.
This re-runs the affected tasks so the recorded rows come from the stated
fixture rather than the silent one.

    python rerun_tasks.py --plan
    python rerun_tasks.py --tree results --tasks wf2_retry hf_retry_backoff
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Per-tree environment. A tree is only re-runnable if we know how it was made.
TREES = {
    "results": {"LATTICE_BACKEND": "ollama",
                "LATTICE_EVAL_MODEL": "qwen2.5-coder:7b-instruct-q4_K_M",
                "LATTICE_RESULTS_SUBDIR": "results"},
    "results_nemotron_nothink": {"LATTICE_BACKEND": "ollama",
                                 "LATTICE_EVAL_MODEL": "nemotron-gpu",
                                 "LATTICE_THINK": "0",
                                 "LATTICE_MIN_PREDICT": "400",
                                 "LATTICE_RESULTS_SUBDIR": "results_nemotron_nothink"},
    "results_nemotron_think": {"LATTICE_BACKEND": "ollama",
                               "LATTICE_EVAL_MODEL": "nemotron-gpu",
                               "LATTICE_THINK": "1",
                               "LATTICE_MIN_PREDICT": "4096",
                               "LATTICE_RESULTS_SUBDIR": "results_nemotron_think"},
}
# results_nemotron is deliberately absent: it is the frozen record of the
# dark-stage condition that 50-findings/12 and /13 cite. Mixing fixture
# versions inside it would make those citations unreadable.


def reps_for(rows, tasks):
    """How many reps this arm ran, judged from the rows being replaced."""
    c = collections.Counter(r["task"] for r in rows if r["task"] in tasks)
    return max(c.values()) if c else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", default="results", choices=list(TREES))
    ap.add_argument("--tasks", nargs="+", default=["wf2_retry", "hf_retry_backoff"])
    ap.add_argument("--plan", action="store_true")
    args = ap.parse_args()

    tree = HERE / args.tree
    targets = set(args.tasks)
    plan = []
    for p in sorted(tree.glob("*.json")):
        rows = json.loads(p.read_text(encoding="utf-8"))
        # results/ also holds probe output (reasoning_budget.json), which is not
        # an arm file. An arm file is a list of rows carrying `task`.
        if not isinstance(rows, list) or not rows or "task" not in rows[0]:
            continue
        n = reps_for(rows, targets)
        if n:
            plan.append((p, n, sum(1 for r in rows if r["task"] in targets)))

    print(f"tree {args.tree}, tasks {' '.join(sorted(targets))}\n")
    print(f"{'arm':22s} {'reps':>5s} {'rows to replace':>16s}")
    for p, n, k in plan:
        print(f"{p.stem:22s} {n:5d} {k:16d}")
    print(f"\n{len(plan)} arms, {sum(k for _, _, k in plan)} rows")
    if args.plan:
        return

    t0 = time.monotonic()
    for i, (p, n, _) in enumerate(plan, 1):
        rows = json.loads(p.read_text(encoding="utf-8"))
        kept = [r for r in rows if r["task"] not in targets]
        p.write_text(json.dumps(kept, indent=2) + "\n", encoding="utf-8")

        env = {**os.environ, **TREES[args.tree]}
        cmd = [sys.executable, str(HERE / "run_suite.py"), "--arm", p.stem,
               "--reps", str(n), "--resume", "--tasks", *sorted(targets)]
        out = HERE / f"rerun_{args.tree}_{p.stem}.log"
        print(f"[{i}/{len(plan)}] {p.stem} reps={n} ...", flush=True)
        with out.open("a", encoding="utf-8") as fh:
            rc = subprocess.call(cmd, cwd=str(HERE), stdout=fh,
                                 stderr=subprocess.STDOUT, env=env)
        after = json.loads(p.read_text(encoding="utf-8"))
        got = sum(1 for r in after if r["task"] in targets)
        print(f"      -> exit {rc}, {got} rows, {(time.monotonic()-t0)/60:.0f} min",
              flush=True)
    print(f"\nDONE in {(time.monotonic()-t0)/60:.0f} min")


if __name__ == "__main__":
    main()
