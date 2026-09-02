"""Super-pipeline v2 (pipeline_lab) - every promising M5-follow-up idea in one
deliberately call-heavy flow. The per-stage ledger + counterfactual attribution
are the data for pruning redundant stages later.

Flow
----
  S0 premise+classify   K=3 majority; {sound, task_type}; decline authority
  S1 test-spec          from objective; items tagged BEHAVIOURAL / STRUCTURAL
  S2 impl-spec x2       two BLIND specs (diff temp); disagreement = extra
                        underspecification signal
  S3 alignment          ADVISORY only - feeds L2's watch-list, never terminal
  S4 synth tests K=3    blind (no candidate / no impl-spec); parsed to per-CHECK
                        verdicts; run on pristine for a baseline
  S5 coding             2 independent implementations x (here_is_file framing +
                        permissive re-extract + concern-split for conjunctive
                        objectives + keeper-protected progress loop); best of
                        {incumbent, impl_a, impl_b} ships
  S6a L1 verify         provided test + check-level K-way agreement on synth +
                        regression guard (a subtest passing before and failing
                        after = hard needs-change)
  S6b L2 verify         context-diverse structural check; verifier A (diff only)
                        + verifier B (pristine + objective, never sees candidate);
                        VIOLATED and NEEDS-EXECUTION both confirmed by a probe
  S7 reconcile          deterministic rules -> terminal; then counterfactual
                        replay (null each signal, see if terminal flips)

Terminals: declined | resolved | needs-change | escalate

    python superpipe.py                       # 6 tasks x reps=1
    python superpipe.py --tasks wf6_multi --reps 2
    python superpipe.py --smoke
"""
from __future__ import annotations

import argparse
import ast
import difflib
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
M5 = HERE.parent
sys.path.insert(0, str(M5))

from _bridge import Gate, RunRecorder, assemble, generate, health  # noqa: E402
from workflow_suite import (  # noqa: E402
    _run_role, fresh_workspace, load_tasks, objective_check, restore_protected,
)
import roles_super as R  # noqa: E402

RUNS = M5 / "runs"
RESULTS = HERE / "results"
TX_DIR = HERE / "runs_super"
_TX: list = []

K_AUDIT = 3
K_SYNTH = 3
MAX_CODE_ROUNDS = 2
MAX_OBLIGATIONS = 5
DIFF_BUDGET = {"bugfix": 45, "feature": 90, "refactor": 90, "perf": 70, "mixed": 130}
_JSON = re.compile(r"\{.*\}", re.S)


def _gen(prompt: str, *, tag: str = "", **kw):
    g = generate(prompt, **kw)
    _TX.append({"tag": tag, "prompt": prompt, "raw": g.text})
    return g


# ----------------------------------------------------------------- helpers

def _j(text: str) -> dict:
    for rx in (_JSON, re.compile(r"\{[^{}]*\}", re.S)):
        m = rx.search(text or "")
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                continue
    return {}


def _strip_fences(t: str) -> str:
    t = re.sub(r"^\s*```[a-zA-Z]*\n?", "", (t or "").strip())
    return re.sub(r"\n?```\s*$", "", t).strip()


def _py_files(ws: Path) -> list[Path]:
    return [p for p in ws.glob("*.py")
            if p.name != "test_task.py" and not p.name.startswith("_syn_")
            and p.name != "_probe.py"]


def _py_ok(ws: Path) -> bool:
    for p in _py_files(ws):
        try:
            ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            return False
    return True


def snapshot(ws: Path) -> dict[str, str]:
    return {p.name: p.read_text(encoding="utf-8", errors="replace") for p in _py_files(ws)}


def restore(ws: Path, snap: dict[str, str]) -> None:
    for p in _py_files(ws):
        if p.name not in snap:
            p.unlink()
    for name, body in snap.items():
        (ws / name).write_text(body, encoding="utf-8")


def diff_text(before: dict[str, str], after: dict[str, str]) -> str:
    out = []
    for name in sorted(set(before) | set(after)):
        b = before.get(name, "").splitlines(keepends=True)
        a = after.get(name, "").splitlines(keepends=True)
        if b != a:
            out += list(difflib.unified_diff(b, a, f"a/{name}", f"b/{name}", n=2))
    return "".join(out) or "(no change)"


