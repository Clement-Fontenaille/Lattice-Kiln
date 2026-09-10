# Use Cases — what is this thing actually for?

**State:** OPEN
**Opened:** 2026-09-03

## Why this thread exists

The charter states an ambition ("a reproducible AI-assisted software-development
environment"). The milestones state a mechanism (processors, orchestrator,
invariant floor, evaluation suite). Neither states what a person sits down and
*does* with it.

M0–M6 measured whether the machinery works. The 30-task suite measures whether a
pipeline can complete a *task*. No milestone so far has asked whether the tasks
are the ones anyone wants done, or whether the shape of the interaction — a
request handed to a supervised loop — is the shape a user actually wants.

That question was cheap to defer while the answer was "whatever a 7B can survive."
It is about to stop being cheap.

## Why now

Three things shift at roughly the same time:

1. **The constrained-model line continues** — the 7B remains a subject, not a
   dead end.
2. **A stronger model becomes available** — hypotheses and workflows can be
   tested against a capable model rather than only against one that fails in
   ways that may be idiosyncratic to its size.
3. **A multi-model / multi-size experiment may be possible** — capability becomes
   an *axis* rather than a fixed constraint.

Consequence: findings currently phrased as "a 7B cannot do X" become testable as
"does X depend on capability, or on the system around it?" That is the
constrained-intelligence thesis' central open question
(`10-foundations/01`) becoming answerable — but only if we know what X should be.
Hence: use cases first.

---

## 1. Impressions from use

_The user's own experience. Unfiltered; not yet evidence._

### The setting

Method-and-tools team of an HPC facility inside a large company. A few thousand
users. Twenty-odd years of accretion. Ergonomics are not the strong point, and
the surface needs constant attention.

The people served and the people worked with are **the same people** — no
principal-agent gap, no distant stakeholder to impress. The evaluation function
is real satisfaction of real colleagues, which is honest and *not measurable by a
test suite*.

Blast radius is the defining operational fact: a regression is not a bug, it is a
thousand jobs failing and the team's credibility with them.

**Local-first is non-negotiable** — institutional policy, not preference. The
codebase cannot leave the building. Two independent motivations now stack:
the hardware discipline of the thesis, and a hard constraint.

### The work that isn't getting done

Five projects named as wanted-but-unreachable:

1. Environment- and feature-driven management strategy for configuration-as-code
   repos.
2. Displacing the roofline model for HPC architecture evaluation, using knowledge
   of the applications' actual binaries only.
3. Automatic job-failure detection and diagnostic.
4. Job-data strategy: GPFS vs local; `cp` / `scp` / RDMA for result movement;
   what each approach actually buys.
5. A complete stale-data audit — a petabyte, ~5 % genuine archives indistinguishable
   at a glance from the other 95 % — involving users and incorporating their
   feedback, with pre-classification.

**Shape of that list:** four of five are *investigation → judgment → write-up*.
None of them is "write me a function." (See open question OQ-1.)

### What is in the way

- **"Job X crashed, figure out why."** Explicitly *not* a 15× candidate per
  instance. The win is **/15 in occurrence** — environments hardened, tunings
  consolidated, so the expensive non-human-error class stops recurring. The
  human-error class shrinks too, via documentation and guides that currently
  don't get written.
- **Analysis, script rework, software testing, bug identification, config
  trials.** The lever named is *setup cost for a replication experiment*: drive
  it low enough and the task fits in the gap while an install runs, instead of
  consuming half a day.
- **"Plot job wait time by walltime, find the outliers, work out why, is there a
  hole in the configuration?"** — two days.
- **Ticket triage.** "Paste the issue, see where it goes" would resolve ~80 % of
  human-error tickets, or return *"plausible culprit is X, but there isn't enough
  information — please provide Y."*
- **Keeping things organized.** Named as the place the true 15× lives: reading,
  checking, cross-checking, testing, writing, keeping it tight.

### The friction loop

