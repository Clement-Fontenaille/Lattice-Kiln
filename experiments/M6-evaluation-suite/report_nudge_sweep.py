"""Read the nudge sweep out of the store, grouped by adapter fingerprint.

Read from the STORE, not from results/*.json. The three sweep arms run
concurrently and every one of them writes results/judge_anchored.json, so that
file holds whichever process finished last. The store is per-cell and appended,
so it is the only honest source here.

Grouped by `params.adapter`, which is what makes the arms distinguishable at
all: the nudge text feeds adapter_fingerprint(), so a nudged row and an
unnudged one carry different adapters and cannot pool. Rows are matched back to
their nudge by recomputing the fingerprint for each candidate text.

RUN_OK IS THE HEADLINE, NOT AN ASIDE. A truncated run produced no attempt, so
its workspace is untouched and scoring it measures the fixture rather than the
model. Those rows are excluded from pass rates everywhere -- which means a
pass rate alone is computed over survivors and says nothing about how many
runs died. Both are reported, and the pass rate is meaningless without the
completion rate beside it.

    python report_nudge_sweep.py [--task wf2_retry] [--arm judge_anchored]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "evalkit"))
from jsonl_read import load_jsonl  # noqa: E402  (tolerates a partial tail)

ROOT = Path(__file__).resolve().parents[2]
STORE = ROOT / "evalkit_store"
M4 = ROOT / "experiments" / "M4-ephemeral-processors"

NUDGES = {
    "control": "",
    "first_pass": "Form a judgement on the first pass and write it.",
    "answer_first": ("Write your answer FIRST, then stop. Any reasoning you do "
                     "must fit in a few sentences before it."),
}


def fingerprint_for(nudge: str) -> str:
    """adapter_fingerprint() under a given nudge, in a clean interpreter.

    A subprocess because the fingerprint reads module-level state set from the
    environment at import; re-importing in-process would return whatever the
    first import captured.
    """
    env = dict(os.environ)
    env["LATTICE_NUDGE"] = nudge
    env["LATTICE_PROTOCOL"] = "tools"
    out = subprocess.run(
        [sys.executable, "-c",
         "import sys;sys.path.insert(0,r'%s');import processor;"
         "print(processor.adapter_fingerprint())" % M4],
        capture_output=True, text=True, env=env, check=True)
    return out.stdout.strip()


def load(task: str, arm: str) -> list[dict]:
    idx = load_jsonl(STORE / "index.jsonl")
    out, seen = [], set()
    for r in idx:
        if r.get("arm") != arm or r.get("task") != task:
            continue
        p = json.loads(r.get("params") or "{}")
        # Payload files are keyed by CELL, not by row_sha, and each holds every
        # rep of that cell. An index entry is written per rep, so the same file
        # is reached repeatedly -- dedupe on (cell, rep) or a ten-rep cell is
        # counted ten times over.
        f = STORE / "rows" / f"{r['cell_id']}.jsonl"
        if not f.exists():
            continue
        for d in load_jsonl(f):
            key = (r["cell_id"], d.get("rep"))
            if key in seen:
                continue
            seen.add(key)
            d["_adapter"] = p.get("adapter")
            out.append(d)
    return out


def main(argv: list[str]) -> None:
    task, arm = "wf2_retry", "judge_anchored"
    if "--task" in argv:
        task = argv[argv.index("--task") + 1]
    if "--arm" in argv:
        arm = argv[argv.index("--arm") + 1]

    fps = {name: fingerprint_for(text) for name, text in NUDGES.items()}
    rows = load(task, arm)
    print(f"{arm} / {task} -- {len(rows)} stored rows\n")
    print(f"  {'nudge':13} {'adapter':13} {'runs':>5} {'completed':>10} "
          f"{'truncated':>10} {'pass':>8} {'subtests':>9} {'gen_tok':>9} {'wall_s':>8}")
    for name, fp in fps.items():
        rs = [r for r in rows if r.get("_adapter") == fp]
        if not rs:
            print(f"  {name:13} {fp:13} {'-':>5}  (no rows)")
            continue
        ok = [r for r in rs if r.get("run_ok")]
        trunc = len(rs) - len(ok)
        passed = sum(1 for r in ok if r.get("objective_pass"))
        # final_sub is [passed, total], not a scalar. Reported as a fraction so
        # a task with a different subtest count stays comparable.
        sub = [v[0] / v[1] for r in ok
               if isinstance(v := r.get("final_sub"), list) and len(v) == 2 and v[1]]
        tok = [r.get("gen_tok", 0) for r in ok]
        wall = [r.get("wall_s", 0) for r in ok]
        print(f"  {name:13} {fp:13} {len(rs):>5} "
              f"{len(ok):>10} {trunc:>10} "
              f"{(str(passed) + '/' + str(len(ok))):>8} "
              f"{(sum(sub) / len(sub) if sub else 0):>9.2f} "
              f"{(sum(tok) / len(tok) if tok else 0):>9.0f} "
              f"{(sum(wall) / len(wall) if wall else 0):>8.1f}")
    print("\n  completed = run_ok, i.e. the arm did not raise. A truncated run "
          "left the\n  workspace untouched, so its score would measure the "
          "fixture and is excluded.\n  A pass rate is over SURVIVORS and means "
          "nothing without the truncation count.")


if __name__ == "__main__":
    main(sys.argv[1:])
