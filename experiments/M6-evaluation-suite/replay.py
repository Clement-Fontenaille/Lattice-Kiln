"""Re-derive the pass verdict on every recorded row, from data already on disk.

E0 defect 1, operator ruling 2026-09-18: **all dimensions gate.** `objective_pass`
had meant only "the check's exit code was 0", while several checks deliberately
keep their structural dimensions out of that exit code -- `wf6_multi`'s own
docstring calls them "quality signal, does not gate". Every downstream reader has
nonetheless read the field as "the task was done".

This is a **scoring** change, not a collection change. Every raw observation --
`SUBTESTS 5/5`, `STRUCTSCORE 0/3`, `DOCSCORE 2/4` -- is already recorded on every
row, so the new verdict is computable without re-running anything. Nothing
measured moves; only what is derived from it.

    gate_pass      = the check's exit code, the old `objective_pass`
    objective_pass = gate_pass AND every recorded dimension at full marks

Both are written, so prior figures stay reproducible and any analysis can say
which reading it used.

Idempotent, and safe to run while the queue is working: `run_suite.py --resume`
loads existing rows verbatim and writes them back, so fields added here survive a
later resume. An arm that is mid-flight when this runs will overwrite its own
file on completion; run this again afterwards to pick it up.

    python replay.py            # both result trees
    python replay.py --dry-run  # report what would change, write nothing
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TREES = ["results", "results_nemotron"]


def as_bool(v):
    if isinstance(v, bool) or v is None:
        return v
    if v == "True":
        return True
    if v == "False":
        return False
    raise ValueError(f"not a boolean: {v!r}")


def replay_row(r):
    """Returns (changed, note). Mutates r in place."""
    # Rows recorded before `run_ok` existed. The terminal is the evidence: an
    # arm that raised has one starting "error:", anything else ran. Backfilled so
    # every row carries the field and a downstream filter cannot silently treat a
    # failed run as an executed one.
    if "run_ok" not in r:
        r["run_ok"] = not str(r.get("terminal", "")).startswith("error")
    if not r.get("run_ok", True):
        # The arm raised: no attempt was made, so neither verdict is true of it.
        before = (r.get("gate_pass"), r.get("objective_pass"))
        r["gate_pass"] = None
        r["objective_pass"] = None
        return before != (None, None), "no-attempt"

    # The old objective_pass IS the gate reading, so it seeds gate_pass on rows
    # written before the split existed.
    gate = as_bool(r.get("gate_pass", r.get("objective_pass")))
    struct = r.get("struct") or {}
    met = bool(gate) and all(e == t for e, t in struct.values())

    changed = (r.get("gate_pass") != gate) or (as_bool(r.get("objective_pass")) != met)
    r["gate_pass"] = gate
    r["objective_pass"] = met
    return changed, ("demoted" if gate and not met else "")


def main():
    dry = "--dry-run" in sys.argv
    total = demoted = touched = 0
    print(f"{'file':44s} {'rows':>5s} {'demoted':>8s}")
    print("-" * 62)
    for tree in TREES:
        d = HERE / tree
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.json")):
            rows = json.loads(p.read_text(encoding="utf-8"))
            n = dem = 0
            for r in rows:
                changed, note = replay_row(r)
                n += 1
                if note == "demoted":
                    dem += 1
                if changed:
                    touched += 1
            total += n
            demoted += dem
            if not dry:
                p.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
            print(f"{tree + '/' + p.name:44s} {n:5d} {dem:8d}")
    print("-" * 62)
    print(f"{'TOTAL':44s} {total:5d} {demoted:8d}")
    print(f"\nrows whose stored verdict changed: {touched}")
    print("demoted = passed the gate, does not meet every dimension")
    if dry:
        print("\n--dry-run: nothing written")


if __name__ == "__main__":
    main()
