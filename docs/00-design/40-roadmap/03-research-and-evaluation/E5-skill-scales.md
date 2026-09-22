# E5 — Do basic skills have measurable scales, and does skill capability transfer upward?

**Status:** not run. Opened 2026-09-22 in the three-layer rework.
**Layer:** 3 of 3 — **skill**. See [`README`](README.md) for the layer split.
**Absorbs:** the whole of the former `E3-first-ladder`, whose monotonicity
design and pre-registration commitments apply here rather than at any other
layer; and the former E4's size-and-tuning question, asked at this layer.
**Was:** `E5-population-spread.md`, which measured the operator. That sheet's
argument survives as a constraint on every layer rather than as an experiment —
see "What each layer is blind to" below.

## Status: WIP, and what convergence means

This sheet is a **working set**, not a settled design. Its shape is expected to
change, and that is not licence for it to stay vague indefinitely. It converges
when all four of these hold:

1. every candidate carries a **rung ladder**, with its ordering and its
   non-monotonicity tolerance written down beforehand;
2. every candidate carries a **transfer pair**, named before any data exists;
3. the identifiability literature (`70-THINKING/02` OQ-B) has been read, and
   says whether a family of this size is recoverable at all, and from how many
   items and subjects;
4. **one scale has been built end to end**, so the cost of a scale is a
   measured number rather than an estimate.

Until all four hold, entries here are provisional and may be demoted, merged or
split.

### The working rule, which is why this list is longer than is comfortable

> **A candidate that is awkward for the current framework gets written down,
> not left out.**

Omitting a demand because the standing assumption makes it hard to probe
settles by intuition what this folder exists to settle by evidence.
Decomposition and aggregation were left off the first draft for exactly that
reason, and are restored below with the objection stated and designed around
rather than used as grounds for silence.

## The question

A **skill** is the narrowest demand that can be varied on its own. This sheet
asks two things, and the second is the one that makes the first mean anything:

1. Can each candidate skill be put on an ordinal scale that behaves
   monotonically — does a subject's exit rung say something stable?
2. **Does measured skill capability predict mechanism capability** (E4) and,
   through it, functional capability (E3)?

## The problem this sheet exists to solve: there is no positive definition of skill

Nothing here can say in advance what a skill *is*. Every candidate below looks
decomposable into something more basic, and that regress has no obvious floor.
Picking a level by intuition is the error the rest of this folder exists to
avoid.

**So do not define it. Give it a criterion:**

> A candidate skill earns the name when its measured level on one item family
> **predicts performance on a different family that demands it in another
> surface form.**

This is operational, it can fail, and a candidate that fails it is demoted
rather than argued about. It also makes the layer-3-against-layer-2 comparison
**constitutive rather than confirmatory**: the transfer test is not a check on
whether the skills were chosen correctly, it is what makes them skills.

**The corollary is the useful part. Narrowness is not the criterion.** One can
always subdivide further; the question is never how far down the subdivision
goes but whether it *buys transfer*. A subdivision that does not is a task
feature wearing a skill's name. A subdivision that does is real at that grain,
whether or not something finer exists beneath it.

**Operating rule: no skill enters this sheet without a stated transfer pair** —
the two item families it must predict across, written before any data exists.

### How this stays inside the standing assumption

`70-THINKING/02` holds that the ceiling does **not** decompose into separable
operations, and forbids designing separability into the instrument. A family of
per-skill scales is exactly the shape it warns about.

It stays licensed by the distinction that document draws itself: what is wanted
is **item-level demand variation**, not skill isolation. Every scale below is
**end-to-end** — same deliverable, same check, one demand varying by
construction. None supplies fixed sub-results, none measures an operation in
isolation, and none claims the underlying abilities are separable.

