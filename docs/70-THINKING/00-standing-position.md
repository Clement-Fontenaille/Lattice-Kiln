# Standing Position

**Updated:** 2026-09-04
**Purpose:** the anti-circling artifact. What is settled, what is open, what would
kill what, and what to run next — across threads `01`, `02`, `03`. Thread `04`
(praxis) is open and has settled nothing yet; it is not covered here.

Read this first. If something here is relitigated without new evidence, that is
the circle this document exists to break. If something here is **wrong**, change
it here rather than arguing it again in a thread.

> **Standing rule (2026-09-04): every ranking in this document is a claim, not a
> schedule.**
>
> This document is full of ordered tables — probe targets, corpus candidates,
> artifact spectra, implement/interface/delegate. Each was produced by intuition
> and each *reads* as a plan. Running only the top rows confirms the intuition
> without ever risking it, and the ranking silently becomes an unexamined premise.
>
> **Where testing the whole set is affordable, test the whole set** — the rows
> predicted to fail are what make the ordering falsifiable, and the row ranked
> last is often the one that can kill the framework. Where it is not affordable,
> say so explicitly and record the ranking as an **untested assumption** rather
> than letting it pass as a finding.
>
> First application: E1 below.

---

## 1. Goals of the thinking

Not the project's goals — these threads'.

| | goal | state |
|---|---|---|
| **G1** | Decide what the system is *for*: which work, whose, at what unit | substantially answered (`01`) |
| **G2** | Decide whether *capability = granularity ceiling* is a usable frame or should be dropped | **open** — currently a lens, not a theory (`02`) |
| **G3** | Know where the field stands, so nothing is rebuilt or re-derived | **done** (`03`) |
| ~~**G4**~~ | ~~Produce a measure that accumulates across milestones~~ | **Demoted 2026-09-04 from goal to hoped-for byproduct — see below** |
| **G4′** | Build a **benchmark for a skill out of a set of scales**, capturing something more robust than the scales measure separately | **the actual challenge.** Open, and the psychometric literature is the relevant prior art |

### G4 — where it came from, and why it is demoted

**Provenance, stated plainly: G4 was authored in this session by Claude, not
sourced from the charter, the roadmap, or any finding.** It began as an
observation — that the lift framing supplies a unit that accumulates — and was
then promoted to a *goal* without that promotion being flagged. That is exactly
the move this folder exists to catch, so it is being unwound here.

**Its one legitimate root** is real and should be kept: **M15 cross-generation
benchmarking** requires commensurable measurement across system generations. That
is a genuine future requirement. Everything beyond it — "the findings log stays a
series of one-offs", "a unit of progress" — was inference stated with more force
than the root supports.

**Is it sound to drop?** Yes, as a goal. Four reasons:

- **It is premature.** Designing the currency before the economy exists. G2 is
  unresolved; a unit for an unvalidated construct is decoration.
- **Nothing blocks on it.** No experiment in §5 needs rungs to be a *unit* —
  every one works on raw per-ladder scores.
- **It invites Goodharting the project's own measure**, which `30-adaptation/04`
  warns about specifically.
- **Under G4′ it is redundant anyway.** A latent-trait estimate *is* a
  commensurable measure by construction. Commensurability falls out of the
  construct-validity work or it does not arrive at all — wanting it does not
  produce it.

**Kept as:** a byproduct to notice if it appears, and a note that M15 will
eventually need it. Not a thing to pursue.

### G4′ — the real challenge, and what it actually needs

> **Build a benchmark for a skill from a set of scales, capturing something more
> robust than what the scales measure separately.** On success, work out how it
> integrates with the task-granularity idiom and the system loop.

Individual ladders are **indicators**, not measurements. The thing of interest is
estimated from their *joint pattern*. That reframing dissolves two of the three
conditions previously listed under G4:

- ~~**Rungs comparable across ladders.**~~ **Withdrawn — never needed.**
  Calibration does not presuppose homogeneity. If a ladder is too coarse for a
  model, insert an intermediate rung; if its ceiling sits too low, build a harder
  one. Both are *local* refinements. Cross-ladder aggregation was imported from an
  industrialisation phase that has not arrived and may never be this project's
  problem. It is also unnecessary in principle: latent-trait methods handle items
  on unrelated difficulty scales natively — that is what they are for. This
  likewise retires the worry that tuning-divergence threatens comparability; it
  threatened a requirement that does not exist.
