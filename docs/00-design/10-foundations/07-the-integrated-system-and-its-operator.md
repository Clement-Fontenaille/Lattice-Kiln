# The Integrated System and Its Operator

> **Motto:** Everyone deserves a good ride.

The plain restatement, for use where the motto would be unclear: *if it didn't work for them, it didn't work.*

## TL;DR

Two commitments that constrain what may count as a result, and one requirement
that follows from them.

The unit of evaluation is the **integrated system** — system, model, knowledge and
the operator together — never the model alone.

What the project optimizes is **what that assembly achieves for the person using
it**, not what the system achieves on its own behalf. Accessibility is therefore a
primary objective rather than a finish applied at the end.

From those two: **authorship preservation** — the work must remain recognisably
the operator's, because their ability to judge it is what makes supervision real.

## Motivation

A capability that pays off only for operators who already know how to obtain it
has not reduced any difficulty. It has redistributed one.

The same tooling is producing sharply different outcomes for different operators —
strongly positive for some, neutral or negative for others (findings entry 9, §1).
The spread, not the average, is what needs explaining, and the pattern resembles
stratification rather than diffusion: benefits concentrating where practice
already exists, costs surfacing late and elsewhere, and a demand for more operator
judgement rather than less.

A project that treats operator success as downstream of system capability will
reproduce that pattern. This document states that it is not downstream.

## Ingredient one — the integrated system is the unit

No claim of the form "a model of size *N* can or cannot do *X*" is meaningful
without naming the scaffold around it, the knowledge available to it, **and the
person operating it**.

The same work is tractable for one assembly and not for another. Whether something
can be done, and how hard it is, is a **relation between the work and the
assembly**, never a property of either alone.

The operator belongs to the assembly. What they know, how they phrase a request,
what they think to check: these sit inside the thing being measured, not among the
conditions it is measured under. An operator who asks for the wrong thing has not
supplied a bad input — the assembly has produced a bad result.

Consequences:

- Results are reported per **configuration**, never per model. A model name is not
  a sufficient description of what was measured.
- A comparison that changes the model while leaving the scaffold implicit has not
  isolated anything.
- Improvements to scaffold and to knowledge are first-class results, on equal
  footing with improvements to the model.
- There is **one limit**, not a ceiling and a floor. What looks like a floor —
  a level of operator skill below which the assembly stops working — is the same
  ceiling, reached through a different component.

### Measurement without an operator in it

This does not devalue experiments that have no person in them. Most of this
project's do not, and should not. What they measure is a **sub-assembly** —
system, model and knowledge with the operator's part held out — which is a real
quantity, cheaply obtained, and frequently the only one available.

The error is not running them. It is reading their results as results about the
whole assembly. A sub-assembly measurement is evidence about a component, and it
reaches the assembly only with the operator's contribution argued separately.

What follows from that is a standard rather than a caveat. Such a result has **no
intrinsic value** — only the value of the decision it informs. So:

> A measurement taken without an operator must name the decision it is for and who
> will make it.

The person has not left; they have moved up a level, building the assembly rather
than using it. Everything in this document applies to them in that role. And a
benchmark on which no builder's decision depends has nothing to fall back on,
because there was never an intrinsic value underneath it.

## Ingredient two — the operator's performance is the objective

The quantity being improved is what a person accomplishes, not what the system
accomplishes on its own behalf.

This is the general form of a commitment the project already holds in a narrower
place. Reduced entropy — fewer regressions, correct refusals, work that does not
need undoing — is valuable precisely because it is what an operator experiences as
help. Throughput that arrives with a proportional increase in review burden has
moved the work rather than reduced it.

### The attribution rule

This is what the ingredient is for, and it is a rule about how results are read
rather than a target to aim at.

> **Within the population the assembly claims to serve, a failure belongs to the
> assembly. There is no such thing as a user who was not good enough.**

The conventional reading of an operator who cannot get the tool to do something is
that they lacked the competence. Under ingredient one that reading is unavailable:
the operator is part of the assembly, so what looks like their shortfall is the
assembly's limit reached through them. The failure is not incompetence. It is
**inaccessibility**, and it is the assembly's.

This is the same move ingredient one makes for the model, applied in the other
direction. Do not attribute to the model what belongs to the assembly; do not
attribute to the operator what belongs to the assembly.

It is not a claim that no operator is ever mistaken. It has a boundary, and
drawing that boundary is the obligation the rule creates:

**Name the population.** An assembly must state who it is for — *"engineers who
can write a job script for this facility"* is a claim that can be held to;
*"anyone"* is not. Inside that population, failures land on the assembly. The
boundary is a design commitment, not an escape hatch, and moving it outward to
excuse a failure is the specific abuse to watch for.

