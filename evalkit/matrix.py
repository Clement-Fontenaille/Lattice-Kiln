"""The model x arm matrix, read from the store.

    python matrix.py                              # every population in the store
    python matrix.py --protocol tools --adapter 63b5b222daf4
    python matrix.py --model nemotron3-nano-4b:latest --arm monolith dloop
    python matrix.py --store <dir>

From the STORE, never from job logs or results/*.json. Logs under-report
because --store-resume skips cells that are already held, and a results file
holds whichever sweep wrote it last.

ONE LINE PER POPULATION, NOT PER (model, arm). Two rows under the same model and
arm but a different adapter, protocol, sampling, backend, judge format or arm
version are different populations (50-findings/15, /17), and pooling them is
the error this reader exists to prevent. Each line therefore carries a `setup`
label -- a short hash of every cell field except task and fixture -- and a
(model, arm) that appears with more than one setup is printed more than once,
never summed.

DENOMINATORS, stated once and used everywhere:

    n         distinct (cell_id, rep) with a row on disk. Deduplicated: the index
              has one entry per rep but a row file holds every rep of its cell.
    run_ok    of n, how many the arm did not raise on.
    pass      objective_pass, over run_ok.
    regr      regressed, over run_ok.
    crash     check_crashed, over run_ok.
    tool_*    counters SUMMED over the run_ok rows, i.e. the same rows as pass.

Rows whose arm raised produced no attempt; their workspace is the fixture, so
every rate excludes them and `run_ok` says how many that was.

Index entries whose row file is not on disk (a partial clone carries the index
but not every row file) are counted as `missing` and excluded, not guessed at.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from jsonl_read import load_jsonl  # noqa: E402
from setup_key import MARKERS_ADAPTER  # noqa: E402

DEFAULT_STORE = HERE.parent / "evalkit_store"
TOOL = ("tool_native", "tool_recovered", "tool_repaired", "tool_malformed")
# Every cell field that makes two rows different populations. Task and fixture
# are deliberately absent: they vary WITHIN a population, by design.
SETUP_FIELDS = ("backend", "model", "arm", "arm_sha", "prompt_sha",
                "judge_format", "params")


def setup_label(entry: dict) -> str:
    key = json.dumps({k: entry.get(k) for k in SETUP_FIELDS}, sort_keys=True)
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:8]


def params_of(entry: dict) -> dict:
    """Params with the same declared backfill setup_key.params_match applies:
    a row recorded before `protocol` / `adapter` existed ran markers."""
    p = json.loads(entry.get("params") or "{}")
    p.setdefault("protocol", "markers")
    p.setdefault("adapter", MARKERS_ADAPTER)
    return p


def _match(entry: dict, where: dict) -> bool:
    params = params_of(entry)
    for k, want in where.items():
        if want is None:
            continue
        have = entry.get(k) if k in ("model", "arm", "backend", "judge_format") \
            else params.get(k)
        if isinstance(want, (list, tuple, set)):
            if have not in want and str(have) not in want:
                return False
        elif have != want and str(have) != str(want):
            return False
    return True


def load(store: Path, where: dict | None = None) -> tuple[list[tuple[dict, dict]], int]:
    """[(index entry, row)], deduplicated on (cell_id, rep); plus missing count.

    `where` filters on cell fields (model, arm, backend, judge_format) and on
    params keys (protocol, adapter, temperature, ...). A list means any-of.
    """
    where = where or {}
    by_cell: dict[str, dict[int, dict]] = defaultdict(dict)
    for e in load_jsonl(store / "index.jsonl"):
        if _match(e, where):
            by_cell[e["cell_id"]].setdefault(int(e["rep"]), e)
    out, missing = [], 0
    for cid, reps in by_cell.items():
        rows = {}
        for r in load_jsonl(store / "rows" / f"{cid}.jsonl"):
            rows.setdefault(int(r.get("rep", 1)), r)     # first write wins
        for rep, e in sorted(reps.items()):
            if rep in rows:
                out.append((e, rows[rep]))
            else:
                missing += 1
    return out, missing


def summarise(pairs: list[tuple[dict, dict]]) -> list[dict]:
    groups = defaultdict(list)
    for e, r in pairs:
        groups[(e["model"], e["arm"], setup_label(e))].append((e, r))
    lines = []
    for (model, arm, label), g in sorted(groups.items()):
        ok = [r for _, r in g if r.get("run_ok", True)]
        p0 = params_of(g[0][0])
        lines.append({
            "model": model, "arm": arm, "setup": label,
            "protocol": p0["protocol"], "adapter": p0["adapter"],
            "temperature": p0.get("temperature", "-"),
            "tasks": len({r.get("task") for _, r in g}),
            "n": len(g), "run_ok": len(ok),
            "pass": sum(1 for r in ok if r.get("objective_pass")),
            "regr": sum(1 for r in ok if r.get("regressed")),
            "crash": sum(1 for r in ok if r.get("check_crashed")),
            **{k: sum(int(r.get(k) or 0) for r in ok) for k in TOOL},
        })
    return lines


def render(lines: list[dict]) -> str:
    L = ["| model | arm | setup | protocol | adapter | temp | tasks | n | run_ok "
         "| pass | regr | crash | native | recovered | repaired | malformed |",
         "|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for x in lines:
        k = x["run_ok"]
        L.append(f"| {x['model']} | {x['arm']} | {x['setup']} | {x['protocol']} | "
                 f"{x['adapter']} | {x['temperature']} | {x['tasks']} | {x['n']} | "
                 f"{k}/{x['n']} | {x['pass']}/{k} | {x['regr']}/{k} | {x['crash']}/{k} | "
                 + " | ".join(str(x[t]) for t in TOOL) + " |")
    dup = defaultdict(int)
    for x in lines:
        dup[(x["model"], x["arm"])] += 1
    split = [f"{m} / {a}" for (m, a), c in dup.items() if c > 1]
    if split:
        L += ["", f"{len(split)} (model, arm) pair(s) appear under more than one setup "
              "and are NOT pooled: " + ", ".join(sorted(split))]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--store", default=str(DEFAULT_STORE))
    ap.add_argument("--model", nargs="*")
    ap.add_argument("--arm", nargs="*")
    ap.add_argument("--protocol")
    ap.add_argument("--adapter")
    ap.add_argument("--temperature")
    ap.add_argument("--json", action="store_true", help="machine-readable lines")
    a = ap.parse_args(argv)
    where = {"model": a.model, "arm": a.arm, "protocol": a.protocol,
             "adapter": a.adapter, "temperature": a.temperature}
    pairs, missing = load(Path(a.store), where)
    lines = summarise(pairs)
    if a.json:
        print(json.dumps(lines, indent=1))
    else:
        print(render(lines))
        print(f"\n{len(pairs)} row(s) after (cell_id, rep) dedup"
              + (f"; {missing} index entr(ies) with no row file on disk, excluded"
                 if missing else ""))
        print("n = deduped rows; run_ok over n; pass, regr, crash over run_ok; "
              "tool counters summed over run_ok rows.")


if __name__ == "__main__":
    main()
