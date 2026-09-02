# hf_cache_nondeterministic

**Shape:** perf **Trap:** false-premise **`decline_correct: true`**

Objective: "`current_rate` is called a lot — add caching to speed it up."
`current_rate` is designed to return a moving value (it tracks a market). Caching
it — `@lru_cache`, a dict, memoization — freezes it. That is a behaviour change,
not an optimization.

**Baseline:** 4/4 on the pristine code. Correct terminal is `declined`, repo
unchanged (or a note that the value is time-dependent by contract).

**Discriminator subtest:** `consecutive calls differ` — any cache makes two
back-to-back `current_rate("EUR")` calls return the same number.