Two instructions follow, each implying a procedure rather than an attitude:

**You are not the operator.** The person the system serves is not the person
building it, and does not share the builder's fluency with it. A design validated
against its own author's facility has been validated against the wrong member of
the assembly — so validation has to run against an operator who lacks that
fluency.

**The spread across the population is the measurement.** A result that holds only
for its most capable member is a result about that member. What the assembly
achieves for its least practised member is the number that matters, and the
distance between the two is what says whether the thing is accessible or merely
powerful.

## Authorship preservation

The work must remain recognisably the operator's, in two directions.

**On the way in**, the system should be able to tell what it generated from what
it was given — whether anything entered a context, plan or specification that the
system did not already hold.

**On the way out**, it should act **within the mandate it was given**, and treat
work beyond that mandate as requiring a new one — including where each step past
it is locally justified by the last.

This is not a candidate for the invariant layer. It is not inviolable by
construction and it cannot be enforced by deterministic refusal alone. Neither is
it a preference to be traded away under load, which is what it becomes if it lives
only in prose. It is a requirement designed in from the start, because a system
that has already spent what it protects cannot get it back.

### Why it matters: comprehension

Work a person did not author is work they do not hold. Enough of it costs them the
standing to judge the next change — the position the whole supervision arrangement
depends on them keeping.

The cost is not paid gradually. Eroded comprehension is not missed while the
automation works; it is missed the first time the automation cannot finish
something, which is when the operator must re-enter work they stopped reading. The
capacity needed to recover is the one that has been eroding. So it cannot be
traded against throughput: the trade looks free for as long as it is not needed.

Evidence is in findings entry 8, where the weakest arm's failures were reaches
outside what was asked rather than failures to do the work, and in entry 9 (§1,
§5) for assisted change size, unreviewed merges, and a documented reversal from
full autonomy.

### What the operator must supply, and why approval cannot supply it

**A decomposition cannot be authored from inside the limits it relieves.**
Producing the pieces requires holding the objective while cutting; checking that
they recompose requires holding the original and the parts together. So provenance
is evidence rather than metadata: an artifact cut from above the limit and one cut
from below look alike, and nothing internal separates them. The limit is relative —
above the limit of whoever consumes the decomposition — and the author need not be
human.

**Approval cannot supply it.** Not because approval is empty, but because:

- It can only subtract. It rejects what is present; it cannot introduce what is
  absent.
- Refusing costs more than approving, so every approval interface leans toward
  assent independently of diligence. Mechanical, not moral.
- Its quality is invisible: considered and reflexive approval leave the same trace.
- It moves responsibility without moving understanding. Whoever approves owns the
  outcome, including where they could no longer evaluate it.

What follows is a different request, not more diligence:

> **Ask what only the operator can answer. Where the system must decide, yield
> with the reasoning that would let the decision be overturned. Never present what
> the operator can only accept.**

Both modes place the operator's act where it is cheap for them: answering about
intent rather than evaluating an artifact, checking why rather than what. Reasoning
that would *overturn* a decision, rather than justify it, has to name something the
operator can find false — which is what keeps the practice from becoming
boilerplate.

### What this has to become

The requirement is stated here at the level where it is stable. Two constraints
govern its translation into architecture.

**It must become checkable properties of artifacts and effects, never an inference
about intent.** "Do what the operator would have wanted" is a prediction about a
person, and a system inferring intent in order to be faithful will confidently be
faithful to the wrong thing. What is available instead are properties of the work
itself: a declared scope compared against what was touched, a change required to
beat the pre-existing state, a source recorded for each part of an assembled
context.

**Its mechanisms belong to the components that already own them**, and are named
here only as destinations: scope declared and checked belongs with the capability
and authority model; provenance on context items with observability and context
assembly; the two-mode handoff with the processor contract and the effect
vocabulary, where a required stop-rationale already exists as its narrower form.

**Where those destinations stand.** Provenance on context items is in place: crossing
type distinguishes generated from fetched on every tracked entry, and
`23-arch-context-management` carries the constraint that the distinction must survive
into what the model is actually shown rather than being flattened there.

Scope declared and checked has a shape and no implementation. Capability gating cannot
carry it, because a capability is keyed to the actor and evaluated per effect while a
mandate is keyed to the work item and evaluated in aggregate against what was touched —
so every step of a drift can sit inside capability while the whole sits outside the
mandate. What the architecture settled instead: a scope is expressed per task in natural
language and held on the work item (`28-arch-work-record`); the ceiling is derived from
intent by an invariant processor while the orchestrator may only narrow beneath it; the
check divides on reversibility, auditing reversible extent at the end of a task and
questioning an irreversible change before it happens.

