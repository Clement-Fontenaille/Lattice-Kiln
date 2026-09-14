"""M7c - m7b plus an independent judge, measured and given no authority.

R1..R5 as m7b, plus the judge below. See PREDICTION-M7C.md.

Original m7b header follows.

M7b - the static supervised workflow, variant 2.

R1..R5 from INVENTORY.md. Differences from `m7` are marked R1..R5 inline.
Prediction recorded in PREDICTION-M7B.md before the run.

Original header follows.

M7 - the static supervised workflow.

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
import re
import difflib
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
M6 = HERE.parent / "M6-evaluation-suite"
sys.path.insert(0, str(M6))
from _m6bridge import Gate, RunRecorder, assemble, generate, run_processor  # noqa: E402

RUNS = HERE / "runs_m7c"
STAGE_LOG = HERE / "stage_influence_m7c.jsonl"
CMD = ["python", "test_task.py"]

# v0 values, from M6's observed 1-4 call range. Neither is derived from anything;
# both are recorded per run so the suite can move them.
STALL_N = 2
PASS_BUDGET = 4          # model calls per implementation pass
TASK_CALL_CAP = 12       # stops a many-concern split from running away
# R2: a call cap did not bound the worst case -- one task took 43% of the arm's wall
# clock inside its cap. Wall time is what the operator actually pays, so bound that
# too. Set WIDE deliberately: the median task is 10s and the worst observed is 356s,
# so 600 fires on nothing seen so far. That keeps R2 a safety net rather than a
# behaviour change, leaving R1 as the only remediation here able to move a number
# -- which is what makes the result attributable.
TASK_WALL_CAP_S = 600

_SCORE = re.compile(r"^([A-Z]+SCORE|SUBTESTS)\s+(\d+)\s*/\s*(\d+)", re.M)
_FAIL = re.compile(r"^\s{2,}([^\n]{2,120})$", re.M)

# R1: the keeper must see the SET of failing checks, not how many there are.
#
# Two traps, both of which the harness own extractor falls into and this one must
# not. Its pattern excludes only the colon, and that class also matches a newline,
# so a label can run across lines and land on the wrong text; and a failure line
# with no colon yields no label at all, which is most of them. Under that extractor
# a regression is visible only on checks whose failure text happens to contain a
# colon.
#
# Here: one label per line, the text before the first colon, or the whole line when
# there is none. Splitting on the colon keeps a label stable when only the reported
# values move (an "input: got 3 want 5" line).
_FAILLINE = re.compile(r"^[ \t]{2,}(\S[^\n]{0,119})$", re.M)


def _labels(out: str) -> frozenset:
    return frozenset(ln.split(":", 1)[0].strip() for ln in _FAILLINE.findall(out))
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
                "failset": frozenset({"TIMEOUT"}), "py": _py_ok(ws), "dims": 0}
    sc = {m.group(1): (int(m.group(2)), int(m.group(3))) for m in _SCORE.finditer(out)}
    sub = sc.get("SUBTESTS", (0, 1))
    return {
        "sub": sub,
        "comb": sum(p for p, _ in sc.values()),
        "tot": sum(t for _, t in sc.values()) or 1,
        "full": bool(sc) and all(p == t for p, t in sc.values()),
        "fails": "\n".join(_FAIL.findall(out)[:12]),
        "failset": _labels(out),              # R1
        "py": _py_ok(ws),
        "dims": len(sc),                      # how many dimensions the check reports
    }


# --------------------------------------------------------------- stage 1

AUDIT = (
    "You are a senior engineer reading a task before any code is written. You do NOT "
    "decide whether the task should be attempted - something else decides that. Your "
    "output is advice.\n\n"
    "Report two things:\n"
    '  "segments": the independent changes the objective asks for, as a list, each '
    "written as a standalone instruction, in the order the objective gives them. "
    "Use a one-element list when the objective asks for a single thing.\n"
    '  "concern": one sentence naming anything that looks wrong about the premise, '
    'or "" if nothing does. Read by a human, never by the engineer doing the work.\n\n'
    "Answer with ONE JSON object and nothing else.\n\n"
    "OBJECTIVE:\n{obj}\n\nCODE:\n{code}")

# R5: `classification` is gone from the prompt as well as from the record. Thirty
# were produced across the m7 run and nothing consumed one.



def premise_audit(objective: str, ws: Path) -> dict:
    """Stage 1. Always fires. ADVISORY - it has no way to produce a terminal.

    One call, not the K=3 majority `staged` used. The vote existed to make a
    *gate* safer, because a wrong decline was terminal. Advice needs no quorum,
    and dropping it returns two calls per task to the implementation budget.
    """
    code = "\n".join(f"--- {p.name} ---\n{p.read_text(errors='replace')}"
                     for p in _py_files(ws))
    t0 = time.monotonic()
    out = {"segments": None, "concern": "", "parsed": False}
    try:
        g = generate(AUDIT.replace("{obj}", objective).replace("{code}", code[:4000]),
                     temperature=0.3, num_predict=200)
        m = _JSON.search(g.text)
        if m:
            d = json.loads(m.group(0))
            segs = d.get("segments")
            if isinstance(segs, list):
                segs = [str(x).strip()[:400] for x in segs if str(x).strip()]
                out["segments"] = segs or None
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

    R4: in `m7` the firing signal and the splitting mechanism were decoupled -- it
    fired on a syntactic marker OR the model's boolean, while segmentation was
    syntactic only. When the model fired alone the stage fired and had nothing to
    split, which made the influence record say a stage fired when nothing happened.

    Here the audit returns the segments themselves, so the model signal can act. The
    syntactic reading is kept as a fallback and as a cross-check: disagreement between
    the two is recorded, since that is the data a better firing rule would be learned
    from (22-arch-cognition/08 argues both are the wrong shape, and neither compares
    demand against what the assembly can hold).
    """
    syn = [s.strip() for s in _SEG.split(objective) if re.match(r"\(\d\)", s.strip())]
    syntactic = len(syn) >= 2
    model_segs = audit.get("segments") or []
    model = len(model_segs) >= 2

    segments = model_segs if model else (syn if syntactic else None)
    return {
        "fired": bool(segments),
        "source": "model" if model else ("syntactic" if syntactic else None),
        "signal_syntactic": syntactic,
        "signal_model": model,
        "agreed": syntactic == model,
        "n_segments": len(segments) if segments else 1,
        "segments": segments,
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
          greenfield: bool, deadline: float) -> dict:
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
        if time.monotonic() > deadline:          # R2
            best["over_budget"] = True
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
        # R1: strict improvement AND no check that was passing has begun to fail.
        # The count rule (sub[0] >= best sub[0]) accepts a candidate that fixes three
        # and breaks one; the set rule does not. findings-log entry 10.
        broke = s["failset"] - best["s"]["failset"]
        improved = (not broke
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


# --------------------------------------------------------------- the judge

JUDGE = """You are reviewing a change somebody else made. You did not write it and
you have not seen their reasoning.

You are given three things: the request as it was made, a note from an earlier reader
about whether the request itself looked sound, and the change as a diff.

You are NOT given any test result. Judge from the request and the diff alone.

Answer with ONE JSON object and nothing else:
  "verdict": one of "met", "not_met", "unsound_request"
      met             - the change does what the request asked
      not_met         - the request was reasonable and the change does not do it,
                        including when the diff is empty or merely cosmetic
      unsound_request - the request should not be carried out as stated
  "why": one sentence, citing something you can point at in the diff

REQUEST:
{obj}

EARLIER READER'S NOTE:
{concern}

DIFF:
{diff}"""

_VERDICTS = {"met", "not_met", "unsound_request"}


def _diff(before: dict, after: dict) -> str:
    """Unified diff of the .py files, before against after.

    This is the whole of what the judge sees of the work. Deliberately absent: the
    implementer's output text, the retry hints the loop folded into objectives, the
    check's output, and the incumbent/candidate churn.

    That absence is the independence being tested. `50-findings/07` measured a panel
    that shared the work's context and made a deterministic gate worse -- 9/10 alone,
    6/10 with the panel added. The hypothesis here is that sharing the context was the
    variable rather than the judging.

    Note what this is NOT: substrate isolation. Every call in this harness is already
    its own sequence, so no prefix is carried. What is isolated is the content of the
    prompt (`14-context-manager.md`, The isolation preference).
    """
    out = []
    for name in sorted(set(before) | set(after)):
        a = before.get(name, "").splitlines(keepends=True)
        b = after.get(name, "").splitlines(keepends=True)
        if a == b:
            continue
        out.extend(difflib.unified_diff(a, b, fromfile=name, tofile=name, n=3))
    d = "".join(out)
    return d[:6000] if d else "(no change to any .py file)"


def judge_change(objective: str, concern: str, before: dict, after: dict) -> dict:
    """Records a verdict. Changes nothing.

    The judge has NO authority here, and that is the experiment rather than a
    limitation. `11-static-workflow.md` forbids a lone model probe flipping a terminal
    state, and wiring this one in before measuring it would rebuild `staged`. So the
    verdict is scored against the check afterwards, and the arm behaves identically
    with the judge and without it.
    """
    t0 = time.monotonic()
    diff = _diff(before, after)
    out = {"verdict": None, "why": "", "parsed": False, "authority": "none",
           "diff_bytes": len(diff), "diff_empty": diff.startswith("(no change")}
    try:
        prompt = (JUDGE.replace("{obj}", objective)
                       .replace("{concern}", concern or "(nothing flagged)")
                       .replace("{diff}", diff))
        g = generate(prompt, temperature=0.2, num_predict=220)
        m = _JSON.search(g.text)
        if m:
            d = json.loads(m.group(0))
            v = str(d.get("verdict", "")).strip().lower()
            out["verdict"] = v if v in _VERDICTS else None
            out["why"] = str(d.get("why", ""))[:300]
            out["parsed"] = out["verdict"] is not None
    except Exception as e:  # noqa: BLE001
        out["error"] = repr(e)[:120]
    out["calls"] = 1
    out["wall_s"] = round(time.monotonic() - t0, 1)
    return out


# --------------------------------------------------------------- the arm

def run_m7(objective: str, ws: Path) -> str:
    rec = RunRecorder(RUNS, intent_text=objective, meta={"arm": "m7c", "suite": "m6"})
    root = rec.invocation(role="m7c-workflow", model_identity={"name": "harness"},
                          intent_ref="m7", config_ref="m7")
    t0 = time.monotonic()
    stage = {"task_objective": objective[:200]}
    try:
        # ---- stage 1: always fires, advisory
        audit = premise_audit(objective, ws)
        stage["s1_premise_audit"] = {**audit, "fired": True, "advisory": True}
        stage["variant"] = ("m7c: m7b (R1 set-keeper, R2 wall governor, R3 blocked split, "
                            "R4 model segments, R5 classification retired) + an independent judge with no authority")

        # ---- stage 2: fires on condition
        split = concern_split(objective, audit)
        stage["s2_concern_split"] = split

        targets = split["segments"] if (split["fired"] and split["segments"]) else [objective]

        # ---- stages 3 + 4
        incbase = _score(ws)
        pristine = _snap(ws)          # the judge's "before", taken before any call
        greenfield = not _py_files(ws)
        best = {"s": incbase, "snap": _snap(ws), "src": "incumbent",
                "n_targets": len(targets)}
        calls = [audit["calls"]]
        deadline = t0 + TASK_WALL_CAP_S          # R2
        attempts = []
        for t in targets:
            before = best["s"]["comb"]
            best = _pass(t, ws, rec, root, best, calls, greenfield, deadline)
            attempts.append({"target": t[:120], "comb_before": before,
                             "comb_after": best["s"]["comb"]})
        _restore(ws, best["snap"])
        fin = _score(ws)

        # The judge. It sees the request, the audit's note and the diff -- and no
        # check output, no implementer text, no retry hint. Its verdict is recorded
        # and scored afterwards; nothing below reads it.
        verdict = judge_change(objective, audit.get("concern", ""), pristine, _snap(ws))
        calls[0] += verdict["calls"]

        # ---- terminal. Only the gate and the escalation rule produce one.
        # R3: `blocked` carried two situations wanting opposite escalations -- five
        # tasks where nothing moved at all, three that progressed and stalled. One
        # terminal cannot ask both questions of the operator.
        if best["src"] == "incumbent":
            terminal = "declined" if fin["full"] else "blocked-no-progress"
        elif fin["full"]:
            terminal = "answered"
        else:
            terminal = "blocked-partial"

        payload = None
        if terminal.startswith("blocked"):
            payload = _escalation_payload(objective, audit, split, attempts, fin)

        # ---- stage influence: what each stage produced, and who consumed it.
        # The third field is the one that is easy to omit and the one that makes
        # retirement possible.
        stage["influence"] = {
            "s1_segments_consumed_by": (
                ["s3_targets"] if split["source"] == "model" else []),
            "s1_concern_consumed_by": (["escalation_payload"] if payload else []),
            "s1_concern_nonempty": bool(audit.get("concern")),
            "s2_consumed_by": (["s3_targets"] if split["fired"] and split["segments"]
                               else []),
        }
        stage["judge"] = verdict
        stage["influence"]["judge_consumed_by"] = []      # by construction: nothing
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


ARMS_EXTRA = {"m7c": run_m7}
