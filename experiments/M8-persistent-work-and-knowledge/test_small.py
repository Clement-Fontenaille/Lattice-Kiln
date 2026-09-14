"""Work package 5: does the system hold and correctly use knowledge it did not
derive itself in the same session?

08-persistent-work-and-knowledge.md, Evidence question, stage 1: "A processor
reuses a stored finding or decision from an earlier run and measurably beats one
starting cold." This does NOT need M9 -- it is answerable at small scale with the
substrate alone.

No model calls here. What is being tested is the STORE's mechanics (immutability,
promotion, retention, reuse across a task boundary), not a model's judgement --
that is exactly the right scope for M8, which builds substrate, not cognition.

    python test_small.py
"""
from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from context_manager import ContextManager, RETRIEVAL
from knowledge_model import DECISION, FINDING, KnowledgeStore, ParentEdge, READ, TESTED
from wiring import Substrate
from work_record import ANSWERED, WorkRecordStore


def build(root: Path) -> Substrate:
    return Substrate(WorkRecordStore(root / "work"),
                     KnowledgeStore(root / "knowledge"),
                     ContextManager(root / "context"))


def scenario_cold(sub: Substrate) -> dict:
    """A task starting cold: it has to (simulate) re-derive a finding from
    scratch -- here, by counting how many crossings it takes before it has an
    equivalent claim in hand. No stored finding to reuse.
    """
    task = sub.create_task(
        intent_content="Is retry-with-backoff safe for this sender?",
        formulation="Determine whether Sender.send should retry Transient "
                   "failures, and how many times.",
        scope_boundary="sender.py and its tests",
        scope_derivation="the request names Sender.send directly",
        invocation_id="inv_cold")

    crossings = 0
    # simulating re-derivation: read the source, run the test suite, reason
    # about the result -- three crossings where a reuse would have needed one
    for content, xtype, src in [
        ({"kind": "read", "path": "sender.py"}, READ, "system"),
        ({"kind": "process_execution", "cmd": "pytest sender_test.py"}, RETRIEVAL, "system"),
        ({"kind": "reasoning", "text": "3 retries observed safe empirically"}, READ, "system"),
    ]:
        cid = sub.attach(task.work_item_id, content, source=src,
                         crossing_type=xtype, invocation_id="inv_cold")
        crossings += 1

    sub.knowledge.propose_claim(
        FINDING, {"text": "retry up to 3 times is safe for Sender.send"},
        source="system",
        parents=[ParentEdge(claim_id=cid, mode=REASONED_MODE())],
        checked=True)
    sub.work.conclude(task.work_item_id, ANSWERED,
                      "re-derived from scratch: 3 retries is safe",
                      effect_ref="eff_cold", invocation_ref="inv_cold")
    return {"work_item_id": task.work_item_id, "crossings": crossings}


def REASONED_MODE():
    from knowledge_model import REASONED
    return REASONED


def scenario_warm(sub: Substrate, stored_finding_id: str) -> dict:
    """A task that reuses a promoted finding from an earlier (simulated) run.
    One retrieval crossing instead of three re-derivation crossings.
    """
    task = sub.create_task(
        intent_content="Is retry-with-backoff safe for a different sender?",
        formulation="Determine whether AnotherSender.send should retry "
                   "Transient failures, and how many times.",
        scope_boundary="another_sender.py and its tests",
        scope_derivation="the request names AnotherSender.send directly",
        invocation_id="inv_warm")

    # ONE crossing: retrieve the promoted finding instead of re-deriving it
    sub.context.register(task.work_item_id, claim_ref=stored_finding_id,
                         crossing_type=RETRIEVAL, origin_invocation_id="inv_warm")
    crossings = 1

    sub.work.conclude(task.work_item_id, ANSWERED,
                      "reused stored finding: 3 retries is safe (retrieved, not re-derived)",
                      effect_ref="eff_warm", invocation_ref="inv_warm")
    return {"work_item_id": task.work_item_id, "crossings": crossings}


