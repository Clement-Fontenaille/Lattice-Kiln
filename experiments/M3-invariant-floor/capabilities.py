"""M3 capability and authority model - static-grant MVP form.

Implements docs/10-technical/03-capability-authority-model.md: an actor may
*request* an effect only if it holds a grant for that effect type whose
constraints the request satisfies. Fails closed. Sits above the gate; passing
this is not evidence of passing the gate (that is gate.py).

Stdlib only.
"""
from __future__ import annotations

import posixpath
from dataclasses import dataclass, field
from typing import Any

# Effect type ids from docs/10-technical/01-effect-vocabulary.md
EFFECT_TYPES = {
    1: "workspace_mutation", 2: "process_execution", 3: "network_access",
    4: "work_record_mutation", 5: "memory_mutation", 6: "processor_invocation",
    7: "configuration_mutation", 8: "promotion", 9: "capability_grant_revocation",
}


class CapabilityError(RuntimeError):
    """Raised on a malformed request - never swallowed, never treated as permit."""


@dataclass
class CapabilityDecision:
    permit: bool
    reason: str

    def __bool__(self) -> bool:  # truthy == permitted
        return self.permit


@dataclass
class CapabilitySet:
    """grants: {effect_type -> constraints dict}. An absent type means the actor
    may not request it. An empty set may request nothing."""
    role: str
    grants: dict[int, dict[str, Any]] = field(default_factory=dict)
    revoked: bool = False

    def revoke(self) -> None:
        """Immediate, unilateral - no proposal, no evaluation, no wait.
        (docs/10-technical/03 Authority; 07-invariant-enforcement decommissioning)"""
        self.grants = {}
        self.revoked = True


def _norm(path: str) -> str:
    return posixpath.normpath(path.replace("\\", "/"))


def _within(path: str, root: str) -> bool:
    if not root:
        return False  # unresolvable constraint -> fail closed
    p, r = _norm(path), _norm(root).rstrip("/")
    return p == r or p.startswith(r + "/")


# ---- MVP seed grants (authored here as the human-operator seed config) --------
# docs/10-technical/03 - illustrative; the constraint vocabulary is an open contract.
def default_capability_sets() -> dict[str, CapabilitySet]:
    return {
        "orchestrator": CapabilitySet("orchestrator", {
            6: {"max_concurrent": 1, "roles": ["implementer", "reviewer"]},
            4: {},
        }),
        "implementer": CapabilitySet("implementer", {
            1: {"path_within": "<workspace_root>"},
            2: {"command_allowlist": ["build", "test", "lint", "fmt", "pytest"]},
            4: {},
        }),
        "reviewer": CapabilitySet("reviewer", {}),  # reads only
        # a role that is allowed to reach package registries, for gate tests
        "fetcher": CapabilitySet("fetcher", {
            3: {"destination_class": "registry"},
        }),
    }


def authorize(actor: CapabilitySet, effect: dict[str, Any]) -> CapabilityDecision:
    """Decide whether `actor` may request `effect`. Fails closed on anything
    malformed or unresolvable."""
    if not isinstance(effect, dict):
        raise CapabilityError("effect must be a dict")
    et = effect.get("effect_type")
    if et not in EFFECT_TYPES:
        raise CapabilityError(f"unknown effect_type: {et!r}")

    if actor.revoked or not actor.grants:
        return CapabilityDecision(False, f"actor '{actor.role}' holds no capabilities (fail closed)")
    if et not in actor.grants:
        return CapabilityDecision(False, f"no grant for {EFFECT_TYPES[et]} (type {et})")

    c = actor.grants[et]
    env = effect.get("envelope", {}) or {}

    if et == 1:  # workspace_mutation
        want = c.get("path_within")
        if want is not None:
            root = env.get("workspace_root") if want == "<workspace_root>" else want
            if not _within(env.get("target_path", ""), root or ""):
                return CapabilityDecision(False, "target_path not within granted workspace root")
    elif et == 2:  # process_execution
        allow = c.get("command_allowlist")
        if allow is not None:
            head = (env.get("command", "").strip().split() or [""])[0]
            base = head.rsplit("/", 1)[-1]
            if base not in allow:
                return CapabilityDecision(False, f"command '{base}' not in allowlist")
    elif et == 3:  # network_access
        dc = c.get("destination_class")
        if dc is not None and env.get("destination_class") not in (dc, None):
            return CapabilityDecision(False, f"destination_class != granted '{dc}'")
    elif et == 6:  # processor_invocation
        mx = c.get("max_concurrent")
        if mx is not None and int(env.get("concurrent_invocations", 1)) > mx:
            return CapabilityDecision(False, f"would exceed max_concurrent={mx}")
        roles = c.get("roles")
        if roles is not None and env.get("child_role") not in (None, *roles):
            return CapabilityDecision(False, f"child_role not in granted set {roles}")

    return CapabilityDecision(True, f"granted {EFFECT_TYPES[et]}")