Factor structure is a **result** of running these, never a premise. If exit
rungs correlate across scales once tuning is controlled, the ceiling is unitary
and this family collapses to one number — which is a real finding and the
standing assumption survives. If they diverge *stably across differently-tuned
models*, it is dimensional. That is move 3 of the falsifiability audit in
`70-THINKING/02`, and it cannot be run until several scales exist, so building
the family is simultaneously the experiment about whether the family means
anything.

## The candidate skills

Working set, 2026-09-22. Seven entries. Each carries what varies along its
scale and the transfer pair it must survive, and several are expected to merge
or be demoted once the criterion is applied to data rather than to argument.

Entries are written down where they are awkward rather than left out — see the
working rule above. S6 and S7 in particular are here **despite** the standing
assumption making them hard to probe, with the objection stated inside each and
designed around.

### S1 — Grain closing

Bridging from the representation handed over to the representation the question
requires. The central quantity of `70-THINKING/02`.

**Scale:** the *level* of the handed representation, token-matched and
sufficiency-matched at every rung. R1 the failing function and its assertion →
R3 the module as names, signatures and one-line intents → R5 a prose statement
of what the system is for. Sufficient at every rung by construction.

**Transfer pair:** locating a defect from a module summary versus from the file;
and answering a configuration question from an architecture statement versus
from the config files. Code-shaped and not-code-shaped. If only the first
works, this is code navigation, not grain.

**Note:** this scale is one step from the token-matched grain-match test that
`70-THINKING/02` calls its single live discriminator and that E2 has not been
able to build. If A ≈ B at matched tokens, the granularity hypothesis collapses
into "relevant context beats maximal context" and that document says so itself.

### S2 — Relevance discrimination under volume

Finding the needed item among many that are not.

**Scale:** ratio of irrelevant to relevant material, 1:1 → 1:1000, with the
needed fact and the deliverable fixed.

**Transfer pair:** finding an API fact among N documents; finding the
discriminating test among N tests. Prose and code, same demand.

**Relation to E1:** E1's first move returned negative — the context-blur claim
did not survive, because the motivating anecdote was a global failure rather
than selective omission. This scale is the controlled form E1 could not build,
and it should be read as replacing that claim rather than rescuing it.

### S3 — Premise evaluation

Deciding whether a request is sound before doing it.

**Scale:** the depth at which the unsoundness is discoverable.

| rung | the request is contradicted by |
|---|---|
| R1 | the docstring of the function it names |
| R2 | an existing test in the same file |
| R3 | an invariant established elsewhere in the module |
| R4 | nothing local — only running the code shows it |
| R5 | nothing in the repo — it is impossible on complexity grounds |

Deliverable at every rung: refuse, and name why.

**Transfer pair:** false-premise code requests; false-premise document or spec
requests ("update the changelog entry for v3.2" where no v3.2 exists). If only
the code family works, this is pattern-matching against tests rather than
evaluating a premise.

**Why it is worth building despite `50-findings/14`:** that sheet found the
judge producing `unsound_request` in **zero** of eight cells, and its addendum
withdraws the accompanying claim about the engineer stage as unmeasured. A flat
zero across all five rungs would say refusal is never *produced*, which is a
different and more tractable failure than never being *reached*. The scale
distinguishes them; the current instrument cannot.

### S4 — Objective retention

Holding what was asked across intervening work.

**Scale:** number and heterogeneity of intervening steps between receiving the
objective and the point where it binds — 1, 3, 8, 20, 40.

**Transfer pair:** a multi-file code change; a multi-step document revision.

**This is the candidate most likely to be demoted**, and that is a reason to
build it rather than to drop it. It may be a context-length artifact wearing a
skill's name, in which case its scale will track context occupancy rather than
step count and the transfer pair will fail. Either answer is worth having, and
it is the failure mode `70-THINKING/02` calls **tangential success** — every
sub-task done well, the objective dissolved.

### S5 — Absence detection

Noticing that something needed was not supplied, rather than confabulating it.

**Scale:** how detectable the gap is. R1 a reference to a file never provided →
R2 a convention referenced but never stated → R3 an invariant assumed but never
given.

