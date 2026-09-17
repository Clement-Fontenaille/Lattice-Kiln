# E7 — Which scenarios flipped between the M4 and M5 arms?

**Status:** not run. **Needs no new runs and no decisions.**
**Protocol:** [`experiments/E7-paired-reanalysis/PROTOCOL.md`](../../../../experiments/E7-paired-reanalysis/PROTOCOL.md)

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
