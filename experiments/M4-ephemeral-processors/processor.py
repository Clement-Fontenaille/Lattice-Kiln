"""M4 processor runtime - one ephemeral instance per docs/10-technical/06.

Binds a role + objective + context bundle + capability set, calls the working
-default model once, parses its control block, routes EVERY proposed effect
through the M3 enforcement pipeline, records EVERY event through the M2
RunRecorder, and realizes only what the floor passes. No resume.
"""
from __future__ import annotations

import json
import re
import shlex
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from _bridge import CapabilitySet, Gate, submit_effect
from context_assembly import ContextBundle
from ollama_client import DEFAULT_MODEL, generate
from roles import ROLE_GRANTS, prompt_for

_BLOCK = re.compile(r"===PROCESSOR-OUTPUT===\s*(.*?)\s*===END===", re.DOTALL)
_EFFECT_TYPE = {"workspace_write": 1, "process_run": 2}
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
    gen_tokens_per_s: float = 0.0
    raw_output: str = field(default="", repr=False)


def capability_set_for(role: str) -> CapabilitySet:
    return CapabilitySet(role=role, grants=dict(ROLE_GRANTS.get(role, {})))


def _extract(text: str) -> dict[str, Any] | None:
    m = _BLOCK.search(text)
    if not m:
        return None
    body = m.group(1).strip()
    if body.startswith("```"):
        body = re.sub(r"^```[a-zA-Z]*\n?|\n?```$", "", body).strip()
    try:
        obj = json.loads(body)
        return obj if isinstance(obj, dict) else None
    except json.JSONDecodeError:
        return None


def _norm_abs(workspace_root: Path, rel: str) -> Path:
    return (workspace_root / rel).resolve()


def run_processor(*, role: str, objective: str, context: ContextBundle,
                  workspace_root: str | Path, recorder, gate: Gate,
                  parent_invocation_id: str | None = None,
                  interaction_mode: str = "oneshot",
                  extra_input: str | None = None,
                  intent_ref: str | None = None,
                  model: str = DEFAULT_MODEL) -> ProcessorResult:
    ws = Path(workspace_root).resolve()
    actor = capability_set_for(role)

    inv = recorder.invocation(
        role=role, model_identity=dict(MODEL_IDENTITY),
        parent_invocation_id=parent_invocation_id, intent_ref=intent_ref,
        context_ref=f"bundle:{context.token_estimate}tok:{len(context.entries)}src",
        config_ref="m4-baseline")

    prompt = prompt_for(role, context.render(), objective, extra=extra_input)
    gen = generate(prompt, model=model)
    out = gen.text
    parsed = _extract(out)
    if parsed is None:
        gen = generate(prompt + "\n\nYour previous reply had no valid control block. "
                                "Reply again with ONLY the ===PROCESSOR-OUTPUT=== block.",
                       model=model)
        out = gen.text
        parsed = _extract(out)

    res = ProcessorResult(invocation_id=inv, role=role, terminal_state="blocked",
                          summary="", parse_ok=parsed is not None,
                          gen_tokens_per_s=round(gen.tokens_per_s, 1), raw_output=out)
    if parsed is None:
        res.summary = "no valid control block in model output"
        _record_conclusion(recorder, gate, actor, inv, ws, res)
        recorder.close("blocked")
        return res

    res.terminal_state = str(parsed.get("terminal_state", "blocked"))
    res.summary = str(parsed.get("summary", "")).strip()
    effects = parsed.get("effects") or []

    for e in effects if isinstance(effects, list) else []:
        if not isinstance(e, dict):
            continue
        etype = _EFFECT_TYPE.get(e.get("type"))
        if etype is None:
            continue
        _route_effect(recorder, gate, actor, inv, ws, etype, e, res)

    _record_conclusion(recorder, gate, actor, inv, ws, res)
    recorder.close(res.terminal_state if res.terminal_state in
                   ("answered", "blocked", "declined") else "completed")
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
        "terminal_state": res.terminal_state, "summary": res.summary}}
    verdict = submit_effect(eff, actor, gate=gate)
    disp = "realized" if verdict.proceed else (
        "rejected_by_gate" if verdict.stopped_by == "gate" else "rejected_by_capability")
    recorder.proposed_effect(inv, effect_type=4,
                             payload_ref=f"conclude:{res.terminal_state}",
                             disposition=disp)
    if verdict.proceed:
        recorder.realized_effect(inv, effect_type=4, envelope=eff["envelope"],
                                 outcome="realized", result_ref="conclusion recorded")
