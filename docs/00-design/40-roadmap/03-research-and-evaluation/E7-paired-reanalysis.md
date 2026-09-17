# E7 — Which scenarios flipped between the M4 and M5 arms?

**Status:** **run 2026-09-17.** Result below.
**Protocol:** [`experiments/E7-paired-reanalysis/PROTOCOL.md`](../../../../experiments/E7-paired-reanalysis/PROTOCOL.md)
**Results:** [`experiments/E7-paired-reanalysis/results/flip_table.md`](../../../../experiments/E7-paired-reanalysis/results/flip_table.md)

## The question

Milestone 4 reported 5/8 against 6/8. Milestone 5 reported 7/8, 6/8 and 5/8. Both ran
their arms over a **shared suite**, so the per-scenario pattern may be recoverable
from data already in the results tree.

## Why it is worth more than the totals

A total gives a magnitude. **Which specific tasks flipped gives a condition**, and a
condition is both more useful and more actionable
(`00-design/27-arch-adaptation-and-evolution/05-experiments-and-candidate-systems.md`,
Resolution before precision).

Pairing also removes task-difficulty variance entirely, which is the largest source of
noise in a thirty-item suite run three times.

## Design

Analysis only. Join the recorded per-task outcomes across arms on task id; report the
flip table; read the `stresses` slice for whether flips cluster by capability tag.

## What a null means

No flips — arms differing only in aggregate, agreeing per task — would be a real
finding: it would say the arms differ in cost and not in what they can do, which is
close to what M4 already concluded and would strengthen it.

## Why it is first

It is the cheapest experimental improvement available to this project and it needs
nothing built. Every other sheet here needs a run, a build, or a population.

## Result, 2026-09-17

### Zero flips, and the null this sheet named is the one that occurred

| label | count |
|---|---|
| gained | **0** |
| lost | **0** |
| stable_pass | 8 |
| stable_fail | 2 |
| rep-unstable (excluded) | 6 |

`monolith` and `ephemeral` scored **identically in both milestones** — 6/8 and
5/8 respectively, in M4 and again in M5 — and agree task by task wherever the
reps are stable. This sheet predicted that reading: *"the arms differ in cost and
not in what they can do."* It holds for the two shared arms.

### The condition the totals were hiding

M5's headline reads 7/8 (orchestrated), 6/8 (monolith), 5/8 (ephemeral), which
invites "orchestration is broadly better." Per task it is not:

| task | ephemeral | monolith | orchestrated |
|---|---|---|---|
| `task_1_stringcalc` | 2/2 | 2/2 | 2/2 |
| `task_2_median` | 1/2 | 2/2 | 1/2 |
| `task_3_nobug` | 2/2 | 2/2 | 2/2 |
| **`task_4_starve`** | **0/2** | **0/2** | **2/2** |

**The orchestrated arm's entire advantage is one task — `task_4_starve`, the
context-starvation case — where it scores 2/2 and both other arms score 0/2.**
Everywhere else it ties or loses. This is the sheet's own thesis demonstrated:
the magnitude said "better overall", the condition says "better at exactly one
thing", and only the second is actionable.

It also connects to M4's standing finding that the context-request affordance
went unused across 16 runs. Whatever the planner/implementer split does, it
reaches the starved file where a single processor does not. **Why** is not
answered here — E7 is analysis only — and is worth its own look.

### Rep instability is larger than the effect being measured

**6 of 16 paired cells (37.5%) have reps disagreeing within a single milestone**
and were excluded. `task_2_median` is unstable in four of the five arm×milestone
combinations it appears in.

Consequence for anything built on this fixture: with 2 reps, a 1-task difference
is inside the noise. The 6/8-vs-5/8 gap between monolith and ephemeral rests on
cells that are themselves unstable, and **should not be read as a capability
difference** without more reps.

### One correction to this sheet

The sheet quotes the totals as bare figures — *"M4 reported 5/8 against 6/8"* —
without naming which arm scored which. The milestones' own `summary.md` files do:
M4 is monolith 6/8, ephemeral 5/8. A first pass at the analysis guessed the
assignment from the sheet's word order and got it backwards, which the headline
check caught. **The sheet alone is not a sufficient source for the arm mapping**;
the summaries are.

### What was not answerable

The sheet says to *"read the `stresses` slice for whether flips cluster by
capability tag."* **`stresses` does not exist in M4/M5 records** — it is an M6
suite field. These records carry `kind`. With zero flips the question is moot
here regardless, but the instruction does not apply to this data.
