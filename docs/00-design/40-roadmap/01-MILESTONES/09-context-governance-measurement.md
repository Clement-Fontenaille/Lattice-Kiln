# M9 — Context governance measurement

**State:** open. Possibly a prerequisite for evaluating M7's front half — see
[`../00-backlog.md`](../00-backlog.md).
**Was:** M7, before rework 2
**Baseline it measures against:** [`07-naive-context-assembly.md`](../../../10-technical/07-naive-context-assembly.md)
**Design:** [`04-context-as-governed-resource.md`](../../10-foundations/04-context-as-governed-resource.md), [`03-evidence-belief-and-provenance.md`](../../10-foundations/03-evidence-belief-and-provenance.md) (Weighing claims, Scope)

## What this milestone is

The goal is **not** to design good context governance. It is to establish the
naive default from [M4](completed/04-ephemeral-processors.md) as a measurable
baseline, and to develop **metrics for context quality that are independent of
final task success**.

Without those metrics, a later decision to commission a context-curator role
cannot be made on evidence. This milestone produces the evidence base; it does not
pick the mechanism.

This is [M8](08-persistent-work-and-knowledge.md)'s experimental framework, in the
sense that follows: M8 builds the substrate and runs a first sweep against it —
does the system hold and use knowledge it did not derive itself. This milestone is
what turns "it seemed to work" into a measurement, by supplying dimensions that do
not collapse into task outcome.

## Why the independence matters

A context-quality metric scored by task outcome is a failure predictor wearing
another name. If context quality can only be recognised after the task succeeded
or failed, it cannot be used to *decide* anything during assembly — and the
curator role it is supposed to justify would be evaluated by the same signal that
already evaluates everything else.

This is the same construct problem experiment E1 in
[`../03-research-and-evaluation/`](../03-research-and-evaluation/) attacks from the probe
side: label by **construction**, not by outcome.

## What measures this now has to work with

The 2026-09-10 foundations pass gave this milestone dimensions it did not have
when it was written. `03`'s Weighing claims names three — validity, reliability,
pertinence — each stated as assessable independently of whether the claim they
describe ends up load-bearing in a successful task. `03`'s Scope names a fourth,
harder one: a claim's own bounded domain of applicability, which cannot be
recovered from provenance after the fact and has to be assessed near creation —
making it the sharpest test of "independent of final task success," since a
scope failure is exactly a claim used correctly by outcome but outside where it
actually held.

`70-THINKING/ideas.md` I11 (retrospective ground truth) is an existing, unadopted
candidate method: reconstruct what a context assembly should have contained from
an eventual real solution, and grade each stage's recall against it after the
fact rather than by whether the task passed. It was recorded before this
milestone had a substrate to grade against; it has one now.

## Evidence question

Do validity, reliability, pertinence, and scope — assessed on `03`'s terms,
recorded at the point a claim enters or leaves an assembled context — separate
the naive assembler's known failures (the wrong-file writes on `wf1`, the missed
helper on `wf4`/`wf6`) from its successes, without consulting whether the task
that used them passed?

The bar recorded at rework 1 is still the right shape as a floor:

> The naive assembler's observed failures are quantifiable, and a less-naive
> assembler moves the metric.

## Why it may need to move earlier

[M7](07-static-supervised-workflow.md)'s proposed front half is convergence before
implementation, and its unresolved problem is that **convergence closes on
nothing** — `dloop` closes on a test, but nothing validates the artifact the
convergence step produces. Validating that artifact is a context-quality question,
which is this milestone's subject.

If M7's front half is pursued, this milestone becomes a prerequisite rather than a
later measurement chore. If M7 ships with the settled back half only, it does not.
That decision is open and is tracked in [`../00-backlog.md`](../00-backlog.md).

## Relationship to M8

[M8](08-persistent-work-and-knowledge.md) builds what this milestone measures.
This milestone does not depend on M8's corpus sweep having succeeded — a sweep
that fails is exactly the kind of result these metrics need to be able to
explain — but it does depend on M8's substrate existing to assess in the first
place.

## What foundations now gives this milestone to measure

[`04-context-as-governed-resource.md`](../../10-foundations/04-context-as-governed-resource.md)
names **four failure modes**, and a context-quality metric has to be able to tell
them apart rather than score context on one axis.

