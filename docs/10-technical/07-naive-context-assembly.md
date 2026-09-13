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

Two deliberately unglamorous defaults, specified together because they are what a
run needs before anything smarter exists.

**A seeding heuristic** — which reads the caller performs so an instance's live
set is not empty on turn one. **A degenerate recall policy** — present everything
the live set holds, in a fixed order, until the budget runs out, then drop the
rest.

No relevance modelling, no embeddings, no model calls, and a full trace of what
was included and what was dropped.

> **Motto:** Deliberately unglamorous, so the curator has something to beat.

## Status of this document

v0. The concrete rules below are illustrative; three properties are **normative**:
it MUST stay simple (no embeddings, no model calls, no history), it MUST be
deterministic, and it MUST emit a trace. Milestone 9 measures context quality
against this baseline and may **replace** either half — never accrete onto it.

## Narrowing

`10-foundations/04` requires "some unglamorous, possibly poor, context-assembly
behavior on day one" and explicitly defers the real design.
`23-arch-context-management/01` then established what the real design is made of,
and this document is narrowed to sit inside it rather than alongside it:

- **This is a recall policy, not a separate mechanism.** Recall everything until
  the budget runs out, then drop the rest, is a policy on the same axis as
  anything richer. Naming it that way is what makes a better policy a replacement
  rather than a different kind of thing.
- **Seeding is the caller's, not the context manager's.** The term-matching rule
  below chooses **which reads to perform**, and reads are ordinary crossings
  performed by whoever issues them. The context manager never initiates a
  crossing; it registers what comes back. Discarded: an assembler that fetches on
  a processor's behalf, which is the shape the removed `context_bundle` had.
- **There is no bundle.** Nothing is bound at instantiation and held. The turn
  input is composed afresh every turn (`14-context-manager.md`).

## Responsibility

Two things, separable and specified separately:

1. **Seed selection.** Given an objective and a repository, decide which files the
   caller reads before an instance's first turn, deterministically and within
   budget.
2. **The degenerate recall policy.** Given a live set and a budget, decide what
   goes into a turn input and in what order.

It owns only the naive baseline. It does not define context governance, retrieval
quality, or the context-quality metric (Milestone 9).

## Part 1 — Seed selection

### Inputs

- `objective` — the processor's objective text.
- `repo_root` — the repository to draw from (read-only).
- `path_hints` *(optional)* — explicit files or directories the caller names as
  relevant.
- `read_budget` — a byte or token bound on the seeding reads, sized against the
  same envelope as the turn budget below.

### The seeding rule (illustrative)

1. **Always read**, in this order: the repo's top-level `README` (truncated to a
   fixed cap), and a file tree to depth `N` (names and sizes only, no contents).
   The objective is not a read — it is bound at instantiation
   (`06-processor-contract.md`).
2. **If `path_hints` are given**: read those files whole, in the given order,
   until `read_budget` is reached.
3. **Otherwise**: take salient terms from the objective (literal tokens, minus a
   small stopword list), match them case-insensitively as substrings against file
   paths and — for a bounded number of candidate files — file contents; read
   matched files whole, highest match-count first, ties broken by shortest path,
   until `read_budget` is reached.
4. **Never read as part of seeding**: any previous processor's conversation.
   Persistent memory is not read here either — a claim enters a live set through
   the model calling the retrieval tool, which is a crossing this heuristic does
   not make on its behalf.

### What happens to the result

Each read is an ordinary crossing: capability-checked like any read
(`03-capability-authority-model.md`, permissive default), executed by the runtime,
written to `12-knowledge-model.md` as an Observation, and **registered into the
live set** by `14-context-manager.md`.

There is no object handed to the processor. The instance starts with a live set
that is no longer empty, which is the whole of what seeding does.

**A `review`-mode invocation is seeded with the prior processor's conclusion
only**, not its reasoning history (`06-processor-contract.md`). That is an
independence cut, and it is enforced by what is seeded rather than by what is
recalled.

## Part 2 — The degenerate recall policy

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

`turn_budget` and `read_budget` are sized to keep the working-default 7B fully
resident on the reference host (M0, findings-log entry 1); an illustrative default
is 8k tokens for the turn input, leaving generation headroom. Host-specific.

A **token count is a proxy for the thing that actually binds**, and the proxy is
loose. What binds is KV footprint, which runs two to three orders of magnitude
above text size — hundreds of kilobytes per thousand tokens against roughly four
kilobytes of text (`00-project/05-vocabulary.md`). `05-provisional-invariant-list.md`
R4 is the ceiling that matters; the budget here is a cheap approximation of it and
MUST NOT be mistaken for the ceiling itself.

## Determinism (normative)

Identical `(objective, repo state, budgets, path_hints, interaction_mode)` MUST
produce identical seeding reads. Identical `(live set, turn_budget)` MUST produce
an identical turn input.

No clock, no network, no model call, no randomness, no filesystem-order dependence
— entries are sorted by an explicit key before selection.

## The trace (mandatory)

Two traces, both required, both consumed by the Milestone 9 measurement.

- **Seed trace** — which terms were extracted, which files matched and with what
  score, which matched files were not read for budget, and where truncation
  happened.
- **Recall trace**, per turn — which live-set entries were included, in what
  order, which were dropped, and where truncation happened.

The recall trace is the one the comparison programme needs: two policies over the
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
- **Empty live set at turn one.** Seeding always reads at least the README and the
  tree, so an instance starting with nothing registered is a defect.
- **Nondeterminism.** Any run-to-run variation for identical inputs is a defect.
- **Crossing type flattened.** See Presentation above.
- **A bundle reappearing.** Any object composed once per invocation and held
  across turns is a defect against `14-context-manager.md`, however convenient.
- **Seeding from another processor's conversation.** Breaks the independence this
  baseline is supposed to preserve, and does it invisibly, since the material
  arrives looking like ordinary context.

## Relationships

- **Context manager** (`14-context-manager.md`) — this document is one policy
  inside that component, and the seeding half is a caller's heuristic that feeds
  it. Everything about registration, the live set, and composition is owned there.
- **Context as a governed resource** (`10-foundations/04`) — the concept, and the
  clause that mandates a naive baseline exist at all.
- **Knowledge model** (`12-knowledge-model.md`) — where the seeding reads land as
  Observations.
- **Processor contract** (`06-processor-contract.md`) — binds a `live_set_id`; the
  `review` independence cut is enforced by seeding.
- **Observability** (`02-observability-event-model.md`) — both traces are part of
  the run record.
- **Milestone 9** — the consumer of the baseline measurement. This document
  deliberately does not define the quality metric.

## Open contracts

- **Budget numbers.** Concrete `turn_budget` and `read_budget`, and how they track
  the resident inference envelope once hardware is a variable. Shared with R4,
  which needs a footprint estimate rather than a token proxy.
- **Ranking rule for seeding step 3.** Substring count versus path proximity
  versus filename-exact-match priority. v0 picks one; evidence may replace it.
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
  never sees one. What remains here is the consequence: seeding MUST NOT read
  another processor's conversation, which the rule above already states.

  The alternative shape — a handoff written somewhere durable and **read** by the
  next instance, arriving as a crossing this component would register — is not
  adopted and is not available until live-set seeding is settled
  (`14-context-manager.md`).
- **`review` independence cut.** Whether "prior conclusion only" is the right
  isolation for adversarial review (`00-design/22-arch-cognition/02-processors.md`).
