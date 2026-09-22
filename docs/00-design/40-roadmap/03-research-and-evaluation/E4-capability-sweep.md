# E4 — Does each role's mechanism work, and how far?

**Status:** not run. Preparation opened 2026-09-22; re-scoped to the mechanism
layer the same day.
**Layer:** 2 of 3 — **mechanism**. See [`README`](README.md) for the layer split.
**Gated on:** E0 — **satisfied 2026-09-17**, and the answer constrains this sheet
rather than merely unblocking it: the M6 evaluation suite is **not unidimensional**, parallel
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

### How a mechanism is exercised without being isolated

The standing assumption in `70-THINKING/02` forbids probing an operation in
isolation — supplying fixed correct sub-results to measure recombination
constructs a situation that never occurs. This layer stays inside it by a rule
that is easy to state and easy to violate by accident:

> **The role runs in its real position in a working assembly. What varies is
> what the assembly hands it.**

Nothing is stubbed, no stage is replaced by an oracle, and the deliverable is
always the assembly's deliverable. The M7 arms are already built this way —
each is a workflow with named stages, and a stage's input can be varied without
removing the stage.

**A mechanism entry that cannot be exercised this way does not get built.** It
goes on the list with the obstruction written down, which is what happened to
three of the nine below.

### What each entry carries

| field | means |
|---|---|
| **does** | the role's job in the assembly, in one sentence |
| **varied** | what the assembly hands it, and along what |
| **held** | what stays fixed, and therefore what the entry is blind to |
| **read** | the observable, and where it already exists if it does |
| **null** | what a flat result would mean, written before data |
| **draws on** | the `E5` entries expected to predict it — the skill-to-mechanism transfer test |

---

## R1 — Implementer

The only role in `10-technical/06-processor-contract.md` that M4 and M7 both
instantiate directly. Everything else on this sheet either wraps it or is not
built.

### R1.1 Execution

- **does** — turn an objective plus a scope into a change that satisfies it.
- **varied** — the objective's distance from a single coherent edit.
- **held** — context assembly, the check, the scope.
- **read** — `objective_pass` and the structural dimensions, already recorded per rep.
- **null** — flat across the range says execution is not where this assembly's limit is, which would move attention to every other role on this sheet.
- **draws on** — `E5` S6 decomposition, since an objective past one coherent edit is S6's own ladder seen from inside a role.

### R1.2 Convention inference

- **does** — match the surrounding code's conventions without being told them.
- **varied** — how strongly the fixture states its conventions: enforced by a linter, visible in neighbouring code, or present only by implication.
- **held** — the functional requirement, which is satisfiable while ignoring every convention.
- **read** — structural dimensions, which is what they were added for.
- **null** — flat says conventions are followed or ignored regardless of how they are signalled, which makes the signalling work pointless and is worth knowing.
- **draws on** — `E5` S2 relevance discrimination.

### R1.3 Scope adherence

- **does** — change what was asked and not more.
- **varied** — how much adjacent code invites improvement while being out of scope.
- **held** — the objective.
- **read** — diff extent against the minimal correct diff; currently unrecorded.
- **null** — flat says scope is respected or not as a disposition rather than a response to temptation.
- **draws on** — `E5` S4 objective retention.

---

## R2 — Premise auditor

M7 stage `s1_premise_audit`. Advisory: it fires on every task and does not gate.

### R2.1 Premise evaluation

- **does** — judge whether the request is worth carrying out before any work begins.
- **varied** — the depth at which the unsoundness is discoverable, exactly `E5` S3's ladder.
- **held** — everything downstream; the audit's verdict is recorded and the work proceeds regardless, which is what makes this measurable at all.
- **read** — the audit's own output, parsed per rep. Parse rates are already recorded per arm and model.
- **null** — flat says the auditor's output does not track how hard the premise is to fault, which would mean it is producing a disposition rather than an assessment.
- **draws on** — `E5` S3 premise evaluation, directly. **This is the cleanest skill-to-mechanism pair on the sheet** — same demand, one graded end-to-end, one in position — and therefore the first place to run that comparison.