- **Rungs stable across model generations.** *Retained as a real risk*, but only
  where cross-generation comparison is actually being made (i.e. M15). If a new
  model changes a ladder's **shape** rather than position on it, comparison breaks
  silently. Cheapest check: re-run an old ladder on a new model and look for
  *disproportionate* gains at particular rungs rather than a uniform shift.
- **The operator-skill axis must be operationalised** — expanded below, since it
  was too compressed to be actionable. **But note it is now the smaller half of
  something larger:** the axis is the adopt-or-stratify question, and the
  commitment behind it has been **promoted out of this folder** to
  `00-design/10-foundations/07-the-integrated-system-and-its-operator.md`.
  Dispersion is *one attempted measurement of it*, not its definition, and the
  design commitment must not be compressed into the benchmark.

**What G4′ needs that does not exist yet: the tools.** Item analysis,
dimensionality checks, difficulty targeting near p≈.5, and whatever refinement of
these suits a setting where "subjects" are model configurations rather than
people. These have to be built and discussed, not assumed. This is the same
machinery **U0/F5′** needs, so it is one tooling effort serving both.

### The operator-skill axis, unpacked

The dispersion metric is *outcome variance across operator skill*. Measuring it
needs at least two **defined** operator behaviours, and "naive arm" named none —
which matters, because you can manufacture any spread you like by choosing a
weaker naive arm. Without pinning it, the number is not reproducible and not
comparable to itself later.

"Operator skill" here is not a person. It is **a set of behaviours at the
interface**, and at least five things vary independently:

1. how the request is phrased — one vague line vs. a precise objective;
2. whether relevant files are named or the agent must find them;
3. whether constraints, prior context and done-criteria are supplied;
4. whether the operator iterates mid-run or accepts the first output;
5. whether the operator has configured the scaffold at all — hooks, rules, gates.

A workable first definition, both arms against the **same** model and scaffold:

| arm | definition |
|---|---|
| **naive** | the task's user-facing request **verbatim**; no file hints, no constraints, no done-criteria; accept the first terminal output; no scaffold configuration |
| **expert** | hand-authored objective, named files, stated constraints and done-criteria; up to *N* corrections; scaffold configured |

The M6 suite may already contain both halves — each task carries a realistic
request (naive-shaped) alongside documented discriminators and subtests
(expert-shaped) — so construction could be cheap.

**One contamination risk to design around:** the expert arm must be
*expert-in-process*, not *expert-in-this-task's-answer*. An operator who knows the
solution is not measuring skill, and would make the floor look far higher than it
is.

---

## 2. Premises — held, with why and how firmly

Held means: **do not reopen without new evidence.**

| | premise | strength | basis |
|---|---|---|---|
| **P-a** | Entropy reduction is the product, not throughput | **strong** | M6 internally; Faros / CircleCI / LinearB externally, large magnitudes |
| **P-b** | The deliverable is insight, not a tool | **decided** | a choice, not a finding. Not falsifiable; revisit only if the purpose changes |
| **P-c** | Local-first is non-negotiable | **settled** | institutional constraint, not a preference |
| **P-d** | More *true* context can degrade outcomes | **strong** | Aider + Cursor docs, Sourcegraph 100K-vs-5K, ETH context files, and already project doctrine (`10-foundations/04`) |
| **P-e** | Decomposition has a cost that can exceed its benefit | **strong** | M4 fixed chain, concern-split at 252 s, SDD in the field, ADaPT's own failure catalogue |
| **P-f** | A 7B cannot hold the judging seat | **strong locally, untested against capability** | judge-lab; no framing lifted it. Whether it is capability-bound is U1/U2 |
| **P-g** | Overload and oversize are **relations** between input and capacity, not properties of input | **settled by argument, 2026-09-04** | same input, opposite verdict across model sizes. Consequence: labels are per `(model, context)`; probes train per model |
| **P-h** | dloop is **half** the field's remedy | **settled** | it solves shipping-broken and doing-unneeded; it does not touch reviewability, upfront understanding, or comprehension over time (`03`) |

---

## 3. Uncertainties — ordered by how much they gate

