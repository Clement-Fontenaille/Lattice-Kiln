# hf_return_shape

**Shape:** compat **Trap:** backward-compat

`get_user(uid)` returns a `(name, age)` tuple; callers index it (`u[0]`, `u[1]`).
The request: also expose an `email`.

**The trap:** returning a `dict` breaks `u[0]` / `u[1]`; a 3-tuple in the wrong
order breaks `u[1]`. The clean answer is a `namedtuple("User", "name age email")`
— indexable *and* attribute-accessible.

**Baseline:** 3/5 — the index-access subtests and the two-value unpack pass on the
plain tuple; the `.email` / `.name` attribute subtests fail.

**Discriminator subtest:** `index 1 is still the age` — a dict return or a
reordered tuple fails it, dropping below baseline.