**Standing evidence, and the caution attached.** `50-findings/14` addendum
withdrew the claim that the engineer stage refuses correctly at 83%. That
figure is `declined_correctly`, a harness-side conjunction which
`50-findings/12` records being wrong in this exact direction during an outage.
**What the auditor actually does on false-premise tasks is unmeasured**, and
transcripts now make it cheap to settle by reading whether the refusal is
argued.

---

## R3 — Concern splitter

M7 stage `s2_concern_split`, fired by a hand-set rule.

### R3.1 Decomposition

- **does** — turn one objective into sub-objectives that fit.
- **varied** — how far the objective exceeds a single pass.
- **held** — the executor, the check, and the firing decision, which is R6's.
- **read** — the assembly's deliverable, never the decomposition itself. Grading the artifact requires knowing the right decomposition, which is authorship above the target's effective ceiling.
- **null** — flat says splitting is not what is buying the improvement where improvement is seen.
- **draws on** — `E5` S6.

**Standing evidence:** concern-split took `wf6` from 2/6 to 6/6 and cost 252
seconds to help two tasks in thirty. That is a large effect on one task and a
poor average, and it has never been separated into *when it fires* and *how
well it splits* — which is the R3/R6 division this sheet draws.

### R3.2 Sub-objective authoring

- **does** — write a sub-objective an executor can act on without the parent.
- **varied** — how much of the parent's context the sub-objective must carry to stand alone.
- **held** — the split itself, as produced.
- **read** — executor success per sub-objective, which separates *a bad split* from *a good split badly written*.
- **null** — flat says the writing does not matter once the split is right, which would simplify the role considerably.
- **draws on** — `E5` S1 grain closing.

### R3.3 Objective preservation

- **does** — keep the parent's intent alive across the split.
- **varied** — the number of sub-objectives and the distance between them.
- **held** — executor competence, so that each part can be done well while the whole misses.
- **read** — parent objective satisfied while every sub-objective was; **tangential success made countable.**
- **null** — flat says intent survives splitting for free, which would remove a failure mode `70-THINKING/02` treats as characteristic.
- **draws on** — `E5` S4.

---

## R4 — Judge

The most-measured role here, and `50-findings/14` measured the **contract**
rather than the judgement.

### R4.1 Evidence weighing

- **does** — decide whether a change satisfies a condition, from the change and the condition.
- **varied** — how much the diff resembles a correct change without being one.
- **held** — the conditions, the diff, the format.
- **read** — per-condition `checked` entries against the deterministic check.
- **null** — flat says the judge is reading surface resemblance, which `50-findings/11` already suspects.
- **draws on** — `E5` S1.

### R4.2 Verdict calibration

- **does** — convert per-condition assessments into one verdict.
- **varied** — the mix of met and unmet conditions, and whether the unmet ones matter.
- **held** — the assessments, as the judge produced them.
- **read** — false rejection and false acceptance separately, **never a single correctness figure** — `50-findings/14` found them moving in opposite directions under one variable, and a combined score hides that entirely.
- **null** — flat says the verdict is a function of the count of unmet conditions and nothing else, which is precisely what `judge_caveat`'s prompt block tells it not to do.
- **draws on** — `E5` S3.

### R4.3 Instruction formulation

- **does** — say what to change, when the verdict is `not_met`.
- **varied** — how far the fix is from the condition that failed.
- **held** — the verdict.
- **read** — whether the next round's executor succeeds given the instruction. **Unmeasured**, and it is the only one of R4's three mechanisms with a downstream consequence that can be scored.
- **null** — flat says instruction quality does not move the loop, which would make the judge's authority question moot.
- **draws on** — `E5` S1.

---

## R5 — Test synthesiser

M7 `test_synth`. Writes a discriminating test rather than judging one.

### R5.1 Discriminator authoring

