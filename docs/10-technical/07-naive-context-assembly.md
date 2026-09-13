# Naive Context Assembly (v0, expected to be replaced)

**Traces to:** `00-design/10-foundations/04-context-as-governed-resource.md`
("a naive default is still required"),
`00-design/23-arch-context-management/01-context-manager.md`,
`00-design/10-foundations/05-ephemeral-conversation-curated-memory.md`,
`00-design/40-roadmap/01-MILESTONES/completed/04-ephemeral-processors.md` (M4),
`00-design/40-roadmap/01-MILESTONES/09-context-governance-measurement.md` (M9);
binds to `10-technical/14-context-manager.md`,
`10-technical/06-processor-contract.md`,
`10-technical/02-observability-event-model.md`.

## TL;DR

One deliberately unglamorous default: **a degenerate recall policy.** Present
everything the live set holds, in registration order, until the budget runs out, then
drop the rest.

No relevance modelling, no embeddings, no model calls, and a full trace of what was
included and what was dropped.

> **Motto:** Deliberately unglamorous, so the curator has something to beat.

## Status of this document

v0. The concrete rules below are illustrative; three properties are **normative**:
it MUST stay simple (no embeddings, no model calls, no history), it MUST be
deterministic, and it MUST emit a trace. Milestone 9 measures context quality
against this baseline and may **replace** it — never accrete onto it.

## Narrowing

`10-foundations/04` requires "some unglamorous, possibly poor, context-assembly
behavior on day one" and explicitly defers the real design.
`23-arch-context-management/01` then established what the real design is made of,
and this document is narrowed to sit inside it rather than alongside it:

- **This is a recall policy, not a separate mechanism.** Recall everything until
  the budget runs out, then drop the rest, is a policy on the same axis as
  anything richer. Naming it that way is what makes a better policy a replacement
  rather than a different kind of thing.
- **There is no seeding heuristic.** A rule that always reads the README, probes the
  file tree and term-matches the objective performs orientation unconditionally, and
  many tasks need none — *"Test, test! say hello :)"* would trigger all of it and use
  none of it, spending context budget on material irrelevant to the objective, which
  is the failure `10-foundations/04` names. What a task's live set starts with is
  whatever the scope evaluation already had to read in order to derive the ceiling,
  attached at task creation (`70-THINKING/18-task-artifact-edges.md`). Orientation
  becomes demand-driven, by an actor that can tell a trivial task from a substantial
  one, instead of unconditional.
- **There is no bundle.** Nothing is bound at instantiation and held. The turn
  input is composed afresh every turn (`14-context-manager.md`).

## Responsibility

One thing: **the degenerate recall policy.** Given a live set and a budget, decide
what goes into a turn input and in what order.

It owns only the naive baseline. It does not define context governance, retrieval
quality, or the context-quality metric (Milestone 9).

## The degenerate recall policy

### The recall rule (illustrative)

Given a live set and `turn_budget`:

1. Order entries by `registered_at` ascending — oldest crossing first.
2. Include entries in that order until `turn_budget` would be exceeded.
3. Truncate the final entry to fit; record that a truncation occurred.
4. Drop the remainder; record each drop.

### What this policy is missing, stated precisely

It has **no basis for the drop decision beyond position in a budget.** That is the
gap, and it is worth naming exactly because two other candidate gaps are not real:

- It is not missing a way to un-drop something. An entry that leaves the live set
  is recovered by **retrieval**, a fresh crossing, not by a richer recall
  (`14-context-manager.md`).
- It is not missing a request/response loop. A processor's request for more
  context is an ordinary tool call (`06-processor-contract.md`), and no servicing
  path should be built.

### Presentation is still normative

Even a degenerate policy MUST carry crossing type into the turn input. A
generation MUST NOT be presented indistinguishably from a read or a retrieval
(`10-foundations/07`; `14-context-manager.md`). Ordering by registration time does
not excuse flattening the marking.

## Budgets

`turn_budget` is sized to keep the working-default 7B fully resident on the reference host (M0, findings-log entry 1); an illustrative default
is 8k tokens for the turn input, leaving generation headroom. Host-specific.

