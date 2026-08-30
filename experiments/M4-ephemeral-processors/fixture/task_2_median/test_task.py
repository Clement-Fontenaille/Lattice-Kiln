"""Objective check for task_2_median. Run: python test_task.py"""
import sys

from stats import median

CASES = [
    ("median([3,1,2])", lambda: median([3, 1, 2]), 2),
    ("median([1,2,3,4])", lambda: median([1, 2, 3, 4]), 2.5),
    ("median([10,2,8,4])", lambda: median([10, 2, 8, 4]), 6),
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