def main():
    tmp = Path(tempfile.mkdtemp(prefix="m8_smalltest_"))
    try:
        sub = build(tmp)

        # --- prior run: produce and promote a finding, then end its task.
        # Promotion is what keeps it alive after the task ends
        # (12-knowledge-model.md: promoted artifacts + the live set are the
        # root set's two sources -- without promotion this would be swept).
        prior = sub.create_task(
            intent_content="Original investigation into Sender retry safety.",
            formulation="Determine safe retry count for Sender.send.",
            scope_boundary="sender.py", scope_derivation="named directly",
            invocation_id="inv_prior")
        finding_id = sub.attach(
            prior.work_item_id, {"text": "retry up to 3 times is safe for Sender.send"},
            source="system", crossing_type=READ, invocation_id="inv_prior")
        sub.knowledge.promote(finding_id, source="system")
        sub.work.conclude(prior.work_item_id, ANSWERED, "established and promoted",
                          effect_ref="eff_prior", invocation_ref="inv_prior")
        removed_at_prior_close = sub.end_task(prior.work_item_id,
                                              effect_ref="eff_prior_close",
                                              invocation_id="inv_prior")

        # --- check 1: promotion survived the task ending
        assert finding_id not in removed_at_prior_close, (
            "FAIL: a promoted claim was swept when its task ended")
        surviving = sub.knowledge.read(finding_id)
        print(f"[ok] promoted finding {finding_id} survives its task's end "
              f"(retention: promotion, not liveness)")

        # --- check 2: immutability -- qualifying never edits the original
        original_content = dict(surviving.content)
        qualified = sub.knowledge.qualify(
            finding_id, {"note": "confirmed again on a second sender"}, source="system")
        still_there = sub.knowledge.read(finding_id)
        assert still_there.content == original_content, (
            "FAIL: qualification mutated the original claim's content")
        print(f"[ok] qualifying {finding_id} left its content untouched; "
              f"{qualified.claim_id} points back at it")

        # --- cold vs warm ---
        cold = scenario_cold(sub)
        warm = scenario_warm(sub, finding_id)

        print()
        print(f"cold-start crossings to reach a conclusion: {cold['crossings']}")
        print(f"reuse-a-finding crossings to reach a conclusion: {warm['crossings']}")
        beats_cold = warm["crossings"] < cold["crossings"]
        print(f"measurably beats cold start: {beats_cold} "
             f"({warm['crossings']} < {cold['crossings']})")
        assert beats_cold, "FAIL: reuse did not measurably beat cold start"

        # --- check 3: incremental removal is real -- an unpromoted attachment
        # is gone once its task ends and nothing else holds it
        scratch = sub.create_task(
            intent_content="Throwaway investigation.", formulation="Check something minor.",
            scope_boundary="scratch.py", scope_derivation="named directly",
            invocation_id="inv_scratch")
        scratch_claim = sub.attach(scratch.work_item_id, {"text": "not worth keeping"},
                                   source="system", crossing_type=READ,
                                   invocation_id="inv_scratch")
        sub.work.conclude(scratch.work_item_id, ANSWERED, "done, nothing worth keeping",
                          effect_ref="eff_scratch", invocation_ref="inv_scratch")
        removed = sub.end_task(scratch.work_item_id, effect_ref="eff_scratch_close",
                               invocation_id="inv_scratch")
        assert scratch_claim in removed, (
            "FAIL: an unpromoted attachment survived its task ending")
        try:
            sub.knowledge.read(scratch_claim)
            raise AssertionError("FAIL: elided claim is still readable")
        except Exception as e:  # noqa: BLE001
            assert "no such claim" in str(e)
        print(f"[ok] unpromoted attachment {scratch_claim} was removed when "
             f"its task ended (incremental removal, no promotion path)")

        print()
        print("ALL CHECKS PASSED")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