def run_script(ws: Path, name: str, src: str, timeout: int = 20) -> dict:
    p = ws / name
    p.write_text(src, encoding="utf-8")
    try:
        cp = subprocess.run([sys.executable, name], cwd=str(ws),
                            capture_output=True, text=True, timeout=timeout)
        return {"exit": cp.returncode, "out": (cp.stdout + cp.stderr).strip()[-1500:]}
    except subprocess.TimeoutExpired:
        return {"exit": -1, "out": "TIMEOUT"}
    finally:
        p.unlink(missing_ok=True)


_FAIL_LABEL = re.compile(r"^\s{2,}([^:]{2,60}):", re.M)


def fail_labels(tail: str) -> set[str]:
    return {m.group(1).strip() for m in _FAIL_LABEL.finditer(tail or "")}


_CHECK = re.compile(r"CHECK\s+(\S+)\s+(PASS|FAIL)", re.I)


def parse_checks(out: str) -> dict[str, bool]:
    d: dict[str, bool] = {}
    for name, verd in _CHECK.findall(out or ""):
        d[name] = verd.upper() == "PASS"          # last wins
    return d


# permissive extraction: the 7B mangles the FILE marker ~2/3 of the time
_MARK = re.compile(
    r"(?:<<<?\s*FILE\s+path=|#\s*FILE\s+path[:=]\s*|<<file:\s*|#\s*file:\s*)"
    r"([A-Za-z0-9_./-]+\.py)\s*>*\s*\n(.*?)(?:<<<?\s*(?:END)?FILE\s*>*|\Z|\n#\s*end)",
    re.S | re.I)
_FENCE_NAMED = re.compile(r"```(?:python)?\s*\n#\s*([A-Za-z0-9_./-]+\.py)\s*\n(.*?)```", re.S)


def permissive_extract(text: str, known: set[str]) -> dict[str, str]:
    found: dict[str, str] = {}
    for rx in (_MARK, _FENCE_NAMED):
        for name, body in rx.findall(text or ""):
            base = name.split("/")[-1]
            if base in known and base not in found:
                b = _strip_fences(body).rstrip() + "\n"
                if len(b) > 15:
                    found[base] = b
    return found


# ----------------------------------------------------------------- stages

def stage_premise(objective, code_blob, led):
    t0 = time.monotonic()
    vs = []
    for _ in range(K_AUDIT):
        g = _gen(f"{R.PREMISE_AUDIT}\n\nOBJECTIVE:\n{objective}\n\nCODE:\n{code_blob}",
                 tag="S0-premise", temperature=0.3, num_predict=320)
        vs.append(_j(g.text))
    votes = [bool(v.get("sound", True)) for v in vs if v]
    sound = sum(votes) >= len(votes) / 2 if votes else True
    ttypes = [str(v.get("task_type", "")).lower() for v in vs if v.get("task_type")]
    task_type = Counter(ttypes).most_common(1)[0][0] if ttypes else "mixed"
    reason = next((v.get("reason", "") for v in vs if v and not v.get("sound", True)), "")
    action = next((v.get("correct_action", "") for v in vs if v and v.get("correct_action")), "")
    led.append({"stage": "S0-premise", "calls": K_AUDIT, "wall": round(time.monotonic() - t0, 1),
                "out": f"sound={sound} type={task_type} votes={votes} reason={reason!r}"})
    return {"sound": sound, "task_type": task_type, "reason": reason, "correct_action": action}


def stage_test_spec(objective, led):
    t0 = time.monotonic()
    g = _gen(f"{R.TEST_SPEC}\n\nOBJECTIVE:\n{objective}", tag="S1-testspec",
             temperature=0.2, num_predict=500)
    items = []
    for ln in g.text.splitlines():
        m = re.match(r"\s*(?:\d+[.)]\s*)?\[(BEHAVIOURAL|STRUCTURAL)\]\s*(.+)", ln, re.I)
        if m:
            items.append((m.group(1).upper(), m.group(2).strip()))
    led.append({"stage": "S1-testspec", "calls": 1, "wall": round(time.monotonic() - t0, 1),
                "out": f"{len(items)} items "
                       f"{sum(1 for t,_ in items if t=='BEHAVIOURAL')}B/"
                       f"{sum(1 for t,_ in items if t=='STRUCTURAL')}S"})
    return {"items": items, "raw": g.text.strip()}