| | uncertainty | gates |
|---|---|---|
| **U0** | **Is the M6 suite measuring one coherent thing?** | everything that uses the suite as a ruler — which is most of the plan |
| **U1** | Is the granularity frame a theory or a vocabulary? | G2, and whether `02` survives at all |
| **U2** | Does a **grain** effect exist independent of **amount**? | U1 directly. Nobody has separated them |
| **U3** | Does load show in processing independently of whether the model represents it as uncertainty? | the entire white-box direction. **Reclassified 2026-09-04: this is a hypothesis, not a premise** |
| **U4** | What is the Amdahl split on real requests? | the 15× claim, and which use case is worth building |
| ~~**U5**~~ | ~~Can the ticket corpus be used at all?~~ **CLOSED 2026-09-04: no, permanently.** Not via incorporation, not as flagged-public findings, not as remote logs | resolved into **E-corpus** — find a corpus of the same shape |
| **U6** | Does the ceiling bind on decomposition, or on **aggregation**? | route (b) — whether conceptual work is reachable by decomposing |

---

## 4. Falsifications to attempt

Each is stated so it can lose. Where pre-commitment is required, it is named,
because pre-commitment is the part that costs something.

| | claim under test | what kills it |
|---|---|---|
| **F1** | grain ≠ amount | token-matched, sufficiency-matched, grain-varied arms come out **equal**. Then the whole account collapses to *"relevant beats maximal"* and should be retired to that sentence |
| **F2** | capability moves the ceiling in a granularity-ordered way | a **flat % lift** across granularity classes (→ plain capability), or **lift everywhere except judging** (→ approval bias is a training artifact). Requires **size × tuning**, not size alone |
| **F3** | processing carries a load signature | a probe cannot separate a **constructed** stress from its matched control above chance — *using construction, not outcome, as the label* |
| **F4** | the scaffold is packaged, not taught | dispersion across operator skill does **not** decline as scaffolding improves |
| ~~**F5**~~ | ~~a ladder measures one ordered quantity~~ | **Withdrawn 2026-09-04 — not a real falsifier.** A ladder is ordered *by construction*; monotonicity is close to guaranteed if the rungs were built correctly, so it tests the builder, not the instrument. Replaced by **F5′** |
| **F5′** | a ladder's items **cohere** — they are indicators of something, not a list of unrelated tasks | standard item analysis fails: **item difficulty** collapsed (items all at p≈0 or p≈1 carry no information; informative items sit near **p≈.5**), **item–total correlation** near zero (an item that does not track the total is not measuring the same thing), or **dimensionality** showing several unrelated factors where one was claimed. Same machinery as **U0**, applied to a different item set |
| **F6** | the structural-vs-semantic boundary is real — probes see input structure, not semantic truth | the **predicted ordering** of E1's stress classes fails. Two ways: **false premise shows signal** (the boundary is wrong), or **all classes score equally** (it is a generic failure detector, not a pathology classifier). Requires running the arms predicted to fail |

---

## 5. Experiments — ordered by information per unit cost

### E0 — Is the M6 suite coherent? *(cheapest; may need no new runs)*

Construct validation before anything uses the suite as a ruler. Possibly
answerable from **runs already recorded**. Gates E2–E5.

### E1 — Contradiction probe *(the win-condition first experiment)*

**Why not overload first, despite it benchmarking easily.** Overload's ground
truth is *"the model could not handle it"* — so a probe trained against that label
is **a failure predictor wearing a different name**. There is no construct
independent of the outcome it is meant to predict. That circularity, not signature
instability, is the disqualifying problem.

Criteria for a good first target, and how the candidates score:

| target | ground truth by **construction**? | sharp binary? | cheap matched pairs? | distinctive signature expected? |
|---|---|---|---|---|
| **contradictory requirements** | **yes** — you authored the conflict | **yes** | **yes** — append one conflicting clause, hold all else fixed | **yes** — two incompatible targets held at once is structurally unlike ordinary difficulty |
| **missing context** *(upgraded 2026-09-04)* | **yes** — you removed the referent | **yes** | **yes** — same task, referent present vs absent | **yes, via failed binding** — see below |
| calculus / arithmetic | yes | yes | yes | yes, but **domain-specific**; weak transfer to code work. Its role is a **positive control**, not a result |
| overload | only if the **dose is constructed** (append a known distractor block) — which does rescue it | no, graded | yes | dosage-dependent, diffuse |
| false premise | yes | yes | yes | **no** — semantic; the established blind spot |

