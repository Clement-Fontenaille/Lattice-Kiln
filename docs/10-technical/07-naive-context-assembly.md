# Naive Context Assembly (v0, expected to be replaced)

**Traces to:** `00-design/10-foundations/04-context-as-governed-resource.md`
("a naive default is still required"),
`00-design/10-foundations/05-ephemeral-conversation-curated-memory.md`,
`00-design/40-roadmap/01-milestones.md` (Milestones 4 and 7);
binds to `10-technical/06-processor-contract.md`,
`10-technical/02-observability-event-model.md`.

## TL;DR

Given an objective and a repository, produce a `context_bundle` for one processor
invocation: deterministically, cheaply, with **no relevance modelling**, and with
a full trace of what it included and what it dropped. Its job is to be a
measurable baseline, not to be good.

> **Motto:** Deliberately unglamorous, so the curator has something to beat.

## Status of this document

v0 for Milestone 4. The concrete algorithm below is illustrative, but two
properties are **normative**: it MUST stay simple (no embeddings, no model calls,
no history) and it MUST emit a selection trace. Milestone 7 measures context
quality against this baseline and may *replace* the algorithm — never accrete
onto it.

## Narrowing

`04-context-as-governed-resource.md` requires "some unglamorous, possibly poor,
context-assembly behavior on day one" and explicitly defers the real design. This
document fixes that day-one behavior and commits to its replacement. It does
**not** define context governance, retrieval quality, the request/response loop,
or the context-quality metric (Milestone 7).

## Responsibility

Produce a `context_bundle` (the `06-processor-contract.md` input) from an
objective, a repo, optional path hints, and a token budget — deterministically
and within budget — plus the trace that makes the selection auditable. It owns
only the naive baseline.

## Inputs

- `objective` — the processor's objective text.
- `repo_root` — the repository to draw from (read-only).
- `path_hints` *(optional)* — explicit files/dirs the caller names as relevant.
- `token_budget` — default sized to keep the working-default 7B fully resident at
  ≤16k context on the reference host (M0 findings-log entry 1); an illustrative
  default is 8k tokens for context, leaving generation headroom. Host-specific.
- `interaction_mode` — from the processor contract; `review` mode additionally
  receives the prior processor's **conclusion text only**.

## The naive algorithm (v0, illustrative)

1. **Always include**, in this order: the objective text verbatim; the repo's
   top-level `README` (truncated to a fixed cap); a file tree to depth `N` (names
   and sizes only, no contents).
2. **If `path_hints` are given**: include those files whole, in the given order,
   until the budget is reached.
3. **Otherwise**: take salient terms from the objective (literal tokens, minus a
   small stopword list), match them as case-insensitive substrings against file
   paths and — for a bounded number of candidate files — file contents; include
   matched files whole, highest match-count first, ties broken by shortest path,
   until the budget is reached.
4. **Never include**: embeddings or any vector retrieval; summaries; project
   history; persistent memory; any previous processor's conversation — except a
   `review`-mode invocation's single prior-conclusion string.
5. **Truncate** the final file to fit the budget; record that a truncation
   occurred.

## Output — the context bundle

- An **ordered list** of entries: `(source_ref, bytes, included_fully | truncated)`.
- A **token estimate** for the whole bundle, which MUST be `<= token_budget`.
- A **selection trace** (mandatory): which terms were extracted, which files
  matched and with what score, which matched files were dropped for budget, and
  where truncation happened. Milestone 7 measures against this trace.

## Determinism (normative)

Identical `(objective, repo state, token_budget, path_hints, interaction_mode)`
MUST produce an identical bundle and trace. No clock, no network, no model call,
no randomness, no filesystem-order dependence (entries are sorted by an explicit
key before selection).

## Authority

None. Reading the repo is a read, not an effect (`01-effect-vocabulary.md`). This
component MUST NOT mutate the workspace and MUST NOT call the model.

## Failure modes

- **Budget overshoot.** A bundle over `token_budget` would push the processor to
  CPU offload (M0 cliff) — a defect. MUST truncate and record.
- **Silent drop.** A file that matched the naive rule but was dropped for budget
  with no trace entry defeats the Milestone 7 measurement — a defect.
- **Empty bundle.** Even with no term matches, the bundle still carries objective
  + README + tree. A genuinely empty bundle is a defect.
- **Nondeterminism.** Any run-to-run variation for identical inputs is a defect.
- **Unresolvable `context_ref`.** The bundle must be resolvable to its actual
  content for the run's retention window (`02-observability-event-model.md`).

## Relationships

- **Context as a governed resource**
  (`04-context-as-governed-resource.md`) — the concept and the clause that
  mandates this baseline exist.
- **Processor contract** (`06-processor-contract.md`) — consumes the bundle as
  `context_bundle`.
- **Observability** (`02-observability-event-model.md`) — the selection trace is
  part of the run record; `context_ref` resolves to the bundle content.
- **Milestone 7** — the consumer of the baseline measurement. This document
  deliberately does not define the quality metric.

## Open contracts

- **Budget number.** The concrete `token_budget` and how it tracks the resident
  inference envelope once hardware is a variable (post-MVP rework).
- **Ranking rule for step 3.** Substring count vs. path proximity vs.
  filename-exact-match priority — v0 picks one; M7 evidence may replace it.
- **Context-quality metric.** Owned by Milestone 7; explicitly not here.
- **Request/response loop.** When naive one-shot assembly gains the ability to
  answer a processor's mid-run request for more context
  (`04-context-as-governed-resource.md`).
- **`review` independence cut.** Whether "prior conclusion only" is the right
  isolation for adversarial review (`02-processors.md` open question).
