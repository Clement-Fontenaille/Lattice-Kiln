# E3 — Does a full system serve a request a user would actually make?

**Status:** not run. Re-scoped 2026-09-22 in the three-layer rework.
**Layer:** 1 of 3 — **functional**. See [`README`](README.md) for the layer split.
**Was:** `E3-first-ladder.md`, a single graded ladder of relational demand. That
content moved wholesale to [`E5`](E5-skill-scales.md), where a ladder is the
instrument rather than the subject — including its monotonicity tolerance and
the commitment not to rebuild a ladder that fails, which is the part least
worth losing in a move.
**Depends on:** the shared preparation in [`E4`](E4-capability-sweep.md) —
preflight, what travels, what is collected, and the specification contract. This
sheet does not restate them.

## The question

Everything below is a **whole system answering a request phrased the way a user
would phrase it.** No stage is isolated, no demand is graded, nothing is held at
a chosen level. The subject is the assembly, and the score is whether the
request was served.

This is the layer whose result is worth having and whose result explains
nothing.

## Why it cannot attribute, and why that is the design

A functional failure does not say which mechanism failed. That is not a defect
to engineer away — it is what distinguishes this layer from
[`E4`](E4-capability-sweep.md), and attributing would require holding constant
the very things a real request does not hold constant.

Its job is to be **the thing the other two layers are checked against.** If
mechanism scores (E4) rise and functional outcomes here do not, the composition
is the constraint — which is what `70-THINKING/02` predicts if aggregation
rather than execution bounds the integrated system ceiling. That gap is
visible only because this
layer refuses to attribute.

## What is held constant, and therefore what this layer is blind to

Almost nothing is held constant, which is the point. What *is* fixed is the
**operator** — and the former `E5-population-spread` is the sheet that named
the cost: *every experiment that holds the operator constant scores the assembly
minus the person using it.* This layer is the one where that bites hardest,
because a real request is exactly where an operator would be intervening.

So a null here is ambiguous in a way the other layers' nulls are not: it may be
the assembly, or it may be the absence of anyone steering it.

## The directions

Six, from the operator's own list, 2026-09-22. The **borrow-or-build** call is
settled; the specifications are not, and each gets its own discussion.

| # | direction | measures | check | source |
|---|---|---|---|---|
| 1 | add a basic feature | navigation, convention-following | new tests pass | **borrow** |
| 2 | fix a basic error | localisation | red → green | **borrow** |
| 3 | fix a harder bug | depth of understanding | red → green **+ held-out** | **borrow the task, author the held-out check** |
| 4 | change + docs + CI | objective retention, **aggregation** | three independent structural checks | **build** |
| 5 | dig a large corpus, then implement | retrieval under volume | feature works | **build** |
| 6 | diagnose a failure from logs | inference from evidence | structured claim, exact match | **build** |
| 7 | apply one decision across many sites | **internal consistency**, drift | agreement across sites, first ten against last ten | **build** |
| 8 | a fault the failing evidence points away from | **locating a fault against misleading evidence** | red → green **+ held-out** | **build, from this project's own history** |

### Why 1–3 are borrowed, and what is actually borrowed

They are SWE-bench-shaped. Building them here means fewer items and unproven
checks, and **a wrong check is worse than a missing item** — it injects
correlated noise into the response matrix, and correlated noise is
indistinguishable from a factor (`70-THINKING/02`). A cluster of subtly broken
checks presents as a clean, spurious dimension.

This project's asset is not the tasks. It is the instrumented comparison: setup
keys, the setup-keyed results store, per-cell transcripts, the judge arms, reps
with intervals, a pool that survives being killed.

**What is borrowed is the task, not the check.** The held-out check is authored
here in every case, because it is what makes direction 3 a measurement rather
than a lookup — and because a check that travels with a task has usually been
seen alongside it.

### Contamination: a recorded caveat, not a question this sheet asks

Borrowed items are contaminated to an unknown degree, and **this sheet does not
adjudicate what that means.** Whether a fast correct answer from a practiced
pattern match differs usefully from one arrived at by reasoning is a real
question and not one that has to be answered to use these items — the line
between retrieved and derived is not clean in people either.