**Missing context, reconsidered.** An earlier draft dismissed it: *"absence has no
direct signature."* That was wrong about where to look. **A sound request is
expected to resonate with its context** — so the signature is not the absence,
which is indeed nothing, but the **failed binding**: a referent with nothing to
ground against still produces an attention pattern, a diffuse or self-attending
one rather than a peaked one. A null result is a result; `grep` finding nothing
still exits with a code.

This is also **the strongest available argument for probing internals at all.**
If every pathology were visible in the input, the right tool would be a linter.
Missing context is precisely the case the text cannot show and the processing can.

*Its specific risk is confabulation:* if the model grounds to something
plausible-but-invented, the binding succeeds spuriously — the M4 case exactly.
Whether retrieval-like binding and generation-from-prior are distinguishable is a
hypothesis, not an assumption.

**Run all of them. The table above is an intuition, and a schedule that runs only
its top rows never tests it** (decided 2026-09-04).

Running contradiction, getting signal, and stopping confirms the prediction
without ever risking it. The table becomes evidence only if the arms it predicts
will fail are actually run.

This changes the design from four experiments into **one battery with a
pre-registered predicted ordering**: same probe apparatus, same model, same base
tasks, five stress classes × matched present/absent pairs.

**Pre-registered prediction — written before any data exists:**

> detection quality: **calculus ≈ contradiction > missing-context > overload >
> false-premise ≈ chance**

**The ordering is the hypothesis.** No single cell is. This has two properties
worth having:

- **It is robust to a mediocre apparatus.** If the probe is weak, every score
  shrinks but the *ordering* may survive. An ordering claim degrades more
  gracefully than a threshold claim.
- **It inverts which arm matters most.** *False premise is now the highest-information
  cell in the design*, not the one to cut. It is the predicted null, and a
  predicted null that comes back **positive** falsifies the structural-vs-semantic
  boundary this whole document has been building on. The arm ranked last is the
  only one that can kill the framework.

**Two distinct negative outcomes, which mean very different things:**

| result | reads as |
|---|---|
| all arms near chance | the apparatus does not work — E1-control should already have caught this |
| all arms **equal and above chance** | the probe detects *"something is wrong"* generically. **You have a failure detector, not a pathology classifier** — which is the overload-circularity worry, generalised, and now measured rather than argued |

**Price of the design:** the ordering must be **fixed in writing before any data**,
with the same discipline F5 demands of rung order. Otherwise post-hoc
reinterpretation ("missing context was always ambiguous") absorbs any result.

