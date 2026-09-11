# Findings — the evidence-belief-and-provenance conceptual pass

**Date:** 2026-09-10, continuing 2026-09-11
**Serves:** `10-foundations/03-evidence-belief-and-provenance.md`, revised in place
throughout; `10-foundations/02-reasoning-vs-runtime.md`, from F15 onward, once Thinking
turned out to be misplaced in `03`; `10-foundations/01-constrained-intelligence-
thesis.md` and `10-foundations/05-ephemeral-conversation-curated-memory.md`, both from
F19, once the pass widened from the knowledge model itself to the other locations
knowledge lives in (external world, model weights, conversation) and what draws the
line between them. `70-THINKING/01-use-cases.md` also carries two direct edits (P3),
recorded here rather than there because they are this pass's, not the litreview's.
`10-foundations/04-context-as-governed-resource.md`, from F30, once the pass returned to
context after the knowledge-and-reasoning substrate was in place — first against `03`'s
graph alone, then, from F31's correction on 2026-09-11, against all four of `01`'s
locations of knowledge once a concrete scenario showed the graph-only framing too
narrow. From F37 the pass widened again, out of foundations and into the architecture
band itself, once the 2026-09-11 reorg left `20-arch-runtime.md` describing
responsibilities that had acquired owners and `22-arch-cognition/01`'s work model with
no actor holding it: `20-arch-runtime.md`, `22-arch-cognition/01`, and the new
`28-arch-work-record/01` carry those edits. This file is the justification record for all of it — the design-set counterpart to
`50-findings/`, produced by a design conversation and a hand-tagging trial against the
existing corpus rather than by a milestone experiment.

