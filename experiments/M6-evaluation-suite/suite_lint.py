"""Lint the M6 evaluation suite against the normative rules in
docs/10-technical/10-evaluation-task-suite.md.

    python suite_lint.py
"""
from __future__ import annotations

import ast
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUITE = HERE / "suite"
STDLIB = set(sys.stdlib_module_names)


def task_local_modules(d: Path) -> set[str]:
    return {p.stem for p in d.glob("*.py")}


def check_task(t, protected) -> list[str]:
    d = SUITE / Path(t["dir"]).name
    errs = []
    if not d.is_dir():
        return [f"missing dir {d}"]
    tt = d / "test_task.py"
    if not tt.is_file():
        return ["no test_task.py"]
    if "test_task.py" not in protected:
        errs.append("test_task.py not in protected_files")

    local = task_local_modules(d)
    try:
        tree = ast.parse(tt.read_text(encoding="utf-8"))
    except SyntaxError as e:
        return [f"test_task.py syntax error: {e}"]
    for node in ast.walk(tree):
        mods = []
        if isinstance(node, ast.Import):
            mods = [a.name.split(".")[0] for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            mods = [node.module.split(".")[0]]
        for m in mods:
            if m not in STDLIB and m not in local:
                errs.append(f"non-stdlib import in check: {m}")

    # runs, and fast
    t0 = time.monotonic()
    try:
        cp = subprocess.run([sys.executable, "test_task.py"], cwd=str(d),
                            capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired:
        return errs + ["check did not finish in 10s"]
    dt = time.monotonic() - t0
    if dt > 2.0:
        errs.append(f"check slow: {dt:.1f}s (> 2s)")
    out = cp.stdout + cp.stderr
    if "SUBTESTS " not in out:
        errs.append("check prints no SUBTESTS line")

    # discriminator documented (non-decline tasks)
    if not t["expect"]["decline_correct"]:
        rd = d / "README.md"
        txt = rd.read_text(encoding="utf-8").lower() if rd.is_file() else ""
        if "discriminator" not in txt:
            errs.append("README has no documented discriminator")

    # pristine passes the regression-guard set: baseline SUBTESTS > 0 unless
    # it's a pure greenfield implement task
    import re
    m = re.search(r"SUBTESTS (\d+)/(\d+)", out)
    if m and t["shape"] not in ("implement", "feature") and int(m.group(1)) == 0:
        errs.append(f"no pre-existing passing subtests (baseline {m.group(0)})")
    return errs


def main():
    doc = json.loads((HERE / "tasks.json").read_text(encoding="utf-8"))
    tasks, protected = doc["tasks"], doc["protected_files"]
    ids = [t["id"] for t in tasks]
    bad = 0
    print(f"suite {doc['suite_version']} - {len(tasks)} tasks\n")
    if len(ids) != len(set(ids)):
        print("DUPLICATE task ids"); bad += 1
    shapes, traps = set(), set()
    for t in tasks:
        errs = check_task(t, protected)
        shapes.add(t["shape"])
        traps.add(t["trap"])
        mark = "ok " if not errs else "ERR"
        print(f"  {mark} {t['id']:22} {t['shape']}/{t['trap']}")
        for e in errs:
            print(f"        - {e}")
            bad += 1
    print(f"\nshapes covered: {sorted(shapes)}")
    print(f"traps covered:  {sorted(traps)}")
    n_decline = sum(t["expect"]["decline_correct"] for t in tasks)
    print(f"decline_correct tasks: {n_decline}")
    print(f"\n{'LINT FAILED' if bad else 'lint clean'} ({bad} issue(s))")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
