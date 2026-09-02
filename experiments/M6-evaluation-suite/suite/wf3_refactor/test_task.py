"""Objective check for wf3_refactor. Run: python test_task.py"""
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
    sys.exit(0 if passed == len(CASES) else 1)


main()
