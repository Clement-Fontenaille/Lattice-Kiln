"""Check for hf_timeout_param. Run: python test_task.py

Discriminator subtest: 'timeout=0 still times out' - `if timeout:` treats 0 as
"no timeout" and lets a slow fetch through.
"""
import sys

from fetch import fetch


def _raises(fn, exc):
    try:
        fn()
        return False
    except exc:
        return True
    except Exception:  # noqa: BLE001
        return False


CASES = [
    ("no-arg call unchanged (regression)", lambda: fetch("a.example"), "ok-a"),
    ("default = no timeout, slow ok (regression-ish)", lambda: fetch("slow.example"), "ok-slow"),
    ("positive timeout, fast ok", lambda: fetch("b.example", timeout=5), "ok-b"),
    ("positive timeout, slow raises",
     lambda: _raises(lambda: fetch("slow.example", timeout=1), TimeoutError), True),
    ("timeout=0 still times out",
     lambda: _raises(lambda: fetch("slow.example", timeout=0), TimeoutError), True),
    ("timeout=0, fast still ok", lambda: fetch("a.example", timeout=0), "ok-a"),
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
