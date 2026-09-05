# What the External Evidence Actually Carries

**State:** OPEN
**Opened:** 2026-09-05
**Serves:** `00-design/50-findings/09-field-evidence-2026-09.md` (the field
entry), `03-how-the-field-frames-it.md`, and any design document that cites one
of these studies.
**Companion to:** `05-primary-source-verification.md` (which checked whether the
citations are *accurate*). This document asks the next question — **what each
study can actually bear**, and whether the thing the project wants from it is the
study's central result or a by-product.

## How to read the "signal strength" line

Every entry ends with one of three verdicts on the takeaway the project draws:

- **CORE** — the study was designed to establish this. It is the headline, it is
  powered, it survived whatever review the venue applies. Safe to lean on, within
  the study's scope.
- **SUPPORTED SIDE RESULT** — a real analysis in the paper, but secondary: a
  sub-group, a smaller N, an ablation, or a measurement the design allows but was
  not built around. Usable, with the weight turned down.
- **INTERPRETIVE / INCIDENTAL** — a mechanism sketch, a single example, a framing
  sentence, or a vendor's gloss on their own numbers. Directionally useful,
  citable as "consistent with", never as "shown".

The distinction matters here because several of the project's borrowed arguments
rest on the *incidental* layer of a study whose *core* is about something else.

---

## 1. METR — the productivity RCT

**Approach.** A randomised controlled trial, which is rare in this area and is
why it carries weight. 16 experienced open-source developers, 246 real tasks from
their *own* mature repositories (multi-year familiarity), each task randomised to
allow or forbid early-2025 AI tools (mostly Cursor Pro + Claude 3.5/3.7 Sonnet).
Completion time measured, not self-reported. The authors then collect evidence
against 20 candidate explanations for the result.

**Key findings.** Developers forecast a 24% speed-up, and *still* estimated a 20%
speed-up after finishing — while measured time went *up* 19%. The perception gap
is the striking part: roughly 40 points between felt and actual, in the same
people, on the same tasks.

**Why it applies.** The project's OQ-3 and the "15×" expectation are built on
impressions of pace, including the user's own. METR is the cleanest available
demonstration that impression and measurement diverge sharply and that the
impression is optimistic. It licenses one specific move: *do not accept a
self-reported speed-up as evidence, run the stopwatch* (P2 mechanism B).

**Where it does not reach.** It is 16 people, early-2025 models, on codebases they
already hold in their heads — close to the maximum-disadvantage case for AI
assistance. It does **not** show "AI makes developers slower" in general, and the
authors say so. Anything about 2026 agents on unfamiliar twenty-year-old code is
outside it.

**Signal strength: CORE** for the perception gap and the "measure, don't ask"
consequence. The −19% point estimate itself is CORE-but-narrow — real, powered,
and scoped to conditions the project's setting does not share.

---

## 2. ETH Zurich — "Evaluating AGENTS.md"

**Approach.** Task-completion evaluation of coding agents with and without
repository context files, in two settings: 300 SWE-bench Lite tasks with
LLM-generated context files, and CTXbench — 138 tasks from 12 Python repos that
already carry developer-written context files, built specifically to resist the
contamination that SWE-bench suffers. Four agent/model pairs, three arms (none /
generated / developer-written). Workshop paper (MemAgents, ICLR 2026).

**Key findings.**
1. Context files produce **no improvement in task success** and add **>20%
   inference cost**, across models, agents, and both authorship types. This is
   the headline and it is what the abstract leads with.
2. **Repository overviews specifically are not helpful**; instructions *are*
   followed. So the failure is not agents ignoring the file.
3. Developer-written files: **+2.4%, not significant (p≈0.21)** on the one
   benchmark where they were tested. (Secondary coverage rounds this to "+4%";
   the paper does not.)
4. **The redundancy ablation:** strip documentation-type files from the repo
   *before* generating the context file, and the generated file then improves
   performance ~2.7% and **beats the developer-written one**. Authorship was a
   proxy for parsimony; remove the redundancy and the proxy inverts.

