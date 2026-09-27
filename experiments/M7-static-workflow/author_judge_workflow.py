"""author_judge - `author`, plus judge_fullctx's judge on the kept state. Queue A13.

A12 plus a judge, so the briefing effect is separable from the judging effect.
Everything up to the terminal is `author`, copied verbatim; see its header.

WHICH JUDGE, AND WHY. judge_fullctx's: one call, one verdict, NO conditions -- no
`expected`, no `checked`, no `n_conditions`. Operator decision 2026-09-27, on
structure rather than on score: 50-findings/18 shows the checklist judges fail by
compounding per-condition noise through an all(yes) rule, at a rate set by how
many conditions the author wrote. This judge has no conjunction to compound. Its
accuracy is not established by that; only that it cannot fail in that way.

Like judge_fullctx it has NO authority: the verdict is recorded and nothing reads
it. It runs on every task, including those stage 1 ended with a yield or decline,
so a verdict is recorded per task.

WHAT CHANGES UNDERNEATH IT. judge_fullctx is defined as a judge holding the same
material the worker held. Here that material includes the authored brief, so the
judge is handed the brief and checks the work against the same brief that
produced it. That asks whether the worker did what it was told. It is coherent,
and it is NOT the independence test judge_fullctx was built for. Each stage
record says which one it ran as `judge_question`:

    compliance-with-brief   a brief was written; the judge holds it
    fullctx-unbriefed       no brief (yield, decline, unparsed); judge_fullctx's
                            own question, on the request and the code alone

CONTROL. The queue names judge_caveat ("same audit stage, same judge, differing
only in whether the worker is briefed"). With the judge now judge_fullctx's, that
control shares neither the judge nor, since stage 1 was rewritten, the audit
stage exactly. Recorded here, not resolved here.

`author` header follows.

author - stage 1 authors the worker's brief, or yields, or declines. No judge.

Queue A12. In the judge-anchored family stage 1 already writes `expected` -- 2 to
5 observable conditions, before any work exists -- and `expected` reaches the
judge in three arms and the implementer in none. This arm turns that stage from a
reporter into an author: its conditions ARE the worker's brief, handed over word
for word.

A ROLE CHANGE, NOT A CONFIG CHANGE. The family's stage-1 prompt says "You do NOT
decide whether the task should be attempted - something else decides that."
That sentence is gone, and the prompt is rewritten rather than patched: the
stage now decides. It produces exactly one of three outcomes --

    yield     something the task depends on is missing; ask for it  -> blocked-yield
    decline   the request rests on something false                  -> declined
    brief     the task is sound; write the conditions the worker gets -> implement

-- and the first two are terminal. Stage 1 now CAN produce a terminal, which the
family's header forbade; that is the authority being tested.

Everything after stage 1 is the family's loop unchanged: the concern split, the
incumbent-protected keeper, and the dloop hint ("Current state still fails",
50-findings/17) -- so the worker still sees the gate's failing names every round,
exactly as in the control. What is added is the brief in the worker's instruction.
What is removed is the judge.

RECORDED PER RUN (stage record and row `arm_extra.author`): which outcome stage 1
took, its reason, and `n_conditions` -- how many conditions the brief carried.
50-findings/18 shows the count of conditions is a live variable for a judge; here
it is the size of the brief, and it is recorded rather than left to the author's
discretion and forgotten. A stage-1 reply that does not parse is recorded as
outcome `unparsed` and the worker runs on the objective alone, unbriefed; it is
never counted as any of the three.

CONTROL. The queue names `judge_caveat`: same audit stage, same judge, differing
only in whether the worker is briefed. That describes `author_judge`, not this arm,
and since A13 was moved to judge_fullctx's judge (operator decision 2026-09-27) it
no longer describes either exactly. Recorded here, not resolved here.

Built from judge_caveat_workflow.py; the workspace helpers, the check, the concern
split and the escalation payload are copied verbatim. A copy, not an import, on
purpose: arm_sha hashes this file alone, so a change to a shared helper would move
this arm's behaviour without moving its key.
"""
from __future__ import annotations

import ast
import difflib
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
from stage_tags import setup_tags  # noqa: E402
import row_extra  # noqa: E402

RUNS = HERE / "runs_author_judge"
STAGE_LOG = HERE / "stage_influence_author_judge.jsonl"

