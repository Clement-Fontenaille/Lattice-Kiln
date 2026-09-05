# How the Field Frames It

**State:** OPEN
**Opened:** 2026-09-04
**Serves:** `01-use-cases.md` §3 (community positions), and bears on §2.

## Method and its limits

Survey of major coding-agent frontends: official documentation, product
positioning, and practitioner/community discussion, read with vendor rhetoric and
interface mechanics deliberately separated.

**Limitations, stated up front because they affect how much weight this carries:**

- Direct page fetching was blocked by network policy on the workstation. Sources
  reached **through search-engine synthesis**, not by reading primary pages.
  Quotes are therefore second-hand and specific figures should be re-verified
  against primaries before being cited anywhere load-bearing.
- Source mix is uneven: peer-reviewed work, vendor blogs, and individual
  practitioner posts. Provenance is marked per claim below.
- Several vendors' own numbers describe their own customers. Marked where known.

This is **positioning and documented practice**, not a feature comparison. Feature
tables date in weeks; the assumptions behind an interface do not.

---

## 1. The only axis that matters: what unit of work does the interface assume?

Feature lists obscure the real division. Sorted by the **unit the interface takes
as its objective**, the field collapses into very few positions:

| unit of work | tools | what the interface is shaped around |
|---|---|---|
| **the next line** | Tabby, Copilot completions, Continue (autocomplete) | a cursor position; no objective at all |
| **the turn** | Continue chat, Cursor Ask | a question about code |
| **the diff** | Cursor Agent, Cline, Aider, Claude Code, Codex CLI, Windsurf | a described change to a codebase, ending at a reviewable diff |
| **the spec → diff** | Kiro, GitHub Spec Kit, BMAD, OpenSpec, Tessl | same terminus; a written artifact inserted before it |
| **the issue → PR** | Copilot coding agent, Jules, Devin, OpenHands | a tracker item in, a pull request out |
| **the fleet** | OpenHands Agent Control Plane, Cline Enterprise | many of the above, with policy, audit and cost attribution |

**Nothing in the field takes the backlog as its objective.** Even the issue→PR
tier consumes a *single, already-triaged* item; the triage that produced it is
assumed done, and the terminus is still a diff. The most useful framing found in
the whole survey came from a practitioner post describing the failure directly:

> An agent working on a feature that hits an obvious unrelated bug two lines away
> doesn't stop, doesn't file a ticket, doesn't mention it — because the task is
> the feature, not the bug.

That is named as *correct prioritisation given a single objective*, not
disobedience — and it is exactly the shape of `01-use-cases.md` P4. **An agent
whose objective is the backlog rather than the diff is a different product**, and
the survey found no one building it. Triage exists only as a bolt-on feature
(Codex "Automations" for scheduled issue triage; Claude Code triage skills;
GitHub Actions that label issues on open).

---

## 2. Rhetoric versus mechanics

Paired, because the gap is the finding.

| what is said | what the interface actually does |
|---|---|
| Cline: memory "resets completely between sessions — this isn't a limitation, it's what drives perfect documentation" | there is no memory. The user maintains markdown files re-read at every task start, and **must manually say "update memory bank" before the window fills** |
| "Repository-wide understanding without manual file selection" (Cursor indexing) | RAG over embeddings; the agent sees files named in the conversation plus auto-associated dependencies. Default agent-mode file reads are partial (~250 lines, extended on demand) |
| Spec-driven development as "living specifications", "specs as source of truth" | Böckeler's taxonomy — *spec-first* / *spec-anchored* / *spec-as-source* — finds **most tools claim the higher levels and deliver only spec-first**. Kiro and Spec Kit specs are static and do not update as implementation evolves |
| "Autonomous agents that ship features" | HumanLayer ran genuinely lights-off from July 2025, and reverted after months: an unsolvable issue, a codebase nobody had read in months, "slop code", and an outage during the debug |
| Context files make agents project-aware | the one controlled evaluation found **no success-rate improvement and >20% added cost** (below) |
| Model-agnostic / BYOK / "runs local" | true, and the quality gap at 7B–13B is acknowledged in the same breath by the same sources; local tiers are positioned on *control*, never on capability |

The most honest line found in any vendor documentation, and the one with the most
architectural content:

> **Hooks are for anything that must happen; CLAUDE.md and skills are requests,
> not guarantees.**

That is `10-foundations/06`'s enforcement-not-statement distinction, arrived at
independently and stated in a user manual.

---

## 3. What the interfaces make easy — and hard

**Easy, everywhere:** starting a change from a described intent; iterating on a
diff; running tests in-loop; reverting; restricting a session to read-only
(plan/ask modes); scoping instructions per-directory.

**Hard, everywhere:**

- **Carrying anything across sessions.** Every tool's persistence is a file the
  human curates. There is no promotion mechanism, no provenance, no aging, no
  contradiction handling. `10-foundations/05` describes machinery the field has
  not built.
- **Declining.** No interface is *shaped* around refusing work or reporting
  insufficient information. The closest found is a Jira orchestrator that moves
  under-specified tickets to "Blocked" with a comment naming what is missing —
  i.e. **decline-with-payload, built by a practitioner, absent from every
  product**.
- **Reporting non-diff results.** Nothing has a first-class output for
  "investigated, eliminated four hypotheses, here is the one standing." Output is
  a diff or a chat message. `01-use-cases.md` P5's requirement has no surface in
  any tool surveyed.
