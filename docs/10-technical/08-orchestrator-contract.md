# Orchestrator Contract (v0)

**Traces to:** `00-design/22-arch-cognition/03-orchestrator.md`,
`00-design/22-arch-cognition/01-work-intent-and-task-model.md`,
`00-design/10-foundations/02-reasoning-vs-runtime.md`,
`00-design/10-foundations/04-context-as-governed-resource.md`,
`00-design/40-roadmap/01-MILESTONES/completed/05-intelligent-orchestration.md` (M5);
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
its own performance (higher-level evaluation, Milestone 12+).

## Inputs

- The **originating intent** — human-authored, carried verbatim. The orchestrator
  MUST NOT rewrite it (`01-work-intent-and-task-model.md`: preserve the goal,
  question the task). It may conclude the task derived from the intent is wrong.
- Its own **live set**. The orchestrator is itself under context governance
  (`03-orchestrator.md`) and is fed the same way anything else is: a turn input
  composed afresh each turn by `14-context-manager.md` out of what has crossed
  into its live set. It does **not** receive the full repository or every
  processor's full conversation.

  **The orchestrator holds no context policy of its own.** It does not assemble,
  select, or budget its own input, and it has no privileged access to a wider one.
  Whatever recall policy is in force applies to it as to any instance — which is
  what makes an orchestrator's context a measurable subject rather than an
  exception carved out of the measurement.
- Its **scope**, inherited. The orchestrator operates under the intent's scope and
  may narrow it for the items below; it does not derive it (Authority, below).
- Its own **capability set** — for the MVP, `processor_invocation` (type 6) and
  `work_record_mutation` (type 4) only. It MUST NOT propose workspace, process,
  or network effects directly; those go through the processors it spawns.
- The **role library** — free-text role definitions available to bind
  (`06-processor-contract.md`); open-ended, except for the invariant processors,
  which are not in it (`04-enforcement-gate.md`).

## Outputs

- A sequence of **processor invocations** (type 6 effects), each carrying the seven
  things `06-processor-contract.md` binds: a role, an objective the orchestrator
  formulated, a **scope contained in the work item's**, a live-set identity, an
  isolation preference, the capability set seed configuration gives that role, and
  an interaction mode. It does not select context; there is nothing to select.

  On isolation it MAY tighten and MUST NOT loosen. Asking for an independent review
  is a legitimate reason to demand more isolation than the reviewer role defaults
  to; waiving what a judging role requires is not available to it.
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
  processors within its capability set; **narrow** a scope for a work item or an
  invocation beneath it; route one processor's output to another; stop the effort.
- **MUST NOT**: realize workspace / process / network effects directly; rewrite
  the intent; **derive a scope ceiling from intent**; **widen any scope**; use a
  processor to accomplish what it is itself forbidden to do (e.g. instructing an
  implementer solely to edit the invariant list); define its own success metric or
  evaluate its own performance; loop without bound.
