# Orchestrator / Runtime Boundary (v0)

**Traces to:** `00-design/10-foundations/02-reasoning-vs-runtime.md`,
`00-design/20-cognitive-architecture/05-runtime.md`,
`00-design/20-cognitive-architecture/03-orchestrator.md`,
`00-design/90-notes/01-next-conceptual-pass.md`,
`00-design/40-roadmap/01-MILESTONES/completed/05-intelligent-orchestration.md` (M5);
binds to `10-technical/06-processor-contract.md`,
`10-technical/08-orchestrator-contract.md`,
`10-technical/01-effect-vocabulary.md`,
`10-technical/04-enforcement-gate.md`.

## TL;DR

Exactly two things cross from the reasoning side (orchestrator + processors) to
the runtime: a **proposed effect** and a **processor-invocation request**.
Exactly three things cross back: an **effect result** (or typed refusal), an
**assembled context**, and an **objective signal** where one exists. Nothing
else. The runtime validates the four properties plus the deny-list gate and makes
**no semantic judgment** about the work.

> **Motto:** The model proposes; the runtime makes it real — and checks only what it can check without understanding.

## Status of this document

v0 for Milestone 5. It narrows the "how much does the runtime validate?" open
question (`02-reasoning-vs-runtime.md`, `05-runtime.md`) to a concrete MVP
answer, and fixes the crossings and the assumptions each side may not make. The
placement of the gate relative to the runtime stays open
(`07-invariant-enforcement.md`); the call *order* is pinned here.

## Narrowing

`90-notes/01-next-conceptual-pass.md` flags "the exact orchestrator/runtime
boundary" as the highest-value seam to narrow before specifying machinery. This
document does that narrowing. Discarded alternatives are named under each
crossing and under Validation depth.

## The crossings

### Reasoning → runtime

| Crossing | Payload | Not allowed |
|---|---|---|
| **Proposed effect** | typed `1..9`, with its four-property envelope (`01-effect-vocabulary.md`) | calling a runtime internal; reading raw runtime state; instructing the runtime to skip or reorder a check |
| **Processor-invocation request** | role, objective, context reference, requested capability set (`06`) | requesting a capability the caller does not hold; binding a processor outside the role library without recording the definition |

### Runtime → reasoning

| Crossing | Payload | Not allowed |
|---|---|---|
| **Effect result** | the realized effect's result reference, or the typed refusal (`rejected_by_capability` / `rejected_by_gate` → kind-3) | leaking another run's data; exposing the gate's internal rule set |
| **Assembled context** | the `context_bundle` for an invocation, resolvable to its content for the retention window (`07`) | presenting the bundle as complete when it was budget-truncated (the trace MUST say so) |
| **Objective signal** | build / test / lint outcome where the runtime can produce one | fabricating a signal where none exists; treating absence of a signal as success |

## Validation depth (the narrowed open question)

For the MVP the runtime checks, and only checks:

1. **Representable** — the effect is expressible in the runtime's model of the
   world (e.g. the path is inside the assigned workspace). Non-representable
   effects are **rejected before the gate**, not gated.
2. **Permitted** — the proposing actor holds the capability
   (`03-capability-authority-model.md`).
3. **Attributable** — the effect is tied to a specific invocation.
4. **Reversible where required** — an undo path exists (VCS for a file write,
   etc.).
5. **The deny-list gate** — `04-enforcement-gate.md`.

The runtime makes **no semantic judgment**: it does not read a diff to decide
whether the change is *good*, does not run a type-checker or linter before
realizing a write, does not assess whether a test is meaningful. "Is this the
right change?" is a cognitive question answered by a reviewer processor, never by
the runtime.

Discarded: a runtime that semantically validates before realizing (lint,
type-check, spec-conformance). It recreates the rigid workflow engine
`02-reasoning-vs-runtime.md` exists to prevent, and it puts a persuadable-by
-construction judgment in the one place that must stay mechanical.

## Call order (pinned; placement still open)

Every effect that reaches the runtime is processed in this order, and the runtime
**cannot be instructed to reorder or skip a step**:

```
representability pre-check  ->  capability  ->  invariant gate  ->  realize
        (runtime)              (policy)          (floor)          (runtime)
```

Whether the gate is a component *of* the runtime or a layer the runtime is
subordinate *to* is left open (`07-invariant-enforcement.md`). What is fixed:
there is no runtime code path to an effect realization that bypasses the gate.

## What each side may not assume

**Reasoning MUST NOT assume:**

- a proposed effect will be realized — it may be refused;
- its context is complete — it may be budget-truncated or simply missing a file;
- a spawned processor will run or succeed.

**Runtime MUST NOT assume:**

- a proposed effect is safe because a capable actor proposed it — it still gates;
- it should interpret the work's purpose to decide how hard to validate — depth
  is fixed at the four properties + gate, regardless of what the work "means".

## Failure modes

- **Boundary bypass.** A reasoning-side code path that reaches a runtime internal
  without going through a proposed effect. A conformance failure even if nothing
  harmful happens through it.
- **Semantic creep.** The runtime begins making cognitive judgments ("this test
  is weak", "this refactor is unnecessary") to decide whether to realize. Defect
  — that is a reviewer's job.
- **Assumed realization.** Reasoning proceeds as though an effect happened without
  checking the result or refusal.
- **Context assumed complete.** Covered by `07`; restated here as a boundary
  assumption the reasoning side must not make.
- **Signal fabrication.** The runtime reports an objective signal it did not
  actually obtain, or treats "no signal" as "pass".

## Relationships

- **Reasoning and runtime boundary** (`02-reasoning-vs-runtime.md`) — the concept;
  this document is its interface narrowing.
- **Runtime** (`05-runtime.md`) — owns representability and reversibility
  judgments and effect realization; this document says what it may not also do.
- **Orchestrator contract** (`08`) / **processor contract** (`06`) — the reasoning
  side of the boundary.
- **Enforcement gate** (`04`) / **effect vocabulary** (`01`) — the checks and the
  effect-type domain that cross the boundary.
- **Observability** (`02`) — every crossing in both directions is recorded.

## Open contracts

- **Runtime validation depth beyond the MVP.** The `02-reasoning-vs-runtime.md`
  open question is narrowed here for Milestones 5; it reopens for the post-MVP
  rework, where "too little makes evolution unsafe, too much recreates a workflow
  engine" has to be resolved with evidence.
- **Streaming across the boundary.** The MVP is request/response per invocation.
  When does a processor stream intermediate effects the orchestrator reacts to
  mid-run?
- **Objective signals as a first-class crossing.** The MVP wires the fixture's
  per-task check in ad hoc; the record shape is the `02-observability-event-model.md`
  "objective signals" open contract.
- **One boundary or two.** Whether the orchestrator/runtime boundary and the
  processor/runtime boundary are the same seam with the same rules, or distinct.
- **Gate placement.** Component of the runtime, or a layer above it
  (`07-invariant-enforcement.md`).