**Why it applies.** Three project positions lean on this. `10-foundations/04`
(relevant beats maximal) — supported. P8's risk that a convergence artifact adds
nothing but ceremony — supported, and quantified: non-additive content is not
neutral, agents spend ~10–22% more reasoning tokens obeying it. And the withdrawn
`02` OQ-7 authorship claim — the ablation is what withdrew it.

**Signal strength.**
- Finding 1 (no benefit, +cost): **CORE.**
- Finding 2 (overviews specifically): **CORE.**
- Finding 4 (redundancy is the operative variable): **SUPPORTED SIDE RESULT** —
  it is an ablation, not the headline, but it is a designed comparison and it is
  the mechanism the authors offer. This is the one the project leans on hardest,
  so the weight should be honest: strong for an ablation, not the paper's
  centrepiece.
- Finding 3 (developer-written helps a little): **not a result** — n.s. Treat as
  "no measured benefit", not "+2.4%".

---

## 3. ADaPT — as-needed decomposition

**Approach.** An algorithm: attempt the task directly; if the executor LLM
reports failure and depth < max_depth, decompose into sub-tasks, recurse,
recombine. Evaluated on three interactive benchmarks — ALFWorld (simulated
household tasks), WebShop (web navigation), TextCraft (Minecraft-recipe
crafting). NAACL Findings 2024.

**Key findings.** Substantial success-rate gains over strong baselines: up to
+28.3% (ALFWorld), +27% (WebShop), +33% (TextCraft). Decomposition depth comes
out **emergent** — averaging 1.9 on depth-2 TextCraft recipes, 2.8 on depth-3 —
rather than fixed, and the paper frames the method as adapting to *both* task
complexity and model capability.

**The named limitation.** ADaPT's decompose-or-not decision rests on the
executor's *self-assessed* success, and that self-assessment inflates —
over-30-point overestimation on WebShop. The paper recommends external verifiers
or calibration. This is stated as a limitation of the method, in the paper.

**Why it applies.** ADaPT is the prior art for the rule `02` and
`20-cognitive-architecture/08` have been circling: decompose on failure, depth
emergent, tune to task *and* capability. That the rule is validated (in its
domains) is genuinely useful — it means the project is calibrating a known
control structure, not inventing one. And the named limitation is a direct hit on
`10-foundations/01`'s open question (*what makes a direct attempt count as
failed*) and on dloop's `STALL_TOL`: the trigger for decomposition cannot be the
model's own "am I done", because that signal is biased.

**Where it does not reach.** Household and crafting simulators are not software
engineering. The *magnitudes* (+28%, depth 1.9→2.8) do not transfer; the *control
structure* and the *limitation* transfer by argument.

**Signal strength.**
- As-needed decomposition beats fixed planning: **CORE.**
- Emergent-depth adapting to complexity and capability: **CORE.**
- Executor can't self-assess success: **SUPPORTED SIDE RESULT** — it is a stated
  limitation with one supporting number, not a studied phenomenon. But it is the
  paper's own admission, which makes it more solid than an outside inference.
- "Tangential success" (objective dissolution): **NOT IN THIS STUDY.** It is an
  uncited blog concern. Held elsewhere in the set as a hypothesis; it has no
  evidentiary backing at all and must not be cited as ADaPT's.

---

## 4. ARIES — decomposition depth and aggregation

**Approach.** A framework for LLM agents reasoning over "interactive thought graph
environments" — game-of-24, sorting, and similar puzzles where a policy agent
repeatedly transforms a graph of intermediate results. The relevant analysis is a
breakdown of *where* the policy agent's errors occur as task depth increases.

**Key findings.** On the hardest tested case (sorting a 64-element list),
performance deteriorated by up to **4.12×** as depth rose (2.6× on sorting128).
The deterioration concentrates in the **aggregation step** — recombining sub-results
— which accounts for 86% / 68% of all policy-agent errors on those tasks. The
paper's conclusion: if merging sub-task outputs is error-prone, deeper
decomposition actively hurts.

**Why it applies.** `02`'s "integrated system ceiling" and the depth-bound
candidate contribution both need it to be true that *recombination, not
execution, is the binding constraint on how far you can decompose*. ARIES is the
one piece of external evidence pointing that way, and the mechanism it describes
(each aggregation transformation carries its own failure probability; depth
multiplies them) is architecture-independent enough to borrow.

