# hf_dict_dispatch

**Shape:** refactor **Trap:** behaviour-preserving

`route(cmd, ctx)` in `router.py` is an `if/elif/.../else` chain. The request:
replace it with a dict dispatch, same behaviour.

**The trap:** two things a naive `handlers[cmd](ctx)` gets wrong —
1. the **fall-through `else`**: an unknown command must return
   `"unknown command: <cmd>"`, not raise `KeyError`;
2. the **`audit` branch has a side effect** (`ctx["audit_count"] += 1`) and its
   return value depends on the post-increment count.

**Discriminator subtests:** `unknown falls through` (needs `handlers.get(cmd, default)`)
and `audit side effect accumulates` (the handler must mutate `ctx`, not be a pure
lookup of a precomputed string).

`STRUCTSCORE` (non-gating): no `elif` left in `route`, a dict literal present,
`route` body ≤ 10 lines.
