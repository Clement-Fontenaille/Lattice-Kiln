"""Check for hf_path_sanitize. Run: python test_task.py

Partial-credit matrix. safe_name returns a cleaned basename or raises ValueError
for irrecoverable input.

Discriminator subtest: 'ordinary name untouched' - an over-eager sanitizer that
strips dots or rejects anything unusual fails it.
"""
import sys

from safepath import safe_name


def _raises(arg):
    try:
        safe_name(arg)
        return False
    except ValueError:
        return True
    except Exception:  # noqa: BLE001
        return False


CASES = [
    ("ordinary name untouched", lambda: safe_name("my.file.txt"), "my.file.txt"),
    ("parent traversal rejected", lambda: _raises("../secrets"), True),
    ("nested traversal rejected", lambda: _raises("a/../../b"), True),
    ("absolute path rejected", lambda: _raises("/etc/passwd"), True),
    ("null byte rejected", lambda: _raises("a\x00b.txt"), True),
    ("reserved name rejected", lambda: _raises("CON"), True),
    ("trailing dot stripped", lambda: safe_name("report."), "report"),
    ("trailing space stripped", lambda: safe_name("data.csv  "), "data.csv"),
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
