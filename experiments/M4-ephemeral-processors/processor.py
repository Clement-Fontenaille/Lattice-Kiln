"""M4 processor runtime - one ephemeral instance per docs/10-technical/06.

Binds a role + objective + context bundle + capability set, calls the working
-default model once, parses its control block, routes EVERY proposed effect
through the M3 enforcement pipeline, records EVERY event through the M2
RunRecorder, and realizes only what the floor passes. No resume.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from _bridge import CapabilitySet, Gate, submit_effect
from context_assembly import ContextBundle
from ollama_client import DEFAULT_MODEL, chat, generate
from roles import PROTOCOL as PROTOCOL_MARKERS  # the marker text
from roles import PROTOCOL_TOOLS, ROLE_GRANTS, TOOLS, prompt_for

# LATTICE_PROTOCOL: how the model is asked to hand back its work.
#
#   "tools"    -- write_file / conclude as tool definitions, sent through
#                 /api/chat so Ollama's per-model RENDERER serialises them into
#                 whatever dialect the model was tuned on.
#   "markers"  -- the bespoke FILE / CONTROL blocks, every row before today.
#
# This is a variable, not a constant, and it is in the setup key. Findings 15
# showed the marker form is a measured cause of failure on at least one model
# while carrying no trained state change in its vocabulary -- so a score under
# it is a joint measurement of capability and of familiarity with a dialect
# this harness invented. Flipping the default without keying it would have put
# every new row in a different regime from every old one, invisibly. That was
# the defect the finding closed on; this is the fix.
PROTOCOL = os.environ.get("LATTICE_PROTOCOL", "tools").strip().lower()
if PROTOCOL not in ("tools", "markers"):
    raise ValueError(f"LATTICE_PROTOCOL must be tools|markers, got {PROTOCOL!r}")

_FILE = re.compile(r"<<<FILE\s+path=(.+?)>>>\r?\n(.*?)\r?\n<<<ENDFILE>>>", re.DOTALL)
_CTRL = re.compile(r"<<<CONTROL>>>\s*(.*?)\s*<<<ENDCONTROL>>>", re.DOTALL)
MODEL_IDENTITY = {"name": "qwen2.5-coder", "quant": "Q4_K_M", "params_b": 7,
                  "runtime": "ollama", "offloaded": False}
PROC_TIMEOUT_S = 120


@dataclass
class ProcessorResult:
    invocation_id: str
    role: str
    terminal_state: str
    summary: str
    parse_ok: bool
    proposed: int = 0
    realized: int = 0
    refused_by_gate: int = 0
    refused_by_policy: int = 0
    files_written: list[str] = field(default_factory=list)
    process_runs: list[dict[str, Any]] = field(default_factory=list)
    context_requests: list[str] = field(default_factory=list)
    control: dict[str, Any] = field(default_factory=dict, repr=False)
    body_text: str = field(default="", repr=False)
    gen_tokens_per_s: float = 0.0
    raw_output: str = field(default="", repr=False)


def capability_set_for(role: str) -> CapabilitySet:
    return CapabilitySet(role=role, grants=dict(ROLE_GRANTS.get(role, {})))


def _extract(text: str) -> dict[str, Any] | None:
    """-> {"control": <dict>, "files": {path: content}} or None if no valid
    CONTROL block. File bodies are raw text and never parsed as JSON."""
    ctrl = None
    m = _CTRL.search(text)
    if m:
        body = m.group(1).strip()
        if body.startswith("```"):
            body = re.sub(r"^```[a-zA-Z]*\n?|\n?```$", "", body).strip()
        try:
            obj = json.loads(body)
            ctrl = obj if isinstance(obj, dict) else None
        except json.JSONDecodeError:
            ctrl = None
    if ctrl is None:
        # fallback: last {...} object (one nesting level) carrying terminal_state
        for cand in reversed(re.findall(r"\{(?:[^{}]|\{[^{}]*\})*\}", text, re.DOTALL)):
            if '"terminal_state"' in cand:
                try:
                    obj = json.loads(cand)
                except json.JSONDecodeError:
                    continue
                if isinstance(obj, dict):
                    ctrl = obj
                    break
    if ctrl is None:
        return None
    files = {p.strip(): c for p, c in _FILE.findall(text)}
    return {"control": ctrl, "files": files}


def adapter_fingerprint() -> str:
    """Hash of the MODEL-FACING surface, as distinct from the arm's.

    Two different things were being conflated under one absent key.

    ARM-DEPENDENT text varies with the experiment -- the AUDIT and JUDGE
    prompts, the workflow's shape. `arm_sha` and `prompt_sha` already cover it,
    and a change there means a different question is being asked.

    MODEL-DEPENDENT text varies with the adapter -- the output protocol, the
    tool schemas, the wire format of a tool result. It is IDENTICAL across
    every arm, and it changes when we point at a different model or fix a
    renderer quirk, not when we change the experiment. Folding it into
    `arm_sha` would make an adapter fix look like a new arm, which is the same
    conflation running the other way.

    So it gets its own hash, and it hashes the TEXT THE MODEL SEES rather than
    the file that produces it -- comments and docstrings move constantly and
    never reach the model, while a one-word change inside the protocol block
    changes everything and would not move a file hash any more than a typo fix
    in a comment does.

    The occasion for this: a tool result briefly ended with "then call conclude
    exactly once to finish". That is an instruction, present in every tool-mode
    run, and under the old key it would have been invisible -- same cell id
    before and after. Cf. 50-findings/15, which closes on precisely this defect
    one layer up.
    """
    parts = [f"protocol={PROTOCOL}"]
    if PROTOCOL == "tools":
        parts.append(PROTOCOL_TOOLS)
        parts.append(json.dumps(TOOLS, sort_keys=True))
        # Representative results, so a change to their WORDING moves the hash.
        sample = {"a.py": "x"}
        for call in ({"name": "write_file",
                      "arguments": {"path": "a.py", "content": "x"}},
                     {"name": "write_file", "arguments": {"path": ""}},
                     {"name": "conclude", "arguments": {}},
                     {"name": "_unknown", "arguments": {}}):
            parts.append(_tool_result(call, sample))
    else:
        parts.append(PROTOCOL_MARKERS)
    return hashlib.sha256(chr(10).join(parts).encode("utf-8")).hexdigest()[:12]


def _tool_result(call: dict[str, Any], files: dict[str, str]) -> str:
    """What the runtime tells the model after one of its calls.

    A tool result is the model's only evidence that its turn had an effect. An
    uninformative one leaves it to infer the state of the world, which is the
    single most expensive thing a reasoning model can be asked to do.

    STATE ONLY. NO INSTRUCTION. An earlier version ended every result with
    "then call conclude exactly once to finish", which is wrong twice over.
    It presumes concluding is what comes next, when it is only true at the end
    -- after the first of five files the model needs to keep working, and being
    pointed at the exit each time biases it toward stopping early. And it makes
    the runtime a second voice giving directions: the obligation to conclude is
    stated once, in PROTOCOL_TOOLS, and a protocol repeated after every call is
    a prompt, not a protocol.

    It also quietly contaminated measurement. The same text would have been
    present in every tool-mode run, so any later comparison of prompt wording
    would have been measuring this line as well, with nothing recording that it
    was there.

    So: what happened, and nothing else. "accepted" and not "applied", because
    the gate has not ruled yet.
    """
    name = call.get("name", "")
    args = call.get("arguments") or {}
    if name == "write_file":
        path = str(args.get("path", "")).strip()
        body = str(args.get("content", ""))
        if not path:
            return json.dumps({"status": "error",
                               "detail": "write_file requires a non-empty path"})
        return json.dumps({
            "status": "accepted",
            "path": path,
            "bytes": len(body),
            "lines": body.count(chr(10)) + 1,
            "files_so_far": sorted(files),
        })
    if name == "conclude":
        return json.dumps({"status": "accepted"})
    return json.dumps({"status": "error", "detail": f"unknown tool {name!r}"})


_LIST_FIELDS = ("run", "context_requests")


def _clean_conclude(args: dict[str, Any]) -> dict[str, Any]:
    """Normalise one conclude call's arguments.

    Two things, both observed rather than anticipated:

    Empty slots are dropped. The XML recovery path returns every parameter the
    model listed, including ones it left blank, so `verdict` arrives as "" --
    and "" is the absence of a verdict, not a bad one. Keeping it would let a
    reviewer that declined to judge read as one that judged badly.

    List fields arrive as JSON STRINGS. Measured 2026-09-23 on
    nemotron3-nano-4b: `run` came back as the two characters `[]` rather than
    an empty list, because the tool-call convention allows arguments to be a
    JSON string and some renderers do not decode one level down. The caller
    tests `isinstance(..., list)` before executing anything, so a model asking
    to run its own tests would have been dropped in silence -- no error, no
    record, just commands that never ran.
    """
    out: dict[str, Any] = {}
    for k, v in args.items():
        if isinstance(v, str) and k in _LIST_FIELDS:
            try:
                v = json.loads(v)
            except json.JSONDecodeError:
                v = [v] if v.strip() else []
        if v in ("", [], None) or v == {}:
            continue
        out[k] = v
    return out


MAX_TOOL_TURNS = 6
"""Turns a tool-mode processor may take before it is called unparseable.