**Where it does not reach.** Sorting a 64-element list is about as far from
"investigate why job X crashed and write it up" as a benchmark can be. The 4.12×
is one number on one synthetic task; the project has repeatedly and correctly
refused single-number transfers.

**Signal strength: INTERPRETIVE / INCIDENTAL** for the project's use. The
*mechanism* (aggregation is where depth cost concentrates) is a SUPPORTED SIDE
RESULT within ARIES's own domain — a real error-attribution analysis. As
transferred to software work it is a plausibility argument, not evidence. The
"4.12×" should never appear in the design set as a magnitude, only as "observed
to be large on one synthetic task."

---

## 5. Faros AI — "The Acceleration Whiplash" (2026)

**Approach.** Two years of engineering telemetry from ~22,000 developers across
4,000+ teams, comparing outcomes as the *same* organisations moved from low to
high AI adoption. Observational, not randomised — a before/after on
self-selecting adopters, not a controlled experiment.

**Key findings.** Output rose: epics completed per developer +66%, task
completion +34%. Quality and control fell further: production incidents per PR
**+242.7%**, bugs per developer +54%, PRs merged with **no review at all** +31.3%,
median review time +441.5%, code churn +861%.

**Why it applies.** This is P3 ("entropy reduction is the product, not
throughput") at industry scale, and the magnitudes are not marginal — throughput
up two-thirds, incidents per PR up two-and-a-half times. The M6 monolith's 7
regressions and 4 crashes in 30 tasks is the same shape at laboratory scale. It
is the strongest external support for the project's central bet that a faster
entropy producer is not an improvement.

**Where it does not reach.** No randomisation; the high-AI period is also later in
calendar time (other things changed). Several figures are vendor-published, and
the essay that popularised this cut (HumanLayer's) sells a product premised on the
conclusion. Directionally corroborated by two other vendors (below), which is the
main reason to credit it.

**Signal strength: CORE** for the direction (throughput up, entropy up more) —
it is the report's entire thesis and it replicates across vendors. The **specific
percentages are INTERPRETIVE**: precise to the decimal in the report, but from an
uncontrolled before/after, so "+242.7%" is really "rose a lot".

---

## 6. LinearB — 2026 Software Engineering Benchmarks

**Approach.** Metadata analysis of ~2.7M pull requests across ~4,800 teams (larger
counts appear in derived analyses), classifying PRs as AI-assisted via commit
co-authorship metadata with a configurable threshold. Observational.

**Key findings.** AI-assisted PRs merge at **32.7%** within 30 days versus
**84.5%** for unassisted work; they wait far longer for first review pickup
(single-digit multiples; agentic PRs worst) and run ~2.5× larger at the upper
quartile. Against that: the teams leaning hardest on AI **merged ~98% more** of
their AI PRs year over year.

**Why it applies.** Two things. First, the merge-rate and size figures are P3
again — more change proposed, less of it good enough to ship. Second, and more
interesting for the project's *thesis*, the **dispersion**: the elite-vs-median
spread is enormous, which is the project's "practice, not tooling" /
"packaged, not taught" question measured across organisations instead of across
operators (`03` §5; `10-foundations/07`).

**Where it does not reach.** Metadata classification of "AI-assisted" is
contested — a competing vendor argues it cannot be done from co-authorship alone.
The elite "≈2×" is a raw merge-count ratio; LinearB's own analysis nets it down to
roughly +10% organisational gain once the added review time is subtracted. So
"elite teams doubled" is real but the *net* is modest.

**Signal strength.**
- Merge-rate gap (32.7 vs 84.5): **CORE** — it is the report's headline number.
- Pickup delay and PR-size inflation: **CORE.**
- "The variance is the story" / dispersion implies practice dominates: **INTERPRETIVE**
  — it is the project's reading of the spread, not LinearB's finding. LinearB
  reports the spread; the inference that it means *packaging beats teaching* is
  the project's, and `03`'s own Corrections 1–2 already walk it back partway.
- "Elite teams doubled": **SUPPORTED SIDE RESULT**, with the net-of-review-cost
  caveat mandatory.

---

## 7. CircleCI — 2026 State of Software Delivery

**Approach.** Aggregate analysis of ~28M CI/CD workflows across CircleCI's
customer base, year over year. Observational, platform-wide.

**Key findings.** Overall workflow throughput **+59% YoY** — but concentrated in
the top few percent of teams. For the median team, feature-branch throughput rose
~15% while **main-branch throughput fell ~7%**. Main-branch success rate hit a
five-year low (70.8%, against a recommended 90%).

**Why it applies.** It is the third independent vendor showing the same split:
activity up, delivery-to-production flat or down, quality of what reaches main
degrading. "Feature branches move faster, main moves slower" is exactly the
entropy/throughput divergence P3 predicts, and having it from CI telemetry
(rather than PR metadata or epic counts) is a genuinely different measurement of
the same effect.

**Where it does not reach.** Platform aggregates hide composition change (who
started using CircleCI, which projects got more active). The 59% is an average
dragged by a small top group — `03` currently mislabels it "feature-branch
throughput"; it is the overall figure. Corrected in this pass.

**Signal strength: CORE** for the median-team main-branch decline — it is the
report's framed headline ("more code, less software"). The +59% is CORE as a
number but **misleading without the distribution**, which is the report's own
point.

---

## 8. CodeRabbit — "State of AI vs Human Code Generation" (Dec 2025)

**Approach.** Automated review-tool analysis of 470 open-source GitHub PRs,
comparing issue counts in AI-co-authored versus human-only PRs across several
categories (logic, readability, security, formatting, error handling).

**Key findings.** AI-authored changes carried **~1.7× more issues** per PR (10.83
vs 6.45). Larger multipliers in specific categories: readability ~3×, security up
to ~2.7×. High-issue outliers much more common in AI PRs.

**Why it applies.** Direct, PR-level corroboration of the entropy claim, and
independent of the telemetry vendors — a different method (static review counts)
reaching the same place. Supports the M6 finding that ~1 task in 3 the monolith
makes things worse.

**Where it does not reach.** The "issues" are one review tool's findings, not
confirmed defects or incidents; CodeRabbit sells that tool. 470 PRs is a modest
sample. No control over task difficulty between the AI and human sets.

**Signal strength: SUPPORTED SIDE RESULT.** The 1.7× is the report's headline and
is cleanly stated, but the instrument (self's own tool) and the vendor incentive
keep it below CORE. Best used as "a third method agrees on direction."

---

## 9. "Where Do AI Coding Agents Fail?" (arXiv:2601.15195, MSR 2026)

**Approach.** Empirical study of ~33,000 pull requests authored by five coding
agents on GitHub, comparing merged and non-merged PRs on size, files touched, and
CI outcomes.

**Key findings.** Non-merged agent PRs are larger (~+17% LoC), touch more files
(~+10%), and fail CI more often (each failed check ≈ −15% merge odds).
Documentation / CI / build tasks merge best; performance and bug-fix tasks worst.

**Why it applies.** It characterises *what agent failure looks like at the diff
level* — bigger, broader, CI-breaking — which is the concrete texture behind P3
and behind dloop's test-gating and incumbent-protection. The task-type gradient
(docs merge, bug-fixes don't) is a useful prior for which of the user's five
stalled projects an agent could plausibly touch.

**Signal strength: CORE** for the merged-vs-not-merged differences — it is the
study's whole design. The task-type ranking is **SUPPORTED SIDE RESULT**.

---

## 10. 1.02M PRs / 207 projects (Zhong et al., 2026)

**Approach.** Large-scale observational analysis of AI *reviewer* adoption across
1.02M PRs in 207 projects — how review behaviour changes when an AI reviewer is
introduced.

**Key finding.** Agent-involved review is associated with **faster review
decisions but no measurable improvement in review quality**.

**Why it applies.** It is the counter to the optimistic "AI will absorb the review
load" story, and it bears on the judge-lab result: adding a model to the review
seat sped things up without making them better, which is the field-scale echo of
"the deterministic gate scores 9/10, the 7B panel drops it to 6/10."

**Signal strength: CORE** — it is the paper's headline result, on a large sample,
and it is a null (no quality gain), which is harder to overstate than a positive.
"No improvement" is exactly what it says.

---

## 11. Sourcegraph — context-engineering benchmark

**Approach.** Vendor benchmark: coding agents on identical tasks, given either a
~100K-token codebase summary or ~5K tokens of targeted retrieval.

**Key finding.** The 5K targeted-retrieval agents **outperformed** the 100K-summary
agents. Also cited: structural retrieval lifted precision@5 from 0.14 to 0.48 over
a grep baseline.

**Why it applies.** Third-party confirmation at scale of `10-foundations/04`
(relevant beats maximal), and it is what let `02` retire the "removal test" as a
falsifier — the effect is no longer in doubt, so it cannot discriminate the
granularity hypothesis.

**Where it does not reach.** 100K vs 5K is **not token-matched** — amount and
relevance are confounded, so it cannot separate "less material" from
"better-chosen material". The grain-match test (token-matched, level-varied)
remains unrun by anyone. Vendor benchmark, sells retrieval tooling.

**Signal strength: SUPPORTED SIDE RESULT.** Real, directionally clear, widely
echoed — but a vendor benchmark on a confounded comparison. Enough to retire a
falsifier; not enough to settle the grain question, which it does not address.

---

## 12. HumanLayer — "Why Software Factories Fail" (Dex Horthy, 2026)

**Approach.** A conference talk and essay. One team's account of running fully
autonomous agent-driven development from July 2025 and reverting after ~3 months.
Not a study — a narrated post-mortem, plus argument.

**Key content.** The reported sequence: an issue the agents could not resolve; a
maintainer returning to a codebase they had stopped reading; unrecognised
"slop" code; an outage during recovery. The remedy adopted: keep humans reading
code, invest upfront in shared understanding (product review, architecture,
vertical slices), use AI to compress the review cycle rather than remove it.

**Why it applies.** It is the concrete failure story behind P8's "half two" —
the comprehension half of the field's remedy that dloop does not touch. Two
properties make it worth more than a typical anecdote: it is a **reversal** (the
position was tested in practice before it was argued), and it is published by
someone whose commercial incentive runs the *other* way, and who discloses that.
The reading that comprehension debt is "called in at the worst moment" — when the
automation fails and the human most needs to understand the system — is the
project's interpretation, and it is a good one.

**Signal strength: INTERPRETIVE / INCIDENTAL.** N = 1 team, self-reported, by an
interested party. Treated correctly in entry 9 as "an existence proof of a
failure mode, not a measurement of its frequency." The comprehension-debt *term*
is Addy Osmani's / O'Reilly Radar's popularisation, not Agoda's and not from a
study. Use this to motivate P5 and the comprehension half of P8; never as
evidence of how often it happens.

---

## 13. Böckeler — spec-driven-development taxonomy (Thoughtworks / martinfowler.com)

**Approach.** Practitioner analysis in the "Exploring Gen AI" series. A taxonomy
plus observation, not measurement.

**Key content.** Three levels of SDD commitment: **spec-first** (spec written, then
abandoned after code ships), **spec-anchored** (spec maintained alongside code),
**spec-as-source** (humans never touch code; spec is the artifact). Observation:
most tools claim the higher levels and deliver spec-first; specs go stale; the
approach "doesn't scale across different problem sizes" — small fixes attract
disproportionate ceremony.

**Why it applies.** This is the natural experiment for `02` Consequence 1 —
decomposition fired unconditionally, at a fixed heavy artifact, failing exactly
where "decomposing below the ceiling is pure cost" predicts. It is also the
direct contrast case for P8: vary the artifact, not whether the step fires. The
"doesn't scale across problem sizes" line is a restatement of the missing firing
rule.

**Signal strength: INTERPRETIVE.** Credible practitioner synthesis at a reputable
venue, but it is taxonomy and observation, no data. Use it to *frame* the SDD
failure mode; the project's own M4 fixed-chain result is the actual evidence that
the pattern holds at N=8.

---

## 14. AGENTS.md convergence (adoption fact)

**What it is.** Not a study — a fact about the field. AGENTS.md, released by
OpenAI August 2025, is used by 60,000+ open-source projects and is a founding
contribution to the Linux Foundation's Agentic AI Foundation (formed December
2025).

**Why it applies.** Combined with the ETH result, it makes one clean point:
**60,000 projects and a Linux Foundation standard rest on a practice that
controlled evaluation says does not help.** Convergence is not evidence. This is
`03`'s single most durable observation and it is unaffected by any of the
corrections.

**Signal strength: CORE** as a fact (the numbers are from the LF announcement).
The inference — "widespread adoption ≠ validation" — is INTERPRETIVE but nearly
tautological given entry 9 §3.

---

## 15. Claude Code: TodoWrite → Tasks API (product-history fact)

**What it is.** Claude Code v2.1.16 (Jan 2026) replaced the TodoWrite tool with a
Tasks API; from v2.1.233 the task/todo tools are **off by default** on Sonnet 5 /
Opus 4.8 / Fable 5 and later, on the stated reasoning that those models track
multi-step work internally and the tool definitions cost context.

**Why it applies.** It is a real, dated instance of a scaffold being *removed
because the model got better* — the clearest field example of `02`'s "lift goes
to zero for a specific scaffold across a model generation", i.e. a rungs-of-lift
observation happening in production.

**Signal strength: SUPPORTED SIDE RESULT.** The version history and the vendor's
stated reasoning are verifiable fact. That it *demonstrates* the granularity
account's lift-decay is the project's reading — a good one, but the vendor did not
frame it that way and did not measure the lift.

---

## 16. SpackIt — "LLMs as Packagers of HPC Software" (arXiv:2511.05626)

**Approach.** An end-to-end framework (repo analysis + example retrieval +
iterative refinement with an error-aware repair loop of up to k attempts) for
generating Spack package recipes. Evaluated on 308 open-source HPC packages, with
Spack build/install success as the ground-truth signal.

**Key findings.** Install success rose from ~20% zero-shot to >80% in the best
configuration, driven mainly by the error-aware repair loop.

**Why it applies.** This is the **only domain-matched study** in the whole survey.
It is HPC software packaging — the user's setting (`01-use-cases.md` §1, project 1:
config-as-code management). It gives (a) a deterministic-ground-truth agentic
benchmark in the target domain, (b) direct evidence that a repair loop over build
errors is the thing that works — which is dloop's structure, in the user's own
problem space — and (c) a corpus lead (Spack issues) for the E-corpus question.

**Signal strength: CORE** for "error-aware repair loop moves install success from
~20% to ~80%" — it is the paper's headline and the ~20/~80 figures are its central
result (`00-standing-position.md`'s "19.7 / 82.9" are the precise values). The
transfer argument to *this* project is unusually strong here because the domain
matches, but it is still a different task (recipe generation, not investigation)
and should be cited as domain-adjacent, not domain-identical.

---

## What this changes about how the set uses the evidence

Three patterns, for the record:

1. **The telemetry (5–10) is strong on direction and weak on magnitude.** Every
   one is observational, several are vendor-published, none is randomised. The
   convergence across four independent vendors is what makes the *direction*
   (throughput up, entropy up more) safe to treat as CORE. Every specific
   percentage should be read as "large" / "small", and the design set should stop
   quoting figures like "+242.7%" as if they were measurements.

2. **The academic work (1–4, 9–11) is strong within scope and the scope is
   narrow.** METR is early-2025 experts on familiar code. ADaPT and ARIES are
   household and puzzle simulators. Their *mechanisms* are borrowable by argument;
   their *numbers* are not borrowable at all. The project already knows this
   (`09` §4 says so); the risk is that a number like "4.12×" or "+28.3%" gets
   repeated until it sounds like a result about software work.

3. **The project's sharpest borrowed claims sit on the incidental layer.**
   "Tangential success" had no layer at all (removed). "The variance is the story"
   is the project's reading of LinearB's spread, not LinearB's finding. The
   comprehension-debt argument is one team's post-mortem. These are worth keeping
   as *framing* and as *hypotheses to test on the project's own apparatus* — which
   is exactly what `70-THINKING` is for — but they should not migrate into
   `00-design/` as though they were established.

## Output

_On close: whichever of these framings the design set adopts, and where the
signal-strength verdicts are recorded against the citations in entry 9._
