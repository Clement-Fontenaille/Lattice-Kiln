# Context Manager

## TL;DR

The context manager registers artifacts crossing in from tool calls or the model's own output, tracks the live set they form, and runs a recall policy deciding which of them actually reach the model at any given turn.

> **Motto:** Nothing crosses without being counted.

## Status of this document

Draft. A naive default already exists in part — `10-technical/07-naive-context-assembly.md` — and is credited here, not replaced.

## Motivation

`10-foundations/04` established that a context is the set of artifacts currently live, each the product of a crossing from one of three locations, and that none of its four failure modes are checkable without an explicit, first-class live record. This actor owns that record.

## The actor and its responsibility

- **Register** artifacts as they cross in from any tool call — a read, a test run, any effect response — or from the model's own generated output. What crosses in is written to `21-arch-knowledge-model` as an Observation, and what this actor keeps is a **reference to that entry plus its own tracking metadata**: crossing type, live or archived state, and whatever else recall needs. This actor holds no artifact content of its own. It never initiates a crossing either, only records what came back once something else did.
- **Track** the live set registration populates.
- **Recall** — a separate, later decision, governed by an explicit policy: of what is already in the tracked pool, which artifacts are actually fed to the model on a given turn, and which are held back. Recall means presentation, nothing else — it never fetches anything new, it only decides visibility over content already registered. That boundedness is the point: given a fixed pool, a policy chooses a subset, which makes different recall policies directly comparable and testable against each other, holding the pool itself constant.

**The pool is an index, not a store (2026-09-11).** Everything a crossing returns is written to `21-arch-knowledge-model` first, so there is exactly one copy of any artifact's content and this actor points at it. An earlier version of this document made that arrangement a special case for knowledge-base retrievals only, on the grounds that a retrieved claim already had an identity there while a tool output did not. Registering every crossing as an Observation removes the asymmetry: the special case becomes the rule, and the exception disappears.

This is provisional, adopted to see where it leads rather than because it has been shown correct. What it buys is worth naming. One copy instead of two, so the pool cannot drift from the record. A pool that is pure bookkeeping — references and metadata — which is exactly the mechanical-engine half `70-THINKING/ideas.md` I12 describes. And provenance roots that exist by construction: `10-foundations/03` requires a chain's roots to stay raw because nothing regenerates an observation that was never kept, and an observation that is written the moment it crosses is never not kept.

What it costs is write volume, and the answer to that is curation rather than selective registration — see `22-arch-cognition/05-curation.md`.

Knowledge-base retrieval is a tool like any other — the model calls it, the runtime executes it, this actor registers the reference. This actor never initiates that call itself, on a processor's behalf or otherwise. Once a reference is in the pool it is subject to the same recall policy as anything else, regardless of which crossing put it there.

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

How a pool is seeded when a processor starts. Register records what a crossing returned and recall presents what a pool already holds, so neither of this actor's two operations can put anything in a pool before the first crossing — a pool is empty at turn zero by construction. Two shapes are available. Inheritance could be a third primitive alongside register and recall, moving or referencing already-registered artifacts across pools with no crossing involved. Or it could be no new mechanism at all: the preceding step writes a handoff into something durable — an attachment on a work item (`28-arch-work-record`) is the obvious candidate — and the next instance reads it, registering the result exactly like any other read. The second is cheaper and fits what already exists, which is a reason to prefer investigating it first, not a reason to consider it settled.

This is not the fork/join-versus-continuation question (`22-arch-cognition/08`). That one governs whether sibling instances see each other's crossings, which is pool isolation; it says nothing about how much any single pool starts with, and either recombination model works with a thin or a fat seed.

What the recall policy actually is. Named here as a required, distinct responsibility — arbitrary by design, not yet specified — governing recall and archive transitions; nothing here fixes what triggers either direction.

Whether "not yet taken" is indexable for the generation crossing type the way an unread file or an unretrieved claim is — `04` did not settle this.
