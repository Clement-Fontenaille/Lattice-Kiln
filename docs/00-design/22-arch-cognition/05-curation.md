# Curation

## TL;DR

Everything that crosses into a conversation is written to the knowledge model as it arrives. Curation is what later decides which of it the project keeps holding, which of it is compressed to a souvenir, and which of it stops being held at all.

> **Motto:** Remembering is the default; forgetting is the decision.

## Status of this document

First draft, written 2026-09-11. It follows directly from the decision recorded in `23-arch-context-management/01-context-manager.md` that the live pool holds only references into `21-arch-knowledge-model` plus its own metadata, and that every crossing is registered there as an Observation. That decision is itself provisional, so this document is too.

It names the actor, the decision, the mechanism, and the trigger. It does not specify the criterion by which something is judged worth keeping — that is the hard part, and the last section says why it cannot be borrowed from anywhere already written.

## Motivation: the inversion

Until this pass, the arrangement was additive. Artifacts lived in the conversation, the knowledge model held only what had been promoted into it, and anything not promoted simply went away when the episode ended. `10-foundations/05`'s Collapsing described that disappearance, and this pass briefly concluded that Collapsing therefore cost nothing, because nothing performed it.

Registering every crossing inverts that. Nothing goes away on its own any more. The record grows with every tool call, every test run, every generated response, and it keeps growing until something decides otherwise. Forgetting has become an act that needs an actor, a mechanism, a trigger, and a criterion — which is what this document supplies, and what the additive arrangement never needed.

Two things are gained by accepting that cost. Provenance roots now exist by construction: `10-foundations/03` requires a chain's roots to stay raw, because nothing regenerates an observation that was never kept, and an observation written the instant it crosses is never not kept. And there is exactly one copy of any artifact's content, so the live pool cannot drift from the record.

## What curation decides

For each entry, one of three outcomes.

- **Keep raw.** The entry is a root — an Observation that nothing regenerates. A test result, a file's contents as read at a moment, a human's stated constraint. `03` requires these to stay raw, so this is not a judgment about value, it is a classification.
- **Compress to a souvenir.** The entry is a checked demonstration step whose working is re-derivable from roots that are being kept. What remains is its named inputs, its conclusion, and a note of the argument's shape only where the connection between the two is not obvious from those alone (`03`, Provenance). The claim stays; its working goes.
- **Elide.** The entry stops being held. This is the outcome the additive arrangement got for free and now has to be chosen.

Eliding has a hard precondition rather than only a policy. An entry that anything still cites may not be elided, and a root may not be elided, because every souvenir above a root depends on that root remaining available to re-derive from. Eliding a root would quietly turn every souvenir descending from it into an assertion that cannot be checked. `21-arch-knowledge-model` carries this as a constraint on the operation itself rather than leaving it to whoever calls it.

## The criterion is not available anywhere yet

Curation has to judge whether something will be needed by a comparison that has not happened yet. `10-foundations/05` already states the problem precisely: that is a different question from Pertinence, which asks whether a claim matters to the comparison in front of it now, and none of `03`'s three weighing dimensions looks forward at all. Validity, reliability, and pertinence are all assessable against what exists. Expected future need is not.

So curation needs a judgment the substrate does not supply, and this document does not invent one. Naming the absence is the honest position: the mechanism can be built and the criterion left as a parameter, which at least makes different criteria comparable the way `23`'s recall policy does.

## When it fires

Two moments, and they are not the same kind of thing.

**Scope, at creation.** `10-foundations/03` says a claim's scope has to be assessed near its own creation or not at all, because the domain a claim was born into was never fully representable and no later reader recovers it. This cannot wait for a curation pass. It is curation's one obligation that runs at write time.

**Keep, compress, or elide — at the end of an episode.** When a conversation ends, its pool stops being live. That is the natural moment to decide what the episode leaves behind, because it is the first point at which the episode is complete enough to judge. The trigger is therefore a pool lifecycle event in `23-arch-context-management`, even though the decision is a processor's and the mechanism is `21-arch-knowledge-model`'s.

Whether end-of-episode is the only moment is open. A long-running episode might need curation before it ends, and nothing here says what would prompt that.

## Who performs it, and through what

Three actors, each doing the thing it already does.