Things sit under the stair mostly on **effort and friction**, not on nerve or
lost knowledge. Decisions bottleneck, but mostly because *having the discussion
and iterating over alternatives is itself investigation work nobody has time
for.*

Compounding it: **testing and investigation time is systematically
under-estimated, so it does not feel like progress.** The resulting frustration
degrades the capacity to take on new work and to stay organized — which increases
friction, which increases investigation time.

This is a loop, and it is plausibly the actual mechanism keeping the backlog
where it is.

### What this project is for

Explicitly **not** destined to become the team's real tool, or part of its
ecosystem. Money is being spent and effort made elsewhere to bring a tool of this
kind to the work. This project's contribution is **understanding what is
needed, and feeding back insight** that helps that effort go in the right
direction.

### Request substrate

Tickets, emails, chat messages.

---

## 2. External signal

_Feedback gathered from other people. Who, in what context, and what they
actually said — not the summarized version._

## 3. Community positions

**Done (2026-09-04) → `03-how-the-field-frames-it.md`.** Survey of the major
frontends: documented practice and positioning, mechanics separated from
rhetoric. Headlines:

- **No product takes the backlog as its objective.** The field's unit of work is
  the *diff*; the issue→PR tier consumes an already-triaged item and still
  terminates in a diff. Triage exists only as a bolt-on.
- **The field found this project's results and shipped them as user advice**, not
  system behaviour — add fewer files, skip the plan if the diff is one sentence,
  repo maps instead of file contents, hooks-not-prose for anything that must
  happen, cross-model plan review.
- **P3 is confirmed at industry scale.** Completed epics/dev +66 %, production
  incidents per PR **+242.7 %**, unreviewed PRs to main +31.3 % (Faros);
  median-team main-branch throughput *falling* while overall throughput rises
  59 % YoY (CircleCI).
- **Context files do not work.** ETH Zurich, controlled: no success improvement,
  >20 % added cost. ~~And the sign flips on authorship.~~ **Corrected
  2026-09-04:** the operative variable is **redundancy, not authorship** — strip
  the redundant material and machine-generated files *beat* human-written ones.
  What survives: non-additive content is **actively costly**, not neutral.
- **Challenge to §1:** developers *feel* ~20 % faster and are *~19 % slower*
  — **METR** (RCT, 16 devs, 246 tasks, early-2025 tooling; forecast −24 % →
  self-estimate −20 % → measured +19 % time). *(Corrected 2026-09-05: the first
  draft credited this to LinearB, ~8.1M PRs — that conflated two studies, see
  `03` §5. LinearB's separate contribution is the merge-rate / PR-size / pickup
  spread.)* Bears directly on OQ-3 and the 15× expectation.

---

## 4. Positions taken

_Running log. Adjustments recorded in place, with what caused them — the
superseded position is struck through, not deleted._

### P1 — The deliverable is insight, not an assistant (2026-09-03)

The project will not ship the team's tool. Its output is the findings log and the
comparisons that produce it.

**Consequence:** optimizing for a good shippable assistant is a category error.
The value is in *rigorous, reproducible, adversarially-designed comparison of
system configurations* — which is precisely what the M6 machinery was built to
do, and which almost nobody else is positioned to produce cleanly, because
everyone else is optimizing a product.

**Sharpest form:** when the stronger model and the multi-size sweep land, the
prize is not "my assistant got better." It is *"here is what changes and what
does not when capability rises"* — a finding that requires exactly this project's
apparatus and exactly this project's disinterest in shipping.

### P2 — "15×" is three different mechanisms, not one (2026-09-03)

They need different evidence and different system properties, and conflating them
makes the claim untestable.

| # | mechanism | shape | example |
|---|---|---|---|
| A | **Occurrence reduction** | amortized, delayed, compounding — the fix is permanent and consolidated | crash classes stop recurring: `/15` in occurrence, not `×15` in speed |
| B | **Latency collapse** | *categorical*, not quantitative — a task drops below the threshold where it needs a scheduled block, so it fits in gaps | bug-replication setup, fired off while an install runs |
| C | **Raw throughput** | genuine ×15 | reading, cross-checking, testing, writing, keeping it tight |

