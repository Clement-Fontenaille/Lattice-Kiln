"""Check for hf_suppress. Run: python test_task.py

Discriminator subtest: 'real error still surfaces' - a bare try/except that
returns {} makes load(None) succeed-with-nothing, hiding an upstream bug.
"""
import sys

from loader import load


def _raises(arg):
    try:
        load(arg)
        return False
    except Exception:  # noqa: BLE001
        return True


CASES = [
    ("all-numeric loads (regression)", lambda: load({"a": "1", "b": "2"}), {"a": 1, "b": 2}),
    ("empty maps to empty (regression)", lambda: load({}), {}),
    ("non-numeric value is skipped, not fatal",
     lambda: load({"a": "1", "b": "x", "c": "3"}), {"a": 1, "c": 3}),
    ("real error still surfaces", lambda: _raises(None), True),
]


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
