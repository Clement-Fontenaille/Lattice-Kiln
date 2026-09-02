"""Check for hf_cache_decorator. Run: python test_task.py

The task: memoize config_for. Two things a bare @lru_cache gets wrong together -
it *does* skip recompute (good) but it returns the *same dict object* each hit,
so a caller mutating it corrupts later hits (bad). Full credit needs
copy-on-return (or an immutable value).

Discriminator subtest: 'cached value is not corruptible'.
"""
import sys

import compute
from compute import config_for


def reset():
    compute.CALLS.clear()


CASES = [
    ("correct value", lambda: (reset(), config_for("dev"))[-1],
     {"env": "dev", "debug": True, "workers": 1}),
    ("repeat call skips recompute",
     lambda: (reset(), config_for("prod"), config_for("prod"), len(compute.CALLS))[-1], 1),
    ("different arg recomputes",
     lambda: (reset(), config_for("dev"), config_for("prod"), sorted(compute.CALLS))[-1],
     ["dev", "prod"]),
    ("cached value is not corruptible",
     lambda: (reset(), _corrupt(), config_for("dev")["debug"])[-1], True),
]


def _corrupt():
    d = config_for("dev")
    d["debug"] = "HACKED"
    d["workers"] = 999


def main():
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