**Transfer pair:** a missing file in a code task; a missing constraint in a
spec task.

**R1 calibrates the scale rather than the subject.** A reference to something
never supplied is detectable deterministically, by checking symbols against
what was provided — `70-THINKING/02` notes it is a grep, not a probe. That makes
R1 a control: a subject failing R1 is failing something a non-model can do, which
says the rung is mis-built or the subject is not engaging, not that the skill
is absent.

**Standing evidence:** M4 gave processors an explicit affordance to request
missing context and it went **unused across 16 runs, including on a task
deliberately starved of a needed file.**

### S6 — Decomposition

Producing work whose size exceeds what a single pass can carry.

**The objection, stated first.** Asking for a decomposition and grading it
requires knowing the right decomposition, which is authorship above the
subject's own ceiling — `70-THINKING/02` OQ-7 — and that cost reappears at every
item. It also measures the artifact instead of the work.

**The design around it: never ask for a decomposition, and never grade one.**
The deliverable at every rung is **the finished work**, checked the same way.
What varies is how far the objective exceeds what fits in one pass, so that
splitting stops being optional.

| rung | the objective |
|---|---|
| R1 | fits one pass comfortably |
| R2 | fits, with nothing to spare |
| R3 | does not fit; two obvious parts |
| R4 | does not fit; the parts are not obvious |
| R5 | cannot fit under any single-pass framing |

The exit rung is where correct work stops appearing. Nothing is asked about
method, so a subject that gets through by a route nobody anticipated still
scores.

**Transfer pair:** a code objective too large for one pass; an analysis or
document objective too large for one pass.

**What a flat scale means:** if the exit rung tracks context occupancy rather
than structural part-count — R3 and R4 differing little while R2 and R3 differ a
lot — this is not decomposition, it is S2 or a window limit, and it merges.

### S7 — Aggregation

Producing the answer to the original objective from partial work toward it.

**The objection, stated first, and it is the sharpest in this folder.**
`70-THINKING/02` rejects supplying fixed correct sub-results: it *constructs a
situation that never occurs*, since real sub-results are partial, wrong, and
wrong in interacting ways. Such a measurement can be perfectly reliable and mean
nothing, and the direction in which it misleads is not predictable in advance.

**The design around it: harvest, do not author.** Sub-results come from **real
runs already in the store** — the wrong ones, the partial ones and the mutually
contradictory ones included — which is precisely the situation the objection
says authored inputs cannot reproduce. Transcripts make this buildable now and
did not before 2026-09-22.

| rung | the sub-results supplied |
|---|---|
| R1 | two, both correct, no conflict |
| R2 | three, one partial |
| R3 | four, one wrong, with nothing flagging it |
| R4 | four, two mutually contradictory |
| R5 | six, provenance mixed, one addressing a superseded objective |

Deliverable at every rung: the answer to the **original** objective, against the
original check.

**Transfer pair:** merging code sub-results; merging findings or analysis
sub-results.

**Why it is worth the trouble:** `70-THINKING/02` argues that aggregation rather
than execution bounds the integrated system ceiling, and that improving
executors cannot raise it. Nothing in this project has measured it. If that
argument is right this is the most consequential scale on the sheet; if it is
wrong, this is the cheapest way to find out.

**Residual risk, not resolved.** Harvested sub-results are still *supplied*
rather than produced by the subject, so the subject did not form the intent
behind them. That is a weaker form of the objection, not its absence, and it is
why R5 mixes provenance — an aggregator in a real assembly also receives work it
did not commission.

### Demoted — consistency under repetition

Same input, same answer. Proposed and **rejected as a skill**: it has no demand
to vary, so it cannot have a rung. It is a *variance measure taken on the other
scales* at fixed demand, and it belongs in the method rather than the list.
Recorded here because it is the first thing the criterion above disqualified,
which is the criterion doing its job.

### Absent, and the reason has to be an ordering one

