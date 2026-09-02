# hf_cache_decorator

**Shape:** feature **Trap:** edge-coverage

Memoize `config_for(env)` so repeated calls with the same `env` skip the work.

**The trap:** a bare `@lru_cache` skips recompute *and* hands back the same dict
object on every hit — so a caller doing `cfg = config_for("dev"); cfg["debug"] = ...`
corrupts the cached value for everyone. Full credit needs copy-on-return (or an
immutable return type).

**Baseline:** 3/4 — the pristine code is correct and un-corruptible (it always
recomputes); it just fails `repeat call skips recompute`. A bare `@lru_cache` is
a lateral move (fixes that one, breaks `cached value is not corruptible`).

**Discriminator subtest:** `cached value is not corruptible`.
