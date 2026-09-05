# Entry 9 — Field evidence, September 2026

**Kind:** field entry. Not a milestone. No evidence question of ours, no
reconstructable run, no verdict — external work that parts of the design set now
rest on, recorded so those claims are citable and so their ageing is visible.

**Date:** 2026-09-05
**Re-verify by:** 2027-03-05, or before any of it is used to justify a new
commitment, whichever comes first.

## Standing reliability caveat

**No primary source below was read directly.** Network policy on the workstation
blocked direct retrieval; everything was reached through search-engine synthesis.
One consequence has already been observed: the ETH result in §3 was initially
recorded with its central finding inverted, and the error propagated to six
places before being caught.

Treat every figure here as **directional and unverified**. Per-claim reliability
is marked. Reading the primaries is owed work, not a formality.

> **A verification pass ran 2026-09-05** with working retrieval — see the
> **Addendum** at the end of this entry, and
> `70-THINKING/05-primary-source-verification.md`. Most of this entry verified;
> the corrections it did surface are listed there.

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
for Coding Agents?"*, arXiv:2602.11988, February 2026; ICLR 2026 workshop.

**What it reports.** 438 tasks — SWE-bench Lite (300) plus a purpose-built
AGENTbench (138, from 12 repositories that already carry developer-written
context files). Four agent/model pairs, three arms: no file, generated file,
developer-written file. Context files produced **no improvement in task success
at >20 % added cost**. Generated files reduced success in 5 of 8 settings;
developer-written files gained ~4 % on the one benchmark where they could be
compared, still at ~19 % added cost. Agents followed file instructions at 1.6–2.5×
baseline tool-use rates, so the weak effect is not agents ignoring them.

**The load-bearing detail.** Removing material already available elsewhere in the
repository before generating the files made the generated ones **improve and
outperform the human-written ones**. The operative variable is **redundancy, not
provenance**. The authors' own recommendation is that context files state only
minimal requirements.

**Why it is held.** Content that adds nothing the assembly already holds is not
neutral — it is attended to, and costly.

**Reliability: moderate.** Peer-reviewed venue and a contamination-resistant
benchmark. But small effects, one benchmark for the human-written arm, the SRI
Lab's own framing is more conservative than secondary coverage, and a June 2026
revision may differ from v1. **Previously misrecorded here** — see the standing
caveat.

**Touches:** `10-foundations/04`, `10-foundations/07`.

---

## 4. Decomposition: cost, and two failure modes beyond cost

**Sources.** ADaPT (UNC Chapel Hill / AI2 / Saarland) on as-needed decomposition.
ARIES on decomposition depth. Böckeler (Thoughtworks) on spec-driven development.

**What they report.** ADaPT attempts a task directly and decomposes only on
failure, recursively; depth comes out **emergent** rather than set — averaging
1.9 on depth-2 tasks and 2.8 on depth-3 — and is framed as adapting to both task
complexity and model capability. Its failure catalogue names over-decomposition
overhead and **tangential success**: sub-tasks completed with high fidelity whose
result is irrelevant to the original goal, because each acquired a local
optimisation target in place of it. Left to choose, agents tend to **under**-split.
ARIES reports deterioration rising sharply with depth, concentrated in the
aggregation step. Böckeler separates spec-first / spec-anchored / spec-as-source,
finds most tooling claims the higher levels and delivers the first, and reports
small fixes expanding into large artifact sets — the failure being that the
approach "doesn't scale across different problem sizes."

**Why it is held.** Splitting is cheap and rejoining is not; the decision of when
to split cannot be made by advance classification; and evaluating the composite is
where the cost concentrates.

**Reliability: moderate-to-good.** ADaPT and ARIES are academic with reported
benchmarks; Böckeler is practitioner analysis at a reputable venue. Benchmark
domains are not this project's, so transfer is assumed rather than shown.

**Touches:** `10-foundations/01`.

---

## 5. Comprehension debt, and one documented reversal from autonomy

**Sources.** HumanLayer, *"Why Software Factories Fail"* (July 2026 talk and
essay). Agoda, for the term *comprehension debt*.

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
`70-THINKING/05-primary-source-verification.md`. Appended, not merged into the
sections above, per the append-only rule.

**Verified against primary or ≥2 independent sources — reliability marks may
rise accordingly:** §1 Faros (epics/dev +66%, incidents/PR +242.7%, unreviewed
+31.3%, bugs/dev +54% — all exact), CircleCI (+59% YoY is the *overall* average,
not feature-branch; median-team main-branch −7%), LinearB (merge 32.7% vs 84.5%
exact; elite "≈2×" is raw, nets to ≈+10% org after review cost). §2 METR (all
figures confirmed; abstract carries no CI). §3 ETH — authors, dates, task/repo
counts, 641-word average, LLM-generated −0.5%/−2% at +20–23% cost, **and the
redundancy correction (strip docs first → generated files +2.7% and beat
developer-written)** all confirmed. §6 Sourcegraph 100K-vs-5K exact. §7 AGENTS.md
60k+ projects under the LF Agentic AI Foundation; TodoWrite→Tasks API at Claude
Code v2.1.16, off-by-default on Sonnet 5 / Opus 4.8 from v2.1.233.

**Corrections owed:**

- **§3.** Benchmark is **CTXbench**, not "AGENTbench". Developer-written gain is
  **+2.4%, p≈0.21 (not significant)**, not "~4%" (that is secondary coverage).
  The "obedience trap" label and the "ICLR 2026 workshop" venue are **unsourced**
  — no version of the paper states either; do not rest "peer-reviewed venue" on
  the latter. Reasoning-token increase is +10–22% (GPT models), not +14–22%.
- **§4.** "Tangential success" is **not in the ADaPT paper** — it is informal
  secondary writing (a dev.to synthesis). ADaPT's actual named limitation is
  that the executor model **cannot reliably judge its own success** (>30-point
  overestimation on WebShop), which is the more useful finding for
  `10-foundations/01` and should replace the tangential-success line here.
  ARIES's **4.12×** is one synthetic task (sorting64; sorting128 was 2.6×), not
  a depth-response curve; the aggregation-is-binding mechanism does hold.
- **§5.** *Comprehension debt* — attribute to **Addy Osmani / O'Reilly Radar**,
  not Agoda (no Agoda origin found; the term's coverage also re-conflates the
  METR −19%).

**Not re-checked** (OQ-1 stays open only for these): compaction-threshold table,
Cline memory-bank quotes, Aider repo-map internals, the "5 of 6 trials"
decomposition claim (source not locatable), and the `00-standing-position.md`
corpus figures (GitBugs / validity corpus / Debian BTS).
