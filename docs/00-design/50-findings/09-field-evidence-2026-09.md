# Entry 9 — Field evidence, September 2026

**Kind:** field entry. Not a milestone. No evidence question of ours, no
reconstructable run, no verdict — external work that parts of the design set now
rest on, recorded so those claims are citable and so their ageing is visible.

**Date:** 2026-09-05
**Re-verify by:** 2027-03-05, or before any of it is used to justify a new
commitment, whichever comes first.

## Standing reliability caveat

**This entry was first written from search-engine synthesis, not primary pages** —
network policy on the workstation blocked direct retrieval. That produced two
recorded errors: the ETH result in §3 was first recorded with its central finding
inverted (propagated to six places before being caught), and its benchmark name
and human-written figure were wrong (caught 2026-09-05).

> **Verification pass, 2026-09-05** (working retrieval;
> `70-THINKING/05-primary-source-verification.md`). §§1–7 were checked against
> primary sources or ≥2 independent ones and **substantially hold**; the section
> texts above now carry the corrections inline, and the **Addendum** at the end
> lists them. What remains unverified: the compaction-threshold and vendor-quote
> details behind §7's general claims, and one decomposition sub-claim. Treat
> figures in those as directional; the rest can be cited with a source check, not
> as unverified.

---

## 1. Outcomes vary far more between operators than on average

**Sources.** LinearB 2026 benchmarks (2.7M pull requests, ~4,800 teams; larger
figures appear in derived analyses). Faros AI (≈22,000 developers, two years).
CircleCI 2026.

**What they report.** Assisted changes merge at a much lower rate than unassisted
ones and wait far longer for review; they are roughly 2.5× larger at the upper
quartile. Completed work per developer rose substantially while production
incidents per change rose several times further, and changes merged with **no
review at all** rose by about a third. Feature-branch throughput rose while
median-team main-branch throughput fell. Against this, the strongest adopters
roughly doubled their merge rate over the same period.

**Why it is held.** The dispersion, not the central tendency. The same tooling
produces opposite outcomes depending on who is operating it.

**Reliability: low-to-moderate.** All vendor-published, none a controlled
experiment. The Faros cut compares the same organisations across periods rather
than randomising. Classification of "AI-assisted" is metadata-based and
threshold-configurable. Directionally consistent across three independent
vendors, which is the main reason to credit it at all.

**Touches:** `10-foundations/07` (Motivation).

---

## 2. Perceived speed-up is not evidence

**Source.** METR, July 2025 — a randomised controlled trial on experienced
open-source developers using early-2025 tooling.

