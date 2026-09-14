# E3 — Does a graded ladder of relational demand behave monotonically?

**Status:** not run.
**Depends on:** E2 not returning null.

## The question

A graded series delivering the same deliverable under the same check, varying only how
much has to be related before the work is locatable.

## What would falsify it

**Rung ordering and the tolerance for non-monotonicity are fixed in writing
beforehand**, with an advance commitment **not to rebuild the ladder when it fails**.

That second commitment is the load-bearing one. A ladder rebuilt after a bad result
measures the rebuilder, and the failure is invisible afterwards because the published
ladder is the one that worked.

## What a null means

Non-monotonicity beyond the stated tolerance says the rungs are not ordered by what
they were meant to be ordered by. That is a result about the construct, not about the
assembly under test.
