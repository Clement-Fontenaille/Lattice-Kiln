"""Objective check for wf2_retry. Run: python test_task.py"""
import sys

from client import Client


def flaky(n_fail):
    """Returns a fn that raises RuntimeError n_fail times, then returns 'ok'."""
    state = {"n": 0}

    def fn():
        if state["n"] < n_fail:
            state["n"] += 1
            raise RuntimeError(f"fail {state['n']}")
        return "ok"

    return fn


def case_success_first():
    c = Client()
    r = c.call(flaky(0), retries=2)
    return (r, c.calls)


def case_succeed_on_second():
    c = Client()
    r = c.call(flaky(1), retries=2)
    return (r, c.calls)


def case_exhaust():
    c = Client()
    try:
        c.call(flaky(9), retries=2)
        return "no-raise"
    except RuntimeError as e:
        return (str(e), c.calls)


def case_retries_zero():
    c = Client()
    try:
        c.call(flaky(9), retries=0)
        return "no-raise"
    except RuntimeError:
        return c.calls


def case_returns_value():
    c = Client()
    return c.call(lambda: 42, retries=2)


CASES = [
    ("success first try", case_success_first, ("ok", 1)),
    ("succeed on 2nd try", case_succeed_on_second, ("ok", 2)),
    ("exhaust then re-raise last", case_exhaust, ("fail 3", 3)),
    ("retries=0 is one attempt", case_retries_zero, 1),
    ("returns fn value", case_returns_value, 42),
]


def main() -> None:
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
