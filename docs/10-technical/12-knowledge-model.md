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

**No write revises an existing entry.** Content is fixed when an entry is created
(`01-effect-vocabulary.md`, type 5). A qualification or a requalification is a new
entry plus an edge, never an edit to the entry it qualifies, which is
`10-foundations/03`'s append-only rule made structural rather than conventional.

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

Produce a souvenir — named inputs, a conclusion, and a note of the argument's shape
**only where that connection is not obvious from the two alone** — for a **checked**
claim, and drop the working it replaces.

**This creates rather than rewrites.** An entry's content is never revised
(`01-effect-vocabulary.md`, type 5), so a souvenir is a new entry with its own edges
to the roots, and what happens to the working is deletion rather than replacement.

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
- **Splitting a processor's output does not perform this operation.** Reasoning and
  conclusion arriving as separate artifacts (`14-context-manager.md`) makes the
  working separable, and separable is not compressed: dropping the reasoning leaves a
  conclusion without its named inputs or its argument's shape, which is a bare
  assertion. Compression likely needs a step that analyses the argument and labels its
  stages, and no evidence supports expecting a model to annotate its own reasoning
  finely enough to skip that.

## Elide — and why reachability is nearly the whole retention rule

Remove an entry. **This is the default path rather than an exceptional one**: an
entry no longer live that nothing registered for remembrance is swept, and most of
what crosses is swept.

Using this store as the main home for crossings does **not** make the default
"keep". The knowledge base is where an artifact already sits from the moment it
arrives, which avoids copying it out of a conversation later; it is not a decision
that the artifact is worth keeping.

### The root set, and what promotion is

Reachability is computed from a **root set with exactly two sources**.

- **Promoted artifacts.** **Promotion is inscription in the root set** — that is what
  the word means here, and it is deliberately an *act* rather than a property derived
  from a claim's type. Nothing is promoted by being a Finding rather than an
  Observation; something is promoted when something promotes it.
- **The live set.** Everything attached to a live task is a root for as long as that
  task exists (`14-context-manager.md`). Note what this is **not** keyed to: not
  whether the model was recently shown the artifact, but whether a task still holds
  it. Being worked on is the reason to keep something, and it expires on its own when
  the work ends.

An entry is kept when a root reaches it by following provenance links. The rest of
this section is the consequence.

### Removal is incremental, and there is no sweep

A periodic sweep over the whole graph is **not needed**, and specifying one would
add a mechanism the information does not require.

The reason is that reachability only ever changes at moments the system already
knows about. A root enters the set when something is promoted or registers as live.
A root leaves it when an item **leaves the live set**, and at that moment the system
holds the departing item's identity — it does not have to go looking for what
changed.

**A task ending is the trigger**, because that is when its live set ends and its
members stop being roots. Removal runs there:

- Each artifact the ending task held loses its root status. If it is not also
  promoted, and no other live task holds it, it is a deletion candidate.
- From it, walk **up** its provenance edges. Each ancestor is deleted if it is not
  promoted **and** no remaining path from any root still reaches it.
- That second condition is what the child index exists for. An ancestor may be
  reachable through a different descendant that is still live or promoted, and
  deleting it on the strength of one departing child would be the reachable-root
  failure below, arrived at by arithmetic instead of by carelessness.

This trades one large occasional cost for many small ones, and it removes the
question of when a sweep runs by removing the sweep. It is also what makes the
naive filesystem shape viable for longer: nothing walks the whole graph.

**Precondition: eliding a reachable root is still refused.**

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

**Observability holds references here and is not a root**, deliberately. It keeps
its own copy precisely so that what is removed here remains reconstructable there.
A deleted entry stops being something the system knows and stays something an
auditor can find.

**The work record's attachments are a narrower case than they look.** Attachment to
a task is what live-set membership *is*, so anything a live task holds is already a
root and cannot be deleted underneath it. What `13-work-record.md` adds is a
**deliberate, curated** attachment — this Finding, this decision, as opposed to
everything that happened to cross. The two relations have the same shape and
different weight.

The residual question is what happens to a curated attachment when its task ends.
Either the deliberate act promotes — which would be the point of making it deliberate —
or the attachment is expected to dangle afterwards and `13-work-record.md` must
detect it. Open below.

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

- **Whether a curated attachment promotes.** While its task lives, an attached
  claim is a root by virtue of the task holding it. When the task ends, a deliberate
  attachment is exactly the kind of act that ought to promote — and does not, as
  specified. Either it does, or the work record detects dangling attachments. Both
  are cheap; they are not the same behaviour.
- **Who promotes, and on what.** Promotion is an act rather than a property, which
  leaves open which actors hold it and what they weigh. The natural reading is a
  thinking processor at the moment it proposes a claim worth keeping, but a claim
  can also deserve promotion long after it was written.
- **Cost of the incremental walk.** Removal now runs on every departure from the
  live set rather than occasionally over everything. That is the right trade at this
  size and nobody has measured where it stops being one.
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
- **Deletion versus supersession.** Now largely settled by content being immutable:
  a correction is always a supersession, and deletion is always by reachability. What
  remains is whether a **superseded** entry is itself subject to deletion once the
  task that held it ends, since it is reachable from its successor and that may be the
  only thing keeping it.
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
