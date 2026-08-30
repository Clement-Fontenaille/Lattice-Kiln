"""M2 - read a recorded run and answer reconstruction questions.

The point of the milestone: a question nobody designed the schema for should be
answerable from the stored records alone. This module provides the primitive
queries the contract requires (per-actor ordered history, per-intent lineage,
safety interventions) plus a demo of an unplanned question.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Iterable


class Run:
    def __init__(self, run_dir: str | Path):
        self.dir = Path(run_dir)
        try:
            self.header = json.loads((self.dir / "run.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            # a lost/partial header is recoverable - the events are the record
            self.header = {"run_id": self.dir.name, "meta": {}, "outcome": None,
                           "header_recovered": True}
        self.events: list[dict[str, Any]] = []
        with open(self.dir / "events.jsonl", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    self.events.append(json.loads(line))
        # contract: total order within a run is the per-run monotonic seq
        seqs = [e["seq"] for e in self.events]
        if seqs != sorted(seqs) or len(set(seqs)) != len(seqs):
            raise ValueError(f"{self.dir}: events are not a strict monotonic sequence")

    # -- primitives ----------------------------------------------------
    def of_kind(self, *kinds: str) -> list[dict[str, Any]]:
        return [e for e in self.events if e["kind"] in kinds]

    def invocations(self) -> list[dict[str, Any]]:
        return self.of_kind("invocation")

    def invocation(self, inv_id: str) -> dict[str, Any] | None:
        return next((e for e in self.events
                     if e["kind"] == "invocation" and e["invocation_id"] == inv_id), None)

    # -- per-actor ordered history (contract requirement) ------------
    def per_actor(self, invocation_id: str) -> list[dict[str, Any]]:
        """Ordered proposed_effect / realized_effect / safety_intervention
        records attributable to one invocation."""
        out = []
        for e in self.events:  # already seq-ordered
            if e["kind"] in ("proposed_effect", "realized_effect") and e.get("invocation_id") == invocation_id:
                out.append(e)
            elif e["kind"] == "safety_intervention" and e.get("on_invocation_id") == invocation_id:
                out.append(e)
        return out

    # -- per-intent lineage (contract requirement) ------------------
    def _children(self, inv_id: str) -> Iterable[dict[str, Any]]:
        return (e for e in self.invocations() if e.get("parent_invocation_id") == inv_id)

    def intent_lineage(self, root_invocation_id: str) -> list[str]:
        """All invocation ids in the parent/child tree rooted at one invocation."""
        acc, stack = [], [root_invocation_id]
        while stack:
            cur = stack.pop()
            if cur in acc:
                continue
            acc.append(cur)
            stack.extend(c["invocation_id"] for c in self._children(cur))
        return acc

    def per_intent(self, intent_ref: str) -> dict[str, Any]:
        roots = [e["invocation_id"] for e in self.invocations()
                 if e.get("intent_ref") == intent_ref and not e.get("parent_invocation_id")]
        inv_ids: list[str] = []
        for r in roots:
            for i in self.intent_lineage(r):
                if i not in inv_ids:
                    inv_ids.append(i)
        effects = [e for e in self.events
                   if e["kind"] in ("proposed_effect", "realized_effect")
                   and e.get("invocation_id") in inv_ids]
        return {"intent_ref": intent_ref, "invocation_ids": inv_ids, "effects": effects}

    # -- safety interventions (distinct category) ------------------
    def safety_interventions(self) -> list[dict[str, Any]]:
        return self.of_kind("safety_intervention")

    # -- unplanned-question demo -----------------------------------
    def unplanned_answer(self) -> dict[str, Any]:
        """A question the schema was not shaped around:
        'For every effect that was refused by the gate, which model served the
        proposing invocation, and was that inference offloaded from GPU?'
        Answerable purely by joining stored records - no field was added for it.
        """
        rows = []
        for iv in self.safety_interventions():
            if iv["safety_kind"] not in ("gate_refusal", "gate_alter"):
                continue
            inv = self.invocation(iv.get("on_invocation_id") or "")
            if not inv:
                # fall back: find the invocation via the refused proposed_effect
                pe = next((e for e in self.of_kind("proposed_effect")
                           if e.get("links", {}).get("intervention_id") == iv["intervention_id"]), None)
                inv = self.invocation(pe["invocation_id"]) if pe else None
            mi = (inv or {}).get("model_identity", {})
            rows.append({
                "intervention_id": iv["intervention_id"],
                "safety_kind": iv["safety_kind"],
                "role": (inv or {}).get("role"),
                "model": mi.get("name"),
                "quant": mi.get("quant"),
                "offloaded": mi.get("offloaded"),
                "retry_eligible": iv["retry_eligible"],
            })
        return {"question": "gate-refused effects -> serving model + offload flag", "rows": rows}


def summarise(run_dir: str | Path) -> None:
    r = Run(run_dir)
    print(f"run {r.header['run_id']}  outcome={r.header.get('outcome')}  events={len(r.events)}")
    for e in r.invocations():
        print(f"  inv {e['invocation_id']}  role={e['role']:<12} parent={e['parent_invocation_id']} "
              f"model={e['model_identity'].get('name')} offloaded={e['model_identity'].get('offloaded')}")
    for iv in r.safety_interventions():
        print(f"  !! {iv['safety_kind']} on {iv.get('on_invocation_id') or iv.get('on_effect_id')} "
              f"-> {iv['disposition']}  retry_eligible={iv['retry_eligible']}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: reconstruct.py <runs/<run_id>>")
        raise SystemExit(2)
    summarise(sys.argv[1])
