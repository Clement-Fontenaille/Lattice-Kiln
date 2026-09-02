"""Check for hf_multi_recipient. Run: python test_task.py

Discriminator subtest: 'string not iterated char-wise' - a naive `for r in to:`
rewrite turns notify("bob", m) into three deliveries b, o, b.
"""
import sys

import notify as N
from notify import notify


def reset():
    N.SENT.clear()


CASES = [
    ("single string still works (regression)",
     lambda: (reset(), notify("alice", "hi"), list(N.SENT))[-1], [("alice", "hi")]),
    ("string not iterated char-wise",
     lambda: (reset(), notify("bob", "hi"), len(N.SENT))[-1], 1),
    ("list of recipients fans out",
     lambda: (reset(), notify(["a", "b"], "hi"), list(N.SENT))[-1],
     [("a", "hi"), ("b", "hi")]),
    ("tuple of recipients fans out",
     lambda: (reset(), notify(("x", "y"), "m"), list(N.SENT))[-1],
     [("x", "m"), ("y", "m")]),
    ("single string return unchanged (regression)",
     lambda: (reset(), notify("alice", "hi"))[-1], "sent to alice"),
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
