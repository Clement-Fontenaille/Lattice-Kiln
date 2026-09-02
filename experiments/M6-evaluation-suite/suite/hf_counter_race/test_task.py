"""Check for hf_counter_race. Run: python test_task.py

Discriminator subtest: 'concurrent increments do not lose updates' - the
read-modify-write with a yield point drops updates without a lock around the
whole operation.
"""
import sys
import threading
import time

from counter import Counter

N_THREADS, PER = 8, 500


def hammer():
    c = Counter()
    threads = [threading.Thread(target=lambda: [c.incr() for _ in range(PER)])
               for _ in range(N_THREADS)]
    t0 = time.monotonic()
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=10)
    return c.n, time.monotonic() - t0, any(t.is_alive() for t in threads)


CASES = [
    ("single-threaded still works",
     lambda: (lambda c: ([c.incr() for _ in range(5)], c.n)[-1])(Counter()), 5),
    ("concurrent increments do not lose updates",
     lambda: hammer()[0], N_THREADS * PER),
    ("no deadlock", lambda: not hammer()[2], True),
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
