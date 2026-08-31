# Loop-lab (bundle D) — findings

**Date:** 2026-09-01
**Model:** `qwen2.5-coder:7b-instruct-q4_K_M`. 6 workflow tasks × 3 arms × 2 reps
= 36 runs, `MAX_ROUNDS=3`, `STALL_TOL=1`.
**Question:** given the judge-lab result (reviewer verdict unreliable, test result
reliable), can loop control be driven off the measurable signal so the
implement↔review loop stops thrashing on a bad reviewer and never ships worse
than it started?

Arms: `oneshot` (implementer once) / `naive_loop` (`(reviewer→implementer)*`
while the reviewer says needs-change, return last state — what the current `fixed`
arm does) / `d_loop` (bundle D). Table: `results/summary.md`.

## Result

| task | oneshot | naive_loop | d_loop | notes |
|---|---|---|---|---|
| wf1 crossfile (/5) | 5.0 | 5.0 | 5.0 | all pass; d_loop in 1 call vs naive's 2 |
| wf2 retry (/5) | 3.0 | 5.0 | 5.0 | loop earns its keep; **d_loop 2 calls, naive 4** |
| wf3 refactor (/5) | 5.0 | 5.0 | 5.0 | **d_loop 0 calls — and did no work (see limits)** |
| wf4 false premise (/5) | 5.0 | 5.0 | 5.0 | **d_loop 0 calls, by construction**; naive 4–6 calls |
| wf5 partial (/7) | 5.0 | **7.0** | 6.0 | naive wins — d_loop's stall-stop too eager |
| wf6 multi (/6) | 1.0 | **0.0** | **2.0** | naive *destroyed* it; d_loop held the floor |

| arm | obj pass | regressions vs baseline | model calls (36 runs) |
|---|---|---|---|
| oneshot | 6/12 | 1 | 12 |
| naive_loop | **10/12** | **2** | 48 |
| d_loop | 9/12 | **0** | **14** |

## What bundle D bought

**1. Zero regressions, as a hard guarantee.** The pre-existing repo state is an
entrant in the keeper pool; a round's output is accepted only if it *beats* it;
the best snapshot ever seen is what ships. Across 12 runs d_loop never ended below
its baseline. `naive_loop` regressed twice — both on wf6, where the review/fix
loop drove the implementer's shaky output to **non-parsing Python and the
reviewer approved it** (`reviewer-approved`, final `0/0`). An unreliable reviewer
driving a loop *amplifies* damage; a test-gated keeper caps it.

**2. wf4 (false premise) solved by construction, for free.** The incumbent linear
scan passes 5/5, so d_loop's loop never runs — `rounds=0, calls=0,
terminal=resolved`. `naive_loop` also reached 5/5 but spent 4–6 calls to get
there (the implementer churns, the reviewer eventually approves something that
happens to still pass). d_loop doesn't need to *recognise* the false premise — it
just refuses to accept a change that doesn't beat a passing incumbent.

**3. ~3.4× cheaper than `naive_loop`** (14 vs 48 calls) because it stops on a
green test instead of waiting for a reviewer to say approve, and skips the loop
entirely when the incumbent already passes (wf3, wf4 → 0 calls).

**4. Its worst case is honest.** wf6: both reps ended `no-improvement`,
`best_src=incumbent`, `kept_best=True` — "I could not improve this; here is the
untouched original" — escalation, not a false claim of success. Contrast
`naive_loop`'s wf6: shipped broken code, `reviewer-approved`.

## Limits found

**A. "First, do no harm" degrades to "do nothing" when the test does not capture
the deliverable.** wf3 is a pure behaviour-preserving refactor. Its check tests
behaviour, not "duplication removed". The pristine `discounts.py` already passes
5/5, so d_loop stops at `calls=0` having done no refactor at all — a free "pass"
it did not earn. Any task whose objective is not fully expressed by an executable
check needs a second signal (a structural check, or a human) or d_loop will
no-op it.

**B. `STALL_TOL=1` stops too early on climbable tasks.** wf5 rep 1: round 0 got
5/7, rounds 1–2 did not improve, d_loop stopped at 5/7. `naive_loop` got 7/7 in a
single review/fix round the same day. When round 0 is mediocre, one more nudge
sometimes lands; the aggressive stall-stop leaves subtests on the table. Cheap to
tune (`STALL_TOL=2`, or "stop only if no round in the last 2 improved").

## Composed picture

Bundle D + the judge-lab result give a coherent loop for a 7B fixed sequence:

- **Gate the loop on the test, not the reviewer verdict** (judge-lab: verdict is
  systematically approve-biased; test is 9/10).
- **Keep the incumbent as the floor; ship the best snapshot, not the last**
  (0 regressions; caps a bad reviewer's damage; solves false premises for free).
- **Escalate on stall instead of thrashing** (wf6: "here's the untouched
  original" beats "shipped broken, approved").
- **Unresolved:** behaviour-preserving work (refactors) has no test signal to
  drive or verify it — needs a structural check or a human in the loop. This is
  where the "generate the missing tests, blind, K-way" experiment (judge-lab
  follow-up) and a human-review affordance both point.
