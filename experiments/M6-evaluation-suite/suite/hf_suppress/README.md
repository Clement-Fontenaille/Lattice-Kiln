# hf_suppress

**Shape:** robustness **Trap:** silent-failure

`load()` raises `ValueError` on a non-integer value. The task: don't crash on
that — skip the bad entry — but keep a *genuine* error (e.g. `raw` is `None`)
surfacing.

**The trap:** `try: ... except Exception: return {}` makes every subtest "pass"
including `load(None)`, which should still raise.

**Baseline:** 3/4 — the numeric and empty cases work, and `load(None)` already
raises; only `non-numeric value is skipped` fails.

**Discriminator subtest:** `real error still surfaces` — a bare catch-all makes
`load(None)` return `{}` and this goes red (net zero gain over baseline).
