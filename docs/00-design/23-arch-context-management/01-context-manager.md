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

- **What the model sees on a given turn.** Composed at the moment of feeding, out of what is in the pool and what recall selects from it. This is not a package delivered once per invocation and then held: it is recomposed every turn, over a pool that grew since the last one. It is also richer than the naive default's flat file list, since each entry carries its crossing type.
- **A live-state query**, for any of `04`'s failure-mode checks to consult.

Nothing has to ask for the first of these. This actor sits in the path everything to and from the model takes, so it composes because a turn is happening, not because something requested a composition. There is no assembly call to place, and no caller to name.

## General shape and a naive default

`10-technical/07-naive-context-assembly.md` already implements a fragment of this: deterministic substring matching, a flat token budget, a mandatory selection trace — no embeddings, no model calls. It has no recall policy in any real sense: everything selected is presented, nothing is ever archived-then-recalled, and anything past the budget is truncated once with no path back. That truncation is itself a degenerate recall policy — recall everything until the budget runs out, then archive the rest permanently — and naming it this way is what exposes its one missing piece: recall.

The naive default should grow artifact registration and a real live record first, since both cost nothing extra to compute. A recall policy that can actually restore something already archived is the harder addition and has no existing precedent to build from.

`70-THINKING/ideas.md` I12's mechanical-engine account still applies to the bookkeeping half of all of this — registering, tracking, running a fixed policy — with judgment called out to only where a query genuinely needs it.

## Interactions

- **`20-arch-runtime.md`** executes a tool call a processor proposed; this actor registers the output. It does not itself initiate a crossing. The runtime does not fetch context on a processor's behalf either — `20-arch-runtime.md`, Instantiation, and then a loop, states why there is nothing to fetch: what the model sees is composed on each turn as the turn happens, not bound at instantiation.
- **`21-arch-knowledge-model`** answers a query only when the model calls the retrieval tool; this actor registers what comes back the same as any other tool output.
- **`22-arch-cognition`** processors are instantiated with role instructions, an objective, and a capability set, and with a pool identity rather than with context itself; what they see is composed turn by turn. They may call the knowledge-base retrieval tool mid-reasoning — an ordinary tool call, and the only way knowledge-base content enters the pool. A processor's own role instructions can require that call rather than leave it to unprompted judgment — the "prompted or required" fix `10-foundations/04`'s Expected behavior already names for exactly this class of problem, using role definition, not a new mechanism. `10-foundations/04`, findings-log entry 5 (one model, one prompting setup) showed an *unprompted-and-unsupported* request affordance going unused; that bounds a claim about that condition only, not about a role-required call, and not about whether the result holds across model scale, prompting, or finetuning, which is untested.
- **`26-arch-observability`** needs this actor's selection trace and lifecycle transitions to answer what context a processor actually received, and when.
- **`27-arch-adaptation-and-evolution`** treats the recall policy as tunable system configuration: system-level feedback may propose a revision to it, a generation carries one, and a bootstrapped instance inherits the validated version. This is the loop recall's boundedness was meant to serve — two policies over the same pool are directly comparable, which is what makes a proposed revision evaluable rather than merely plausible.
- **`24-arch-permission-layer`** decides whether a call is allowed at all, before this actor ever sees what it produces. That check is not uniform across crossing types: a read — a file, a knowledge-model query — is not an effect and is only capability-gated, while an effect passes capability gating and then the invariant gate. Either way, what reaches this actor has already been allowed; this actor never gates anything itself.

## Relationships

- **`10-foundations/04`** — owns the schema this actor realizes.
- **`21-arch-knowledge-model`** — a tool-call target the model queries; this actor registers the result, not the query.
- **`20-arch-runtime.md`** — executes the crossings whose outputs this actor registers.
- **`22-arch-cognition`** — what this actor composes for, turn by turn, and the source of live, model-initiated retrieval calls. Not a consumer in the calling sense: a processor never requests its own context.
- **`26-arch-observability`** — a separate store, not a shared one, same reasoning as `21-arch-knowledge-model`'s relationship to it. This actor's live record and observability's history have different lifecycles; the selection trace and lifecycle transitions are what this actor contributes, but observability keeps its own copy.

## Open question

How a pool is seeded when a processor starts. Recall governs what is presented out of a pool; nothing here says what is in one at turn zero. `22-arch-cognition/08` holds this under another name — fork/join implies a near-empty pool with a later reconciliation, continuation implies one seeded by the preceding step — and whatever settles that settles this.

What the recall policy actually is. Named here as a required, distinct responsibility — arbitrary by design, not yet specified — governing recall and archive transitions; nothing here fixes what triggers either direction.

Whether "not yet taken" is indexable for the generation crossing type the way an unread file or an unretrieved claim is — `04` did not settle this.