What has to be recorded is where it lands:

> Contamination **inflates the estimated effective ceiling**, and the
> decomposition firing rule consumes that estimate. An inflated ceiling biases
> the assembly toward decomposing **less** than it should, on work that was
> never in training — which is the operator's own repository.

So the bias has a known direction, and it is the unhelpful one.

**It is not being measured.** No perturbed variants, no study of how much
surface change defeats recall, no effect size across degrees of item
modification. That is a research programme of its own and it is not this one.

**Standing caveat: any effective-ceiling estimate resting on borrowed items is
an upper bound, not an estimate.** Directions 4–8 are authored here and do not
carry it, which is one more reason the built directions are where the weight
should sit.

### Why 1 and 2 are anchors rather than discriminators

They will saturate on a large model, and that is their job: they hold the
bottom of the difficulty range so that ability and lift stay estimable above
it. An item set that tops out near the subject's effective ceiling cannot tell a
good
scaffold from a great one, and the preflight in E4 exists to find out whether
the current suite already has that problem.

### The three that are built, and what each is for

**4 — change + docs + CI** tests the failure the design set says is binding.
`70-THINKING/02` argues aggregation, not execution, bounds the integrated
system ceiling, and that **tangential success** — every sub-task done well, the
objective dissolved — is the characteristic failure. Neither has been measured
here, because every existing task is too short to drift. Scoring stays
structural: does the docstring name the new parameter, does the changelog carry
an entry, does CI actually run the new test. No judge required.

**5 — dig a corpus, then implement** is the only direction with a
**controllable difficulty dial**: hold the task fixed, vary how much material
surrounds the fact needed to do it. Everything else is authored at a difficulty
and hoped over. The dial scales to the next model without re-authoring, and it
is the functional form of [`E5`](E5-skill-scales.md)'s S2 — which makes this
pair the first place to look for skill-to-function transfer.

**6 — diagnose from logs** needs its scoring inverted to be checkable at all.
An explanation as output puts the measurement back on prose judging, which
`50-findings/14` found returning **zero** unsound-request calls in eight cells
of eleven. Instead: **synthesise the failure so the true cause is known**, and
score a structured claim — which service, which call, which line, what cause —
by exact match. Different faculty from everything else here, and the one no
existing corpus serves.

### 7 — one decision, many sites, and the two senses of consistency

Added 2026-09-22. It exists because "consistency" was being used for two
quantities that need different treatment:

| sense | what it is | where it is measured |
|---|---|---|
| **repetition variance** | the same objective run again, and how far the outcome moves | already in the data — every cell is run at several reps. See `E5`, *Derived* |
| **internal consistency** | many related decisions inside **one** deliverable that must agree with each other | **nowhere yet.** This direction |

Only the second needs a scenario, and nothing in this project has measured it.

**The buildable instance: a cross-cutting convention change.** *Every public
function must validate its inputs and raise a domain-specific error*, across
forty call sites. Each site is a small decision; the requirement is that they
are the **same** decision.

- scored by **AST-matching each site against the intended pattern**, so
  agreement is a count rather than a judgement;
- it has a **dial** — ten sites, forty, two hundred — so it scales to a larger
  model without re-authoring;
- the fixture is ours, so there is no contamination;
- and failure means inconsistency rather than four other things, which is rare
  at this layer.

**It measures drift, which is the part worth having.** Score the first ten
sites against the last ten. A convention that holds early and decays late is
`70-THINKING/02`'s **tangential success** showing up in miniature — each
decision locally defensible, the whole no longer coherent. That makes this
direction the functional partner of [`E5`](E5-skill-scales.md)'s **S4 objective
retention**, the way direction 5 partners with S2, and therefore a
mechanism-to-function transfer probe rather than only a task.

**The anchor instance: port a codebase to another language.** The operator's
own candidate, and it demands consistency far harder — every construct
translated the same way, a helper introduced in file 3 still used in file 40,
naming holding across hundreds of sites. It also has an elegant held-out check
available: port the implementation, keep **language-agnostic test vectors**
(data in, data out) that the subject never sees, and run them against both
sides.

