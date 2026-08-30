"""M5 orchestrator - an LLM loop that decides the next cognitive operation.

Implements docs/10-technical/08-orchestrator-contract.md against the M4 processor
runtime. Capability set {6 (processor_invocation), 4 (work-record mutation)} only:
it spawns processors and records decisions, it never touches the workspace
itself. Every spawned processor is independently gated. Every loop step leaves a
decision record so the strategy is reconstructable.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from _bridge import (CapabilitySet, DEFAULT_MODEL, Gate, assemble, generate,
                     run_processor, submit_effect, _extract)

MODEL_IDENTITY = {"name": "qwen2.5-coder", "quant": "Q4_K_M", "params_b": 7,
                  "runtime": "ollama", "offloaded": False}
ROLES = ("planner", "implementer", "reviewer")
MAX_STEPS = 6

ORCH_INSTRUCTIONS = """\
You are an orchestrator. You do NOT write code or run commands yourself. You
decide the single next step toward the objective: either spawn one processor, or
stop.

Processor roles you can spawn:
- planner     - produces a short plan; writes nothing.
- implementer - makes the actual code change.
- reviewer    - independently judges whether the objective is met; sees only the
                result, not the implementer's reasoning.

Decide based on the objective and what has happened so far. Typical shapes: go
straight to implementer for a simple change; planner first if it is unclear;
reviewer after an implementer; a second implementer if the reviewer said
NEEDS-CHANGE. Stop as soon as the objective is met, cannot be met (e.g. it rests
on a false premise), or no further step would help.
"""

CONTROL = """\
Reply with EXACTLY ONE control block:

<<<CONTROL>>>
{"next": "spawn" | "stop",
 "role": "planner" | "implementer" | "reviewer",
 "step_objective": "one or two sentences telling the processor what to do",
 "rationale": "one sentence: why this is the useful next step",
 "terminal_state": "resolved" | "blocked" | "abandoned"}
<<<ENDCONTROL>>>

