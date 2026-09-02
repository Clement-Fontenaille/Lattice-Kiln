"""Objective check for wf6_multi. Run: python test_task.py

Emits three score lines:
  SUBTESTS a/b   - algorithmics (gates objective_pass)
  DOCSCORE c/d   - documentation attended to (quality signal, does not gate)
  TODOSCORE e/f  - TODO gardening (quality signal, does not gate)
"""
import sys
from pathlib import Path

import graphlib
from graphlib import build_graph, topo_sort

SRC = Path(__file__).with_name("graphlib.py").read_text(encoding="utf-8")


def is_topo(order, graph):
    if sorted(order) != sorted(graph):
        return False
    pos = {n: i for i, n in enumerate(order)}
    return all(pos[u] < pos[v] for u in graph for v in graph[u])


def algo():
    passed, fails = 0, []

    def chk(name, cond):
        nonlocal passed
        if cond:
            passed += 1
        else:
            fails.append(name)

    try:
        chk("build_graph basic",
            build_graph([("a", "b"), ("b", "c")]) == {"a": ["b"], "b": ["c"], "c": []})
    except Exception as e:  # noqa: BLE001
        fails.append(f"build_graph basic raised {e!r}")
    try:
        chk("build_graph empty", build_graph([]) == {})
    except Exception as e:  # noqa: BLE001
        fails.append(f"build_graph empty raised {e!r}")
    try:
        g = build_graph([("a", "b"), ("b", "c")])
        chk("topo chain", is_topo(topo_sort(g), g))
    except Exception as e:  # noqa: BLE001
        fails.append(f"topo chain raised {e!r}")
    try:
        g = build_graph([("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")])
        chk("topo diamond", is_topo(topo_sort(g), g))
    except Exception as e:  # noqa: BLE001
        fails.append(f"topo diamond raised {e!r}")
    try:
        topo_sort(build_graph([("a", "b"), ("b", "a")]))
        fails.append("topo cycle: no exception raised")
    except NotImplementedError:
        fails.append("topo cycle: still NotImplementedError")
    except Exception:
        passed += 1
    try:
        chk("topo empty", topo_sort({}) == [])
    except Exception as e:  # noqa: BLE001
        fails.append(f"topo empty raised {e!r}")

    total = 6
    print(f"SUBTESTS {passed}/{total}")
    for f in fails:
        print("  " + f)
    return passed == total


def doc_score():
    pts, notes = 0, []
    md = graphlib.__doc__ or ""
    if len(md.strip()) >= 20:
        pts += 1
    else:
        notes.append("no module docstring")
    bg = build_graph.__doc__ or ""
    if "Args" in bg and "Returns" in bg:
        pts += 1
    else:
        notes.append("build_graph docstring missing Args/Returns")
    ts = topo_sort.__doc__ or ""
    if "Args" in ts and "Returns" in ts and "Raises" in ts:
        pts += 1
    else:
        notes.append("topo_sort docstring missing Args/Returns/Raises")
    notes_md = Path(__file__).with_name("NOTES.md")
    if notes_md.is_file() and "cycle" in notes_md.read_text(encoding="utf-8").lower():
        pts += 1
    else:
        notes.append("NOTES.md missing or no cycle-handling note")
    print(f"DOCSCORE {pts}/4")
    for n in notes:
        print("  " + n)


def todo_score():
    pts, notes = 0, []
    checks = [
        ("implement topo_sort", "TODO: implement topo_sort"),
        ("2019 networkx todo", "TODO(2019)"),
        ("stale O(n^2) todo", "O(n^2)"),
    ]
    for label, needle in checks:
        if needle not in SRC:
            pts += 1
        else:
            notes.append(f"{label} still present")
    print(f"TODOSCORE {pts}/3")
    for n in notes:
        print("  " + n)


def main() -> None:
    ok = algo()
    doc_score()
    todo_score()
    sys.exit(0 if ok else 1)


main()
