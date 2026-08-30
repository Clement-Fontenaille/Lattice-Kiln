"""M3 - the 'an effect must pass every layer' pipeline.

docs/10-technical/04-enforcement-gate.md, "Position and order":

    representability (runtime)  ->  capability  ->  gate.check  ->  gate.check_sequence

Passing an earlier layer is not evidence of passing a later one. The first layer
to stop the effect is reported. Nothing here realizes an effect - a `proceed`
verdict means the runtime *may* realize it.
"""
from __future__ import annotations

import posixpath
from dataclasses import dataclass
from typing import Any

from capabilities import CapabilityError, CapabilitySet, authorize
from gate import Gate

_LAYERS = ("representability", "capability", "gate", "sequence")


@dataclass
class Verdict:
    proceed: bool
    stopped_by: str | None      # one of _LAYERS, or None when proceed
    clause: str | None
    reason: str

    def __bool__(self) -> bool:
        return self.proceed


def _norm(p: str) -> str:
    return posixpath.normpath((p or "").replace("\\", "/"))


def _representable(effect: dict[str, Any]) -> tuple[bool, str]:
    """The runtime's own pre-check (05-runtime.md): reject the non-representable
    *before* the gate is consulted. Deliberately overlaps invariant H1 - the
    gate re-checks the workspace boundary so a bug here cannot open it."""
    et = effect.get("effect_type")
    env = effect.get("envelope") or {}
    if et == 1:
        root, tgt = env.get("workspace_root", ""), env.get("target_path", "")
        if not root:
            return False, "no assigned workspace root to resolve against"
        r = _norm(root).rstrip("/")
        p = _norm(tgt)
        if not (p == r or p.startswith(r + "/")):
            return False, f"workspace mutation targets '{tgt}' outside assigned workspace"
    return True, ""


def submit_effect(effect: dict[str, Any], actor: CapabilitySet,
                  gate: Gate | None = None,
                  history: list[dict[str, Any]] | None = None) -> Verdict:
    gate = gate or Gate()

    ok, why = _representable(effect)
    if not ok:
        return Verdict(False, "representability", None, why)

    try:
        cap = authorize(actor, effect)
    except CapabilityError as e:
        return Verdict(False, "capability", None, f"malformed request: {e}")
    if not cap.permit:
        return Verdict(False, "capability", None, cap.reason)

    g = gate.check(effect, actor=actor)
    if g.refused:
        return Verdict(False, "gate", g.clause, g.reason)

    s = gate.check_sequence(history or [], effect)
    if s.refused:
        return Verdict(False, "sequence", s.clause, s.reason)

    return Verdict(True, None, None, "all layers passed")
