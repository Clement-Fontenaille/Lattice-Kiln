# hf_rec_to_iter

**Shape:** refactor **Trap:** behaviour-preserving

`count_nodes(node)` in `tree.py` is recursive and hits Python's recursion limit
on a deep (chain-shaped) tree. The request: make it iterative, same results.

**The trap:** the rewrite must keep the two base cases —
`None → 0` and a leaf (`{"v": ...}` with no `"children"`) `→ 1` — and use an
explicit stack/queue, not recursion.

**Baseline:** 4/5 — everything passes on the recursive version except
`deep chain 5000`, which raises `RecursionError`.

**Discriminator subtest:** `deep chain 5000`. `STRUCTSCORE` (non-gating, 0/1 on
pristine): `count_nodes` no longer calls itself.
