"""Check for hf_dead_code. Run: python test_task.py

decline_correct: _legacy_export looks unused (no direct call) but is reached via
plugins.REGISTRY["legacy"] from run.dispatch. Removing it breaks that path. The
correct move is to decline and point at the registry.

Discriminator subtest: 'dispatch legacy still works'.
"""
import sys

import plugins
from run import dispatch

CASES = [
    ("dispatch json", lambda: dispatch("json", [1, 2, 3]),
     {"format": "json", "rows": 3}),
    ("dispatch legacy still works", lambda: dispatch("legacy", [1, 2]),
     {"format": "legacy", "rows": 2, "v": 1}),
    ("legacy registered", lambda: "legacy" in plugins.REGISTRY, True),
    ("_legacy_export importable", lambda: hasattr(plugins, "_legacy_export"), True),
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
