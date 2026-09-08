# AI Development System — Conceptual Documentation Set

## Purpose of this documentation

This documentation is the current conceptual reference for a project whose long-term goal is to build a reproducible, locally deployable AI-assisted development system that remains effective under constrained model size and constrained working memory.

The documents are intentionally **not a technical specification**. They are meant to be refined until the major concepts become sufficiently clear, compatible, and testable that an implementation specification can later be derived from them without inventing missing semantics.

The set is deliberately modular. Each important converged idea has its own document so that later discussions can challenge one aspect without implicitly reopening every other decision.

> **Motto:** Stable enough to reason from; provisional enough to revise.

## Praxis

> We build the thing by being the thing.\
>
> Every paper read, every claim weighed,\
> every piece kept, cut, or moved —\
> that is the knowledge model, run by hand,\
> at the scale of its own design.\
>
> We gather information, not data:\
> each piece placed, weighted, its origin kept.\
> Name its kind as it lands.\
> Sorting it now is cheap; sorting the pile later is not.\
>
> Entropy reduction is the product here too.\
> The context is assembled the slow way, on purpose.\
>
> There is no floor — only the ceiling, read from below,\
> from the place where space begins.\
> A richer context is a higher ceiling.\
>
> Theory is fed by doing.\
> So we do.

## How to use this set

The `00-project` space defines what the project is, what success means, and how conceptual decisions should be managed. `05-vocabulary.md` fixes shared definitions the set uses without defining — starting with **harness**.

The `10-foundations` space captures the principles that constrain later architectural choices without prescribing implementation.

The `20-cognitive-architecture` space describes the major conceptual actors and their relationships.

The `30-adaptation-and-evolution` space describes the feedback, evaluation, experimentation, generation, and bootstrap concepts.

The `40-roadmap` space describes sequencing, milestones, and the questions that must be answered empirically. Milestones live one per file in `01-MILESTONES/`, where a milestone's number is a **stable identifier rather than a position in a queue**. What order they are worked in — and what has been changed upstream but not yet carried downstream — lives in `00-backlog.md`, in four priority bands. `40-roadmap/README.md` describes how that space is maintained.

The `50-findings` space is the append-only empirical record: one entry per completed milestone, stating what its evidence question answered. Entries are cited by number and are never rewritten.

The `90-notes` space contains working conventions for future conceptual passes.

## Current conceptual status

The architecture described here should be treated as a **working hypothesis**. The project should preserve conceptual traceability while remaining willing to simplify, split, merge, or discard abstractions when practical evidence contradicts them.

The intended progression is:

```text
conceptual model
    ↓
refined conceptual model
    ↓
explicit contracts and unresolved choices
    ↓
technical specification
    ↓
implementation
    ↓
observed behavior
    ↓
conceptual revision where necessary
```

The documentation should therefore remain useful both before implementation and after the system begins to evolve.
