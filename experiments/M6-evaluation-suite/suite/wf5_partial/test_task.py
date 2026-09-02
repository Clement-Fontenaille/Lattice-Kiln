"""Objective check for wf5_partial. Run: python test_task.py"""
import sys

from durations import parse_duration

CASES = [
    ("minutes", lambda: parse_duration("45m"), 2700),
    ("hours", lambda: parse_duration("2h"), 7200),
    ("h+m", lambda: parse_duration("1h30m"), 5400),
    ("seconds", lambda: parse_duration("90s"), 90),
    ("h+m+s", lambda: parse_duration("1h2m3s"), 3723),
    ("empty is zero", lambda: parse_duration(""), 0),
    ("whitespace", lambda: parse_duration("  1h "), 3600),
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
