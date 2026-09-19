"""Seed E8's decision_first cells from runs already recorded at the same setup.

`decision_first` IS the contract every run before 2026-09-19 used, so rows
already on disk are valid E8 observations provided the setup matches exactly.
Verified before copying:

  * **format** - decision_first. `judge_format.apply()` returns the prompt
    unchanged in that mode, and the three arm files were diffed against their
    pre-patch versions: the only changes are the import and the hook itself.
  * **model and params** - qwen rows carry no `think` key, matching E8's qwen
    env; nemotron rows come from `results_nemotron_nothink`, which is
    LATTICE_THINK=0 with MIN_PREDICT=400, exactly E8's nemo env.
  * **arm code** - judge_bypass changed at 31a5000 (the rotated-argument fix);
    its surviving rows are from the post-fix re-run. judge_anchored and
    judge_caveat last changed 2026-09-14, before their rows were recorded.
  * **suite** - 0.4.1. The 2026-09-19 fixture repair touched only wf2_retry and
    hf_retry_backoff; this script REFUSES to seed a tree whose rows for those
    two tasks predate the repair, because those rows were produced against a
    fixture that did not state its counter semantics.

Rows are copied, not moved. The source trees stay as the record findings 12 and
13 cite.

    python seed_from_existing.py --check    # report only
    python seed_from_existing.py
"""
from __future__ import annotations

import argparse
import collections
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
M6 = HERE.parent / "M6-evaluation-suite"
ARMS = ["judge_anchored", "judge_bypass", "judge_caveat"]
REPAIRED = {"wf2_retry", "hf_retry_backoff"}
REQUIRED_SUITE = "0.4.1"

SOURCES = {
    "qwen": M6 / "results",
    "nemo": M6 / "results_nemotron_nothink",
}


def audit(model, arm):
    src = SOURCES[model] / f"{arm}.json"
    if not src.is_file():
        return None, "absent"
    rows = [r for r in json.loads(src.read_text(encoding="utf-8")) if r.get("run_ok")]
    if not rows:
        return None, "no executed rows"
    reps = max(collections.Counter(r["task"] for r in rows).values())
    # The fixture repair must already be in these rows, or the seeded cell mixes
    # a stated fixture with a silent one on the two tasks that changed. Checked
    # on the row's own `suite_version`, not on the task being present: the stale
    # rows carry those tasks too, which is why the first version of this check
    # passed a tree whose repair had not run.
    stale = sorted({r["task"] for r in rows
                    if r["task"] in REPAIRED
                    and r.get("suite_version") != REQUIRED_SUITE})
    if stale:
        return None, (f"{', '.join(stale)} not on suite {REQUIRED_SUITE} "
                      f"- run rerun_tasks.py for this tree first")
    return (rows, reps), "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    print(f"{'model':6s} {'arm':16s} {'reps':>5s} {'rows':>6s}  status")
    plan = []
    for model in SOURCES:
        for arm in ARMS:
            got, status = audit(model, arm)
            if got:
                rows, reps = got
                print(f"{model:6s} {arm:16s} {reps:5d} {len(rows):6d}  {status}")
                plan.append((model, arm, rows, reps))
            else:
                print(f"{model:6s} {arm:16s} {'-':>5s} {'-':>6s}  {status}")

    if args.check:
        print("\n--check: nothing written")
        return
    if len(plan) != len(SOURCES) * len(ARMS):
        print("\nREFUSING to seed: not every cell is clean (see status above).")
        sys.exit(1)

    for model, arm, rows, reps in plan:
        dest_dir = HERE / "results" / f"{model}_decision_first"
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / f"{arm}.json"
        dest.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
        md = SOURCES[model] / f"{arm}.md"
        if md.is_file():
            shutil.copy2(md, dest_dir / f"{arm}.md")
        print(f"seeded {model}_decision_first/{arm}.json  {len(rows)} rows, reps={reps}")

    print("\nThe queue tops these up to N=5 with --resume; reason_first runs from zero.")


if __name__ == "__main__":
    main()
