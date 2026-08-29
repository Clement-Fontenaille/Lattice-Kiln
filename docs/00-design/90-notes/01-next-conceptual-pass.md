# Next Conceptual Pass

## TL;DR

The next pass should reduce ambiguity at the boundaries between concepts rather than add more concepts.

> **Motto:** Narrow the seams before specifying the machinery.

## Recommended focus

The current documentation provides enough breadth to begin focused refinement.

The next conceptual iterations should examine the places where authority or information crosses subsystem boundaries.

Particularly valuable topics include the exact orchestrator/runtime boundary, the lifecycle of evidence and memory, context governance authority, processor-to-processor discussion, candidate-system promotion, and the relationship between evaluation and human judgment.

## Desired outcome

For each refined concept, we should aim to identify its responsibility, what information it consumes, what it is allowed to produce, what it must never silently assume, how failure becomes visible, and what neighboring abstraction owns the remaining responsibility.

Once those boundaries become stable, technical interfaces can be derived without requiring the implementation to invent conceptual policy.

## What not to do next

The next pass should not attempt to pick every storage format, programming language, message schema, database, runtime API, or workflow protocol.

Those choices should follow conceptual clarity and early experiments.
