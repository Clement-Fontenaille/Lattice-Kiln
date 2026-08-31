# Orchestrator Contract (v0)

**Traces to:** `00-design/20-cognitive-architecture/03-orchestrator.md`,
`00-design/20-cognitive-architecture/01-work-intent-and-task-model.md`,
`00-design/10-foundations/02-reasoning-vs-runtime.md`,
`00-design/10-foundations/04-context-as-governed-resource.md`,
`00-design/40-roadmap/01-milestones.md` (Milestone 5);
binds to `10-technical/06-processor-contract.md`,
`10-technical/01-effect-vocabulary.md` (effect type 6),
`10-technical/03-capability-authority-model.md`,
`10-technical/02-observability-event-model.md`,
`10-technical/09-orchestrator-runtime-boundary.md`.

## TL;DR

The orchestrator owns the **strategy** of one cognitive effort: at each step it
observes what is known, decides which cognitive operation is useful next, spawns
a processor to do it, integrates the result, and decides whether to stop. It does
not own truth, runtime authority, effect realization, or the definition of its
own success. Every step it takes leaves a decision record, so the strategy is
reconstructable.

> **Motto:** Coordinate the work; do not become the system.

## Status of this document

v0 for Milestone 5. It fixes the orchestrator loop, the per-step decision record,
the delegation rules, and the stopping rules — enough to run "does
natural-language orchestration beat a fixed workflow?" against the M4 fixed chain
and the monolith. Recursive orchestration, competing orchestrators, and
free-form multi-processor debate are named as open contracts and deferred.

## Narrowing

`03-orchestrator.md` says the orchestrator "interprets current work and
knowledge, decides what cognitive operation appears useful next, selects or
defines a processor role, formulates the processor objective, mediates
discussions, and synthesizes results." This document narrows that to:

- an **orchestrator loop** — observe → decide next operation → spawn processor(s)
  → integrate → stop-or-continue;
- a **decision record** per loop step (the "stays understandable" requirement of
  the Milestone 5 evidence question);
- **mediation**, for the MVP, means **routing one processor's output as another's
  input** (e.g. a reviewer's `needs-change` becomes a fresh implementer
  invocation carrying the critique) — not free-form debate among processors.

## Responsibility

Own the strategy of one cognitive effort from a single originating intent: decide
what to do next, delegate it, integrate what comes back, and decide when the
effort is done. It does not realize effects (the runtime), does not decide
whether an effect is permissible (`04-enforcement-gate.md`), and does not judge
its own performance (higher-level evaluation, Milestone 10+).

## Inputs

- The **originating intent** — human-authored, carried verbatim. The orchestrator
  MUST NOT rewrite it (`01-work-intent-and-task-model.md`: preserve the goal,
  question the task). It may conclude the task derived from the intent is wrong.
- A **curated context** — the orchestrator is itself under context governance
  (`03-orchestrator.md`). For the MVP: the intent, a bounded running summary of
  what processors have concluded so far, and the naive repo bundle
  (`07-naive-context-assembly.md`). It does **not** receive the full repository
  or every processor's full conversation.
- Its own **capability set** — for the MVP, `processor_invocation` (type 6) and
  `work_record_mutation` (type 4) only. It MUST NOT propose workspace, process,
  or network effects directly; those go through the processors it spawns.
- The **role library** — free-text role definitions available to bind
  (`06-processor-contract.md`); open-ended.

## Outputs

- A sequence of **processor invocations** (type 6 effects), each carrying a role,
  an objective the orchestrator formulated, a context selection, and a capability
  set **bounded by the orchestrator's own** — it cannot grant what it does not
  hold.
- A **decision record per loop step** (recorded as a type-4 work-record
  mutation): what was observed, which operation was chosen and a one-line
  natural-language rationale, and what the step is expected to produce. This is
  what makes the strategy reconstructable and is mandatory. **A `stop` decision
  MUST carry a rationale too** — M5 (findings-log entry 6) found stop decisions
  were routinely recorded with none, leaving "why the orchestrator judged the
  work done" unreconstructable.
- A final **synthesis**: the outcome handed back, plus a terminal state:
  - `resolved` — the objective was met;
  - `declined` — the effort should not proceed (false premise, wrong problem,
    already satisfied); distinct from `blocked` and MUST carry the reason;
  - `blocked` — could not proceed (stuck, repetition, budget) — an *unprincipled*
    stop, distinct from `declined`;
  - `abandoned` — a spawned processor declined and the orchestrator concurred.
  M5 found the orchestrator collapsing `declined` into `blocked`; keeping them
  distinct is normative.

