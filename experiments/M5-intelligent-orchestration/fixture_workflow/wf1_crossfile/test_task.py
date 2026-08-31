"""Objective check for wf1_crossfile. Run: python test_task.py"""
import sys

from orders import total
from pricing import line_price

O1 = {"lines": [{"unit_price": 5, "qty": 1}]}
O2 = {"lines": [{"unit_price": 5, "qty": 3}]}
O3 = {"lines": [{"unit_price": 2, "qty": 2}, {"unit_price": 10, "qty": 1}]}

CASES = [
    ("total qty=1", lambda: total(O1), 5),
    ("total qty=3", lambda: total(O2), 15),
    ("total mixed", lambda: total(O3), 14),
    ("total empty", lambda: total({"lines": []}), 0),
    # forces the fix into pricing.line_price, not a patch on total()
    ("line_price direct", lambda: line_price({"unit_price": 5, "qty": 4}), 20),
]


def main() -> None:
    passed, fails = 0, []
    for name, fn, want in CASES:
        try:
            got = fn()
        except Exception as e:  # noqa: BLE001
            fails.append(f"{name}: raised {e!r}")
            continue
        if got == want:
            passed += 1
        else:
            fails.append(f"{name}: got {got!r} want {want!r}")
    print(f"SUBTESTS {passed}/{len(CASES)}")
    for f in fails:
        print("  " + f)
    sys.exit(0 if passed == len(CASES) else 1)


main()
