# m7b — expected effect, recorded before the run

_2026-09-14, written before `m7b_workflow.py` was executed. Not revised afterwards._

## What changed, and which changes can move a number

Five remediations from `INVENTORY.md`. Separating them matters, because a variant that
changes five things at once cannot attribute its result.

**Measurable — these can move the score:**

- **R1. The keeper compares the set of failing checks, not the count.** Strictly more
  conservative: it rejects candidates `m7` accepted.
- **R2. A 180-second wall governor per task**, alongside the existing call cap. One
  task took 356 s under `m7`.

**Free — no expected effect on pass, regressions or declines:**

- **R3.** `blocked` splits into `blocked-no-progress` and `blocked-partial`. A record
  change; the work is identical.
- **R4.** The audit returns `segments` rather than a boolean, so the model signal can
  actually split. Under `m7` it fired alone once, on `hf_csv`, and did nothing.
- **R5.** The `classification` field is retired from prompt and record. Thirty were
  produced and nothing consumed one. It rode an existing call, so no call is saved.

## The prediction

**1. The `wf6_multi` regression disappears.** This is what R1 is for and it is the one
thing R1 must deliver. Anything else is a bonus.

**2. And `wf6_multi` gets *worse* on the score.** Under `m7` it reached combined 10
**by accepting the losing trade**. R1 rejects that candidate, so it should fall back
toward 2 and land in `blocked-no-progress`. **I expect to trade progress for safety on
this task and I am predicting the loss rather than hoping it does not happen.**

**3. Overall pass: 22–25, most likely at or just below `m7`'s 24.** R1 can only remove
accepted candidates, never add them. Any task where the model fixed several checks and
broke one now keeps the incumbent.

**4. Regressions: 0.** If R1 does not deliver zero, it is implemented wrong — the
keeper and the harness now read the same `fails` label set.

**5. Decline accuracy 5/5, and `wf3_refactor` still false-declines.** Untouched by all
five remediations. R6 is a formulation repair and no code change reaches it.

**6. Wall clock drops below `m7`'s 13.7 min**, mostly from R2 capping `wf6_multi` at
180 s instead of 356.

**7. The concern split fires on more than 3 of 30.** Under `m7` only the two tasks
with `(1)(2)(3)` markers could actually split. With R4 the model can segment prose,
and `hf_csv` is the known case. **If it still fires on exactly 3 and splits on 2, R4
did not work.**

## What would falsify each remediation

| | falsified if |
|---|---|
| R1 | a regression survives, or the pass rate drops by more than 2 |
| R2 | the longest task still exceeds ~200 s |
| R3 | the two blocked kinds do not split roughly 5 / 3 as in the `m7` run |
| R4 | the split still acts on 2 tasks only |
| R5 | nothing — it is a deletion, and its point is that nothing changes |

R5 is the honest one to watch. **If retiring a field changes any outcome, the influence
record was lying about what consumed it**, and that matters more than the field did.

## What this run cannot settle

Whether `m7b` is better than `m7`. `dloop` at N=5 varied by 3 tasks against itself
(24 23 24 22 25), so a one-run difference of one or two tasks means nothing. This is
N=1 and it is a **defect check**, not a comparison: does R1 remove the regression, does
R2 bound the cost, does R4 make the stage act. The comparison needs N=5 and comes after.