Each entry states a claim, the mode by which the claim itself was produced (not the
mode of whatever it is about — the two can differ, per the pass's own third finding),
what grounds it, and what it changed.

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

**Grounds.** `22-arch-cognition/01-work-intent-and-task-model.md`'s existing
Intent concept ("the underlying desired outcome or concern") is what actually decides
which side leads — checked directly, not assumed. This also directly answers the
standing complaint that opened this whole pass: that knowledge has to come from
feedback gathered by running the thing, not from reasoning about it — a claim that only
holds if doing is allowed to be the point, not merely thinking's errand.

**Changed.** `02-reasoning-vs-runtime.md` §Feedback: added the border-effects
distinction, the reverse direction of the bridge (doing calling thinking), and the
explicit no-hierarchy statement.

---

## F19 — The model's own weights are a fourth location for knowledge: a world model, distinct in kind from `03`'s substrate

**Claim.** Alongside the external world (`02`), the knowledge base (`03`), and
conversation (`05`), the model's own weights are a location where knowledge already
lives — a world model, compressed by training. This does not compete with or
duplicate `03`: the difference is structural, not a matter of degree. The model's
world model is general (not particular to this project), frozen (not current), and
carries no provenance (cannot say why it believes something or when that was last
checked). `01`'s existing "durable project knowledge" is durable precisely because the
model's own knowledge is not.

**Mode: Reasoned**, prompted directly in discussion by a four-locations framework
raised two turns earlier (external world / KB / model weights / conversation).

**Grounds.** None external — argued from `03`'s own already-established properties
(provenance, currency) applied by contrast, and from `01`'s pre-existing "durable
project knowledge" line, which the new material explains rather than duplicates.

**Changed.** `10-foundations/01-constrained-intelligence-thesis.md`: added §The
model's own world model, between Motivation and Working hypothesis.

**Unchecked.** This surfaces a real gap in Mode of acquisition (`03`): a claim stated
from trained-in knowledge, consulting no specific external source at the moment it is
made, fits none of Read, Reasoned, Tested, or Operated. Flagged, not fixed.

---

## F20 — Entropy reduction promoted from `70-THINKING/01-use-cases.md` P3 into `02`, in part

**Claim.** "Entropy reduction is the product" (P3) was fully evidenced (M6: 0
regressions vs 7, 0 crashes vs 4, 5/5 correct declines) but sitting unpromoted. Its
core claim belongs in `02`'s Proposal and effect: at the system level entropy
reduction is the product; at the level of a single proposed effect it is the desired
side effect of executing the task's actual intent well, not a competing goal — a bug
fix's job is to fix the bug. This is why the runtime's four checks are not bureaucratic
caution: an effect that needed undoing spread entropy regardless of whether it
succeeded at its stated task.

**Mode: Operated.** Found by reading P3's cited M6 numbers and `07`'s existing,
narrower citation of the same commitment directly, not by reasoning abstractly about
what "the product" should mean.

**Grounds.** `70-THINKING/01-use-cases.md` P3; `10-foundations/07-the-integrated-
system-and-its-operator.md` ("Reduced entropy... is valuable precisely because it is
what an operator experiences as help").

**Changed.** `02`: added the entropy-reduction paragraph to Proposal and effect.
`01-use-cases.md` P3: added a promotion note distinguishing the promoted core claim
from the still-gated motto revision (which wants the capability sweep P3 itself
names, and was left untouched in `01`).

---

## F21 — The entropy material in `02` needed a floor/ceiling correction

**Claim.** Framing entropy-bounding (via reversibility) as protection against a
"floor" beneath a separately-raised "ceiling" contradicts the project's own locked
position: there is no floor, only the ceiling, read from below. An assembly that
regresses on one task in three does not have a high ceiling guarded by a weak floor —
it has a lower ceiling than its peak output suggests, because the ceiling is what it
reliably delivers.

**Mode: Reasoned**, prompted directly by the user's reminder, checked against the
root README's own wording before being applied.

**Grounds.** Root README ("There is no floor — only the ceiling, read from below");
[[praxis-run-the-knowledge-model]] memory, same principle; P3's own cited numbers,
re-read under this framing rather than a new check.

**Changed.** `02`: added the floor/ceiling sentence to the entropy paragraph in
Proposal and effect.

---

## F22 — Reversibility cannot be required of every effect; irreversible-effect risk evaluation is reasoning-based, not invariant-layer material

**Claim.** Some requested changes are irreversible by nature — that is what was asked
for, not an accident of execution — and refusing them on reversibility grounds alone
would refuse the work itself. What such an effect needs instead is a real, contextual
risk evaluation. That evaluation is explicitly not the invariant layer's to make: the
invariant layer holds effects that may never occur regardless of what any loop
concludes, and a legitimate irreversible effect is, by definition, not one of those.
It belongs to thinking instead, weighed the same way any other claim is.

**Mode: Reasoned**, raised directly by the user; the invariant-layer boundary was read
directly from `06` before being asserted, not assumed.

**Grounds.** `10-foundations/06-the-invariant-layer.md`, read in full for this check:
"Hard constraints — effects that may never occur regardless of what any loop
concludes."

**Changed.** `02`: added the risk-evaluation paragraph to Proposal and effect,
immediately after the four-checks sentence it qualifies.

---

## F23 — The floor-language critique of P3's own motto phrasing was itself an overcorrection, and its fix was recorded by collapsing, not appending

**Claim.** "Bound what the model can make worse" does not posit a floor separate from
the ceiling — it is the ceiling, read from below, which the principle licenses rather
than forbids; P3's own numbers show the mechanism, not just the wording, is doing the
same work either way. An earlier annotation on P3 claiming this phrase "needs
rewording" was itself the error. Because that annotation never left this conversation —
nothing else cited or relied on it before the next exchange checked it — recording the
fix as a dated, appended "Correction" (as first attempted) applied `03`'s Qualification
convention past where its own justification reaches. It was collapsed instead: the
wrong annotation and its append-style correction were both replaced by the single
settled paragraph now in `01-use-cases.md`.

**Mode: Reasoned.** Two corrections in sequence, both raised directly by the user: the
substantive one (the phrase was fine), then a separate, sharper one about how to record
having been wrong (collapse, don't append) — which is also this finding's own grounds
for F24, below.

**Grounds.** Root README's "read from below" line, re-examined; `03`'s own Friction
logic (append-only earns its keep for claims that got *used* elsewhere) applied to a
case that never met that condition.

**Changed.** `01-use-cases.md` P3: the floor-language critique and its appended
"Correction (2026-09-10)" paragraph were both removed; replaced with one clean,
settled paragraph carrying no trace of either.

---

## F24 — Collapsing named and placed in `05`; resolves the `05`/`03` promotion-boundary weakness

**Claim.** An attempted argument superseded before it is ever promoted needs no
append-only trail: it **collapses** to the settled state, because nothing outside the
still-active reasoning episode could have relied on the superseded step. This is
distinct from Qualification/open contract (`03`), which applies once a claim has been
promoted and potentially used elsewhere. It resolves the boundary an earlier pass
flagged as a real weakness: `03` lists attempted arguments as something Provenance
tracks without saying how much of a walk's internal churn actually reaches that graph.
F23, immediately above, is itself the first applied instance.

**Mode: Reasoned**, proposed directly by the user, applied reflexively to F23's own
recording before being written up here — the concept was named by first doing the
thing it names.

**Grounds.** `05`'s own pre-existing text, read directly: "revise its conclusion"
(Ephemeral interaction) and its Open question ("contradiction... remain intentionally
unresolved") both already anticipated this, unnamed.

**Changed.** `05`: added §Collapsing, between Ephemeral interaction and Curated
memory; narrowed Open question (contradiction before promotion vs. after). `03`:
added a cross-reference in Provenance stating that not every attempted argument a
walk forms reaches the graph.

---

## F25 — Curated memory rebuilt to match Collapsing's rigor

**Claim.** `05`'s Curated memory section, unlike its direct complement Collapsing
(F24), still used pre-session vocabulary and gave no real criterion for what is worth
persisting. Rebuilt to state precisely: curated memory is what survives Collapsing — a
claim checked, held as a demonstration step, and judged worth a souvenir (`03`) rather
than left to disappear with the episode that produced it. Its forward-looking question
("will this matter to a comparison that has not happened yet") is distinct from
Pertinence (`03`, Weighing claims), which only asks whether a claim matters to the
comparison in front of it now — a question Weighing claims cannot run before the next
claim arrives.

**Mode: Reasoned**, prompted directly by the user's observation ("the curated memory
section feels weak"), diagnosed by comparing it against how much more developed
Collapsing already was.

**Grounds.** `03`'s own existing definitions (Pertinence, souvenir, demonstration
step) applied by contrast; `05`'s own pre-existing "revise its conclusion" language,
already the basis for Collapsing.

**Changed.** `05`: Curated memory section rewritten.

---

## F26 — "Confidence" dropped for "reliability"

**Claim.** Keeping the word "confidence" in the preservation list, even while
explaining that it maps to Reliability, perpetuates exactly the translation gap that
produced the apparent friction it came from. Using "reliability" directly removes the
gap instead of documenting it.

**Mode: Reasoned**, direct instruction from the user.

**Grounds.** The gallicism clarification given earlier in this same pass: "confidence"
in `05`'s original text was intended as trustworthiness/reliability, a French usage,
not a distinct scalar concept.

**Changed.** `05`: "confidence" replaced with "reliability" in the preservation list.

---

## F27 — "Evidence" dropped from the preservation list as redundant with Provenance

**Claim.** Listing "evidence" alongside "provenance" as two peer items to preserve is
a category error: Evidence is one of the claim types Provenance already connects, and
Evidence's own definition in `03` requires it to retain provenance to count as
evidence at all. What might have motivated separating them — raw content versus
connective structure — is already `03`'s raw/souvenir distinction, not a separate
axis.

**Mode: Reasoned**, direct correction from the user, confirmed against `03`'s own
Evidence and Provenance definitions before being applied.

**Grounds.** `03`'s pre-existing Evidence definition ("Evidence should retain enough
provenance...") and Provenance's connects-list, which already includes findings and
other claim types as node kinds.

**Changed.** `05`: "evidence" dropped from the preservation list; an explanatory
clause was added and then removed again per a direct instruction to keep it tight —
net change is the reduced three-item list (scope, provenance, reliability).

---

## F28 — Scope named precisely, then relocated from `05` to `03` as a general claim-property

**Claim.** Scope is the domain a claim was actually born into — the host, the model
family, the project's state at that moment — and unlike everything else in `03`, it
cannot be reconstructed later from provenance, however capable the reader, because the
birth-context was never fully representable to begin with, only assessable near the
time it existed. This is categorically different from souvenir's premise (full
re-derivability from intact roots) and from Weighing claims' three dimensions (each
fully assessable in principle). As a general property of claims rather than a
curation-specific detail, it belongs in `03`; `05` keeps only the cost-management
question it actually owns — how much assessment effort an inherently incomplete
judgment is worth.

**Mode: Reasoned** throughout — first characterized directly by the user in
discussion, then relocated on the user's explicit direction ("rephrase in a
foundational direction").

**Grounds.** None external — an argued epistemological distinction, checked for
consistency against `03`'s existing souvenir and Weighing-claims premises, both of
which explicitly assume a reconstructability Scope explicitly denies.

**Changed.** `03`: added §Scope, between Weighing claims and Friction and
re-evaluation. `05`: Curated memory's scope material rewritten to reference `03`'s
definition and focus only on cost management; Open question updated to reflect scope
now having a home.

---

## F29 — Expected consequence rewritten: Collapsing's real payoff is cheap scope-assessment; independent reassessment is Convergence/Friction by name

**Claim.** `05`'s original Expected consequence ("fresh instances begin from curated
knowledge... supports constrained context and independent reassessment") had become
true by construction once Collapsing and Curated memory were precisely defined, and
stopped adding information. The consequence actually worth stating: Collapsing keeps
the expensive, necessarily-imperfect work of scope-assessment rare, because most of a
reasoning episode's churn never reaches curated memory at all. And "independent
reassessment," when a fresh instance actually re-derives rather than trusts what it
inherits, is precisely Convergence (agreement, corroborating) or Friction
(disagreement, forcing re-evaluation) — not a separate, vaguer benefit.

**Mode: Reasoned**, prompted by the user flagging the section as obsolete and asking
whether to drop or replace it.

**Grounds.** `03`'s own Scope, Convergence, and Friction definitions, applied to
explain what Collapsing and Curated memory actually buy, not newly derived for this
finding.

**Changed.** `05`: Expected consequence section fully rewritten.

---

## F30 — "Redundancy, not volume" was in tension with the granularity hypothesis; redundancy and convergence are different axes, not opposites

**Claim.** `04`'s existing claim that "what makes context costly is redundancy, not volume" stated a real, evidenced finding (findings entry 9, §3) as if it were the whole story. It is not: the granularity hypothesis (`22-arch-cognition/08-decomposition.md`) predicts a volume-driven ceiling independent of redundancy, and a context can be entirely non-redundant and still overload a small assembly. The original phrasing also invited a second, separate confusion — treating redundancy as the absence of Convergence (`03`) — when the two are unrelated axes: Convergence is independent corroboration between claims, strengthening reliability; redundancy is duplicated coverage inside one assembled window, a pure budget cost.

**Mode: Reasoned.** Both corrections raised directly by the user in discussion: the volume tension first ("That is in direct tension with the granularity hypothesis"), the convergence distinction second, correcting my own "redundancy is the absence of convergence" claim mid-discussion.

**Grounds.** `50-findings/09-field-evidence-2026-09.md` §3 (the redundancy evidence itself, re-read to confirm it supports only the duplication claim, not a volume claim); `22-arch-cognition/08-decomposition.md` (the granularity hypothesis, read in full for this check); `03`'s existing Convergence definition (Friction and re-evaluation), read directly rather than assumed.

**Changed.** `04`: the old §"What makes context costly is redundancy, not volume" was removed; its evidenced claim survives, narrowed and correctly scoped, inside the new §Failure modes' Redundancy entry, with an explicit paragraph distinguishing it from both Convergence and Overload.

---

## F31 — `04` needed an actual shape for "context": not a projection of `03`'s graph alone, but the set of artifacts produced by crossings into conversation, judged on two independent axes

**Claim.** Every other foundations document this pass touched ended up with a structural account of its own subject — `03` has claims, modes, weighing dimensions; `02` has Thinking and Feedback as procedures. `04` had only principles (context is relational, redundancy is costly) and no account of what a context actually *is*. A first draft defined it as a bounded projection of `03`'s provenance graph alone. Working the shape against a concrete scenario (a knowledge graph, a workspace of files, a task, live artifacts, several processors) showed that definition too narrow: the naive default (`10-technical/07`) draws its bundle from raw repository files, never touching `03`'s graph at all, and a workspace full of unread papers is not itself context by merely existing. The corrected shape: nothing is context until it **crosses** into conversation, the fourth of `01`'s four locations of knowledge — a tool call reaching the external world, a retrieval reaching `03`'s knowledge base, a generation drawing on the model's weights are the three ways a crossing happens, and what a crossing produces, never the thing reached, is an **artifact**. A context, at any point, is the set of artifacts currently live. Not every artifact is already a `03` claim — a tool call's output is raw until Thinking turns it into one — so `03`'s own apparatus (mode of acquisition, weighing, convergence) applies once an artifact becomes a claim, not to artifacts as such. The two independent axes survive the correction unchanged: **coverage** (does the selection contain what the objective needs), a property of the selection, and **integration** (can the assembly hold what coverage included), a property of the assembly.

**Mode: Reasoned**, in two stages. The axes and the initial projection-of-`03` framing were prompted by the user's own framing ("03 tells you the shape of the knowledge base... here we need the shape of the context, the context model"). The correction was prompted by the user proposing a concrete scenario to stress-test it ("we have a knowledge graph, we have a workspace with a folder hierarchy with a number of papers, we have a task, we have a set of live artifacts, we have a set of processors") and then supplying the actual mechanism directly ("The filesystem is the outside world, its not context. The pieces of filesystem read will be gathered by the context manager as the output of a tool call, an artifact, and the models response, another one. It also tracks the discussion") — the connection to `01`'s pre-existing four locations of knowledge was then drawn by this pass and confirmed by the user before being written.

**Grounds.** `10-technical/07-naive-context-assembly.md`'s naive algorithm, re-read directly and found to draw only from repository files, not `03`'s graph — the concrete fact that broke the first draft; `10-foundations/01-constrained-intelligence-thesis.md`'s pre-existing four-locations material (F19, this same pass); `02-reasoning-vs-runtime.md`'s Feedback (doing produces raw Observations, thinking turns them into knowledge) as the basis for the raw-artifact/claim distinction.

**Changed.** `04`: §The shape of a context rewritten in place (collapsed, not appended — nothing outside this session's drafting had relied on the graph-only version); "claim" language in Failure modes, What is live has to be tracked not inferred, What each failure mode requires, The objective itself is not a given, and Forcing the choice was correspondingly loosened to "artifact" wherever those sections did not specifically mean a `03` claim.

---

## F32 — Context failure has four modes, not one: Insufficiency, Redundancy, Uselessness, Overload — split by which axis fails and evidenced separately

**Claim.** The two axes in F31 generate four distinct failure modes rather than one undifferentiated "too much / too little." Insufficiency and Redundancy are opposite-direction coverage failures (missing versus duplicated), both evidenced in the existing corpus. Uselessness is a third, previously unnamed coverage failure — present, non-duplicating, but irrelevant — predicted to be harmless alone and harmful only by contributing to Overload, with nothing in the corpus testing it in isolation. Overload is the only integration failure: content-quality-agnostic aggregate volume crossing the assembly's ceiling, where the granularity hypothesis lives, itself only retrodictively supported and not yet subjected to its own named falsifier (E2).

**Mode: Reasoned.** Constructed across several rounds of direct correction from the user: an initial three-way split was corrected to separate Uselessness from Overload ("that one is not harmful, until it becomes overload"), and Overload itself was generalized from "individually relevant, non-redundant material that still exceeds the ceiling" (my narrower framing) to content-quality-agnostic "context blur, in general" (the user's correction).

**Grounds.** `50-findings/09-field-evidence-2026-09.md` §3 (Redundancy); the Milestone 4 finding already in `04`'s own Expected behavior section (Insufficiency); `22-arch-cognition/08-decomposition.md`, including its own "Status of this account" section ("a lens, not a theory") and `08-next-experiments.md`'s E2 (Overload's evidence status). Uselessness has no grounding beyond the argument itself — flagged as predicted, not evidenced, in the text.

**Changed.** `04`: added §Failure modes, replacing the old redundancy-only section.

---

## F33 — Each failure mode's document-level obligation is what to track and what decision it feeds, not how to resolve it

**Claim.** An initial attempt to answer what `04` owes for Overload reached directly for a resolution technique — `03`'s checked/unchecked (souvenir) distinction, condense versus split — before establishing what actually needs tracking and deciding. The user flagged this as off-topic: out of scope for what a foundations document owes, which is naming what must be addressed, not proposing how. The corrected shape states, per mode, what must be tracked for the mode to be detectable and what decision the tracking feeds, leaving execution to architecture — the same deferral `03`'s Weighing claims already makes for pertinence. Working through this also surfaced gaps worth naming precisely: Insufficiency has no trackable representation of an objective's information requirements yet; Redundancy has to be defined at the level of coverage, not text, to rule out a cheap wrong implementation; Uselessness's real decision is whether detecting it is worth the judgment cost at all, not simply whether to filter it; Overload already has a naive, existing answer (`10-technical/07`'s flat token budget) whose limitation this document's own relational claim already names.

**Mode: Reasoned.** The souvenir-mechanism draft was corrected directly by the user mid-edit ("that is off-topic... what do we need to track and what kind of decisions need to be made"); the per-mode content was then built in discussion before being written, confirmed as "a good start" before finishing.

**Grounds.** `10-technical/07-naive-context-assembly.md` (the existing flat-budget behavior, read directly, not assumed); `22-arch-cognition/01-work-intent-and-task-model.md`'s Intent concept (checked as the nearest, not-yet-fitting candidate for Insufficiency's tracking need); `50-findings/09` §3 (re-confirmed as a material-duplication result, grounding the coverage-not-text framing for Redundancy).

**Changed.** `04`: the drafted §Responding to overload (souvenir/condense-split) was replaced before being carried forward as settled — collapsed, not appended, since nothing outside this session's own drafting had relied on it — with §What each failure mode requires.

---

## F34 — Live context needs an explicit, trackable record; none of the four failure modes are detectable without one

**Claim.** Every track/decide pair in F33 presupposes the system can consult what is currently live in context while assembly is happening — Redundancy's overlap check, Insufficiency's missing-coverage check, Overload's running total, and Uselessness's per-item pertinence judgment all compare a candidate or a total against the live set, not against `03`'s full graph. `04`'s own TL;DR already commits to context "measured as a resource" without ever stating what measuring it actually requires: an explicit, first-class, inspectable record of what is live, distinct from what merely exists in `03`'s graph but is not currently loaded.

**Mode: Reasoned.** Raised directly by the user as "one central aspect" of the whole discussion, not derived from a file; grounded here against `70-THINKING/ideas.md` I12, which had already sketched close to this bookkeeping account for a different reason (placing "context manager" in the cognitive architecture) earlier in the same pass.

**Grounds.** `70-THINKING/ideas.md` I12, read directly — its bookkeeping list ("tracking what the model is currently fed... live versus archived") already names most of what this finding requires, though I12 was written to answer a different question (where a context manager sits architecturally) and is cited here as a candidate account, not adopted.

**Changed.** `04`: added §What is live has to be tracked, not inferred, between Failure modes and What each failure mode requires; Open question gained two new items (an objective's trackable information-requirement shape; ownership of the live-context record) and one item reworded (Overload's proxy/threshold, no longer framed as a condense/split question).

---

## F35 — The objective itself is not a given; and context assembly cannot make that judgment, only feed it

**Claim.** `04`'s shape, failure modes, and track/decide obligations all presuppose the objective is genuine, unique, and actually needs new work — an assumption real request traffic (the GitLab-issues case) breaks routinely (duplicate tickets, user error, under-specified reports). `22-arch-cognition/01-work-intent-and-task-model.md` already names the needed system behavior — discovering a request "already has been satisfied" or resting on "a false assumption" — but only as a capability, not as something fed. A first attempt to fold this into `04` treated "checking whether the objective is already answered" as itself a context-assembly step, deciding the question. That was corrected directly: context assembly cannot make that judgment — it is a processor's output, reached by Thinking (`02`) — context assembly's job stops at surfacing candidate matches from `03`'s provenance graph for the processor to judge. A false-premise or under-specified objective has no equivalent candidate to surface at all, since the objective's own claim has not yet been weighed; `04` should name that boundary rather than silently assume it away.

**Mode: Reasoned.** Prompted directly by the user ("think of the gitlab issues experiments"), grounded against `22-arch-cognition/01`'s existing text, read directly rather than assumed; then corrected again directly by the user when the first draft blurred context assembly's role into the judgment itself ("The context cannot provide for that judgment. That is a processor's output. It will need the proper context to operate though.").

**Grounds.** `22-arch-cognition/01-work-intent-and-task-model.md` (Expected behavior, read in full for this check); `02-reasoning-vs-runtime.md`'s Thinking and `03`'s Convergence, applied to distinguish "surfacing a candidate" (context assembly's role) from "judging whether it resolves the objective" (a processor's role) — the same split already drawn for Insufficiency's request-more-context affordance.

**Changed.** `04`: added §The objective itself is not a given, immediately after What each failure mode requires (the section that followed it, first drafted and then retracted, is F36's); Open question gained a new item on the objective-validity boundary's missing owner.

---

## F36 — Context selection can be a forced choice over an indexed menu; self-judgment evidence does not apply to it and was retracted

**Claim.** A first attempt at naming who performs context selection reached for this project's own self-judgment evidence (Entry 7's judge-lab, ADaPT's self-assessment inflation) and treated selection as a judgment-reliability question. The user retracted this directly: judging correctness or sufficiency and selecting from a presented set are different operations, and evidence against the first does not transfer to the second. The pattern actually being pointed at — described by the user from a GitLab-issues study, not read directly in this pass — is a forced choice: the harness presents an indexed menu of candidate context and requires a selection at a defined point, rather than leaving a request optional (the M4 finding's own failure mode) or asking the model to self-assess whether it has enough. This needs two things `04` had not named: an index of what is available but not yet live, distinct from the live record itself, and arbitration over which candidates are offered and which choices are honoured.

**Mode: Reasoned**, and **second-hand** (`03`) for the study itself: the mechanism (index, arbitration, forcing) is taken on the user's direct account, not verified against a primary source by this pass.

**Grounds.** `04`'s own pre-existing M4 finding (Expected behavior: "being able to ask is not enough; the behaviour has to be prompted or required") as the gap this mechanism concretely answers; `10-technical/07-naive-context-assembly.md`'s existing substring-match step, re-read as an unnamed, crude precedent for arbitration.

**Changed.** `04`: the retracted §The model is not a safe default judge of its own failure modes was collapsed — not appended over, since nothing outside this session's own drafting had relied on it — and replaced with §Forcing the choice: an index, and arbitration over it, including a marked prediction (forcing raises selection rate over the M4 optional-affordance baseline) with a named falsifier — a re-run of the M4 setup with a forced-menu arm added; Open question's live-context-record item reworded to drop the self-judgment framing and ask about arbitration instead, and gained a new item naming the prediction as untested.

---

## F37 — The context bundle is stale: context is not bound at instantiation, it is composed every turn, so nothing asks for it

**Claim.** The 2026-09-11 reorg moved concerns out of the old bundled folder but did not revise the runtime document that now heads the band. Its Expected responsibilities still claimed capability boundaries, observation recording, and state persistence as the runtime's own, when `24`, `26`, and `21`/`23`/`28` had become their owners — the runtime is where those become real, which is not the same as deciding them. Separately, every document in the band named its own edges and none drew the order.

A first attempt at drawing that order asked **who requests a processor's context bundle** and answered "the runtime," on the grounds that it was the only assignment that stayed uniform when the instance being invoked is the orchestrator. The user rejected the question rather than the answer: the bundle itself is stale. It survives from `10-technical/07-naive-context-assembly.md`, which is one-shot by its own account, and it contradicts the register/track/recall split F34 and the `04` pass had already established — recall decides what is fed to the model **on a given turn**, over a pool that grows with every crossing. A bundle is a package assembled once and held; what actually exists is a composition made at each feeding and discarded, with the state living in the pool rather than in anything passed between steps.

So the question has no answer because it has no referent. Nothing requests a composition: this actor sits in the path everything to and from the model takes, so it composes because a turn is happening. It is traversed, not called. This also disposes of the orchestrator problem more cleanly than the rejected answer did — the orchestrator needs nobody to fetch on its behalf, because there is no fetch.

Dropping the bundle surfaces a question it had been concealing: **what is in a pool when an instance starts**. A bundle made this look settled, since a bundle is by definition what an instance begins with.

A first attempt placed that question in `22-arch-cognition/08`, calling it the fork/join-versus-continuation question in different clothes — fork/join implying a near-empty pool with a later reconciliation, continuation implying one seeded by the preceding step. The user rejected the link and it does not survive a counterexample in either direction: fork/join runs perfectly well with richly seeded branches, since what fork/join constrains is whether siblings see *each other's* crossings rather than what any one of them starts with, and continuation runs perfectly well handing forward almost nothing, since `08`'s own phrasing is "what the next step needs," which can be very little. All four combinations are coherent. The two questions are orthogonal and were linked only because both were unresolved.

Stated as a context-management question it gets sharper rather than vaguer. Register records what a crossing returned and recall presents what a pool already holds, so neither operation can put anything in a pool before the first crossing: a pool is empty at turn zero by construction. Inheritance is therefore either a third primitive — already-registered artifacts moving or being referenced across pools with no crossing — or no new mechanism at all, with the preceding step writing a handoff into something durable and the next instance reading it like any other read. The second is cheaper, has a home in `28-arch-work-record` as an attachment on a work item, and is preferred as the thing to investigate first rather than as an adopted position.

**Mode: Reasoned**, with the correction itself **Operated** in the weak sense that the user identified the staleness directly rather than it being derived here. Nothing was tested or read against an outside source.

**Grounds.** `23-arch-context-management/01`'s own Recall responsibility, which already said "on a given turn" and "over a fixed pool" — the bundle contradicted a distinction this band had already drawn, so this is an internal inconsistency found, not new material; `10-technical/07-naive-context-assembly.md`'s self-described one-shot shape as the bundle's actual provenance; `10-technical/01-effect-vocabulary.md`'s What is not an effect and `10-foundations/02`'s Proposal and effect, which both exclude plain reads from the gate by name.

**Changed.** `20-arch-runtime.md`: two dead links in the architecture map repaired (they pointed at the stub READMEs deleted when `21` and `23` were written); Expected responsibilities rewritten to separate what the runtime decides from what it realizes on a named owner's behalf; §The path an invocation takes was **collapsed** — written and then rewritten within this pass, with nothing outside it having relied on the bundle version — and replaced by §Instantiation, and then a loop, stating that only role, objective, capability set and a pool identity bind at instantiation, and that compose/act/register repeats per turn; new §What instantiation does not settle, naming the pool-seeding question and stating explicitly that it is not a decomposition question. `22-arch-cognition/08` briefly gained a paragraph and an open-question clause tying recombination to pool seeding; both were **reverted** in full once the link was rejected, leaving that document as it stood. `23-arch-context-management/01`: the service restated as what the model sees on a given turn rather than a bundle per invocation, with an explicit note that nothing asks for it; the runtime-as-requester claim removed; `22-arch-cognition` recast from "consumer of bundles" to what this actor composes for; the claim that `24-arch-permission-layer` "gates the tool call" corrected, since it had flattened two different paths — a read is capability-gated only, an effect passes capability gating and then the invariant gate. `22-arch-cognition/03`'s Context constraint rewritten on the same grounds: not consumer-to-service either, since a consumer calls and the orchestrator never does.

---

## F38 — Work-record mutation had a schema, a policy, and exercised runs, but no actor in the band owned the record it mutates

**Claim.** `10-technical/01-effect-vocabulary.md` type 4 makes changing the durable representation of work a first-class gated effect, `10-technical/03-capability-authority-model.md` writes policy for it, and the M3 runs routed real type-4 mutations through the gate — so something was already persisting work items in practice. No actor in `21`–`27` held it. `22-arch-cognition/01-work-intent-and-task-model.md` defines intent, work items, and work units without storing any of them, and `21-arch-knowledge-model` holds `03`'s claims, which a work item is not: it is what claims attach to. Folding the record into `21` was rejected on write discipline rather than on subject matter — a claim there is append-only and superseded, so its current truth is the end of a chain, whereas a work item's current state must be readable without walking anything, since the orchestrator interprets current work on every loop step. A separate actor holds both a mutable current view and an immutable transition log; collapsing the two into `21` would force one of those to give.

**Mode: Reasoned**, with one operated input: the M3 runs are real exercised evidence that type 4 carves cleanly, not an argument.

**Grounds.** `50-PROGRESS/archives/M3-invariant-floor.md` item 9 — three of nine effect types exercised across the M4 runs, work-record mutation among them, all carving cleanly; `10-technical/01` type 4's own text, which covers attaching a finding, proposal, or decision to a work item and classes a processor's recorded conclusion as a type-4 mutation rather than a memory write; the same document's effect-sequence requirement that realized effects be reconstructable **per intent lineage**, a chain nothing in the band supplied; `22-arch-cognition/01`'s own statement that a work item is refined, challenged, split, merged, deferred, or abandoned, which is what makes it mutable by design.

**Changed.** New `28-arch-work-record/01-work-record.md`, stating the actor, its service — intent lineage, current work state, transition history, attached-claim references — and a filesystem-naive shape, with work units left open exactly as `22-arch-cognition/01` left them. `22-arch-cognition/01` gained §Where this model is held and two pointers, keeping the vocabulary there and the storage in `28`. `21-arch-knowledge-model/01` gained a one-way reference relationship: `28` resolves claims against `21`, and `21` knows nothing about work items. `26-arch-observability/01` extended its separate-store argument to three actors rather than two. `20-arch-runtime.md`'s map, `00-design/README.md`, `manifest.json`, `10-technical/01`'s traces and relationships, and `40-roadmap/00-backlog.md`'s reorg note all updated.

---

## F39 — `27`'s "context policy" was pre-split vocabulary for what is now the recall policy, and that loop is the consumer recall's boundedness was designed for

**Claim.** `27-arch-adaptation-and-evolution` named "context policy" in four places as something system-level feedback proposes changes to, a generation carries, and a bootstrapped instance inherits — with no owner and no definition, since it was written before any actor held context. It is `23-arch-context-management`'s recall policy. Naming it that does more than fix vocabulary: it supplies the consumer that `23`'s central argument had been missing. `23` justifies keeping recall separate from registration on the grounds that a policy choosing a subset of a fixed pool makes two policies directly comparable, holding the pool constant. That property is worth having only if something tunes policies, and `27` is that something. The two documents were each carrying half of one argument.

**Mode: Reasoned**, from reading the two documents against each other. No run has tuned a policy, and the comparability claim remains a design property rather than a demonstrated one.

**Grounds.** `27-arch-adaptation-and-evolution/02`'s Object of adaptation, `06`'s generation contents, and `07`'s inheritance list, all naming "context policy" without an owner; `23-arch-context-management/01`'s Recall responsibility, which states the comparability property without naming who would use it.

**Changed.** `27/02`: the term replaced throughout, plus a new paragraph singling the recall policy out and stating why its boundedness matters to this loop — including that `23` leaves the policy's content unspecified deliberately rather than by omission. `27/06` and `27/07`: the term replaced and the owner cited. `23/01`: a reciprocal interaction with `27`, naming this as the loop recall was shaped to serve.

---

## F40 — The read exclusion answered the wrong kind of question: whether to gate reads is a rule, whether the framework can is structural

**Claim.** `10-foundations/02`, Proposal and effect, excluded reads from the invariant gate's reach "because gating every read would recreate exactly the rigid workflow engine this document exists to prevent." The user rejected the argument on a sharper ground than the one this pass had reached for. A first pass here argued the boundary sat in the wrong place — that a read changes governed state under `04` and so meets the effect definition. The user's objection is that the passage settles the wrong *category* of question: being able to gate every read is a rule to adopt or decline within a framework that permits it, not a high-level design decision to foreclose. The argument given is about what gating costs, which is a policy consideration, and it was used to remove a capability.

The asymmetry is what makes it load-bearing. A policy default is reversible; a vocabulary exclusion is not. `10-technical/01-effect-vocabulary.md` states that adding an effect type "requires a design-set decision" and "MUST NOT happen as an implementation convenience" — so under the excluding vocabulary, "hold a rule about this read" is a change to the system's operational surface rather than to its configuration. A permissive default ("reads pass unless a rule names them") buys the same economy without that cost.

Two further consequences, each a thing the exclusion makes inexpressible rather than merely unused. `10-foundations/06` holds resource ceilings among invariant-layer content, context is a bounded resource whose ceiling is `04`'s Overload mode, and a read crossing that ceiling is a resource-ceiling matter the gate cannot see. And `25-arch-invariant-layer`'s Composition risk exists to catch sequences of individually-permitted actions; the canonical such sequence is accumulated reads followed by one permitted carrying effect, and a gate evaluating only typed effects sees the carrying step with none of what filled it. `25`'s own argument for binding to effects — that they are "a bounded set the runtime already represents in order to execute anything at all" — applies to reads equally well and never excluded them; the exclusion was a separate, weaker claim sitting beside it.

**Mode: Reasoned**, and the correction is **Operated** in the same weak sense as F37: the user identified the category error directly rather than it being derived here. Nothing was tested.

**Grounds.** `10-foundations/02`'s own line 39 as the sole site of the argument — `10-technical/04-enforcement-gate.md` never mentions reads at all, having inherited the exclusion silently, which is itself evidence that it propagated as an assumption rather than a decision; `10-technical/01-effect-vocabulary.md`'s statement that vocabulary changes are design-set decisions, which supplies the reversibility asymmetry; `25-arch-invariant-layer/01`'s effect-binding argument and Composition risk section, neither of which needs the exclusion.

**Changed.** `10-foundations/02`: the claim **qualified and dated rather than rewritten**, per `03`'s own rule that a promoted claim other documents relied on is appended to, not silently revised — the leg withdrawn here is that the gate may therefore not evaluate a read. This entry also preserved a second leg, that a workspace read changes nothing outside the system; **F41 withdraws that one too**, so nothing of the original claim's reasoning stands. Its Feedback section's "reaches outside it or changes state" narrowed to "changes the world beyond it," since a read changes the system's own context record and that does not make it an effect. Open question gained the permissive-default content and granularity item. `25-arch-invariant-layer/01`: new §What the gate may see is wider than what it evaluates, stating the input domain as runtime-mediated operations with typed effects as the outside-world-changing subset; Composition risk gained the reads-in-the-sequence consequence. `20-arch-runtime.md`: the read path restated as short by default rather than by construction, and its open question replaced — the capability question is settled, the default's content and whether a read eventually earns its own type are not.

---

## F41 — A read does change the outside world; what separates it from an effect is footprint, a gradient, not kind

**Claim.** F40 withdrew one leg of `10-foundations/02`'s read exclusion and explicitly preserved the other: that a workspace read does not change the world outside the system, and is therefore not a typed effect. The user rejected that leg too, and it does not hold. A read leaves an access record and a modified access time. A query makes its store do work — warming or evicting caches, moving query statistics, holding a connection, competing for capacity. Reading a metered source spends quota that does not come back. Some reads are state transitions outright: dequeuing a queue item, marking a message read, firing a watcher, materializing a lazily-evaluated view. "Changes nothing outside the system" holds only if the world means file contents.

So the read/effect boundary is not a distinction in kind at all. Every runtime-mediated operation changes the world; they differ in **footprint**, which is a gradient. Intent does not rescue the boundary — a write's purpose is its change while a read's change is incidental, but that is a fact about the proposer, and a gate keyed to what a proposer meant is persuadable by construction (`25-arch-invariant-layer/01`). What the typed-effect vocabulary actually enumerates is the set of operations whose footprint this project has judged worth naming and tracking, not the set that has one. Weaker than the original claim, true, and it preserves everything the vocabulary was useful for: still bounded, still closed, still checkable without reasoning. What it gives up is membership following from the nature of the operation.

One consequence worth recording on its own: the original cost argument points the other way. "Gating every read is expensive" was offered as grounds that reads need not be gated. Load is itself a footprint in the outside world, so the expense is evidence the operation is consequential rather than inert. The premise supported the opposite of its conclusion.

**Mode: Reasoned**, with the correction **Operated** in the same weak sense as F37 and F40 — the user supplied the counterexamples (trace, database calls, load, state transition) directly.

**Grounds.** `26-arch-observability/01`'s Privacy and cost, which already argues for a separate store partly so that "every reconstruction query competes with `21-arch-knowledge-model`'s own query load" — the project was already treating a read as a real cost that degrades something while a foundation claimed reads change nothing, so this is an internal contradiction already present in the corpus rather than new material; `25-arch-invariant-layer/01`'s persuadability argument, which rules out intent as the rescuing criterion; `10-technical/01-effect-vocabulary.md`'s own open contract on who assigns a reversibility class, which already treats footprint-like properties as unresolved rather than type-intrinsic.

**Changed.** `10-foundations/02`: the Qualification extended from "the second half is withdrawn" to "both legs are withdrawn," with the footprint account, the intent-does-not-rescue-it argument, the vocabulary-as-judgment reframing, and the reversed cost argument; the Feedback section's "or changes the world beyond it" clause dropped entirely, since a read changes state too; Open question gained whether footprint admits a usable measure. `25-arch-invariant-layer/01`: the input-domain section's basis replaced — typed effects are the tracked-footprint subset, not the world-changing subset — with the read's membership in the domain now resting on a stronger reason than before. `20-arch-runtime.md`: the same basis replaced on the action path, plus a note that the runtime's existing semantic-classification work (destructive action versus read-only inspection) is a footprint judgment and therefore on the same axis rather than a special case; open question updated to lead with whether footprint is measurable.

---

## F42 — Thinking is a family of processor roles whose defining product is a proposed knowledge-state transition; the membership test is which store moves

**Claim.** `10-foundations/02` defines Thinking as a procedure and says "thinking is what a processor does with it" without naming any processor, and `22-arch-cognition` represented none of it. This pass first recorded that only as a gap. The user supplied the shape: thinking is to be understood as a **family of processors whose primary role is to explicitly trigger knowledge-state transitions**.

The word doing the work is *explicitly*. It converts a description of careful reasoning into a mechanical membership test — a processor belongs to the family when its product is a proposed mutation of the knowledge model (`10-technical/01-effect-vocabulary.md` type 5). That separates thinking from chain-of-thought by reference to something checkable: **which store moves**. Reasoning inside a generation produces tokens, which `04`'s account registers as an artifact into the live context pool, and nothing the project holds has changed. A knowledge-state transition is `21-arch-knowledge-model` changing. A processor can reason at length and perform no thinking, and can perform thinking with one short proposal.

Two consequences follow that were not asked for and are results rather than restatements.

**Collapsing (`05`) is the null case, not an act.** Nothing performs it and nothing decides it, which is exactly why it is cheap: it is what happens to everything no thinking processor proposes a promotion about. This also dissolves an apparent conflict between `05`'s "no visible trail" and `26-arch-observability`'s reconstruction requirement — the absent trail is in the knowledge model, not in observability's own history, and the two were never in competition. (F43 briefly withdrew this and was itself corrected; the claim stands as written.)

**Curated memory gets an actor without a new one being invented.** `03` hands scope assessment to whoever curates and `05` accepts the job, but no actor existed to hold it. Deciding a claim is worth keeping, and assessing its scope, are both proposals that change what the project holds, so both are family members. Scope is the member with a deadline — `03` says it must be assessed near creation or not at all — which distinguishes it from a promotion decision that can wait.

A third consequence is stated in the new document and deliberately **not** adopted: if nothing reaches `21` except through this family, the knowledge model is write-gated by role, which would give `03`'s motivating worry — an interpretation stored as truth and later read as evidence — a structural answer rather than only a schema. The line that would make it affordable is `03`'s own motto, since an observation entering the record is runtime bookkeeping and needs no thinking processor while an interpretation does. It is stronger than anything the foundations currently require, so it is held as a consequence to argue, and `21` keeps its unqualified "a processor."

**Mode: Reasoned**, the framing **Operated** in the weak sense used in F37, F40 and F41 — the user supplied the family-of-processors formulation directly; the membership test, the store-based distinction from chain-of-thought, and the three consequences were derived here.

**Grounds.** `10-foundations/02`'s Thinking section, which already calls a walk's product a knowledge-state transition and already assigns it to a processor without naming one; its Feedback section, which already says what doing returns is raw and that turning it into knowledge is thinking's half — so promotion-to-a-claim was a thinking act before the family had a name; `10-foundations/04`'s crossing account, which is what makes the generation/pool versus knowledge-model distinction available at all and which did not exist when `02` was written; `10-foundations/03`'s Scope and Provenance sections for the curation and souvenir members; `22-arch-cognition/02-processors.md`'s open, evidence-grown role vocabulary, which is what permits a family rather than requiring one role.

**Changed.** New `22-arch-cognition/04-thinking.md`: membership test, the chain-of-thought distinction, why a family rather than one role, five candidate members, what the family does not do (record, sequence, or index), and the write-gating consequence held as unadopted. `10-foundations/02`'s Thinking section points at the actor and states the store-based test. `21-arch-knowledge-model/01` gains **Traverse dependents** as a distinct service — the walk searches downward through what cites a claim, the opposite direction to an ordinary provenance lookup — plus a note that write-gating by role is proposed and not adopted. (Both this entry and `04-thinking.md` first pointed at I5 as where an index for the traversal would go; **removed**, on the user's instruction not to optimize prematurely. The pointer also contradicted `21`'s own naive-default paragraph two sections away, which forbids an index until evidence names the naive version as the bottleneck. The service stands; only the anticipated optimization went.) `22-arch-cognition/02-processors.md` names the family as a recognised subset of the role vocabulary. `10-foundations/05` gains Collapsing-as-default and the curation actor. `20-arch-runtime.md`'s map line for `22` updated.

---

## F43 — The knowledge model is where artifact content lives; that is a storage decision and does not change the retention default, which stays forgetting

**Claim.** The user set a provisional arrangement: artifacts are registered into `21-arch-knowledge-model`, and the live pool holds only references to those entries plus context-management metadata.

This generalises what was previously a single exception. `23-arch-context-management` held a reference-plus-metadata for knowledge-base retrievals only, because a retrieved claim already had an identity while a tool output did not. Registering every crossing as an Observation makes the exception the rule and removes the asymmetry. `10-foundations/03`'s Observation type already covers what crosses — "a test failed, a command returned a value, a file changed... a processor produced a recommendation" — so nothing in the substrate had to be stretched. The purpose is narrow and the user stated it directly: it avoids rewriting artifacts from context into the record, because a promoted artifact was never anywhere else.

A first pass here read it as a retention decision and drew three conclusions from that, all wrong. It held that nothing is forgotten by default; that Collapsing therefore becomes an act and F42's null-case claim falls; and that scope assessment consequently runs at every write, breaking half of `05`'s cheapness argument. The user corrected the premise: where content lives and how long it is kept are independent. **The default remains that an artifact no longer live, which nothing registered for remembrance, is removed.** F42's claim stands, `05`'s cheapness argument stands whole, and scope runs at promotion rather than at every crossing, since scope is a property of a claim and a swept observation never becomes one.

The correction also makes the design substantially cheaper than the version it replaces, by way of a consequence neither side stated. For nearly everything, remembrance needs no judgment at all: it is **reachability**. `03`'s roots-stay-raw rule already means a promoted claim's cited observations cannot be removed, and an observation no promoted claim cites has nothing depending on it. So something survives because a thinking processor built on it — a decision already made on its own merits — and the rest is swept by graph traversal. Judgment is needed only for the deliberate exception: keeping something nothing has cited yet. That is a far smaller surface than deciding the fate of every entry, and it needs no model calls for the common case.

One repair to F42 does hold. Its membership test, "which store moves," no longer discriminates, because both thinking proposals and ordinary crossings write to `21`. What discriminates is **whether anything was proposed**: an Observation is bookkeeping, unproposed and ungated, which `10-technical/01` already classes that way, while everything above Observation is a thinking proposal. The test gets sharper rather than weaker and lands exactly on `03`'s motto — what happened is recorded automatically, what it means is not.

**Mode: Reasoned**, the arrangement and its correction both **Operated** in the weak sense used since F37 — the user set the arrangement and then identified the over-reading directly. The reachability consequence and the membership-test repair were derived here.

**Grounds.** `10-foundations/03`'s Observation definition, which already admits tool outputs and processor products; its Provenance section's roots-stay-raw requirement, which is what makes reachability a sufficient retention rule rather than a heuristic, and its souvenir mechanism for compression; `10-foundations/05`'s Curated memory, which already states that the forward-looking judgment is not among `03`'s three weighing dimensions; `10-technical/01-effect-vocabulary.md`'s bookkeeping exclusion, which is what lets Observation registration be ungated.

**Changed.** `23-arch-context-management/01`: Register rewritten so what crosses is written to `21` while this actor keeps a reference plus metadata and no content of its own; new §The pool is an index, not a store, stating explicitly that it is about where content lives and not about retention, since reading it the other way inverts `10-foundations/05`. `21-arch-knowledge-model/01`: Write split into bookkeeping and proposal paths; new **Compress** and **Elide** services, with Elide framed as the default path and reachability as both its precondition and, for nearly everything, the whole rule. New `22-arch-cognition/05-curation.md`, rewritten once on the correction — default sweep, judgment only for the exception, compression separable, scope at promotion. `22-arch-cognition/04-thinking.md`: membership test restated on proposal rather than store, chain-of-thought section corrected, curation described as marking exceptions rather than as deciding everything. `10-foundations/05`: the Collapsing passage **collapsed back** to the default framing after the same-day qualification proved wrong, with the storage arrangement and the reachability rule written into it. `26-arch-observability/01`: its own copy named as what outlives the sweep.

The ARES material this pass first attached to curation was **relocated**. `70-THINKING/07-when-to-decompose/18-ares-soundness.md` retains claims in a premise set carried forward to later reasoning steps, which is what is available to reason from next — recall (`23-arch-context-management`), not what is durably kept. Its finding that keeping every base claim was consistently best with a strong judge, and that selective retention helped only a weaker binary one, is therefore evidence about the recall policy. What transfers to curation is only the collapse mode: an overconfident judge drives retention toward one, the filter stops filtering, the mechanism becomes a no-op at full cost, and the sheet notes no diagnostic was proposed. That applies to deliberate remembrance and not to the sweep, which has no judge. Both readings are second-hand (`03`) — the sheet is this project's read of that paper.

---

## F44 — The naive-default restraint sequences the work; it does not doubt that a real store will be needed, and that difference has one design consequence

**Claim.** `21-arch-knowledge-model` states the restraint as "no graph database, no vector index, no model-mediated retrieval, until evidence says the naive version is the actual bottleneck." Read plainly, "until evidence says" makes the sophisticated version **contingent** — something that might turn out to be needed. The user corrected the reading: a proper ontology, model-mediated knowledge, and a real graph store are obviously going to be needed. Only the timing is open.

That is a small change in wording and a real one in consequence. If the replacement is certain rather than contingent, the naive shape has an obligation it does not have otherwise: it must not foreclose the replacement. What has to stay stable across the change is each actor's **service surface**, not its storage shape, and a caller must never learn that a claim or a work item is a file. If paths, formats, or directory structure leak into an interface, the eventual move stops being a substitution and becomes a rewrite of every caller — which is the one way a deliberately crude starting point turns into a trap rather than a baseline.

Worth noting that the ontology is not starting from nothing either. `10-foundations/03`'s four claim types, and its source, mode-of-acquisition and scope axes, are already a proto-ontology, and they were reached from real cases — the hand-tagging trial, the ETH correction — rather than designed in advance. That is the shape the rest of it should take.

**Mode: Reasoned**, the correction **Operated** in the weak sense used since F37 — the user stated the position directly. The interface-stability consequence was derived here.

**Grounds.** `21-arch-knowledge-model/01`'s own naive-default paragraph, whose "until evidence says" phrasing is what carried the contingent reading; `10-foundations/04`'s "a naive default is still required" argument, which asks for something crude and measurable so a smarter version has a baseline to beat — an argument that assumes a smarter version is coming, and therefore already implied this without saying it.

**Changed.** `21-arch-knowledge-model/01`: the restraint reframed as sequencing rather than doubt, with the service-surface obligation stated and `03` named as the ontology's existing seed. `28-arch-work-record/01`: the same reading applied to its own naive default in one sentence.

---

## F45 — Objective validation is a system-instance strategy, not an unowned architectural boundary; only its recorded verdict is architectural

**Claim.** `04`'s The objective itself is not a given closed by saying the objective-validity boundary "has no owner yet," and this pass proposed taking it next as a missing-actor gap of the same kind as the work record and thinking. The user rejected the framing: whether a system instance validates its objectives is that instance's to implement or not.

The rejection holds on inspection. Architecture would have to own this only if it needed something that does not already exist, and nothing does. A processor reasoning over what it was given is the definition of a processor. Recording that a task rests on a false assumption is already enumerated under `10-technical/01-effect-vocabulary.md` type 4. The candidate matches `04` says context assembly must surface for the "already satisfied" case arrive as ordinary retrieval artifacts, which needed no new service from `23-arch-context-management`. So there is no missing actor, no missing mechanism, and no missing capability — only an open question about whether a deployment commissions such a role, which `22-arch-cognition/02-processors.md`'s deliberately open role vocabulary already governs.

This is the same correction the user made to arbitration earlier in this pass, and the pattern is worth naming because it recurs: a behavior named in the foundations, with no actor attached, reads as an architectural gap whether or not it is one. It is one when something must exist for the behavior to be possible. It is not one when the behavior only requires that somebody choose to configure it.

What survives as architectural is narrower and concerns representation rather than judgment. If an instance does run the check, its verdict has to be distinguishable from an ordinary failure to proceed, and Milestone 5 recorded that distinction collapsing — the orchestrator resolved both "the task rests on a false premise" and "I cannot find a next step" to a generic `blocked`, where the Milestone 4 arms had explicitly declined.

**Mode: Reasoned**, the correction **Operated** in the weak sense used since F37. The evidence cited on both sides is **operated**: findings-log entries 5 and 6 are real runs.

**Grounds.** `10-technical/01-effect-vocabulary.md` type 4, whose Includes line already names "recording that a task rests on a false assumption" — so the recording half was never unowned; `22-arch-cognition/02-processors.md`'s open role vocabulary and its statement that the set of roles grows on evidence; findings-log entry 5 for the M4 positive (both arms declined a false-premise task) and entry 6 for the M5 collapse.

**Changed.** `10-foundations/04`: the closing "no owner yet" clause replaced by a dated §On ownership note, stating that validation needs no mechanism that does not exist and that commissioning is instance strategy, while naming the representation residue. `28-arch-work-record/01`: the recorded-conclusion responsibility now says why keeping *declined* distinct from *blocked* is load-bearing, citing the M5 collapse, and separates that from whether an instance judges validity at all.

---

## Unchecked justifications

Findings above are grounded in something read or directly checked. The items below are
not — they are attempted arguments this pass relied on without independently verifying
them, and the next pass on `03` should treat them as open rather than settled.

- **Reachability as a sufficient retention rule (F43) is argued from `03`'s
  roots-stay-raw requirement and has never been run.** It is attractive because it needs
  no judgment, but it assumes every artifact worth keeping gets cited by something
  promoted during the episode that produced it. The failure case is an artifact whose
  value is only recognised later, after the sweep already took it — and nothing in this
  design notices that happening, because the evidence it happened was removed. The
  deliberate-remembrance exception exists precisely for this and is the part with no
  criterion.

- **Peak store size during a long episode is unestimated.** Steady state is bounded by
  what is live plus what was remembered, which is the argument that the arrangement is
  affordable. That argument says nothing about an episode that runs long enough to
  accumulate a large live set before any sweep fires.

- **A remembrance judgment that has stopped discriminating produces an absence, and
  nothing detects it.** The ARES sheet
  (`70-THINKING/07-when-to-decompose/18-ares-soundness.md`) describes the collapse: an
  overconfident judge drives every retention probability toward one, the filter stops
  filtering, and the mechanism becomes a no-op while still costing what it cost before,
  with no diagnostic proposed. The sweep bounds the damage here — an over-generous
  curator grows the store rather than corrupting it — but this pass proposed no
  diagnostic either.

- **The thinking family's membership test (F42) has never been applied to a real
  processor.** "Its product is a proposed knowledge-state transition" is crisp on
  paper, and no run has produced a case where it was unclear whether a processor
  qualified. The likely hard case is a processor whose main job is something else and
  which proposes one claim along the way: the test says it performed thinking, which
  may be the right answer or may show the test is too coarse to carry the write-gating
  consequence built on top of it.

- **"Detection can stay incidental while resolution is deliberate" (F42) splits a
  question `03` poses as binary, and nothing checks that the split is legitimate.** It
  is attractive because it explains the ETH case — friction arose from use, resolution
  took a deliberate reread — but one case that fits is retrodiction, the same standing
  this pass gives the granularity account in `22-arch-cognition/08`.

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

- **Scope (F28) is argued entirely from internal consistency.** No case was checked
  against it the way OQ-7 grounded requalification or `50-findings/09` grounded
  convergence. Whether "cannot be reconstructed from provenance" actually holds for a
  real claim in this corpus, rather than being a plausible-sounding distinction, is
  untested.

- **"Nothing requests a composition; the context manager is traversed, not called"
  (F37) is a claim about where a boundary sits, and no implementation has tested
  whether it survives contact with one.** It is coherent with everything else in the
  band, which is weaker than being right. In particular, it assumes there is always a
  well-defined "turn" to compose at — an assumption that holds for a request/response
  model call and may not hold for streaming, for a model that emits several tool calls
  before yielding, or for any arrangement where feeding is continuous rather than
  discrete. Nothing in this pass checked that.

- **The mutability argument separating `28-arch-work-record` from `21` (F38) has no
  measurement behind it.** That a work item's current state "must be readable without
  walking anything" is asserted from the orchestrator consulting it per loop step; the
  cost of walking a supersession chain instead was never estimated, and at the scale
  these runs operate at it may be negligible. The separation may be right for reasons of
  write discipline and still be unjustified on the performance grounds offered alongside
  it.

- **The GitLab-issues study behind F36 has not been read by this pass.** Its
  index/arbitration/forced-choice mechanism is carried entirely on the user's own
  account (second-hand, per `03`) — no citation, no verification that the study
  describes the mechanism this accurately, or at all. `04`'s new section rests on it
  as stated; a primary-source check is owed before this is promoted further.
