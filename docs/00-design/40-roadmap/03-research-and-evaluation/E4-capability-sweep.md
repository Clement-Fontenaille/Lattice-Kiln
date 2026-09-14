# E4 — How does the suite behave across model size and tuning?

**Status:** not run.
**Gated on:** E0. Running a sweep with an uncharacterised instrument produces
differences that cannot be attributed.

## The question

The existing suite across models. **Size and tuning, not size alone.**

## Why the design must vary both

Tuning reshapes results unevenly across domains, so a size-only design cannot separate
a capability effect from a tuning artifact. A sweep that varies size and holds tuning
uncontrolled will report a capability curve that is partly a tuning curve, and nothing
in the result says which part.

## What a null means

Flat across sizes, with the instrument validated, is a strong result: it says the
suite measures something the models under test do not differ on, which bounds what the
suite can ever discriminate.
