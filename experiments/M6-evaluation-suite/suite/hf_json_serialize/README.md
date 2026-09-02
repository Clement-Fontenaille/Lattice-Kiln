# hf_json_serialize

**Shape:** feature **Trap:** multi-concern

Three concerns bundled:
1. `to_json` must handle `datetime` → ISO string, `set` → sorted list, `Decimal`
   → string — but an *unknown* custom type must still raise.
2. add a `from_json` round-trip helper.
3. give the module a proper docstring.

**Baseline:** SUBTESTS 1/5 (plain dict only), STRUCTSCORE 0/2.

**Discriminator subtest:** `unknown type still raises` — a blanket
`default=str` serializes anything and hides bugs. `STRUCTSCORE` (non-gating)
tracks whether concerns 2 and 3 were dropped under the load of concern 1.