Six, because a turn costs a call and the contract needs at most: one turn per
file, plus conclude. No observed role writes more than a few files, and a
runaway loop is a cost, not a result.
"""


def _run_tools(prompt: str, *, model: str, num_predict: int = 1536
               ) -> tuple[Any, dict[str, Any] | None, str]:
    """Drive the tool loop until `conclude` arrives. -> (gen, parsed, log).

    The model emits one call, stops, and waits for a result before emitting the
    next. Measured, not assumed: on nemotron3-nano-4b turn one is write_file
    and conclude does not appear until turn two.

    The result fed back says WHAT HAPPENED and WHAT IS LEFT TO DO, and that is
    load-bearing rather than cosmetic. The first version returned the bare word
    "recorded", and the single truncated call in the whole corpus turned out to
    be a turn whose only new input was that word: the model had just written a
    file, was told nothing about the outcome, and reasoned in circles working
    out what had become of it. 4,466 characters of thinking and no answer.

    That failure was read at first as Nemotron being unable to stop. It was the
    loop starving it. The marker protocol never had the problem because it was
    single-shot -- there was no second turn to under-inform.

    Nothing is realized here. Every proposed effect still goes through the gate
    afterwards, exactly as the marker protocol's FILE blocks did, so the result
    says "accepted", never "applied" -- the model is told its call was received
    and well-formed, never that it was permitted.
    """
    msgs: list[dict[str, Any]] = [{"role": "user", "content": prompt}]
    files: dict[str, str] = {}
    ctrl: dict[str, Any] | None = None
    log: list[str] = []
    gen = None
    for _ in range(MAX_TOOL_TURNS):
        gen = chat(msgs, model=model, tools=TOOLS, num_predict=num_predict)
        log.append(gen.text)
        if not gen.tool_calls:
            break
        raw_msg = (gen.raw.get("message") or {})
        msgs.append({"role": "assistant",
                     "content": raw_msg.get("content", ""),
                     "tool_calls": raw_msg.get("tool_calls") or []})
        for c in gen.tool_calls:
            args = c.get("arguments") or {}
            if c.get("name") == "write_file":
                path = str(args.get("path", "")).strip()
                if path:
                    files[path] = str(args.get("content", ""))
            elif c.get("name") == "conclude":
                # Drop empty slots. The XML recovery path returns every
                # parameter the model listed, including ones it left blank, so
                # `verdict` arrives as "" rather than absent -- and "" is not a
                # valid verdict, it is the absence of one. Keeping it would let
                # a reviewer that declined to judge read as a reviewer that
                # judged badly.
                ctrl = _clean_conclude(args)
            msgs.append({"role": "tool", "tool_name": c.get("name", ""),
                         "content": _tool_result(c, files)})
        if ctrl is not None:
            break
    parsed = None if ctrl is None else {"control": ctrl, "files": files}
    return gen, parsed, "\n".join(t for t in log if t)


def _norm_abs(workspace_root: Path, rel: str) -> Path:
    return (workspace_root / rel).resolve()


def run_processor(*, role: str, objective: str, context: ContextBundle,
                  workspace_root: str | Path, recorder, gate: Gate,
                  parent_invocation_id: str | None = None,
                  interaction_mode: str = "oneshot",
                  extra_input: str | None = None,
                  intent_ref: str | None = None,
                  model: str = DEFAULT_MODEL,
                  prompt: str | None = None,
                  config_ref: str = "m4-baseline") -> ProcessorResult:
    ws = Path(workspace_root).resolve()
    actor = capability_set_for(role)

    inv = recorder.invocation(
        role=role, model_identity=dict(MODEL_IDENTITY),
        parent_invocation_id=parent_invocation_id, intent_ref=intent_ref,
        context_ref=f"bundle:{context.token_estimate}tok:{len(context.entries)}src",
        config_ref=config_ref)

    use_tools = PROTOCOL == "tools"
    if prompt is None:  # callers (e.g. M5 roles_v2) may supply a tuned prompt
        prompt = prompt_for(role, context.render(), objective, extra=extra_input,
                            protocol=PROTOCOL_TOOLS if use_tools else None)
    if use_tools:
        nudge = ("\n\nYou did not call conclude. Do the work, then call "
                 "conclude exactly once.")
        gen, parsed, out = _run_tools(prompt, model=model)
        if parsed is None:
            gen, parsed, out = _run_tools(prompt + nudge, model=model)
    else:
        nudge = ("\n\nYour previous reply had no valid <<<CONTROL>>> block. "
                 "Reply again following the OUTPUT FORMAT exactly: FILE blocks "
                 "then one <<<CONTROL>>> block with valid JSON.")
        gen = generate(prompt, model=model)
        out = gen.text
        parsed = _extract(out)
        if parsed is None:
            gen = generate(prompt + nudge, model=model)
            out = gen.text
            parsed = _extract(out)

    res = ProcessorResult(invocation_id=inv, role=role, terminal_state="blocked",
                          summary="", parse_ok=parsed is not None,
                          gen_tokens_per_s=round(gen.tokens_per_s, 1), raw_output=out)
    if parsed is None:
        res.summary = ("model never called conclude" if use_tools
                   else "no valid control block in model output")
        _record_conclusion(recorder, gate, actor, inv, ws, res)
        return res

    ctrl = parsed["control"]
    res.control = ctrl
    # On the tool path the parser already lifted the calls out, so whatever is
    # left in `text` IS the body -- there is nothing to split off.
    res.body_text = out.strip() if use_tools else re.split(
        r"<<<CONTROL>>>|\{[^{}]*\"terminal_state\"", out, maxsplit=1)[0].strip()
    res.terminal_state = str(ctrl.get("terminal_state", "blocked"))
    res.summary = str(ctrl.get("summary", "")).strip()
    creqs = ctrl.get("context_requests") or []
    res.context_requests = [str(c) for c in creqs] if isinstance(creqs, list) else []

    for path, content in parsed["files"].items():
        _route_effect(recorder, gate, actor, inv, ws, 1,
                      {"type": "workspace_write", "path": path, "content": content}, res)
    for cmd in (ctrl.get("run") or []) if isinstance(ctrl.get("run"), list) else []:
        if isinstance(cmd, str) and cmd.strip():
            _route_effect(recorder, gate, actor, inv, ws, 2,
                          {"type": "process_run", "command": cmd.strip()}, res)

    _record_conclusion(recorder, gate, actor, inv, ws, res)
    # NB: the caller owns the run lifecycle. A processor terminating is not the
    # run terminating (spec 06 lifecycle); the harness calls recorder.close().
    return res


def _route_effect(recorder, gate, actor, inv, ws: Path, etype: int,
                  e: dict[str, Any], res: ProcessorResult) -> None:
    res.proposed += 1
    if etype == 1:
        rel = str(e.get("path", "")).strip()
        target = _norm_abs(ws, rel)
        exists = target.exists()
        eff = {"effect_type": 1, "envelope": {
            "workspace_root": str(ws), "target_path": str(target),
            "op": "modify" if exists else "create",
            "representable": True, "attributable": inv, "reversible": "vcs"}}
        payload = f"write:{rel}"
    else:  # etype == 2
        cmd = str(e.get("command", "")).strip()
        eff = {"effect_type": 2, "envelope": {
            "workspace_root": str(ws), "command": cmd,
            "representable": True, "attributable": inv, "reversible": "n/a"}}
        payload = f"run:{cmd}"

    verdict = submit_effect(eff, actor, gate=gate)

    if verdict.proceed:
        recorder.proposed_effect(inv, effect_type=etype, payload_ref=payload,
                                 disposition="realized")
        _realize(recorder, inv, ws, etype, e, eff, res)
        return

    if verdict.stopped_by == "gate":
        ivid = recorder.safety_intervention(
            kind="gate_refusal", disposition="halted", on_invocation_id=inv,
            note=f"{payload} :: {verdict.clause} {verdict.reason}")
        recorder.proposed_effect(inv, effect_type=etype, payload_ref=payload,
                                 disposition="rejected_by_gate",
                                 links={"intervention_id": ivid})
        res.refused_by_gate += 1
    else:  # capability | representability | sequence
        recorder.proposed_effect(inv, effect_type=etype, payload_ref=payload,
                                 disposition="rejected_by_capability",
                                 links={"stopped_by": verdict.stopped_by,
                                        "reason": verdict.reason})
        res.refused_by_policy += 1


def _realize(recorder, inv, ws: Path, etype: int, e: dict, eff: dict,
             res: ProcessorResult) -> None:
    if etype == 1:
        rel = str(e.get("path", "")).strip()
        target = _norm_abs(ws, rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        content = e.get("content", "")
        target.write_text(content if isinstance(content, str) else str(content),
                          encoding="utf-8")
        res.files_written.append(rel)
        recorder.realized_effect(inv, effect_type=1, envelope=eff["envelope"],
                                 outcome="realized",
                                 result_ref=f"wrote:{rel}:{len(content)}B")
    else:
        cmd = str(e.get("command", "")).strip()
        try:
            cp = subprocess.run(shlex.split(cmd), cwd=str(ws), capture_output=True,
                                text=True, timeout=PROC_TIMEOUT_S)
            tail = (cp.stdout + cp.stderr)[-800:]
            rec = {"command": cmd, "exit": cp.returncode, "tail": tail}
        except (subprocess.TimeoutExpired, OSError, ValueError) as ex:
            rec = {"command": cmd, "exit": None, "tail": f"<runtime error: {ex}>"}
        res.process_runs.append(rec)
        recorder.realized_effect(inv, effect_type=2, envelope=eff["envelope"],
                                 outcome="realized",
                                 result_ref=f"exit={rec['exit']}")
    res.realized += 1


def _record_conclusion(recorder, gate, actor, inv, ws: Path,
                       res: ProcessorResult) -> None:
    """The processor's own conclusion, recorded as a work-record mutation
    (effect type 4). Whether a conclusion is genuinely an 'effect' is exactly
    the kind of boundary question M4 exists to surface - noted in findings."""
    eff = {"effect_type": 4, "envelope": {
        "representable": True, "attributable": inv, "reversible": "work-record",
        "terminal_state": res.terminal_state, "summary": res.summary,
        "role": res.role, "verdict": res.control.get("verdict"),
        "context_requests": list(res.context_requests)}}
    verdict = submit_effect(eff, actor, gate=gate)
    disp = "realized" if verdict.proceed else (
        "rejected_by_gate" if verdict.stopped_by == "gate" else "rejected_by_capability")
    recorder.proposed_effect(inv, effect_type=4,
                             payload_ref=f"conclude:{res.terminal_state}",
                             disposition=disp)
    if verdict.proceed:
        recorder.realized_effect(inv, effect_type=4, envelope=eff["envelope"],
                                 outcome="realized", result_ref="conclusion recorded")