**B is the sleeper.** A half-day task you must schedule and a ten-minute task you
fire into a gap are different *kinds* of thing, not the same thing at different
speeds. Half-day tasks queue behind each other and rot; gap-sized tasks do not
queue at all. Much of the backlog may be a scheduling-granularity artifact.

### P3 — Entropy reduction is the product (2026-09-03)

The user's requirement — *"consolidates, evaluates, and helps organizing things,
not spread entropy"* — was already discovered by this project's own evidence and
mis-filed as safety.

Every mechanism behind dloop's M6 win is entropy suppression, not productivity:
0 regressions vs 7, 0 crashes vs 4, 5/5 correct declines, incumbent-in-keeper-pool
(a change must *beat* doing nothing). The monolith is **faster** and produces
**more change**, and loses anyway, because ~1 task in 3 it makes things worse.

**Proposed motto revision** (`10-foundations/01`):

> ~~Spend system design to save model capacity.~~
> **Spend system design to bound what the model can make worse.**

The original is justified by scarcity and expires when capability rises — plausibly
on someone else's schedule. The replacement is a permanent property and is what
the data actually supports. A more capable model is not an entropy reducer; it is
a faster, more plausible entropy producer. Nothing in incumbent-protection,
test-gating, or correct declines says *"because 7B."*

**Not yet promoted to `00-design/`** — wants the capability sweep as evidence.

**Promoted (2026-09-10), in part.** The core claim — entropy reduction is the
product, not throughput — is now in `10-foundations/02-reasoning-vs-runtime.md`,
Proposal and effect, cited directly to this entry. The proposed motto revision above
is not promoted: it is a claim about robustness across model capability, and still
wants the capability sweep this entry names — `10-foundations/01`'s motto is
unchanged on that basis alone. The wording itself needs no revision: "bound what the
model can make worse" is the ceiling, read from below, not a floor separate from it,
and dloop's higher ceiling *is* that bounding (0 regressions vs 7, 0 crashes vs 4,
5/5 correct declines), not a separate mechanism protecting a ceiling raised some
other way.

### P4 — The suite measures a verb the use cases did not name (2026-09-03)

The requirement uses three verbs: **consolidate, evaluate, organize**. The M6
suite measures a fourth: **implement**. Every one of its 30 tasks arrives
pre-triaged, pre-scoped and pre-justified — the expensive part of the real job is
done by the fixture author before any arm runs.

The ruler is good for what it measures. It cannot see four of the five wanted
projects, and it cannot see the ticket-triage case at all.

### P5 — Investigation must be legible as progress (2026-09-03)

From the friction loop: investigation is under-estimated, therefore feels like
non-progress, therefore produces frustration that degrades organization and
raises friction.

Therefore a system requirement almost nobody builds for: **the system must render
investigation as a result.** "Four hypotheses eliminated, here is why, here is the
one that survives and the evidence needed to settle it" is a *deliverable*, not a
failed attempt to produce a patch.

**The apparatus already exists.** `10-foundations/03` — observation / evidence /
finding / decision, *"a conclusion is not an observation"* — is exactly the
vocabulary that makes eliminated hypotheses countable. The M2 record was built to
audit the system; it doubles as an instrument for making invisible work visible.
That was not a designed benefit and it may be one of the larger ones.

### P6 — This repository is a legitimate fixture (2026-09-03)

"Keeping things tight and organized" is the named 15× target. This repository is
a live, non-confidential, continuously human-judged instance of exactly that
work, available today, with none of OQ-2's data-policy problem.

Formerly posed as an open question; it is not one, and the self-reference is not
a joke. The relevant doctrine is already written: *"notice the symmetry; do not
design toward it"* (`30-adaptation-and-evolution/08`). A corpus that happens to
be at hand is a symmetry to **exploit cheaply**. It would become the failure that
document warns about only if the project started shaping the work to make the
self-reference hold — building for the fixture rather than using the fixture that
exists.