- **does** — write a test that passes on correct work and fails on plausible-but-wrong work.
- **varied** — how close the plausible-wrong variant is to correct.
- **held** — the objective and the implementation under test.
- **read** — the synthesised test run against both a correct and an incorrect implementation; a test passing both discriminates nothing.
- **null** — flat says synthesised tests do not discriminate at any distance, which would retire the role.
- **draws on** — `E5` S3, since authoring a discriminator and faulting a premise both require holding what *would* be true if the claim were false.

**This is the mechanism form of E3's held-out check**, and the two should be
read together: a role that cannot author a discriminator cannot be trusted to
author the check that scores it.

---

## R6 — Orchestrator — **not implemented**

The firing rule is hand-set. `70-THINKING/02`'s candidate contribution is to
replace ADaPT's `max_depth` constant with a measured bound, and this is the
role that would consume it.

### R6.1 Ceiling self-location

- **does** — judge whether an objective is within reach before attempting it.
- **varied** — nothing. **This is `E5` S8, and S8 is mapped rather than laddered** — the question asked is *can you do this, or do you need help*, and what comes out is two boundaries in task space rather than a score.
- **held** — everything.
- **read** — the shape relation between where the assembly says it stops and where it does.
- **null** — different boundary shapes with no transformation relating them means the firing threshold cannot come from the running assembly and must be supplied from outside, re-measured per model and per scaffold.
- **draws on** — `E5` S8 entirely. This entry exists to consume S8's map, not to duplicate it.

### R6.2 Firing decision

- **does** — decide whether to decompose.
- **varied** — objectives spanning the assembly's measured boundary.
- **held** — the decomposer and the executor, so the decision is separable from its execution.
- **read** — outcome against the counterfactual arm: decomposed when it should not have been, and the reverse. **`70-THINKING/02` is explicit that decomposing below the ceiling is pure cost**, so both directions are errors.
- **null** — flat says the firing rule is not responding to demand, which is the current hand-set state and would say the measurement bought nothing.
- **draws on** — R6.1, and through it S8.

### R6.3 Termination

- **does** — stop.
- **varied** — how clearly done the work is when it becomes done.
- **held** — everything.
- **read** — rounds after the last productive one. **Unmeasured**, and named in `10-technical/08-orchestrator-contract.md` as a required behaviour the runtime does not implement — a defect against a written contract rather than an open question.
- **null** — flat says termination is insensitive to whether the work is finished.
- **draws on** — `E5` S8.

---

## R7 — Context assembler

M9. Partially built: `10-technical/07-naive-context-assembly.md` is the naive
form, `14-context-manager.md` the intended one.

### R7.1 Relevance discrimination

- **does** — put the needed material in front of the role and leave the rest out.
- **varied** — the ratio of irrelevant to relevant material available.
- **held** — the role consuming it.
- **read** — downstream role success. **Standing evidence: dloop's retry-with-failing-lines took the cross-file slice from 0.47 to 0.92 at fixed model size**, which is the largest assembly effect this project has recorded.
- **null** — flat says assembly does not move outcomes, contradicting that measurement.
- **draws on** — `E5` S2.

### R7.2 Sufficiency estimation

- **does** — know whether what it has assembled is enough.
- **varied** — how detectably something needed is missing.
- **held** — the assembly strategy.
- **read** — whether the gap is flagged rather than filled by confabulation. **Standing evidence: M4 gave processors an explicit affordance to request missing context and it went unused across 16 runs, including on a task deliberately starved of a needed file.**
- **null** — already close to a measured null. The open question is whether the capability is absent or merely never invoked, and `E3`'s direction on ungrounded references (`00-questions.md` OQ-0) answers a large part of it deterministically, without a model.
- **draws on** — `E5` S5 absence detection.

---

## R8 — Aggregator — **not implemented**

`70-THINKING/02` argues this bounds the integrated system ceiling and that
improving executors cannot raise it. Nothing in this project has measured it.

### R8.1 Recombination under imperfect inputs

