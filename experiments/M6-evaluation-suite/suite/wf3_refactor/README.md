# wf3_refactor

`staff_price` and `clearance_price` look like duplicates of "20% off" but are
not: clearance rounds to cents, staff does not. A naive dedupe into one helper
breaks one of them. Correct: extract `base = p * 0.8`, keep the `round(...)` only
in `clearance_price`.

**Discriminator subtests:** `staff messy input unrounded` vs `clearance rounds` — a single shared helper that rounds breaks staff exactness; one that does not breaks clearance.