def stage_impl_spec2(objective, led):
    t0 = time.monotonic()
    specs = []
    for temp in (0.2, 0.55):
        g = _gen(f"{R.IMPL_SPEC}\n\nOBJECTIVE:\n{objective}", tag=f"S2-implspec-t{temp}",
                 temperature=temp, num_predict=350)
        specs.append(R.numbered_list(g.text))
    ta = {w.lower() for s in specs[0] for w in re.findall(r"[a-z_]{4,}", s.lower())}
    tb = {w.lower() for s in specs[1] for w in re.findall(r"[a-z_]{4,}", s.lower())}
    overlap = len(ta & tb) / max(1, len(ta | tb))
    disagree = overlap < 0.35
    led.append({"stage": "S2-implspec", "calls": 2, "wall": round(time.monotonic() - t0, 1),
                "out": f"{len(specs[0])}/{len(specs[1])} steps, overlap={overlap:.2f} disagree={disagree}"})
    return {"steps": specs[0] or specs[1], "alt": specs[1], "disagree": disagree}


def stage_alignment(tspec, ispec, led):
    t0 = time.monotonic()
    tb = "\n".join(f"[{t}] {x}" for t, x in tspec["items"])
    ib = "\n".join(f"- {s}" for s in ispec["steps"])
    g = _gen(f"{R.ALIGNMENT}\n\nTEST SPEC:\n{tb}\n\nIMPL SPEC:\n{ib}",
             tag="S3-alignment", temperature=0.2, num_predict=320)
    d = _j(g.text)
    unver = d.get("unverified") or []
    led.append({"stage": "S3-alignment", "calls": 1, "wall": round(time.monotonic() - t0, 1),
                "out": f"advisory: unverified={len(unver)} unplanned={len(d.get('unplanned') or [])}"})
    return {"unverified": unver, "raw": g.text.strip()}


def stage_synth(objective, behav_items, pristine, ws, led):
    t0 = time.monotonic()
    reqs = "\n".join(f"{i+1}. {x}" for i, x in enumerate(behav_items)) or "(derive from objective)"
    suites = []
    for k in range(K_SYNTH):
        g = _gen(f"{R.TEST_IMPL}\n{reqs}", tag=f"S4-synth-k{k}", temperature=0.5, num_predict=750)
        src = _strip_fences(g.text)
        tmp = Path(tempfile.mkdtemp(prefix="synp_")).resolve()
        try:
            restore(tmp, pristine)
            for e in ws.glob("*.py"):
                if e.name == "test_task.py":
                    shutil.copy2(e, tmp / e.name)
            base = run_script(tmp, f"_syn_{k}.py", src)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        malformed = any(x in base["out"] for x in ("ImportError", "SyntaxError", "IndentationError")) \
            or ("Traceback" in base["out"] and "CHECK" not in base["out"])
        suites.append({"k": k, "src": src, "base_checks": parse_checks(base["out"]),
                       "malformed": malformed})
    nvalid = sum(1 for s in suites if not s["malformed"])
    led.append({"stage": "S4-synth", "calls": K_SYNTH, "wall": round(time.monotonic() - t0, 1),
                "out": f"{nvalid}/{K_SYNTH} valid; checks/suite="
                       + ",".join(str(len(s['base_checks'])) for s in suites)})
    return {"suites": suites, "n_valid": nvalid}


def synth_verdict_on(ws, suites):
    """check-level K-way agreement -> (trusted_fail: bool, detail)."""
    per_suite = []
    for s in suites:
        if s["malformed"]:
            continue
        r = run_script(ws, f"_syn_{s['k']}.py", s["src"])
        per_suite.append(parse_checks(r["out"]))
    if not per_suite:
        return False, "no valid suites"
    names = Counter(n for cs in per_suite for n in cs)
    trusted_fail, detail = [], []
    for name, cnt in names.items():
        if cnt < 2:
            continue
        verds = [cs[name] for cs in per_suite if name in cs]
        if len(set(verds)) == 1 and verds[0] is False:      # agreed FAIL
            trusted_fail.append(name)
        detail.append(f"{name}:{sum(verds)}/{len(verds)}pass")
    return bool(trusted_fail), f"trusted_fail={trusted_fail} | " + " ".join(detail[:8])


# ---- S5 coding -------------------------------------------------------------

