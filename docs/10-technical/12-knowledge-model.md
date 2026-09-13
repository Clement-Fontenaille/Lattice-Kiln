# Knowledge Model (v0)

**Traces to:** `00-design/21-arch-knowledge-model/01-knowledge-model.md`,
`00-design/10-foundations/03-evidence-belief-and-provenance.md`,
`00-design/10-foundations/05-ephemeral-conversation-curated-memory.md`,
`00-design/22-arch-cognition/04-thinking.md`,
`00-design/22-arch-cognition/05-curation.md`;
binds to `10-technical/01-effect-vocabulary.md` (effect type 5),
`10-technical/02-observability-event-model.md`,
`10-technical/13-work-record.md`,
`10-technical/14-context-manager.md`.

## TL;DR

The durable store for claims and their provenance. Six operations — **Write,
Read, Query, Traverse dependents, Compress, Elide** — over a directed acyclic
graph of Observations, Evidence, Findings and Decisions. It records what it is
given and answers what it is asked; it judges neither the claim nor the question.

> **Motto:** The record outlives the reasoning that made it.

## Status of this document

v0. The **service surface is binding and the storage shape is not**, and that
asymmetry is the document's main structural commitment rather than a hedge: a
naive filesystem store is expected to be replaced, and the replacement has to be a
substitution rather than a rewrite of everything that calls it.

Two things are specified with a placeholder rather than a value, because the
design set has them genuinely open and guessing would be worse than leaving the
field named. **How a claim's scope is inscribed** blocks the record format and is
unanswered. **Who assigns tags, and how** does not terminate under the obvious
answer, and neither escape has been adopted.

## Responsibility

Hold the provenance graph durably across invocations and sessions: every claim,
its type, its source, the mode by which each of its parents was acquired, and the
edges connecting them. Accept new claims, serve queries, compress checked working,
and remove what nothing needs.

It does **not** judge whether a returned candidate is pertinent to the objective in
front of it — pertinence is a property of a comparison and is judged live by
whoever asked (`10-foundations/03`, Weighing claims). It does not detect whether
two claims converge or collide; that is a walk a thinking processor performs, not
a query result this store can precompute.

## Narrowing

`21-arch-knowledge-model/01` states an actor, six services, and a naive shape,
deliberately stopping short of a schema. This document narrows to:

- **Mode of acquisition carried on the edge, not on the claim.** A hand-tagging
  trial against the real corpus found that mode is assessed per *link* of a
  provenance chain rather than once per claim (`90-notes/02` F6) — a result no
  specification written in advance would have caught. A claim with two parents can
  inherit a different mode from each, so a single `mode` field on the claim would
  have to lie about one of them.
- **Two write paths with different gating**, rather than one uniform write.
- **Deterministic matching for the naive query.** Term matching over content and
  tags, edit-distance and token-overlap for fuzzy. Discarded for now: embeddings,
  a vector index, model-mediated retrieval — not as wrong, but as unsequenced.
- **Traverse dependents as its own operation**, not a special case of Query.

## The claim record

Fields marked *(illustrative)* name intent, not a fixed shape.

MUST carry:

- `claim_id` — stable, and referenced from outside this store (by
  `13-work-record.md`'s attachment edges and by `14-context-manager.md`'s live
  set).
- `type` — one of `observation`, `evidence`, `finding`, `decision`.
- `content` — structured, not free prose. What "structured" means per type is an
  open contract; what it excludes is a single unparsed paragraph, because the
  naive query matches over this field.
- `source` — who produced it. An axis across the types, not a fifth type: a human
  and a processor can both produce a finding.
- `parents` — zero or more edges, each carrying the parent's `claim_id` **and the
  mode by which that parent was acquired**: `read`, `reasoned`, `tested`,
  `operated`. A `read` edge additionally carries whether the source is
  **second-hand** — a report of someone else's measurement, reachable only through
  their account of it.
- `scope` — the domain the claim was born into. Its representation is open; the
  field is not. `10-foundations/03` requires scope to be assessed near a claim's
  creation because **no later reader recovers it**, which makes it a requirement
  on this format rather than on somebody's diligence.
- `tags` *(illustrative)* — whatever the producer assigned at write time. The
  naive query matches over these alongside content.

Normative consequences:

