"""Check for hf_dict_dispatch. Run: python test_task.py

Discriminator: 'unknown falls through' - a dict dispatch that does
handlers[cmd](ctx) with no default raises KeyError on an unknown command.
"""
import inspect
import re
import sys

import router
from router import route


def ctx(items=None):
    return {"items": list(items or []), "arg": "x", "audit_count": 0}


CASES = [
    ("add", lambda: route("add", (c := ctx())) and c["items"], ["x"]),
    ("remove present", lambda: (c := ctx(["x", "y"]), route("remove", c), c["items"])[-1], ["y"]),
    ("remove absent is quiet", lambda: (c := ctx(["y"]), route("remove", c), c["items"])[-1], ["y"]),
    ("count", lambda: route("count", ctx(["a", "b", "c"])), "3"),
    ("unknown falls through", lambda: route("frobnicate", ctx()), "unknown command: frobnicate"),
    ("audit side effect accumulates",
     lambda: (c := ctx(), route("audit", c), route("audit", c), c["audit_count"])[-1], 2),
    ("audit return value", lambda: route("audit", ctx()), "audit #1"),
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

    src = inspect.getsource(router)
    body = inspect.getsource(route)
    s = 0
    s += 1 if not re.search(r"\belif\b", body) else 0
    s += 1 if re.search(r"\{[^}]*:", body) or re.search(r"=\s*\{", src) else 0   # a dict literal
    s += 1 if len([l for l in body.splitlines()[1:] if l.strip()]) <= 10 else 0
    print(f"STRUCTSCORE {s}/3")
    if re.search(r"\belif\b", body):
        print("  still an if/elif chain")

    sys.exit(0 if passed == len(CASES) else 1)


main()
