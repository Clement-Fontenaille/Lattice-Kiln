"""Check for hf_retry_backoff. Run: python test_task.py

send() should retry a Transient failure up to 3 extra times (4 attempts total),
then re-raise the last Transient. A Permanent failure is raised on attempt 1 -
never retried.

Discriminator subtest: 'permanent is not retried'.
"""
import sys

from sender import Permanent, Sender, Transient


def run(payload):
    s = Sender()
    try:
        r = s.send(payload)
        return ("ok", r, s.attempts)
    except Transient:
        return ("transient", s.attempts)
    except Permanent:
        return ("permanent", s.attempts)


CASES = [
    ("happy path (regression)", lambda: run("ok"), ("ok", "ok", 1)),
    ("recovers after 2 transients", lambda: run("flaky2"), ("ok", "ok", 3)),
    ("gives up after 4 attempts", lambda: run("always"), ("transient", 4)),
    ("permanent is not retried", lambda: run("permanent"), ("permanent", 1)),
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
