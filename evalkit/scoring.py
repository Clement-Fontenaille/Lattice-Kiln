"""Aggregate a set of rows into one number, without letting rep count vote.

    from scoring import score
    s = score(rows, "objective_pass")
    print(s.rate, s.ci, s.coverage)

THE RULE
--------
**Average within a task first, then average over tasks.** Every task counts
once, whatever its rep count.

Row-weighting — counting passing rows over total rows — makes a task with ten
reps ten times more important to the result than a task with one. Nothing
intends that. It is an artifact of which cells someone got round to filling.

It was found on 2026-09-23 in the one place it should have been impossible.
`baseline` changes nothing in 100% of runs, so its score is a property of the
fixtures and is deterministic per task; it nonetheless read **17.6% for one
model and 15.8% for another**. Zero of 34 tasks disagreed. The difference was
that one subject had 32 tasks at one rep and two at three, both of the
triply-repped ones fail at baseline, and four extra failing rows moved the
aggregate by 1.8 points — a tenth of the quantity. See `50-findings/14`,
addendum 4.

The judge arms are near-uniform and the same correction moves them by at most
1.6 points, so this is not a reinterpretation of past results. It is a defect
that was small where it was looked at and large in the control nobody ran
evenly.

THE INTERVAL
------------
The confidence interval is computed **over tasks, not over rows**, and that is
a correction rather than a convenience.

Reps of one task are not independent observations. They share a fixture, an
objective and a check, and they fail together for the same reasons. A binomial
interval over rows assumes independence it does not have, and reports a
precision the data cannot support — the more reps per task, the more confident
it claims to be about a task set that has not grown.

So the observations here are the **per-task rates**, and the interval is the
standard error of their mean. With 34 tasks the interval reflects 34
independent things, which is what there are.

COVERAGE IS PRINTED, NOT ASSUMED
--------------------------------
`score()` returns the per-task rep distribution alongside the rate. Uneven
coverage is invisible in a rate and visible in a distribution, and a cell with
668 rows looks better powered than one with 374 while saying nothing about how
they are spread. Print it beside the number so that the reader sees it, rather
than leaving it for someone who asks why a control moved.
"""
from __future__ import annotations

import collections
import math
from dataclasses import dataclass, field


@dataclass
class Score:
    rate: float | None          # task-weighted, 0-100
    ci: tuple[float, float]     # over tasks
    tasks: int
    rows: int
    row_rate: float | None      # row-weighted, for comparison only
    coverage: dict              # reps per task -> how many tasks
    per_task: dict = field(repr=False, default_factory=dict)

    @property
    def gap(self) -> float:
        """Task-weighted minus row-weighted. Non-zero means uneven coverage."""
        if self.rate is None or self.row_rate is None:
            return 0.0
        return self.rate - self.row_rate

    @property
    def uniform(self) -> bool:
        return len(self.coverage) <= 1

    def coverage_str(self) -> str:
        if not self.coverage:
            return "no rows"
        if self.uniform:
            n, t = next(iter(self.coverage.items()))
            return f"{t} tasks x {n}"
        parts = ", ".join(f"{t}x{n}" for n, t in sorted(self.coverage.items()))
        return f"uneven: {parts}"


def per_task(rows, key, truth=None) -> dict:
    """task -> (hits, reps). `truth` overrides the default bool(row[key])."""
    out = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        t = out[r["task"]]
        t[0] += bool(truth(r) if truth else r.get(key))
        t[1] += 1
    return {k: tuple(v) for k, v in out.items()}


def score(rows, key=None, truth=None) -> Score:
    """Task-weighted rate, its interval over tasks, and the coverage behind it."""
    if not rows:
        return Score(None, (0.0, 0.0), 0, 0, None, {})
    pt = per_task(rows, key, truth)
    rates = [h / n for h, n in pt.values()]
    m = sum(rates) / len(rates)
    if len(rates) > 1:
        var = sum((x - m) ** 2 for x in rates) / (len(rates) - 1)
        se = math.sqrt(var / len(rates))
    else:
        se = 0.0
    hits = sum(h for h, _ in pt.values())
    n = sum(n for _, n in pt.values())
    return Score(
        rate=100 * m,
        ci=(100 * max(0.0, m - 1.96 * se), 100 * min(1.0, m + 1.96 * se)),
        tasks=len(pt),
        rows=n,
        row_rate=100 * hits / n if n else None,
        coverage=dict(collections.Counter(c for _, c in pt.values())),
        per_task=pt,
    )


def compare(a: Score, b: Score) -> dict:
    """Difference between two task-weighted rates, with a paired interval.

    Paired over the tasks both cover, because the same task appearing in both
    arms is the same fixture and the same check — treating the two rates as
    independent throws away the pairing and widens the interval for nothing.
    """
    shared = sorted(set(a.per_task) & set(b.per_task))
    if not shared:
        return {"shared": 0, "delta": None, "ci": (0.0, 0.0)}
    d = [b.per_task[t][0] / b.per_task[t][1] - a.per_task[t][0] / a.per_task[t][1]
         for t in shared]
    m = sum(d) / len(d)
    if len(d) > 1:
        var = sum((x - m) ** 2 for x in d) / (len(d) - 1)
        se = math.sqrt(var / len(d))
    else:
        se = 0.0
    return {
        "shared": len(shared),
        "delta": 100 * m,
        "ci": (100 * (m - 1.96 * se), 100 * (m + 1.96 * se)),
        "significant": abs(m) > 1.96 * se,
    }


def _selftest():
    """The baseline case that found this, reduced to eight rows."""
    rows = []
    for t, passes, reps in (("a", True, 1), ("b", False, 3), ("c", True, 1),
                            ("d", False, 1)):
        rows += [{"task": t, "objective_pass": passes} for _ in range(reps)]
    s = score(rows, "objective_pass")
    assert round(s.rate, 1) == 50.0, s.rate          # 2 of 4 tasks
    assert round(s.row_rate, 1) == 33.3, s.row_rate  # 2 of 6 rows
    assert not s.uniform and s.coverage == {1: 3, 3: 1}, s.coverage
    even = [{"task": t, "objective_pass": p}
            for t, p in (("a", True), ("b", False), ("c", True), ("d", False))]
    e = score(even, "objective_pass")
    assert e.rate == e.row_rate == 50.0 and e.uniform
    print("ok  task-weighted 50.0% vs row-weighted 33.3% on the uneven set;")
    print("ok  identical at 50.0% once coverage is even")


if __name__ == "__main__":
    _selftest()