## Authority

- **MAY**: formulate processor objectives; choose or define roles; spawn
  processors within its capability set; route one processor's output to another;
  stop the effort.
- **MUST NOT**: realize workspace / process / network effects directly; rewrite
  the intent; grant a processor a capability it does not itself hold; use a
  processor to accomplish what it is itself forbidden to do (e.g. instructing an
  implementer solely to edit the invariant list); define its own success metric
  or evaluate its own performance; loop without bound.
- Every processor it spawns is **independently gated** (capability + invariant
  gate). Orchestrator authorization is not processor authorization.

## Stopping rules

The loop MUST be able to terminate by at least these
(`03-orchestrator.md`: prevent useless reasoning loops):

- **Objective met** — a processor reports success and, where an objective signal
  exists (`09`), it confirms.
- **Repetition** — the same operation on the same target N times without
  measurable progress → stop, mark `blocked`. *(M5 workflow re-test, findings-log
  entry 6 addendum: the first implementation omitted this rule and an orchestrator
  spawned the planner 4–6 times consecutively without progress. It is normative,
  not optional.)*
- **Budget** — max loop steps, max total processor invocations, or wall-clock,
  from invariant-list resource ceiling R3. Hitting it is a **stop for human
  review**, not a silent truncation.
- **No useful next operation** — the orchestrator cannot name an operation likely
  to help → stop, mark `blocked`, with its reasoning recorded.

## Failure modes

- **Runaway loop.** Neither stops nor progresses. R3 backstops it; an orchestrator
  that relies on the backstop rather than its own stopping rules is defective.
- **Intent drift.** The synthesis answers a different question than the intent.
  The intent is recorded verbatim, so a later reader can detect it.
- **Silent strategy.** A loop step with no decision record — reconstruction
  cannot explain *why* the orchestrator acted. This is the Milestone 5
  observability defect.
- **Authority laundering.** Spawning a processor with a capability the
  orchestrator lacks, or delegating a forbidden intent. The gate catches the
  effect; this contract forbids the attempt.
- **Context bloat.** Accumulating every processor's full conversation, recreating
  the working-memory problem the processor architecture exists to solve. The MVP
  orchestrator carries only a bounded running summary.

## Relationships

- **Processor contract** (`06`) — the orchestrator is the caller that issues the
  type-6 effect; it formulates the five-part input envelope.
- **Effect vocabulary** (`01`) — processor invocation is effect type 6; decision
  records are type 4.
- **Capability model** (`03`) — the orchestrator's own set bounds what it can
  delegate.
- **Enforcement gate** (`04`) — every spawned effect is still gated; the
  orchestrator cannot pre-authorize.
- **Observability** (`02`) — decision records + the invocation lineage
  (`parent_invocation_id` chains to the orchestrator) are how the strategy is
  reconstructed.
- **Naive context assembly** (`07`) — assembles both the orchestrator's own
  context and each processor's.
- **Orchestrator/runtime boundary** (`09`) — the seam: what crosses, in which
  direction, and what each side may not assume.

## Open contracts

- **Recursion.** May orchestration be delegated to a sub-orchestrator
  (`03-orchestrator.md` open question)? Out for the MVP — one orchestrator.
- **Competing orchestrators.** Comparing two orchestrators on the same effort —
  Milestone 13.
- **Processor-to-processor debate.** Free-form challenge and re-investigation
  among processors, versus the MVP's route-output-as-input. Deferred.
- **Orchestrator context budget.** The MVP uses "intent + running summary + naive
  bundle"; Milestone 7 measures context quality and may change it.
- **Orchestrator model.** The MVP uses the one resident 7B (M0: no per-role model
  switching on the reference host). Whether a stronger orchestrator model changes
  the result is a Milestone 13 question.
- **No objective signal.** The MVP fixture has a per-task check; most real work
  does not. What the orchestrator's stopping rules do without one is deferred.
- **Handoff framing** *(M5 workflow re-test)*. A constrained local model treats a
  prior processor's raw prose (a plan, a critique) passed as free-form side input
  as a cue to *discuss* rather than *act*, and stops emitting effects. Prior-step
  output must be folded into the next objective or a structured field, never
  appended as narration. How the context assembler (`07`) should structure that
  handoff is open.
- **Planner terminal state.** The tuned planner over-returned `blocked` on
  ordinary "add a capability the code does not yet have" objectives. A planner
  should `block`/`decline` only for a genuine false premise; "not built yet" is
  the normal case.
