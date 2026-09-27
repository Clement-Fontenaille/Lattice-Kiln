"""Paired comparison: which tasks flip between two (model, arm) populations.

    python flips.py --a nemotron3-nano-4b:latest monolith \\
                    --b nemotron3-nano-4b:latest dloop [--adapter 63b5b222daf4]
    python flips.py --a M X --setup-a 68de1209 --b M Y --setup-b 41b6a6fc
    python flips.py ... --rule majority           # when a side has >1 rep per task

Read from the store through matrix.load(), so the same dedup on (cell_id, rep)
and the same population rule apply: a side that spans more than one setup is
refused, with the setup labels listed, rather than pooled. Pick one with
--setup-a / --setup-b (labels as matrix.py prints them) or narrow it with
--protocol / --adapter / --temperature, which apply to both sides.

A task's outcome on a side is objective_pass over that side's run_ok rows.
Rows whose arm raised made no attempt and are not a fail; a task with no
run_ok row on a side is listed as `no attempt`, outside the four cells.

With one rep per task a side's outcome is that rep. With more, the collapse
rule is a choice that changes the table, so it is not made silently: --rule
is REQUIRED and must be one of

    all        every run_ok rep passed
    any        at least one did
    majority   more than half did (a tie is not a pass)

and each task's k/n is printed beside its cell either way.
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from matrix import DEFAULT_STORE, load, setup_label  # noqa: E402

RULES = {"all": lambda k, n: k == n,
         "any": lambda k, n: k > 0,
         "majority": lambda k, n: 2 * k > n}


def side(store: Path, model: str, arm: str, where: dict, setup: str | None):
    """{task: (passes, run_ok reps)}, the setup label, and tasks with no attempt."""
    pairs, _ = load(store, {**where, "model": model, "arm": arm})
    labels = defaultdict(int)
    for e, _r in pairs:
        labels[setup_label(e)] += 1
    if setup:
        pairs = [(e, r) for e, r in pairs if setup_label(e) == setup]
    elif len(labels) > 1:
        raise SystemExit(
            f"{model} / {arm} spans {len(labels)} setups and will not be pooled: "
            + ", ".join(f"{k} ({v} rows)" for k, v in sorted(labels.items()))
            + ". Choose one with --setup-a/--setup-b, or narrow with "
              "--protocol/--adapter/--temperature. `matrix.py` shows what each is.")
    if not pairs:
        raise SystemExit(f"no rows for {model} / {arm} under that selection")
    out, seen = defaultdict(lambda: [0, 0]), set()
    for e, r in pairs:
        seen.add(r["task"])
        if not r.get("run_ok", True):
            continue
        out[r["task"]][1] += 1
        out[r["task"]][0] += bool(r.get("objective_pass"))
    label = setup or next(iter(labels))
    return dict(out), label, sorted(seen - set(out))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--a", nargs=2, metavar=("MODEL", "ARM"), required=True)
    ap.add_argument("--b", nargs=2, metavar=("MODEL", "ARM"), required=True)
    ap.add_argument("--setup-a")
    ap.add_argument("--setup-b")
    ap.add_argument("--protocol")
    ap.add_argument("--adapter")
    ap.add_argument("--temperature")
    ap.add_argument("--rule", choices=sorted(RULES))
    ap.add_argument("--store", default=str(DEFAULT_STORE))
    a = ap.parse_args(argv)
    where = {"protocol": a.protocol, "adapter": a.adapter, "temperature": a.temperature}
    store = Path(a.store)
    A, la, noA = side(store, *a.a, where, a.setup_a)
    B, lb, noB = side(store, *a.b, where, a.setup_b)

    multi = any(n > 1 for _, n in list(A.values()) + list(B.values()))
    if multi and not a.rule:
        raise SystemExit("a side has more than one run_ok rep for some task; the "
                         "collapse rule changes the table, so pass --rule "
                         f"{'|'.join(sorted(RULES))}")
    rule = RULES[a.rule or "all"]

    both_tasks = sorted(set(A) & set(B))
    cells = {"A not B": [], "B not A": [], "both": [], "neither": []}
    for t in both_tasks:
        pa, pb = rule(*A[t]), rule(*B[t])
        key = ("both" if pa and pb else "A not B" if pa else
               "B not A" if pb else "neither")
        cells[key].append(t)

    name_a, name_b = f"{a.a[0]} / {a.a[1]} [{la}]", f"{a.b[0]} / {a.b[1]} [{lb}]"
    print(f"A = {name_a}\nB = {name_b}")
    if multi:
        print(f"rule: {a.rule} (per task, over run_ok reps)")
    print(f"\n{len(both_tasks)} task(s) attempted on both sides\n")
    print("| | B pass | B fail |\n|---|---:|---:|")
    print(f"| **A pass** | {len(cells['both'])} | {len(cells['A not B'])} |")
    print(f"| **A fail** | {len(cells['B not A'])} | {len(cells['neither'])} |")
    for key in ("A not B", "B not A", "both", "neither"):
        print(f"\n### {key} ({len(cells[key])})")
        for t in cells[key]:
            print(f"- {t}  A {A[t][0]}/{A[t][1]}  B {B[t][0]}/{B[t][1]}")
    onlyA, onlyB = sorted(set(A) - set(B)), sorted(set(B) - set(A))
    notes = [("attempted in A only", onlyA), ("attempted in B only", onlyB),
             ("no attempt in A (arm raised on every rep)", noA),
             ("no attempt in B (arm raised on every rep)", noB)]
    for label, ts in notes:
        if ts:
            print(f"\n{label} ({len(ts)}), outside the table: {', '.join(ts)}")


if __name__ == "__main__":
    main()
