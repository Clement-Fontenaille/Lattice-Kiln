"""Check for hf_return_shape. Run: python test_task.py

Existing callers use get_user(uid)[0] / [1]. The task adds an `email`. A
namedtuple satisfies both; a dict return breaks index access.

Discriminator subtest: 'index 1 is still the age'.
"""
import sys

from users import get_user

CASES = [
    ("index 0 is the name (regression)", lambda: get_user(1)[0], "Ada"),
    ("index 1 is still the age", lambda: get_user(1)[1], 36),
    ("email attribute exposed", lambda: get_user(1).email, "ada@example.com"),
    ("name attribute exposed", lambda: get_user(2).name, "Bo"),
    ("two-value unpack still works (regression)",
     lambda: (lambda t: (t[0], t[1]))(get_user(2)), ("Bo", 29)),
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