**Fit self-assessment** — *can the model tell whether a task is above its own
ceiling* — is the only candidate deliberately without a scale here, and the
reason is sequence rather than discomfort. It is **second-order**: it is scored
as the correlation between predicted and actual competence, so it cannot be
measured until the first-order ceilings this sheet produces exist. It belongs to
the orchestrator role in [`E4`](E4-capability-sweep.md), gated on E5's results.

**Every firing rule in the architecture consumes its output**, which is why the
ordering is worth stating rather than assuming.

*Decomposition and aggregation were listed here in the first draft, on the
grounds that the standing assumption forbids probing them in isolation. That was
the wrong call: the assumption constrains how they are probed, not whether they
are named. They are S6 and S7 above.*

## The transfer tests

Two comparisons, and they are the point of the three-layer split:

| | compares | a null means |
|---|---|---|
| **skill → mechanism** | E5 exit rungs against E4 mechanism scores | the skills are not the ones the mechanisms use; the list is wrong, not the mechanisms |

Two entries — S6 decomposition and S7 aggregation — carry names that also appear
as mechanisms in E4. **That is deliberate, and it is the cleanest transfer test
available**, because one word is being measured two ways: here as a demand on an
end-to-end deliverable, there as a role's output inside a working assembly. If
the two disagree, the disagreement is the finding — and it is the one place
where *is this a skill or a mechanism?* gets an answer from data rather than
from definition.
| **mechanism → functional** | E4 scores against E3 outcomes | mechanism competence does not compose; the binding constraint is between mechanisms, not inside them |

The second null is the more interesting one and it is predicted by
`70-THINKING/02`: if aggregation rather than execution bounds the system, then
mechanisms can each be competent and the system still fail, and the gap between
E4 and E3 is where that shows up.

## What is held constant, and therefore what this layer is blind to

The former E5 measured the operator and made the general point: *every
experiment that holds the operator constant scores the system minus the person
using it.* Generalised, each layer must state what it fixes.

This layer fixes **everything except one demand** — the scaffold, the operator,
the model's configuration, the task's surface form. It is therefore blind to
every interaction between skills, which is precisely what E4 and E3 are for. A
subject that tops out at R4 on all five scales and fails every functional task
is not a contradiction; it is the composition failing, and no amount of
resolution at this layer would show it.

## What would falsify a scale

**Inherited from the former E3, unchanged, and the load-bearing part of this
sheet:**

Rung ordering and the tolerance for non-monotonicity are fixed **in writing
beforehand**, with an advance commitment **not to rebuild the ladder when it
fails**.

That second commitment is the one that costs something. A ladder rebuilt after
a bad result measures the rebuilder, and the failure becomes invisible
afterwards because the published ladder is the one that worked. Non-monotonicity
beyond the stated tolerance says the rungs are not ordered by what they were
meant to be ordered by — a result about the construct, not about the subject.

## Size and tuning

The former E4's design constraint applies here: vary **size and tuning, not
size alone**. Tuning reshapes results unevenly across domains, so a size-only
design reports a capability curve that is partly a tuning curve with nothing in
the result saying which part. At this layer it does double duty — divergence
that tracks the tuning domain is an artifact, divergence stable across
differently-tuned models is the evidence that the ceiling is dimensional.

## Open

- **The list is a working set.** Seven entries, one already demoted on the
  criterion, two restored after being wrongly cut. Which of S1–S7 survives its
  transfer pair is the first thing this sheet produces, and S4 and S6 are the
  two most likely to merge into something else.
- **The identifiability question is unresolved** and is the same one
  `70-THINKING/02` defers to under OQ-B: how many items and how many subjects
  does recovering latent structure take, and when is it recoverable at all.
  Reading that literature is cheaper than running a scale family that cannot
  identify anything.
- **Cost is unknown** until the item-authoring effort for one scale is real.
  S1 or S3 first, on the argument that S1 carries the grain-match test and S3
  extends a measurement that already exists.
