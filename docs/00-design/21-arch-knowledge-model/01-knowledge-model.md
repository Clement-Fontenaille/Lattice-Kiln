# Knowledge Model

## TL;DR

The knowledge model holds `10-foundations/03`'s substrate — claims and their provenance — as a durable, queryable record that outlives any one processor invocation.

> **Motto:** The record outlives the reasoning that made it.

## Status of this document

Draft. States the actor's responsibility, the service it provides, and a general shape — deliberately not a schema, a storage format, or a query language, all of which belong to technical specification.

## Motivation

`10-foundations/03` defines what a claim is, how it is weighed, and how provenance connects them into a graph. It does not say where that graph actually lives between invocations, or how a processor gets a claim in or out. Without an actor responsible for this, `03`'s substrate stays a schema with no home — findings and observations would persist only for the duration of one conversation, which is exactly the gap `10-foundations/05` (curated memory) argues this project cannot afford to leave open.

## The actor and its responsibility

Hold the provenance graph durably: every claim — Observation, Evidence, Finding, Decision — its source, mode of acquisition, and prior weighing, and the edges connecting them, across processor invocations and sessions. Accept new claims proposed by a processor (a memory-mutation effect, `10-technical/01-effect-vocabulary.md` type 5) and record them with their provenance intact. Serve queries against what it holds without judging what the query means or whether a result is actually pertinent — that judgment stays with whoever asked (`03`, Weighing claims).

## Service provided to the rest of the system

- **Write.** Given a claim and its parent links, persist it and confirm. Two paths reach this, and they are not the same kind of act. An **Observation** is written as bookkeeping: every crossing `23-arch-context-management` registers lands here immediately, unproposed and ungated, because `10-technical/01-effect-vocabulary.md` already classes the runtime recording its own observations as bookkeeping rather than an effect. Everything above Observation — Evidence, Finding, Decision, a qualification, a requalification — arrives as a **proposal** from a thinking processor (`22-arch-cognition/04-thinking.md`) and is gated like any other memory mutation. `10-foundations/03`'s motto is the line: a conclusion is not an observation, so what happened is recorded automatically and what it means is not.
- **Compress.** Replace a checked claim's full working with a souvenir — its named inputs, its conclusion, and a note of the argument's shape only where that connection is not obvious from those alone (`10-foundations/03`, Provenance). The claim stays; its working is what goes.
- **Elide.** Remove an entry. This is the default path rather than an exceptional one: an entry no longer live that nothing registered for remembrance is swept, and most of what crosses is swept. The precondition is **reachability** — an entry a promoted claim cites is one of that claim's roots, and `03` makes raw roots the condition on which every souvenir above them stays re-derivable, so removing one would silently convert every souvenir descending from it into an assertion nobody can check. Reachability is therefore both the constraint on this operation and, for nearly everything, the entire retention rule; `22-arch-cognition/05-curation.md` holds only the part that needs judgment instead.
- **Read.** Given a claim's identity, return the claim and its immediate provenance neighborhood.
- **Query.** The entry step, and the one open problem on this list — `23-arch-context-management/02-context-as-experimental-surface.md` treats it as such, since nothing settles from first principles which representation finds useful material. A rich interface, not a single fixed lookup — the caller sets breadth (how many candidates, how loose a match counts), depth (return just the matched claim, or walk N hops of its provenance neighborhood too), and matching mode (literal text, or fuzzy). These are parameters exposed on the query itself, always available, the same way a tool's own parameter surface is present whether or not a given call uses all of it.
- **Traverse dependents.** Given a claim, return what cites it — the direction opposite to a provenance lookup. This is a distinct service rather than a special case of Query, because it is the access pattern `22-arch-cognition/04-thinking.md`'s walk is made of: a correction is useful only if what rests on the corrected claim can be found, and that is a search downward through children rather than upward through parents. It is satisfied by following child links, which the naive shape below already records. Unlike Query above, this is not an open problem: once an artifact is in hand the graph says where to go, and the difficulty lives entirely in getting the first one.

Explicitly not provided: whether a returned candidate is pertinent to the objective in front of it (`03`, Weighing claims — pertinence is judged live by whatever is asking); whether two claims converge or collide (`03`, Friction and re-evaluation — that is a walk Thinking performs, not a query result this actor can precompute).

## General shape and a naive default

`50-findings/07-m5-followup-investigation.md` (judge-lab) already showed a deterministic mechanism beating a 7B judgment panel at an adjacent decision, and `10-technical/07-naive-context-assembly.md` already commits its own naive default to the same restraint — no embeddings, no model calls. The knowledge model's naive shape should hold to it too: claims as structured records, not free prose, each carrying explicit parent-claim identities; held in the filesystem; queried by deterministic term-matching over claim content and whatever tags a processor assigned at write time, walking parent/child links for depth. Fuzzy does not mean embeddings — edit-distance and token-overlap matching are deterministic and satisfy it within the same discipline. No graph database, no vector index, no model-mediated retrieval, until evidence says the naive version is the actual bottleneck.

**The restraint is about sequencing, not about doubt.** A proper ontology, model-mediated retrieval, and a real graph store are expected to become necessary. That is not held open as a question. What the naive default buys is that each of them arrives on evidence about this project's own access patterns, rather than on a guess made before any access pattern existed — and that the project learns what it actually asks of this store before paying to make those questions fast.

