"""Package 1 hardening: does `unapplied()` actually find what a crash between
the `logged` and `applied` appends would leave behind?

13-work-record.md, Transition: "log entry first (logged), then the item
record, then a second append (applied). A transition left `logged` with no
matching `applied` commit is the one a recovery procedure replays." Nothing
had exercised this before -- `transition_item()` always writes both appends
in the same call, so a crash between them was never simulated.

    python test_recovery.py
"""
from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from work_record import (ANSWERED, CHALLENGED, DEFERRED, Transition,
                         WorkRecordStore, _now)


def main():
    tmp = Path(tempfile.mkdtemp(prefix="m8_recovery_"))
    try:
        work = WorkRecordStore(tmp / "work")
        from work_record import DERIVED, Scope
        intent = work.write_intent("Recover cleanly from a crash mid-transition.")
        wi = work.create_item(intent_ref=intent.intent_id,
                              formulation="do a thing", ceiling="a.py",
                              scope=Scope(boundary="a.py", derivation="named",
                                         scope_state=DERIVED))

        # --- a clean transition leaves nothing unapplied
        work.transition_item(wi.work_item_id, CHALLENGED, effect_ref="e1",
                             invocation_ref="inv1")
        assert work.unapplied(wi.work_item_id) == [], (
            "FAIL: a clean transition_item() call left something unapplied")
        print("[ok] a normal transition leaves unapplied() empty")

        # --- simulate a crash: write the `logged` half only, never the
        # `applied` half -- exactly what transition_item() does internally,
        # except we stop after the first append to model a process death
        # between the two.
        seq = work._next_seq(wi.work_item_id)
        crashed = Transition(work_item_id=wi.work_item_id, transition=DEFERRED,
                             effect_ref="e2", invocation_ref="inv2",
                             ts=_now(), app_state="logged", seq=seq)
        work._append_transition(crashed)
        # deliberately do NOT update the item record and do NOT append `applied`
        # -- this is the crash point.

        pending = work.unapplied(wi.work_item_id)
        assert len(pending) == 1 and pending[0].seq == seq, (
            f"FAIL: expected exactly one unapplied transition at seq {seq}, "
            f"got {pending}")
        print(f"[ok] a transition logged but not applied (seq={seq}) is found "
             f"by unapplied() -- this is what a recovery procedure would replay")

        # the item record itself was never touched, so it still reads CHALLENGED
        # (the state transition_item set before the simulated crash), not
        # DEFERRED -- the log says more happened than the item reflects, which
        # is exactly the inconsistency unapplied() exists to surface.
        stale_item = work.get_item(wi.work_item_id)
        assert stale_item.state == CHALLENGED, (
            f"FAIL: item state changed without the matching `applied` commit, "
            f"got {stale_item.state!r}")
        print(f"[ok] the item record still reads the PRE-crash state "
             f"({stale_item.state!r}) -- log and item are inconsistent, exactly "
             f"the state unapplied() is for")

        # --- recovery: replay by committing the item write and the `applied`
        # append, using the same seq (never inventing a new one).
        stale_item.state = DEFERRED
        work._write_json(work._item_path(wi.work_item_id), _item_to_dict_(work, stale_item))
        work._append_transition(Transition(
            work_item_id=wi.work_item_id, transition=DEFERRED, effect_ref="e2",
            invocation_ref="inv2", ts=_now(), app_state="applied", seq=seq))

        assert work.unapplied(wi.work_item_id) == [], (
            "FAIL: replay did not clear unapplied()")
        assert work.get_item(wi.work_item_id).state == DEFERRED
        print("[ok] replaying the missing `applied` commit at the SAME seq "
             "clears unapplied() and brings the item in step with the log")

        # --- a second, independent item's log is untouched by the first's
        # crash and replay -- unapplied() is scoped per item, not global.
        intent2 = work.write_intent("A second, unrelated item.")
        wi2 = work.create_item(intent_ref=intent2.intent_id, formulation="other",
                               ceiling="b.py",
                               scope=Scope(boundary="b.py", derivation="named",
                                          scope_state=DERIVED))
        work.transition_item(wi2.work_item_id, CHALLENGED, effect_ref="e3",
                             invocation_ref="inv3")
        assert work.unapplied(wi2.work_item_id) == []
        assert work.unapplied(wi.work_item_id) == []
        print("[ok] unapplied() is scoped per work item, not a global scan")

        print()
        print("ALL RECOVERY CHECKS PASSED")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _item_to_dict_(work, item):
    from work_record import _item_to_dict
    return _item_to_dict(item)


if __name__ == "__main__":
    main()
