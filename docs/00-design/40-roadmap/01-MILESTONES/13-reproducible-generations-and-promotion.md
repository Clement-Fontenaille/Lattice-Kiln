# M13 — Reproducible generations and promotion

**State:** open
**Was:** M11, before rework 2
**Design:** [`06-system-generations.md`](../../30-adaptation-and-evolution/06-system-generations.md)

## What this milestone is

Define trusted system generations, lineage, candidate variants, promotion,
rejection, rollback, and bootstrap reconstruction.

At this point the system itself becomes an experimental artifact.

## Why the invariant list already refers to it

Invariant **H3** — *no in-place modification of trusted configuration; no
automated promotion* — refuses **every** promotion effect (type 8) outright,
because there is no promotion pipeline for one to be legitimate against. That
blanket refusal is scoped to hold *until this milestone exists*.

This milestone is therefore the one that makes a currently-total prohibition into
a conditional one. That is a floor change, and it is made against
[M11](11-safety-response.md)'s literature pass rather than on this milestone's own
judgment.

## Evidence question

*Not yet stated.* The relevant question when it is written is less "can generations
be packaged" than "does a promoted generation carry the improvement to a fresh
instance" — which is [M16](16-bootstrap-generation-closure.md)'s subject and
suggests these two may want a shared evidence question.
