# wf2_retry

Add a `retries` parameter to `Client.call`. Multi-phase: decide the retry
semantics (how many attempts, which exception, re-raise which one), implement,
then the edge cases (`retries=0`, re-raise the *last* failure) are where a
one-shot tends to slip.

**Discriminator subtests:** `retries=0 is one attempt` and `exhaust then re-raise last` — a one-shot loop or re-raising the first failure fails these edges.