One obligation follows, and it is worth stating now because it costs nothing now and a great deal later. What must stay stable across that replacement is this actor's **service surface** — Write, Read, Query, Traverse dependents, Compress, Elide — and not its storage shape. A caller must never learn that a claim is a file. If paths, file formats, or directory structure leak into the interface, the eventual move to a real store stops being a substitution and becomes a rewrite of everything that calls it, which is the one way a deliberately crude starting point can turn into a trap.

`10-foundations/03`'s four claim types, and its source, mode-of-acquisition and scope axes, are already the beginning of that ontology. They were arrived at from real cases — a hand-tagging trial, the ETH correction — rather than designed in advance, which is the shape the rest of it should take as well.

This is not a final answer — it is `10-foundations/04`'s "a naive default is still required" argument, applied here: something crude and measurable, so a smarter version has a baseline to beat. It is also not a new invention: `50-findings/` and `90-notes/02`'s own Grounds and Changed lines are already hand-maintained claims with explicit provenance citations in plain files. The naive default formalizes a practice this project is already running by hand.

## Interactions

- A processor proposes a claim, typically a Finding, once Thinking has checked it; this actor persists it. `22-arch-cognition/04-thinking.md` argues that the proposing processor should always be a member of the thinking family, since a knowledge-state transition is that family's defining product — which would make this actor write-gated by role. That is stated there as a consequence rather than a rule, and this document keeps the unqualified "a processor" until it is argued rather than assumed.
- `23-arch-context-management` never queries this actor on its own initiative. The model calls a retrieval tool; the tool queries this actor; the context manager registers whatever comes back, the same as any other tool output.
- `26-arch-observability` has an overlapping interest: "why did this change become trusted" (`03`, Provenance) is the same reconstruction question observability exists to answer. They are separate stores, not one shared between them — see Relationships, below.
- `28-arch-work-record` holds references to claims held here, attaching a finding, proposal, or decision to a work item. The reference points one way only: that actor resolves claims against this one, and this actor knows nothing about work items. Claims stay the unit of truth; work items are what they are attached to.
- `24-arch-permission-layer` and `25-arch-invariant-layer` have no dependency on this actor. The invariant gate is deliberately not smart (`25-arch-invariant-layer/01`); consulting a knowledge graph before deciding would reintroduce exactly the persuadability that document exists to close off. This is a boundary that holds cleanly, not a gap to fill later.

## Relationships

- **`10-foundations/03`** — owns the schema this actor realizes.
- **`22-arch-cognition/04-thinking.md`** — the family whose proposals change what this actor holds, and the consumer of dependent traversal.
- **`23-arch-context-management`** — the primary consumer of queries.
- **`26-arch-observability`** — a separate store, not a shared one. Claims here and observability's history have different lifecycles and different retention needs, so observability keeps its own copy rather than reading this actor's graph directly.
- **`28-arch-work-record`** — a separate store holding one-way references into this one. A claim is append-only and superseded here; a work item there is mutable, which is why the two are not one store.
- **`20-arch-runtime.md`** — persists whatever this actor's writes resolve to, the same way it persists any other selected state.

## Open question

What "a tag a processor assigned at write time" actually looks like as a concrete mechanism, and **who assigns it**. The obvious answer — a thinking processor does it — was proposed and rejected, because it does not terminate: interactions with the model are the discussion, so a labelling call is itself a crossing producing an artifact that would in turn need labelling. Two escapes exist and neither is adopted. Labels can be carried **inline**, by asking the producing model to format its output so that labels and relations come with it, which removes the separate call and therefore the regress. Or they can be assigned **out of band** by a smaller, more specialised model whose calls are not part of the discussion being labelled. The first couples label quality to the reasoning model's compliance with a format; the second makes labelling a separately evaluable and trainable capability, at the cost of a labeller that never saw the reasoning it is annotating. `90-notes/03` holds the fuller statement.

The methodology sits underneath both and is unanswered either way. The one prior result is instructive: a hand-tagging trial against the real corpus found that mode of acquisition is assessed per *link* of a provenance chain rather than once per claim (`90-notes/02` F6), which no specification written in advance would have caught. Running that trial again with the current vocabulary is the cheapest way to find whatever the next such result is.

How **scope** is concretely inscribed. `10-foundations/03` requires it to be assessed near a claim's creation because no later reader recovers it, which makes it a requirement on this actor's format and not only on somebody's diligence. Whatever scope turns out to be, this store has to be able to hold it, so this question blocks the data format rather than following from it.

Whether claims are ever deleted or only ever superseded. `03`'s append-only Qualification rule suggests the latter, which has storage-growth consequences a naive filesystem shape will feel before a smarter one would. **Elide** above is a partial answer and sharpens the rest of the question: append-only governs *corrections* to a claim that was promoted and relied on, which is a different matter from discarding an Observation nothing ever built on. What is not settled is whether those two rules can coexist without an entry existing in a state where neither clearly applies.

How much of this store is raw Observation rather than anything anyone reasoned about, once every crossing registers here (`23-arch-context-management`, The live set is an index). Steady-state size is bounded by what is live plus what was remembered, not by cumulative writes, since the default sweeps everything else. Peak size during a long episode is the part nothing has measured, and it is the one a naive filesystem shape would feel first.
