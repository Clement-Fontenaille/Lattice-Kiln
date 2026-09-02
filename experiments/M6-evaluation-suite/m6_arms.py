"""Comparison arms for the M6 suite runner.

  monolith : one implementer pass (defined in run_suite).
  dloop    : the loop_lab bundle-D core - incumbent-protected keeper,
             test-gated progress, best-of-N, escalate-on-stall. Reimplemented
             compactly here against the M6 bridge (loop_lab's own harness is
             coupled to fixture_workflow).
  staged   : the Milestone-7 leading candidate - premise audit (K=3) + a
             concern-split-aware dloop core + "refactor with no test signal ->
             escalate". NOT the always-on super-pipeline (that data is already
             in pipeline_lab / findings-log entry 7 addendum).
"""
from __future__ import annotations

import ast
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _m6bridge import Gate, RunRecorder, assemble, generate, run_processor  # noqa: E402

RUNS = HERE / "runs"
CMD = ["python", "test_task.py"]
MAX_ROUNDS = 3
STALL_TOL = 1
_SCORE = re.compile(r"^([A-Z]+SCORE|SUBTESTS)\s+(\d+)\s*/\s*(\d+)", re.M)
_FAIL = re.compile(r"^\s{2,}([^\n]{2,120})$", re.M)
_JSON = re.compile(r"\{.*\}", re.S)


def _py_files(ws: Path):
    return [p for p in ws.glob("*.py") if p.name != "test_task.py"]


def _snap(ws: Path) -> dict:
    return {p.name: p.read_text(encoding="utf-8", errors="replace") for p in _py_files(ws)}
    # NOTES.md etc. are re-created by the arm; only .py is snapshotted


def _restore(ws: Path, snap: dict):
    for p in _py_files(ws):
        if p.name not in snap:
            p.unlink()
    for n, b in snap.items():
        (ws / n).write_text(b, encoding="utf-8")


def _py_ok(ws: Path) -> bool:
    for p in _py_files(ws):
        try:
            ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            return False
    return True


def _score(ws: Path) -> dict:
    try:
        cp = subprocess.run(CMD, cwd=str(ws), capture_output=True, text=True, timeout=30)
        out = (cp.stdout + cp.stderr).strip()
    except subprocess.TimeoutExpired:
        return {"sub": (0, 1), "comb": 0, "tot": 1, "full": False, "fails": "", "py": _py_ok(ws)}
    sc = {m.group(1): (int(m.group(2)), int(m.group(3))) for m in _SCORE.finditer(out)}
    sub = sc.get("SUBTESTS", (0, 1))
    comb = sum(p for p, _ in sc.values())
    tot = sum(t for _, t in sc.values()) or 1
    full = bool(sc) and all(p == t for p, t in sc.values())
    fails = "\n".join(_FAIL.findall(out)[:12])
    return {"sub": sub, "comb": comb, "tot": tot, "full": full, "fails": fails, "py": _py_ok(ws)}


def _implement(objective: str, ws: Path, rec, root):
    b = assemble(objective, ws, token_budget=8000)
    pr = run_processor(role="implementer", objective=objective, context=b, workspace_root=ws,
                       recorder=rec, gate=Gate(), parent_invocation_id=root, intent_ref="m6",
                       interaction_mode="oneshot")
    return pr


def _rec(arm):
    r = RunRecorder(RUNS, intent_text="m6", meta={"arm": arm, "suite": "m6"})
    root = r.invocation(role=f"m6-{arm}", model_identity={"name": "harness"},
                        intent_ref="m6", config_ref="m6")
    return r, root


