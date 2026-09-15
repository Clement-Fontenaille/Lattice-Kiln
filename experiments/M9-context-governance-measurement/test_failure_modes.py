"""Package 3: do the four failure-mode detectors behave the way the milestone
says each of them can -- two real and mechanical, two honest stubs?

    python test_failure_modes.py
"""
from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent /
                      "M8-persistent-work-and-knowledge"))

from context_manager import ContextManager, READ  # noqa: E402
from knowledge_model import EVIDENCE, KnowledgeStore  # noqa: E402
from wiring import Substrate  # noqa: E402
from work_record import WorkRecordStore  # noqa: E402

from failure_modes import (NOT_REDUNDANT, UNASSESSED, check_insufficiency_visible,  # noqa: E402
                          check_overload, check_redundancy, check_uselessness,
                          overload_rate)


def build(root: Path) -> Substrate:
    return Substrate(WorkRecordStore(root / "work"),
                     KnowledgeStore(root / "knowledge"),
                     ContextManager(root / "context"))


def main():
    tmp = Path(tempfile.mkdtemp(prefix="m9_failuremodes_"))
    try:
        sub = build(tmp)
        ctx = sub.context

        task = sub.create_task(intent_content="Analyse the module.",
                               formulation="find the bug", scope_boundary="mod.py",
                               scope_derivation="named", invocation_id="inv0")
        wid = task.work_item_id

        # --- OVERLOAD: real, mechanical, content-agnostic
        rec_light = ctx.recall(wid, invocation_id="inv1", turn_budget=8000)
        v_light = check_overload(rec_light)
        assert v_light.occurred is False and v_light.dropped_count == 0
        print(f"[ok] overload: light turn (turn {v_light.turn_index}) -> "
             f"occurred=False, matching truncated=False on the record")

        for i in range(20):
            sub.attach(wid, {"kind": "note", "i": i, "text": "y" * 40},
                      source="worker", crossing_type=READ, invocation_id="inv2")
        rec_heavy = ctx.recall(wid, invocation_id="inv3", turn_budget=400,
                               approx_tokens_per_entry=200)
        v_heavy = check_overload(rec_heavy)
        assert v_heavy.occurred is True and v_heavy.dropped_count > 0
        print(f"[ok] overload: heavy turn (turn {v_heavy.turn_index}) -> "
             f"occurred=True, {v_heavy.dropped_count} dropped -- read only "
             f"truncated/dropped, never opened `content`")

        rate = overload_rate(ctx.turn_inputs(wid))
        assert 0.0 < rate <= 1.0
        print(f"[ok] overload_rate across the task's {len(ctx.turn_inputs(wid))} "
             f"turns so far: {rate:.2f}")

        # --- INSUFFICIENCY (visible half): real, mechanical, partial by
        # the milestone's own account
        v_insuf = check_insufficiency_visible(ctx.live_set(wid), ctx.turn_inputs(wid), wid)
        assert v_insuf.never_recalled, (
            "FAIL: with 20 attachments and a 400-token budget, something must "
            "have been registered but never included in any turn")
        assert "invisible from this store" in v_insuf.blind_spot
        print(f"[ok] insufficiency (visible half): {len(v_insuf.never_recalled)} "
             f"live entries were registered but never once presented across "
             f"{len(ctx.turn_inputs(wid))} turns; blind_spot documents the "
             f"invisible half rather than pretending it was checked")

        # --- REDUNDANCY: honest stub, UNASSESSED not NOT_REDUNDANT
        v_red = check_redundancy({"text": "the bug is a race condition"},
                                 [{"text": "the bug is a race condition, confirmed"}])
        assert v_red.verdict == UNASSESSED and v_red.stub is True
        print(f"[ok] redundancy stub returns UNASSESSED (never claims "
             f"NOT_REDUNDANT) even when the candidate obviously overlaps a "
             f"live artifact in substance")

        # --- an injected real checker CAN return NOT_REDUNDANT
        def real_redundancy(candidate, live):
            return (NOT_REDUNDANT, "no live artifact shares this candidate's coverage")
        v_red2 = check_redundancy({"text": "unrelated"}, [], checker=real_redundancy)
        assert v_red2.verdict == NOT_REDUNDANT and v_red2.stub is False
        print("[ok] an injected real checker can return a clean verdict; the "
             "seam does not hard-code UNASSESSED, only the default does")

        # --- USELESSNESS: same discipline
        v_use = check_uselessness({"text": "irrelevant tangent"}, "find the bug")
        assert v_use.verdict == UNASSESSED and v_use.stub is True
        print("[ok] uselessness stub returns UNASSESSED, never NEEDED, "
             "even for content that looks obviously off-topic")

        print()
        print("ALL FAILURE-MODE CHECKS PASSED")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
