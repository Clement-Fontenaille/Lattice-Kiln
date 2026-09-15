"""Work package 3: the four failure-mode detectors.

Specification: docs/00-design/40-roadmap/01-MILESTONES/09-context-governance-measurement.md
Foundations: docs/00-design/10-foundations/04-context-as-governed-resource.md

Four failure modes are named there, and this milestone's own text is explicit
that they are not equally checkable:

  Insufficiency  divides. Half is invisible (material that never crossed --
                 nothing here can compare against what was never fetched).
                 The other half (crossed but not recalled) IS visible from the
                 live set and the turn-input record. Only that half is built.
  Redundancy     needs overlap AT THE LEVEL OF COVERAGE, not text -- two
                 artifacts can restate one finding with no shared substring.
                 That is a semantic judgement this module does not make; a
                 stub seam only, honest about not having judged anything.
  Uselessness    "predicted, not evidenced" by the milestone's own account.
                 Same treatment as Redundancy: a stub seam.
  Overload       "the only content-quality-agnostic one" -- whether the
                 aggregate exceeded what one turn's assembly could integrate.
                 This is checkable mechanically, off the turn-input record's
                 own `truncated` flag, with no semantic judgement required.
                 Built for real, not stubbed.

The honesty rule carried over from M8's mandate_check.py stub_checker: a stub
that has not actually judged anything MUST NOT be able to claim the clean
verdict (here, "not redundant" / "not useless"). Claiming it would make an
unassessed case indistinguishable from an assessed, clean one -- exactly the
failure 03-capability-authority-model.md names for the mandate check, and the
same logic applies to any quality dimension recorded by this project.
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Optional

# ------------------------------------------------------------- Overload

@dataclass
class OverloadVerdict:
    turn_index: int
    occurred: bool          # == the turn-input record's own `truncated` flag
    dropped_count: int
    checked_at: str


def check_overload(turn_input_record) -> OverloadVerdict:
    """Content-quality-agnostic by construction: reads only `truncated` and
    the drop count off a kind-5 record (context_manager.TurnInputRecord).
    Never opens `content` on anything -- Overload is a volume question, and
    reading content to answer it would be answering a different question.
    """
    return OverloadVerdict(
        turn_index=turn_input_record.turn_index,
        occurred=turn_input_record.truncated,
        dropped_count=len(turn_input_record.dropped),
        checked_at=_now())


def overload_rate(turn_input_records: list) -> float:
    """Across a task's whole life: what fraction of turns hit Overload.
    A per-task aggregate is what a corpus sweep (M9 package 5, re-grading E6)
    would actually read, not a single turn's verdict in isolation.
    """
    if not turn_input_records:
        return 0.0
    hits = sum(1 for r in turn_input_records if r.truncated)
    return hits / len(turn_input_records)


# --------------------------------------------------------- Insufficiency

@dataclass
class InsufficiencyVerdict:
    work_item_id: str
    never_recalled: list       # live_set_ids registered but included in NO turn
    checked_at: str
    blind_spot: str = (
        "material that never crossed at all is invisible from this store by "
        "construction -- nothing here can compare against what was never "
        "fetched. This verdict covers only the visible half: material that "
        "DID cross (is in the live set) but was never once included in any "
        "turn's presented context before the check ran."
    )


def check_insufficiency_visible(live_set_entries: list, turn_input_records: list,
                                work_item_id: str) -> InsufficiencyVerdict:
    """The checkable half only, per the milestone's own division of this mode.
    Mechanical: a set difference between what is live and what was ever
    presented across every recorded turn. No semantic judgement about whether
    the never-recalled material was actually NEEDED -- that would be reaching
    into Uselessness's territory (the mirror-image question) or Pertinence
    (03-evidence-belief-and-provenance.md), neither of which this function
    attempts.
    """
    ever_included = set()
    for rec in turn_input_records:
        ever_included.update(live_set_id for live_set_id, _crossing_type in rec.included)
    all_live = {e.live_set_id for e in live_set_entries}
    never_recalled = sorted(all_live - ever_included)
    return InsufficiencyVerdict(work_item_id=work_item_id,
                                never_recalled=never_recalled, checked_at=_now())


# ------------------------------------------------------ Redundancy / Uselessness

REDUNDANT = "redundant"
NOT_REDUNDANT = "not_redundant"
UNASSESSED = "unassessed"
REDUNDANCY_VERDICTS = {REDUNDANT, NOT_REDUNDANT, UNASSESSED}

NEEDED = "needed"
USELESS = "useless"
USELESSNESS_VERDICTS = {NEEDED, USELESS, UNASSESSED}


@dataclass
class QualityVerdict:
    dimension: str            # "redundancy" | "uselessness"
    verdict: str
    reasoning: str
    checked_at: str
    stub: bool


RedundancyChecker = Callable[[dict, list], tuple]     # (candidate_content, live_contents) -> (verdict, reasoning)
UselessnessChecker = Callable[[dict, str], tuple]     # (candidate_content, objective) -> (verdict, reasoning)


def _stub_redundancy_checker(candidate_content: dict, live_contents: list) -> tuple:
    """Coverage-level overlap ("two artifacts restating one finding in
    different words, with no shared substring") is a semantic reading this
    stub cannot perform. It MUST NOT return `not_redundant` -- that would
    silently claim a dedup pass ran when none did. `unassessed` is the only
    honest answer from a non-reasoning stub, mirroring
    mandate_check.py::stub_checker's DUBIOUS-only discipline.
    """
    return (UNASSESSED,
           f"stub: no coverage-level comparator wired in; {len(live_contents)} "
           f"live artifact(s) were never actually compared against the candidate")


def _stub_uselessness_checker(candidate_content: dict, objective: str) -> tuple:
    """Whether material was NEEDED is a pertinence judgement
    (03-evidence-belief-and-provenance.md: pertinence is a property of the
    comparison, assessed live, not a static claim property) -- this stub does
    not judge it and must not claim `needed` for the same reason it must not
    claim `not_redundant` above.
    """
    return (UNASSESSED,
           "stub: no live pertinence-against-objective comparator wired in")


def check_redundancy(candidate_content: dict, live_contents: list, *,
                     checker: Optional[RedundancyChecker] = None) -> QualityVerdict:
    fn = checker or _stub_redundancy_checker
    verdict, reasoning = fn(candidate_content, live_contents)
    if verdict not in REDUNDANCY_VERDICTS:
        raise ValueError(f"checker returned an invalid verdict: {verdict!r}")
    return QualityVerdict(dimension="redundancy", verdict=verdict, reasoning=reasoning,
                          checked_at=_now(), stub=(checker is None))


def check_uselessness(candidate_content: dict, objective: str, *,
                      checker: Optional[UselessnessChecker] = None) -> QualityVerdict:
    fn = checker or _stub_uselessness_checker
    verdict, reasoning = fn(candidate_content, objective)
    if verdict not in USELESSNESS_VERDICTS:
        raise ValueError(f"checker returned an invalid verdict: {verdict!r}")
    return QualityVerdict(dimension="uselessness", verdict=verdict, reasoning=reasoning,
                          checked_at=_now(), stub=(checker is None))


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