**What it reports.** 16 developers, 246 tasks, randomised per task, working in
**their own** repositories (large, long-established, ~5 years' familiarity), with
Cursor Pro and Claude 3.5/3.7 Sonnet. Forecast +24 % speed-up; self-estimate
afterwards +20 %; measured **−19 %**, CI roughly [−40 %, −2 %].

**Why it is held.** Self-reported ease is disqualified as evidence of
performance, including this project's assessment of its own tooling.

**Reliability: high for what it measures, narrow in scope.** A genuine RCT, which
is rare here. But small N, and conditions close to the maximum-disadvantage case:
peak expertise, deep pre-existing context, and models two-plus generations old.
It does **not** support "AI makes developers slower" as a general claim, and the
authors say so.

**Touches:** `10-foundations/07` (open questions).

---

## 3. Context files: redundancy is the operative variable, not authorship

**Source.** Gloaguen, Mündler, Müller, Raychev, Vechev — ETH Zurich SRI Lab with
LogicStar.ai, *"Evaluating AGENTS.md: Are Repository-Level Context Files Helpful
for Coding Agents?"*, arXiv:2602.11988, February 2026 (v2 June 2026); MemAgents
ICLR 2026 workshop, 27 Apr 2026.

**What it reports.** *[figures verified against the paper 2026-09-05 — see
`70-THINKING/05`; benchmark name and the human-written figure were wrong in the
first draft and are corrected here.]* 438 tasks — SWE-bench Lite (300) plus a
purpose-built **CTXbench** (138, from 12 repositories that already carry
developer-written context files). Four agent/model pairs, three arms: no file,
generated file, developer-written file. Context files produced **no improvement
in task success at >20 % added cost**. Generated files reduced success in 5 of 8
settings (−0.5 % SWE-bench Lite, −2 % CTXbench); developer-written files gained
**+2.4 %, not statistically significant (p ≈ 0.21)**, on the one benchmark where
they could be compared, still at ~19 % added cost. Agents followed file
instructions at raised tool-use rates and spent ~10–22 % more reasoning tokens on
them, so the weak effect is not agents ignoring them.

**The load-bearing detail.** Removing material already available elsewhere in the
repository before generating the files made the generated ones **improve and
outperform the human-written ones**. The operative variable is **redundancy, not
provenance**. The authors' own recommendation is that context files state only
minimal requirements.

**Why it is held.** Content that adds nothing the assembly already holds is not
neutral — it is attended to, and costly.

**Reliability: moderate.** Workshop-reviewed venue and a contamination-resistant
benchmark. But small effects, one benchmark for the human-written arm, and a June
2026 revision exists. **Previously misrecorded here twice** — the original sign
inversion (see the standing caveat), and the benchmark name / human-written
figure (fixed 2026-09-05). The redundancy result is the robust part: strip
documentation from the repo before generating, and generated files improve ~2.7 %
and beat developer-written ones.

**Touches:** `10-foundations/04`, `10-foundations/07`.

---

## 4. Decomposition: cost, and two failure modes beyond cost

**Sources.** ADaPT (UNC Chapel Hill / AI2 / Saarland) on as-needed decomposition.
ARIES on decomposition depth. Böckeler (Thoughtworks) on spec-driven development.

**What they report.** *[source attributions corrected 2026-09-05 — see
`70-THINKING/05`.]* ADaPT attempts a task directly and decomposes only on
failure, recursively; depth comes out **emergent** rather than set — averaging
1.9 on depth-2 tasks and 2.8 on depth-3 — and is framed as adapting to both task
complexity and model capability. **ADaPT's own named limitation** is that the
decompose-or-not decision rests on the executor model's *self-assessed* success,
which inflates — over-30-point overestimation on one benchmark — so it recommends
external verifiers. ARIES (thought-graph puzzles) reports deterioration reaching
**4.12× on one synthetic sorting task**, concentrated in the aggregation step,
which is the majority of its policy-agent errors. Böckeler separates spec-first /
spec-anchored / spec-as-source, finds most tooling claims the higher levels and
delivers the first, and reports small fixes expanding into large artifact sets —
the failure being that the approach "doesn't scale across different problem
sizes." *(A third failure mode — "tangential success", sub-tasks done well but
off the goal — was recorded here as ADaPT's; it is not in any paper, it is an
uncited blog concern. Kept as a hypothesis elsewhere, removed from this entry.)*

**Why it is held.** Splitting is cheap and rejoining is not; the decision of when
to split cannot be made by advance classification, and is itself unreliable
because a model judges its own success poorly; and evaluating the composite is
where the cost concentrates.

**Reliability: moderate.** ADaPT and ARIES are academic with reported benchmarks;
Böckeler is practitioner analysis at a reputable venue. Benchmark domains are far
from this project's (household tasks, sorting puzzles), so the *mechanisms*
transfer by argument and the *magnitudes* do not transfer at all.

**Touches:** `10-foundations/01`.

---

## 5. Comprehension debt, and one documented reversal from autonomy

**Sources.** HumanLayer (Dex Horthy), *"Why Software Factories Fail"* / *"Harness
Engineering is not Enough"* (2026 talk and essay). For the term *comprehension
debt*: Addy Osmani / O'Reilly Radar *(the first draft credited Agoda; not
confirmed — corrected 2026-09-05)*.

**What they report.** A team ran fully autonomous agent-driven development from
July 2025 — agents shipping small and medium work against specs and tickets
without human review — and reverted after several months. The reported sequence:
an issue the agents could not resolve, a maintainer returning to a codebase they
had stopped reading, work they did not recognise, and an outage during recovery.
The remedy adopted was upfront investment in shared understanding, humans still
reading code, and automation used to compress the review cycle rather than remove
it. *Comprehension debt* names the underlying accumulation: developers understand
less of their own codebase as unread machine-written code builds up.

**Why it is held.** The cost of displaced authorship is comprehension, and it is
missed at the moment automation fails rather than gradually.

**Reliability: moderate for an anecdote, and unusually so.** A single team, and
the author sells tooling premised on the conclusion — an incentive that would
suppress this finding rather than manufacture it, and which he discloses. It is a
**reversal**: the position was tested before it was argued. Treated as an
existence proof of a failure mode, not as a measurement of its frequency.

**Touches:** `10-foundations/07`.

---

## 6. Relevant context beats maximal context