- **Cross-repository and cross-concern work.** Aider documents cross-repo as a
  workaround (`/read` from another repo, or dumping repo maps to files). Cursor
  degrades on large monorepos; sub-project opening is the advice.
- **Knowing when to stop.** Universal. Covered next.

---

## 4. The convergent practices, read as confessions

Every widely-documented practice compensates for something the interface cannot
do. Read as a list of admissions, the field has independently found most of this
project's results — and shipped them as **user-facing advice rather than system
behaviour**.

| documented practice | what it admits |
|---|---|
| Aider: *"only add the files that need to be edited… if you add too many files the LLM can get overwhelmed and confused"*; Cursor: *"including 20 files via @file when only 3 are relevant dilutes attention"* | more true context degrades outcomes — the removal effect, as primary user advice |
| Aider's **repo map** (signatures, classes, imports; PageRank over the dependency graph, `--map-tokens` budget); Cursor's embedding index | full fine-grained content does not work. **A coarse structural abstraction is substituted for it.** This is `02-capability-as-granularity.md`'s arm B, in production, for years |
| Claude Code: *"plan mode adds overhead… if you could describe the diff in one sentence, skip the plan"*; planning is for *"uncertain approach, multiple files, unfamiliar code"* | **a decomposition stopping rule** — hand-set, delivered as advice, never measured |
| Cline handoff at >50% context; auto-compact; `/newtask`, `/smol` | the working window is the binding constraint and it is managed, not solved |
| Cline: memory-bank files must be kept to a page — *"the Memory Bank itself consumes context"* | the compensation competes with the work it enables |
| AGENTS.md convergence: 60k+ projects, Linux Foundation stewardship, near-universal adoption | every agent needs durable project knowledge and none has any |
| *"Hooks are for anything that must happen; CLAUDE.md is a request"* | prose instruction is not enforcement |
| Cross-model / second-instance plan review as recommended practice | single-model self-review is not trusted — the judge-lab finding, as folklore |
| Vertical slices over horizontal phases (*"AI defaults to horizontal phasing, delaying end-to-end feedback"*) | decomposition **shape** changes outcomes independently of decomposition amount |

The pattern is consistent and worth stating plainly: **the field has located the
same problems and resolved them into human discipline. This project's distinct
move is trying to resolve them into measured system behaviour.**

---

## 5. What the evidence says

The strongest material in the survey is where measurement contradicts practice.

### Context files do not work (independent, peer-reviewed)

Gloaguen, Mündler, Müller, Raychev & Vechev — ETH Zurich SRI Lab with
LogicStar.ai, *"Evaluating AGENTS.md: Are Repository-Level Context Files Helpful
for Coding Agents?"*, arXiv:2602.11988, Feb 2026. SWE-bench Lite (300 tasks) plus
**AGENTbench** (138 tasks from niche repos, built to dodge contamination), across
Claude Code/Sonnet 4.5, Codex/GPT-5.2 and GPT-5.1-mini, Qwen Code/Qwen3-30B-Coder;
three arms — none, auto-generated per vendor recommendation, developer-written.

Presented at the ICLR 2026 workshop on memory for LLM-based agentic systems.
438 tasks total; AGENTbench's 12 repos were chosen *because* they already carry
developer-written context files. Average context file: **641 words**.

- **No improvement in task success. Inference cost up >20%.**
- LLM-generated files **reduced** success in 5 of 8 settings (−0.5 % SWE-bench
  Lite, −2 % AGENTbench; +20–23 % cost).
- **Human-written files: +4 %** (+19 % cost), AGENTbench only.
- Agents follow context-file instructions at **1.6–2.5× baseline tool-usage
  rates** — the weak effect is *not* agents ignoring the files. Whether human- or
  machine-written, they spend 14–22 % more reasoning tokens and 2–4 extra steps.
- Mechanism: unnecessary requirements make the task harder. Dubbed **"the
  obedience trap."** Authors' own recommendation: context files should state
  **only minimal requirements**.

**Correction (2026-09-04) — the authorship reading was wrong, and it had already
propagated.**

An earlier version of this section concluded *"the sign flips on authorship —
human-written helps, machine-written hurts,"* and cited it as external evidence
for `02`'s OQ-7 and the Principia constraint. **The same paper rules that reading
out.** When redundant material was removed before generating them, LLM-generated
files **improved by 2.7 % and outperformed the human-written ones.**

The operative variable is **redundancy, not provenance**: machine-generated files
reproduced what the repository already held elsewhere (README, docs,
CONTRIBUTING). Authorship was a *proxy* for parsimony, and the ablation breaks the
proxy. This is the finding that was missing, and it inverts the interpretation.

**What the study does support**, which is narrower and still useful:

1. **60,000+ projects and a Linux Foundation standard rest on an unvalidated
   practice.** Convergence is not evidence. Unaffected by the correction, and
   still the single most useful thing in the survey.
2. **Non-additive content is actively costly, not neutral.** Agents obey it,
   spending steps and tokens on it. Ceremony has a negative price. That is the
   premise `01`'s P8 needs — it does not require authorship to be causally
   special, only that the system can tell whether anything was added.