def _dloop_core(objective: str, ws: Path, rec, root, segments: list[str] | None) -> str:
    targets = segments or [objective]
    incbase = _score(ws)
    best = {"s": incbase, "snap": _snap(ws), "src": "incumbent"}
    for seg in targets:
        stall = 0
        for rnd in range(MAX_ROUNDS):
            if best["s"]["full"] and not segments:
                break
            _restore(ws, best["snap"])
            hint = best["s"]["fails"]
            step = seg
            if rnd or (best["src"] == "incumbent" and best["s"]["sub"][0] > 0) or segments:
                step = (f"{seg}\n\nCurrent state still fails:\n{hint}\n"
                        "Output the whole corrected file(s).")
            _implement(step, ws, rec, root)
            s = _score(ws)
            # never accept a subtest regression, even for a structural gain
            if (s["sub"][0] >= best["s"]["sub"][0] and s["comb"] > best["s"]["comb"]
                    and s["py"]):
                best = {"s": s, "snap": _snap(ws), "src": f"r{rnd}"}
                stall = 0
            else:
                stall += 1
                if stall > STALL_TOL:
                    break
    _restore(ws, best["snap"])
    fin = _score(ws)
    if best["src"] == "incumbent":
        # nothing the arm produced beat the starting point
        return "declined" if fin["full"] else "escalate"
    if fin["full"]:
        return "resolved"
    return "needs-change"


def _segments(objective: str) -> list[str] | None:
    segs = [s.strip() for s in re.split(r"(?=\(\d\))", objective) if re.match(r"\(\d\)", s.strip())]
    return segs if len(segs) >= 2 else None


def run_dloop(objective: str, ws: Path) -> str:
    rec, root = _rec("dloop")
    try:
        return _dloop_core(objective, ws, rec, root, None)
    finally:
        rec.close("completed")


PREMISE = (
    "You are a senior engineer auditing whether a task is SOUND to attempt, before any code "
    "is written. You have the objective and the current code.\n\n"
    "SOUND is the normal case. In particular these are ALL sound:\n"
    "  - the code currently produces the wrong result in the way the objective describes;\n"
    "  - the feature the objective asks for does not exist yet;\n"
    "  - a straightforward refactor or implementation;\n"
    "  - a task that bundles several changes (large / multi-part is NOT a reason for UNSOUND).\n\n"
    "Mark UNSOUND only when the objective cannot be satisfied as literally stated:\n"
    "  (a) the goal is impossible given the code or data (e.g. O(log n) lookup on unordered data);\n"
    "  (b) the premise about what is broken is itself false - the named bug does not exist and "
    "the code is already correct;\n"
    "  (c) the objective is self-contradictory.\n"
    "'the current code is wrong' is NOT a reason for UNSOUND - that is what a fix is for.\n\n"
    'Answer with ONE JSON object: {"sound": true | false, "reason": "<one sentence>"}\n\n'
    "OBJECTIVE:\n{obj}\n\nCODE:\n{code}")


def run_staged(objective: str, ws: Path) -> str:
    rec, root = _rec("staged")
    try:
        code = "\n".join(f"--- {p.name} ---\n{p.read_text(errors='replace')}" for p in _py_files(ws))
        votes = []
        for _ in range(3):
            g = generate(PREMISE.replace("{obj}", objective).replace("{code}", code[:4000]),
                         temperature=0.3, num_predict=180)
            m = _JSON.search(g.text)
            try:
                votes.append(bool(json.loads(m.group(0)).get("sound", True)) if m else True)
            except Exception:  # noqa: BLE001
                votes.append(True)
        if sum(votes) < len(votes) / 2:      # majority unsound
            return "declined"

        base = _score(ws)
        term = _dloop_core(objective, ws, rec, root, _segments(objective))
        fin = _score(ws)
        # refactor with no test signal: subtests were already full and stayed full,
        # but a structural dimension is unmet -> we cannot verify it, escalate
        if base["sub"][0] == base["sub"][1] and fin["sub"][0] == fin["sub"][1] and not fin["full"]:
            return "escalate"
        return term
    finally:
        rec.close("completed")


ARMS_EXTRA = {"dloop": run_dloop, "staged": run_staged}