**Source.** Sourcegraph benchmark.

**What it reports.** Agents given a 100K-token codebase summary performed worse
than agents given 5K tokens of targeted retrieval.

**Why it is held.** Direct support for a position the design set already holds.

**Reliability: low-to-moderate.** Vendor benchmark. Note the comparison is **not
token-matched**, so quantity and relevance are confounded and it cannot separate
"less material" from "better-chosen material." A circulating figure attributing
~65 % of enterprise agent failures to context drift is weakly sourced and is not
relied on.

**Touches:** `10-foundations/04`.

---

## 7. Vendor documentation as admission

**Sources.** Published documentation for widely used coding agents.

**What it reports.** Recurring guidance across independent products: add only the
files that need editing, since too many degrade results; substitute a structural
map of a repository for its contents; skip the planning stage where the change can
be described in one sentence; hand off before the working window fills; and —
stated plainly in one vendor's manual — *hooks are for anything that must happen;
instruction files are requests, not guarantees.*

**Why it is held.** Several positions this project reached independently appear in
the field as **user-facing advice rather than system behaviour**. That convergence
is corroborating, and the gap between advice and mechanism is itself the
observation.

**Reliability: primary for what vendors claim, not for whether it is true.**
Documentation is direct evidence of a vendor's position and no evidence at all
that the position is correct. The ETH result in §3 is the standing reminder: a
practice can be near-universal, documented everywhere, and not work.

**Touches:** `10-foundations/01`, `04`, `06`.

---

## What this entry does not establish

It contains no measurement of this project's own system. Every claim here
concerns other people's tools, other people's codebases, and mostly other people's
models. It is background against which this project's own findings are read — not
a substitute for them, and not transferable to this project's configuration
without argument.

---

## Addendum — verification pass, 2026-09-05

Run with working retrieval; full record in
`70-THINKING/05-primary-source-verification.md`. The section texts above were
corrected inline the same day (the user authorised it); this addendum is the
change log.

**Verified against primary or ≥2 independent sources:** §1 Faros (epics/dev +66%,
incidents/PR +242.7%, unreviewed +31.3%, bugs/dev +54% — all exact), CircleCI
(+59% YoY is the *overall* average, not feature-branch; median-team main-branch
−7%), LinearB (merge 32.7% vs 84.5% exact; elite "≈2×" is raw, nets to ≈+10% org
after review cost). §2 METR (all figures confirmed; abstract carries no CI). §3
ETH — authors, dates, task/repo counts, 641-word average, LLM-generated
−0.5%/−2% at +20–23% cost, **the redundancy correction (strip docs first →
generated files +2.7% and beat developer-written)**, and the **MemAgents ICLR
2026 workshop** venue all confirmed. §6 Sourcegraph 100K-vs-5K exact. §7 AGENTS.md
60k+ projects under the LF Agentic AI Foundation; TodoWrite→Tasks API at Claude
Code v2.1.16, off-by-default on Sonnet 5 / Opus 4.8 from v2.1.233.

**What was corrected (now reflected in the sections above):**

- **§3.** Benchmark is **CTXbench**, not "AGENTbench". Developer-written gain is
  **+2.4%, p≈0.21 (not significant)**, not "~4%" (that was secondary coverage).
  "Obedience trap" is coverage/project vocabulary, not the paper's. Reasoning-token
  increase is +10–22% (GPT models). *The "ICLR 2026 workshop" was briefly flagged
  as unsourced during the pass; that flag was wrong — the venue is real.*
- **§4.** "Tangential success" is **not in the ADaPT paper** — it is informal
  secondary writing (a dev.to synthesis) and has been removed from this entry.
  ADaPT's actual named limitation — the executor model **cannot reliably judge
  its own success** (>30-point overestimation on WebShop) — replaces it, and is
  the more useful finding for `10-foundations/01`.
  ARIES's **4.12×** is one synthetic task (sorting64; sorting128 was 2.6×), not
  a depth-response curve; the aggregation-is-binding mechanism does hold.
- **§5.** *Comprehension debt* — attribute to **Addy Osmani / O'Reilly Radar**,
  not Agoda (no Agoda origin found; the term's coverage also re-conflates the
  METR −19%).

**Not re-checked** (OQ-1 stays open only for these): compaction-threshold table,
Cline memory-bank quotes, Aider repo-map internals, the "5 of 6 trials"
decomposition claim (source not locatable), and the `00-standing-position.md`
corpus figures (GitBugs / validity corpus / Debian BTS).