Contradiction still leads the *build* order, because its signature is a presence
rather than a non-event and it is on the critical path for the use case —
contradictory requirements are a frequent real ticket pathology, and detecting
them **is** decline-with-payload (`01` P8/OQ-7, and `03` §1's unoccupied space) —
but leading the build order is not a reason to stop there.

### E1-control — calculus as a positive control *(runs first, proves nothing)*

Not a question about feasibility. The apparatus **does not exist yet**, and a
known-answer target is what tells you cheaply that it is broken *before* spending
on the substantive target. Standard positive control: if the probe cannot detect
arithmetic error, the pipeline is wrong and nothing downstream is interpretable.

It is scheduled first and contributes **no evidence about the hypothesis**.

**Note this experiment tests U3 (F3), which was until today miscarried as a
premise.** *"Load shows in processing regardless of whether the model represents
it as uncertainty"* is the hypothesis under test, not a result standing behind it.

### E2 — Grain-match test *(F1)*

Token-matched, sufficiency-matched, grain-varied. `02`'s one live discriminator
and unrun by anyone in the field.

### E3 — Ladder v1, indirection *(F5)*

Pre-registered rung order and monotonicity tolerance, with the no-rebuild
commitment recorded before any data exists.

### E4 — Capability sweep on the existing suite *(F2)*

Size × tuning. Gated on E0.

### E5 — Operator-dispersion *(F4)*

Hold model and suite fixed; vary operator skill. Measures the **floor**, which
rungs cannot see.

### E-corpus — a substitute for the ticket corpus *(U5 is closed: no)*

**U5 resolved 2026-09-04: the ticket corpus is out of reach, permanently.** Not
via incorporation, not as flagged-public findings, not as remote logs. Plan
around it; do not revisit.

A substitute needs the same *shape*: natural-language problem reports from
non-expert users against a technical system, with recorded ground truth, and a
mix of real defects, user error, duplicates and under-specified requests.

| source | what it gives | cost | domain match |
|---|---|---|---|
| **GitBugs** (2025) — [av9ash/gitbugs](https://github.com/av9ash/gitbugs/) | 150k+ reports, 9 projects (Firefox, Cassandra, VS Code), GitHub+Bugzilla+Jira, **standardised fields and predefined train/test splits**, duplicate rates, resolution times | **lowest** — off the shelf | general software |
| **The validity corpus** — >700k reports, 4 OSS communities, 10+ yrs | the **exact three-way taxonomy**: valid / duplicate / insufficient-information. This is precisely *"plausible culprit is X, but provide Y"* | low–medium | general software |
| **Spack / EasyBuild trackers** | user-reported **build and environment failures** against config-as-code, thousands of users. No published dataset; mine `spack/spack` issues by label via the GitHub API | medium — needs mining | **closest to the real distribution** |
| **Debian BTS** (`bugs-mirror.debian.org` + UDD) | richest triage semantics — `moreinfo`, `unreproducible`, `wontfix` tags plus a **merge graph** standing in for duplicates. No resolution enum; labels derive from tags. MSR 2010 documents the pipeline's traps | medium–high | general packaging |
| **De-triaged M6 tasks** | take a well-formed suite task and rewrite it as a vague user complaint. Ground truth is known **because you started from it** | lowest | synthetic — a **matched control**, not a substitute |

**Recommended path:** GitBugs to start moving immediately; **Spack** as the
domain-matched corpus that actually resembles the target distribution; de-triaged
M6 tasks as the controlled arm alongside either.

**The caveat that matters.** These are bug reports against **public open-source
projects**, not support tickets against a facility. The distributions differ in
exactly the place that matters: a large share of real facility tickets are *"the
user did something wrong in their own environment,"* a class OSS trackers
under-represent because such reports get closed immediately or never filed.
**Spack is the closest available match precisely because build and environment
failure *is* that class.**

Related and worth reading regardless: an arXiv paper on **LLMs as packagers of
HPC software** uses Spack build outcomes as evaluation signal — 19.7 % install
success zero-shot, ~82.9 % with an error-aware repair loop. An existing
HPC-domain agentic benchmark with deterministic ground truth.

---

## 6. Hanging issues

Real, unresolved, **not yet actionable** — recorded so they are not rediscovered.

- **Aggregation above the ceiling** (U6). ARIES reports 4.12× deterioration on
  one synthetic task, aggregation-dominated (distant domain — mechanism transfers,
  multiplier does not); aggregation is coarse-grained by construction. No
  experiment designed. A ladder measuring only decomposition measures the easy
  half.
- **P8's loop does not close** (`01` OQ-10). Convergence quality cannot be
  evaluated without M9-style context-quality metrics. So M7's front half would
  ship unmeasured — the exact criticism this project levels at the field.
- **White-box collection engineering** — scoped to a separate project, gated on
  the strategy proving sound. Not in this plan.
- **The backlog-as-objective product shape** — the clearest unoccupied space in
  `03`, with no design attached.
- **`01` §2 — external signal** is still empty. Every position in `01` rests on
  one person's experience plus a literature survey.
- **Comprehension debt** — named as not solvable here (`03`). The commitment is
  *do not worsen it, and measure it*. Nothing more should be claimed.
- **Rung stability across model generations** (G4 condition 3). If a new model
  changes a ladder's **shape** rather than position on it, a rung stops being a
  fixed unit and cross-generation comparison breaks silently — which is the one
  thing rungs exist to enable. No detection method designed. Cheapest available
  check: re-run an old ladder on a new model and look for *disproportionate*
  gains at particular rungs rather than a uniform shift.

---

## 7. What would make this document wrong

Stated so the failure is visible rather than gradual:

- **E0 says the M6 suite is incoherent.** Then most of §5 loses its instrument and
  the plan reorders around building a coherent one.
- **F1 comes back null.** Then `02` retires to a sentence and `00`/§3 U1–U2 close.
- **U5 comes back "no."** Then the highest-value use case needs a synthetic
  substitute and loses most of its value; §5 reorders.
- **The stronger model arrives before E0–E2 run.** Then the comparisons are run
  against a moving target and the temporal-validity rules in `03` apply to this
  project's own results, not only to the field's.
