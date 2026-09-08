# AI Development System — Conceptual Documentation Set

## Purpose of this documentation

This documentation is the current conceptual reference for a project whose long-term goal is to build a reproducible, locally deployable AI-assisted development system that remains effective under constrained model size and constrained working memory.

The documents are intentionally **not a technical specification**. They are meant to be refined until the major concepts become sufficiently clear, compatible, and testable that an implementation specification can later be derived from them without inventing missing semantics.

The set is deliberately modular. Each important converged idea has its own document so that later discussions can challenge one aspect without implicitly reopening every other decision.

> **Motto:** Stable enough to reason from; provisional enough to revise.

## Praxis

> It starts as a thesis.\
> Intuition, stemming, with no experience behind it yet.\
> We write it down. Each converged idea its own page.\
>
> Then we try to build it — in pieces, one increment at a time,\
> each piece carrying a question it has to answer.\
>
> The pieces strain.\
> The order we planned them in does not hold.\
> We rework the sequence. Then we rework it again.\
> The intuition was thinner than it looked, with no field beneath it.\
>
> So we stop adding.\
> We read — deeply, one paper at a time, sealed off from the rest.\
> We recurse. We review. We index. We select.\
> Each piece weighed, sorted, its origin kept.\
> This is information, not data.\
> Nothing is only gathered; everything is placed.\
>
> And only here, doing this, do we see it:\
> the reading is the knowledge model, run by hand,\
> at the scale of the whole project.\
> The method mirrors the mechanism.\
> We almost missed that. We named it just now.\
>
> Notice the symmetry. Do not build for it —\
> not until you can leverage it.\
>
> This is not a detour.\
> Every hunch, every rework, every paper\
> articulates into one thing:\
> the context of the change we will eventually make.\
> Entropy reduction is the product.\
> The context is assembled the slow way, on purpose.\
>
> There is no floor — only the ceiling, read from below,\
> from the place where space begins.\
> A richer context is a higher ceiling.\
>
> We build the thing by being the thing.

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
