"""M2 observability event model - minimal append-only recorder.

Implements the v0 contract in docs/10-technical/02-observability-event-model.md:
four mandatory event kinds (invocation, realized_effect, safety_intervention,
proposed_effect) plus human_correction, written one-JSON-object-per-line to
runs/<run_id>/events.jsonl with a per-run monotonic sequence number.

Stdlib only. Illustrative storage shape - the RunRecorder / reader split is the
seam where a different store would be swapped in.
"""
from __future__ import annotations

import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_RUN = "m2-run/0"
SCHEMA_EVENT = "m2-event/0"

# Effect type ids from docs/10-technical/01-effect-vocabulary.md
EFFECT_TYPES = {
    1: "workspace_mutation",
    2: "process_execution",
    3: "network_access",
    4: "work_record_mutation",
    5: "memory_mutation",
    6: "processor_invocation",
    7: "configuration_mutation",
    8: "promotion",
    9: "capability_grant_revocation",
}

EVENT_KINDS = (
    "invocation",
    "proposed_effect",
    "realized_effect",
    "safety_intervention",
    "human_correction",
)

SAFETY_KINDS = ("gate_refusal", "gate_alter", "decommission", "accumulation_stop")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sid(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


class RecorderError(RuntimeError):
    """Raised when the recorder cannot record - never swallowed (contract:
    a silent gap is a specification defect)."""


class RunRecorder:
    def __init__(self, runs_dir: str | os.PathLike, run_id: str | None = None,
                 intent_text: str | None = None, meta: dict[str, Any] | None = None):
        self.run_id = run_id or _sid("run")
        self.dir = Path(runs_dir) / self.run_id
        self.dir.mkdir(parents=True, exist_ok=True)
        self.events_path = self.dir / "events.jsonl"
        self._seq = 0
        self._fh = open(self.events_path, "a", encoding="utf-8")
        self._header = {
            "schema": SCHEMA_RUN,
            "run_id": self.run_id,
            "started": _now_iso(),
            "intent_text": intent_text,
            "meta": meta or {},
        }
        self._write_header()

    def _write_header(self) -> None:
        try:
            self.dir.mkdir(parents=True, exist_ok=True)
            (self.dir / "run.json").write_text(json.dumps(self._header, indent=2), encoding="utf-8")
        except OSError as e:
            # the events.jsonl is the source of truth and is already durable;
            # a lost header is recoverable (reconstruct.Run synthesises one).
            print(f"WARN RunRecorder: could not write {self.dir/'run.json'}: {e}", file=sys.stderr)

    # -- low level ---------------------------------------------------------
    def _emit(self, kind: str, body: dict[str, Any]) -> dict[str, Any]:
        if kind not in EVENT_KINDS:
            raise RecorderError(f"unknown event kind: {kind}")
        self._seq += 1
        rec = {
            "schema": SCHEMA_EVENT,
            "run_id": self.run_id,
            "seq": self._seq,
            "ts": _now_iso(),
            "kind": kind,
            **body,
        }
        try:
            self._fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            self._fh.flush()
            os.fsync(self._fh.fileno())
        except OSError as e:  # a gap must be loud, not hidden
            raise RecorderError(f"failed to write {kind} event: {e}") from e
        return rec

    # -- kind 1: invocation record --------------------------------------
    def invocation(self, role: str, model_identity: dict[str, Any],
                   parent_invocation_id: str | None = None,
                   intent_ref: str | None = None,
                   context_ref: str | None = None,
                   config_ref: str | None = None) -> str:
        """model_identity carries name, quant and - per M0 findings-log entry 1 -
        whether inference was offloaded from GPU (predicts latency 10-20x)."""
        inv_id = _sid("inv")
        self._emit("invocation", {
            "invocation_id": inv_id,
            "parent_invocation_id": parent_invocation_id,
            "intent_ref": intent_ref,
            "role": role,
            "model_identity": model_identity,
            "context_ref": context_ref,
            "config_ref": config_ref,
        })
        return inv_id

    # -- kind 4: proposed-effect / decision record ---------------------
    def proposed_effect(self, invocation_id: str, effect_type: int,
                        payload_ref: str, disposition: str,
                        links: dict[str, str] | None = None) -> str:
        """disposition in: realized | rejected_by_capability | rejected_by_gate.
        links may carry effect_id / intervention_id of the resulting record."""
        if effect_type not in EFFECT_TYPES:
            raise RecorderError(f"unknown effect_type {effect_type}")
        pe_id = _sid("pe")
        self._emit("proposed_effect", {
            "proposed_effect_id": pe_id,
            "invocation_id": invocation_id,
            "effect_type": effect_type,
            "effect_type_name": EFFECT_TYPES[effect_type],
            "payload_ref": payload_ref,
            "disposition": disposition,
            "links": links or {},
        })
        return pe_id

    # -- kind 2: realized-effect record -------------------------------
    def realized_effect(self, invocation_id: str, effect_type: int,
                        envelope: dict[str, Any], outcome: str,
                        result_ref: str | None = None) -> str:
        """envelope carries enough to later judge the effect representable,
        permitted, attributable, reversible (carrier is an open contract).
        outcome in: realized | failed | safety_intervened."""
        if effect_type not in EFFECT_TYPES:
            raise RecorderError(f"unknown effect_type {effect_type}")
        eff_id = _sid("eff")
        self._emit("realized_effect", {
            "effect_id": eff_id,
            "invocation_id": invocation_id,
            "effect_type": effect_type,
            "effect_type_name": EFFECT_TYPES[effect_type],
            "envelope": envelope,
            "outcome": outcome,
            "result_ref": result_ref,
        })
        return eff_id

    # -- kind 3: safety-intervention outcome -------------------------
    def safety_intervention(self, kind: str, disposition: str,
                            on_invocation_id: str | None = None,
                            on_effect_id: str | None = None,
                            note: str = "") -> str:
        """kind in SAFETY_KINDS. disposition in:
        logged_and_proceeded | escalated | halted.
        Always retry_eligible=False: not eligible for automatic retry without
        recorded human review."""
        if kind not in SAFETY_KINDS:
            raise RecorderError(f"unknown safety kind: {kind}")
        iv_id = _sid("iv")
        self._emit("safety_intervention", {
            "intervention_id": iv_id,
            "safety_kind": kind,
            "on_invocation_id": on_invocation_id,
            "on_effect_id": on_effect_id,
            "disposition": disposition,
            "retry_eligible": False,
            "human_review_ref": None,
            "note": note,
        })
        return iv_id

    # -- kind 5: human correction (open contract - minimal) ---------
    def human_correction(self, target_ref: str, kind: str, detail: str) -> str:
        hc_id = _sid("hc")
        self._emit("human_correction", {
            "human_correction_id": hc_id,
            "target_ref": target_ref,
            "correction_kind": kind,
            "detail": detail,
        })
        return hc_id

    # -- lifecycle -------------------------------------------------------
    def close(self, outcome: str = "completed") -> None:
        if not self._fh.closed:
            self._fh.close()
        # update the in-memory header and rewrite - no disk round-trip, so a
        # missing/renamed run.json cannot lose a complete events.jsonl
        # (M5 surfaced this: close() used to json.loads the file back).
        self._header["ended"] = _now_iso()
        self._header["outcome"] = outcome
        self._header["event_count"] = self._seq
        self._write_header()

    def __enter__(self) -> "RunRecorder":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close("error" if exc_type else "completed")