**Standing caveats:** small effects, one benchmark for the human-written arm, the
SRI Lab's own framing ("no improvement") is more conservative than secondary
coverage's ("+4 % for human-written"), and a v2 revision (June 2026) may differ
from v1. **All of the above is still search-mediated — the paper has not been
read directly.** See OQ-1.

### Less context, better results (vendor benchmark — Sourcegraph)

Agents given a **100K-token codebase summary performed worse than agents given 5K
tokens of targeted retrieval.** Also circulating: ~65 % of enterprise agent
failures attributed to *context drift* — reasoning over the wrong tokens — rather
than model capability. The framing: *"the bottleneck isn't what an agent could
know, but what it's forced to look at."*

This **retires the removal test for good** (`02`, already withdrawn): the effect
is confirmed at scale by a third party. Note it does *not* test grain — 100K vs
5K is not token-matched, so amount and level are confounded. **The token-matched
grain-match test remains unrun by anyone.**

### Throughput rises; the system degrades (industry telemetry)

| source | finding |
|---|---|
| Faros AI (22,000 devs, 2 yrs) | completed epics/dev **+66 %**; **production incidents per PR +242.7 %**; unreviewed PRs merged to main **+31.3 %**; bugs/dev +54 % |
| CircleCI 2026 | feature-branch throughput **+59 % YoY**; **main-branch throughput for the median team fell** |
| LinearB 2026 (~8.1M PRs, 4,800+ orgs) | agentic PRs picked up **5.3× slower**; AI-assisted PRs **2.6× larger** (408 vs 157 LoC, p75) |
| CodeRabbit (470 OSS PRs) | ~**1.7× more issues** in AI-co-authored PRs |
| ~33,000 agent-authored PRs | non-merged agent PRs are larger, touch more files, fail CI more |
| study of 1.02M PRs / 207 projects | agent involvement → faster review decisions, **no improvement in review quality** |

**This is `01-use-cases.md` P3 at industry scale**, and it is not a marginal
effect: throughput up two-thirds, incidents per PR up two-and-a-half times. The
M6 monolith's 7 regressions and 4 crashes in 30 tasks is the laboratory-scale
image of exactly this.

*Caveats:* Faros compares the same companies across low- and high-AI periods, not
a controlled experiment. Several figures are vendor-published. HumanLayer, whose
essay popularised the Faros cut, sells a product premised on the thesis and
discloses it.

### The perception gap — corrected attribution, and it matters

**An earlier draft of this document attributed "feel 20 % faster, are 19 % slower"
to LinearB. That was wrong — two separate studies were conflated.** The figure is
METR's, and its conditions change what it can support.

**METR, July 2025** — *"Measuring the Impact of Early-2025 AI on Experienced
Open-Source Developer Productivity"* (Becker, Rush, Barnes, Rein). A genuine RCT,
which is why it carries weight:

| | |
|---|---|
| participants | **16 developers**, 246 tasks, randomised per task |
| repositories | **their own** — 22k+ stars, 1M+ LOC, avg **5 years' experience in that repo** |
| tooling | **Cursor Pro with Claude 3.5 / 3.7 Sonnet** |
| forecast → self-estimate → measured | +24 % → +20 % → **−19 %** (95 % CI ≈ [−40 %, −2 %]) |

Read the conditions rather than the headline. This is close to the
**maximum-disadvantage case** for AI assistance: maximal human expertise,
deep pre-loaded context, a codebase the developer already holds in their head,
and models two-plus generations old. It says a great deal about experts on
familiar ground in early 2025 and very little about a 2026 agent on an
unfamiliar twenty-year-old codebase. METR said as much themselves.

**LinearB is a different dataset with a different — and more interesting —
finding.** 2.7M PRs in the 2026 benchmarks report (8.1M+ in derived analyses,
4,800 teams). AI-assisted PRs merge at **32.7 % vs 84.5 %**; pickup 2.5–5.3×
slower; ~2.5× larger at p75. And:

> **Elite AI teams nearly doubled their merge rate in 2026, while developers
> using no AI stalled.**

**The variance is the story, not the mean.** Elite teams roughly doubled; the
median got worse; the aggregate looks bad. A wide distribution with a misleading
centre implies the differentiator is **practice, not tooling** — which is the
thesis this project exists to test.

*Method caveat:* LinearB classifies via metadata (AI agents as commit co-authors),
threshold-configurable, default 50 %. A competing vendor argues metadata alone
cannot identify AI-generated code. Time period and classifier models are not
stated in accessible summaries.

**Consequence for `01-use-cases.md` OQ-3:** the 15× is neither confirmed nor
refuted by any of this. What survives is narrower and still binding —
*self-reported speedup is not a measurement*, including this project's own. The
stopwatch on setup-time-to-first-signal (P2 mechanism B) is the answer, not
impressions of pace.

### What the elite/median spread actually means

An earlier draft read the spread as *"the differentiator is practice, not
tooling."* Two corrections and a question follow, and the question is the useful
part.

#### Correction 1 — practice and tooling are not independent

The dichotomy is false. Practice is *encoded in* tooling, and §4 of this document
is the evidence: the field's collective knowledge exists as **advice**, and the
teams that pull ahead are plausibly the ones who converted that advice into
**mechanism** — hooks, gates, CI, custom harnesses — rather than the ones who read
it more carefully.

The vendor line quoted earlier is the whole distinction in one sentence: *hooks
are for anything that must happen; CLAUDE.md is a request.* Elite teams write
hooks. Median teams write CLAUDE.md — and the ETH result says the file they wrote
may be making things worse.

