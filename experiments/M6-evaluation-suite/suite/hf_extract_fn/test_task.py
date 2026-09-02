"""Check for hf_extract_fn. Run: python test_task.py

Behaviour must be identical after the refactor. The discriminator is
'skips bad record' - a naive split that inlines the transform without the
try/except crashes on a record missing "amount".
"""
import inspect
import sys

import pipeline
from pipeline import process

GOOD = [{"amount": 10, "name": "a"}, {"amount": 5, "name": "b", "double": True}]
MIXED = [{"amount": 10}, {"name": "no-amount"}, {"amount": 3, "double": True}]

CASES = [
    ("empty input early-return", lambda: process([]),
     {"ok": [], "skipped": [], "total": 0}),
    ("normal", lambda: process(GOOD),
     {"ok": [{"name": "a", "value": 10}, {"name": "b", "value": 10}],
      "skipped": [], "total": 20}),
    ("skips bad record", lambda: process(MIXED)["ok"],
     [{"name": "?", "value": 10}, {"name": "?", "value": 6}]),
    ("bad record is logged", lambda: len(process(MIXED)["skipped"]), 1),
    ("all-bad input", lambda: process([{"x": 1}, {"y": 2}]),
     {"ok": [], "skipped": ["{'x': 1}: missing 'amount'", "{'y': 2}: missing 'amount'"],
      "total": 0}),
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

    # STRUCTSCORE: did it actually split the function?
    src = inspect.getsource(pipeline)
    helpers = [n for n, o in vars(pipeline).items()
               if inspect.isfunction(o) and o.__module__ == "pipeline" and n != "process"]
    body = inspect.getsource(process).splitlines()
    body_lines = len([l for l in body[1:] if l.strip() and not l.strip().startswith("#")])
    s = 0
    s += 1 if len(helpers) >= 2 else 0
    s += 1 if body_lines <= 12 else 0
    s += 1 if "def process" in src else 0
    print(f"STRUCTSCORE {s}/3")
    if len(helpers) < 2:
        print(f"  process not split (helpers: {helpers})")
    if body_lines > 12:
        print(f"  process body still {body_lines} lines")

    sys.exit(0 if passed == len(CASES) else 1)


main()
