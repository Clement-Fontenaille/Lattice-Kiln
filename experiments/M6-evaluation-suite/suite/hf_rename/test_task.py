"""Check for hf_rename. Run: python test_task.py

Discriminator: 'recalc_all intact' + 'wire key unchanged' - a blind
search/replace of 'calc' -> 'compute' renames recalc_all to recompute_all and
changes the LEDGER key from "calc" to "compute", breaking callers and the wire
format.
"""
import inspect
import sys

import billing

SRC = inspect.getsource(billing)

CASES = [
    ("compute exists and works", lambda: billing.compute(10), 12.0),
    ("calc name is gone", lambda: hasattr(billing, "calc"), False),
    ("recalc_all still exists", lambda: hasattr(billing, "recalc_all"), True),
    ("recalc_all still works", lambda: billing.recalc_all([10, 5]), [12.0, 6.0]),
    ("wire key unchanged",
     lambda: (billing.LEDGER.clear(), billing.post(1, 10), "calc" in billing.LEDGER["1"])[-1],
     True),
    ("wire key not renamed",
     lambda: (billing.LEDGER.clear(), billing.post(2, 5), "compute" in billing.LEDGER["2"])[-1],
     False),
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

    s = 0
    s += 1 if "def recalc_all" in SRC else 0
    s += 1 if '"calc"' in SRC or "'calc'" in SRC else 0        # wire key literal kept
    s += 1 if "def compute" in SRC and "def calc(" not in SRC else 0
    print(f"STRUCTSCORE {s}/3")

    sys.exit(0 if passed == len(CASES) else 1)


main()
