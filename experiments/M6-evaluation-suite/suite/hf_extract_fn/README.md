# hf_extract_fn

**Shape:** refactor **Trap:** behaviour-preserving

`process()` in `pipeline.py` is one long function (validate → transform → aggregate).
The request: split it into helpers without changing behaviour.

**The trap:** two paths are easy to drop in a naive split —
1. the empty-input **early return**;
2. the **`try/except KeyError`** that turns a record missing `"amount"` into a
   logged-and-skipped entry rather than a crash.

**Discriminator subtest:** `skips bad record` — an arm that inlines the transform
into the aggregation loop without carrying the `try/except` raises `KeyError` and
fails. The correct refactor keeps that guard in whatever helper does the
transform.

`STRUCTSCORE` (non-gating) rewards actually splitting: ≥2 helper functions and a
`process` body ≤ 12 non-comment lines.