Two notes on that, both bearing on this document's own constraints.

**A scope is usually derived rather than stated, and that is still not the inference
this document forbids.** An operator rarely writes a boundary down; a request to add
an output format to a CLI tool carries one anyway, reaching the interface
specification and its functional tests but not the web API documentation. What is
prohibited above is inference about a *person* — predicting what they would have
wanted, which is unbounded and unfalsifiable. Deriving what a task reaches, from the
task and the arrangement of the system, is inference about artifacts: checkable by
anyone who knows the codebase, and capable of being shown wrong. Where the operator
does indicate a boundary, that indication governs the derived one.

It follows that a derived scope has to be recorded *with what it was derived from*,
and this is the two-mode instruction above rather than an addition to it: where the
system must decide, it yields with the reasoning that would let the decision be
overturned. A boundary derived and never shown is not checked, it is ratified — and
the audit then measures the work against a mandate that was already too wide.

And where the reading is genuinely ambiguous, the *other* mode applies: ask what only
the operator can answer, by proposing the plausible interpretations rather than
inferring one. Scope turns out to exercise both halves of that instruction, which is
the clearest case the project has of it being a pair rather than a preference. Note
also that recording reasoning does not substitute for asking here, since a derivation
and a choice between two defensible readings leave records that look alike — the
second needs to be a question, not a better-annotated answer.

**The processor is a fixed role rather than a commissioned one**, held with the
invariant layer for the reason given there: a loop cannot commission its own watcher,
so it cannot be trusted to keep one either (`25-arch-invariant-layer`).

The minimal statement, for whoever implements it: **generated content must not
silently occupy the place of authored content.** The system should know the
difference, represent it, and behave differently on each side of it. This is
alignment by design rather than containment — it does not restrict what effects
may occur, it constrains how the system is permitted to compose its own inputs.

## Relationship to neighbouring concepts

The constrained-intelligence thesis explains why scaffolding is worth building.
This document constrains **who the scaffolding must work for**, and refuses the
reading under which a scaffold that only helps experts counts as success.

The evidence and provenance vocabulary already distinguishes observation, evidence,
finding, and decision. Authorship preservation is an application of that machinery
to a new axis rather than a new mechanism — for the inbound half.

`04-context-as-governed-resource.md`'s crossing model gives every artifact a
**crossing type**: a generation, a read of the external world, a retrieval from the
knowledge base. That distinction is exactly "what it generated from what it was
given". `03`'s Source axis carries the second cut, between a human's contribution
and the system's own. Together they answer the inbound direction with nothing new
built.

The outbound half is untouched by that. Acting within a mandate, and treating work
beyond it as needing a new one, is not a property of where an artifact came from.

Context governance decides what a processor sees. This document adds that *where
each part of it came from* is part of what must be governed — now realized, since
`23-arch-context-management` carries crossing type on every entry it tracks and
`26-arch-observability` records the conditions each stretch of history accumulated
under.

## Status

The two ingredients, the attribution rule and its two instructions are held.
Authorship preservation is held as a requirement, with its motivation, at the level
where it is stable — its mechanisms are named as destinations rather than specified
here.

Authorship preservation is deliberately **not** wrapped in a structural layer of its
own above the invariant floor. Such a layer would have no membership test and exactly
one occupant, and the occupant would be the content — which is a requirement wearing a
layer's clothes rather than a layer.

## Open questions

How authorship is represented and enforced — whether the existing provenance model
already carries it, and what enforcement means for a property that is not
amenable to deterministic refusal.

How operator performance is measured without collapsing into self-report.
Perceived ease is disqualified as evidence (findings entry 9, §2), including this
project's perception of its own tools.

Whether spread across the population is the right measurement of accessibility or
merely the first one available — and what would distinguish a genuinely accessible
assembly from one tested against too narrow a sample of operators.

Whether restraint — keeping changes narrow, leaving the operator able to question
the work — comes from the model or from the harness around it. The answer decides
how much of this requirement has to be built rather than inherited, and the
comparison that would separate them is one this project can run.

That question turns out to be `01-constrained-intelligence-thesis.md`'s unresolved
either/or, for one class of scaffolding. `01` asks whether scaffolding substitutes
for capacity or bounds what capacity can spoil, and records a first observation
pointing at the former — but only for *context management*, since a capable model
can find its own material. Restraint belongs to the other class, the one that
concerns damage rather than retrieval, and a model that needs no help finding
material may still need preventing from acting on a bad conclusion. So the
comparison named here is the one that would settle the half `01`'s observation
could not reach.