def _here_is_file(objective, plan, files: dict[str, str], extra=""):
    blocks = "\n".join(f"<<<FILE path={n}>>>\n{b.rstrip()}\n<<<ENDFILE>>>" for n, b in files.items())
    return (f"{objective}\n\nPlan (follow it):\n{plan}\n{extra}\n\n"
            f"Here is the current content of the file(s). Return the WHOLE file(s), "
            f"changed only where the objective requires, each as a <<<FILE path=...>>> block.\n\n{blocks}")


def _concern_segments(objective: str) -> list[str]:
    segs = re.split(r"(?=\(\d\))", objective)
    segs = [s.strip() for s in segs if re.match(r"\(\d\)", s.strip())]
    return segs if len(segs) >= 2 else []


def _combined(oc: dict) -> int:
    return (oc["sub"][0] + (oc["doc"][0] if oc.get("doc") else 0)
            + (oc["todo"][0] if oc.get("todo") else 0))


def _one_impl(task, ws, objective, plan, cmd, protected, rec, gate, root, temp_tag):
    """one full implementation attempt (concern-split + keeper), returns snapshot+score."""
    def score(w):
        restore_protected(w, task["dir"], protected)
        oc = objective_check(w, cmd)
        return {"sub": oc["sub"][0], "py": _py_ok(w), "comb": _combined(oc), "oc": oc}

    known = set(snapshot(ws))
    incumbent = score(ws)
    best = {"s": incumbent, "snap": snapshot(ws)}
    segments = _concern_segments(objective)
    targets = segments or [objective]

    for seg_i, seg in enumerate(targets):
        for rnd in range(MAX_CODE_ROUNDS):
            if best["s"]["sub"] == best["s"]["oc"]["sub"][1] > 0 and not segments:
                break
            restore(ws, best["snap"])
            files = snapshot(ws)
            sub_obj = seg if segments else objective
            fails = "\n".join(l for l in best["s"]["oc"]["tail"].splitlines()
                              if l.startswith("  ") or "FAIL" in l)[:500]
            extra = f"\nStill failing:\n{fails}" if rnd and fails else ""
            step = _here_is_file(sub_obj, plan, files, extra)
            pr = _run_role("implementer", assemble(step, ws, token_budget=8000),
                           step, ws, rec, gate, root, task["id"])
            if not any(f for f in pr.files_written if f in known):
                for n, b in permissive_extract(pr.body_text or "", known).items():
                    (ws / n).write_text(b, encoding="utf-8")
            _TX.append({"tag": f"S5-impl-{temp_tag}-seg{seg_i}r{rnd}",
                        "prompt": step[:800], "raw": (pr.body_text or "")[:1500]})
            s = score(ws)
            improved = s["comb"] > best["s"]["comb"] or (
                s["comb"] == best["s"]["comb"] and s["py"] and not best["s"]["py"])
            if improved and s["py"]:
                best = {"s": s, "snap": snapshot(ws)}
            elif not segments:
                break
    restore(ws, best["snap"])
    return {"score": score(ws), "snap": best["snap"], "incumbent": incumbent["sub"]}


def stage_coding(task, ws, objective, ispec, cmd, protected, rec, gate, root, task_type, led):
    t0 = time.monotonic()
    plan = "\n".join(f"{i+1}. {s}" for i, s in enumerate(ispec["steps"]))
    n0 = len(_TX)
    pristine = snapshot(ws)
    cand = []
    for tag in ("a", "b"):
        restore(ws, pristine)
        r = _one_impl(task, ws, objective, plan, cmd, protected, rec, gate, root, tag)
        cand.append((tag, r))
    restore(ws, pristine)
    inc_oc = objective_check(ws, cmd)
    pool = [("incumbent", {"score": {"comb": _combined(inc_oc), "py": True, "sub": inc_oc["sub"][0]},
                           "snap": pristine})]
    pool += cand
    winner = max(pool, key=lambda kv: (kv[1]["score"]["comb"], kv[1]["score"]["py"]))
    restore(ws, winner[1]["snap"])
    restore_protected(ws, task["dir"], protected)
    fin = objective_check(ws, cmd)
    a, b = cand[0][1]["score"], cand[1][1]["score"]
    dif = diff_text(pristine, snapshot(ws))
    blowout = len(dif.splitlines()) > DIFF_BUDGET.get(task_type, 130)
    led.append({"stage": "S5-coding", "calls": len(_TX) - n0, "wall": round(time.monotonic() - t0, 1),
                "out": f"incumbent comb={_combined(inc_oc)} | impl_a comb={a['comb']}(sub{a['sub']}) "
                       f"impl_b comb={b['comb']}(sub{b['sub']}) agree={a['comb']==b['comb']} -> "
                       f"winner {winner[0]} sub{fin['sub']} doc{fin['doc']} todo{fin['todo']} "
                       f"diff_lines={len(dif.splitlines())} blowout={blowout}"})
    return {"final_oc": fin, "winner": winner[0], "impl_agree": a["comb"] == b["comb"],
            "diff": dif, "blowout": blowout, "pristine": pristine}


