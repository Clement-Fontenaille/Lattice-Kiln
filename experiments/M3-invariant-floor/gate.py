"""M3 enforcement gate - deny-list form (v0).

Implements docs/10-technical/04-enforcement-gate.md against the provisional
invariant list in docs/10-technical/05-provisional-invariant-list.md
(machine form: invariants.json).

Properties the spec makes normative and this module holds to:
  - deterministic: a pure function of (effect, loaded invariants). No model
    call, no clock, no randomness, no role dependence.
  - refuse-only: the gate never grants, widens, or realizes.
  - fail closed: anything it cannot evaluate -> refuse.
  - the sequence check is a wired-in stub (always passes) so callers are hooked
    up now; hardening is deferred (Milestone 9 / 07-invariant-enforcement).

Stdlib only.
"""
from __future__ import annotations

import fnmatch
import json
import posixpath
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
DEFAULT_INVARIANTS = HERE / "invariants.json"

# clause evaluation order is fixed (determinism); first match wins
_HARD_ORDER = ["H1", "H2", "H3", "H4", "H5", "H6", "H7"]


class GateError(RuntimeError):
    """Raised only for programmer error (bad construction). Effect-evaluation
    problems become a `refuse` decision, never an exception, never a pass."""


@dataclass
class GateDecision:
    outcome: str            # "pass" | "refuse"
    clause: str | None = None
    reason: str = ""

    @property
    def passed(self) -> bool:
        return self.outcome == "pass"

    @property
    def refused(self) -> bool:
        return self.outcome == "refuse"


def _norm(p: str) -> str:
    return posixpath.normpath((p or "").replace("\\", "/"))


def _within(path: str, root: str) -> bool:
    if not root:
        return False
    p, r = _norm(path), _norm(root).rstrip("/")
    return p == r or p.startswith(r + "/")


def _glob_any(path: str, globs: list[str]) -> bool:
    p = _norm(path)
    return any(fnmatch.fnmatch(p, g) or fnmatch.fnmatch(p, g.lstrip("*/")) for g in globs)