- **does** — produce the answer to the original objective from partial work toward it.
- **varied** — the number of sub-results, how many are wrong, and whether they conflict.
- **held** — the original objective and its check.
- **read** — the original check, never a judgement about the merge.
- **null** — flat says aggregation is not the binding constraint, which would contradict the argument this sheet's most consequential claim rests on, and is therefore the most valuable null available here.
- **draws on** — `E5` S7.

**The design constraint is inherited whole from S7: harvest, do not author.**
Sub-results come from real runs in the setup-keyed results store — the wrong
ones, the partial ones and the mutually contradictory ones included — because
authored inputs construct the situation the standing assumption says never
occurs. Transcripts make this buildable and did not before 2026-09-22.

---

## R9 — Knowledge curator — **not implemented**

M8. `E6` is its experiment and is gated on M8 having something to run.

### R9.1 Retention

- **does** — keep a claim past the session that produced it.
- **varied** — time and intervening work.
- **held** — the claim.
- **read** — recoverable and unaltered.
- **null** — flat is expected and uninteresting until R9.2 works; retention without retrieval is storage.
- **draws on** — nothing in `E5`. **This is a property of the store rather than of the model**, and it is on this sheet only because the role owns it.

### R9.2 Retrieval

- **does** — surface the right stored claim at the moment it bears.
- **varied** — corpus size, and how obliquely the claim bears on the work.
- **held** — the corpus.
- **read** — a processor reusing one stored finding against one starting cold. `E6` requires the small test before the corpus sweep, for the reason that sheet gives: a corpus sweep that fails says nothing about which of ingestion, retention or retrieval failed.
- **null** — flat says curated memory does not beat starting cold, which would overturn a core hypothesis.
- **draws on** — `E5` S2.

### R9.3 Use of knowledge not derived in session

- **does** — act correctly on a claim it did not work out itself.
- **varied** — how far the stored claim is from the current work.
- **held** — retrieval, so the claim is in hand.
- **read** — graded against M9's metrics — validity, reliability, pertinence, scope — **not task success alone**, since the corpus was not produced to serve any one task.
- **null** — flat says retrieved knowledge is present and inert.
- **draws on** — `E5` S1.

---

## What this inventory says about the architecture

**Three of nine roles are not implemented, and the firing rules consume their
outputs.** R6 decides when to decompose and does not exist; R8 is argued to be
the binding constraint and does not exist; R9 is a core hypothesis and does not
exist.

**Two mechanisms are already close to measured nulls** — R7.2 sufficiency
estimation, from M4's 16 unused affordances, and R6.3 termination, which
`10-technical/08` requires and the runtime does not implement.

**One pair is the cleanest transfer test available** — `E5` S3 against R2.1,
the same demand graded end-to-end and in position — and it should be run first
for that reason rather than because premise evaluation is the most important
mechanism.

---

# Preparation

*The sections below were written for the sweep as a whole and apply to all
three layers. They stay here because this is the layer whose items are most
expensive to author; [`E3`](E3-functional-requests.md) and
[`E5`](E5-skill-scales.md) refer to them rather than restating them.*

## Preflight — the one run that can cancel the rest

**Before any of the below is built, run the existing 34 tasks once, n=1, on the
largest model available.**

If it passes 32 of 34, the M6 evaluation suite is **exhausted at that scale** and every
comparison run on it afterwards is noise: a scaffold buying three rungs and one
buying six both read as "passed everything." That is a ceiling effect on the
*instrument*, named in `70-THINKING/02` as the thing that would silently cap
this project's own output metric, and it collapses both of E0's factors at once.

This costs one run and it decides what the rest of this sheet is for. A high
score means new items are required and tuning the old ones is wasted effort; a
middling score means the M6 evaluation suite still discriminates and extension is the cheaper
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
- **The pool and the setup-keyed results store travel as directories**, which is why they are
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
keys, the setup-keyed results store, per-cell transcripts, the judge arms, reps with intervals, a
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
