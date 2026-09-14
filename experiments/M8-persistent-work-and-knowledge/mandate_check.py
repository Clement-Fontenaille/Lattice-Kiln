"""The aggregate scope check's seam, not its judgement.

Specification: docs/10-technical/03-capability-authority-model.md

"An implementation MUST run the aggregate check once per work item at
termination" -- on `abandoned` and `executed`, not `challenged`/`deferred`
(that document, restated 2026-09-14 after the consolidation pass this session
continues). The check itself is a natural-language judgement over four inputs
(the operator's request, the derived ceiling, the invocation's scope, the
accumulated change set) and belongs to an INVARIANT PROCESSOR -- binding
`share_nothing`, built in M17, not M8.

What M8 owes, per its own work package list, is the store's half: a trigger
point that fires exactly on the two terminal states, a place to compose
`change_set()` from `work_record.py`, and a place to record the verdict. This
module is that seam. Its default checker is an explicit stub that MUST NOT be
mistaken for the real thing -- it always returns `dubious`, because always
returning `inside` would silently satisfy G4 without a check ever having run,
which is precisely the failure `03-capability-authority-model.md` names as
worse than an absent one.
"""
from __future__ import annotations

import time
from dataclasses import asdict, dataclass
from typing import Callable, Optional

INSIDE = "inside"
OUTSIDE = "outside"
DUBIOUS = "dubious"
VERDICTS = {INSIDE, OUTSIDE, DUBIOUS}


@dataclass
class MandateVerdict:
    work_item_id: str
    verdict: str            # inside | outside | dubious
    reasoning: str
    checked_at: str
    stub: bool               # True until a real invariant processor replaces this


# A checker's signature: (request_text, ceiling_text, change_set) -> (verdict, reasoning)
Checker = Callable[[str, str, list], tuple]


def stub_checker(request: str, ceiling: str, change_set: list) -> tuple:
    """The explicit stand-in. Always `dubious`, never `inside`.

    03-capability-authority-model.md's own words: "outside is not a failure to
    reach a verdict... dubious is the verdict that corresponds to the second of
    10-foundations/07's two modes: ask what only the operator can answer." A
    stub that has not actually reasoned about anything has no basis to claim
    `inside`, and claiming it would make an unchecked task indistinguishable
    from a checked one that passed -- the exact failure mode
    (03-capability-authority-model.md, Failure modes: "A conformance verdict
    recorded only on failure... the system cannot tell an unscoped run from a
    clean one afterwards"). `dubious` is the only verdict a non-reasoning stub
    can honestly return.
    """
    return (DUBIOUS,
           f"stub checker: no real invariant processor is wired in; "
           f"{len(change_set)} change(s) accumulated under this item were never "
           f"actually compared to the declared boundary")


def run_aggregate_check(work_item_id: str, *, request: str, ceiling: str,
                        change_set: list,
                        checker: Optional[Checker] = None) -> MandateVerdict:
    """Runs the check and returns the verdict. Recording it durably is the
    caller's job (wiring.py composes this with the knowledge model, since
    WorkItem itself has no field for it -- the real home for a conformance
    verdict is observability's kind-4 disposition, which M8 does not build).
    """
    fn = checker or stub_checker
    verdict, reasoning = fn(request, ceiling, change_set)
    if verdict not in VERDICTS:
        raise ValueError(f"checker returned an invalid verdict: {verdict!r}")
    return MandateVerdict(work_item_id=work_item_id, verdict=verdict,
                          reasoning=reasoning, checked_at=_now(),
                          stub=(checker is None))


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
