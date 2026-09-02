"""Check for hf_validate_withdraw. Run: python test_task.py

Discriminator subtests: 'exact balance is allowed' and 'zero is a no-op' -
over-validation (amt <= 0 or amt >= balance) rejects legitimate calls.
"""
import sys

from bank import withdraw


def _raises(acct, amt):
    try:
        withdraw(acct, amt)
        return False
    except (ValueError, TypeError):
        return True
    except Exception:  # noqa: BLE001
        return False


CASES = [
    ("normal withdrawal (regression)", lambda: withdraw({"balance": 100}, 30), 70),
    ("exact balance is allowed", lambda: withdraw({"balance": 100}, 100), 0),
    ("zero is a no-op", lambda: withdraw({"balance": 100}, 0), 100),
    ("negative amount rejected", lambda: _raises({"balance": 100}, -5), True),
    ("overdraw rejected", lambda: _raises({"balance": 100}, 150), True),
    ("non-numeric rejected", lambda: _raises({"balance": 100}, "lots"), True),
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