CMD = ["python", "test_task.py"]
NL = chr(10)

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

AUDIT = """You are a senior engineer reading a task before any code is written. You
decide whether it should be attempted, and when it should, you write the brief the
engineer doing the work will be given.

Choose exactly ONE outcome.

  "yield": the task cannot be done from what is here. Something it depends on is
  missing from both the request and the code, and doing it would mean guessing.
  Name what is missing in "reason".

  "decline": the request rests on something false about this code, or asks for a
  change that would make the code wrong. Say what, in "reason".

  "brief": the request is sound and can be done. Then also report:

    "segments": the independent changes the objective asks for, as a list, each
    written as a standalone instruction, in the order the objective gives them. Use
    a one-element list when the objective asks for a single thing.

    "expected": what a FINISHED change must exhibit, as 2 to 5 short observable
    conditions. The engineer is handed this list, word for word, as their brief.
    Name the specific values, edge cases and behaviours the objective implies, not
    the topic of the work.
        good: ["retries=0 makes exactly one attempt",
               "the LAST exception is re-raised when every attempt fails",
               "retries=2 makes three attempts in total"]
        bad:  ["the retry logic works", "a retries parameter is added"]
    You are writing this BEFORE any work exists, so describe the target, never an
    attempt at it.

Answer with ONE JSON object and nothing else:
  "outcome": "yield", "decline" or "brief"
  "reason": one sentence
  "segments": a list (brief only)
  "expected": a list (brief only)

OBJECTIVE:
{obj}

CODE:
{code}"""

_OUTCOMES = {"yield", "decline", "brief"}

# How the brief reaches the worker. Model-facing; arm_sha covers it.
BRIEF = "A finished change must satisfy every one of these:\n{conds}"


def author_stage(objective: str, ws: Path) -> dict:
    """Stage 1. Always fires. HAS AUTHORITY: two of its outcomes are terminal.

    One call, as in the family. `outcome` is None when the reply does not parse
    or names none of the three; the arm records that as `unparsed` and never
    reads it as one of them.
    """
    code = "\n".join(f"--- {p.name} ---\n{p.read_text(errors='replace')}"
                     for p in _py_files(ws))
    t0 = time.monotonic()
    out = {"outcome": None, "reason": "", "segments": None, "expected": [],
           "parsed": False}
    try:
        g = generate(AUDIT.replace("{obj}", objective).replace("{code}", code[:4000]),
                     temperature=0.3, num_predict=260)
        m = _JSON.search(g.text)
        if m:
            d = json.loads(m.group(0))
            oc = str(d.get("outcome", "")).strip().lower()
            out["outcome"] = oc if oc in _OUTCOMES else None
            out["reason"] = str(d.get("reason", ""))[:300]
            segs = d.get("segments")
            if isinstance(segs, list):
                segs = [str(x).strip()[:400] for x in segs if str(x).strip()]
                out["segments"] = segs or None
            exp = d.get("expected")
            if isinstance(exp, list):
                out["expected"] = [str(x).strip()[:200] for x in exp
                                   if str(x).strip()][:5]
            out["parsed"] = out["outcome"] is not None
    except Exception as e:  # noqa: BLE001
        out["error"] = repr(e)[:120]
    out["calls"] = 1
    out["wall_s"] = round(time.monotonic() - t0, 1)
    return out


def _brief_text(expected: list) -> str:
    return BRIEF.replace("{conds}", "\n".join(f"  {i}. {c}"
                                              for i, c in enumerate(expected, 1)))


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
    """Stage 3. One implementer instance per attempt."""
    b = assemble(objective, ws, token_budget=8000)
    return run_processor(role="implementer", objective=objective, context=b,
                         workspace_root=ws, recorder=rec, gate=Gate(),
                         parent_invocation_id=root, intent_ref="m7",
                         interaction_mode="oneshot", config_ref="author_judge")


