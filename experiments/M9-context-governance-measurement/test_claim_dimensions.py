"""Package 4: do the four claim dimensions behave the way 03 says each of
them can -- validity/pertinence/scope as honest stubs, reliability as real
evidence without a synthesised verdict, and pertinence's signature enforcing
live (not cached) comparison?

    python test_claim_dimensions.py
"""
from __future__ import annotations

import shutil
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent /
                      "M8-persistent-work-and-knowledge"))

from knowledge_model import EVIDENCE, KnowledgeStore, ParentEdge, READ, REASONED  # noqa: E402

from claim_dimensions import (IN_SCOPE, PERTINENT, UNASSESSED, VALID,  # noqa: E402
                             assess_pertinence, assess_scope, assess_validity,
                             reliability_evidence)


def main():
    tmp = Path(tempfile.mkdtemp(prefix="m9_claimdim_"))
    try:
        ks = KnowledgeStore(tmp / "knowledge")

        root_a = ks.write_observation({"text": "log line 42: timeout after 30s"},
                                      source="system")
        root_b = ks.write_observation({"text": "second vendor also reports 30s timeout"},
                                      source="operator")
        claim = ks.propose_claim(
            EVIDENCE, {"text": "the timeout is real and reproducible"}, source="worker",
            parents=[ParentEdge(claim_id=root_a.claim_id, mode=READ),
                    ParentEdge(claim_id=root_b.claim_id, mode=REASONED, second_hand=True)])

        # --- VALIDITY: honest stub, no objective needed in the signature
        v = assess_validity(claim)
        assert v.verdict == UNASSESSED and v.stub is True
        print("[ok] validity stub returns UNASSESSED, never VALID, on an "
             "unexamined claim")

        def real_validity(content):
            return (VALID, "argument checks out")
        v2 = assess_validity(claim, checker=real_validity)
        assert v2.verdict == VALID and v2.stub is False
        print("[ok] an injected real checker can return VALID; the seam is "
             "not hard-wired to UNASSESSED")

        # --- RELIABILITY: real evidence, deliberately NOT a verdict
        parent_claims = [ks.read(root_a.claim_id), ks.read(root_b.claim_id)]
        ev = reliability_evidence(claim, parent_claims)
        assert ev.modes == ["read", "reasoned"]
        assert ev.any_second_hand is True
        assert ev.independent_parent_sources == 2, (
            f"FAIL: expected 2 distinct parent sources (system, operator), "
            f"got {ev.independent_parent_sources}")
        assert not hasattr(ev, "verdict"), (
            "FAIL: ReliabilityEvidence must not carry a verdict field -- 03 is "
            "explicit that mode/source are evidence FOR reliability, not the "
            "weight itself; synthesising one here would be the exact step 03 "
            "reserves for a real reasoner")
        print(f"[ok] reliability_evidence: modes={ev.modes}, "
             f"any_second_hand={ev.any_second_hand}, "
             f"independent_parent_sources={ev.independent_parent_sources} "
             f"(convergence evidence) -- no verdict field exists to check")

        # --- without parent_claims, independent_parent_sources stays 0 and
        # visibly so, rather than silently guessing from claim.parents alone
        ev_partial = reliability_evidence(claim)
        assert ev_partial.independent_parent_sources == 0
        print("[ok] reliability_evidence without parent_claims leaves "
             "independent_parent_sources at 0 rather than fabricating a count")

        # --- PERTINENCE: signature FORCES a live objective, never cached
        pv1 = assess_pertinence(claim, current_objective="diagnose the timeout")
        pv2 = assess_pertinence(claim, current_objective="fix an unrelated typo")
        assert pv1.verdict == UNASSESSED and pv2.verdict == UNASSESSED  # both stub
        assert pv1.reasoning != pv2.reasoning, (
            "FAIL: the two calls carried different objectives and must produce "
            "different reasoning strings -- if they matched, the objective "
            "argument would be getting ignored, i.e. treated as cacheable, "
            "exactly what 03 rules out for this dimension")
        print("[ok] pertinence assessed twice against two different objectives "
             "produces two distinct records -- the call shape itself enforces "
             "'judged live', even before a real judge exists")

        def real_pertinence(content, objective):
            return (PERTINENT, f"directly relevant to {objective!r}") if "timeout" in objective else (
                "not_pertinent", f"unrelated to {objective!r}")
        pv3 = assess_pertinence(claim, current_objective="diagnose the timeout",
                                checker=real_pertinence)
        assert pv3.verdict == PERTINENT
        print("[ok] an injected real checker can return PERTINENT")

        # --- SCOPE: honest stub, plus the near-creation staleness guard
        sv = assess_scope(claim, domain_context="this host, this model family")
        assert sv.verdict == UNASSESSED and sv.stub is True
        print("[ok] scope stub returns UNASSESSED on a fresh claim")

        def real_scope(content, domain):
            return (IN_SCOPE, f"holds within {domain!r}")
        sv2 = assess_scope(claim, domain_context="this host", checker=real_scope)
        assert sv2.verdict == IN_SCOPE
        print("[ok] an injected real checker can return IN_SCOPE on a fresh claim")

        # a claim past the staleness window is forced to UNASSESSED even
        # with a real checker injected, because 03 says a late reading
        # cannot be trusted regardless of what runs it
        stale_claim = ks.propose_claim(
            EVIDENCE, {"text": "an old reading"}, source="worker",
            parents=[ParentEdge(claim_id=root_a.claim_id, mode=READ)])
        object.__setattr__  # (not used; created_at is a plain str field)
        stale_claim.created_at = time.strftime(
            "%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - 10_000))
        sv3 = assess_scope(stale_claim, domain_context="this host",
                           checker=real_scope, max_staleness_s=60)
        assert sv3.verdict == UNASSESSED, (
            f"FAIL: a claim 10000s old with a 60s staleness window must be "
            f"forced to UNASSESSED even with a real checker injected, got "
            f"{sv3.verdict!r}")
        assert "near-creation window" in sv3.reasoning
        print("[ok] a stale claim is forced to UNASSESSED under a staleness "
             "window even with a real checker available -- 03: no later "
             "reading recovers scope, so the seam refuses to launder one "
             "into a confident verdict")

        print()
        print("ALL CLAIM-DIMENSION CHECKS PASSED")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
