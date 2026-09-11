# Context Manager

## TL;DR

The context manager registers artifacts crossing in from tool calls or the model's own output, tracks the live set they form, and runs a recall policy deciding which of them actually reach the model at any given turn.

> **Motto:** Nothing crosses without being counted.

## Status of this document

Draft. A naive default already exists in part — `10-technical/07-naive-context-assembly.md` — and is credited here, not replaced.

## Motivation

`10-foundations/04` established that a context is the set of artifacts currently live, each the product of a crossing from one of three locations, and that none of its four failure modes are checkable without an explicit, first-class live record. This actor owns that record.

## The actor and its responsibility

- **Register** artifacts as they cross in from any tool call — a read, a test run, any effect response — or from the model's own generated output. A knowledge-base retrieval is the one exception to "the same way regardless of origin": since the claim already exists and has its own identity in `21-arch-knowledge-model`, this actor holds a reference to it plus its own tracking metadata (crossing type, live/archived state), not a full copy of the claim's content. This actor never initiates a crossing itself, only records what comes back once something else has.
- **Track** the live set registration populates.
- **Recall** — a separate, later decision, governed by an explicit policy: of what is already in the tracked pool, which artifacts are actually fed to the model on a given turn, and which are held back. Recall means presentation, nothing else — it never fetches anything new, it only decides visibility over content already registered. That boundedness is the point: given a fixed pool, a policy chooses a subset, which makes different recall policies directly comparable and testable against each other, holding the pool itself constant.

Knowledge-base retrieval is a tool like any other — the model calls it, the runtime executes it, this actor registers what comes back. This actor never initiates that call itself, on a processor's behalf or otherwise; the only way knowledge-base content enters the tracked pool is through a call the model actually makes. Once it is in the pool, though, it is subject to the same recall policy as anything else — recall and archive apply uniformly regardless of how an artifact got there.

## Service provided to the rest of the system

- **A context bundle**, per invocation, reflecting what the recall policy currently presents — richer than the naive default's flat file list, since it carries each entry's crossing type.
- **A live-state query**, for any of `04`'s failure-mode checks to consult.

## General shape and a naive default

`10-technical/07-naive-context-assembly.md` already implements a fragment of this: deterministic substring matching, a flat token budget, a mandatory selection trace — no embeddings, no model calls. It has no recall policy in any real sense: everything selected is presented, nothing is ever archived-then-recalled, and anything past the budget is truncated once with no path back. That truncation is itself a degenerate recall policy — recall everything until the budget runs out, then archive the rest permanently — and naming it this way is what exposes its one missing piece: recall.

The naive default should grow artifact registration and a real live record first, since both cost nothing extra to compute. A recall policy that can actually restore something already archived is the harder addition and has no existing precedent to build from.

`70-THINKING/ideas.md` I12's mechanical-engine account still applies to the bookkeeping half of all of this — registering, tracking, running a fixed policy — with judgment called out to only where a query genuinely needs it.

## Interactions

- **`20-arch-runtime.md`** executes a tool call a processor proposed; this actor registers the output. It does not itself initiate a crossing.
- **`21-arch-knowledge-model`** answers a query only when the model calls the retrieval tool; this actor registers what comes back the same as any other tool output.
- **`22-arch-cognition`** processors receive a context bundle at instantiation and may call the knowledge-base retrieval tool mid-reasoning — an ordinary tool call, and the only way knowledge-base content enters the pool. A processor's own role instructions can require that call rather than leave it to unprompted judgment — the "prompted or required" fix `10-foundations/04`'s Expected behavior already names for exactly this class of problem, using role definition, not a new mechanism. `10-foundations/04`, findings-log entry 5 (one model, one prompting setup) showed an *unprompted-and-unsupported* request affordance going unused; that bounds a claim about that condition only, not about a role-required call, and not about whether the result holds across model scale, prompting, or finetuning, which is untested.
- **`26-arch-observability`** needs this actor's selection trace and lifecycle transitions to answer what context a processor actually received, and when.
- **`24-arch-permission-layer`** gates the tool call that produces an artifact before this actor ever sees it.

## Relationships

- **`10-foundations/04`** — owns the schema this actor realizes.
- **`21-arch-knowledge-model`** — a tool-call target the model queries; this actor registers the result, not the query.
- **`20-arch-runtime.md`** — executes the crossings whose outputs this actor registers.
- **`22-arch-cognition`** — the consumer of bundles, and the source of live, model-initiated retrieval calls.
- **`26-arch-observability`** — a separate store, not a shared one, same reasoning as `21-arch-knowledge-model`'s relationship to it. This actor's live record and observability's history have different lifecycles; the selection trace and lifecycle transitions are what this actor contributes, but observability keeps its own copy.

## Open question

What the recall policy actually is. Named here as a required, distinct responsibility — arbitrary by design, not yet specified — governing recall and archive transitions; nothing here fixes what triggers either direction.

Whether "not yet taken" is indexable for the generation crossing type the way an unread file or an unretrieved claim is — `04` did not settle this.
