"""Check for hf_json_field. Run: python test_task.py

Add a `tier` field to the response. Records without a "tier" key (they predate
the field) must default to "free".

Discriminator subtest: 'old record defaults to free' - `rec["tier"]` without a
.get default raises KeyError on a pre-tier record.
"""
import sys

from resp import build

NEW = {"id": 1, "name": "x", "tier": "pro"}
OLD = {"id": 2, "name": "y"}


CASES = [
    ("id preserved (regression)", lambda: build(NEW)["id"], 1),
    ("name preserved (regression)", lambda: build(OLD)["name"], "y"),
    ("tier from record", lambda: build(NEW)["tier"], "pro"),
    ("old record defaults to free", lambda: build(OLD)["tier"], "free"),
    ("no extra keys", lambda: set(build(NEW)), {"id", "name", "tier"}),
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
