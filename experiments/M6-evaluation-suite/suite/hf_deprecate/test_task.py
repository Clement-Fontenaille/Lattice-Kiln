"""Check for hf_deprecate. Run: python test_task.py

The task: old_parse must (a) emit a DeprecationWarning, (b) delegate to
new_parse so it returns the same result. new_parse is the pre-existing passing
reference.

Discriminator subtest: 'old_parse matches new_parse' - a deprecation that only
adds the warning but keeps the legacy raw-split fails it.
"""
import sys
import warnings

from parse import new_parse, old_parse

INPUTS = ["a, b ,c", "x,,y", " one ", ""]


def _warns():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        old_parse("a,b")
        return any(issubclass(x.category, DeprecationWarning) for x in w)


CASES = [
    ("new_parse reference (regression)", lambda: new_parse("a, b ,c"), ["a", "b", "c"]),
    ("old_parse emits DeprecationWarning", _warns, True),
    ("old_parse matches new_parse",
     lambda: all(_quiet(old_parse, s) == new_parse(s) for s in INPUTS), True),
    ("old_parse strips like new_parse", lambda: _quiet(old_parse, " one "), ["one"]),
]


def _quiet(fn, s):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return fn(s)


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
