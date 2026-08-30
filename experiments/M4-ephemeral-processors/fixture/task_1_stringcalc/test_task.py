"""Objective check for task_1_stringcalc. Run: python test_task.py"""
import sys

from stringcalc import add

CASES = [
    ('add("")', lambda: add(""), 0),
    ('add("42")', lambda: add("42"), 42),
    ('add("1,2,3")', lambda: add("1,2,3"), 6),
    ('add(" 4 , 5 ")', lambda: add(" 4 , 5 "), 9),
]


def main() -> None:
    fails = []
    for name, fn, want in CASES:
        try:
            got = fn()
        except Exception as e:  # noqa: BLE001
            fails.append(f"{name}: raised {e!r}")
            continue
        if got != want:
            fails.append(f"{name}: got {got!r}, want {want!r}")
    if fails:
        print("FAIL")
        for f in fails:
            print("  " + f)
        sys.exit(1)
    print("OK")


main()
