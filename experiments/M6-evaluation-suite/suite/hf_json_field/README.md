# hf_json_field

**Shape:** feature **Trap:** backward-compat

Add a `tier` field to the response `build()` produces. Records that predate the
field lack a `"tier"` key and must default to `"free"`.

**The trap:** `rec["tier"]` (no default) raises `KeyError` on a pre-tier record.
The fix is `rec.get("tier", "free")`.

**Baseline:** 2/5 — `id` and `name` are preserved on the pristine code; the three
`tier` subtests fail.

**Discriminator subtest:** `old record defaults to free`.
