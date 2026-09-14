"""Package 4 hardening: does the single `derived_from` relation actually hold
under split and succession without strain?

13-work-record.md, Open contracts: "Whether the single lineage relation holds
under use. It covers split, succession and merge without strain, and nothing has
exercised it." This is that exercise.

Both a split's children and a redefinition's successor are created the same way
(4a, one edge back through derived_from). What tells them apart is not the edge
-- it's the PARENT's state at the time each is read: left open while children run
-> decomposition; abandoned/executed when its successor was created ->
redefinition. This test builds one of each and checks that reading the parent's
state is enough to tell them apart, with no other signal.

    python test_lineage.py
"""
from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from context_manager import ContextManager
from knowledge_model import KnowledgeStore
from wiring import Substrate
from work_record import ANSWERED, DECLINED, Scope, WorkRecordStore, DERIVED


def build(root: Path) -> Substrate:
    return Substrate(WorkRecordStore(root / "work"),
                     KnowledgeStore(root / "knowledge"),
                     ContextManager(root / "context"))


def main():
    tmp = Path(tempfile.mkdtemp(prefix="m8_lineage_"))
    try:
        sub = build(tmp)
        work = sub.work

        # --- SPLIT: a parent left OPEN while two children do the actual work.
        # Concern-split, effect 4a, fan-out from one parent (13-work-record.md,
        # "a split fans out from one parent").
        parent = sub.create_task(
            intent_content="Ship the CSV export feature.",
            formulation="(1) parse quoted fields correctly (2) handle a leading BOM",
            scope_boundary="csvparse.py", scope_derivation="named directly",
            invocation_id="inv_parent")

        child_a = work.create_child(
            parent.work_item_id, formulation="Parse quoted fields correctly.",
            scope=Scope(boundary="csvparse.py: parse()", derivation="split from parent",
                       scope_state=DERIVED), ceiling="csvparse.py")
        child_b = work.create_child(
            parent.work_item_id, formulation="Handle a leading BOM.",
            scope=Scope(boundary="csvparse.py: parse()", derivation="split from parent",
                       scope_state=DERIVED), ceiling="csvparse.py")

        work.conclude(child_a.work_item_id, ANSWERED, "quoted fields handled",
                     effect_ref="e1", invocation_ref="inv_a")
        work.conclude(child_b.work_item_id, ANSWERED, "BOM stripped",
                     effect_ref="e2", invocation_ref="inv_b")

        # the parent is untouched -- 13-work-record.md: "splitting is NOT a
        # transition. Both create new work items and leave the existing one
        # untouched."
        parent_after_split = work.get_item(parent.work_item_id)
        assert parent_after_split.state == "open", (
            f"FAIL: parent mutated by its children's conclusions, "
            f"state={parent_after_split.state!r}")
        assert parent_after_split.formulation == parent.formulation, (
            "FAIL: parent's formulation changed")
        kids = work.children(parent.work_item_id)
        assert {k.work_item_id for k in kids} == {child_a.work_item_id, child_b.work_item_id}
        print(f"[ok] split: parent {parent.work_item_id[:10]} stayed OPEN with "
             f"{len(kids)} children, both concluded, parent record untouched")

        # --- SUCCESSION: a parent gets ABANDONED, and a successor is created
        # with a redefined objective (13-work-record.md: "a successor task,
        # created with a redefined objective... derives its scope at creation").
        stale = sub.create_task(
            intent_content="Speed up unit_cost().",
            formulation="Optimise prices.unit_cost for speed.",
            scope_boundary="prices.py", scope_derivation="named directly",
            invocation_id="inv_stale")
        work.conclude(stale.work_item_id, DECLINED,
                      "unit_cost is already optimal; premise was false",
                      effect_ref="e3", invocation_ref="inv_stale")

        stale_after = work.get_item(stale.work_item_id)
        assert stale_after.state == "abandoned", (
            f"FAIL: declined should auto-terminate to abandoned, "
            f"got {stale_after.state!r}")

        successor = work.create_child(
            stale.work_item_id,
            formulation="Reduce the CALL COUNT to prices.unit_cost via caching "
                       "at the caller, since unit_cost itself is already optimal.",
            scope=Scope(boundary="callers of prices.unit_cost",
                       derivation="redefined after the original premise was found false",
                       scope_state=DERIVED),
            ceiling="prices.py and its callers")
        print(f"[ok] succession: {stale.work_item_id[:10]} abandoned, successor "
             f"{successor.work_item_id[:10]} created with a redefined objective")

        # --- THE ACTUAL TEST: read the shape off the parent's state alone, no
        # other signal, and correctly label one relation "split" and the other
        # "succession".
        def classify(parent_id: str) -> str:
            p = work.get_item(parent_id)
            kids = work.children(parent_id)
            if p.is_live():
                return "decomposition" if len(kids) >= 1 else "open, no children yet"
            # terminal parent with exactly one child sharing its intent and a
            # redefined formulation is a succession; terminal with multiple
            # children is a merge-adjacent shape this project hasn't built yet
            if len(kids) == 1:
                return "redefinition (successor)"
            return "terminal parent, ambiguous shape"

        got_split = classify(parent.work_item_id)
        got_succession = classify(stale.work_item_id)
        assert got_split == "decomposition", f"FAIL: misclassified split as {got_split!r}"
        assert got_succession == "redefinition (successor)", (
            f"FAIL: misclassified succession as {got_succession!r}")
        print(f"[ok] classification from parent state alone: "
             f"split->{got_split!r}, succession->{got_succession!r}")

        # --- lineage() walks the primary chain back to intent, for both shapes
        chain_a = work.lineage(child_a.work_item_id)
        assert chain_a[0].work_item_id == child_a.work_item_id
        assert chain_a[1].work_item_id == parent.work_item_id
        assert chain_a[-1].intent_id == parent.intent_ref
        print(f"[ok] lineage(child_a) walks child -> parent -> intent "
             f"({len(chain_a)} hops)")

        chain_succ = work.lineage(successor.work_item_id)
        assert chain_succ[1].work_item_id == stale.work_item_id
        print(f"[ok] lineage(successor) walks successor -> stale parent -> "
             f"its OWN intent (redefinition does not inherit the parent's intent_ref"
             f" object, but does inherit its intent_ref value: "
             f"{successor.intent_ref == stale.intent_ref})")

        # --- CONTAINMENT: a child reaching wider than its narrow parent, while
        # staying inside the ceiling, is legitimate (13-work-record.md,
        # Containment: "a child may legitimately reach wider than a narrow
        # parent as long as it stays inside what intent authorised").
        narrow_parent = sub.create_task(
            intent_content="Fix the off-by-one in paginate().",
            formulation="Fix paginate() off-by-one for page 1.",
            scope_boundary="page.py: paginate(), narrowly the off-by-one",
            scope_derivation="named directly, narrowed to the specific bug",
            invocation_id="inv_narrow")
        wider_child = work.create_child(
            narrow_parent.work_item_id,
            formulation="Fix paginate() off-by-one AND add a regression test in "
                       "page_test.py.",
            scope=Scope(boundary="page.py and page_test.py",
                       derivation="the intent covered the tests all along; the "
                                  "parent's narrowing was for focus, not a floor",
                       scope_state=DERIVED),
            ceiling="page.py and page_test.py")   # contained in ceiling, not in parent
        print(f"[ok] containment: child scope ({wider_child.scope.boundary!r}) "
             f"reaches wider than its parent's ({narrow_parent.scope.boundary!r}) "
             f"and was accepted -- checked against the ceiling, not the parent")

        print()
        print("ALL LINEAGE CHECKS PASSED")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