- **Insufficiency** — needed coverage absent. It divides: material that never
  crossed, and material that crossed but was not recalled. Only the second is
  visible from the live set (`10-technical/14-context-manager.md`); nothing can be
  compared against what was never fetched.
- **Redundancy** — duplicated coverage inside one window. Evidenced, findings entry 9
  §3. It requires tracking overlap **at the level of coverage rather than text**: two
  artifacts restating one finding in different words are redundant with no shared
  substring, so a deduplication pass measures the wrong thing.
- **Uselessness** — material neither needed nor duplicated. Predicted, not evidenced,
  and predicted to be harmless in isolation — Overload's raw material rather than a
  cost of its own.
- **Overload** — the aggregate exceeding what the assembly can integrate in one pass.
  Predicted, argued from retrodiction, not directly tested. Its named falsifier is
  E2.

**Only Overload is content-quality-agnostic.** The other three are about *which*
artifacts are present; Overload is about how much is present once coverage has
decided that.

### Two earlier phrasings this milestone should not carry down

An earlier statement of the same ground held that *what makes context costly is
redundancy, not volume*. `04` now says the opposite half of that explicitly: a
context can be entirely non-redundant and still be too much for a given assembly,
which is **Overload**, a different axis rather than a restatement. Volume is a real
cost with its own name.

The companion phrase, *too much is a relation and not a property*, survives and
sharpens: too much is relative to an assembly and an objective, which is why the
metric cannot be a threshold on size. `10-technical/07-naive-context-assembly.md`
truncates by token count, which is the volume reading of both, and carries that as
its own open contract.

## Work packages

1. **The recall trace.** Per turn: which live-set entries were included, in what
   order, which were dropped, where truncation happened
   ([`07-naive-context-assembly.md`](../../../10-technical/07-naive-context-assembly.md)
   requires it already). Two policies over one live set are comparable **only if what
   each presented was recorded**, so this is the package everything else here rests
   on — and it costs nothing at runtime, which is why it is the one most likely to be
   skipped.
2. **Turn-input records** — kind 5 in
   [`02-observability-event-model.md`](../../../10-technical/02-observability-event-model.md).
   Built in [M8](08-persistent-work-and-knowledge.md) or here, whichever runs first.
3. **The four failure-mode detectors**, one per mode named below. Insufficiency
   divides and only half of it is detectable; Redundancy needs overlap **at the level
   of coverage rather than text**; Uselessness is predicted and unevidenced; Overload
   is the only content-quality-agnostic one.
4. **The four claim dimensions** — validity, reliability, pertinence, scope — assessed
   on `03`'s terms at the point a claim enters or leaves an assembly. Scope is the
   sharpest of the four and the hardest: a scope failure is a claim used correctly by
   outcome but outside where it actually held, which is precisely the case an
   outcome-scored metric cannot see.
5. **Re-grade E6.** [M8](08-persistent-work-and-knowledge.md) runs the corpus sweep;
   this milestone is what makes its result mean something other than *it seemed to
   work*.
6. **A less-naive assembler**, as the thing that moves the metric. The bar recorded at
   rework 1 has two halves and the second is usually forgotten: the naive assembler's
   failures are quantifiable, **and** a less-naive one moves the measurement.

Packages 1 and 2 are plumbing and can land with M8. Packages 3 and 4 are the
milestone. Package 6 is what falsifies the metric — a dimension no better assembler
can move is a dimension that was measuring something else.

### A cost this milestone should know about before it baselines

[M17](17-mandate-chain.md) carves a **permanent share of the resident envelope** for
the scope checker's slot, busy or not, because isolation costs context for every slot
that exists (`10-technical/14-context-manager.md`). Overload is measured against that
envelope.

So a baseline taken before M17 and compared against a reading taken after it is a
comparison across two different machines. Either this milestone runs after M17, or it
records which side of that line each reading was taken on.
[`../00-backlog.md`](../00-backlog.md) currently orders them the other way, and the
question is open rather than decided.

### What the metric depends on existing

None of the four modes is checkable without the live set being a first-class,
inspectable record rather than a byproduct of whatever assembly did. Redundancy
compares a candidate against what is already live; Insufficiency compares what is
live against what the objective needs; Overload needs a running total rather than a
count taken afterwards. That record now exists in specification
(`10-technical/14-context-manager.md`), which removes the precondition this
milestone used to owe.
