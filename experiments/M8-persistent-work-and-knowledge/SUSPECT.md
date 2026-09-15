# Suspect list — M8

Things noticed while hardening M8 that are worth a second pass before this
milestone (and M9, which builds on it) is closed. Not blocking — each is
either unreachable from the wired system today, or a deliberate open build
decision restated here for visibility. Add to this list rather than fixing
inline unless the fix is trivial and clearly in scope.

## 1. `elide()`'s refusal condition is narrower than its own docstring

`knowledge_model.py::elide()` docstring: "Refuses a reachable root" and
names the reachable set as "a promoted claim, or a live task's attachment"
(12-knowledge-model.md, Elide). The implementation
(`_is_reachable_root`) only ever checks the promoted set:

```python
def _is_reachable_root(self, claim_id: str) -> bool:
    return claim_id in self._promoted_ids()
```

A claim held live by an ongoing task's attachment but never promoted is not
protected — `elide()` will delete it. Demonstrated in
`test_knowledge_ops.py` (the "SUSPECT confirmed" line).

**Why it hasn't bitten anything yet:** `wiring.py` never calls `elide()`
directly. The one removal path that's wired (`end_task` -> `sweep_from`) is
given an explicit `still_live` set computed from the other two stores and
does its own containment check — `elide()`'s weaker guard is simply never on
the call path. So the gap is real in the function's contract but currently
unreachable in practice.

**Before closing M8 or M9:** either narrow the docstring to match what
`elide()` actually checks (promoted-only), or wire `still_live` into it the
way `sweep_from` receives it, so a future direct caller isn't misled into
trusting a guarantee that isn't there.

## 2. `change_set()` is a stand-in, not what the spec describes

`work_record.py::change_set()` returns the item's transition log because
that is the only history this store holds. 13-work-record.md's own open
contract says the real shape needs observability's realized-effect history,
which M8 does not build (`02-observability-event-model.md` is out of scope
here). This means the aggregate mandate check (`mandate_check.py`,
`wiring.py::check_mandate`) is currently reasoning over state *transitions*
(challenged/deferred/abandoned/executed), not the actual *edits* a task
made — two different notions of "how much happened under this item." A real
invariant processor wired in later (M17) will need the observability
version of this, not the current one.

## 3. Containment checking (`_looks_contained`) is `bool(ceiling)`, nothing else

Documented already in `README.md`, restated here because it's the kind of
placeholder that's easy to forget is still a placeholder once several other
things are built on top of it. Any test that exercises "containment" in this
codebase (`test_lineage.py`'s wider-child case included) is exercising the
*shape* of the containment check (does the seam get called with the right
arguments, does a missing ceiling get refused), never real semantic
containment. A malicious or merely careless `ceiling` string currently passes
as long as it's non-empty.

## 4b. (Fixed while building M9) `recall()`'s `truncated` flag could read False while entries were being dropped

Found building M9's `check_overload()` against a turn where the *labelled*
anchors alone (intent/objective/scope) already exhausted the turn budget
before the unlabelled loop started. The old logic set
`truncated = truncated or budget > 0` at the point of the first drop, which
is `False` whenever budget was already at or below zero — so a turn that
dropped 21 entries could still report `truncated=False`. Fixed to
`truncated = bool(dropped)`. All of M8's own tests passed before and after;
none had exercised the "anchors alone exhaust the budget" case, which is the
only reason this survived as long as it did. Recorded here rather than only
in M9's README since the bug and its fix are both in M8's file.

## 4. `still_live` computation in `wiring.py` is O(all live work items) per `end_task`

`_live_claim_refs` globs every `live_sets/*.jsonl` file and replays each one
on every single `end_task` call. Fine at M8's test scale (the spec's own
naive-default reasoning), but worth flagging now rather than rediscovering it
as a surprise once M9's corpus sweep (package 6) or any real workload starts
calling `end_task` at volume.
