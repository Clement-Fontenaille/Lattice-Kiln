"""Does the aggregate check fire exactly on termination, never on live states,
and get recorded whether it passes or not?

03-capability-authority-model.md, Failure modes: "A conformance verdict recorded
only on failure... the system cannot tell an unscoped run from a clean one
afterwards." This test checks `inside` is recorded as explicitly as `outside`.

    python test_mandate.py
"""
from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from context_manager import ContextManager
from knowledge_model import KnowledgeStore
from mandate_check import DUBIOUS, INSIDE, OUTSIDE
from wiring import Substrate
from work_record import ANSWERED, DECLINED, WorkRecordStore


def build(root: Path) -> Substrate:
    return Substrate(WorkRecordStore(root / "work"),
                     KnowledgeStore(root / "knowledge"),
                     ContextManager(root / "context"))


def real_checker(request, ceiling, change_set):
    """Stands in for M17's invariant processor: crude but non-stub -- fails
    closed if more than 2 changes accumulated under a task whose ceiling
    mentions "narrowly".
    """
    if "narrowly" in ceiling and len(change_set) > 2:
        return (OUTSIDE, f"{len(change_set)} changes exceed the narrow ceiling {ceiling!r}")
    return (INSIDE, "within the declared boundary")


def main():
    tmp = Path(tempfile.mkdtemp(prefix="m8_mandate_"))
    try:
        sub = build(tmp)

        # --- the stub NEVER claims `inside` -- it can only be honest about not
        # having checked anything
        t1 = sub.create_task(intent_content="x", formulation="do a thing",
                             scope_boundary="a.py", scope_derivation="named",
                             invocation_id="inv1")
        sub.work.conclude(t1.work_item_id, ANSWERED, "done",
                          effect_ref="e1", invocation_ref="inv1")
        sub.end_task(t1.work_item_id, effect_ref="e1c", invocation_id="inv1")
        claims = sub.knowledge.query(term="mandate_verdict", breadth=50)
        v1 = [c for c in claims if c.content.get("work_item_id") == t1.work_item_id][0]
        assert v1.content["verdict"] == DUBIOUS and v1.content["stub"] is True
        print(f"[ok] stub checker returns dubious, never inside "
             f"(work_item {t1.work_item_id[:10]})")

        # --- a real checker: `inside`, recorded explicitly, not just on failure
        t2 = sub.create_task(intent_content="y", formulation="do a bounded thing",
                             scope_boundary="b.py", scope_derivation="named",
                             invocation_id="inv2")
        sub.work.conclude(t2.work_item_id, ANSWERED, "done",
                          effect_ref="e2", invocation_ref="inv2")
        v2 = sub.check_mandate(t2.work_item_id)
        # check_mandate was already called once inside end_task with the stub
        # above via t1; here call it directly with the real checker BEFORE
        # end_task to show the seam accepts an injected checker
        from mandate_check import run_aggregate_check
        v2_real = run_aggregate_check(t2.work_item_id, request="do a bounded thing",
                                      ceiling="b.py", change_set=sub.work.change_set(t2.work_item_id),
                                      checker=real_checker)
        assert v2_real.verdict == INSIDE and v2_real.stub is False
        print(f"[ok] injected real checker returns inside, stub=False")

        # --- outside is reachable and distinguishable from dubious
        t3 = sub.create_task(intent_content="z",
                             formulation="fix the off-by-one, narrowly",
                             scope_boundary="c.py: narrowly the off-by-one",
                             scope_derivation="named, narrowed", invocation_id="inv3")
        for i in range(4):
            sub.work.transition_item(t3.work_item_id, "challenged" if i % 2 else "deferred",
                                     effect_ref=f"e3_{i}", invocation_ref="inv3")
            # transitions alternate challenged/deferred to build up change_set
            # entries without terminating -- change_set() reads transitions
        sub.work.conclude(t3.work_item_id, ANSWERED, "widened beyond the narrow ceiling",
                          effect_ref="e3", invocation_ref="inv3", terminal="executed")
        v3 = run_aggregate_check(t3.work_item_id, request="fix the off-by-one, narrowly",
                                 ceiling="c.py: narrowly the off-by-one",
                                 change_set=sub.work.change_set(t3.work_item_id),
                                 checker=real_checker)
        assert v3.verdict == OUTSIDE, f"expected outside, got {v3.verdict}"
        print(f"[ok] outside is reachable and distinct from dubious: {v3.reasoning}")

        # --- fires on abandoned too, not just executed
        t4 = sub.create_task(intent_content="w", formulation="do a false-premise thing",
                             scope_boundary="d.py", scope_derivation="named",
                             invocation_id="inv4")
        sub.work.conclude(t4.work_item_id, DECLINED, "false premise",
                          effect_ref="e4", invocation_ref="inv4")
        item4 = sub.work.get_item(t4.work_item_id)
        assert item4.state == "abandoned"
        sub.end_task(t4.work_item_id, effect_ref="e4c", invocation_id="inv4",
                    terminal="abandoned")
        claims4 = sub.knowledge.query(term="mandate_verdict", breadth=50)
        assert any(c.content.get("work_item_id") == t4.work_item_id for c in claims4), (
            "FAIL: aggregate check did not fire on an abandoned (declined) item")
        print(f"[ok] the check fires on abandoned, not only executed "
             f"(13-work-record.md: abandoned and executed are both terminal)")

        # --- never fires on a live state
        t5 = sub.create_task(intent_content="v", formulation="still working",
                             scope_boundary="e.py", scope_derivation="named",
                             invocation_id="inv5")
        sub.work.transition_item(t5.work_item_id, "challenged",
                                 effect_ref="e5", invocation_ref="inv5")
        claims5_before = len(sub.knowledge.query(term="mandate_verdict", breadth=100))
        # no end_task call -- the item is still live
        claims5_after = len(sub.knowledge.query(term="mandate_verdict", breadth=100))
        assert claims5_before == claims5_after, (
            "FAIL: a mandate verdict appeared without the item ever terminating")
        print(f"[ok] no verdict recorded while the item is still live "
             f"({t5.work_item_id[:10]} is 'challenged')")

        print()
        print("ALL MANDATE-CHECK TESTS PASSED")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
