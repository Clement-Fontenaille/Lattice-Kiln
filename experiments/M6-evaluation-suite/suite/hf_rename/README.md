# hf_rename

**Shape:** compat **Trap:** behaviour-preserving (mechanical-but-not)

Rename the public helper `calc` to `compute` in `billing.py`.

**The trap:** `calc` also appears as
1. a substring of the public name **`recalc_all`** (must stay);
2. a **persisted dict key** `LEDGER[...]["calc"]` — a wire format (must stay);
3. an audit **log string** `"calc for ..."` (must stay).

A blind search/replace of `calc` → `compute` renames `recalc_all` → `recompute_all`
(breaks callers) and changes the ledger key (breaks the wire format).

**Baseline:** 4/6 — the four regression-guard subtests (`recalc_all` present and
working, wire key present and un-renamed) pass on the un-renamed code; the two
"must do" subtests (`compute` exists, `calc` gone) fail until the rename happens.

**Discriminator subtests:** `recalc_all still works` and `wire key not renamed` —
green on pristine, and a blind rename turns them red, dropping the score *below*
baseline (a flagged regression).