A **token count is a proxy for the thing that actually binds**, and the proxy is
loose. What binds is KV footprint, which runs two to three orders of magnitude
above text size — hundreds of kilobytes per thousand tokens against roughly four
kilobytes of text (`00-project/05-vocabulary.md`). `05-provisional-invariant-list.md`
R4 is the ceiling that matters; the budget here is a cheap approximation of it and
MUST NOT be mistaken for the ceiling itself.

## Determinism (normative)

Identical `(live set, turn_budget)` MUST produce an identical turn input.

No clock, no network, no model call, no randomness, no filesystem-order dependence
— entries are sorted by an explicit key before selection.

## The trace (mandatory)

One trace, per turn, consumed by the Milestone 9 measurement: which live-set entries
were included, in what order, which were dropped, and where truncation happened.

It is what the comparison programme needs: two policies over the
same live set are comparable only if what each presented was recorded
(`14-context-manager.md`).

## Authority

None. Reading the repository is a read, not an effect
(`01-effect-vocabulary.md`). This component MUST NOT mutate the workspace, MUST
NOT call the model, and MUST NOT initiate a crossing on a processor's behalf — it
tells the caller what to read; the caller reads.

## Failure modes

- **Budget overshoot.** A turn input over `turn_budget` pushes the processor
  toward CPU offload (the M0 cliff) — a defect. MUST truncate and record.
- **Silent drop.** An entry dropped with no trace entry defeats the Milestone 9
  measurement — a defect, and the more damaging half because it is the recall
  trace that makes policies comparable.
- **Empty live set at turn one.** A task's live set holds at least the intent from
  the moment the task is created, so an instance starting with nothing registered is a
  defect.
- **Nondeterminism.** Any run-to-run variation for identical inputs is a defect.
- **Crossing type flattened.** See Presentation above.
- **A bundle reappearing.** Any object composed once per invocation and held
  across turns is a defect against `14-context-manager.md`, however convenient.
- **Recalling another processor's reasoning to an instance that must not see it.**
  Breaks the `review` independence cut invisibly, since the material arrives looking
  like ordinary context. The cut is made against the subdivided `generation` crossing
  type (`14-context-manager.md`).

## Relationships

- **Context manager** (`14-context-manager.md`) — this document is one policy
  inside that component. Everything about registration, the live set, and composition
  is owned there.
- **Context as a governed resource** (`10-foundations/04`) — the concept, and the
  clause that mandates a naive baseline exist at all.
- **Knowledge model** (`12-knowledge-model.md`) — where the live set's entries point.
- **Processor contract** (`06-processor-contract.md`) — binds a `live_set_id`; the
  `review` independence cut is made against the crossing type at recall.
- **Observability** (`02-observability-event-model.md`) — the recall trace is part of
  the run record.
- **Milestone 9** — the consumer of the baseline measurement. This document
  deliberately does not define the quality metric.

## Open contracts

- **Budget numbers.** A concrete `turn_budget`, and how it tracks
  the resident inference envelope once hardware is a variable. Shared with R4,
  which needs a footprint estimate rather than a token proxy.
- **Ordering rule for recall.** Registration order is the cheapest defensible
  choice and nothing argues it is good. Position affects what a model attends to
  (`14-context-manager.md`, prefix persistence), so ordering is a real lever this
  policy spends arbitrarily.
- **Context-quality metric.** Owned by Milestone 9; explicitly not here.
- **Cost as relation and redundancy, not volume** *(`10-foundations/04`)*. Two
  positions the foundation holds and this document does not implement: *too much is
  a relation, not a property* — a turn input is too large **for a given processor
  and objective**, not in itself — and *what makes context costly is redundancy,
  not volume*. v0 truncates by token count, which is the volume reading of both.
  What replaces a flat budget, and can redundancy be detected cheaply enough to
  compose against?
- **Prior-step handoff framing — closed.** It is not this component's contract. A
  handoff is folded into the **objective**, which is bound at instantiation, so the
  rule lives with `06-processor-contract.md` (Handoff framing) and this component
  never sees one.

  The alternative shape — a handoff written somewhere durable and **read** by the
  next instance, arriving as a crossing this component would register — is not
  adopted, and nothing measured supports it.
- **`review` independence cut.** Whether "prior conclusion only" is the right
  isolation for adversarial review (`00-design/22-arch-cognition/02-processors.md`).
