"""M7 - the static supervised workflow.

Specification: docs/10-technical/11-static-workflow.md

Four stages in fixed order; two always fire, two fire on condition.

  1. premise audit    always fires, ADVISORY ONLY - may never produce a terminal
  2. concern split    fires on condition
  3. implement        always fires
  4. test gate/keeper always fires - incumbent-protected, escalate on stall

Terminals are the processor contract's three: answered | declined | blocked.
Only the test gate and the escalation rule produce one; no model call does.

Built from the `dloop` core in M6's m6_arms.py, which is where the spine and the
keeper were measured. What is new here is stage 1 made advisory, stage 2 made
conditional, and the per-stage influence record that lets a stage be retired.
"""
from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
M6 = HERE.parent / "M6-evaluation-suite"
sys.path.insert(0, str(M6))
from _m6bridge import Gate, RunRecorder, assemble, generate, run_processor  # noqa: E402

RUNS = HERE / "runs"
STAGE_LOG = HERE / "stage_influence.jsonl"
CMD = ["python", "test_task.py"]

# v0 values, from M6's observed 1-4 call range. Neither is derived from anything;
# both are recorded per run so the suite can move them.
STALL_N = 2
PASS_BUDGET = 4          # model calls per implementation pass
TASK_CALL_CAP = 12       # stops a many-concern split from running away

_SCORE = re.compile(r"^([A-Z]+SCORE|SUBTESTS)\s+(\d+)\s*/\s*(\d+)", re.M)
_FAIL = re.compile(r"^\s{2,}([^\n]{2,120})$", re.M)
_JSON = re.compile(r"\{.*\}", re.S)
_SEG = re.compile(r"(?=\(\d\))")


# --------------------------------------------------------------- workspace

def _py_files(ws: Path):
    return [p for p in ws.glob("*.py") if p.name != "test_task.py"]


def _snap(ws: Path) -> dict:
    return {p.name: p.read_text(encoding="utf-8", errors="replace") for p in _py_files(ws)}


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
    """The objective check. The only thing in this workflow that produces a terminal."""
    try:
        cp = subprocess.run(CMD, cwd=str(ws), capture_output=True, text=True, timeout=30)
        out = (cp.stdout + cp.stderr).strip()
    except subprocess.TimeoutExpired:
        return {"sub": (0, 1), "comb": 0, "tot": 1, "full": False, "fails": "",
                "py": _py_ok(ws), "dims": 0}
    sc = {m.group(1): (int(m.group(2)), int(m.group(3))) for m in _SCORE.finditer(out)}
    sub = sc.get("SUBTESTS", (0, 1))
    return {
        "sub": sub,
        "comb": sum(p for p, _ in sc.values()),
        "tot": sum(t for _, t in sc.values()) or 1,
        "full": bool(sc) and all(p == t for p, t in sc.values()),
        "fails": "\n".join(_FAIL.findall(out)[:12]),
        "py": _py_ok(ws),
        "dims": len(sc),                      # how many dimensions the check reports
    }


# --------------------------------------------------------------- stage 1

AUDIT = (
    "You are a senior engineer reading a task before any code is written. You do NOT "
    "decide whether the task should be attempted - something else decides that. Your "
    "output is advice.\n\n"
    "Report three things:\n"
    '  "classification": one of "bugfix", "feature", "refactor", "perf"\n'
    '  "multi_concern": true if the objective asks for several independent changes '
    "that could be worked one at a time, false otherwise\n"
    '  "concern": one sentence naming anything that looks wrong about the premise, or '
    '"" if nothing does. This is read by a human, never by the engineer doing the work.\n\n'
    "Answer with ONE JSON object and nothing else.\n\n"
    "OBJECTIVE:\n{obj}\n\nCODE:\n{code}")

_VALID_CLASS = {"bugfix", "feature", "refactor", "perf"}


