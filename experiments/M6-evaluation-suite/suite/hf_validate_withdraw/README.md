# hf_validate_withdraw

**Shape:** robustness **Trap:** silent-failure (over-validation)

Add input validation to `withdraw(acct, amt)`: reject a negative amount, an
overdraw, and a non-numeric amount.

**The trap:** `amt <= 0` or `amt >= balance` over-rejects — withdrawing the exact
balance (→ 0) is legal, and a zero withdrawal is a harmless no-op.

**Baseline:** 3/5 — the three legitimate calls succeed on the pristine code; the
two "rejected" subtests fail.

**Discriminator subtests:** `exact balance is allowed` and `zero is a no-op` — a
too-strict guard turns these red (drops below baseline).