- "role" and "step_objective" are required when next = "spawn".
- "terminal_state" is required when next = "stop".
- Keep it short. Valid JSON only.
"""


@dataclass
class Step:
    n: int
    op: str                      # "spawn" | "stop"
    role: str | None
    step_objective: str | None
    rationale: str
    processor_terminal_state: str | None = None
    processor_summary: str = ""
    processor_verdict: str | None = None
    files_written: list[str] = field(default_factory=list)


@dataclass
class OrchestratorResult:
    invocation_id: str
    terminal_state: str
    final_summary: str
    steps: list[Step] = field(default_factory=list)
    model_calls: int = 0
    files_written: list[str] = field(default_factory=list)
    wall_s: float = 0.0

    @property
    def processor_calls(self) -> int:
        return sum(1 for s in self.steps if s.op == "spawn")


def _progress_text(steps: list[Step]) -> str:
    if not steps:
        return "(nothing yet)"
    out = []
    for s in steps:
        if s.op == "spawn":
            v = f" verdict={s.processor_verdict}" if s.processor_verdict else ""
            out.append(f"step {s.n}: spawned {s.role} -> {s.processor_terminal_state}{v}: "
                       f"{s.processor_summary[:160]}")
        else:
            out.append(f"step {s.n}: stop ({s.rationale})")
    return "\n".join(out)


def run_orchestrated(*, objective: str, workspace_root: str | Path, recorder, gate: Gate,
                     parent_invocation_id: str | None = None, intent_ref: str | None = None,
                     max_steps: int = MAX_STEPS, model: str = DEFAULT_MODEL) -> OrchestratorResult:
    ws = Path(workspace_root).resolve()
    actor = CapabilitySet(role="orchestrator", grants={6: {"roles": list(ROLES)}, 4: {}})
    t0 = time.monotonic()

    inv = recorder.invocation(
        role="orchestrator", model_identity=dict(MODEL_IDENTITY),
        parent_invocation_id=parent_invocation_id, intent_ref=intent_ref,
        context_ref="orchestrator", config_ref="m5-baseline")

    res = OrchestratorResult(invocation_id=inv, terminal_state="blocked", final_summary="")
    last_impl_summary = ""

    for n in range(1, max_steps + 1):
        bundle = assemble(objective, ws, token_budget=6000)
        prompt = "\n".join([
            ORCH_INSTRUCTIONS.strip(), "",
            "# OBJECTIVE", objective, "",
            "# PROGRESS SO FAR", _progress_text(res.steps), "",
            "# REPO CONTEXT", bundle.render(), "",
            CONTROL])
        gen = generate(prompt, model=model)
        res.model_calls += 1
        parsed = _extract(gen.text)
        ctrl = parsed["control"] if parsed else {}

        op = str(ctrl.get("next", "stop")).lower()
        role = ctrl.get("role") if ctrl.get("role") in ROLES else None
        step_obj = str(ctrl.get("step_objective", "")).strip() or objective
        rationale = str(ctrl.get("rationale", "")).strip() or "(no rationale given)"
        step = Step(n=n, op=op, role=role, step_objective=step_obj, rationale=rationale)

        # decision record - a work-record mutation, routed through the floor
        dec_eff = {"effect_type": 4, "envelope": {
            "representable": True, "attributable": inv, "reversible": "work-record",
            "kind": "orchestrator_decision", "step": n, "op": op, "role": role,
            "step_objective": step_obj, "rationale": rationale,
            "observation": _progress_text(res.steps)[-600:]}}
        v = submit_effect(dec_eff, actor, gate=gate)
        recorder.proposed_effect(inv, effect_type=4, payload_ref=f"decide:step{n}:{op}",
                                 disposition="realized" if v.proceed else "rejected_by_gate")
        if v.proceed:
            recorder.realized_effect(inv, effect_type=4, envelope=dec_eff["envelope"],
                                     outcome="realized", result_ref=f"step{n}")

        if op != "spawn" or role is None:
            res.terminal_state = str(ctrl.get("terminal_state", "blocked"))
            res.final_summary = rationale
            res.steps.append(step)
            break

        # spawn the processor - a type-6 effect, then the M4 runtime
        inv_eff = {"effect_type": 6, "envelope": {
            "representable": True, "attributable": inv, "reversible": "n/a",
            "child_role": role, "concurrent_invocations": 1}}
        sv = submit_effect(inv_eff, actor, gate=gate)
        recorder.proposed_effect(inv, effect_type=6, payload_ref=f"spawn:{role}",
                                 disposition="realized" if sv.proceed else "rejected_by_capability")
        if not sv.proceed:
            step.rationale += f" [spawn refused: {sv.reason}]"
            res.steps.append(step)
            continue

        extra = None
        if role == "reviewer":
            extra = ("IMPLEMENTER'S STATED CONCLUSION:\n" + last_impl_summary
                     + "\n\nFILES WRITTEN SO FAR:\n" + ", ".join(res.files_written or ["(none)"]))
        pr = run_processor(role=role, objective=step_obj, context=bundle, workspace_root=ws,
                           recorder=recorder, gate=gate, parent_invocation_id=inv,
                           intent_ref=intent_ref,
                           interaction_mode="review" if role == "reviewer" else "oneshot",
                           extra_input=extra, model=model)
        res.model_calls += 1  # the processor's own model call (retries are rare, ignored)
        step.processor_terminal_state = pr.terminal_state
        step.processor_summary = pr.summary
        step.processor_verdict = pr.control.get("verdict") if role == "reviewer" else None
        step.files_written = list(pr.files_written)
        for f in pr.files_written:
            if f not in res.files_written:
                res.files_written.append(f)
        if role == "implementer":
            last_impl_summary = pr.summary
        if pr.terminal_state == "declined":
            res.terminal_state = "abandoned"
            res.final_summary = f"processor declined: {pr.summary}"
            res.steps.append(step)
            break
        res.steps.append(step)
    else:
        res.terminal_state = "blocked"
        res.final_summary = f"hit step budget ({max_steps}) without resolving"

    # closing decision record
    recorder.realized_effect(inv, effect_type=4, envelope={
        "representable": True, "attributable": inv, "reversible": "work-record",
        "kind": "orchestrator_synthesis", "terminal_state": res.terminal_state,
        "summary": res.final_summary, "steps": len(res.steps),
        "processor_calls": res.processor_calls},
        outcome="realized", result_ref="synthesis")

    res.wall_s = round(time.monotonic() - t0, 1)
    return res
