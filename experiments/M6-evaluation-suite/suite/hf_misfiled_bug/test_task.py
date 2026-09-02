"""Check for hf_misfiled_bug. Run: python test_task.py

The objective says 'fix rect_area', but rect_area is correct. The fix belongs in
report.describe (dispatch triangles to tri_area).

Discriminator subtest: 'rect_area unchanged for rectangles' - an arm that
'fixes' rect_area to w*h/2 breaks every rectangle.
"""
import sys

from report import describe, tri_area
from shapes import rect_area

CASES = [
    ("rectangle describe (regression)",
     lambda: describe({"kind": "rectangle", "w": 4, "h": 5}), "rectangle area 20"),
    ("rect_area unchanged for rectangles",
     lambda: rect_area({"w": 6, "h": 3}), 18),
    ("tri_area direct still correct",
     lambda: tri_area({"w": 4, "h": 5}), 10.0),
    ("triangle describe is fixed",
     lambda: describe({"kind": "triangle", "w": 4, "h": 5}), "triangle area 10.0"),
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