class Gate:
    def __init__(self, invariants_path: str | Path = DEFAULT_INVARIANTS):
        self.path = Path(invariants_path)
        try:
            self.inv = json.loads(self.path.read_text(encoding="utf-8"))
        except OSError as e:
            # spec: unreadable invariant list -> refuse everything, do not
            # fall back to a permissive default.
            self.inv = None
            self._load_error = str(e)
        else:
            self._load_error = None
            if self.inv.get("schema") != "m3-invariants/0":
                self.inv = None
                self._load_error = f"unexpected schema in {self.path}"
        self._compiled = None
        if self.inv is not None:
            self._compiled = [re.compile(p) for p in
                              self.inv["denylists"]["destructive_command_patterns"]]

    # -- public API ---------------------------------------------------------
    def check(self, effect: dict[str, Any], actor: Any = None) -> GateDecision:
        """Single-effect check against the deny-list. `actor` is accepted for a
        uniform call signature but MUST NOT affect the decision (the gate binds
        effects, not roles)."""
        if self.inv is None:
            return GateDecision("refuse", "LOAD", f"invariant list unavailable: {self._load_error}")
        try:
            et = effect["effect_type"]
        except (TypeError, KeyError):
            return GateDecision("refuse", "MALFORMED", "effect has no effect_type")
        if et not in range(1, 10):
            return GateDecision("refuse", "MALFORMED", f"effect_type {et!r} outside 1..9")

        env = effect.get("envelope") or {}

        # resource ceilings that are per-effect (R1, R2 on a type-6 invocation)
        if et == 6:
            r = self._check_invocation_ceilings(env)
            if r.refused:
                return r

        for cid in _HARD_ORDER:
            d = self._match_hard(cid, et, effect, env)
            if d is not None:
                return d
        return GateDecision("pass")

    def check_sequence(self, history: list[dict[str, Any]],
                       proposed_effect: dict[str, Any]) -> GateDecision:
        """STUB (v0). Always passes. Wired so callers depend on it now; turning
        sequence evaluation on later is a body change here, not a call-site
        change everywhere. Window/grouping/pattern semantics are an open
        contract owned by 07-invariant-enforcement.md."""
        _ = (history, proposed_effect)
        return GateDecision("pass", None, "sequence check not yet implemented (v0 stub)")

    def check_run_bounds(self, effects_realized: int, minutes_elapsed: float) -> GateDecision:
        """R3 - a run must stop for human review past N effects or T minutes.
        Values are provisional (open contract); the default here is a placeholder."""
        r3 = next(c for c in self.inv["resource_ceilings"] if c["id"] == "R3")
        lim = r3.get("value") or r3.get("provisional_default", {})
        n, t = lim.get("max_effects"), lim.get("max_minutes")
        if n is not None and effects_realized >= n:
            return GateDecision("refuse", "R3", f"run hit effect ceiling ({effects_realized} >= {n})")
        if t is not None and minutes_elapsed >= t:
            return GateDecision("refuse", "R3", f"run hit time ceiling ({minutes_elapsed:.1f}m >= {t}m)")
        return GateDecision("pass")

    # -- internals --------------------------------------------------------
    def _check_invocation_ceilings(self, env: dict[str, Any]) -> GateDecision:
        if env.get("over_resident_envelope") is True:
            return GateDecision("refuse", "R1",
                                "model/quant/context exceeds resident VRAM envelope")
        r2 = next(c for c in self.inv["resource_ceilings"] if c["id"] == "R2")
        if int(env.get("concurrent_invocations", 1)) > int(r2["value"]):
            return GateDecision("refuse", "R2",
                                f"would exceed concurrency ceiling ({r2['value']})")
        return GateDecision("pass")

    def _match_hard(self, cid: str, et: int, effect: dict, env: dict) -> GateDecision | None:
        clause = next(c for c in self.inv["hard_constraints"] if c["id"] == cid)
        if et not in clause["effect_types"]:
            return None
        rule = clause["match_rule"]
        allow = self.inv["allowlists"]
        deny = self.inv["denylists"]
        tgt = env.get("target_path", "")
        op = (env.get("op") or "").lower()

        if rule == "path_outside_workspace":
            if not _within(tgt, env.get("workspace_root", "")):
                return GateDecision("refuse", cid, f"path '{tgt}' outside workspace root")

        elif rule == "host_not_in_allowlist":
            host = (env.get("host") or "").lower()
            if host not in {h.lower() for h in allow["network_hosts"]}:
                return GateDecision("refuse", cid, f"host '{host}' not on allowlist")

        elif rule == "targets_trusted_config_or_any_promotion":
            if et == 8:
                return GateDecision("refuse", cid, "no automated promotion before Milestone 11")
            if et == 7 and env.get("config_target") == "trusted":
                return GateDecision("refuse", cid, "type-7 may only produce a candidate")

        elif rule == "initiated_by_cognition":
            if (effect.get("initiated_by") or env.get("initiated_by") or "cognition") != "runtime":
                return GateDecision("refuse", cid,
                                    "capability change not initiated by the runtime")

        elif rule == "target_is_protected_path":
            if _glob_any(tgt, deny["protected_path_globs"]):
                return GateDecision("refuse", cid, f"'{tgt}' is a protected floor artifact")

        elif rule == "target_is_run_record":
            if _glob_any(tgt, deny["run_record_globs"]) and op in ("", "delete", "truncate", "rewrite", "modify"):
                return GateDecision("refuse", cid, f"'{tgt}' is an observability record")

        elif rule == "command_matches_denylist":
            cmd = env.get("command", "")
            for pat in self._compiled:
                if pat.search(cmd):
                    return GateDecision("refuse", cid, f"command matches destructive pattern /{pat.pattern}/")

        else:  # unknown rule in the file -> fail closed
            return GateDecision("refuse", cid, f"unrecognised match_rule '{rule}' (fail closed)")

        return None
