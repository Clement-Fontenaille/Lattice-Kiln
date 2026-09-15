"""Work package 6: a less-naive assembler, as the thing that moves the metric.

Specification: 09-context-governance-measurement.md, Work packages, #6 --
"The bar recorded at rework 1 has two halves and the second is usually
forgotten: the naive assembler's failures are quantifiable, AND a less-naive
one moves the measurement." Also: "Package 6 is what falsifies the metric --
a dimension no better assembler can move is a dimension that was measuring
something else."

Scope, honestly stated: of the four failure modes in failure_modes.py, only
two are real (Overload, Insufficiency-visible); Redundancy and Uselessness
are stubs with no verdict a policy could move. Of those two real ones,
Overload is a pure volume question -- REORDERING what gets included cannot
change whether the aggregate exceeds the budget, only WHICH items are inside
it when it does. Only Insufficiency-visible is something an ordering policy
can actually move, so that is the one axis this module targets. This is a
narrower falsification than the milestone eventually needs (a real assembler
would also need to move Redundancy/Uselessness, which needs the semantic
judgement this project has deliberately not built yet), but it is a real,
checkable one rather than a claimed one.

The naive baseline (context_manager.py::recall(), no `order_unlabelled`
passed) replays the SAME registered_at order every single turn. Under
sustained budget pressure, this systematically starves whichever entries
sort last -- typically the most recently attached material, since
`registered_at` only grows. `recall_antistarvation` breaks that by ordering
unlabelled entries on (times previously dropped, DESC; registered_at, ASC):
an entry that has been passed over before earns priority next time. Nothing
here is a smarter judgement of WHAT matters -- it is a fairness policy over
WHO gets seen, which is exactly the kind of "less naive" the naive baseline's
own asymmetry (always favouring the oldest) invites as the first, cheapest
fix.
"""
from __future__ import annotations


def recall_antistarvation(context_manager, work_item_id: str, **kwargs):
    """Same call shape as `context_manager.recall()`, plus the antistarvation
    ordering wired in as `order_unlabelled`. `policy_name` is fixed here so a
    turn-input record produced by this policy is unambiguously attributable
    (kind 5's own point: two policies are comparable only if what each
    presented was recorded, including WHICH policy it was).
    """
    def _order(unlabelled_entries, wid):
        drop_counts = _drop_counts(context_manager, wid)
        return sorted(
            unlabelled_entries,
            key=lambda e: (-drop_counts.get(e.live_set_id, 0), e.registered_at))

    kwargs.setdefault("policy_name", "antistarvation-v1")
    return context_manager.recall(work_item_id, order_unlabelled=_order, **kwargs)


def _drop_counts(context_manager, work_item_id: str) -> dict:
    counts: dict = {}
    for record in context_manager.turn_inputs(work_item_id):
        for live_set_id in record.dropped:
            counts[live_set_id] = counts.get(live_set_id, 0) + 1
    return counts
