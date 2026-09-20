"""Generated tokens per minute over a suite, and what a second worker does to it.

    python throughput.py                      # everything the store has timed
    python throughput.py --model qwen2.5-coder:7b-instruct-q4_K_M
    python throughput.py --arm judge_bypass --since "2026-09-20 14:05"

Two rates, and confusing them is how a real speedup gets read as a regression:

  decode    tokens / gen_s   -- what the card does while it is decoding, summed
                                over streams. Two workers sharing one GPU split
                                its decode capacity, so PER STREAM this falls.
  suite     tokens / minute  -- tokens over wall clock, the union of the
                                intervals actually worked. This is the number
                                that says whether the sweep finishes sooner.

A rep is not decoding for most of its wall time: it sets up a fixture, scores a
baseline, runs an arm that may call the model several times with Python between
the calls, restores protected files and scores again. Those gaps are why a
second worker can help at all -- it decodes while the first one is scoring. The
gap fraction below is how much room there was for that to happen.

Concurrency is read off the rows rather than declared. Each rep records the
process that ran it and its wall interval; a rep is at concurrency N when N
distinct runners' intervals overlap it. So a pool worked by one worker and then
by two produces both buckets with no experiment design, and the comparison is
between real reps rather than a benchmark standing in for them.

Reps recorded before the meter existed carry no `gen_tok` and are skipped, with
a count reported so a thin table is never mistaken for a slow one.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from store import Store  # noqa: E402


def _when(text: str) -> float:
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).astimezone().timestamp()
        except ValueError:
            continue
    raise SystemExit(f"cannot read {text!r} as a date or a date and time")


def load(store: Store, want: dict) -> tuple[list[dict], int]:
    """Timed rows matching `want`, plus how many matched but predate the meter."""
    idx = defaultdict(list)
    with (store.path / "index.jsonl").open(encoding="utf-8") as fh:
        for line in fh:
            e = json.loads(line)
            idx[e["cell_id"]].append(e)

    out, untimed = [], 0
    for cell_id, entries in idx.items():
        e0 = entries[0]
        if any(e0.get(k) != v for k, v in want.items() if v is not None):
            continue
        p = store.rows_dir / f"{cell_id}.jsonl"
        if not p.is_file():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("gen_tok") is None or r.get("t_start") is None:
                untimed += 1
                continue
            r["_model"], r["_arm"] = e0["model"], e0["arm"]
            out.append(r)
    return out, untimed


def union_seconds(spans: list[tuple[float, float]]) -> float:
    """Wall clock actually covered. Overlapping reps must count their shared
    seconds ONCE, or two workers appear to have had twice the time and their
    throughput halves on paper."""
    if not spans:
        return 0.0
    ordered = sorted(spans)
    total, cur_a, cur_b = 0.0, *ordered[0]
    for a, b in ordered[1:]:
        if a > cur_b:
            total += cur_b - cur_a
            cur_a, cur_b = a, b
        else:
            cur_b = max(cur_b, b)
    return total + (cur_b - cur_a)


def concurrency(rows: list[dict]) -> None:
    """Tag each row with how many distinct runners were live during it.

    Peak rather than mean: a rep that spent any of its life beside another
    worker was competing for the card, and averaging would let a long rep with
    one brief overlap look solitary.
    """
    events = []           # (time, +1/-1, runner) -- a sweep line over the reps
    for r in rows:
        events.append((r["t_start"], 1, r["runner"]))
        events.append((r["t_end"], -1, r["runner"]))
    events.sort()

    live: dict[str, int] = defaultdict(int)
    marks: list[tuple[float, int]] = []
    for t, d, runner in events:
        live[runner] += d
        if live[runner] <= 0:
            live.pop(runner, None)
        marks.append((t, len(live)))

    for r in rows:
        peak = 1
        for t, n in marks:
            if r["t_start"] <= t <= r["t_end"]:
                peak = max(peak, n)
        r["_conc"] = peak


def report(rows: list[dict], untimed: int, label: str) -> None:
    if not rows:
        print(f"no timed reps{label}"
              + (f" ({untimed} recorded before the meter existed)" if untimed else ""))
        return

    concurrency(rows)
    buckets = defaultdict(list)
    for r in rows:
        buckets[r["_conc"]].append(r)

    print(f"generated tokens per minute{label}\n")
    print(f"{'workers':>7} {'reps':>5} {'tok':>9} {'tok/rep':>8} "
          f"{'decode':>9} {'suite':>10} {'gap':>6} {'wall':>8}")
    print(f"{'':>7} {'':>5} {'':>9} {'':>8} {'tok/s':>9} {'tok/min':>10} "
          f"{'%':>6} {'min':>8}")
    print("-" * 70)

    for c in sorted(buckets):
        rs = buckets[c]
        tok = sum(r["gen_tok"] for r in rs)
        gen_s = sum(r["gen_s"] for r in rs)
        span = union_seconds([(r["t_start"], r["t_end"]) for r in rs])
        busy = sum(r["t_end"] - r["t_start"] for r in rs)
        decode = tok / gen_s if gen_s else 0.0
        suite = 60 * tok / span if span else 0.0
        gap = 100 * (1 - gen_s / busy) if busy else 0.0
        print(f"{c:>7} {len(rs):>5} {tok:>9,} {tok/len(rs):>8,.0f} "
              f"{decode:>9.1f} {suite:>10,.0f} {gap:>6.0f} {span/60:>8.1f}")

    # Compare only buckets substantial enough to mean something. A worker
    # between batches leaves one or two reps briefly alone, and that sliver
    # lands in a lower bucket as though it were a measured condition: at three
    # workers it produced "x3.34 suite" off a SINGLE rep. A ratio against a
    # tail artifact reads exactly like a result, so it is not printed at all.
    MIN = 10
    solid = sorted(c for c in buckets if len(buckets[c]) >= MIN)
    thin = sorted(c for c in buckets if len(buckets[c]) < MIN)
    if len(solid) > 1:
        lo, hi = solid[0], solid[-1]

        def rate(c, key):
            rs = buckets[c]
            tok = sum(r["gen_tok"] for r in rs)
            if key == "suite":
                sp = union_seconds([(r["t_start"], r["t_end"]) for r in rs])
                return 60 * tok / sp if sp else 0.0
            g = sum(r["gen_s"] for r in rs)
            return tok / g if g else 0.0

        print()
        print(f"{hi} workers vs {lo}: "
              f"suite x{rate(hi,'suite')/rate(lo,'suite'):.2f}, "
              f"decode per stream x{rate(hi,'decode')/rate(lo,'decode'):.2f}")
    elif len(buckets) > 1:
        print()
        print(f"no comparison: only one bucket has {MIN}+ reps")
    if thin:
        which = ", ".join(f"{c} worker(s): {len(buckets[c])} rep(s)" for c in thin)
        print(f"too thin to compare ({which}) -- a worker between batches "
              f"leaves reps briefly alone")

    if untimed:
        print(f"\n{untimed} rep(s) skipped: recorded before the meter existed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model")
    ap.add_argument("--arm")
    ap.add_argument("--judge-format")
    ap.add_argument("--since", metavar="WHEN",
                    help="YYYY-MM-DD or 'YYYY-MM-DD HH:MM', local time")
    ap.add_argument("--until", metavar="WHEN",
                    help="same forms. A phase boundary is a MINUTE, not a day: "
                         "two phases run hours apart on the same date, and a "
                         "date-only bound silently pools them.")
    ap.add_argument("--by-arm", action="store_true",
                    help="one table per arm as well as the whole selection")
    args = ap.parse_args()

    store = Store()
    rows, untimed = load(store, {"model": args.model, "arm": args.arm,
                                 "judge_format": args.judge_format})
    if args.since:
        rows = [r for r in rows if r["t_start"] >= _when(args.since)]
    if args.until:
        rows = [r for r in rows if r["t_end"] <= _when(args.until)]

    bits = [f"{k}={v}" for k, v in
            (("model", args.model), ("arm", args.arm),
             ("format", args.judge_format), ("since", args.since),
             ("until", args.until)) if v]
    label = f"  [{', '.join(bits)}]" if bits else ""
    report(rows, untimed, label)

    if args.by_arm:
        for arm in sorted({r["_arm"] for r in rows}):
            print()
            report([r for r in rows if r["_arm"] == arm], 0, f"  [arm={arm}]")


if __name__ == "__main__":
    main()
