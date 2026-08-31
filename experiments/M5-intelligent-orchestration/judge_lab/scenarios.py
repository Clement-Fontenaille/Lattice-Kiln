"""Frozen review scenarios for the judge-lab.

Each scenario is a *candidate submission* to be judged against an objective, with
a known-correct verdict. The lab runs several review pipelines over the same set
and compares verdict-vs-truth and, more importantly, the reasoning.

`files` = what the (hypothetical) implementer wrote. `originals` = the repo
before the change, for the "did anything actually change?" precheck. `fixture`
names the fixture_workflow dir whose test_task.py adjudicates.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# ---- originals (pre-change repo state) -----------------------------------

ORIG = {
    "wf1_crossfile": {
        "orders.py":
            'from pricing import line_price\n\n\n'
            'def total(order):\n'
            '    """Sum of all line prices in an order."""\n'
            '    return sum(line_price(li) for li in order["lines"])\n',
        "pricing.py":
            'def line_price(item):\n'
            '    """Price for one order line: unit price times quantity."""\n'
            '    return item["unit_price"]  # BUG: ignores item["qty"]\n',
    },
    "wf3_refactor": {
        "discounts.py":
            'def staff_price(price):\n'
            '    """20% off, exact (no rounding)."""\n'
            '    return price * 0.8\n\n\n'
            'def clearance_price(price):\n'
            '    """20% off, rounded to cents."""\n'
            '    return round(price * 0.8, 2)\n',
    },
    "wf4_assumption": {
        "search.py":
            'def find(items, target):\n'
            '    """Return the index of target in items, or -1 if absent."""\n'
            '    for i, x in enumerate(items):\n'
            '        if x == target:\n'
            '            return i\n'
            '    return -1\n',
    },
    "wf2_retry": {
        "client.py":
            'class Client:\n'
            '    def __init__(self):\n'
            '        self.calls = 0\n\n'
            '    def call(self, fn):\n'
            '        """Invoke fn() once and return its result."""\n'
            '        self.calls += 1\n'
            '        return fn()\n',
    },
    "wf5_partial": {
        "durations.py":
            'def parse_duration(s):\n'
            '    """Parse a duration string into total seconds."""\n'
            '    raise NotImplementedError\n',
    },
}


@dataclass(frozen=True)
class Scenario:
    id: str
    fixture: str
    objective: str
    claim: str
    files: dict[str, str]              # candidate submission
    expect: str                       # "approve" | "needs-change"
    why: str
    originals: dict[str, str] = field(default_factory=dict)


def _s(id, fixture, objective, claim, files, expect, why):
    return Scenario(id, fixture, objective, claim, files, expect, why,
                    originals=ORIG[fixture])


OBJ_WF3 = ("staff_price and clearance_price both apply 20% off. Remove the "
           "duplication by extracting a shared helper, without changing what "
           "either function returns.")
OBJ_WF1 = ("orders.total() returns the wrong amount when a line's qty > 1. Fix "
           "the code so totals are correct; a caller uses pricing.line_price "
           "directly, so it must be right too.")
OBJ_WF4 = ("search.find() does a linear scan and is too slow for large inputs. "
           "Rewrite it to run in O(log n).")
OBJ_WF5 = ("Implement durations.parse_duration(s): parse '1h30m','45m','2h',"
           "'90s','1h2m3s' into seconds; '' is 0; tolerate surrounding "
           "whitespace.")
OBJ_WF2 = ("Add a retries parameter to Client.call(fn, retries=2): on raise, "
           "retry up to `retries` more times; if all fail, re-raise the LAST "
           "exception. retries=0 means a single attempt.")


SCENARIOS = [
    # ---- wf3: the refactor trap ----
    _s("wf3_correct", "wf3_refactor", OBJ_WF3,
       "Extracted a shared _base helper; both functions call it; clearance still rounds.",
       {"discounts.py":
        'def _base(price):\n    return price * 0.8\n\n\n'
        'def staff_price(price):\n    """20% off, exact (no rounding)."""\n    return _base(price)\n\n\n'
        'def clearance_price(price):\n    """20% off, rounded to cents."""\n    return round(_base(price), 2)\n'},
       "approve", "correct dedupe; rounding kept only in clearance"),
    _s("wf3_trap", "wf3_refactor", OBJ_WF3,
       "Extracted a shared _discounted helper; both functions call it. Duplication removed.",
       {"discounts.py":
        'def _discounted(price):\n    """20% off, rounded to cents."""\n    return round(price * 0.8, 2)\n\n\n'
        'def staff_price(price):\n    """20% off."""\n    return _discounted(price)\n\n\n'
        'def clearance_price(price):\n    """20% off."""\n    return _discounted(price)\n'},
       "needs-change", "shared helper rounds -> staff_price(1.567) is now 1.25, must be 1.2536"),

    # ---- wf1: cross-file ----
    _s("wf1_correct", "wf1_crossfile", OBJ_WF1,
       "Fixed line_price to multiply unit price by qty.",
       {"pricing.py":
        'def line_price(item):\n    """Price for one order line: unit price times quantity."""\n'
        '    return item["unit_price"] * item["qty"]\n'},
       "approve", "correct one-line fix at the real cause site"),
    _s("wf1_empty", "wf1_crossfile", OBJ_WF1,
       "Fixed line_price to multiply unit price by qty.",
       {"pricing.py": ORIG["wf1_crossfile"]["pricing.py"]},   # UNCHANGED
       "needs-change", "claim says fixed but the file is byte-identical to the original"),
    _s("wf1_symptom", "wf1_crossfile", OBJ_WF1,
       "Patched total() in orders.py to account for qty.",
       {"orders.py":
        'from pricing import line_price\n\n\n'
        'def total(order):\n    """Sum of all line prices in an order."""\n'
        '    return sum(line_price(li) * li["qty"] for li in order["lines"])\n'},
       "needs-change", "symptom patch; the direct line_price caller still gets the wrong number"),

    # ---- wf4: the false premise ----
    _s("wf4_kept_linear", "wf4_assumption", OBJ_WF4,
       "The input is not guaranteed sorted, so binary search would be wrong. Kept the linear scan.",
       {"search.py": ORIG["wf4_assumption"]["search.py"]},   # unchanged, on purpose
       "approve", "correct call: O(log n) is impossible on unsorted data; keeping linear is right"),
    _s("wf4_did_bisect", "wf4_assumption", OBJ_WF4,
       "Rewrote find() with bisect for O(log n).",
       {"search.py":
        'import bisect\n\n\n'
        'def find(items, target):\n'
        '    """Return the index of target in items, or -1 if absent."""\n'
        '    i = bisect.bisect_left(items, target)\n'
        '    if i < len(items) and items[i] == target:\n        return i\n    return -1\n'},
       "needs-change", "bisect assumes sorted input; fails the unsorted subtests"),

    # ---- wf5: partial credit ----
    _s("wf5_partial", "wf5_partial", OBJ_WF5,
       "Implemented parse_duration for hours and minutes.",
       {"durations.py":
        'import re\n\n\n'
        'def parse_duration(s):\n'
        '    """Parse a duration string into total seconds."""\n'
        '    s = s.strip()\n'
        '    if not s:\n        return 0\n'
        '    total = 0\n'
        '    for num, unit in re.findall(r"(\\d+)([hm])", s):\n'   # BUG: no 's' unit
        '        total += int(num) * {"h": 3600, "m": 60}[unit]\n'
        '    return total\n'},
       "needs-change", "seconds unit dropped -> '90s' and '1h2m3s' fail; panel should flag the seconds clause"),

    # ---- wf2: feature with an edge ----
    _s("wf2_correct", "wf2_retry", OBJ_WF2,
       "Added retries with re-raise of the last exception; retries=0 does one attempt.",
       {"client.py":
        'class Client:\n    def __init__(self):\n        self.calls = 0\n\n'
        '    def call(self, fn, retries=2):\n'
        '        """Invoke fn(), retrying on failure up to `retries` times."""\n'
        '        last = None\n'
        '        for _ in range(retries + 1):\n'
        '            self.calls += 1\n'
        '            try:\n                return fn()\n'
        '            except Exception as e:  # noqa: BLE001\n                last = e\n'
        '        raise last\n'},
       "approve", "correct: retries+1 attempts, re-raises last, retries=0 -> one attempt"),
    _s("wf2_offbyone", "wf2_retry", OBJ_WF2,
       "Added retries with re-raise of the last exception.",
       {"client.py":
        'class Client:\n    def __init__(self):\n        self.calls = 0\n\n'
        '    def call(self, fn, retries=2):\n'
        '        """Invoke fn(), retrying on failure."""\n'
        '        last = None\n'
        '        for _ in range(retries):\n'                    # BUG: should be retries + 1
        '            self.calls += 1\n'
        '            try:\n                return fn()\n'
        '            except Exception as e:  # noqa: BLE001\n                last = e\n'
        '        raise last\n'},
       "needs-change", "range(retries) -> retries=0 makes zero attempts and raises None"),
]
