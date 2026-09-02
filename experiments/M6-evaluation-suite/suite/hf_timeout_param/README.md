# hf_timeout_param

**Shape:** feature **Trap:** edge-coverage

Add `timeout=None` to `fetch(url)`. `None` = no timeout (existing callers keep
working). A positive budget raises `TimeoutError` for a URL in `_SLOW`.

**The trap:** `timeout=0` must be a *zero budget* — a slow fetch times out
immediately. `if timeout:` treats `0` as falsy and behaves like `None`.

**Baseline:** 2/6 — the two no-timeout calls work on the pristine code; the rest
need the new parameter.

**Discriminator subtest:** `timeout=0 still times out`.