def premise_audit(objective: str, ws: Path) -> dict:
    """Stage 1. Always fires. ADVISORY - it has no way to produce a terminal.

    One call, not the K=3 majority `staged` used. The vote existed to make a
    *gate* safer, because a wrong decline was terminal. Advice needs no quorum,
    and dropping it returns two calls per task to the implementation budget.
    """
    code = "\n".join(f"--- {p.name} ---\n{p.read_text(errors='replace')}"
                     for p in _py_files(ws))
    t0 = time.monotonic()
    out = {"classification": None, "multi_concern": None, "concern": "", "parsed": False}
    try:
        g = generate(AUDIT.replace("{obj}", objective).replace("{code}", code[:4000]),
                     temperature=0.3, num_predict=200)
        m = _JSON.search(g.text)
        if m:
            d = json.loads(m.group(0))
            c = str(d.get("classification", "")).strip().lower()
            out["classification"] = c if c in _VALID_CLASS else None
            out["multi_concern"] = bool(d.get("multi_concern", False))
            out["concern"] = str(d.get("concern", ""))[:300]
            out["parsed"] = True
    except Exception as e:  # noqa: BLE001
        out["error"] = repr(e)[:120]
    out["calls"] = 1
    out["wall_s"] = round(time.monotonic() - t0, 1)
    return out


# --------------------------------------------------------------- stage 2

def concern_split(objective: str, audit: dict) -> dict:
    """Stage 2. Fires on condition.

    The firing rule is the open part of the specification. v0 records BOTH candidate
    signals and fires on either, so the rule can be moved later against the suite's
    `stresses` slice without re-running to collect the inputs:

      - `syntactic`: the objective enumerates its parts, "(1) ... (2) ...";
      - `model`: the premise audit called it multi-concern.

    22-arch-cognition/08 argues both are the wrong shape - the split should compare
    demand against what the assembly can hold, not classify the task. Neither signal
    does that, and the decision is recorded rather than defended.
    """
    segs = [s.strip() for s in _SEG.split(objective) if re.match(r"\(\d\)", s.strip())]
    syntactic = len(segs) >= 2
    model = bool(audit.get("multi_concern"))
    fired = syntactic or model
    return {
        "fired": fired,
        "signal_syntactic": syntactic,
        "signal_model": model,
        "agreed": syntactic == model,
        "n_segments": len(segs) if syntactic else 1,
        "segments": segs if (fired and syntactic) else None,
    }


# --------------------------------------------------------------- stages 3 + 4

def _implement(objective: str, ws: Path, rec, root):
    """Stage 3. One implementer instance per attempt.

    No plan is injected. What the loop hands forward is the failing check's own
    output, folded into the objective - a signal, not a model's account of one.
    The audit's `concern` never reaches here; it goes to the escalation payload.
    """
    b = assemble(objective, ws, token_budget=8000)
    return run_processor(role="implementer", objective=objective, context=b,
                         workspace_root=ws, recorder=rec, gate=Gate(),
                         parent_invocation_id=root, intent_ref="m7",
                         interaction_mode="oneshot")


def _pass(target: str, ws: Path, rec, root, best: dict, calls: list,
          greenfield: bool) -> dict:
    """Stage 4 around stage 3: the test-gated loop with an incumbent-protected keeper.

    A new attempt replaces the incumbent only on a strict improvement that does not
    regress subtests. A tie keeps the incumbent. This is the rule that produces zero
    regressions and it is the one to preserve if any other is traded away.

    `greenfield` implements M6's third fix: elaborate framing helps only where there
    is pre-existing code to respect. So the first attempt at a greenfield target gets
    the bare objective and no failure preamble - a check reporting 0/N against code
    that does not exist yet says nothing an implementer can act on. Later attempts
    get the hint either way, because by then there is a prior state and the signal is
    about code that now exists.
    """
    stall = 0
    for rnd in range(PASS_BUDGET):
        if calls[0] >= TASK_CALL_CAP:
            break
        if best["s"]["full"] and best["n_targets"] == 1:
            break
        _restore(ws, best["snap"])
        step = target
        plain = greenfield and rnd == 0 and best["src"] == "incumbent"
        if not plain:
            hint = best["s"]["fails"]
            if hint:
                step = (f"{target}\n\nCurrent state still fails:\n{hint}\n"
                        "Output the whole corrected file(s).")
        _implement(step, ws, rec, root)
        calls[0] += 1
        s = _score(ws)
        improved = (s["sub"][0] >= best["s"]["sub"][0]
                    and s["comb"] > best["s"]["comb"]
                    and s["py"])
        if improved:
            best = {**best, "s": s, "snap": _snap(ws), "src": f"r{rnd}"}
            stall = 0
        else:
            stall += 1
            if stall > STALL_N:
                break
    return best