The discomfort is worth keeping as an alarm rather than resolving. It fires
correctly whenever a decision is being made *because* it is recursive rather than
because it is cheap.

### P7 — Capability flows into the scaffold; the scaffold substitutes for capital (2026-09-04)

Design obsolescence is not a threat to be answered — it is history running one
way, and the project has no stake in models staying weak. This position is
therefore about a *mechanism*, not a defence.

Distillation is the well-known channel by which capable models improve small
ones. There is a second, faster and more direct:

> **A capable model improves a small one by building its tooling — at 15×.**

Context assemblers, decomposition rules, deterministic gates, ladder fixtures,
scoring harnesses, documentation. None of it is weights. All of it is the
scaffold, and a capable model produces it far faster than a human can.

Two consequences, and the second is the important one:

1. Capability rise **accelerates** this project. The part being built is the part
   that improves fastest as models improve.
2. The product of that acceleration is a **hardened local scaffold** — and a
   scaffold is a *cheap* artifact. Once built it runs on hardware already owned,
   under local control, at no marginal cost per run.

That second point is the real claim, and it is not about shelter. The
constrained-intelligence thesis is usually read as *spend design to save model
capacity*. Its stronger form is **spend design to save capital**: a
well-scaffolded local model is an argument that frontier-scale work does not
require frontier-scale money.

Which is the operative form of the project's stated motivation — that this
capability *"need not be controlled and auditable only by those who wage war for
money."* Not an enclave to be defended from them. An argument that they are not
required.

Noted honestly: this session is an instance of the mechanism. That is the P6
alarm firing, and it clears — the observation is cheap and true, not chosen
because it is recursive.

**Caveat kept open.** An earlier draft leaned on institutional barriers being
durable — places a hosted model cannot go. That premise is not safe: *some doors
you think are locked.* The position above deliberately rests on the capital
argument instead, which does not require any door to stay shut.

### P8 — Convergence before implementation, with a task-scaled artifact (2026-09-04)

`03-how-the-field-frames-it.md` establishes that the field's remedy has two halves
and dloop is only one: verification-in-the-loop is solved, **preserved human
comprehension is not**, and an autonomous loop plausibly worsens it. P5 named the
requirement. This is the mechanism.

> **Standardise the process — converge on a shared artifact before implementing.
> Vary the artifact, not the process.**

What "documentation and spec" denote is task-dependent: sketching a plotting
script, reworking project documentation, and shipping a feature into a production
environment need the same *step* and completely different *objects*.

#### Why this is not spec-driven development

SDD's documented failure (`03` §5) is firing decomposition **unconditionally** at
a **fixed, heavy** artifact — 4 user stories and 16 acceptance criteria for a bug
fix. Two different fixes are available, and the choice matters:

| fix | what varies | cost of getting it wrong |
|---|---|---|
| **skip the step** (Claude Code: *"if you could describe the diff in one sentence, skip the plan"*) | **whether** convergence fires | reintroduces the comprehension gap on exactly the high-volume small tasks where debt accumulates fastest |
| **scale the artifact** (this position) | **what form** convergence takes | a slightly over-heavy artifact costs some minutes |

The second is preferable on an asymmetry: never skipping means a comprehension
trace exists at *every* size, and mis-sizing degrades gracefully where skipping
does not. It replaces a binary with a continuum.

#### The spectrum

| task | artifact |
|---|---|
| sketch a plotting script | one line: objective + how we will know it worked |
| small fix | + constraints, and what "done" means |
| production feature | + affected surfaces, what must not change, rollback |
| architecture / tradeoff analysis | + alternatives considered and why rejected |
| documentation rework | **the artifact is the deliverable** — spec and output collapse |

#### What it buys, beyond comprehension

The same object serves four purposes the system needs anyway:

