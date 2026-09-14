"""test-synth-retry - test-synth, with the witness allowed to fix its own file.

Operator: give it a second chance. The first run gave the witness ONE call and no
feedback, and 78 of its 93 execution failures read "no SYNTH line" -- the model wrote
a sensible test and printed its own format instead of the demanded one. That is
protocol non-compliance, the same failure entry 6 names, and it is the one class the
arm already repairs for its implementer.

THE RETRY FIRES ON EXECUTION FAILURE ONLY, never on the test being weak. Telling the
model its test passes on broken code says the test is wrong without saying why, and
the cheapest way to satisfy that is to tighten it arbitrarily -- teaching it to
satisfy the discriminator rather than to test the requirement. A traceback leaks
nothing about correctness.

So execution should rise and discrimination should NOT move. If discrimination moves,
something leaked and the measurement is spoiled rather than improved.

Original test-synth header follows.

test-synth - keeper-strict, with the model asked to WRITE a witness rather than
judge one.

Operator question: can a 7B write a mechanical check more reliable than it can judge?
It is the counterpart to the result that a witness beats a judge wherever a witness
is writable, and it asks whether the model can supply the witness itself.

One property makes this different in kind: **the test is executed.** Misreading the
code stops mattering; what matters is whether the requirement can be expressed as
running code. A malformed witness fails loudly rather than returning a confident
wrong verdict, which is the worst mode a judge has.

The synthesised file has no authority and never touches the real workspace.

Original keeper-strict header follows.

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
import os
import re
import shutil
import tempfile
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
M6 = HERE.parent / "M6-evaluation-suite"
sys.path.insert(0, str(M6))
from _m6bridge import Gate, RunRecorder, assemble, generate, run_processor  # noqa: E402

RUNS = HERE / "runs_test_synth_retry"
STAGE_LOG = HERE / "stage_influence_test_synth_retry.jsonl"
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
SYNTH_TRIES = 3          # one first attempt plus two corrections

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
        rc = cp.returncode
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


# --------------------------------------------------------------- the synthesised check

SYNTH = """Write a Python test file that checks whether a request has been carried out.

You are given the request and the code as it stands BEFORE any work. Write the test
against the request, not against the current code -- the current code does NOT satisfy
the request, and your test must FAIL on it.

Rules, all of them load-bearing:
  - one file, plain Python, no pytest, no imports beyond the standard library
  - import what you need from the module named in the request
  - print exactly one line "SYNTH n/m" with the number of checks that passed
  - then sys.exit(0) if all passed, else sys.exit(1)
  - wrap each check so one exception does not stop the rest
  - check the SPECIFIC behaviours the request names: values, edge cases, error types.
    A test that only imports the module, or only checks that a name exists, passes on
    code that does nothing and is worthless.

Emit ONLY the file content, no fence, no commentary.

REQUEST:
{obj}

CODE AS IT STANDS (does not satisfy the request):
{code}"""

REVIEW = """Here is your test file, and what happened when it was run against the
code as it stands -- the code that does NOT satisfy the request.

WHAT IT PRINTED:
{out}
(exit code {rc})

You now choose, and nothing here is a judgement of your file.

  Emit the whole corrected file, if you want to change it.
  Or emit exactly VALIDATE on its own line, and nothing else, if you are content.

REQUEST:
{obj}

