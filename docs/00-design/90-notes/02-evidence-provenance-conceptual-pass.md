# Findings — the evidence-belief-and-provenance conceptual pass

**Date:** 2026-09-10
**Serves:** `10-foundations/03-evidence-belief-and-provenance.md`, revised in place across
this pass, and — from F15 onward, once Thinking turned out to be misplaced in `03` —
`10-foundations/02-reasoning-vs-runtime.md` as well. This file is the justification
record for both revisions — the design-set counterpart to `50-findings/`, produced by a
design conversation and a hand-tagging trial against the existing corpus rather than by
a milestone experiment.

Each entry states a claim, the mode by which the claim itself was produced (not the
mode of whatever it is about — the two can differ, per the pass's own third finding),
what grounds it, and what it changed — in `03` through F14, in both documents from F15.

---

## F1 — Mode of acquisition needs a fourth value: Reasoned

**Claim.** A claim synthesized through live argumentation, with no preexisting written
source behind it, does not fit Read, Tested, or Operated. It needed its own value.

**Mode: Operated.** Found by applying the three-mode draft to real corpus items, not by
discussing the taxonomy in the abstract.

**Grounds.** `70-THINKING/ideas.md` entries I6–I9 are each provenance-tagged "Discussion
2026-09-0X" rather than tied to a sheet — a distinction the project's own working
practice ([[praxis-run-the-knowledge-model]] memory: "keep provenance on
conversation-born bits") already tracked informally before this document named modes.

**Changed.** `03` §Mode of acquisition: added **Reasoned** as the second of four modes.

---

## F2 — Infrastructure self-characterization does not sort into any of the four modes

**Claim.** Measuring the project's own hardware (`50-findings/01`) is neither a
stand-in for real conditions (it is the real host) nor the work the project exists to
do (it characterizes the substrate, not a task performed on it).

**Mode: Operated.** Found by tagging `50-findings/01` directly during the trial.

**Grounds.** `50-findings/01-m0-inference-envelope.md` — a direct hardware measurement,
none of it a benchmark standing in for something else, none of it the system doing
externally-facing work.

**Changed.** `03` §Mode of acquisition: recorded as an open, unforced case rather than
assigned a mode; carried into Open question as possibly needing a fifth mode.

---

## F3 — "Default weight favors operated evidence" was wrong

**Claim.** Mode of acquisition ranked as an absolute ordering (operated > tested > read)
substitutes a fixed rule for the judgment a real comparison requires, and collapses
several independent dimensions (validity, reliability, pertinence) into one. Weight is
relative — it exists only as a comparison, for a question, in a context — not a
property a claim carries alone.

**Mode: Reasoned.** Raised directly in design discussion; no file was consulted to
produce this correction, only the argument itself.

**Grounds.** None external — the argument stands on its own logical shape. This is
itself a first instance of a claim whose mode is Reasoned and whose validity, not
reliability, is what should be checked.

**Changed.** `03`: removed the default-weight ranking; added **Weighing claims**
(validity / reliability / pertinence, held open-ended, not closed).

---

## F4 — Reliability and pertinence are already practiced by hand; validity is not

**Claim.** `50-findings/09` already carries a **Reliability** grade and a separate
**Why it is held** line (pertinence, in effect) on every entry, predating this
document. No entry there separates out validity as its own line — it is folded into
the reliability prose.

**Mode: Operated.** Found by reading `50-findings/09` directly during the trial, not
by inference from the concept.

**Grounds.** `50-findings/09-field-evidence-2026-09.md`, all seven numbered entries.

**Changed.** `03` §Weighing claims cites this file as existing precedent for two of the
three dimensions, and flags validity's absence as unresolved rather than assumed.

---

## F5 — Second-hand is a distinct case of Read that needs its own label

**Claim.** A read claim can be a source's own argument, or it can be a report of an
event — a measurement, a test, an operation — performed by someone else, reaching this
project only through their account of it, over a chain this project cannot inspect or
re-run. The two are not the same reliability situation and the original Read
definition did not distinguish them.

**Mode: Reasoned**, prompted directly in discussion.

**Grounds.** `50-findings/09` is entirely this case: vendor benchmarks and one RCT,
none of them this project's own measurement.

**Changed.** `03` §Mode of acquisition: added **second-hand** as a labeled sub-case of
Read.

---

## F6 — Mode is assessed per link of a claim's chain, not once for the claim as a whole; the trial's "no operated evidence" conclusion does not survive this

**Claim.** A finding that investigates, verifies, or grades second-hand evidence is not
itself second-hand — it is the product of the project's own investigative work. Since
an evidence item and the finding built from it can carry different modes, a corpus with
no read claim above second-hand can still contain operated findings.

**Mode: Reasoned**, prompted directly in discussion; confirmed by re-reading the
correction record described in F7.

**Grounds.** The correction described in F7 below is the concrete instance: real
investigative work, with real stakes, carried out by the project — not read about or
reasoned through in the abstract.

**Changed.** `03` §Why mode of acquisition is tracked: added the per-link principle and
withdrew the earlier trial conclusion that no operated evidence exists in the corpus.

---

## F7 — The ETH correction was triggered by friction from use, a day before the scheduled verification pass, not by that pass

**Claim.** The ETH sign-inversion error was not caught by the systematic primary-source
verification pass (`06-primary-source-verification.md`, run 2026-09-05). It was caught
on 2026-09-04, when the misread claim ("authorship is the operative variable") was
cited as load-bearing external evidence for `02-capability-as-granularity.md`'s OQ-7.
Citing it for that use meant re-engaging the paper closely enough to state precisely
what it supported, and the same paper's own redundancy-ablation result directly
contradicted the authorship reading. The scheduled pass the next day re-confirmed the
correction and caught smaller, unrelated issues, but did not originate this one.

**Mode: Operated.** Found by reading `03-how-the-field-frames-it.md` §5 and
`06-primary-source-verification.md` directly, after an earlier turn in this
conversation mis-attributed the catch to the scheduled pass — the kind of error this
whole framework exists to catch, caught by checking rather than by further discussion.

**Grounds.** `70-THINKING/03-how-the-field-frames-it.md` §5 (`Correction (2026-09-04)`);
`70-THINKING/06-primary-source-verification.md` ("Why this exists": *"One error had
already been caught and re-derived... This is that pass, run 2026-09-05"*).

**Changed.** `03`: added **Friction and re-evaluation** — friction (an incidental
contradiction surfacing from using a claim) and scheduled audit are named as two
distinct, non-substitutable triggers for re-evaluation; corrected the earlier
(F6-adjacent) mis-attribution of which event caught the ETH error.

---

## F8 — Provenance is a graph, not a chain

**Claim.** "Chain" language throughout `03` assumed one predecessor and one successor
per claim. That is false to the document's own Evidence definition ("an observation
*or collection of* observations" — convergent by construction) and to how findings in
this pass are already cited in multiple places at once (divergent).

**Mode: Reasoned.** Argued directly from the document's own existing definitions, not
from an external check.

**Grounds.** `03`'s own Evidence section (pre-existing text); the ETH case itself, where
the authorship and redundancy readings are siblings off one paper rather than a single
line.

**Changed.** `03` §Provenance: added the DAG paragraph; "chain" redefined as one path
through the graph, not the graph itself.

---

## F9 — Friction is not what Weighing claims already settles

**Claim.** An earlier draft of `03` defined friction as any comparison a weighing
process fails to reconcile. That is too broad: a strong claim beating a weak one is an
ordinary weighing outcome. Friction is the narrower case where both sides carry enough
standing that neither is cheaply dismissed.

**Mode: Reasoned**, a direct correction raised in discussion, not derived from a file.

**Grounds.** The ETH case re-examined under this narrower definition: both readings
trace to the same paper, so they were tied on source, reliability, and mode — nothing
in an ordinary weighing comparison could have separated them. This is a real property
of that case, but the *general* claim ("friction requires comparable standing on both
sides") is not independently verified beyond it — see Unchecked justifications, below.

**Changed.** `03` §§Weighing claims / Friction and re-evaluation: friction redefined
against weighing rather than standing independently; the two sections now
cross-reference each other.

---

## F10 — Re-evaluation's outcome is a recorded requalification, not an inversion

**Claim.** When a correction resolves friction, the usual outcome adjusts a claim's
standing (which grounds still support it) rather than inverting or deleting it — and
that outcome should be appended, never substituted for the original, matching
`50-findings/`'s existing Addendum convention.

**Mode: Operated.** Found by reading the actual disposition of OQ-7 after the ETH
correction, not by assuming what "correcting a claim" should look like.

**Grounds.** `70-THINKING/02-capability-as-granularity.md` / `03-how-the-field-frames-it.md`
§5: OQ-7 "keeps its two argued legs... and loses its empirical one. Moved to
'Challenged.'" Not deleted, not inverted — requalified, with the change dated and
named.

**Changed.** `03` §Friction and re-evaluation: added the append-only / requalification
rule, with OQ-7 as the worked example.

---

## F11 — Decision was never exempt from Mode of acquisition, Weighing claims, or friction

**Claim.** A prior turn's framing ("Decision is untouched by this pass") was imprecise.
`03` already states Mode of acquisition and Weighing claims as independent of claim
type, so Decision was already covered; there is no exemption to grant. What is
genuinely unresolved is narrower: `03`'s own Source section already puts Decision on a
different revision footing than Finding ("free to challenge" versus "may not quietly
revise"), and nothing states whether friction reaching a decision's grounds is, on its
own, enough to reopen the decision.

**Mode: Reasoned**, a correction to my own prior framing, raised directly in
discussion.

**Grounds.** `03`'s own pre-existing text (the independence clause; the Source-section
asymmetry). No external case was checked — no actual Decision in this project's record
has yet been hit by friction, so the "unresolved" half of this finding is argued, not
observed.

**Changed.** `03` §Friction and re-evaluation: added the non-exemption statement and
the open question about a decision's revision bar.

---

## F12 — A connective step has two stages: attempted argument, then demonstration step

**Claim.** Calling an inferential move a "demonstration step" at the moment it is
constructed claims a success that has not yet been checked. What exists at
construction is an **attempted argument**; it is promoted to a demonstration step only
once Weighing claims' validity check confirms it holds.

**Mode: Reasoned**, a direct correction raised in discussion.

**Grounds.** The root README's own phrase, "each stone an attempted demonstration"
(checked, direct quote), read literally: attempt and demonstration are not the same
word for a reason. Reasoned mode's own definition, "live argumentation," is why
"argument" was chosen over "demonstration" for the unchecked stage — argument is
already the project's word for the live, dialogic case.

**Changed.** `03` §Mode of acquisition, §Weighing claims, §Provenance, and (relocated in
a later pass, see F15) `02-reasoning-vs-runtime.md` §Thinking: all carry the two-stage
terminology consistently.

---

## F13 — Convergence is friction's positive counterpart, and already has precedent

**Claim.** Two independently-produced claims that agree without depending on each
other are informative in their own right — evidence the chain is not one idiosyncratic
accident — distinct from friction and not yet named anywhere in `03`.

**Mode: Operated.** Found by re-reading `50-findings/09` specifically for this pattern,
not by inventing the concept first and looking for confirmation after.

**Grounds.** `50-findings/09-field-evidence-2026-09.md` §1 ("Directionally consistent
across three independent vendors, which is the main reason to credit it at all") and
§7 ("positions this project reached independently appear in the field... That
convergence is corroborating") — the word "convergence" is already there, predating
this document.

**Changed.** `03` §Friction and re-evaluation: added **Convergence**, and its
distinct response (corroboration, not re-evaluation — nothing to resolve).

---

## F14 — Dependent-discovery is answered in principle by a graph walk; indexing it is architecture's problem

**Claim.** How a corrected claim's other dependents get surfaced, unanswered since F10,
is answered in principle by recursively walking Provenance outward from the corrected
claim, checking each stop for friction or convergence, forming and checking the
attempted argument each implies, and repeating to a fixed point. Doing this
efficiently at scale — an index of dependents, rather than a walk from scratch each
time — is a separate, architectural question.

**Mode: Reasoned.** Proposed directly in discussion (by the user); formalized here
against `03`'s existing vocabulary.

**Grounds.** No external check. This composes only concepts already in `03` (Provenance,
attempted argument / demonstration step, friction, convergence) and has not been
tested against an implemented provenance store, because none exists yet — see
Unchecked justifications.

**Changed.** `03`: added a walk-based answer for dependent-discovery (relocated in a
later pass, see F15); connected it to `70-THINKING/ideas.md` I5 (descendant
invalidation) as the architectural, indexed version of the same walk.

---

## F15 — Thinking was misplaced in `03`; relocated to `02-reasoning-vs-runtime.md`

**Claim.** The walk procedure (F14) is a reasoning activity — interpreting, comparing,
revising conclusions — not a substrate fact. It belongs with `02-reasoning-vs-
runtime.md`'s cognitive side, which already named exactly this activity in bare form
("interpret, challenge, investigate, compare... revise") without ever elaborating it.
`03`'s job is the substrate both the cognitive and runtime sides of `02` draw on, not
either side's procedure.

**Mode: Reasoned**, a structural correction raised directly in discussion, prompted by
stepping back and reading `03` as one document rather than as a sequence of patches.

**Grounds.** `02-reasoning-vs-runtime.md`'s own pre-existing text, read directly rather
than assumed: "Processors and orchestrators may interpret, challenge, investigate,
compare, delegate, propose, and revise their own conclusions" (Cognitive side), and
"The runtime owns persistence, effect execution... provenance..." (Runtime side) —
provenance was already claimed there, unnoticed until this pass looked.

**Changed.** `03`: removed §Thinking; added §Scope, stating plainly that the document is
substrate for context management, thinking, and doing, not a description of any of
them; left a pointer where the walk used to live. `02-reasoning-vs-runtime.md`: added
§Thinking (the walk, reframed as the concrete elaboration of the existing cognitive-side
verbs); a sentence in Proposal and effect connecting a walk's conclusion to the existing
proposal/effect boundary (thinking proposes, the runtime persists); and a
stopping-condition open question mirroring the runtime-validation one already there.

---

## F16 — Feedback was entirely missing: the bridge between thinking, doing, and new information

**Claim.** Neither document accounted for how new information enters the substrate.
Thinking's walk (F14, F15) only traverses claims already recorded; nothing described
what happens when a walk needs something the graph does not yet hold. A first attempt
to name this collapsed investigation entirely into doing ("investigation... is doing");
that was too strong. Investigation is a task spanning both: doing produces raw
material (an observation), and building it into knowledge is thinking's half — the
runtime delivers what was fetched, it does not interpret it.

**Mode: Reasoned**, raised directly in discussion and corrected in the same
discussion after an initial overstatement — friction and re-evaluation happening live,
on this document's own material, not just described by it.

**Grounds.** `03`'s own Observation/Finding split, applied rather than reinvented:
doing's product maps onto Observation, thinking's product onto Finding. The ETH
correction, already the pass's central worked example, grounds it concretely:
rereading the paper was doing's act, raw; recognizing the contradiction and building
the corrected claim from it was thinking's.

**Changed.** `02-reasoning-vs-runtime.md`: added §Feedback (Investigation as a task
spanning both sides); broadened Proposal and effect to include information-gathering
proposals, not only state-changing ones.

---

## F17 — Thinking acts on an instance, not the schema; its product is a knowledge-state transition

**Claim.** `03` defines the schema — what a claim, a mode, a graph can be; a walk never
touches the schema, only this project's actual graph as it currently stands, an
instance of it. A walk's real product is not one isolated conclusion but a
**knowledge-state transition**: the instance moving from what it held before to what it
holds after. `03`'s append-only rule is what a transition looks like once written
down — the prior state preserved, so the move itself stays inspectable.

**Mode: Reasoned**, proposed directly in discussion, formalized against both
documents' existing vocabulary.

**Grounds.** None external — an argument about how to characterize an activity already
defined, checked for consistency against `03`'s own append-only / Addendum material
(already grounded there, F10) rather than against anything new.

**Changed.** `02-reasoning-vs-runtime.md` §Thinking: added the instance/schema
distinction and "knowledge-state transition" as the name for a walk's product. `03`
§Friction and re-evaluation: cross-referenced at the OQ-7 example, tying the term back
to the case that motivated it.

---

## F18 — Doing produces knowledge-state transitions too, at the border; neither side is the intent by default

**Claim.** Thinking's transitions reorganize what the instance already holds; doing's
transitions are border effects — information crossing in, or a decision crossing out
into the world and being recorded as having happened. Framing doing as thinking's
subordinate service (fetch this so a walk can resume) is only one shape a task takes.
A task can just as easily be doing's, with thinking called in only to check something
before it happens. Which side drives is a property of the task's intent, not something
either document should assume.

**Mode: Reasoned**, a direct correction to F16's framing, which had implicitly modeled
thinking as the driver and doing as its service.

**Grounds.** `20-cognitive-architecture/01-work-intent-and-task-model.md`'s existing
Intent concept ("the underlying desired outcome or concern") is what actually decides
which side leads — checked directly, not assumed. This also directly answers the
standing complaint that opened this whole pass: that knowledge has to come from
feedback gathered by running the thing, not from reasoning about it — a claim that only
holds if doing is allowed to be the point, not merely thinking's errand.

**Changed.** `02-reasoning-vs-runtime.md` §Feedback: added the border-effects
distinction, the reverse direction of the bridge (doing calling thinking), and the
explicit no-hierarchy statement.

---

## Unchecked justifications

Findings above are grounded in something read or directly checked. The items below are
not — they are attempted arguments this pass relied on without independently verifying
them, and the next pass on `03` should treat them as open rather than settled.

- **"Nothing in a weighing comparison could have separated the ETH readings" (F9).**
  Verified: both readings trace to the same paper. Not verified: the stronger claim
  that source/reliability/mode being tied is *sufficient* to make a case friction in
  general, rather than a description that happens to fit this one case.

- **The DAG argument (F8) has never been exercised on real data.** It follows
  validly from `03`'s own Evidence definition, but no provenance store exists yet to
  confirm the graph actually behaves this way — no cycles, clean convergence and
  divergence — once real recording starts.

- **The "noticing the symmetry" reconstruction (F12, and the earlier reasoned-observation
  material) is retrospective.** I do not have the original reasoning session that
  produced that claim — only my own memory file's summary of it. Describing it as "the
  demonstration step connected X with Y" is my reconstruction of how it was likely
  formed, not a verified account.

- **Whether "noticing the symmetry" is actually still unchecked, or checked-but-not-yet-
  architected, is unresolved and this pass did not distinguish the two.** The project's
  restraint principle ("notice the symmetry, do not build for it") could mean "this is
  not yet known to be true" (an epistemic caution, matching how F12 used it) or "this is
  believed true but building on it now would be premature" (an architectural caution,
  a different claim entirely). `03` currently reads it as the former without checking
  which the project actually means.

  **Addendum (2026-09-10) — addressed, not resolved.** `03` no longer claims to know
  which reading is correct; the ambiguity is now held explicitly as a qualification /
  open contract rather than asserted as settled. Which reading is actually true is
  still unknown — that has not changed — but the document no longer overclaims it.

- **Thinking (F14) and the claim that it "needs no new machinery" are entirely
  untested.** There is no implemented provenance graph to walk, so nothing about fixed
  points, termination, or whether the walk stays cheap has been exercised — this is
  Reasoned mode only, one step removed from being an attempted argument about attempted
  arguments.

  **Addendum (2026-09-10) — this was wrong, not merely untested.** F16 found that
  Thinking's walk, as originally written, could not resolve a stall on its own;
  Feedback had to be added as new material connecting to doing. "No new machinery" held
  for the walk's internal mechanics, not for what happens once the walk runs out of what
  it already has.

- **Nearly every concept added in this pass — mode of acquisition beyond the initial
  hand-tagging trial, weighing claims, friction, demonstration step, thinking — is
  illustrated by the same single case: the ETH/OQ-7 correction.** That case is real and
  well-checked, but reusing one example to validate many different concepts shows they
  are mutually consistent with that case, not that any of them generalizes. A second,
  independent worked example is the most direct way to test that before this document
  is treated as settled.