1. **The comprehension surface** — the human reads *this*, not the diff. Half two.
2. **The escalation payload** — M7's open design question is *"how does the
   assistant ask for the one thing it cannot decide."* A convergence artifact
   that fails to converge **is** that question, already written down.
3. **A memory-promotion candidate** — `10-foundations/05` needs something to
   promote; a converged artifact is a natural entrant.
4. **A shape for non-code deliverables** — this partly answers **OQ-4**. If the
   evaluable thing is the *convergence* rather than the output, a tradeoff
   analysis acquires the same structure as a feature, and the five stalled
   projects in §1 get a form.

#### The risk that decides whether this works

**Whether the artifact adds anything.** ~~Framed initially as *who authors it*,
citing the ETH human-vs-LLM gap.~~ **Corrected 2026-09-04:** that study's
operative variable is **redundancy, not authorship** (`03` §5) — strip the
redundant material and machine-generated files outperform human-written ones. The
risk is therefore not *who typed it* but **whether anything entered that the
system did not already have.**

The correction does not weaken the risk; it sharpens it. What the study does
establish is that **non-additive content is actively costly, not neutral** —
agents obey it, spending 14–22 % more reasoning tokens and 2–4 extra steps on it.
So a convergence step where the agent drafts and the human rubber-stamps is not a
harmless formality that wastes a few minutes: it is a **negative-value step**,
measured. Which is also precisely the SDD complaint (*"I'd rather review code than
all these markdown files"*).

So convergence must be **actual convergence**: the human has to contribute
something the model could not have produced. Candidate: stakes, constraints
originating outside the codebase, what "done" means to whoever asked, history the
repo does not record — i.e. **exactly the above-ceiling context**
(`02-capability-as-granularity.md`). The artifact is where the Principia
authorship handoff becomes routine rather than heroic.

If the human's only contribution is assent, this is ceremony and should be
dropped.

#### Standing question on lifetime

`10-foundations/05` supplies the default: conversation is working memory,
knowledge is a published result. So the artifact is **ephemeral by default and
promoted only if it proves durable** — which sidesteps SDD's staleness failure
(specs that never update) without requiring a living-document discipline nobody
sustains.

**Status:** M7-shaped. This session deviated from M7 and produced a proposal for
its front half; the back half (dloop) is already settled. Not yet specified —
see OQ-7 to OQ-9.

---

## 5. Open questions

- ~~**OQ-1 — Is "investigate → synthesize → write up" the same faculty that failed
  in the judge-lab?**~~ **Dead end (2026-09-03).** The question presupposes
  *faculties* as the right ontology — that doing and judging are different
  organs, and one asks which organ investigation belongs to. If capability is
  instead a **granularity ceiling on context integration**, the faculty question
  dissolves: doing, judging and investigating are the same operation at
  different granularities. Superseded by `02-capability-as-granularity.md`.
- **OQ-2 — Can the ticket corpus be used at all?** It is the single best ground
  truth available (real requests, real resolutions), and it is real user data at a
  large company: PII, policy, and approval questions apply *even for local-only
  use*. If the answer is no, the triage experiment needs a synthetic or
  sanitised substitute and loses most of its value.
- **OQ-3 — Does the Amdahl split hold?** If code-writing is ~15 % of a request's
  wall-clock, 15× on it is 1.2× overall. Needs an actual measurement, even a
  rough one, on a handful of real closed requests.
- **OQ-4 — What is the unit of evaluation for a non-code deliverable?** There is
  no deterministic sub-second check for "did this tradeoff analysis reach the
  right conclusion." The M6 scoring model does not extend to it. Without an
  answer, the wanted projects cannot be measured and therefore cannot be
  improved on evidence.
- **OQ-5 — Does M8 need to precede M7?** M8 (persistent work and knowledge) scopes
  itself to "only as far as necessary to support **real use cases**" — it is the
  milestone that serves consolidate/evaluate/organize, it is explicitly gated on
  knowing the use cases, and it currently sits behind M7. Flagged, not proposed.
- ~~**OQ-6 — Is this project's own doc corpus a legitimate fixture?**~~ Not an
  open question; the answer is obviously yes. Promoted to **P6**.
**P8's open questions**, reworded (2026-09-04) — the first is the keystone, the
third is largely answered by prior art, and the fourth is the one that was
missing.

- **OQ-7 — Build a cheap detector for "not converged."** *The keystone.* One
  mechanism serves two jobs: it **terminates** convergence (without it, SDD's
  infinite markdown loop) and it **triggers escalation** to a heavier artifact
  (OQ-9). Requirements: decidable in seconds, no model call at the cheap end,
  and false-negative-biased — wrongly declaring convergence is worse than one
  extra round. Candidates to try: an unanswered-question count; an explicit
  *what-would-change-my-mind* line left blank; the human editing the artifact at
  all versus only assenting to it — ~~which is also the ETH authorship signal~~
  **(corrected 2026-09-04:** not an authorship signal; the study's variable is
  redundancy. Editing is still the best available proxy for *"did anything the
  system lacked enter here"*, which is the quantity that actually matters**)**.
- **OQ-8 — Decide what the cheap end is *for*, before building it.** Two
  incompatible claims, and they demand different artifacts:
  **(a)** per-task comprehension — the human ends the step understanding
  something they did not before. Implausible for a typo.
  **(b)** an inspectable accumulation — no single record teaches anything, but
  the *series* makes drift, repetition and scope creep visible in aggregate.
  If (b), the cheap artifact needs to be **uniform and machine-readable** rather
  than informative, and the design changes accordingly. Current lean: (b).
- **OQ-9 — Artifact form: probably no selector needed.** `03` §5b found
  **ADaPT** — decompose *on failure*, never by upfront classification, and depth
  comes out emergent. Transferred to P8: **start at the cheapest artifact and
  escalate when OQ-7's detector says convergence failed.** No blast-radius
  classifier, no upfront rule to get wrong. Cost is one failed cheap attempt,
  which is the right price. Open part: does as-needed escalation transfer from
  *task decomposition* to *artifact selection*, or does convergence differ in
  ways that break it?
- **OQ-10 — What closes the loop on convergence quality?** *The gap that was
  missing.* dloop closes on a test. **Convergence closes on nothing** — if the
  implementation succeeds, the artifact is not thereby shown to be good; if it
  fails, blame is unattributed between artifact and implementation. So the front
  half of M7 would ship unmeasured, which is exactly the criticism this project
  levels at everyone else.

  **This is not a new problem.** It is `10-foundations/04`'s open question —
  *how context quality is measured independently of final task success* — and
  therefore **Milestone 9's entire purpose**. A convergence artifact *is*
  human-authored assembled context. Two consequences: M9's metric work is a
  prerequisite for evaluating P8, not a later measurement chore; and P8 gives M9
  a concrete, human-authored artifact to develop metrics against instead of an
  abstraction.

---

## Output

**2026-09-04 — first promotion out of this folder.**
`00-design/10-foundations/07-the-integrated-system-and-its-operator.md`.

Carries the load-bearing form of P3, P7, the operator-dispersion discussion, and
the adopt-or-stratify findings from `03`. Two commitments now held by the design
set: **the integrated system (system + model + knowledge) is the unit of
evaluation**, and **the operator's performance is what is optimised** — with ease
of use as a primary objective, three design instructions (*ease of use is not a
side quest*; *you are not the operator*; *do not let the least expert user hit the
floor*), and a proposed **second structural layer above the invariant floor**
whose first occupant is **authorship preservation**.

Deliberately *not* carried across: lift and dispersion as measurements. They are
attempts to measure the commitment, and belong to the experiment plan
(`00-standing-position.md`) rather than to the commitment itself. The design
commitment must not be compressed into its benchmark.

Elaboration of the second layer is deferred by intent, not by oversight — see
that document's open questions.

_Remaining threads stay open. On close: where the rest went._