Two costs, one fixable. It **conflates** — a failed port may be inconsistency,
translation competence, target-library knowledge or build-system work, and
while this layer does not attribute by design, an item with four failure routes
is weak even here. And any well-known library has already been ported into the
training data, which is fixable by choosing an obscure or synthetic source.

**Build the convention change; keep the port as the anchor.** The port is the
more realistic item and the one worth having when it is affordable; the
convention change is the one that gets built and answers the question sooner.

### 8 — when the evidence points somewhere other than the fault

Requested 2026-09-22, for a reason that is a design input rather than a
preference: **the operator wants an item family recognisable from their own
work**, in order to read a failure and judge what was missing and which
mechanism would have helped. An item nobody recognises cannot be reasoned about
that way, however well it scores.

**Directions 1–3 share a shape that real debugging often does not have.** The
failing test points at the fault. Localisation is a search over a space the
evidence narrows for you. That is a real and common kind of work, and it is not
the kind that consumes the hours.

The family proposed here inverts it:

> **The failing evidence is accurate, and it points somewhere other than the
> fault.** The defect is not in the code under the assertion; it is in the
> relation between that code and something not visible from it.

**The source is this repository's own history**, which is what makes the items
recognisable and the ground truth exact. Four instances from 2026-09-22 alone:

| symptom | where the fault was |
|---|---|
| a claim aborts with `PermissionError` on unlink | the claim had already succeeded; removing the pending file is tidying, and a losing thread still held it open. Windows only, twelve threads only |
| two models loaded on one card, 7,897 of 8,192 MiB | the guard read residency and decided *before* any load happened. Four workers each read zero and each concluded it fit |
| a model appears to exceed VRAM and OOM | three orphaned `llama-server` processes from earlier restarts were holding 5,830 MiB. The configuration was innocent |
| a judge emits no JSON in 18% of calls | undiagnosable — nothing stored what the model said. The fault is in what was not recorded |

They share a structure. **The evidence is local and the cause is relational** —
to the operating system's atomicity guarantees, to another process, to a
decision made before the observation, to data that was never captured.

**Why this is worth building rather than borrowing.** Corpora are assembled
from resolved issues with a failing test attached, which selects for the shape
in directions 1–3. A fault whose evidence misdirects tends to be resolved with
a commit message rather than a test, so it is under-represented in exactly the
corpora available.

**How it is checked.** As direction 3: red → green on the visible check, plus a
held-out check that the obvious local fix fails. Here the held-out check writes
itself — the obvious fix is *repair the thing the evidence points at*, and the
held-out check is the one that still fails when you do.

**What it measures, and the caution.** The named demand is locating a fault
against misleading evidence. That is a functional-layer label, and this layer
does not attribute, so it may also be measuring tool use, patience, or a
willingness to disbelieve a test. **It is drawn from one project's history and
therefore from one engineer's habits** — a population of one, with all that
implies, and the transfer question is whether these items behave like each
other at all.

## The held-out check does three jobs

Specified in full in [`E4`](E4-capability-sweep.md); restated here only because
it is what makes direction 3 buildable.

> **Author the bug so that the obvious fix passes the visible test and fails
> the held-out one.**

It operationalises "harder", it catches every form of cheating identically, and
it is the only check that survives a model having shell access to the
workspace.

## What a null means

Flat functional outcomes across systems, with E4 showing mechanism differences,
is the **most informative** result this sheet can produce: it says mechanism
capability does not compose, and it locates the constraint between mechanisms
rather than inside any of them.

Flat outcomes with E4 *also* flat says the subjects do not differ on anything
these tasks demand, which bounds the M6 evaluation suite rather than the systems.

## Open

- Per-direction specifications, one discussion each. The contract every one
  must satisfy is in E4; what is not settled is the fixture, the protected set
  and the held-out check for each.
- Which corpus supplies 1–3, and whether its items survive the air-gap rule.
- Whether direction 5's dial can be built at all — E2 has not managed the
  token-matched version, and the note in its folder says why.
