"""Package 2 hardening: compress() and traverse_dependents(), neither exercised
by test_small.py, plus a check on elide()'s stated refusal condition.

12-knowledge-model.md, Compress: refuses an unchecked step or a root, and
produces a souvenir that REPLACES the working claim rather than rewriting it.
Traverse dependents: the direction opposite a provenance lookup, served by the
children/ index every write appends to.

    python test_knowledge_ops.py
"""
from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from knowledge_model import (EVIDENCE, FINDING, KnowledgeError, KnowledgeStore,
                             ParentEdge, READ, REASONED)


def main():
    tmp = Path(tempfile.mkdtemp(prefix="m8_knowledge_ops_"))
    try:
        ks = KnowledgeStore(tmp / "knowledge")

        # --- compress refuses an unchecked step
        root = ks.write_observation({"kind": "raw", "text": "page 4 of the log"},
                                    source="system")
        unchecked = ks.propose_claim(
            EVIDENCE, {"text": "looks like a timeout"}, source="worker",
            parents=[ParentEdge(claim_id=root.claim_id, mode=READ)], checked=False)
        try:
            ks.compress(unchecked.claim_id, {"text": "timeout"}, source="worker")
            assert False, "FAIL: compress() accepted an unchecked claim"
        except KnowledgeError:
            print("[ok] compress() refuses an unchecked step")

        # --- compress refuses a root (no parents)
        try:
            ks.compress(root.claim_id, {"text": "n/a"}, source="worker")
            assert False, "FAIL: compress() accepted a root"
        except KnowledgeError:
            print("[ok] compress() refuses a root (nothing regenerates a kept observation)")

        # --- compress on a checked, non-root claim: produces a souvenir that
        # REPLACES the working claim (deleted, not overwritten -- a new id)
        checked = ks.propose_claim(
            FINDING, {"text": "confirmed: request timed out at 30s"}, source="worker",
            parents=[ParentEdge(claim_id=root.claim_id, mode=REASONED)], checked=True)
        souvenir = ks.compress(checked.claim_id, {"text": "timeout, 30s"}, source="worker")
        assert souvenir.claim_id != checked.claim_id, (
            "FAIL: compress() returned the same id -- it must create, not rewrite")
        assert souvenir.checked is True
        assert [p.claim_id for p in souvenir.parents] == [root.claim_id], (
            "FAIL: souvenir did not inherit the working claim's parent edges")
        try:
            ks.read(checked.claim_id)
            assert False, "FAIL: the working claim survived compress() -- it must be deleted"
        except KnowledgeError:
            print(f"[ok] compress() deletes the working claim ({checked.claim_id[:10]}) "
                 f"and creates a souvenir ({souvenir.claim_id[:10]}) inheriting its edges")

        # --- traverse_dependents: the reverse-provenance direction
        base = ks.write_observation({"kind": "raw", "text": "base fact"}, source="system")
        child1 = ks.propose_claim(
            EVIDENCE, {"text": "cites base, angle A"}, source="worker",
            parents=[ParentEdge(claim_id=base.claim_id, mode=READ)])
        child2 = ks.propose_claim(
            EVIDENCE, {"text": "cites base, angle B"}, source="worker",
            parents=[ParentEdge(claim_id=base.claim_id, mode=READ)])
        deps = ks.traverse_dependents(base.claim_id)
        assert {c.claim_id for c in deps} == {child1.claim_id, child2.claim_id}, (
            f"FAIL: traverse_dependents(base) should return both children, got "
            f"{[c.claim_id for c in deps]}")
        print(f"[ok] traverse_dependents(base) returns both citing claims "
             f"({len(deps)}), the reverse of a provenance walk")
        assert ks.traverse_dependents(child1.claim_id) == [], (
            "FAIL: a leaf claim (nothing cites it yet) should have no dependents")
        print("[ok] a leaf with nothing citing it has no dependents")

        # --- SUSPECT (see SUSPECT.md #1): elide()'s docstring says it refuses
        # anything "reachable from a root (a promoted claim, OR a live task's
        # attachment)" but _is_reachable_root only ever checks the promoted
        # set. A claim held live by an ongoing task's attachment, but never
        # promoted, is NOT protected by elide() even though the docstring
        # says it should be. This test documents the gap rather than hiding it:
        # it demonstrates elide() currently SUCCEEDS on such a claim.
        live_not_promoted = ks.write_observation(
            {"kind": "attachment", "text": "held live by a task, never promoted"},
            source="worker")
        # not promoted -- ks.promote() is never called on it
        ks.elide(live_not_promoted.claim_id)  # currently succeeds
        try:
            ks.read(live_not_promoted.claim_id)
            assert False, ("elide() should have deleted it, which would make this "
                          "SUSPECT note obsolete -- re-check SUSPECT.md #1")
        except KnowledgeError:
            print("[SUSPECT confirmed, see SUSPECT.md #1] elide() deleted a claim "
                 "that was never promoted, without knowing whether some live "
                 "task's attachment set still holds it -- the docstring's "
                 "'or a live task's attachment' half of the refusal condition "
                 "is not implemented. In practice wiring.py never calls elide() "
                 "directly (it goes through sweep_from with an explicit "
                 "still_live set instead), so this gap is not yet reachable "
                 "from the wired system -- but the function's own contract as "
                 "written does not hold if called directly.")

        print()
        print("ALL KNOWLEDGE-OPS CHECKS PASSED (one SUSPECT logged, see SUSPECT.md)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