YOUR FILE:
{src}"""


def _run_check(ws: Path, name: str) -> dict:
    try:
        cp = subprocess.run(["python", name], cwd=str(ws), capture_output=True,
                            text=True, timeout=30)
        out = (cp.stdout + cp.stderr).strip()
        rc = cp.returncode
    except subprocess.TimeoutExpired:
        return {"ran": False, "passed": None, "why": "timed out", "out": "(timed out after 30s)", "rc": -1}
    m = re.search(r"^SYNTH\s+(\d+)\s*/\s*(\d+)", out, re.M)
    if not m:
        why = ("it ran but printed no SYNTH line" if out else "it printed nothing")
        return {"ran": False, "passed": None, "why": why, "out": out[-900:], "rc": rc}
    p, tot = int(m.group(1)), int(m.group(2))
    return {"ran": True, "passed": p == tot and tot > 0, "score": [p, tot],
            "out": out[-900:], "rc": rc}


def synthesise_check(objective: str, pristine: dict, final: dict,
                     tries: int = SYNTH_TRIES) -> dict:
    """Ask the model for an executable witness, with a bounded retry on execution.

    **The retry fires on execution failure only, never on the test being weak.**

    That line is the experiment. Telling the model *your test passes on the broken
    code* says its test is wrong without saying why, and the cheapest way to satisfy
    that is to tighten the test arbitrarily until it fails -- which teaches it to
    satisfy the discriminator rather than to test the requirement. Handing back a
    traceback leaks nothing about correctness.

    So the two rates stay separable. **Execution should rise with retries and
    discrimination should not move.** If discrimination moves, something leaked and the
    measurement is spoiled rather than improved.

    The first run without a retry loop produced 88% parsing, 38% running, and 58% of
    those discriminating -- 20% usable end to end, with 78 of 93 execution failures
    reading `no SYNTH line`. That is protocol non-compliance rather than incapacity,
    and it is the one failure class the arm already repairs for its implementer while
    giving the witness a single call and no feedback.
    """
    t0 = time.monotonic()
    out = {"written": False, "discriminates": None, "verdict": None, "rounds": 0,
           "validated": False, "on_pristine": None, "on_final": None, "calls": 0,
           "authority": "none", "history": []}
    code = "\n".join(f"--- {n} ---\n{c}" for n, c in sorted(pristine.items()))
    src = None
    tmp = Path(tempfile.mkdtemp(prefix="synth_"))
    try:
        for rnd in range(tries):
            out["rounds"] = rnd + 1
            if src is None:
                prompt = (SYNTH.replace("{obj}", objective)
                               .replace("{code}", code[:4000]))
            else:
                pr = out["on_pristine"] or {}
                prompt = (REVIEW.replace("{obj}", objective)
                                .replace("{src}", src[:4000])
                                .replace("{out}", (pr.get("out") or "(nothing)")[:900])
                                .replace("{rc}", str(pr.get("rc", "?"))))
            g = generate(prompt, temperature=0.2, num_predict=900)
            out["calls"] += 1
            reply = g.text.strip()

            if src is not None and re.match(r"^VALIDATE"+chr(92)+"b", reply, re.I):
                out["validated"] = True
                break

            if reply.startswith("```"):
                reply = re.sub(r"^```[a-z]*\n|\n```$", "", reply)
            try:
                ast.parse(reply)
            except SyntaxError as e:
                out["history"].append(f"round {rnd}: does not parse: {e}")
                continue
            src, out["written"] = reply, True

            for f in list(tmp.glob("*.py")):
                f.unlink()
            for name, b in pristine.items():
                (tmp / name).write_text(b, encoding="utf-8")
            (tmp / "synth_check.py").write_text(src, encoding="utf-8")
            out["on_pristine"] = _run_check(tmp, "synth_check.py")
            out["history"].append(f"round {rnd}: {out[chr(39)+chr(39)] if False else out['on_pristine']['why'] if not out['on_pristine']['ran'] else 'ran, ' + str(out['on_pristine']['score'])}")

        pr = out["on_pristine"] or {}
        if pr.get("ran"):
            for f in list(tmp.glob("*.py")):
                if f.name != "synth_check.py":
                    f.unlink()
            for name, b in final.items():
                (tmp / name).write_text(b, encoding="utf-8")
            out["on_final"] = _run_check(tmp, "synth_check.py")
            out["discriminates"] = pr["passed"] is False
            if out["on_final"]["ran"]:
                out["verdict"] = "met" if out["on_final"]["passed"] else "not_met"
    except Exception as e:  # noqa: BLE001
        out["why"] = repr(e)[:140]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
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


# --------------------------------------------------------------- the synthesised check

SYNTH = """Write a Python test file that checks whether a request has been carried out.

You are given the request and the code as it stands BEFORE any work. Write the test
against the request, not against the current code -- the current code does NOT satisfy
the request, and your test must FAIL on it.

Rules, all of them load-bearing:
  - one file, plain Python, no pytest, no imports beyond the standard library
  - import what you need from the module named in the request
  - print exactly one line "SYNTH n/m" with the number of checks that passed
  - then sys.exit(0) if all passed, else sys.exit(1)
  - wrap each check so one exception does not stop the rest
  - check the SPECIFIC behaviours the request names: values, edge cases, error types.
    A test that only imports the module, or only checks that a name exists, passes on
    code that does nothing and is worthless.

Emit ONLY the file content, no fence, no commentary.

REQUEST:
{obj}

CODE AS IT STANDS (does not satisfy the request):
{code}"""

REVIEW = """Here is your test file, and what happened when it was run against the
code as it stands -- the code that does NOT satisfy the request.

WHAT IT PRINTED:
{out}
(exit code {rc})

You now choose, and nothing here is a judgement of your file.

  Emit the whole corrected file, if you want to change it.
  Or emit exactly VALIDATE on its own line, and nothing else, if you are content.

REQUEST:
{obj}