def _pass(target: str, ws: Path, rec, root, best: dict, calls: list,
          greenfield: bool, deadline: float, brief: str) -> dict:
    """Stage 4 around stage 3: the family's test-gated loop, no judge.

    The one addition is `brief`, placed after the target and before the gate's
    hint on every attempt, so the worker is briefed on each round and not only
    the first. Empty when stage 1 did not parse: the worker then runs unbriefed.
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
        step = f"{target}\n\n{brief}" if brief else target
        plain = greenfield and rnd == 0 and best["src"] == "incumbent"
        if not plain:
            hint = best["s"]["fails"]
            if hint:
                step = (f"{step}\n\nCurrent state still fails:\n{hint}\n"
                        "Output the whole corrected file(s).")
        _implement(step, ws, rec, root)
        calls[0] += 1
        s = _score(ws)
        # R1: strict improvement AND no check that was passing has begun to fail.
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

JUDGE = """You are reviewing a change somebody else made to a small Python project.

You are given the code as it stood BEFORE any work, the brief the engineer was given,
and the change as a diff. You did not write any of it and you have not seen the
engineer's reasoning or any test output.

Judge whether the change carries out the request. Read the code, not just the diff:
the diff shows what moved, and whether that is enough depends on what surrounds it.

An empty diff means the engineer changed nothing. Either they could not do the work --
"not_met" -- or they read the request, found it rested on something false, and
correctly refused -- "unsound_request". The code and the request together are what
tell them apart.

Answer with ONE JSON object and nothing else:
  "verdict": one of "met", "not_met", "unsound_request"
  "why": one sentence, citing something you can point at

REQUEST:
{obj}

THE BRIEF THE ENGINEER WAS GIVEN:
{brief}

THE CODE BEFORE ANY WORK:
{code}

