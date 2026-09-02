"""Check for hf_pagination. Run: python test_task.py

Pages are 1-indexed. Correct: start = (num - 1) * size.

Discriminator subtest: 'page 1 is the first items' - the current num*size skips
them; and 'last partial page' - a fix that also changes the slice end drops the
tail element.
"""
import sys

from page import page

ITEMS = list(range(10))

CASES = [
    ("page 1 is the first items", lambda: page(ITEMS, 1, 3), [0, 1, 2]),
    ("page 2", lambda: page(ITEMS, 2, 3), [3, 4, 5]),
    ("last partial page", lambda: page(ITEMS, 4, 3), [9]),
    ("past the end is empty", lambda: page(ITEMS, 5, 3), []),
    ("exact multiple last page", lambda: page(ITEMS, 5, 2), [8, 9]),
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