- The graph MUST be **acyclic**. Nothing is justified by something that depends on
  it.
- A claim MUST be able to have **several parents** and several children. Evidence
  is defined as an observation *or collection of* observations, and one finding
  diverges into several downstream claims.
- **Source travels, and a flag alone loses it at one remove.** A processor's
  finding derived from a human-stated constraint is system-produced and
  human-rooted, and only the chain carries that. An implementation MUST NOT treat
  the `source` field as sufficient to answer "did anything enter that the system
  did not already hold" — that question is answered by walking.
- A **finding may be negative**, and the store must hold it as an ordinary claim.
  That something is not the cause, that an approach does not work, that a
  hypothesis is eliminated — an investigation that eliminated four possibilities
  produced four findings, and a store that counts only artifacts loses all of it.

## Write — two paths, gated differently

The split is `10-foundations/03`'s motto made operational: **what happened is
recorded automatically; what it means is not.**

**Observations are bookkeeping.** Every crossing `14-context-manager.md` registers
lands here immediately, unproposed and ungated. `01-effect-vocabulary.md` already
classes the runtime recording its own observations as bookkeeping rather than an
effect, so there is nothing to propose and nothing to gate.

**Everything above Observation is a proposal.** Evidence, Finding, Decision, a
qualification, a requalification — each arrives as a **type-5 memory mutation**
from a thinking processor (`00-design/22-arch-cognition/04-thinking.md`) and is
gated like any other.

- An implementation MUST NOT let the bookkeeping path write a claim of type
  `evidence`, `finding` or `decision`. Collapsing the two paths would make every
  crossing a belief, which is the distinction `10-foundations/03` exists to keep.
- Whether the proposing processor must be a member of the thinking family — which
  would make this store write-gated by role — is stated in the architecture as a
  consequence rather than a rule, and is **not** narrowed here.

## Read, Query, Traverse dependents

**Read.** Given a `claim_id`, return the claim and its immediate provenance
neighbourhood. Deterministic, cheap, the identity case.

**Query.** The entry step, and the one open problem among the six. Nothing settles
from first principles which representation finds useful material
(`00-design/23-arch-context-management/02-context-as-experimental-surface.md`), so
the interface is specified as a **parameter surface** rather than a fixed lookup:

- `breadth` — how many candidates, and how loose a match counts.
- `depth` — return the matched claim alone, or walk N hops of its provenance
  neighbourhood with it.
- `matching_mode` — literal, or fuzzy.

These MUST be exposed on every query, the way a tool's parameters are present
whether or not a given call uses all of them. A query interface that hardcodes one
point in this space forecloses the measurements `14-context-manager.md` exists to
run.

**Traverse dependents.** Given a claim, return **what cites it** — the direction
opposite to a provenance lookup. This is a distinct operation because it is the
access pattern the thinking walk is made of: a correction is useful only if what
rests on the corrected claim can be found, and that is a search downward through
children rather than upward through parents. It is satisfied by following child
links, which the naive shape below already records.

Unlike Query, this is **not** an open problem. Once a claim is in hand the graph
says where to go; the difficulty lives entirely in getting the first one.

## Compress — the souvenir

Replace a **checked** claim's full working with a souvenir: its named inputs, its
conclusion, and a note of the argument's shape **only where that connection is not
obvious from the two alone**. The claim stays; its working is what goes.

- A trivial step needs nothing beyond its conclusion. A non-trivial one needs
  enough of its shape that a later reader is not left re-deriving the same insight
  from scratch.
- **A chain's roots MUST NOT be compressed.** Observations and evidence a chain
  bottoms out in stay raw, because nothing regenerates an observation that was
  never kept. Raw detail is required exactly where a claim cannot be reliably
  reconstructed without it, and nowhere else.
- Compression is only valid **after** the step has been checked. An attempted
  argument becomes a demonstration step once validity has checked it and it held;
  compressing before that would preserve a conclusion whose support was never
  verified.

## Elide — and why reachability is nearly the whole retention rule

Remove an entry. **This is the default path rather than an exceptional one**: an
entry no longer live that nothing registered for remembrance is swept, and most of
what crosses is swept.

Using this store as the main home for crossings does **not** make the default
"keep". The knowledge base is where an artifact already sits from the moment it
arrives, which avoids copying it out of a conversation later; it is not a decision
that the artifact is worth keeping.

