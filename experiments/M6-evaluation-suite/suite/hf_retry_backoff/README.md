# hf_retry_backoff

**Shape:** robustness **Trap:** silent-failure

Add retry to `Sender.send`: a `Transient` failure is retried up to 3 extra times
(4 attempts total), then the last `Transient` is re-raised.

**The trap:** a `Permanent` failure must be raised immediately — retrying it wastes
attempts and delays a hard failure. A "retry any exception" loop keeps hammering.

**Baseline:** 2/4 — `happy path` works and `permanent` already raises on attempt 1
(no retry loop yet); the two `Transient` cases fail.

**Discriminator subtest:** `permanent is not retried` — a blanket retry makes
`permanent` end at attempt 4.