def _escalation_payload(objective: str, audit: dict, split: dict, attempts: list,
                        fin: dict) -> dict:
    """Bound by 10-foundations/07: ask what only the operator can answer.

    A precise question, not a dump. Carries the audit's concern whether or not
    anything consumed it - which is the point of recording consumption separately.
    """
    unmet = fin["fails"] or "the check reports no failing detail"
    return {
        "objective": objective,
        "attempts": attempts,
        "premise_concern": audit.get("concern", ""),
        "split_taken_on_your_behalf": {
            "fired": split["fired"],
            "into": split["n_segments"],
            "on_signal": ([s for s, on in (("the objective enumerates its parts",
                                            split["signal_syntactic"]),
                                           ("the premise audit called it multi-concern",
                                            split["signal_model"])) if on]
                          or ["neither signal fired"]),
        },
        "question": (
            "The check still reports a shortfall this loop could not close: "
            f"{unmet[:300]}. Is the remaining gap something the objective actually "
            "asks for, or is the check measuring something the objective did not "
            "request?"),
        "reasoning_that_would_overturn": (
            "The loop kept the incumbent because no attempt strictly improved the "
            "check without regressing a subtest. If the check does not measure the "
            "thing the objective asked for, that keeper rule is the wrong rule here "
            "and the work should be judged on the artifact instead."),
    }


# --------------------------------------------------------------- the arm

def run_m7(objective: str, ws: Path) -> str:
    rec = RunRecorder(RUNS, intent_text=objective, meta={"arm": "m7", "suite": "m6"})
    root = rec.invocation(role="m7-workflow", model_identity={"name": "harness"},
                          intent_ref="m7", config_ref="m7")
    t0 = time.monotonic()
    stage = {"task_objective": objective[:200],
             "task": os.environ.get("M6_TASK"),
             "rep": os.environ.get("M6_REP")}
    try:
        # ---- stage 1: always fires, advisory
        audit = premise_audit(objective, ws)
        stage["s1_premise_audit"] = {**audit, "fired": True, "advisory": True}

        # ---- stage 2: fires on condition
        split = concern_split(objective, audit)
        stage["s2_concern_split"] = split

        targets = split["segments"] if (split["fired"] and split["segments"]) else [objective]

        # ---- stages 3 + 4
        incbase = _score(ws)
        greenfield = not _py_files(ws)
        best = {"s": incbase, "snap": _snap(ws), "src": "incumbent",
                "n_targets": len(targets)}
        calls = [audit["calls"]]
        attempts = []
        for t in targets:
            before = best["s"]["comb"]
            best = _pass(t, ws, rec, root, best, calls, greenfield)
            attempts.append({"target": t[:120], "comb_before": before,
                             "comb_after": best["s"]["comb"]})
        _restore(ws, best["snap"])
        fin = _score(ws)

        # ---- terminal. Only the gate and the escalation rule produce one.
        if best["src"] == "incumbent":
            terminal = "declined" if fin["full"] else "blocked"
        else:
            terminal = "answered" if fin["full"] else "blocked"

        payload = None
        if terminal == "blocked":
            payload = _escalation_payload(objective, audit, split, attempts, fin)

        # ---- stage influence: what each stage produced, and who consumed it.
        # The third field is the one that is easy to omit and the one that makes
        # retirement possible.
        stage["influence"] = {
            "s1_classification_consumed_by": (
                ["s2_firing_rule"] if split["signal_model"] else []),
            "s1_concern_consumed_by": (["escalation_payload"] if payload else []),
            "s1_concern_nonempty": bool(audit.get("concern")),
            "s2_consumed_by": (["s3_targets"] if split["fired"] and split["segments"]
                               else []),
        }
        stage.update({"terminal": terminal, "calls": calls[0],
                      "wall_s": round(time.monotonic() - t0, 1),
                      "baseline_comb": incbase["comb"], "final_comb": fin["comb"],
                      "check_dims": fin["dims"], "escalation_payload": payload})
        return terminal
    finally:
        STAGE_LOG.parent.mkdir(parents=True, exist_ok=True)
        with STAGE_LOG.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(stage) + "\n")
        rec.close("completed")


ARMS_EXTRA = {"m7": run_m7}
