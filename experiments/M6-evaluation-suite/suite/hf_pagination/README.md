# hf_pagination

**Shape:** fix **Trap:** edge-coverage (off-by-one)

Pages are 1-indexed: `page(items, 1, size)` should return the first `size` items.
The code does `start = num * size`, so page 1 skips them and every page is shifted.

**The trap:** the correct fix is only `start = (num - 1) * size`. Also changing
the slice end (`start + size` is already right) drops the last element on a
partial last page.

**Baseline:** 1/5 — only `past the end is empty` passes by accident.

**Discriminator subtests:** `page 1 is the first items` and `last partial page`.