YOUR FILE:
{src}"""


def _run_check(ws: Path, name: str) -> dict:
    try:
        cp = subprocess.run(["python", name], cwd=str(ws), capture_output=True,
                            text=True, timeout=30)
        out = (cp.stdout + cp.stderr).strip()
        rc = cp.returncode
    except subprocess.TimeoutExpired:
        return {"ran": False, "passed": None, "why": "timed out", "out": "(timed out after 30s)", "rc": -1}
    m = re.search(r"^SYNTH\s+(\d+)\s*/\s*(\d+)", out, re.M)
    if not m:
        why = ("it ran but printed no SYNTH line" if out else "it printed nothing")
        return {"ran": False, "passed": None, "why": why, "out": out[-900:], "rc": rc}
    p, tot = int(m.group(1)), int(m.group(2))
    return {"ran": True, "passed": p == tot and tot > 0, "score": [p, tot],
            "out": out[-900:], "rc": rc}


def synthesise_check(objective: str, pristine: dict, final: dict,
                     tries: int = SYNTH_TRIES) -> dict:
    """Ask the model for an executable witness, with a bounded retry on execution.

    **The retry fires on execution failure only, never on the test being weak.**

    That line is the experiment. Telling the model *your test passes on the broken
    code* says its test is wrong without saying why, and the cheapest way to satisfy
    that is to tighten the test arbitrarily until it fails -- which teaches it to
    satisfy the discriminator rather than to test the requirement. Handing back a
    traceback leaks nothing about correctness.

    So the two rates stay separable. **Execution should rise with retries and
    discrimination should not move.** If discrimination moves, something leaked and the
    measurement is spoiled rather than improved.

    The first run without a retry loop produced 88% parsing, 38% running, and 58% of
    those discriminating -- 20% usable end to end, with 78 of 93 execution failures
    reading `no SYNTH line`. That is protocol non-compliance rather than incapacity,
    and it is the one failure class the arm already repairs for its implementer while
    giving the witness a single call and no feedback.
    """
    t0 = time.monotonic()
    out = {"written": False, "discriminates": None, "verdict": None, "tries": 0,
           "on_pristine": None, "on_final": None, "calls": 0, "authority": "none",
           "history": []}
    code = "\n".join(f"--- {n} ---\n{c}" for n, c in sorted(pristine.items()))
    src = None
    tmp = Path(tempfile.mkdtemp(prefix="synth_"))
    try:
        for attempt in range(tries):
            out["tries"] = attempt + 1
            if src is None:
                prompt = (SYNTH.replace("{obj}", objective)
                               .replace("{code}", code[:4000]))
            else:
                err = out["history"][-1]
                detail = err["why"] + (("\n\n" + err["out"]) if err.get("out") else "")
                prompt = (RETRY.replace("{error}", detail[:1200])
                               .replace("{src}", src[:4000]))
            g = generate(prompt, temperature=0.2, num_predict=900)
            out["calls"] += 1
            src = g.text.strip()
            if src.startswith("```"):
                src = re.sub(r"^```[a-z]*\n|\n```$", "", src)
            try:
                ast.parse(src)
                out["written"] = True
            except SyntaxError as e:
                out["history"].append({"why": f"it does not parse: {e}", "out": ""})
                continue

            for f in list(tmp.glob("*.py")):
                f.unlink()
            for name, body in pristine.items():
                (tmp / name).write_text(body, encoding="utf-8")
            (tmp / "synth_check.py").write_text(src, encoding="utf-8")
            pr = _run_check(tmp, "synth_check.py")
            out["on_pristine"] = pr
            if pr["ran"]:
                break
            out["history"].append({"why": pr["why"], "out": pr.get("out", "")})

        if out["on_pristine"] and out["on_pristine"]["ran"]:
            for f in list(tmp.glob("*.py")):
                if f.name != "synth_check.py":
                    f.unlink()
            for name, body in final.items():
                (tmp / name).write_text(body, encoding="utf-8")
            out["on_final"] = _run_check(tmp, "synth_check.py")
            out["discriminates"] = out["on_pristine"]["passed"] is False
            if out["on_final"]["ran"]:
                out["verdict"] = "met" if out["on_final"]["passed"] else "not_met"
    except Exception as e:  # noqa: BLE001
        out["why"] = repr(e)[:140]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    out["wall_s"] = round(time.monotonic() - t0, 1)
    return out


# --------------------------------------------------------------- the arm

def run_m7(objective: str, ws: Path) -> str:
    rec = RunRecorder(RUNS, intent_text=objective, meta={"arm": "test_synth_retry", "suite": "m6"})
    root = rec.invocation(role="test-synth-retry-workflow", model_identity={"name": "harness"},
                          intent_ref="m7", config_ref="m7")
    t0 = time.monotonic()
    stage = {"task_objective": objective[:200],
             "task": os.environ.get("M6_TASK"),
             "rep": os.environ.get("M6_REP")}
    try:
        # ---- stage 1: always fires, advisory
        audit = premise_audit(objective, ws)
        stage["s1_premise_audit"] = {**audit, "fired": True, "advisory": True}
        stage["variant"] = ("m7b: R1 set-keeper, R2 wall governor, R3 blocked split, "
                            "R4 model segments, R5 classification retired")

        # ---- stage 2: fires on condition
        split = concern_split(objective, audit)
        stage["s2_concern_split"] = split

        targets = split["segments"] if (split["fired"] and split["segments"]) else [objective]

        # ---- stages 3 + 4
        incbase = _score(ws)
        pristine = _snap(ws)
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

        synth = synthesise_check(objective, pristine, _snap(ws))
        calls[0] += synth["calls"]

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
        stage["synth"] = synth
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


ARMS_EXTRA = {"test_synth_retry": run_m7}
