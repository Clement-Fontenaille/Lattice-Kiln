"""Objective check for task_4_starve. Run: python test_task.py"""
import sys

from report import make_report

CASES = [
    ('make_report("Hello World")', lambda: make_report("Hello World"), "hello-world.md"),
    ('make_report("  Q3 Metrics!!  ")', lambda: make_report("  Q3 Metrics!!  "), "q3-metrics.md"),
    ('make_report("already_a_slug")', lambda: make_report("already_a_slug"), "already-a-slug.md"),
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