So the axis is not practice-vs-tooling. It is **whether practice has been made
mechanical** — which is this project's stated distinct move, restated as an
adoption fact rather than a research position.

#### Correction 2 — the median may not be catching up, in either

The optimistic reading of a wide distribution is that it is a transition and the
median converges upward. That assumes diffusion. Two mechanisms argue against it:

- **The substrate precondition.** Making practice mechanical requires something to
  mechanise against: a test suite that sees the deliverable, CI, module
  boundaries clean enough to gate on. **You cannot gate on tests you do not
  have.** This project already observed the limit — the loop-lab finding that
  bundle D *"no-ops a behaviour-preserving refactor when the test can't see the
  deliverable."* A twenty-year-old codebase with thin coverage is not an
  unfortunate median case; it is the *typical* one, and it is exactly
  `01-use-cases.md` §1's setting.
- **The slack trap.** Converting practice into mechanism costs time. AI-induced
  review burden *consumes* time (pickup 2.5–5.3× slower, PRs 2.5× larger). The
  tool that would eventually buy the slack to build the mechanism takes the slack
  first. Same shape as §1's frustration loop, one level up.

Neither mechanism is measured here. Both are reasons not to assume convergence.

#### The question: what separates technologies that diffuse from ones that stratify?

The honest comparison is not AI-versus-nothing but **git versus testing** — two
development practices of obvious value, adopted with completely different
outcomes. Version control diffused to near-universality. Testing discipline did
not: coverage remains wildly stratified twenty-five years on. Both outcomes are
available.

Markers that appear to separate them:

