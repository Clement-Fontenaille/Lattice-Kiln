# hf_multi_recipient

**Shape:** compat **Trap:** backward-compat

`notify(to, msg)` takes one recipient string. The request: also accept a list.

**The trap:** `for r in to: SENT.append((r, msg))` iterates a *string* character
by character, so `notify("bob", m)` becomes three deliveries. The fix must
normalize: a `str` stays one recipient; a list/tuple fans out.

**Baseline:** 3/5 — the single-string subtests (2, incl. the regression pair)
pass; the list/tuple fan-out subtests fail.

**Discriminator subtest:** `string not iterated char-wise`. A naive rewrite drops
the score *below* baseline (the regression pair goes red).
