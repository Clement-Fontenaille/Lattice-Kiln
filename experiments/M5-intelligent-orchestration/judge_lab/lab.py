"""Judge-lab: run several review pipelines over the frozen scenarios and compare
verdict-vs-truth (and, in the transcripts, the reasoning).

Pipelines
---------
  baseline : the plain reviewer, one call, K samples, majority verdict.
             (this is the M5 reviewer - the thing that hallucinates criteria.)
  vote     : same reviewer, K=5, temp 0.5, majority. "vote down the noise".
  ground   : deterministic prechecks (parse/import/test) + a checklist +
             a one-call-per-clause panel handed the real test output +
             deterministic aggregation. "ground the judgment".

Usage:
  python lab.py                 # all scenarios, all pipelines
  python lab.py --only ground   # one pipeline
  python lab.py --scn wf3_trap  # one scenario
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURES = HERE.parent / "fixture_workflow"
sys.path.insert(0, str(HERE.parent.parent / "M4-ephemeral-processors"))

from ollama_client import DEFAULT_MODEL, generate, health  # noqa: E402
from scenarios import SCENARIOS  # noqa: E402

RUNS = HERE / "runs"
RESULT = HERE / "results.md"

_JSON1 = re.compile(r"\{[^{}]*\}", re.S)
_CHANGE_VERB = re.compile(
    r"\b(fixed|added|implemented|extracted|rewrote|patched|refactored|changed|"
    r"updated|removed)\b", re.I)
_KEPT_VERB = re.compile(r"\b(kept|left|unchanged|did not change|no change)\b", re.I)


# ---------------------------------------------------------------- workspace

def build_ws(scn) -> Path:
    ws = Path(tempfile.mkdtemp(prefix=f"judge_{scn.id}_"))
    src = FIXTURES / scn.fixture
    for p in src.iterdir():
        if p.is_file():
            shutil.copy2(p, ws / p.name)
    for name, body in scn.files.items():
        (ws / name).write_text(body, encoding="utf-8")
    return ws


def run_test(ws: Path) -> dict:
    try:
        cp = subprocess.run([sys.executable, "test_task.py"], cwd=ws,
                            capture_output=True, text=True, timeout=30)
        out = (cp.stdout + cp.stderr).strip()
        m = re.search(r"SUBTESTS (\d+)/(\d+)", out)
        return {"exit": cp.returncode, "out": out,
                "subtests": (int(m.group(1)), int(m.group(2))) if m else None}
    except subprocess.TimeoutExpired:
        return {"exit": -1, "out": "TIMEOUT", "subtests": None}


# ---------------------------------------------------------------- prechecks

def precheck(scn, ws: Path) -> dict:
    pc: dict = {"parses": True, "import_error": None, "changed": False,
                "claim_asserts_change": bool(_CHANGE_VERB.search(scn.claim))
                and not _KEPT_VERB.search(scn.claim)}
    for name, body in scn.files.items():
        orig = scn.originals.get(name)
        if orig is None or body != orig:
            pc["changed"] = True
        if name.endswith(".py"):
            try:
                ast.parse(body)
            except SyntaxError as e:
                pc["parses"] = False
                pc["syntax_error"] = f"{name}: {e}"
    mod = next((n[:-3] for n in scn.files if n.endswith(".py")), None)
    if mod:
        cp = subprocess.run([sys.executable, "-c", f"import {mod}"], cwd=ws,
                            capture_output=True, text=True, timeout=20)
        if cp.returncode != 0:
            pc["import_error"] = cp.stderr.strip().splitlines()[-1][:200]
    pc["test"] = run_test(ws)
    return pc


# ---------------------------------------------------------------- checklist

def _det_checklist(objective: str) -> list[str]:
    parts = re.split(r";|\.\s+|\band\b(?=\s+[a-z])", objective)
    return [p.strip(" .") for p in parts if len(p.strip()) > 12][:6]


def checklist(objective: str) -> tuple[list[str], str]:
    prompt = (
        "Rewrite this objective as a numbered list of 2 to 5 checkable "
        "requirements a correct solution MUST satisfy. One requirement per "
        "line, imperative, concrete. No preamble.\n\nOBJECTIVE:\n" + objective)
    try:
        g = generate(prompt, temperature=0.1, num_predict=220)
        items = [re.sub(r"^\s*\d+[\.\)]\s*", "", ln).strip()
                 for ln in g.text.splitlines() if re.match(r"\s*\d+[\.\)]", ln)]
        items = [i for i in items if len(i) > 8]
        if 2 <= len(items) <= 6:
            return items, g.text.strip()
    except Exception as e:  # noqa: BLE001
        return _det_checklist(objective), f"(model failed: {e!r}; deterministic split)"
    return _det_checklist(objective), "(model output unusable; deterministic split)"


# ---------------------------------------------------------------- panel

def _files_blob(scn) -> str:
    return "\n".join(f"--- {n} ---\n{b}" for n, b in scn.files.items())


def panel(items: list[str], files_blob: str, test_out: str) -> list[dict]:
    res = []
    for it in items:
        prompt = (
            "Check ONE requirement against a submission. Be strict; cite "
            "evidence you can literally see.\n\n"
            f"REQUIREMENT: {it}\n\n"
            f"SUBMISSION FILES:\n{files_blob}\n\n"
            f"TEST OUTPUT (ground truth - trust this over your own reading):\n"
            f"{test_out}\n\n"
            'Answer with one line of JSON only:\n'
            '{"verdict": "met" | "not_met" | "unsure", '
            '"evidence": "<a verbatim line from a file or the test output>"}')
        try:
            g = generate(prompt, temperature=0.1, num_predict=160)
            m = _JSON1.search(g.text)
            obj = json.loads(m.group(0)) if m else {}
            v = str(obj.get("verdict", "unsure")).lower().replace(" ", "_")
            if v not in ("met", "not_met", "unsure"):
                v = "unsure"
            res.append({"item": it, "verdict": v,
                        "evidence": str(obj.get("evidence", ""))[:200],
                        "raw": g.text.strip()})
        except Exception as e:  # noqa: BLE001
            res.append({"item": it, "verdict": "unsure", "evidence": "",
                        "raw": f"ERROR {e!r}"})
    return res


# ---------------------------------------------------------------- baseline / vote

def _reviewer_call(scn, temperature: float) -> dict:
    prompt = (
        "You are an independent reviewer.\n\n"
        f"OBJECTIVE: {scn.objective}\n\n"
        f"IMPLEMENTER CLAIM: {scn.claim}\n\n"
        f"FILES WRITTEN:\n{_files_blob(scn)}\n\n"
        "Is the objective met? Answer with one line of JSON only:\n"
        '{"verdict": "approve" | "needs-change", "reason": "<one sentence>"}')
    g = generate(prompt, temperature=temperature, num_predict=200)
    m = _JSON1.search(g.text)
    obj = json.loads(m.group(0)) if m else {}
    v = str(obj.get("verdict", "?")).lower().strip()
    v = "needs-change" if "need" in v else ("approve" if "approv" in v else "?")
    return {"verdict": v, "reason": str(obj.get("reason", ""))[:200],
            "raw": g.text.strip()}


def run_baseline(scn, k: int) -> dict:
    calls = [_reviewer_call(scn, 0.2) for _ in range(k)]
    votes = Counter(c["verdict"] for c in calls)
    return {"verdict": votes.most_common(1)[0][0], "spread": dict(votes),
            "calls": calls}


def run_vote(scn, k: int = 5) -> dict:
    calls = [_reviewer_call(scn, 0.5) for _ in range(k)]
    votes = Counter(c["verdict"] for c in calls)
    return {"verdict": votes.most_common(1)[0][0], "spread": dict(votes),
            "calls": calls}


# ---------------------------------------------------------------- ground

def run_ground(scn, use_test: bool = True) -> dict:
    ws = build_ws(scn)
    try:
        pc = precheck(scn, ws)
    finally:
        shutil.rmtree(ws, ignore_errors=True)

    hard = None
    if not pc["parses"]:
        hard = "needs-change (syntax error)"
    elif pc["import_error"]:
        hard = "needs-change (import error)"
    elif pc["claim_asserts_change"] and not pc["changed"]:
        hard = "needs-change (claim asserts a change; files are unchanged)"

    items, cl_raw = checklist(scn.objective)
    test_blob = pc["test"]["out"] if use_test else "(no automated test available)"
    pnl = panel(items, _files_blob(scn), test_blob) if not hard else []

    panel_v = "approve"
    if any(p["verdict"] == "not_met" for p in pnl):
        panel_v = "needs-change"
    elif any(p["verdict"] == "unsure" for p in pnl):
        panel_v = "escalate"

    test_v = None
    if use_test and pc["test"]["subtests"]:
        a, b = pc["test"]["subtests"]
        test_v = "approve" if (a == b and pc["test"]["exit"] == 0) else "needs-change"
    elif use_test and pc["test"]["exit"] == 0:
        test_v = "approve"
    elif use_test and pc["test"]["exit"] not in (None,):
        test_v = "needs-change"

    if hard:
        final = hard.split()[0]
    elif test_v == "needs-change" or panel_v == "needs-change":
        final = "needs-change"
    elif panel_v == "escalate":
        final = "escalate"
    else:
        final = "approve"

    return {"verdict": final, "hard": hard, "precheck": pc, "checklist": items,
            "checklist_raw": cl_raw, "panel": pnl, "panel_verdict": panel_v,
            "test_verdict": test_v}


# ---------------------------------------------------------------- driver

def _score(v: str, expect: str) -> str:
    if v == expect:
        return "OK"
    if v == "escalate":
        return "esc"
    return "MISS"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["baseline", "vote", "ground", "ground_notest"])
    ap.add_argument("--scn")
    ap.add_argument("--k", type=int, default=3)
    args = ap.parse_args()
    if not health():
        print("Ollama down", file=sys.stderr)
        sys.exit(1)

    scns = [s for s in SCENARIOS if not args.scn or s.id == args.scn]
    pipes = [args.only] if args.only else ["baseline", "vote", "ground_notest", "ground"]
    RUNS.mkdir(parents=True, exist_ok=True)

    t0 = time.monotonic()
    table: list[tuple] = []
    for scn in scns:
        row = {"id": scn.id, "expect": scn.expect}
        dump = [f"# {scn.id}  expect={scn.expect}", f"_{scn.why}_",
                f"\nOBJECTIVE: {scn.objective}\nCLAIM: {scn.claim}\n"]
        for pipe in pipes:
            if pipe == "baseline":
                r = run_baseline(scn, args.k)
            elif pipe == "vote":
                r = run_vote(scn)
            elif pipe == "ground_notest":
                r = run_ground(scn, use_test=False)
            else:
                r = run_ground(scn, use_test=True)
            row[pipe] = r["verdict"]
            dump.append(f"\n## {pipe}  ->  {r['verdict']}   {_score(r['verdict'], scn.expect)}")
            dump.append(_detail(pipe, r))
            print(f"  {scn.id:16} {pipe:9} -> {r['verdict']:13} {_score(r['verdict'], scn.expect)}")
        (RUNS / f"{scn.id}.md").write_text("\n".join(dump), encoding="utf-8")
        table.append(row)

    _write_results(table, pipes, time.monotonic() - t0)
    print(f"\n{time.monotonic() - t0:.0f}s -> {RESULT}")


def _detail(pipe: str, r: dict) -> str:
    if pipe in ("baseline", "vote"):
        lines = [f"spread: {r['spread']}"]
        for c in r["calls"]:
            lines.append(f"  [{c['verdict']}] {c['reason']}")
        return "\n".join(lines)
    p = r["precheck"]
    lines = [
        f"prechecks: parses={p['parses']} import_error={p['import_error']} "
        f"changed={p['changed']} claim_asserts_change={p['claim_asserts_change']} "
        f"test_exit={p['test']['exit']} subtests={p['test']['subtests']}",
        f"test_out:\n    " + p["test"]["out"].replace("\n", "\n    "),
        f"hard_fail: {r['hard']}",
        f"checklist ({len(r['checklist'])}): " + " | ".join(r["checklist"]),
        f"  raw: {r['checklist_raw']}",
        f"panel_verdict={r['panel_verdict']}  test_verdict={r['test_verdict']}",
    ]
    for pn in r["panel"]:
        lines.append(f"  [{pn['verdict']:8}] {pn['item'][:70]}")
        lines.append(f"             ev: {pn['evidence']}")
    return "\n".join(lines)


def _write_results(table, pipes, dur):
    out = [f"# Judge-lab results",
           f"_model {DEFAULT_MODEL}, {len(table)} scenarios, {dur:.0f}s_", "",
           "| scenario | expect | " + " | ".join(pipes) + " |",
           "|" + "---|" * (len(pipes) + 2)]
    tallies = {p: [0, 0] for p in pipes}  # [correct, total]
    for row in table:
        cells = []
        for p in pipes:
            v = row.get(p, "-")
            mark = "OK" if v == row["expect"] else ("esc" if v == "escalate" else "**MISS**")
            cells.append(f"{v} {mark}")
            tallies[p][1] += 1
            if v == row["expect"]:
                tallies[p][0] += 1
        out.append(f"| {row['id']} | {row['expect']} | " + " | ".join(cells) + " |")
    out += ["", "| pipeline | correct |", "|---|---|"]
    for p in pipes:
        c, t = tallies[p]
        out.append(f"| {p} | {c}/{t} |")
    RESULT.write_text("\n".join(out), encoding="utf-8")


if __name__ == "__main__":
    main()
