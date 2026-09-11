# AI Development System — Conceptual Documentation Set

## Purpose of this documentation

This documentation is the current conceptual reference for a project whose long-term goal is to build a reproducible, locally deployable AI-assisted development system that remains effective under constrained model size and constrained working memory.

The documents are intentionally **not a technical specification**. They are meant to be refined until the major concepts become sufficiently clear, compatible, and testable that an implementation specification can later be derived from them without inventing missing semantics.

The set is deliberately modular. Each important converged idea has its own document so that later discussions can challenge one aspect without implicitly reopening every other decision.

> **Motto:** Stable enough to reason from; provisional enough to revise.

## Praxis

The project's working stance is the **Praxis** stanza in the [root README](../../README.md). That is the canonical copy; it is not duplicated here.

## How to use this set

The `00-project` space defines what the project is, what success means, and how conceptual decisions should be managed. `05-vocabulary.md` fixes shared definitions the set uses without defining — starting with **harness**.

The `10-foundations` space captures the principles that constrain later architectural choices without prescribing implementation.

The architecture space is split by concern rather than held in one folder, since only one of its parts is a reasoning or coordinating actor — the rest are resources or constraints those actors operate with, on, or under. `20-arch-runtime.md` is the entry point and states the split. `21-arch-knowledge-model` and `23-arch-context-management` realize `10-foundations/03` and `04` respectively. `22-arch-cognition` holds the actors: task representation, processors, the orchestrator, decomposition. `24-arch-permission-layer` and `25-arch-invariant-layer` hold what an actor may request and what may never happen regardless. `26-arch-observability` holds what has to be reconstructable after the fact. `28-arch-work-record` holds intent and the work derived from it durably, realizing the model `22-arch-cognition/01` defines but does not store.

The `27-arch-adaptation-and-evolution` space describes the feedback, evaluation, experimentation, generation, and bootstrap concepts.

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
