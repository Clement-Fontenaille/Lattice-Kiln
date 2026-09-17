# E1 — Can context pathology be detected from processing?

**Status:** not run.
**Gates:** nothing downstream depends on it; it feeds `10-foundations/04`'s failure
modes and M9's metric.
**Protocol:** [`experiments/E1-context-pathology-probe/PROTOCOL.md`](../../../../experiments/E1-context-pathology-probe/PROTOCOL.md)
— covers the first move only. The probe battery is blocked on an unspecified
feature space; the folder's README states the gap.

## The question

Whether a probe can distinguish a **constructed** context stress from its matched
control, using construction rather than outcome as the label. Outcome as a label would
make the probe a failure predictor wearing another name.

## Context — where this question comes from

The taxonomy and ordering below were not derived from `10-foundations/04`, despite
this sheet's own header saying it feeds that document's failure modes. `04` names
four modes — Insufficiency, Redundancy, Uselessness, Overload — with no
`contradiction` or `false-premise` category and no cross-mode ordering. E1 borrows
`04`'s Overload concept and, more importantly, its diagnosis of Overload's
circularity risk (a probe trained against "the model could not handle it" is a
failure predictor wearing another name — `04`'s framing, restated below). But
`04` supplies neither the other four categories nor an ordering between them.

The actual design lives in `70-THINKING/00-standing-position.md:200-249`. Two
things feed it:

- **`70-THINKING/08-when-to-stop/18-agentic-abstention.md`** (litreview on Luo,
  Wen & Wang, "Agentic Abstention") groups *false premise* and *contradiction*
  together as one sub-type of request-based abstention — the closest external
  antecedent for treating them as a related pair. The paper does not rank them
  against missing/overloaded context; that ranking is not sourced from there.
- **The standing-position construct-validity table**
  (`standing-position.md:210-216`) scores each candidate stress class on four
  criteria — ground truth by construction, sharp binary, cheap matched pairs,
  distinctive signature — and that table *is* the reasoning for the ordering:
  contradiction and calculus score high on all four; missing-context was
  upgraded (2026-09-04) once a "failed binding" attention signature was argued
  for absence rather than dismissed as signature-free; overload stays
  low because its signature is diffuse and dose-dependent and it risks the
  circularity `04` already flags; false-premise is placed last because it is
  explicitly semantic — "the established blind spot" a structural probe should
  not be able to see, which is what makes it the ordering's designed falsifier.

**No finding in `50-findings/` tests or supports this ordering.** The false-premise
hits in the M4–M7 findings are about whether orchestrators/judges correctly
*decline* false-premise tasks by reasoning about them — a different question from
whether a processing-level probe can *see* the four pathologies at different
resolutions. The ordering is a pre-registered hypothesis, argued once from
first-principles probe-construct design, not an empirical regularity carried
forward from prior runs. That is consistent with E1's own status (`not run`) —
closing that empirical gap is what this experiment is for, not something it can
presuppose. M9's spec (`01-MILESTONES/09-context-governance-measurement.md`)
imports `04`'s four-mode taxonomy for what it *measures* and separately
name-checks E1 as attacking the same construct problem from the probe side, but
does not reconcile the two vocabularies — a terminology gap worth closing before
E1's results are read against M9's metric.

## First move — validate context blur before building the probe

The ladder/probe apparatus below is expensive and its construction is not yet
solved: an honest grain-match design needs representations that are token-matched
and sufficiency-matched without being confounded by format, and neither
invariant is free to build (see the operator's working notes, 2026-09-15 — size
can only be matched by padding the shorter arm with filler validated inert by a
calibration run; content can only be matched as *entailed sufficiency*, not
literal equivalence, since coarsening is lossy by construction; format is only
held fixed by generating both arms from one canonical state through matched
templates, not by hand-writing a raw document and a summary of it). None of that
is built yet.

**A narrower, already-partly-evidenced claim can be checked first, from data
already recorded, at effectively no cost:** the "context blur" mechanism named
above the failure-mode table — degradation under load is not global failure, it
is **selective silent omission biased toward low-salience requirements.** M5's
`wf6` is the one existing data point: monolith drops docs+TODO under load (0/4,
0/3) while the tasks bundling those requirements still deliver their core
objective. One task, one arm — suggestive, not validated.

**What validating it needs, none of it new apparatus:**

1. **Per-requirement outcomes, not `objective_pass`.** Read the structural
   dimensions (`DOCSCORE`, `TODOSCORE`, `SUBTESTS`, etc.) individually rather than
   collapsed into the gating exit code — the same fix E0's defect 1 already
   requires, shared rather than duplicated.
2. **An existing load variable**, not an invented one — context size, concern
   count, the suite's own `stresses` tags — regressed against per-requirement
   pass/fail across the recorded M6/M7 corpus.
3. **The discriminating prediction:** low-salience requirements' pass rate should
   fall **faster** than the core deliverable's as load rises, and the drop should
   be **selective** — some requirements vanish while others hold — not a uniform
   decline across all of them. Uniform decline is ordinary overload/noise, not
   the blur mechanism this claim is naming, and would say the effect does not
   generalise past the one `wf6` anecdote.

This is answerable now, from runs already on disk, the same way E0's three
defects were — and it should run **before** any resource goes into the ladder,
since a negative result here (uniform decline, or no selectivity pattern outside
`wf6`) would mean the probe's target class needs rethinking before its apparatus
is built.

## The hypothesis is an ordering, not a cell

Fixed in writing before any data exists:

> calculus — contradiction > missing-context > overload > false-premise — chance

Two consequences follow from the hypothesis being the ordering. It **degrades
gracefully**: a weak apparatus shrinks every score while the ordering may survive. And
**the arm ranked last is the most informative** — false premise is the predicted null,
and a predicted null returning positive would overturn the structural-versus-semantic
boundary the whole account rests on.

## Design

One battery, not four experiments. Same apparatus, same model, same base tasks; five
stress classes with matched present/absent pairs.

**Calculus runs first as a positive control** and contributes no evidence about the
hypothesis. If the probe cannot detect arithmetic error, nothing downstream is
interpretable.

## What a null means — two different nulls

- **Everything near chance:** the apparatus is broken. Says nothing about context
  pathology.
- **Everything equal and above chance:** the probe detects *something is wrong*
  generically. That is a failure detector, not a pathology classifier, and the
  distinction matters because the four failure modes call for different responses.