The precondition is **reachability**:

- An entry that a promoted claim cites is one of that claim's roots.
  `10-foundations/03` makes raw roots the condition on which every souvenir above
  them stays re-derivable.
- **Eliding a reachable root MUST be refused.** Doing it silently converts every
  souvenir descending from that root into an assertion nobody can check — the
  damage is invisible at the moment it is done and appears only when someone tries
  to verify a descendant.
- For nearly everything, reachability is therefore not merely the constraint on
  this operation but the **entire retention rule**, and the sweep is a graph
  traversal needing no judgment.
  `00-design/22-arch-cognition/05-curation.md` holds only the part that does —
  deliberate remembrance — and the criterion for that is absent from
  `10-foundations/03`'s three weighing dimensions by that document's own account.
  Leave it parametric; do not invent one here.

The naive sweep walks the whole graph from a promoted-claim root set. That is
acceptable until it is not: no index, no incremental reachability, no cached
dependent set, until measurement shows the walk is the actual bottleneck.

**The root set is under-specified, and this is the most consequential unknown in
the document.** "Promoted claims" is what the rule names, and **three other stores
hold references into this one**: `13-work-record.md`'s attachment edges,
`14-context-manager.md`'s live set, and `02-observability-event-model.md`. None of
the three is currently named as a reachability root.

Read literally, that has a consequence nobody wants: a Finding attached to a work
item and cited by no other claim is not reachable, so the sweep removes it and
leaves the work record holding a **dangling reference**. An implementation MUST NOT
sweep on that reading. What the root set actually includes is an open contract
below, and until it is closed, an implementation MUST treat a reference held by any
other store as protective.

**Nothing triggers the sweep either.** Per turn, at an instance's end, on a size
threshold, on demand — the document says the sweep is the default path and never
says when the default runs. Also open below.

## General shape and the naive default

**The filesystem. No database, no vector index, no model-mediated retrieval**,
until evidence says the naive version is the actual bottleneck.

Read that as sequencing rather than doubt. A proper ontology, model-mediated
retrieval and a real graph store are expected to become necessary; what the naive
default buys is that each arrives on evidence about this project's own access
patterns rather than on a guess made before any access pattern existed.

Illustrative default:

```
knowledge/
  claims/<claim_id>.json        # type, content, source, scope, tags, parents[]
  children/<claim_id>.jsonl     # child links, appended on every write
```

The `children/` index is redundant with `parents[]` and is kept anyway, because
Traverse dependents is a first-class operation and deriving it by scanning every
claim would make the walk quadratic in the corpus from the first day.

`10-foundations/03`'s four types and its source, mode and scope axes are already
the beginning of the ontology. They were arrived at from real cases — a
hand-tagging trial, the ETH correction — rather than designed in advance, which is
the shape the rest of it should take.

This is not a new invention either. `50-findings/` and `90-notes/02`'s Grounds and
Changed lines are already hand-maintained claims with explicit provenance
citations in plain files. The naive default formalizes a practice the project runs
by hand.

## Authority

- The store **records and serves**. It never judges pertinence, never ranks
  results, never decides that two claims collide.
- Claims above Observation enter only through a **realized type-5 effect**. A
  cognitive component writing to the store directly is a defect of the same class
  as bypassing the gate.
- It **may refuse** an Elide whose target is reachable, and a Compress whose
  target is a root or an unchecked step. These are the only refusals it makes.
- **Nothing in the permission or invariant layers depends on this store.** The
  gate is deliberately not smart; consulting a knowledge graph before deciding
  would reintroduce the persuadability `25-arch-invariant-layer` exists to close
  off. That is a boundary holding cleanly, not a gap to fill later.

## Failure modes

- **Eliding a reachable root.** The worst failure here, and the quietest: every
  descending souvenir becomes unverifiable and nothing reports it. The reachability
  refusal is the only thing standing in the way, so a sweep that bypasses it is a
  defect even when it removes nothing important.
- **Mode recorded once per claim.** Flattens a multi-parent claim onto whichever
  parent was written first, and F6 says this is the case that actually occurs.
- **Source read off the flag.** Treating `source` as sufficient loses
  human-rootedness at one remove, which is precisely the question the axis exists
  to answer.
