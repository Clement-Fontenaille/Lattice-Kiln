# E1 — Can context pathology be detected from processing?

**Status:** **first move run 2026-09-17 — negative.** The context-blur claim does
not survive: the motivating anecdote is a global failure, not selective omission,
and exactly one suite task carries a low-salience requirement. The probe battery
remains not run and is **blocked** on an unspecified feature space (below).
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

### Result, 2026-09-17 — the claim does not survive

Run over the recorded corpus. Script and outputs:
[`experiments/E1-context-pathology-probe/`](../../../../experiments/E1-context-pathology-probe/).

**1. The anecdote's numbers reproduce. Its reading does not.**

`monolith` on `wf6_multi` scores `DOCSCORE 0/4`, `TODOSCORE 0/3` in every rep —
exactly as reported. But the same rows carry `final_sub = 2/6` and
`objective_pass = False`.

> **The core did not hold.** The claim requires selective omission — periphery
> dropped *while the core is delivered*. What actually happened is that
> everything failed together. That is ordinary global failure, which this
> experiment named in advance as **not** the blur mechanism.

The framing *"monolith drops docs+TODO under load"* has been propagating through
`10-foundations/04`, `02-capability-as-granularity.md` and this sheet as evidence
for selective omission. The numbers are right and the inference is not.

**2. The claim cannot be tested at corpus scale, because the corpus has one task.**

Of 34 suite tasks, exactly **one** carries an explicitly low-salience requirement:

| task | dimensions |
|---|---|
| **`wf6_multi`** | `DOCSCORE`, `TODOSCORE` |
| `hf_dict_dispatch`, `hf_extract_fn`, `hf_json_serialize`, `hf_rec_to_iter`, `hf_rename`, `wf3_refactor_blindview`, `wf3_refactor_witnessed` | `STRUCTSCORE` |
| `hf_audit_perf` | `AUDITSCORE`, `PERFSCORE` |
| `hf_wrong_spec` | `SPECSCORE` |

`STRUCTSCORE` and friends are neither the gate nor obviously peripheral, and were
excluded from the salience assignment in advance rather than pressed into service
after the fact. So the 69 analysable rows are **69 runs of one task**.

**3. Across those 69 rows, the dominant pattern is global failure.**

| pattern | rows | share |
|---|---|---|
| `both_drop` — core and periphery both fail | **36** | **52%** |
| `mixed` | 19 | 28% |
| **`blur` — core holds, periphery dropped** | **10** | **14%** |
| `both_hold` | 4 | 6% |

The blur pattern exists but is a minority, and the `inverse` pattern is visible
too — `judge_staged` rep1 scores `DOCSCORE 4/4`, `TODOSCORE 3/3` while missing a
subtest, which is selectivity running the other way.

**4. No load proxy predicts the gap.** L1 (requirement count) has no variance,
since there is only one task. L2 (worker view) has no variance. L3 (context
budget, 16384 vs 8192) correlates with the core-minus-periphery gap at
**−0.076** — indistinguishable from zero, and in the wrong direction for the
claim.

### What follows

**The probe's target class needs rethinking, which is what this first move was
for.** Context blur, as currently evidenced, is not established as a distinct
selective mechanism — it is one task where failure is usually global and
occasionally selective, with no dose to point at.

Two concrete consequences:

- **A suite-coverage gap, and a cheap one to fix.** Studying selective omission
  requires tasks that *have* separable low-salience requirements. There is one.
  Authoring more is item-writing, not research, and it is the prerequisite for
  any version of this question — including a controlled dose experiment, which
  does not exist and cannot be built on a single item.
- **The claim should be downgraded where it is cited**, in
  `10-foundations/04` and `02-capability-as-granularity.md`, from an observed
  behaviour to an unsupported reading of a global failure — pending fixtures that
  could actually separate the two.

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

## Open decision, 2026-09-16 — the probe has no specified feature space

**This blocks the battery below, and it is a design decision rather than
something further reading will settle.**

This sheet says *probe* throughout and never says what the probe reads. The
candidates are not interchangeable — they differ in what access they need, what
they could detect in principle, and whether the result transfers:

| candidate | what it reads | note |
|---|---|---|
| **attention weights** | entropy/peakedness of attention from query tokens to context | matches the "failed binding — diffuse rather than peaked" language this sheet's own ordering rests on. But attention-as-salience has a standing literature against it |
| **hidden-state activations** | a light classifier over layer activations | the classical sense of "probing classifier". Model-specific coordinates; see `02-capability-as-granularity.md`'s white-box section |
| **output logprobs** | entropy of the next-token distribution | no internal access needed, cheapest, and the weakest — it measures the model's epistemic state, which is empty under confident wrongness |

Nothing in the battery can be designed until one is chosen, because the matched
present/absent pairs have to be scored *by something*. Recorded here as an open
decision with a date rather than left implicit in the word "probe".

## What a null means — two different nulls

- **Everything near chance:** the apparatus is broken. Says nothing about context
  pathology.
- **Everything equal and above chance:** the probe detects *something is wrong*
  generically. That is a failure detector, not a pathology classifier, and the
  distinction matters because the four failure modes call for different responses.
