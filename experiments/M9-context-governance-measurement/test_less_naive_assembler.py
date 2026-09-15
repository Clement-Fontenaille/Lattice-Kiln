"""Package 6's falsification test: does a less-naive assembler actually move
the Insufficiency-visible metric against the same live set the naive baseline
leaves starved?

Two work items, same attachment pattern, same tight budget, same number of
turns -- only the recall policy differs. If antistarvation does not reduce
never_recalled here, package 6 has failed on its own terms and the metric
(or the policy) needs another look, not a claimed win.

    python test_less_naive_assembler.py
"""
from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent /
                      "M8-persistent-work-and-knowledge"))

from context_manager import ContextManager, READ  # noqa: E402
from knowledge_model import KnowledgeStore  # noqa: E402
from wiring import Substrate  # noqa: E402
from work_record import WorkRecordStore  # noqa: E402

from failure_modes import check_insufficiency_visible  # noqa: E402
from less_naive_assembler import recall_antistarvation  # noqa: E402


def build(root: Path) -> Substrate:
    return Substrate(WorkRecordStore(root / "work"),
                     KnowledgeStore(root / "knowledge"),
                     ContextManager(root / "context"))


N_ENTRIES = 10
N_TURNS = 10
TURN_BUDGET = 900          # 2 labelled anchors (400) + room for ~2-3 unlabelled
TOKENS_PER_ENTRY = 200


def run_stress(sub, wid, *, policy) -> int:
    """Repeats a tight-budget recall N_TURNS times, returns how many of the
    N_ENTRIES unlabelled attachments were never once included.
    """
    for _ in range(N_TURNS):
        if policy == "naive":
            sub.context.recall(wid, invocation_id="inv_stress",
                               turn_budget=TURN_BUDGET,
                               approx_tokens_per_entry=TOKENS_PER_ENTRY)
        else:
            recall_antistarvation(sub.context, wid, invocation_id="inv_stress",
                                  turn_budget=TURN_BUDGET,
                                  approx_tokens_per_entry=TOKENS_PER_ENTRY)
    verdict = check_insufficiency_visible(sub.context.live_set(wid),
                                          sub.context.turn_inputs(wid), wid)
    return len(verdict.never_recalled)


def main():
    tmp = Path(tempfile.mkdtemp(prefix="m9_lessnaive_"))
    try:
        sub = build(tmp)

        task_a = sub.create_task(intent_content="x", formulation="naive arm",
                                 scope_boundary="a.py", scope_derivation="named",
                                 invocation_id="inv0a")
        for i in range(N_ENTRIES):
            sub.attach(task_a.work_item_id, {"kind": "note", "i": i},
                      source="worker", crossing_type=READ, invocation_id="inv_att")
        never_recalled_naive = run_stress(sub, task_a.work_item_id, policy="naive")

        task_b = sub.create_task(intent_content="x", formulation="antistarvation arm",
                                 scope_boundary="a.py", scope_derivation="named",
                                 invocation_id="inv0b")
        for i in range(N_ENTRIES):
            sub.attach(task_b.work_item_id, {"kind": "note", "i": i},
                      source="worker", crossing_type=READ, invocation_id="inv_att")
        never_recalled_anti = run_stress(sub, task_b.work_item_id, policy="anti")

        print(f"[data] naive: {never_recalled_naive}/{N_ENTRIES} entries never "
             f"recalled across {N_TURNS} turns")
        print(f"[data] antistarvation: {never_recalled_anti}/{N_ENTRIES} entries "
             f"never recalled across {N_TURNS} turns")

        assert never_recalled_naive > 0, (
            "FAIL: the stress scenario must actually starve the naive policy, "
            "or this test proves nothing -- widen N_ENTRIES or tighten "
            "TURN_BUDGET if this ever passes")
        assert never_recalled_anti < never_recalled_naive, (
            f"FAIL: package 6's own bar -- antistarvation ({never_recalled_anti}) "
            f"must move the metric below the naive baseline "
            f"({never_recalled_naive}), or this is not a less-naive assembler, "
            f"just a different naive one")
        print(f"[ok] the metric MOVED: Insufficiency-visible dropped from "
             f"{never_recalled_naive} to {never_recalled_anti} never-recalled "
             f"entries under identical load -- package 6's falsification test "
             f"passes on this one axis (Insufficiency-visible only; Overload "
             f"is volume-only and reordering cannot move it, and Redundancy/"
             f"Uselessness have no real verdict yet for any policy to move)")

        # --- confirm the naive baseline is untouched by this refactor: same
        # policy_ref as before, same behaviour with no order_unlabelled passed
        history = sub.context.turn_inputs(task_a.work_item_id)
        assert all(r.policy_ref == "naive-degenerate-v1" for r in history)
        history_anti = sub.context.turn_inputs(task_b.work_item_id)
        assert all(r.policy_ref == "antistarvation-v1" for r in history_anti)
        print("[ok] both policies' turn-input records carry the right "
             "policy_ref -- two policies over comparable live sets, "
             "distinguishable in the durable record")

        print()
        print("ALL LESS-NAIVE-ASSEMBLER CHECKS PASSED")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