- **MAY** spawn a processor holding an effect grant it does not itself hold. That is
  what delegation is. Its own grants bound what it may **propose**, not what may
  happen under its mandate, and what bounds delegation instead is the `roles`
  constraint on its type-6 grant, the scope the child inherits, and the gate every
  child effect still meets (`03-capability-authority-model.md`, Where a spawned
  instance's set comes from).
- **The forbidden-effect rule above is weaker than it reads**, and
  `03-capability-authority-model.md` sets out why: it collapses gate-forbidden
  (already refused at the delegate's own gate), capability-forbidden (which
  delegation exists to do), and scope-forbidden (already checked by containment).
  What remains is purpose, which no effect stream shows. Keep it as a statement of
  what the orchestrator should not attempt; do not build a check against it, and do
  not treat its presence as coverage.
- Every processor it spawns is **independently gated** (capability + invariant
  gate). Orchestrator authorization is not processor authorization.

### Why it narrows but does not derive

The orchestrator is under the influence of the feedback loops, so assigning it the
derivation of the ceiling is circular: the actor said to be bounded by the intent's
scope would be the one writing that bound. Deriving the ceiling from intent belongs
to an invariant processor (`03-capability-authority-model.md`, Who may write a
scope).

Narrowing needs no such protection, and the asymmetry is the whole reason the split
is cheap. Narrowing makes the check **stricter**, and an orchestrator that declines
to narrow simply leaves the inherited boundary standing. There is no failure mode on
this side worth building a mechanism against.

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

## Handing something to the operator — two modes, and a forbidden third

The orchestrator is the component that reaches the operator: on a stop for review,
on an escalation, on a scope left `pending`. `10-foundations/07` places a
requirement on the **shape** of that handoff, and this is where it becomes a
contract.

> Ask what only the operator can answer. Where the system must decide, yield with
> the reasoning that would let the decision be overturned. Never present what the
> operator can only accept.

So every handoff MUST take one of exactly two forms:

- **A question with candidate answers.** Where the system cannot decide — two
  defensible readings of a boundary, two incompatible plans — name the
  interpretations and ask. It MUST NOT be posed as an open question ("what should
  the scope be?"), which hands the whole problem back, and MUST NOT be resolved
  into one reading presented for validation.
- **A decision with overturning reasoning.** Where the system must decide, record
  what it decided **and** the reasoning that would let the decision be overturned.
  That reasoning MUST name something the operator can find **false** — an
  assumption, a read of the codebase, a claim about what the change reaches.
  Reasoning that merely justifies the decision does not satisfy this, and is the
  form it decays into.

And one form is forbidden: **a finished artefact presented for approval**, with no
question and nothing falsifiable attached.

The reason is mechanical rather than moral, and worth carrying in the
specification because an implementer will otherwise read it as a style preference.
Approval **can only subtract** — it rejects what is present and cannot introduce
what is absent. **Refusing costs more than approving**, so every approval interface
leans toward assent independently of diligence. **Approval quality is invisible**:
considered and reflexive approval leave the same trace. And it **moves
responsibility without moving understanding** — whoever approves owns the outcome,
including the part they could no longer evaluate.

Both permitted modes place the operator's act where it is cheap for them:
answering about intent rather than evaluating an artefact, checking *why* rather
than *what*.

**The required stop rationale is this rule's narrower form**, already in force
above. A `stop` decision carrying its reasoning is the second mode applied to one
specific decision; what this section adds is that the same shape governs every
handoff, and that the reasoning has to be the overturning kind rather than the
justifying kind.

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
  the working-memory problem the processor architecture exists to solve. The
  orchestrator's live set is governed by the same recall policy as anything else,
  and an implementation that exempts it has removed the only thing bounding this.
- **Approval-shaped handoff.** A finished plan or diff put to the operator with no
  question and nothing falsifiable attached. It looks like diligence and is the
  failure the two-mode rule exists to prevent, because it transfers responsibility
  without transferring understanding.
- **Justifying reasoning in place of overturning reasoning.** A yielded decision
  whose recorded reasoning explains why it is right rather than naming what would
  make it wrong. This is what the mode decays into, and it passes any check that
  only asks whether reasoning was recorded.
- **Self-derived scope.** An orchestrator that writes the ceiling it is bounded by
  has bounded nothing, whatever the text says.

## Relationships

- **Processor contract** (`06`) — the orchestrator is the caller that issues the
  type-6 effect; it formulates the seven-part input envelope.
- **Work record** (`13`) — holds the work items the orchestrator formulates, their
  declared scopes, and the transitions it proposes. It reads current work state
  every loop step, which is why that read must not replay a transition log.
- **Context manager** (`14`) — composes the orchestrator's own turn input, under
  the same policy as everything else.
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
  Milestone 15.
- **Processor-to-processor debate.** Free-form challenge and re-investigation
  among processors, versus the MVP's route-output-as-input. Deferred.
- **The orchestrator's own scope.** It reads work state across items rather than
  operating under one, so the natural reading is that it holds the **intent's**
  scope with work items inheriting narrowed versions. That is consistent with
  mandate descending from intent and is argued nowhere. Shared with
  `03-capability-authority-model.md`.
- **Orchestrator context budget.** Milestone 9 measures context quality and may
  change what recall policy is in force; nothing here fixes one.
- **Orchestrator model.** The MVP uses the one resident 7B (M0: no per-role model
  switching on the reference host). Whether a stronger orchestrator model changes
  the result is a Milestone 15 question.
- **No objective signal.** The MVP fixture has a per-task check; most real work
  does not. What the orchestrator's stopping rules do without one is deferred.
- **Handoff framing — closed.** Specified in `06-processor-contract.md` (Handoff
  framing), and it binds this document because routing one processor's output to
  another *is* the MVP's whole definition of mediation. What the orchestrator MUST
  do when it routes: fold the prior output into the next **objective**, prefer an
  objective signal — a check's own output — over a model's account of one, and keep
  model prose whose audience is the operator out of another instance's objective
  entirely.
- **Planner terminal state.** The tuned planner over-returned `blocked` on
  ordinary "add a capability the code does not yet have" objectives. A planner
  should `block`/`decline` only for a genuine false premise; "not built yet" is
  the normal case.
