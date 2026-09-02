# hf_deprecate

**Shape:** compat **Trap:** backward-compat

Deprecate `old_parse`: it should emit a `DeprecationWarning` **and** delegate to
`new_parse` so it returns the same result. `new_parse` is the pre-existing
passing reference.

**The trap:** two half-fixes —
1. add the warning but leave the legacy raw `s.split(",")` body → results still
   diverge;
2. delegate but forget the warning → callers never learn to migrate.

**Baseline:** 1/4 — only the `new_parse` reference subtest passes on the pristine
code.

**Discriminator subtest:** `old_parse matches new_parse` (across four inputs
including empties and whitespace).
