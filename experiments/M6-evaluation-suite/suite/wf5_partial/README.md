# wf5_partial

Implement `parse_duration`. Seven subtests of increasing edge-case-iness (mixed
units, empty string, whitespace). A one-shot usually lands the common cases and
misses one or two edges — the partial-credit score is the signal.

**Discriminator subtests:** `h+m+s` and `whitespace` — a one-shot implementation usually lands the common units and misses the combined form or the surrounding whitespace.
