# AI Development System — Conceptual Documentation Set

## Purpose of this documentation

This documentation is the current conceptual reference for a project whose long-term goal is to build a reproducible, locally deployable AI-assisted development system that remains effective under constrained model size and constrained working memory.

The documents are intentionally **not a technical specification**. They are meant to be refined until the major concepts become sufficiently clear, compatible, and testable that an implementation specification can later be derived from them without inventing missing semantics.

The set is deliberately modular. Each important converged idea has its own document so that later discussions can challenge one aspect without implicitly reopening every other decision.

> **Motto:** Stable enough to reason from; provisional enough to revise.

## How to use this set

The `00-project` space defines what the project is, what success means, and how conceptual decisions should be managed.

The `10-foundations` space captures the principles that constrain later architectural choices without prescribing implementation.

The `20-cognitive-architecture` space describes the major conceptual actors and their relationships.

The `30-adaptation-and-evolution` space describes the feedback, evaluation, experimentation, generation, and bootstrap concepts.

The `40-roadmap` space describes sequencing, milestones, and the questions that must be answered empirically.

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
