"""Objective check for wf3_refactor_witnessed. Run: python test_task.py

The witnessed half of a matched pair. `wf3_refactor` states the same objective and
checks only the returned prices, so an untouched source and a correct refactor score
identically -- the structural clause has no witness at all
(00-design/40-roadmap/03-research-and-evaluation/E0-suite-construct-validation.md).

Here the same clause is witnessed by STRUCTSCORE, read off the source with an AST
walk. No model, no judgement. The objective admits TWO outcomes rather than one, so
the criterion says what finished looks like without prescribing the method:

  - the two functions collapse into one, or
  - each body reduces to a call into a third function carrying the shared logic.

The pair exists so the cost of an unwitnessed clause is measurable rather than
anecdotal: same objective, same source, one variable.
"""
import ast as _ast
from pathlib import Path as _Path
import math
import sys

from discounts import clearance_price, staff_price

CASES = [
    ("staff round input", lambda: staff_price(10), 8.0),
    ("staff half", lambda: staff_price(2.5), 2.0),
    # staff must stay exact - a shared helper that rounds would break this
    ("staff messy input unrounded", lambda: staff_price(1.567), 1.2536),
    # clearance must stay rounded - a shared helper without rounding breaks this
    ("clearance rounds", lambda: clearance_price(1.567), 1.25),
    ("clearance rounds 2", lambda: clearance_price(2.555), 2.04),
]


def _eq(a, b):
    if isinstance(a, float) or isinstance(b, float):
        return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)
    return a == b


def _structure():
    """Did the duplication actually go? Read off the source, not off a model.

    The invariant is not "one of the names disappeared" -- both must survive, the
    subtests call them. It is that **the shared computation appears once in the
    module** instead of twice. That covers both admissible outcomes: a third function
    carrying it, or one of the two delegating to the other.
    """
    src = _Path(__file__).with_name("discounts.py").read_text(encoding="utf-8")
    try:
        tree = _ast.parse(src)
    except SyntaxError:
        return 0, ["discounts.py does not parse"]
    fns = {n.name: n for n in tree.body if isinstance(n, _ast.FunctionDef)}
    for req in ("staff_price", "clearance_price"):
        if req not in fns:
            return 0, [f"{req} is gone -- callers depend on it"]

    def _has_discount(fn):
        """the 20% computation, written literally in this function's own body"""
        for node in _ast.walk(fn):
            if isinstance(node, _ast.BinOp) and isinstance(node.op, _ast.Mult):
                for side in (node.left, node.right):
                    if isinstance(side, _ast.Constant) and side.value == 0.8:
                        return True
        return False

    holders = [n for n, f in fns.items() if _has_discount(f)]
    notes, score = [], 0

    if len(holders) == 1:
        score += 1
    else:
        # the per-function points are gated on this one: while the computation is
        # still written out twice, nothing below can be read as the duplication
        # having gone, and an untouched source must score zero rather than most of
        # the marks.
        if not holders:
            notes.append("the 20% computation is nowhere -- did the logic move out "
                         "of discounts.py?")
        else:
            notes.append(f"the 20% computation is still written out in "
                         f"{len(holders)} places: {', '.join(sorted(holders))}")
        return 0, notes

    for name in ("staff_price", "clearance_price"):
        if name in holders:
            score += 1                      # this one carries the logic, legitimately
            continue
        calls = [d.func.id for d in _ast.walk(fns[name])
                 if isinstance(d, _ast.Call) and isinstance(d.func, _ast.Name)
                 and d.func.id in fns]
        if calls:
            score += 1                      # it delegates
        else:
            notes.append(f"{name} neither carries the computation nor delegates")
    return score, notes


def main() -> None:
    passed, fails = 0, []
    for name, fn, want in CASES:
        try:
            got = fn()
        except Exception as e:  # noqa: BLE001
            fails.append(f"{name}: raised {e!r}")
            continue
        if _eq(got, want):
            passed += 1
        else:
            fails.append(f"{name}: got {got!r} want {want!r}")
    print(f"SUBTESTS {passed}/{len(CASES)}")
    for f in fails:
        print("  " + f)

    s, notes = _structure()
    print(f"STRUCTSCORE {s}/3")
    for n in notes:
        print("  " + n)
    sys.exit(0 if passed == len(CASES) and s == 3 else 1)


main()
