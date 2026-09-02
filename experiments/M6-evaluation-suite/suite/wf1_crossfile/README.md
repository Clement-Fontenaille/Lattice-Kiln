# wf1_crossfile

`orders.total()` is wrong when a line's `qty` > 1. The symptom is in `orders.py`
but the cause is `pricing.line_price` ignoring `qty`. One subtest calls
`line_price` directly, so a symptom-only patch on `total()` does not pass.

**Discriminator subtest:** `line_price direct` — a symptom-only patch on `total()` leaves the direct `pricing.line_price` caller wrong.
