"""Figures for the arm comparison. Written to `plots/`.

    python plots.py            # all figures
    python plots.py --ascii    # sparklines in the terminal instead, no files

The point of plotting here is not decoration. Two things in this bench are invisible
in a table and obvious in a picture.

**Spread against difference.** An arm varies by about three tasks against itself at
N=5 (`50-findings/10`, finding 2), so an arm comparison is only readable when each
arm's spread is drawn beside the gap between them. A mean printed alone invites reading
a one-task difference as a result, which is the mistake this project made repeatedly.

**Per-task structure.** Totals hide which tasks moved. The heatmap is the paired
reading the suite exists to make available -- each cell is how many reps passed, so a
task that is 5/5 in one arm and 0/5 in another is a real arm effect, while anything
intermediate is noise in both.
"""
from __future__ import annotations

import json
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
OUT = HERE / "plots"
ORDER = ["baseline", "monolith", "dloop", "staged", "m7", "m7b", "m7c", "m7e", "m7f",
         "judge_anchored", "judge_caveat", "judge_bypass", "judge_staged",
         "judge_fullctx", "test_synth", "test_synth_retry"]
BLOCKS = ".,:;-=+*#"      # ascii: a Windows console is cp1252 and eats blocks


def load():
    out = {}
    for a in ORDER:
        p = RES / f"{a}.json"
        if not p.is_file():
            continue
        try:
            r = json.loads(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        if r:
            out[a] = r
    return out


def per_rep(rows):
    by = defaultdict(list)
    for x in rows:
        by[x["task"]].append(x)
    reps = max(len(v) for v in by.values())
    return [sum(1 for t in by if len(by[t]) > i and by[t][i]["objective_pass"])
            for i in range(reps)], by


def ascii_plot(data):
    print("arm                pass per rep          mean   spread")
    for a, rows in data.items():
        per, by = per_rep(rows)
        n = len(by)
        if not per:
            continue
        spark = "".join(BLOCKS[min(8, int(8 * p / max(1, n)))] for p in per)
        gap = max(per) - min(per)
        bar = "#" * int(24 * st.mean(per) / max(1, n))
        print(f"{a:<17} {spark:<8} {bar:<24} {st.mean(per):>4.1f}/{n:<3} +/-{gap}")
    print("\nsparkline = one block per rep, height = share of tasks passed")


def figures(data):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    OUT.mkdir(exist_ok=True)
    arms = {a: per_rep(r) for a, r in data.items() if a != "baseline"}
    arms = {a: v for a, v in arms.items() if v[0]}

    # 1. mean with spread -- the figure that stops a one-task gap being read as a result
    fig, ax = plt.subplots(figsize=(8, 0.42 * len(arms) + 1.6))
    names = list(arms)
    for i, a in enumerate(names):
        per, by = arms[a]
        n = len(by)
        frac = [100 * p / n for p in per]
        ax.plot([min(frac), max(frac)], [i, i], color="#9aa5b1", lw=6, solid_capstyle="butt")
        ax.plot(frac, [i] * len(frac), "o", ms=4, color="#5b6b7c")
        ax.plot(st.mean(frac), i, "D", ms=7, color="#c2410c", zorder=3)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xlabel("tasks passed (%)")
    ax.set_title("mean and spread per arm: a gap smaller than a bar is not a result",
                 fontsize=10)
    ax.grid(axis="x", alpha=.3)
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(OUT / "spread.png", dpi=130)
    plt.close(fig)

    # 2. per-task heatmap -- the paired reading
    tasks = sorted({t for _, (_, by) in arms.items() for t in by})
    grid = [[sum(1 for x in arms[a][1].get(t, []) if x["objective_pass"])
             if t in arms[a][1] else -1 for t in tasks] for a in names]
    fig, ax = plt.subplots(figsize=(0.30 * len(tasks) + 3, 0.42 * len(names) + 2))
    im = ax.imshow(grid, cmap="RdYlGn", vmin=0, vmax=5, aspect="auto")
    ax.set_xticks(range(len(tasks)))
    ax.set_xticklabels(tasks, rotation=90, fontsize=6)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=8)
    ax.set_title("reps passed per task: 5/5 vs 0/5 is an arm effect, "
                 "anything between is noise", fontsize=10)
    fig.colorbar(im, ax=ax, shrink=.6, label="reps passed")
    fig.tight_layout()
    fig.savefig(OUT / "per_task.png", dpi=130)
    plt.close(fig)

    # 3. cost against outcome
    fig, ax = plt.subplots(figsize=(7, 5))
    for a in names:
        per, by = arms[a]
        rows = data[a]
        w = sum(x["wall_s"] for x in rows) / 60 / max(1, len(per))
        ax.scatter(w, 100 * st.mean(per) / len(by), s=48, color="#5b6b7c")
        ax.annotate(a, (w, 100 * st.mean(per) / len(by)), fontsize=7,
                    xytext=(4, 3), textcoords="offset points")
    ax.set_xlabel("wall minutes per rep")
    ax.set_ylabel("tasks passed (%)")
    ax.set_title("what each arm costs for what it returns", fontsize=10)
    ax.grid(alpha=.3)
    fig.tight_layout()
    fig.savefig(OUT / "cost.png", dpi=130)
    plt.close(fig)

    print(f"wrote {OUT}/spread.png, per_task.png, cost.png")


def main():
    data = load()
    if not data:
        raise SystemExit("no results yet")
    if "--ascii" in sys.argv:
        ascii_plot(data)
        return
    ascii_plot(data)
    figures(data)


if __name__ == "__main__":
    main()
