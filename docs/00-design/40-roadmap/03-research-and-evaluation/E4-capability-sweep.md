# E4 — Does each role's mechanism work, and how far?

**Status:** not run. Preparation opened 2026-09-22; re-scoped to the mechanism
layer the same day.
**Layer:** 2 of 3 — **mechanism**. See [`README`](README.md) for the layer split.
**Gated on:** E0 — **satisfied 2026-09-17**, and the answer constrains this sheet
rather than merely unblocking it: the suite is **not unidimensional**, parallel
analysis retains **two** factors, and E0 defect 1 is still open. A sweep across
sizes on a two-factor instrument reports movement on a composite, so arm
ordering here is read per factor or not at all.
**Related:** [`E5`](E5-skill-scales.md) asks whether skills predict these
mechanisms; [`E3`](E3-functional-requests.md) asks whether these mechanisms
compose into a system that serves a request.

## The question

A **mechanism** is what one role does that the architecture depends on. This
sheet asks, per role and per mechanism: does it work, how far does it go, and
how does that move with **size and tuning — not size alone**.

## Why the design must vary both

Tuning reshapes results unevenly across domains, so a size-only design cannot separate
a capability effect from a tuning artifact. A sweep that varies size and holds tuning
uncontrolled will report a capability curve that is partly a tuning curve, and nothing
in the result says which part.

## What a null means

Flat across sizes, with the instrument validated, is a strong result: it says the
mechanism under test is one the models do not differ on, which bounds what any
scaffold built on it can ever buy.

## What is held constant, and therefore what this layer is blind to

The former `E5-population-spread` measured the operator and made the general
point: *every experiment that holds the operator constant scores the system
minus the person using it.* Each layer must now state what it fixes.

This layer fixes **the rest of the system** and varies demand on one mechanism.
It is therefore blind to **composition** — mechanisms can each score well and
the assembly still fail, which is what `70-THINKING/02` predicts if aggregation
rather than execution is the binding constraint. That gap is E3's to find, and
nothing measured here would reveal it.

## The roles and their mechanisms

One subsection per role, one subsubsection per mechanism. First inventory,
2026-09-22, taken from what M7 actually runs plus the roles the architecture
needs and does not yet have. **Three of nine are not implemented, and the
firing rules consume their outputs.**

| role | mechanisms | evidence status |
|---|---|---|
| implementer | execution; convention inference; scope adherence | measured functionally only |
| premise auditor | premise evaluation; unsoundness depth | `s1` fires; parse rate measured |
| concern splitter | decomposition; sub-objective authoring; objective preservation | wf6 2/6 → 6/6, never isolated |
| judge | evidence weighing; verdict calibration; instruction formulation | `50-findings/14` measured the *contract*, not the judgement |
| test synthesiser | discriminator authoring | `test_synth` arm exists |
| orchestrator | **fit self-assessment**; firing decision; termination | **firing rule is hand-set — NYI**, and gated on E5 |
| context assembler | relevance discrimination; sufficiency estimation | M9, partial — dloop took cross-file 0.47 → 0.92 |
| aggregator | recombination under imperfect inputs | **NYI** — `70-THINKING/02` calls it the binding constraint |
| knowledge curator | retention; retrieval; use of knowledge not derived in session | **NYI** — M8, E6 |

Each subsection is still to be written, one per discussion. The inventory is
the settled part; the per-mechanism designs are not.

---

# Preparation

*The sections below were written for the sweep as a whole and apply to all
three layers. They stay here because this is the layer whose items are most
expensive to author; [`E3`](E3-functional-requests.md) and
[`E5`](E5-skill-scales.md) refer to them rather than restating them.*

## Preflight — the one run that can cancel the rest

**Before any of the below is built, run the existing 34 tasks once, n=1, on the
largest model available.**

If it passes 32 of 34, the suite is **exhausted at that scale** and every
comparison run on it afterwards is noise: a scaffold buying three rungs and one
buying six both read as "passed everything." That is a ceiling effect on the
*instrument*, named in `70-THINKING/02` as the thing that would silently cap
this project's own output metric, and it collapses both of E0's factors at once.

This costs one run and it decides what the rest of this sheet is for. A high
score means new items are required and tuning the old ones is wasted effort; a
middling score means the suite still discriminates and extension is the cheaper
path. **Do not skip it because the answer seems obvious** — the whole point of
the two-population design below is that the answer determines which population
needs building.

## What travels

**Assume the repo goes to a machine with no network access**, runs there, and
returns artifacts that are investigated and only then pushed
(`40-roadmap/00-backlog.md`, 2026-09-15). A forge push is not how an experiment
is packaged.

What that forces, in the order it bites:

- **Weights travel in the archive.** Not a pull script. Demonstrated
  2026-09-22: ollama refuses the redirect Hugging Face's xet-backed CDN issues
  — `blocked redirect to a different host` — for both the `nvidia/` and
  `unsloth/` repos, and that is ollama's own check, not a sandbox's. The
  registry copy worked. On an air-gapped host neither route exists, so the
  blobs and the Modelfiles ship together and the archive is verified by loading
  them, not by listing them.
- **The pool and the store travel as directories**, which is why they are
  directories (`evalkit/pool.py`). No daemon, no database, no service to stand
  up on the far side. An interrupted sweep repatriates and resumes.
- **Everything the run needs to identify itself travels with it.** The setup
  key resolves `arm_sha`, `prompt_sha` and `fixture_sha` from files in the
  repo, so a partial archive silently produces different cells rather than
  failing. Hash the archive on both sides.
- **Nothing is fetched at run time.** Any task fixture that would install a
  package, clone a repo or hit an API is disqualified as an item, whatever else
  recommends it. This is a selection criterion for the corpus below, not a
  deployment detail.

## What is collected, and what makes it eligible

The sweep is expensive and runs once. Everything below is recorded **by
default**, because the runs worth re-reading are the ones nobody expected to
need — established the hard way on 2026-09-22, when 1,513 reps on disk could
not answer why a judge emitted no JSON in 18% of calls.

| | where | why it is not optional |
|---|---|---|
| scored row | `evalkit_store/rows/<cell>.jsonl` | the result |
| **setup key** | the cell id the row is filed under | see the rule below |
| **raw generations** | `evalkit_store/transcripts/<cell>/<rep>.jsonl.gz` | prompt, response, thinking, `done_reason`, token counts. ~51x compressed; a sweep is megabytes |
| stage records | `stage_influence_<arm>.jsonl`, stamped with model and judge format | the judge's verdict and per-condition reasoning |
| timings | `gen_s`, `prompt_s`, `wall_s`, `llm_calls`, `runner`, `t_start`, `t_end` | separates decode from prompt from queueing from harness; lets concurrency be reconstructed rather than declared |
| pool records | `done/<cell>.<rep>.json` | who ran what, when, and what was released |

**The eligibility rule, which is the load-bearing one:**

> **Data is eligible for reuse only if its setup was RECORDED at run time, never
> inferred afterwards.**

`provenance: recorded` means the harness wrote the setup because it knew it.
`declared` means a human supplied it from a migration manifest. The two are
never pooled silently, and a waiver naming one field with its evidence is the
only bridge between them.

The reason is measured, not theoretical. Stage records written before
2026-09-21 carried neither the model nor the judge format, and recovering them
by joining on `(arm, task, rep, terminal, wall_s)` put one cell at **+22.7
points where the answer was +4.3**. The join was later validated at 100%
accuracy against 856 stamped records and the corrected numbers stand — but that
validation only existed because a fix landed mid-sweep by accident. **An
instrument needs a channel that can tell you it is lying, and it has to be
built before the measurement.**

For this sweep that means: no item runs whose cell cannot be resolved from the
archive alone.

## Test specifications

### The standing decision: borrow the bug-fix family, build the rest

Directions 1–3 below are SWE-bench-shaped. Building them here means fewer items
and unproven checks, and **a wrong check is worse than a missing item** — it
injects correlated noise into the response matrix, and correlated noise is
indistinguishable from a factor (`70-THINKING/02`). A cluster of subtly broken
checks presents as a clean, spurious dimension.

This project's asset is not the tasks. It is the instrumented comparison: setup
keys, the store, per-cell transcripts, the judge arms, reps with intervals, a
pool that survives being killed. **Borrow 1–3 as anchors; spend the authoring
effort on 4–6, which no corpus covers and which test things this project's own
design documents call load-bearing and unmeasured.**

Borrowed items still have to pass the air-gap rule above and be re-checked
against our own held-out mechanism; a borrowed task is not a borrowed check.

### What every specification must carry

Inherited from the M6 contract and extended for tool use:

- **fixture** — a workspace reset per rep, hashed into `fixture_sha`
- **objective** — the request as given, including the false ones
- **protected set** — files restored before scoring, so editing the test is not
  a route to passing
- **visible check** — stdlib, deterministic, under a second
- **held-out check** — never shown, never in the workspace during the run
- **budget** — maximum tool calls and wall time, recorded whether or not hit
- **trajectory** — every tool call, its arguments and its result, in order

The last one is the tool-calling analogue of the transcript rule: **you cannot
verify a path you did not record**, and at these model sizes the interesting
failures are in the path rather than the final state.

### The held-out check does three jobs