- **Compressing an unchecked step.** Preserves a conclusion whose support was
  never verified and discards the means of verifying it, in one operation.
- **Prose content.** A claim written as one unparsed paragraph cannot be matched
  over, joined on, or compressed into a souvenir with named inputs. This is the
  same failure M2 and M5 both recorded on the effect envelope: reconstruction
  answered unplanned questions only where the record carried structure rather than
  prose.
- **A query result treated as an answer.** Pertinence is judged by the caller. A
  store that ranks and returns a single best match invites the caller to skip the
  judgment it is supposed to make.
- **Storage leaking into the interface.** A caller that can learn a claim is a file
  turns the eventual move to a real store into a rewrite of everything calling it —
  the one way a deliberately crude starting point becomes a trap.
- **Claim content copied into another store.** `13-work-record.md` and
  `14-context-manager.md` both hold references. A copy goes stale silently.

## Relationships

- **`10-foundations/03`** — owns the schema this store realizes.
- **Effect vocabulary** (`01-effect-vocabulary.md`) — type 5 is the gated write
  path; runtime bookkeeping is what the Observation path is classed as.
- **Context manager** (`14-context-manager.md`) — registers every crossing here and
  keeps only references plus its own metadata. It never queries this store on its
  own initiative: the model calls a retrieval tool, the tool queries here, and
  whatever comes back registers like any other tool output.
- **Work record** (`13-work-record.md`) — holds attachment edges pointing into this
  store. One direction only: that store resolves claims against this one, and this
  one knows nothing about work items.
- **Observability** (`02-observability-event-model.md`) — a **separate store, not a
  shared one**. "Why did this change become trusted" is the same reconstruction
  question, but claims and run history have different lifecycles and different
  retention needs, so observability keeps its own copy rather than reading this
  graph.
- **Runtime** (`20-arch-runtime.md`) — persists what a write resolves to, the same
  way it persists any other selected state.

## Open contracts

- **What the reachability root set contains.** Stated as "promoted claims" while
  three other stores hold references here. Candidates for inclusion: a work-item
  attachment, a live-set entry, an operator-marked claim. Whichever way it goes, the
  answer decides what the sweep removes, which makes it the retention rule itself
  rather than a detail of it. Surfaced by `15-information-trajectories.md`.
- **What "promoted" means.** It carries the root set and therefore the whole
  retention rule, and no document in this set defines it. Candidates: any claim
  above Observation, any claim a type-5 proposal realized, any claim something else
  cites. They are not the same set.
- **When the sweep runs.** No trigger is specified anywhere.
- **How scope is inscribed.** Blocks the record format rather than following from
  it. `10-foundations/03` requires it assessed near creation because no later
  reader recovers it; what actually goes in the field is unanswered.
- **Who assigns tags, and how.** The obvious answer — a thinking processor does it
  — does not terminate: interactions with the model *are* the discussion, so a
  labelling call is itself a crossing producing an artifact that would need
  labelling. Two escapes exist and neither is adopted. **Inline**: ask the
  producing model to emit labels and relations with its output, removing the
  separate call and the regress, at the cost of coupling label quality to format
  compliance. **Out of band**: a smaller specialised model whose calls are not part
  of the discussion being labelled, which makes labelling separately evaluable and
  trainable, at the cost of a labeller that never saw the reasoning it annotates.
- **Structured content per type.** What structure an Observation carries versus a
  Decision. Required to be structured; the shape is not fixed.
- **Deletion versus supersession.** `10-foundations/03`'s append-only
  qualification rule governs *corrections to a promoted claim that others relied
  on*. Elide governs *discarding an Observation nothing ever built on*. Both are
  right; what is not settled is whether an entry can exist in a state where neither
  clearly applies.
- **Query representation.** Which retrieval representation actually finds useful
  material. Held open deliberately as
  `00-design/23-arch-context-management/02-context-as-experimental-surface.md`'s
  subject rather than as a gap here.
- **Peak size.** Steady-state size is bounded by what is live plus what was
  remembered, since the sweep removes the rest. **Peak** size during a long episode
  is unmeasured, and it is the figure a naive filesystem shape feels first.
- **Whether the walk must be indexed.** The naive sweep and the naive dependent
  traversal both walk from scratch. `70-THINKING/ideas.md` I5 holds the
  architecture-scoped version of this question; nothing here adopts it.
