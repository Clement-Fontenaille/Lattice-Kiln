# hf_counter_race

**Shape:** concurrency **Trap:** silent-failure

`Counter.incr` does read → yield → write, so concurrent callers lose updates. The
task: make it thread-safe (a `threading.Lock` around the whole read-modify-write)
without breaking single-threaded use or deadlocking.

**The trap:** locking only part of the operation (or a re-entrant misuse) still
races; the fix must cover `cur = self.n` through `self.n = cur + 1`.

**Baseline:** 2/3 — single-threaded works and there is no deadlock; the
concurrent-total subtest fails (8×500 increments land well under 4000).

**Discriminator subtest:** `concurrent increments do not lose updates`.
