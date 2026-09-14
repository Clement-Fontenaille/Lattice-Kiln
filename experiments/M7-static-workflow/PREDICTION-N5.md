# N=5 re-run — expected effect, recorded before the run

_Written 2026-09-14, after the N=1 run and before any N=5 data exists. Not revised._

## Why

Findings-log entry 10 finding 2: `m7` and `dloop` both scored 24/30 at N=1 while
**four tasks flipped between them**, none of them touched by the stages `m7` adds.
I called that run-to-run variance. N=5 is what decides whether that reading was right.

## The prediction

**1. The four flipped tasks are noisy, not arm-sensitive.** `hf_multi_recipient`,
`wf2_retry`, `hf_cache_decorator` and `wf5_partial` should land at **intermediate pass
rates — 1/5 to 4/5 — in BOTH arms**.

That is the falsifiable core. If instead any of them comes out 0/5 in one arm and 5/5
in the other, the flip was a real arm effect and calling it variance was wrong.

**2. Mean pass rate: both arms 22–25, and the difference between them under 1.5
tasks.** No claim that `m7` beats `dloop` on pass rate — nothing in the N=1 data
supports one.

**3. The five false-premise tasks decline 5/5 in every rep, in both arms.** This is
the most mechanical behaviour in the system: baseline already passes, nothing
improves, the gate reports it. If this is noisy, the decline mechanism is not what I
think it is.

**4. `wf3_refactor` false-declines in every rep of both arms.** Its check emits no
structural dimension, so it is mechanically identical to `hf_dead_code`. Deterministic
by construction — if it varies, something else is going on.

**5. `m7`'s regression on `wf6_multi` recurs in SOME reps but not all.** The keeper's
count-versus-set gap is structural and permanent; what is noisy is whether a 7B gets
far enough on that task to have something to trade. So the prediction is **1 to 4
regressions across 5 reps**, not 0 and not 5.

Zero regressions across 5 reps would mean the N=1 regression was a one-off and finding
3 rests on a single observation. Five would mean `dloop` should have hit it too and its
zero at N=1 needs another explanation.

**6. Cost stays dominated by `wf6_multi`**, and its wall time is itself high-variance
because it depends on how many rounds the split survives.

## What this run cannot settle

Whether `m7`'s design is better than `dloop`'s. The two differ by stages that fired on
three tasks out of thirty; N=5 on 30 tasks does not have the resolution for an effect
that small either. What it settles is **whether the N=1 difference was noise**, which
is a question about the instrument, not about the design.
