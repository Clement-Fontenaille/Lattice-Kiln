"""Check for hf_csv. Run: python test_task.py

Partial-credit: 6 subtests of increasing quoting/encoding difficulty. The
stdlib `csv` module is a fine way to pass them.

Discriminator subtest: 'quoted comma' - the naive line.split(",") splits inside
the quotes.
"""
import sys

from csvparse import parse

CASES = [
    ("plain rows", lambda: parse("a,b,c\nd,e,f"), [["a", "b", "c"], ["d", "e", "f"]]),
    ("quoted comma", lambda: parse('x,"a,b",y'), [["x", "a,b", "y"]]),
    ("quoted newline", lambda: parse('x,"l1\nl2",y'), [["x", "l1\nl2", "y"]]),
    ("leading BOM", lambda: parse("﻿a,b"), [["a", "b"]]),
    ("CRLF line endings", lambda: parse("a,b\r\nc,d"), [["a", "b"], ["c", "d"]]),
    ("trailing blank line", lambda: parse("a,b\n"), [["a", "b"]]),
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
