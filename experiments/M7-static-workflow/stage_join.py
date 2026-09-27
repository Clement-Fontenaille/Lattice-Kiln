"""Join stage records to store rows on cell id -- the A14 check.

    python stage_join.py                       # every stage_influence_*.jsonl
    python stage_join.py --arm judge_fullctx
    python stage_join.py --store <dir> --stage-dir <dir>

A stage record written since A14 carries `cell_id` (see stage_tags.py). This
groups records by it and checks two things per group:

  1. the group is ONE setup: the store index gives each cell id exactly one
     model, backend and params (protocol, sampling, adapter); a group whose
     cell id maps to more than one of any of those fails.
  2. the join is exact: the store holds as many reps for the cell as the
     group has records.

Records without `cell_id` predate A14. They are counted and reported as
unattributable, and nothing here tries to attribute them -- guessing is what
50-findings/17 showed to be wrong.

Exit status: 0 when every attributable group passes both checks, 1 when any
fails, 2 when no record is attributable at all.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "evalkit"))
from jsonl_read import load_jsonl  # noqa: E402  (tolerates a partial tail)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def check(store: Path, stage_dir: Path, arms: list[str] | None = None) -> int:
    index = defaultdict(list)
    for e in load_jsonl(store / "index.jsonl"):
        index[e["cell_id"]].append(e)

    files = sorted(stage_dir.glob("stage_influence*.jsonl"))
    if arms:
        files = [f for f in files if f.stem.removeprefix("stage_influence_") in arms]
    bad = n_groups = 0
    print(f"{'stage file':44} {'records':>7} {'untagged':>8} {'cells':>5} "
          f"{'single-setup':>12} {'n==store':>8}")
    for f in files:
        recs = list(load_jsonl(f))
        groups = defaultdict(list)
        untagged = 0
        for r in recs:
            if r.get("cell_id"):
                groups[r["cell_id"]].append(r)
            else:
                untagged += 1
        single = joined = 0
        problems = []
        for cid, g in sorted(groups.items()):
            entries = index.get(cid, [])
            setups = {(e["model"], e["backend"], e["params"]) for e in entries}
            rec_models = {r.get("model") for r in g}
            if len(setups) == 1 and len(rec_models) == 1:
                single += 1
            else:
                problems.append(f"  {cid}: {len(setups)} store setup(s), "
                                f"record models {sorted(map(str, rec_models))}")
            n_store = len({e["rep"] for e in entries})
            if n_store == len(g):
                joined += 1
            else:
                problems.append(f"  {cid}: {len(g)} record(s), store holds {n_store} rep(s)")
        print(f"{f.name:44} {len(recs):>7} {untagged:>8} {len(groups):>5} "
              f"{single:>5}/{len(groups):<6} {joined:>3}/{len(groups):<4}")
        for p in problems:
            print(p)
        bad += len(problems)
        n_groups += len(groups)
    if not n_groups:
        print("\nNOTHING TO CHECK: no record carries a cell_id. Untagged records "
              "predate A14 and are not attributable.")
        return 2
    print(f"\n{'PASS' if not bad else 'FAIL'}: {bad} problem(s) across {n_groups} "
          "attributable group(s). Untagged records predate A14 and are not attributable.")
    return 0 if not bad else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", default=str(ROOT / "evalkit_store"))
    ap.add_argument("--stage-dir", default=str(HERE))
    ap.add_argument("--arm", nargs="*")
    a = ap.parse_args()
    sys.exit(check(Path(a.store), Path(a.stage_dir), a.arm))


if __name__ == "__main__":
    main()