THE CHANGE:
{diff}"""

_VERDICTS = {"met", "not_met", "unsound_request"}


def _diff(before: dict, after: dict) -> str:
    out = []
    for name in sorted(set(before) | set(after)):
        a = before.get(name, "").splitlines(keepends=True)
        b = after.get(name, "").splitlines(keepends=True)
        if a == b:
            continue
        out.extend(difflib.unified_diff(a, b, fromfile=name, tofile=name, n=3))
    d = "".join(out)
    return d[:5000] if d else "(no change to any .py file)"


def judge_change(objective: str, brief: str, pristine: dict, after: dict) -> dict:
    """judge_fullctx's judge_change, with the brief in its material. Records a
    verdict; changes nothing. See the module header for what that makes it."""
    t0 = time.monotonic()
    diff = _diff(pristine, after)
    code = "\n".join(f"--- {n} ---\n{c}" for n, c in sorted(pristine.items()))
    out = {"verdict": None, "why": "", "parsed": False, "authority": "none",
           "diff_empty": diff.startswith("(no change"),
           "code_bytes": len(code), "diff_bytes": len(diff)}
    try:
        prompt = (JUDGE.replace("{obj}", objective)
                       .replace("{brief}", brief or "(no brief was written)")
                       .replace("{code}", code[:7000])
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
        out["error"] = repr(e)[:140]
    out["calls"] = 1
    out["wall_s"] = round(time.monotonic() - t0, 1)
    return out


def _yield_payload(objective: str, author: dict) -> dict:
    """What the operator is asked when stage 1 yields: the missing piece, named."""
    return {
        "objective": objective,
        "missing": author.get("reason", ""),
        "question": ("Before any work, the task was judged to depend on something "
                     f"not present: {author.get('reason', '')[:300]} Can you supply "
                     "it, or say it is not needed?"),
    }


# --------------------------------------------------------------- the arm

def _judge(stage: dict, objective: str, brief: str, pristine: dict, after: dict,
           calls: list) -> None:
    v = judge_change(objective, brief, pristine, after)
    v["scope"] = "task-level, on the kept state"
    calls[0] += v["calls"]
    stage["judge"] = v
    stage["judge_question"] = "compliance-with-brief" if brief else "fullctx-unbriefed"


def run_author_judge(objective: str, ws: Path) -> str:
    rec = RunRecorder(RUNS, intent_text=objective, meta={"arm": "author_judge", "suite": "m6"})
    root = rec.invocation(role="author-judge-workflow", model_identity={"name": "harness"},
                          intent_ref="m7", config_ref="m7")
    t0 = time.monotonic()
    stage = {"task_objective": objective[:200],
             "task": os.environ.get("M6_TASK"),
             "rep": os.environ.get("M6_REP")}
    try:
        # ---- stage 1: always fires, and decides
        author = author_stage(objective, ws)
        outcome = author["outcome"] or "unparsed"
        expected = (author.get("expected") or []) if outcome == "brief" else []
        stage["s1_author"] = {**author, "fired": True, "advisory": False}
        stage["author_outcome"] = outcome
        stage["n_conditions"] = len(expected)
        stage["variant"] = ("author_judge: author plus judge_fullctx's judge, "
                            "handed the brief, no authority")
        calls = [author["calls"]]
        incbase = _score(ws)
        pristine = _snap(ws)          # the judge's "before", taken before any call

        if outcome in ("yield", "decline"):
            # Terminal from stage 1. Nothing is implemented.
            terminal = "declined" if outcome == "decline" else "blocked-yield"
            payload = _yield_payload(objective, author) if outcome == "yield" else None
            stage["influence"] = {"s1_consumed_by": ["terminal"],
                                  "judge_consumed_by": []}          # no authority
            _judge(stage, objective, "", pristine, _snap(ws), calls)
            stage.update({"terminal": terminal, "calls": calls[0],
                          "wall_s": round(time.monotonic() - t0, 1),
                          "baseline_comb": incbase["comb"],
                          "final_comb": incbase["comb"],
                          "check_dims": incbase["dims"],
                          "escalation_payload": payload})
            return terminal

        # ---- stage 2: fires on condition. A brief carries the segments; an
        # unparsed reply carries none, so only the syntactic split can fire.
        split = concern_split(objective, author if outcome == "brief" else {})
        stage["s2_concern_split"] = split
        targets = split["segments"] if (split["fired"] and split["segments"]) else [objective]
        brief = _brief_text(expected) if expected else ""

        # ---- stages 3 + 4
        greenfield = not _py_files(ws)
        best = {"s": incbase, "snap": _snap(ws), "src": "incumbent",
                "n_targets": len(targets)}
        deadline = t0 + TASK_WALL_CAP_S          # R2
        attempts = []
        for t in targets:
            before = best["s"]["comb"]
            best = _pass(t, ws, rec, root, best, calls, greenfield, deadline, brief)
            attempts.append({"target": t[:120], "comb_before": before,
                             "comb_after": best["s"]["comb"]})
        _restore(ws, best["snap"])
        fin = _score(ws)

        if best["src"] == "incumbent":
            terminal = "declined" if fin["full"] else "blocked-no-progress"
        elif fin["full"]:
            terminal = "answered"
        else:
            terminal = "blocked-partial"

        payload = None
        if terminal.startswith("blocked"):
            payload = _escalation_payload(objective, {"concern": author.get("reason", "")},
                                          split, attempts, fin)

        stage["influence"] = {
            "s1_brief_consumed_by": (["s3_instruction"] if brief else []),
            "s1_segments_consumed_by": (
                ["s3_targets"] if split["source"] == "model" else []),
            "s2_consumed_by": (["s3_targets"] if split["fired"] and split["segments"]
                               else []),
        }
        stage["brief"] = brief
        stage["influence"]["judge_consumed_by"] = []      # no authority
        _judge(stage, objective, brief, pristine, _snap(ws), calls)
        stage.update({"terminal": terminal, "calls": calls[0],
                      "wall_s": round(time.monotonic() - t0, 1),
                      "baseline_comb": incbase["comb"], "final_comb": fin["comb"],
                      "check_dims": fin["dims"], "escalation_payload": payload})
        return terminal
    finally:
        # Which outcome stage 1 took, on the row as well as the stage record,
        # so the store alone can split runs by it. Beside the score.
        row_extra.EXTRA["author"] = {
            "outcome": stage.get("author_outcome", "unparsed"),
            "n_conditions": stage.get("n_conditions", 0),
            "reason": (stage.get("s1_author") or {}).get("reason", "")}
        row_extra.EXTRA["judge"] = {
            "verdict": (stage.get("judge") or {}).get("verdict"),
            "parsed": (stage.get("judge") or {}).get("parsed", False),
            "question": stage.get("judge_question")}
        stage.update(setup_tags())
        STAGE_LOG.parent.mkdir(parents=True, exist_ok=True)
        with STAGE_LOG.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(stage) + "\n")
        rec.close("completed")


ARMS_EXTRA = {"author_judge": run_author_judge}