Stated separately because it is the single highest-value mechanism here.

> **Author the bug so that the obvious fix passes the visible test and fails the
> held-out one.**

1. **It operationalises "harder."** Without it, hard means "the author found it
   hard", which is the same weasel as *principally* elsewhere in this project.
2. **It detects cheating.** Editing the test, deleting the assertion, adding a
   skip, patching the symptom — all pass the visible check and fail the
   held-out one identically. One mechanism, no separate cheat detector.
3. **It survives tool access**, which the M6 contract's assumptions do not: a
   model with a shell can reach anything in the workspace, so the only honest
   check is one that was never in it.

### The six directions

| # | direction | measures | check | source |
|---|---|---|---|---|
| 1 | add a basic feature | navigation, convention-following | new tests pass | **borrow** |
| 2 | fix a basic error | localisation | red → green | **borrow** |
| 3 | fix a harder bug | depth of understanding | red → green **+ held-out** | **borrow the task, author the held-out check** |
| 4 | change + docs + CI | objective retention, **aggregation** | three independent structural checks | **build** |
| 5 | dig a large corpus, then implement | retrieval under volume | feature works | **build** |
| 6 | diagnose a failure from logs | inference from evidence | structured claim, exact match | **build** |

**1 and 2 are anchors, not discriminators.** They will saturate at 70B, and
that is their job: they hold the bottom of the difficulty scale so that ability
and lift stay estimable above it. An item set that tops out near the subject's
ceiling cannot tell a good scaffold from a great one.

**5 is the one to build first, and it looks the least like real work.** It is
the only direction with a **controllable difficulty dial**: hold the task fixed
and vary how much documentation surrounds the fact needed to do it. Everything
else is authored at a difficulty and hoped over. That dial scales to the next
model without re-authoring, and it is one step from the **grain-match test**
that `70-THINKING/02` calls its single live discriminator and that has never
been run —

- **arm A**: raw corpus, *N* tokens, provably sufficient
- **arm B**: the same content pre-abstracted, *N* tokens, provably sufficient

If A ≈ B, the granularity hypothesis collapses into "relevant context beats
maximal context" wearing a hat, and that document says so itself. The answer
falls out of building a task type wanted anyway.

**4 tests the failure the design set says is binding.** `70-THINKING/02` argues
aggregation, not execution, bounds the integrated system ceiling, and that
**tangential success** — every sub-task done well, the objective dissolved — is
the characteristic failure. Neither has ever been measured here, because every
existing task is too short to drift. Scoring stays structural: does the
docstring name the new parameter, does the changelog carry an entry, does CI
actually run the new test. No judge required.

**6 needs its scoring inverted to be checkable at all.** An explanation as
output puts the measurement back on prose judging, which `50-findings/14` found
returning **zero** unsound-request calls in eight cells of eleven. Instead:
**synthesise the failure so the true cause is known**, and score a structured
claim — which service, which call, which line, what cause — by exact match.
Different faculty from everything else on this sheet, and the one no existing
corpus serves.

## What this sweep can and cannot settle

**Can:** where each model's cost gradient begins, which is continuous and finer
than where pass rates break; whether lift is non-uniform and ordered by
granularity demand (H1) or roughly constant (H2) or absent only on judging
(H3); whether the held-out check separates depth from search luck.

**Cannot:** anything about factor structure at the new scale, because E0's item
analysis would have to be re-run on the new items; and anything about the two
factors it already found, since a sweep across sizes on a composite reports the
composite.

## Cost and gating

- **Preflight** is one run and gates everything else.
- **Directions 1–3** cost item selection and held-out authoring, not task
  authoring.
- **Direction 5** costs a corpus and one fixture; the dial makes it reusable.
- **Directions 4 and 6** cost new check machinery and are third in line.
- **Reps do not get cut to buy items.** Fewer tasks at the same reps, never more
  tasks at n=1. On 2026-09-22 an effect read **+22.7 points at n≈19** and
  **+4.3 at n≈200** — the same cell, the same data, forty times the reps.
  The budget here is a **window of wall-clock time on a machine that is not the
  development host**, so the cost of getting n wrong is not a larger invoice:
  it is the whole window, spent producing a number that has to be produced
  again. An anecdote is not cheaper than a measurement when the machine has to
  be set up either way.
- **Blocked on** the air-gapped packaging item (`00-backlog.md`, 2026-09-15),
  which is the operator's own stated prerequisite rather than a parallel
  concern. Note the backlog entry frames it around a **rented** H100; the
  constraint it describes — archive in, artifacts out, no network in between —
  is a property of the host being separate and offline, not of how it was
  obtained, and this sheet assumes only the latter.
