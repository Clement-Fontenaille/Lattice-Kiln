"""Check for hf_json_serialize. Run: python test_task.py

Multi-concern: SUBTESTS = serialization (gates), STRUCTSCORE = the round-trip
helper + module docstring (quality).

Discriminator subtest: 'unknown type still raises' - an over-broad default=str
serializes anything and hides real bugs.
"""
import json
import sys

import ser
from ser import to_json

try:
    from ser import from_json
except ImportError:
    from_json = None

from datetime import datetime
from decimal import Decimal


def _loads(s):
    return json.loads(s)


class Weird:
    pass


CASES = [
    ("plain dict (regression)", lambda: _loads(to_json({"a": 1, "b": [2, 3]})),
     {"a": 1, "b": [2, 3]}),
    ("datetime to ISO",
     lambda: _loads(to_json({"t": datetime(2020, 1, 2, 3, 4, 5)}))["t"],
     "2020-01-02T03:04:05"),
    ("set to sorted list",
     lambda: _loads(to_json({"s": {3, 1, 2}}))["s"], [1, 2, 3]),
    ("Decimal to string",
     lambda: _loads(to_json({"d": Decimal("1.50")}))["d"], "1.50"),
    ("unknown type still raises",
     lambda: _raises(lambda: to_json({"x": Weird()})), True),
]


def _raises(fn):
    try:
        fn()
        return False
    except (TypeError, ValueError):
        return True
    except Exception:  # noqa: BLE001
        return False


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

    s = 0
    doc = (ser.__doc__ or "").strip()
    s += 1 if len(doc) >= 20 else 0
    try:
        s += 1 if from_json and from_json(to_json({"a": 1, "b": 2})) == {"a": 1, "b": 2} else 0
    except Exception:  # noqa: BLE001
        pass
    print(f"STRUCTSCORE {s}/2")

    sys.exit(0 if passed == len(CASES) else 1)


main()
