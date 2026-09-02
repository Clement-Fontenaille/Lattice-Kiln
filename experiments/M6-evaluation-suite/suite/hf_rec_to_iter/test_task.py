"""Check for hf_rec_to_iter. Run: python test_task.py

Discriminator: 'deep chain 5000' - the recursive version raises RecursionError;
an iterative version with an explicit stack does not. The base cases (None -> 0,
leaf -> 1) must survive the rewrite.
"""
import inspect
import sys

import tree
from tree import count_nodes


def chain(n):
    root = node = {"v": 0}
    for i in range(1, n):
        node["children"] = [{"v": i}]
        node = node["children"][0]
    return root


def wide(n):
    return {"children": [{"v": i} for i in range(n)]}


CASES = [
    ("none is zero", lambda: count_nodes(None), 0),
    ("single leaf", lambda: count_nodes({"v": 1}), 1),
    ("small tree", lambda: count_nodes({"children": [{"v": 1}, {"children": [{"v": 2}]}]}), 4),
    ("wide", lambda: count_nodes(wide(500)), 501),
    ("deep chain 5000", lambda: count_nodes(chain(5000)), 5000),
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

    body = inspect.getsource(count_nodes)
    # STRUCTSCORE: is it actually iterative (no self-recursion)?
    inner = "\n".join(body.splitlines()[1:])
    s = 1 if "count_nodes(" not in inner else 0
    print(f"STRUCTSCORE {s}/1")
    if not s:
        print("  count_nodes still calls itself")

    sys.exit(0 if passed == len(CASES) else 1)


main()