| marker | diffuses | stratifies | agentic coding today |
|---|---|---|---|
| **floor height** | works when used badly (git) | needs skill to pay off (testing) | **high floor** — bad use actively harms: the obedience trap, more-context-is-worse, SDD overhead |
| **feedback timing** | fast, local (red/green, build breaks) | deferred, diffuse (design quality) | **inverted** — fast positive local signal (the diff works), slow negative distributed cost (comprehension debt, incidents) |
| **failure visibility** | legible (it doesn't compile) | invisible until late | **invisible at production time**, surfacing weeks later attributed elsewhere |
| **discipline required** | replaces a skill (compilers vs assembly) | adds one | **adds one** — more judgement to use well, not less |
| **who pays setup** | commoditised (package managers, CI-as-a-service) | each adopter | **each adopter builds their own harness** |

Four of five markers currently point at **stratification, not diffusion.** Which
supports Correction 2 with a mechanism rather than a worry.

**The one lever that flips it is the last row.** Technologies diffuse when someone
else pays the setup cost and the floor drops — packaged, not taught. Practice
becomes mechanism *for everyone* only when the mechanism is commoditised.

That is `01-use-cases.md` **P7**, arriving as the answer to a question it was not
written for: a capable model building scaffolding at 15× is precisely the
mechanism by which setup cost gets paid by someone other than the adopter. **The
median catches up when the practice is packaged, not when it is explained.**

*Caveat, stated plainly:* the table above is reasoning by historical
pattern-match, not evidence. It generates no prediction that has been tested
here. Its value is in naming which variable to watch — **floor height** — and in
supplying a reason to doubt the convergence story rather than a proof against it.

#### Making "packaged, not taught" measurable

*"Packaged, not taught"* is an explicit design objective and currently has no
progress measure, which makes it a slogan. Proposal:

> **Floor height = outcome variance across operator skill.**
> A packaged technology has **low** variance between skilled and unskilled
> operators. A taught one has high variance. Progress toward packaging is
> **declining dispersion**, not a rising mean.

This is directly measurable on apparatus that already exists. Hold the model and
the suite fixed; vary the **operator input** — expert-tuned prompts and
hand-selected context versus naive one-line requests — and report the spread. Two
arms worth running:

| arm | reads as |
|---|---|
| bare model + expert operator | what skill alone buys |
| scaffold + naive operator | what packaging alone buys |

**If the second approaches the first, the practice has been packaged.** If the
gap stays wide, it has only been automated for people who already knew it.

Note this is a **different quantity from rungs**, and the project needs both:
rungs measure the **lift** (how far the ceiling moved); dispersion measures the
**floor** (who can reach it). A scaffold can raise the ceiling and keep the floor
high — that is the stratifying case, and it would be invisible to rungs alone.

It also matches the field-level observation: LinearB's elite/median spread *is*
this metric, measured across organisations instead of across operators.

#### Structural responses to the other markers — with what is honestly available

| marker | structural response | honest status |
|---|---|---|
| **floor height** | measure dispersion across operator skill (above); target decline | **actionable now**, on existing apparatus |
| **feedback inverted** (fast positive local, slow diffuse negative) | report the **entropy term alongside the throughput term**, always and in the same place. M6 already scores regressions and declines per arm; the discipline is never publishing completion without them | **actionable, half-built** — the metrics exist, the reporting convention does not |
| **failure invisibility** | `10-foundations/06` already commits to failures being non-self-concealing, and M2 is the instrument. What is missing is specifically the **entropy** signals in the record, not more observability in general | **doctrine exists, instrumentation partial** |
| **discipline required** | the packaging problem again — same measure, same response | folds into row 1 |
| **who pays setup** | P7 | **stated, not yet measurable** |

Two things this project **cannot** fix, which are recorded so they do not
contaminate by oversight:

- **Comprehension debt is not solvable here.** A local scaffold cannot make an
  organisation read its own code. What is available is narrower and worth
  committing to: **do not make it worse** — which is what P8 exists for — and
  **measure it**, so the cost is not invisible. Claiming more would be dishonest.
- **The substrate precondition is a fact about the codebase, not the tool.** No
  scaffold gates on tests that do not exist. This bounds what any result here
  transfers to, and it should qualify every claim about applicability rather than
  being discovered later by a reader.

### Temporal validity — how long any of this holds

Every figure above describes a **snapshot of a fast-moving trend**, and the field
is not homogeneous: the same year yields "AI PRs merge at 32.7 %" and "elite AI
teams doubled their merge rate."

Rules for using this document:

1. **Always carry the tooling generation.** A finding from Claude 3.5-era Cursor
   is not a finding about 2026 agents. Where the generation is unstated, treat
   the figure as unusable rather than as weak evidence.
2. **Prefer direction and dispersion to level.** "Incidents per PR rose sharply"
   is more durable than "+242.7 %." Spread between best and median teams is more
   informative than either.
3. **Re-date before reuse.** Anything cited into `00-design/` should be
   re-checked against a current source, not carried forward on this document's
   authority.

### Where the field's remedy is converging — and how much of it dloop is

The remedy has **two halves, and dloop is one of them.** An earlier draft claimed
the convergence outright; that overstated it by reading half the picture.

**Half one — move verification into the loop.** *"The fix is not more review, but
moving validation into the development loop so every change arrives with proof it
works — shifting the burden of proof from reviewer to contributor."* Plus
risk-tiering, smaller diffs, stacked PRs. **This half is dloop**: test-gated
progress, incumbent protection, escalate-on-stall. Genuine convergence, reached
from operational pain rather than a 30-task suite.

**Half two — preserve human comprehension.** HumanLayer's *"turn the lights back
on"*: keep humans reading code, invest heavily upfront in shared understanding
(product review, architecture, program design, vertical slices), use AI to
compress the review cycle rather than remove it. Agoda's **"comprehension debt"**
names the failure: developers understand less of their own codebase over time as
AI-written code accumulates.

**Two readings of that account worth carrying forward** (interpretation, not
quoted findings):

- **The debt is called in at the worst moment.** HumanLayer's reported sequence —
  an issue the agents could not solve, a maintainer returning to a codebase they
  had stopped reading, "slop code", an outage during the recovery — is not gradual
  erosion. The comprehension is missed precisely when the automation fails, so the
  capability needed to recover is the one eroded by the thing now failing. A
  **correlated** failure, which is why comprehension cannot be traded against
  throughput: the trade looks free for exactly as long as it is not needed.
- **The evidence survives its source's incentive.** It is a *reversal* — the
  position was tested before it was argued — published by a party selling tooling
  in the opposite direction. That incentive would suppress the finding, not
  manufacture it. Horthy discloses it.

Also from that account, and load-bearing elsewhere: **the reward signal is
indifferent to maintainability.** Coding models are trained against binary
test-passing, under which a large passing change scores as well as a small one. So
restraint is not expected to arrive with capability — it has to be imposed by the
surrounding system. That is the argument for minimal-change being **structural**
rather than an expectation, and it now sits in `10-foundations/07`.

**Counterpoints kept:** HN commentary notes software factories handle anything
expressible as a one-liner requirement but have not solved intent and subjective
quality; and a stronger objection holds that language-to-code specification is
**inherently lossy**, which bounds how much `01`'s P8 front half can ever carry.

**dloop does not address half two at all — and arguably worsens it.** It is a
loop-control policy scoped to *one task*, whose success condition is a passing
test. It has no upfront-understanding phase, no human in the loop except
escalation, and no output that builds a reader's model of what happened. A dloop
that works perfectly produces **correct code nobody has read**, faster.

What dloop covers and does not:

| the problem | dloop |
|---|---|
| shipping broken code | **solves** — 0 regressions vs 7 |
| doing work that shouldn't be done | **solves** — 5/5 declines |
| knowing when to stop trying | **partly** — escalate-on-stall, `STALL_TOL` mis-tuned |
| diff size / reviewability | **untouched** |
| upfront shared understanding | **untouched** |
| human comprehension over time | **untouched, plausibly worsened** |
| the review seat itself | **untouched** — and the judge-lab says the seat is empty at 7B |

**Consequence.** The correct claim is *"dloop is half the field's remedy."* The
other half is `01-use-cases.md` **P5** — investigation legible as progress —
which is not a nice-to-have alongside the loop but the part of the remedy the
loop structurally cannot supply. That is a stronger argument for P5 than the
frustration loop it was originally derived from.

### Spec-driven development: decomposition without a stopping rule

The clearest natural experiment available for `02`'s Consequence 1.

- *"Kiro turned a small bug fix into 4 user stories with 16 acceptance
  criteria."* Spec Kit generated so many markdown files for a mid-sized feature
  that the reviewer never finished the implementation.
- *"A sledgehammer to crack a nut"*; *"a sea of markdown documents, long agent
  run-times and unexpected friction"*; **"I'd rather review code than all these
  markdown files."**
- Böckeler's verdict: the principle is sound, the tooling *"doesn't scale across
  different problem sizes"* — for complex features the discipline pays; for small
  tasks the overhead is disproportionate.
- Review burden **shifts** from code to artifacts rather than shrinking. Specs go
  stale. Comparison drawn to model-driven development, with the warning that
  spec-as-source risks combining inflexibility *and* non-determinism.

**Read through `02`: SDD fires decomposition unconditionally.** Its documented
failure mode is precisely "decomposing below the ceiling is pure cost," observed
at scale, with the field's own diagnosis — *doesn't scale across problem sizes* —
being a restatement of the missing firing rule. M4's fixed chain losing to the
monolith is the same result at N=8.

---

## 5b. How the field actually handles granularity

The question §1–§5 answered only by gesture. Six mechanism families exist. **Five
of them manage a context budget; one manages granularity — and that one is
academic, not shipped.**

### A — Externalised plan state (the todo list)

Claude Code's `TodoWrite`, Cursor and Cline equivalents. The agent writes a
task list at the start of multi-step work and updates item status as it goes
(`pending` → `in_progress` → `completed`).

Two mechanical details matter more than the feature description:

- **State lives in the transcript, not in storage.** There is no read path; the
  model infers current state from the *response to updating* the list. One
  observer: *"really just a massive reinforcement tool."*
- **It is therefore subject to the very compaction it exists to survive.** The
  documented failure is exactly that: on compaction the agent loses track of
  in-progress work and decisions made. The community workaround is to externalise
  the canonical list to files (`plan.md` / `context.md` / `tasks.md`) with the
  in-session list as a working copy.

**This is not granularity management.** It is *goal persistence under context
churn* — keeping the objective alive while the window is rewritten. A different
problem, frequently conflated with granularity because both are called "context."

**The most interesting datapoint in the survey:** as of Claude Code v2.1.16
(Jan 2026) `TodoWrite` was superseded by a Tasks API, and on newer models the
task-tracking tools are **omitted by default** — the models track multi-step work
without a written list. *The scaffold was removed when the ceiling rose.* That is
a measured instance of `02-capability-as-granularity.md`'s lift going to zero for
one specific scaffold across one model generation, and the closest thing in the
survey to a rungs-of-lift observation.

### B — Context isolation (subagents)

A parent spawns a child with a **fresh** window, its own system prompt, its own
tools, its own permissions. The child works, and returns **one text result**; the
parent never sees the intermediate tool calls. Stated contract:

> **The parent should receive only the conclusion, not the work that produced it.**

That is the grain hypothesis as a shipped design principle. The parent is handed
an *abstraction* of the child's work, not a truncation of it.

Three properties worth recording:

- **Token cost is not reduced.** Every subagent is a separate call; parallel is
  not cheaper than sequential. **Only the parent's window is protected.** So the
  benefit cannot be "fewer tokens are cheaper" — it is that a clean parent window
  works better. Suggestive for grain-over-amount, though still confounded: the
  returned conclusion is both coarser *and* smaller than the trace.
- **The parent must over-specify the handoff.** The child starts blank and
  invocations are one-shot, so goal, file paths, errors, structure and
  constraints must all be passed. **The cost of isolation is paid in authorship of
  the handoff** — OQ-7's cost line, in a product.
- **Documented negative guidance:** skip subagents for quick targeted fixes, for
  files already in context, and for tasks needing frequent back-and-forth.
  A hand-set firing rule, again shipped as advice.

### C — Compaction (lossy summarisation at a threshold)

Universal, and the thresholds differ enough to be informative:

| tool | fires at |
|---|---|
| Gemini CLI | ~50 % |
| Roo Code | ~86–92 % |
| Claude Code | ~89 % (window − min(max_output, 20k) − 13k) |
| Codex CLI | ~90 %, hard ceiling, configurable **downward only** |
| OpenCode | ~96–99 % |

Claude Code is layered rather than single-trigger — snip → microcompact →
collapse → auto-compact — and trims oversized tool results (default 50k chars →
~2 KB preview plus a persisted path) *before* summarising. OpenCode prunes before
it summarises, protecting the last 40k tokens of tool output. Codex preserves the
last ~20k of user messages and **warns in its own documentation that repeated
compaction reduces accuracy.**

The practitioner consensus is the striking part: **compact at ~60 %, not at the
mechanical threshold.** *"Early firing trades context utilisation for stability,
preventing the quality cliffs late-firing agents risk."*

Which is a field-wide, informally-held claim that **the effective ceiling sits
far below the nominal window** — and that degradation is gradual enough to be
felt but not measured. `02`'s OQ-3 (sharp or soft?) has a folk answer here:
*soft, and it starts early.*

### D — Explicit handoff

Cline's `new_task` at a documented >50 % context threshold; HumanLayer's
"intentional compaction" (deliberately write progress to a file and restart).
Same as C, but the boundary is chosen rather than triggered, and the summary is
authored rather than generated. ~~Which, per the ETH sign flip, may be the whole
difference.~~ **Corrected 2026-09-04:** authorship is not the operative variable
(see §5). If handoff beats compaction it should be because a chosen boundary and
an authored summary carry **less redundancy** than an automatic one — testable,
and not established.

### E — User-externalised files

Memory banks, `plan.md`/`context.md`/`tasks.md`, AGENTS.md. Covered in §4 and §5;
the ETH result applies.

### F — Failure-driven recursive decomposition (the one that is actually about granularity)

**ADaPT** — *As-Needed Decomposition and Planning*, UNC Chapel Hill / AI2 /
Saarland. The rule this project has been circling, arrived at from the other
direction:

> Try executing the task directly. If it succeeds, return. If it **fails** and
> depth < max_depth, decompose, recurse on the sub-tasks, combine.

**Depth is emergent, not fixed** — an average depth of 1.9 on depth-2 recipes,
scaling to 2.8 on depth-3 ones. Reported gains up to +28.3 % (ALFWorld), +27 %
(WebShop), +33 % (TextCraft). Explicitly framed as adapting to *both task
complexity and LLM capability* — the two-variable form `02` Consequence 1 needs.

**Its documented failure modes are the important part**, and two of them are
absent from `02`:

1. **Over-decomposition** — overhead. Already held.
2. **Tangential success — "arguably the most insidious."** The agent completes
   decomposed sub-tasks with high fidelity and the completion is *irrelevant to
   the original goal*, because each sub-task acquires its own optimisation target:
   *"do this sub-task well"* rather than *"move toward the goal."* **New to this
   project.** Decomposition does not merely cost overhead; it can dissolve the
   objective.
3. **Aggregation cost at depth** — ARIES reports up to **4.12×** performance
   deterioration as depth rises, concluding that aggregation reliability is the
   binding constraint: *if merging sub-task outputs is error-prone, deeper
   decomposition actively hurts.* **Also new, and it may be the more important
   of the two.**
4. **Agents under-split when left to choose.** In one study they fused stages,
   dropped others, and replaced a classification stage with a fixed threshold in
   5 of 6 trials.

**Notably, F is not in any product surveyed.** Every shipped mechanism is reactive
context-budget management with thresholds tuned to the *window*; ADaPT tunes to
the *task*, and predates all of them.

### What this answers

The frontends address granularity **indirectly**, as a budget problem. The
observation that they "maintain an internal todo list that can be interrupted and
refined mid-flight" is accurate and describes family A — which turns out to be
about goal persistence, not granularity, and which is now being *removed* as
models improve.

The gap is unchanged and better located: **nobody ships a decomposition rule
conditioned on the task.** The literature has one.

---

## 6. Where this leaves the project

### Confirmed from outside

- **P3 — entropy reduction is the product.** Industry telemetry is unambiguous and
  the magnitudes are large. The remedy the field is converging on is dloop's.
- **`02` Consequence 1 — decomposition needs a stopping rule.** SDD is the
  counterexample being lived through publicly.
- **Foundation 04 — relevant beats maximal.** Now over-determined: Aider's docs,
  Cursor's docs, Sourcegraph's benchmark, the ETH paper.
- **Foundation 06 — enforcement, not statement.** Shipped in a vendor manual as
  *hooks vs requests*.
- ~~**`02` OQ-7 — authorship of the abstraction matters.** The ETH human-vs-LLM
  sign flip is external evidence.~~ **Withdrawn 2026-09-04** — the study's
  operative variable is redundancy, not authorship (see §5). OQ-7 keeps its two
  *argued* legs (the Principia position constraint; assent adds no information)
  and **loses its empirical one**. Moved to "Challenged".

### Challenged

- **The 15× expectation.** A 39-point perception gap in the largest dataset
  available. OQ-3 needs a stopwatch, not an impression.
- **Novelty.** Much of what felt discovered here is documented practice
  elsewhere — the removal effect, coarse abstraction over source (repo maps), the
  plan-only-if-uncertain rule, cross-model review. **The findings are confirmed
  rather than original.** What remains distinct is narrower and should be stated
  that way.
- **Vocabulary.** The field calls this **context engineering** (*"curating what
  the model sees so that you get a better result"*). `10-foundations/04` says the
  same thing in different words. Adopting the term costs nothing and buys
  legibility.

### Still unoccupied

1. **A measured stopping rule.** Refined after §5b, because ADaPT exists and the
   original wording was too broad. The accurate three-tier version:
   - **Shipped tools:** reactive context-budget management, thresholds tuned to
     the *window*. No task-conditioned rule at all.
   - **Literature (ADaPT):** an as-needed, failure-driven rule tuned to the
     *task* — the right control structure, validated, and **not shipped by
     anyone.** That gap between literature and product is itself a finding.
   - **Nobody, anywhere:** a **measured bound**. ADaPT caps recursion with a
     hand-set `max_depth`; the documented mitigation for over-decomposition is
     *"set a max depth and check whether decomposition adds value."* A magic
     number plus an unspecified check.

   The unoccupied space is therefore narrower and more precise than first
   stated: **calibrating the bound instead of choosing it.** Rungs of lift
   remains a unit no one in the survey has.
2. **Scoring a pipeline on entropy suppression.** Stated too strongly in an
   earlier draft ("nobody scores regressions"). Correcting to what the survey
   actually supports:
   - **Regressions are measured** — CI failure rates across ~33,000 agent PRs,
     issues-introduced (CodeRabbit, 1.7×), incidents per PR (Faros). SWE-bench-style
     pass/fail also captures breakage insofar as the suite catches it.
   - What the survey found **no instance of** is regressions-caused and
     correct-declines scored as an **arm-level design property** — "pipeline A
     causes N regressions, pipeline B causes zero, at equal task completion" —
     which is the M6 comparison.
   - **Declines look genuinely unrewarded:** in the SWE-bench family a correct
     refusal scores identically to a failure, so the dominant benchmark
     structurally cannot credit it. Stated as a structural observation, not a
     survey of every benchmark — see OQ-6.

   The distinction that survives: the industry measures entropy as an
   **outcome it observes**; M6 measures it as a **property of a configuration it
   chose**.
3. **The backlog as objective.** No product takes it. Triage is a bolt-on
   everywhere it appears.
4. **Investigation as a first-class deliverable.** No interface has a surface for
   it (P5).
5. **The token-matched grain-match test.** Nobody has separated *amount* from
   *level*. It remains `02`'s one live discriminator.

### The governance layer — built and sold, but not the same layer

**Correction (2026-09-04).** An earlier draft called the safety architecture "the
part least worth building here, since it exists and can be adopted." That was
wrong, and wrong in a way worth recording: it conflated **containment of effects**
with a **constraint on the optimisation process**.

What is genuinely built and sold: **OpenHands' Agent Control Plane** — policy
enforcement, isolated sandboxes, complete logging, every action traceable, cost
attribution per workflow, self-hosted / VPC / air-gapped. **Cline Enterprise** —
seat-level SSO / RBAC / audit, air-gapped client deployment. **Tabby** — fully
self-hosted completion.

The distinction that collapsed:

> **A sandbox stops a bad effect. The invariant layer stops the system from
> concluding that a bad effect is good.**

Containment sits **downstream** of cognition — it catches what the system decided
to do. The invariant layer sits **upstream** — it bounds what the system may
conclude is worth doing, and it is read by every loop while writable by none
(`10-foundations/06`). Foundation 06's own membership test explains why one is
purchasable and the other is not: *could any loop author this without being inside
the scope it is meant to constrain?* An ops team can author a sandbox policy from
outside the loop, which is exactly why it can be bought. Nothing outside the
system can author what the system is *for*.

So the real question is the one worth working: **which documented features of
these products belong in the design, and for each — implement, interface, or
delegate?** First pass:

| | what | why |
|---|---|---|
| **Delegate** | sandboxed execution and isolation; container lifecycle; RBAC / SSO; secrets handling; network egress control; cost metering | solved, commodity, no design content. Building any of it is pure cost |
| **Interface** | audit sink; a generic policy-enforcement engine; fleet orchestration | the project's semantics are **richer**, so they must emit *into* these rather than be replaced by them. An ops audit log records what happened; M2 records what was **believed and why** (observation / evidence / finding / decision, `10-foundations/03`). You can derive the former from the latter, never the reverse. Same for the gate: the deny-list is a specific deterministic artifact that can express itself to a policy engine without being one |
| **Implement** | the invariant layer itself; the capability/authority model bound to processor roles; the effect vocabulary; deny-list gate semantics; **decline and escalation as first-class outcomes**; provenance semantics | none of it is sold, because none of it is a security control. It is constitutive of the system's shape — and `01-use-cases.md` P4 already found the field has no surface for declining |

Two things follow. The commercial layer is a **deployment target, not a
substitute** — and it is worth designing toward, since interfacing cleanly with an
ACP-style control plane is a plausible route into an institution that already
has one. And the fact that enterprises purchase the containment layer says what
they can *buy*, not what they *need*; the alignment constraint has no vendor
precisely because no vendor can author it for them.

---

## 7. Open questions

- **OQ-1 — Re-verify the primaries.** Everything above is search-mediated. Before
  any of it is cited in `00-design/`, read arXiv:2602.11988, the Böckeler article,
  the Faros/LinearB reports, and the vendor docs directly.
- **OQ-2 — Does the ETH result hold at 7B?** Their local arm was Qwen3-30B-Coder.
  If context files hurt *more* at smaller sizes, that is a granularity result and
  it is directly measurable on the M6 suite with the existing CLAUDE.md-style
  fixtures.
- **OQ-3 — Is "the backlog as objective" unoccupied because it is hard, or
  because it does not sell?** A tool that declines work is hard to demo and hard
  to price. That would be a market fact rather than a technical one — and it
  would make the space durably open to a project that does not have to sell.
- **OQ-4 — Adopt "context engineering" as the project's term?** Costs nothing,
  buys legibility, risks importing the field's assumptions along with its
  vocabulary.
- **OQ-5 — Does anything change if the ceiling-probe ladder is run against a
  *fleet* rather than a model?** OpenHands-style control planes make
  many-agents-with-policy a real configuration to measure, not a thought
  experiment.
- **OQ-6 — Verify the decline claim.** "No benchmark credits a correct refusal"
  is asserted from the structure of the SWE-bench family, not from a survey.
  Abstention *is* measured in the general LLM literature; whether any
  coding-agent benchmark scores it needs checking before the claim is reused.
- **OQ-7 — Work the implement / interface / delegate split properly.** The table
  above is a first pass written from summaries. The real exercise is reading the
  ACP and Cline Enterprise feature documentation against `10-technical/03`
  (capability-authority) and `04` (enforcement gate), deciding each line, and
  recording what an interface contract to an external control plane would have
  to carry. That is a spec-shaped task, and plausibly M11 work
  (`01-MILESTONES/11-safety-response.md`).

## Output

_On close: where this thread's conclusions went._
