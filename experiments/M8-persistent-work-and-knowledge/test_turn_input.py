"""M9 packages 1-2, landed in M8: does `recall()` actually produce and persist
a kind-5 turn-input record, per 02-observability-event-model.md's MUST list?

"Two policies over the same live set choose different subsets, and that
comparability is a MEASUREMENT only if what each presented was recorded" --
this is the package everything else in M9 rests on, and it was never exercised
before this file (recall() had no test at all prior to this pass).

    python test_turn_input.py
"""
from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from context_manager import ContextManager, GENERATION_CONCLUSION, READ, RETRIEVAL
from knowledge_model import KnowledgeStore
from wiring import Substrate
from work_record import WorkRecordStore


def build(root: Path) -> Substrate:
    return Substrate(WorkRecordStore(root / "work"),
                     KnowledgeStore(root / "knowledge"),
                     ContextManager(root / "context"))


def main():
    tmp = Path(tempfile.mkdtemp(prefix="m9_turninput_"))
    try:
        sub = build(tmp)
        ctx = sub.context

        task = sub.create_task(intent_content="Fix the paginate() off-by-one.",
                               formulation="fix it", scope_boundary="page.py",
                               scope_derivation="named", invocation_id="inv0")
        wid = task.work_item_id

        # --- turn 1: the naive policy, nothing dropped yet (small live set,
        # generous budget)
        rec1 = ctx.recall(wid, invocation_id="inv1", turn_budget=8000)
        assert rec1.turn_index == 1, f"FAIL: expected turn_index 1, got {rec1.turn_index}"
        assert rec1.dropped == [], "FAIL: nothing should be dropped with a generous budget"
        assert all(isinstance(x, tuple) and len(x) == 2 for x in rec1.included), (
            "FAIL: included entries must carry (live_set_id, crossing_type), not just an id")
        print(f"[ok] turn 1: turn_index=1, {len(rec1.included)} entries included "
             f"each with its crossing type, nothing dropped")

        # --- MUST carry: policy_ref, isolation requested vs granted, prefix
        assert rec1.policy_ref == "naive-degenerate-v1"
        assert rec1.isolation_requested == "share_nothing"
        assert rec1.isolation_granted == "share_nothing"
        assert rec1.continued_from is None
        print(f"[ok] policy_ref/isolation/continued_from all carried: "
             f"policy={rec1.policy_ref!r}, requested={rec1.isolation_requested!r}, "
             f"granted={rec1.isolation_granted!r}")

        # --- an isolation preference other than the default is passed through,
        # not silently normalised to share_nothing
        rec_iso = ctx.recall(wid, invocation_id="inv_iso",
                             isolation_requested="share_base")
        assert rec_iso.isolation_requested == "share_base"
        assert rec_iso.isolation_granted == "share_base", (
            "FAIL: the naive policy claims to never degrade -- if granted differs "
            "from requested here, stub_isolation's honesty claim is false")
        assert rec_iso.stub_isolation is True, (
            "FAIL: stub_isolation must stay True -- this policy cannot actually "
            "arbitrate under capacity pressure, and must not claim it can")
        print("[ok] isolation_requested is passed through untouched, and the "
             "record is honest that granting it is not real arbitration "
             "(stub_isolation=True)")

        # --- attach enough unlabelled material to force a real drop, and
        # confirm truncation is recorded, not silently absorbed
        for i in range(30):
            sub.attach(wid, {"kind": "note", "i": i, "text": "x" * 40},
                      source="worker", crossing_type=READ, invocation_id="inv2")
        rec2 = ctx.recall(wid, invocation_id="inv3", turn_budget=500,
                          approx_tokens_per_entry=200)
        assert rec2.turn_index == 3, f"FAIL: expected turn_index 3, got {rec2.turn_index}"
        assert rec2.dropped, "FAIL: a tight budget over 30+ entries must drop something"
        assert rec2.truncated is True
        # the three labelled entries from task creation (intent/objective/scope)
        # must never appear in dropped, whatever the budget does
        labelled_ids = {e.live_set_id for e in ctx.live_set(wid) if e.label}
        assert not (labelled_ids & set(rec2.dropped)), (
            "FAIL: a labelled entry (objective/derived_scope) was dropped under "
            "budget pressure -- 14-context-manager.md: never drop those")
        print(f"[ok] turn 3: budget pressure produced {len(rec2.dropped)} drops "
             f"and truncated=True; labelled entries were never among them")

        # --- persistence: turn_inputs() reads back exactly what was recorded,
        # across all three turns, in order -- this is what makes two policies
        # COMPARABLE rather than just individually plausible
        history = ctx.turn_inputs(wid)
        assert [r.turn_index for r in history] == [1, 2, 3], (
            f"FAIL: turn history out of order or incomplete: "
            f"{[r.turn_index for r in history]}")
        assert history[2].dropped == rec2.dropped
        print(f"[ok] turn_inputs({wid[:10]}) replays all {len(history)} turns "
             f"in order from the durable log, matching what recall() returned "
             f"live -- the record survives past the in-memory return value")

        print()
        print("ALL TURN-INPUT CHECKS PASSED")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
