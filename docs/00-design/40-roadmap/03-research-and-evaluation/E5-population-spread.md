# E5 — How much does the operator account for the outcome?

**Status:** not run.
**Blocked on:** an operator population. `70-THINKING/01-use-cases.md` §2 is empty.

## The question

Hold model and scaffold fixed; vary the operator. Two defined arms:

- the request verbatim, with no configuration;
- a hand-authored objective with named files, stated constraints, and permitted
  correction.

## Why it is different from everything else here

This measures **accessibility rather than capability**
(`00-design/10-foundations/07-the-integrated-system-and-its-operator.md`), and it is
the only item in this folder that measures **the assembly** rather than a
sub-assembly. Every other experiment holds the operator constant and therefore scores
the system minus the person using it.

## The design constraint that decides whether it measures anything

**The expert arm must be expert-in-process, not expert-in-this-task's-answer.** An
operator who knows the answer is not configuring the system, they are supplying the
result, and the arm then measures nothing about accessibility.

## What a null means

No spread across operators, with the arms genuinely differing, would undercut
`10-foundations/07`'s central claim that the operator is part of the assembly being
measured.
