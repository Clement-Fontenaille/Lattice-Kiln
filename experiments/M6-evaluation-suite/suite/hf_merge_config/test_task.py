"""Check for hf_merge_config. Run: python test_task.py

Discriminator subtests: 'nested dict merges' (shallow merge replaces the whole
sub-dict) and 'None deletes the key' (shallow merge sets it to None).
"""
import sys

from merge import merge

CASES = [
    ("flat override", lambda: merge({"a": 1, "b": 2}, {"b": 3}), {"a": 1, "b": 3}),
    ("nested dict merges",
     lambda: merge({"x": {"p": 1, "q": 2}}, {"x": {"q": 9}}), {"x": {"p": 1, "q": 9}}),
    ("None deletes the key", lambda: merge({"a": 1, "b": 2}, {"b": None}), {"a": 1}),
    ("list replaces, not concat",
     lambda: merge({"l": [1, 2, 3]}, {"l": [9]}), {"l": [9]}),
    ("deep merge plus delete",
     lambda: merge({"s": {"keep": 1, "drop": 2}}, {"s": {"drop": None, "add": 3}}),
     {"s": {"keep": 1, "add": 3}}),
    ("base untouched",
     lambda: (lambda b: (merge(b, {"a": 9}), b))({"a": 1})[-1], {"a": 1}),
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