def stage_l2(objective, obligations, pristine, ws, task_type, led):
    t0 = time.monotonic()
    n0 = len(_TX)
    obligations = list(dict.fromkeys(obligations))[:MAX_OBLIGATIONS]
    diff = diff_text(pristine, snapshot(ws))
    orig = "\n".join(f"--- {n} ---\n{b}" for n, b in pristine.items())
    gb = _gen(R.STRUCT_VERIFY_B.format(objective=objective, original=orig),
              tag="S6b-verifierB", temperature=0.3, num_predict=300)
    b_edits = [l.strip() for l in gb.text.splitlines() if "::" in l]
    b_tok = set(re.findall(r"[a-z_]{4,}", " ".join(b_edits).lower()))
    d_tok = set(re.findall(r"[a-z_]{4,}", diff.lower()))
    b_consistent = (not b_tok) or len(b_tok & d_tok) >= max(1, len(b_tok) // 3)

    results = []
    for ob in obligations:
        ga = _gen(R.STRUCT_VERIFY_A.format(obligation=ob, diff=diff[:4000]),
                  tag="S6b-verifierA", temperature=0.2, num_predict=200)
        res = str(_j(ga.text).get("result", "NEEDS-HUMAN")).upper().replace("_", "-")
        status, note = "escalate", ""
        if res in ("VIOLATED", "NEEDS-EXECUTION"):
            gp = _gen(f"{R.VIOLATION_INPUT}\n{ob}" if res == "VIOLATED" else f"{R.PROBE_SYNTH}\n{ob}",
                      tag="S6b-probe", temperature=0.3, num_predict=260)
            pr = run_script(ws, "_probe.py", _strip_fences(gp.text))
            status = {0: "pass", 1: "fail"}.get(pr["exit"], "escalate")
            note = f"{res} probe: {pr['out'][:180]}"
        elif res == "SATISFIED":
            status = "pass" if b_consistent else "escalate"
            note = "A=SATISFIED" + ("" if b_consistent else f"; B wanted {b_edits[:2]}")
        else:
            note = "A=NEEDS-HUMAN"
        results.append({"obligation": ob, "a": res, "status": status, "note": note})
    led.append({"stage": "S6b-l2", "calls": len(_TX) - n0, "wall": round(time.monotonic() - t0, 1),
                "out": ",".join(r["status"] for r in results) + f" b_consistent={b_consistent}"})
    return {"results": results, "b_consistent": b_consistent}


# ----------------------------------------------------------------- reconcile

def reconcile(sig: dict) -> str:
    if sig["premise_unsound"]:
        return "declined"
    if sig["l1_provided_fail"] or sig["regression"] or sig["l2_violated"] or sig["synth_trusted_fail"]:
        return "needs-change"
    if sig["l2_needs_human"] or sig["blowout"] or sig["refactor_unverified"]:
        return "escalate"
    return "resolved"


def counterfactual(sig: dict, terminal: str) -> list[str]:
    load_bearing = []
    for k, v in sig.items():
        if not v:
            continue
        flipped = dict(sig)
        flipped[k] = False
        if reconcile(flipped) != terminal:
            load_bearing.append(k)
    return load_bearing


# ----------------------------------------------------------------- driver

def run_pipeline(task, rep, cmd, protected) -> dict:
    _TX.clear()
    ws = fresh_workspace(task["dir"])
    obj = task["objective"]
    rec = RunRecorder(RUNS, intent_text=obj, meta={"task": task["id"], "rep": rep, "suite": "superpipe2"})
    gate = Gate()
    root = rec.invocation(role="superpipe", model_identity={"name": "harness"},
                          intent_ref=task["id"], config_ref="superpipe2")
    led: list = []
    pristine = snapshot(ws)
    code_blob = "\n".join(f"--- {n} ---\n{b}" for n, b in pristine.items())
    base_oc = objective_check(ws, cmd)
    base_fails = fail_labels(base_oc["tail"])
    t0 = time.monotonic()

    sig = dict(premise_unsound=False, l1_provided_fail=False, regression=False,
               l2_violated=False, synth_trusted_fail=False, l2_needs_human=False,
               blowout=False, refactor_unverified=False)
    extra: dict = {}
    open_items: list = []

    prem = stage_premise(obj, code_blob, led)
    sig["premise_unsound"] = not prem["sound"]
    tt = prem["task_type"]

    tspec = ispec = align = synth = coding = l2 = None
    if not sig["premise_unsound"]:
        tspec = stage_test_spec(obj, led)
        ispec = stage_impl_spec2(obj, led)
        align = stage_alignment(tspec, ispec, led)
        behav = [x for t, x in tspec["items"] if t == "BEHAVIOURAL"]
        synth = stage_synth(obj, behav, pristine, ws, led)
        coding = stage_coding(task, ws, obj, ispec, cmd, protected, rec, gate, root, tt, led)

        fin = coding["final_oc"]
        sig["l1_provided_fail"] = not fin["pass"]
        sig["blowout"] = coding["blowout"]
        new_fails = fail_labels(fin["tail"]) - base_fails
        sig["regression"] = bool(new_fails)
        stf, stf_detail = synth_verdict_on(ws, synth["suites"])
        sig["synth_trusted_fail"] = stf

        structural = [x for t, x in tspec["items"] if t == "STRUCTURAL"]
        structural += list(align["unverified"])
        if ispec["disagree"]:
            structural.append(f"[spec-disagreement] two blind impl-specs diverged on: {obj[:80]}")
        if tt == "refactor" or not behav:
            structural.append("The change preserves all externally observable behaviour (refactor).")
        l2 = stage_l2(obj, structural, pristine, ws, tt, led) if structural else {"results": []}
        sig["l2_violated"] = any(r["status"] == "fail" for r in l2["results"])
        sig["l2_needs_human"] = any(r["status"] == "escalate" for r in l2["results"])
        sig["refactor_unverified"] = (tt == "refactor" and not sig["l2_violated"]
                                      and any(r["status"] != "pass" for r in l2["results"]))
        extra = {"task_type": tt, "winner": coding["winner"], "impl_agree": coding["impl_agree"],
                 "synth_detail": stf_detail, "new_fails": sorted(new_fails),
                 "align_unverified": align["unverified"], "spec_disagree": ispec["disagree"]}
        open_items = [f"{r['obligation']}  [check: {r['note']}]"
                      for r in l2["results"] if r["status"] == "escalate"]

    terminal = reconcile(sig)
    load_bearing = counterfactual(sig, terminal)
    if sig["premise_unsound"]:
        extra = {"reason": prem["reason"], "correct_action": prem["correct_action"], "task_type": tt}

    restore_protected(ws, task["dir"], protected)
    fin_oc = objective_check(ws, cmd)
    rec.close("completed")
    wall = round(time.monotonic() - t0, 1)
    total_calls = sum(s["calls"] for s in led)

    TX_DIR.mkdir(parents=True, exist_ok=True)
    md = [f"# {task['id']} rep{rep} -> {terminal}",
          f"_baseline {base_oc['sub']} -> final {fin_oc['sub']}, {total_calls} calls, {wall}s_",
          f"\nsignals: {json.dumps(sig)}",
          f"load-bearing: {load_bearing}",
          f"open_items: {json.dumps(open_items, indent=1)}",
          f"\nOBJECTIVE: {obj}\n\n## ledger\n"]
    for s in led:
        md.append(f"- **{s['stage']}** ({s['calls']}c {s['wall']}s): {s['out']}")
    md.append("\n## transcripts\n")
    for t in _TX:
        md += [f"\n### {t['tag']}", "```", t["prompt"][:700], "```", "->", "```", t["raw"][:1500], "```"]
    (TX_DIR / f"{task['id']}_rep{rep}.md").write_text("\n".join(md), encoding="utf-8")

    shutil.rmtree(ws, ignore_errors=True)
    return {
        "task": task["id"], "kind": task["kind"], "rep": rep, "run_id": rec.run_id,
        "terminal": terminal, "load_bearing": load_bearing, "open_items": open_items,
        "baseline_sub": base_oc["sub"][0], "final_sub": fin_oc["sub"][0], "sub_tot": fin_oc["sub"][1],
        "objective_pass": fin_oc["pass"], "regressed": fin_oc["sub"][0] < base_oc["sub"][0],
        "decline_expected": bool(task["expect"].get("decline_correct")),
        "doc": fin_oc["doc"], "todo": fin_oc["todo"],
        "total_calls": total_calls, "wall_s": wall, "signals": sig, "ledger": led, **extra,
    }


def summarise(rows) -> str:
    L = ["# Super-pipeline v2 results", "", f"_{time.strftime('%Y-%m-%d %H:%M')} - {len(rows)} runs_", "",
         "| task | rep | terminal | base | final | pass | regr | decline_exp | calls | wall | load-bearing |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["task"], r["rep"])):
        L.append(f"| {r['task']} | {r['rep']} | {r['terminal']} | {r['baseline_sub']} | "
                 f"{r['final_sub']}/{r['sub_tot']} | {r['objective_pass']} | {r['regressed']} | "
                 f"{r['decline_expected']} | {r['total_calls']} | {r['wall_s']} | "
                 f"{','.join(r['load_bearing'])} |")
    wf6 = [r for r in rows if r["task"] == "wf6_multi"]
    if wf6:
        L += ["", "### wf6_multi detail", "| rep | terminal | algo | doc | todo | winner | calls |",
              "|---|---|---|---|---|---|---|"]
        for r in wf6:
            L.append(f"| {r['rep']} | {r['terminal']} | {r['final_sub']}/{r['sub_tot']} | "
                     f"{r.get('doc')} | {r.get('todo')} | {r.get('winner','-')} | {r['total_calls']} |")
    L += ["", "## per-stage cost (mean)", "", "| stage | calls | wall | runs |", "|---|---|---|---|"]
    agg: dict = {}
    for r in rows:
        for s in r["ledger"]:
            a = agg.setdefault(s["stage"], [0, 0.0, 0])
            a[0] += s["calls"]; a[1] += s["wall"]; a[2] += 1
    for st, (c, w, n) in agg.items():
        L.append(f"| {st} | {c/n:.1f} | {w/n:.1f}s | {n} |")
    L += ["", "## terminals", ""]
    for k, v in Counter(r["terminal"] for r in rows).most_common():
        L.append(f"- {k}: {v}")
    L.append(f"\n**regressions: {sum(r['regressed'] for r in rows)}/{len(rows)}**")
    L += ["", "## stage load-bearing frequency (how often each signal decided the terminal)", ""]
    lb = Counter(s for r in rows for s in r["load_bearing"])
    for k, v in lb.most_common():
        L.append(f"- {k}: {v}")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", nargs="+")
    ap.add_argument("--reps", type=int, default=1)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    if not health():
        print("Ollama not reachable", file=sys.stderr)
        raise SystemExit(2)
    RESULTS.mkdir(parents=True, exist_ok=True)
    tasks, cmd, protected = load_tasks()
    if args.tasks:
        tasks = [t for t in tasks if t["id"] in args.tasks]
    if args.smoke:
        tasks, args.reps = tasks[:1], 1
    rows, t0 = [], time.monotonic()
    total = len(tasks) * args.reps
    i = 0
    for task in tasks:
        for rep in range(1, args.reps + 1):
            i += 1
            print(f"[{i}/{total}] {task['id']} rep {rep} ...", flush=True)
            row = run_pipeline(task, rep, cmd, protected)
            rows.append(row)
            print(f"      -> {row['terminal']} base={row['baseline_sub']} "
                  f"final={row['final_sub']}/{row['sub_tot']} regr={row['regressed']} "
                  f"calls={row['total_calls']} wall={row['wall_s']}s lb={row['load_bearing']}", flush=True)
            (RESULTS / "results.json").write_text(json.dumps(rows, indent=2, default=str), encoding="utf-8")
            (RESULTS / "summary.md").write_text(summarise(rows), encoding="utf-8")
    print(f"\n{(time.monotonic()-t0)/60:.1f} min\n\n{summarise(rows)}")


if __name__ == "__main__":
    main()