- **The decision** belongs to a member of the thinking family (`04-thinking.md`). Deciding what the project keeps holding is a proposed change to what the project holds, which is that family's membership test exactly.
- **The mechanism** is `21-arch-knowledge-model`'s Compress and Elide operations. A curation processor proposes; it does not reach into the store.
- **The trigger** is `23-arch-context-management`'s pool lifecycle.

The proposal is a memory mutation like any other (`10-technical/01-effect-vocabulary.md` type 5), so it passes capability policy and the invariant gate before anything is compressed or removed. A processor that could elide directly would be a processor that decides what is true by deciding what remains, which is the authority `10-foundations/02` exists to withhold.

## What Collapsing becomes

`10-foundations/05`'s Collapsing still describes something real — an attempted argument superseded within an episode, which nothing outside the episode ever cited and which is owed no trail. What changes is its mechanics. It is no longer the absence of an act. It is the ordinary outcome of a curation pass deciding that an entry neither roots anything nor was ever checked, and eliding it.

The claim this pass made two days' work ago — that Collapsing is the null case and therefore free — is withdrawn. It was true of the additive arrangement and is false of this one.

One thing survives the change and is worth keeping in view. `05` argues that Collapsing keeps scope assessment cheap by keeping it rare. That argument no longer holds for scope, which now runs at every write. It does still hold for the expensive judgment: deciding expected future need only has to be spent on entries a curation pass actually reaches, not on everything a walk tried along the way.

## Observability holds what curation removes

`26-arch-observability` keeps its own copy of artifacts and events, and under this arrangement that copy is precisely what outlives curation. An entry elided from `21-arch-knowledge-model` may still be reconstructable from observability's history, under observability's own retention rules.

That is not a contradiction of eliding it. The system stops treating an elided entry as something it knows, and stops reasoning from it. An auditor reconstructing how a run went may still find it. Those are different uses, which is why the two stores were separated in the first place.

## General shape and a naive default

The same restraint the rest of the band commits to. A curation pass over one episode's entries, classifying each as root, souvenir-able, or elidable by deterministic rules first: an Observation with no children is a root and stays; a claim with children whose working is long is a souvenir candidate; an entry with no children, no citations, and no check recorded against it is elidable. No model call is needed for any of that.

The criterion that does need judgment — expected future need — is the part to add last, and only once the deterministic pass has a measured failure mode to justify it.

## A failure mode already documented elsewhere

`70-THINKING/07-when-to-decompose/18-ares-soundness.md` describes a retention mechanism over a premise pool, where each claim is carried forward to later steps with probability equal to its own entailment score. Two things in that sheet bear on curation directly, and both are cautions rather than support.

The first is a collapse mode. When the judge is overconfident and returns near-certainty everywhere, every retention probability rises toward one, the pool stops filtering, and the mechanism silently becomes a no-op while still costing everything it cost before. The sheet notes that no diagnostic was proposed to detect this. A curation processor that judges almost everything worth keeping fails the same way, and would be hard to notice, because the symptom is an absence.

The second is more uncomfortable. That paper's own ablation found that keeping *every* base claim, always, was consistently best with its stronger probabilistic judge, and that selective retention only helped a weaker binary one. Their sub-one retention setting was doing overload management — dropping material so the judge was not swamped — which is `10-foundations/04`'s Overload mode under another name. Read across, it suggests eliding may earn nothing except where something downstream is being swamped, and that the case for curation is a case about capacity rather than about tidiness.

Both readings are second-hand (`03`): they come from this project's own analysis sheet about that paper, not from the paper, and the sheet is itself a read of it.

## Open question

What the criterion for expected future need actually is. Named above as absent from `03`'s dimensions and left as a parameter.

Whether eliding pays at all, given the ablation above. The alternative is to compress aggressively and elide nothing, accepting growth in exchange for never having to be right about what will be needed. That is a cheaper position to hold and this document does not argue against it.

What detects a curator that has stopped filtering. The collapse mode above has no proposed diagnostic, and the symptom is an absence rather than an error.

Whether end-of-episode is the only trigger, and what would prompt a pass inside a long-running episode.

How eliding and `03`'s append-only Qualification rule coexist. Append-only governs corrections to a claim that was promoted and relied on; eliding discards an entry nothing built on. The two should not meet, but nothing here proves an entry cannot end up in a state where both apply.
