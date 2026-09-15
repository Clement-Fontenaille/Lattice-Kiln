"""Work package 4: the four claim dimensions, assessed on 03's own terms.

Specification: docs/00-design/10-foundations/03-evidence-belief-and-provenance.md,
Weighing claims + Scope.

Three dimensions come from Weighing claims -- Validity, Reliability, Pertinence
-- and a fourth, harder one from Scope. The document itself flags which of
these can be recorded once at creation and which cannot:

  Validity     "the logical strength of the claim's own argument, independent
               of where it came from." Assessable once, in principle, by a
               real reasoner. Stub seam here (needs the reasoner).
  Reliability  "how trustworthy the chain that produced it was; mode of
               acquisition and source are EVIDENCE for this dimension, NOT
               weights themselves." That distinction is load-bearing: this
               module exposes the evidence (mode, second_hand, source, parent
               count) mechanically, and refuses to synthesise a verdict from
               it, because turning evidence into a weight is exactly the
               judgement 03 does not hand to a mechanical reader.
  Pertinence   "a property of the comparison rather than of the claim alone...
               the same two claims can outweigh each other differently
               depending on what is being decided." 03 names this itself as
               the clearest case of a dimension that CANNOT be recorded once
               at creation and cached -- it must be judged live, against
               whatever is being decided right now. The function signature
               below enforces that shape (an objective is a required
               argument, not something read off the claim), even before a
               real judge exists to fill it.
  Scope        "has to be assessed near its own creation... no later reading
               of the roots recovers it, because the roots never held it
               whole." This is the dimension that most needs a timestamp to
               even define "near" against -- which is what surfaced the gap
               fixed in knowledge_model.py (Claim.created_at) while building
               this file, rather than after.

Same honesty rule as mandate_check.py and failure_modes.py throughout: no stub
here may claim the dimension holds cleanly (`valid`, `pertinent`,
`in_scope`) -- only `unassessed`. A stub asserting a clean verdict would make
an unjudged claim indistinguishable from a judged, sound one.
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Optional

VALID = "valid"
INVALID = "invalid"
UNASSESSED = "unassessed"
VALIDITY_VERDICTS = {VALID, INVALID, UNASSESSED}

PERTINENT = "pertinent"
NOT_PERTINENT = "not_pertinent"
PERTINENCE_VERDICTS = {PERTINENT, NOT_PERTINENT, UNASSESSED}

IN_SCOPE = "in_scope"
OUT_OF_SCOPE = "out_of_scope"
SCOPE_VERDICTS = {IN_SCOPE, OUT_OF_SCOPE, UNASSESSED}


@dataclass
class DimensionVerdict:
    dimension: str
    verdict: str
    reasoning: str
    checked_at: str
    stub: bool


@dataclass
class ReliabilityEvidence:
    """NOT a verdict -- 03 is explicit that mode/source are evidence FOR
    reliability, not the weight itself. Deliberately has no `verdict` field;
    adding one would be the exact synthesis step 03 reserves for a real
    reasoner comparing claims against each other, not this store.
    """
    claim_id: str
    modes: list                # [mode, ...] one per parent edge
    any_second_hand: bool
    source: str
    parent_count: int
    independent_parent_sources: int   # distinct `source` values across parents' claims --
                                        # convergence evidence (Friction and re-evaluation:
                                        # "independent agreement is evidence the chain is
                                        # not one idiosyncratic accident"), still not a verdict
    collected_at: str


ValidityChecker = Callable[[dict], tuple]
PertinenceChecker = Callable[[dict, str], tuple]      # (content, objective) -> (verdict, reasoning)
ScopeChecker = Callable[[dict, str], tuple]            # (content, domain_context) -> (verdict, reasoning)


def _stub_validity(content: dict) -> tuple:
    return (UNASSESSED, "stub: no reasoner has evaluated this claim's own argument")


def _stub_pertinence(content: dict, objective: str) -> tuple:
    return (UNASSESSED,
           f"stub: no live comparison run against objective {objective!r}")


def _stub_scope(content: dict, domain_context: str) -> tuple:
    return (UNASSESSED,
           f"stub: no assessment of the domain this claim was actually born into "
           f"({domain_context!r}) has been made")


def assess_validity(claim, *, checker: Optional[ValidityChecker] = None) -> DimensionVerdict:
    """Assessable once, referencing only the claim's own content -- unlike
    Pertinence below, this signature does NOT take an objective, because
    validity is 03's own example of a claim property independent of use.
    """
    fn = checker or _stub_validity
    verdict, reasoning = fn(claim.content)
    if verdict not in VALIDITY_VERDICTS:
        raise ValueError(f"checker returned an invalid verdict: {verdict!r}")
    return DimensionVerdict(dimension="validity", verdict=verdict, reasoning=reasoning,
                            checked_at=_now(), stub=(checker is None))


def reliability_evidence(claim, parent_claims: Optional[list] = None) -> ReliabilityEvidence:
    """Real, not stubbed -- but deliberately produces evidence, not a verdict.
    `parent_claims` (the actual Claim objects the edges point to, fetched by
    the caller via KnowledgeStore.read) is optional; without it,
    `independent_parent_sources` cannot be computed and is left at 0 with the
    gap visible in the dataclass itself rather than guessed.
    """
    modes = [p.mode for p in claim.parents]
    any_second_hand = any(p.second_hand for p in claim.parents)
    independent = 0
    if parent_claims:
        independent = len({p.source for p in parent_claims})
    return ReliabilityEvidence(
        claim_id=claim.claim_id, modes=modes, any_second_hand=any_second_hand,
        source=claim.source, parent_count=len(claim.parents),
        independent_parent_sources=independent, collected_at=_now())


def assess_pertinence(claim, *, current_objective: str,
                      checker: Optional[PertinenceChecker] = None) -> DimensionVerdict:
    """`current_objective` is REQUIRED and never read off the claim or cached
    on it -- 03: "the same two claims can outweigh each other differently
    depending on what is being decided." A caller that tries to memoise this
    call's result across two different objectives is re-introducing exactly
    the caching 03 rules out; nothing in this module does that memoisation
    for them.
    """
    fn = checker or _stub_pertinence
    verdict, reasoning = fn(claim.content, current_objective)
    if verdict not in PERTINENCE_VERDICTS:
        raise ValueError(f"checker returned an invalid verdict: {verdict!r}")
    return DimensionVerdict(dimension="pertinence", verdict=verdict, reasoning=reasoning,
                            checked_at=_now(), stub=(checker is None))


def assess_scope(claim, *, domain_context: str,
                 checker: Optional[ScopeChecker] = None,
                 max_staleness_s: Optional[float] = None) -> DimensionVerdict:
    """`domain_context` names the domain to check the claim's birth-scope
    against (host, model family, project state -- 03's own list). If
    `max_staleness_s` is given and `claim.created_at` is older than that by
    the time this runs, the verdict is forced to UNASSESSED regardless of what
    the checker says: 03 is explicit that scope "has to be assessed near its
    own creation... no later reading of the roots recovers it." A checker
    that runs against a long-cold claim is answering a question 03 says
    cannot be answered from that distance, and this function refuses to
    launder that into a confident verdict.
    """
    fn = checker or _stub_scope
    if max_staleness_s is not None and claim.created_at:
        age_s = _age_seconds(claim.created_at)
        if age_s is not None and age_s > max_staleness_s:
            return DimensionVerdict(
                dimension="scope", verdict=UNASSESSED,
                reasoning=(f"claim is {age_s:.0f}s old, over the {max_staleness_s:.0f}s "
                          f"near-creation window -- 03-evidence-belief-and-provenance.md: "
                          f"scope assessed this late cannot be trusted regardless of what "
                          f"any checker would report"),
                checked_at=_now(), stub=(checker is None))
    verdict, reasoning = fn(claim.content, domain_context)
    if verdict not in SCOPE_VERDICTS:
        raise ValueError(f"checker returned an invalid verdict: {verdict!r}")
    return DimensionVerdict(dimension="scope", verdict=verdict, reasoning=reasoning,
                            checked_at=_now(), stub=(checker is None))


def _age_seconds(created_at: str) -> Optional[float]:
    try:
        then = time.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
        return time.mktime(time.gmtime()) - time.mktime(then)
    except ValueError:
        return None


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
