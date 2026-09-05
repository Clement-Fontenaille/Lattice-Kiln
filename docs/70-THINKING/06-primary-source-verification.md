# Primary-Source Verification — the September field survey

**State:** OPEN
**Opened:** 2026-09-05
**Serves:** `03-how-the-field-frames-it.md` OQ-1 ("re-verify the primaries"), and
`00-design/50-findings/09-field-evidence-2026-09.md` (its standing reliability
caveat and per-claim reliability marks).

## Why this exists

`03-how-the-field-frames-it.md` and findings entry 9 were both written from
**search-engine synthesis, not primary pages** — direct fetching was blocked by
network policy on the workstation. Both documents say so, repeatedly, and both
ask for the primaries to be read before anything is cited load-bearing. One
error had already been caught and re-derived (the ETH sign inversion).

This is that pass, run 2026-09-05 with working retrieval. Each claim is checked
against the primary where one exists, or against multiple independent secondary
sources where it does not.

**Method note.** arXiv abstracts and HTML were read directly. Vendor telemetry
(Faros, LinearB, CircleCI, CodeRabbit) was checked against the vendors' own
published figures and at least one independent write-up. Two PDFs
(`arxiv.org/pdf/2602.11988`) would not extract cleanly and were read via the
HTML mirror instead.

## Headline

**The survey holds up well.** The industry telemetry is accurate, frequently to
the decimal. The academic papers are real, correctly identified, and their
numbers are mostly right. The prior known error (ETH sign inversion) stays
fixed and its re-derivation checks out — including the load-bearing "redundancy,
not authorship" correction, which is genuinely in the paper.

The residual problems are of one kind: **attribution slippage**. Blog
syntheses got cited as if they were papers; one benchmark is misnamed; one
internal cross-reference went stale; two figures were taken from secondary
coverage rather than the primary.

None of it overturns a design position. Two items (A, D) should be corrected
before the next citation; the rest are annotations.

**Second pass (2026-09-05, same day).** On re-checking: the "ICLR 2026 workshop"
venue flagged below as unfindable **is real** (MemAgents workshop, 27 Apr 2026) —
that flag is retracted (see F). "Tangential success" was confirmed to be an
**uncited** blog coinage (the dev.to author claims it as his own framing, cites
nothing). The "5 of 6 trials" decomposition claim (`03` §5b item 4) was chased to
a plausible candidate (VAT right-sizing pilot, arXiv:2608.23395) and it is **not**
the source — that study varies decomposition manually and reports no such
behaviour. Item 4 stays unsourced; recommend striking it.

---

## A. `tangential success` is misattributed to ADaPT — **correct before reuse**

**Claimed** (`03` §5b item F; `02-capability-as-granularity.md` throughout;
`50-findings/09` §4): ADaPT's "failure catalogue" contains **tangential
success** — "sub-tasks completed with high fidelity, result irrelevant to the
original goal" — described as "arguably the most insidious" and treated as a
documented, evaluated finding.

**Found:** The ADaPT paper (arXiv:2311.05772, NAACL Findings 2024) does **not**
contain the term or the failure mode. Its Limitations section names something
different: the **executor LLM's self-generated success heuristic is unreliable
and inflates success** — over-30-point overestimation on WebShop — and the
paper recommends external verifiers or calibration.

"Tangential success", the "most insidious" framing, and the "research thorough,
analysis sound, recommendation confidently wrong" example all trace to a
**dev.to blog post** ("The Decomposition Problem: Why Breaking Tasks into
Agent-Sized Pieces Is Harder Than It Looks"), a tertiary synthesis with no
evaluation behind it.

**Consequence.** The *concept* may still be worth carrying — locally-optimised
sub-tasks drifting off-objective is a plausible failure and `02` builds real
structure on it (the **integrated system ceiling**, the objective-preservation
operation). But it must be cited as **a hypothesis from informal writing, not a
result from ADaPT**. Every place that reads "ADaPT's documented failure modes"
needs to drop "tangential success" from that list or re-source it.

**Bonus finding, currently uncaptured.** ADaPT's *actual* limitation — models
cannot reliably judge their own "am I done / did this work" — is directly on
point for `10-foundations/01`'s open question (*"what makes a direct attempt
count as failed, cheaply enough that the check costs less than the decomposition
it triggers"*) and for dloop's escalate-on-stall. It is better evidence for a
problem the project already has than "tangential success" was. Worth adding to
entry 9 §4 and `20-cognitive-architecture/08-decomposition.md`.

---

## B. ETH benchmark name: `AGENTbench` → **CTXbench**

**Claimed** (`03` §5, `50-findings/09` §3): the ETH team's purpose-built
benchmark is "**AGENTbench** (138 tasks)".

**Found:** the paper (arXiv:2602.11988v2) calls it **CTXbench** — 138 instances
across 12 Python repositories that carry developer-committed context files.
Secondary coverage is itself split (some write "AGENTbench"; the SRI Lab's
GitHub link uses the string `agentbench`), which is where the error came from.

**Consequence.** Cosmetic but the doc uses "AGENTbench" as if authoritative in
three places. Rename to CTXbench. Task and repo counts (138 / 12) are correct.

---

## C. ETH developer-written effect: doc says `+4%`, paper says `+2.4%` (not significant)

**Claimed** (`03` §5, `50-findings/09` §3): human-written context files give
**+4%** (AGENTbench/CTXbench only), +19% cost.

**Found:** the paper reports **+2.4%** for developer-provided files, explicitly
**marginal — p ≈ 0.21**, i.e. not statistically significant. The +19% cost is
right. The "+4%" is from secondary coverage.

`03` already half-acknowledges this ("the SRI Lab's own framing — 'no
improvement' — is more conservative than secondary coverage's '+4%'"), then uses
+4% in its table anyway. Use **+2.4%, not significant**. This *strengthens* the
doc's actual argument (context files don't help), so there is no reason to keep
the softer secondary number.

**Everything else in the ETH citation checks out and is exact:**

| claim | primary | status |
|---|---|---|
| authors: Gloaguen, Mündler, Müller, Raychev, Vechev | ✓ (Mark Müller) | exact |
| SRI Lab (ETH) + LogicStar.ai | ✓ | exact |
| v1 12 Feb 2026, v2 23 Jun 2026 | ✓ | exact — `03`'s "a v2 revision (June 2026) may differ" was prescient |
| SWE-bench Lite: 300 tasks, 11 repos | ✓ | exact |
| own benchmark: 138 tasks, 12 Python repos | ✓ | exact (name wrong — see B) |
| avg context file 641 words (range 24–2003) | ✓ | exact |
| LLM-generated: −0.5% SWE-bench, −2% own bench, +20–23% cost | ✓ | exact |
| **redundancy correction**: strip documentation files first → LLM-generated files improve ~2.7% and beat developer-written | ✓ | **confirmed** — this is the load-bearing claim and it is real |
| reasoning tokens +14–22% | paper: **+10–22%, GPT models** | low end slightly off |
| tool-use "1.6–2.5× baseline" | paper: `uv` 1.6× *when mentioned*, repo-specific tools 2.5× *when mentioned* | roughly — these are specific tools, doc generalises |
| "2–4 extra steps" | not found | unverified |
| term "obedience trap" | **not in the paper** (checked twice) — project/coverage coinage | see E |
| "presented at ICLR 2026 workshop on memory for LLM-based agentic systems" | **correct** — MemAgents workshop, 27 Apr 2026 | see F (flag retracted) |

---

## D. Internal inconsistency: `01-use-cases.md` still attributes the perception gap to LinearB

**Found:** `01-use-cases.md` §3 reads:

> **Challenge to §1:** developers *feel* 20% faster and are *19% slower*
> (LinearB, ~8.1M PRs).

`03` §5 ("The perception gap — corrected attribution") explicitly retracts this
exact conflation:

> An earlier draft of this document attributed "feel 20% faster, are 19%
> slower" to LinearB. That was wrong — two separate studies were conflated. The
> figure is METR's.

`01`'s bullet was updated for the ETH/redundancy correction in the same pass but
this line was missed. **`01-use-cases.md` §3 should be corrected** to attribute
the −19% to METR (RCT, 16 devs, early-2025 tooling) and keep LinearB only for
the merge-rate / PR-size / pickup-time figures.

---

## E. `obedience trap` is not the ETH paper's term

`03` §5 writes: *"Dubbed **'the obedience trap.'**"* — no attribution, reads as
the authors' coinage. It is not in the paper. Harmless label; mark it as the
project's own (or drop the quotation framing).

---

## F. `ICLR 2026 workshop` — **retracted; the docs were right**

An earlier version of this section flagged the venue claim as unfindable. That
was a miss on the first search pass. **The claim is correct.** The paper was
presented at the **MemAgents ICLR 2026 workshop** (Workshop on Memory for
LLM-Based Agentic Systems) on **27 April 2026**
(`sites.google.com/view/memagent-iclr26`). `03` §5 and `50-findings/09` §3 stand
as written on the venue, and "peer-reviewed venue" is defensible for a workshop
paper.

---

## G. ARIES `4.12×` is one task, not a trend

**Claimed** (`03` §5b, `02` "candidate contribution", `50-findings/09` §4):
"ARIES reports up to **4.12×** performance deterioration **as depth rises**."

**Found:** ARIES (arXiv:2502.21208, "Autonomous Reasoning with LLMs on
Interactive Thought Graph Environments") reports 4.12× on the **sorting64** task
specifically (and 2.6× on sorting128). The *mechanism* claim is supported —
aggregation is the binding constraint; the aggregation transformation is 86% /
68% of policy-agent errors on those tasks. Domain is thought-graph puzzles
(game-of-24, sorting), far from software work.

**Consequence.** `50-findings/09` §4 already flags "benchmark domains are not
this project's, so transfer is assumed rather than shown" — good. But "up to
4.12× as depth rises" reads as a general dose-response curve; it is one data
point on one synthetic task. Soften to "on one task, deterioration reached
4.12× and concentrated in aggregation."

---

## H. `comprehension debt` — attribution to Agoda not confirmed

**Claimed** (`50-findings/09` §5): "Agoda, for the term *comprehension debt*."

**Found:** the prominent, citable source for the term is **Addy Osmani**,
"Comprehension Debt: The Hidden Cost of AI-Generated Code" (O'Reilly Radar /
reposted widely). There is also an arXiv paper ("Comprehension Debt in
GenAI-Assisted Software Engineering Projects", 2604.13277). Could not find an
Agoda origin. Secondary coverage of the term also tends to re-conflate the METR
"19% slower" figure into it, so tread carefully. Recommend: attribute to Osmani
/ O'Reilly Radar, or drop the attribution and keep the concept.

---

## Confirmed accurate — no action needed

Checked against primaries or ≥2 independent sources. Figures below matched
exactly unless noted.

### Academic

- **METR** (arXiv:2507.09089, "Measuring the Impact of Early-2025 AI on
  Experienced Open-Source Developer Productivity"). Authors Becker, Rush,
  Barnes, Rein ✓. 16 developers, 246 tasks, randomised per task ✓. Own repos,
  avg 5 years' experience ✓. Cursor Pro + Claude 3.5/3.7 Sonnet ✓. Forecast
  −24% → post-hoc self-estimate −20% → measured **+19% time** ✓. Experts
  predicted −38% (ML) / −39% (economics) ✓. *Caveat on `03`:* the abstract
  gives no confidence interval; `03`'s "[−40%, −2%]" is from METR's blog, close
  to coverage's "+2% to +39% on time". The "22k+ stars / 1M+ LOC" repo detail
  in `03` is not in the abstract (METR's blog has repo stats; not re-pulled
  here). The scope-limitation framing in `03` ("maximum-disadvantage case")
  matches what METR themselves say.

- **ADaPT** (arXiv:2311.05772, NAACL Findings 2024). Authors Prasad, Koller,
  Hartmann, Clark, Sabharwal, Bansal, Khot ✓ (UNC / AI2 / Saarland). Decompose
  on failure, recurse, cap depth; adapts to task complexity *and* LLM
  capability ✓. Gains +28.3% ALFWorld / +27% WebShop / +33% TextCraft ✓ exact.
  Emergent depth **1.9** (depth-2 recipes) → **2.8** (depth-3), TextCraft
  Table 3 ✓ exact. *See A for what is wrongly attributed to it.*

- **"LLMs as Packagers of HPC Software"** (arXiv:2511.05626). SpackIt;
  install success ~20% zero-shot → >80% best config (≈ `00-standing-position.md`'s
  "19.7% → 82.9%") ✓. Error-aware repair loop ✓. 308 HPC packages ✓.

- **"Where Do AI Coding Agents Fail?"** (arXiv:2601.15195, MSR 2026 Mining
  Challenge). ~33k agent PRs, 5 agents ✓. Non-merged PRs are larger, touch more
  files, fail CI more ✓ (rejected PRs: +17% LoC, +10% files; each failed CI
  check ≈ −15% merge odds).

- **1.02M PRs / 207 projects** (Zhong et al., 2026). Agent involvement → faster
  review decisions, **no measurable improvement in review quality** ✓ exact.

- **Böckeler** (Thoughtworks, martinfowler.com "Exploring Gen AI"). Taxonomy
  **spec-first / spec-anchored / spec-as-source** ✓ (third level also called
  "spec-as-truth"). Spec-first = spec not maintained after ship ✓. The "most
  tools claim the higher levels, deliver spec-first" verdict is practitioner
  analysis, directionally supported, not quoted verbatim here.

### Industry telemetry

- **Faros AI**, "The AI Engineering Report 2026: The Acceleration Whiplash".
  ~22,000 developers, ~2 years, 4,000+ teams ✓. Epics/dev **+66%** ✓.
  Production incidents per PR **+242.7%** ✓. Unreviewed PRs merged **+31.3%** ✓.
  Bugs/dev **+54%** ✓. (Also: tasks/dev +34%, median review time +441.5%, churn
  +861%.) `03`'s Faros row is fully accurate.

- **LinearB 2026 Benchmarks**. AI-assisted 30-day merge rate **32.7% vs 84.5%**
  ✓ exact. Pickup ~4.6–4.8× slower (`03`'s "2.5–5.3×" range brackets it;
  agentic worse than AI-assisted, consistent). "Elite AI teams merged **98%
  more**" ✓ ≈ "nearly doubled". *Caveat:* LinearB's own framing nets the elite
  gain down to ~+10% organisational after review-time cost — `03`'s Corrections
  1–2 grapple with this but the raw "doubled" is what lands in `01` and `09`.
  Report figures: 2.7M PRs in the headline report, ~4,800 teams; larger counts
  (8.1M+) are derived analyses — `03` and `09` state this correctly, `01` just
  says "8.1M".

- **CircleCI 2026 State of Software Delivery**. 28M workflows. Throughput
  **+59% YoY** ✓ — but this is the *overall average*; `03` labels it
  "feature-branch throughput", which is a mislabel (median-team feature-branch
  was +15%). Median-team **main-branch throughput fell (−7%)** ✓. Main-branch
  success rate at a five-year low (70.8%).

- **CodeRabbit**, "State of AI vs Human Code Generation" (Dec 2025). **470 OSS
  PRs** ✓. **~1.7× more issues** in AI-authored PRs (10.83 vs 6.45 per PR) ✓
  exact.

- **Sourcegraph** context-engineering benchmark. Agents given a **100K-token
  summary performed worse than 5K tokens of targeted retrieval** ✓ exact.
  Vendor benchmark; not token-matched — `09` §6 flags both correctly. The
  "~65% of failures = context drift" figure is flagged weak / not relied on ✓.

### Vendor documentation / mechanics

- **AGENTS.md adoption**: 60,000+ projects ✓. Under the Linux Foundation's
  **Agentic AI Foundation** (formed Dec 2025; AGENTS.md a founding contribution,
  donated by OpenAI, released Aug 2025) ✓. `03`'s "Linux Foundation
  stewardship, near-universal adoption" is accurate.

- **"Hooks vs CLAUDE.md"**: the substance is real — Anthropic's own post
  "Steering Claude Code" says *hooks are for anything that must always happen;
  CLAUDE.md is for what the model should merely know; a hook makes it happen
  every time, an instruction sometimes won't.* `03`/`09` render this as a quote
  (*"hooks are for anything that must happen; instruction files are requests,
  not guarantees"*) — it is a faithful **paraphrase**, not verbatim. Fine as
  long as it is not presented as an exact quotation.

- **TodoWrite → Tasks API**: Claude Code **v2.1.16** (22 Jan 2026) introduced
  the Tasks API superseding TodoWrite ✓. Task/todo tools **off by default** on
  Sonnet 5 / Opus 4.8 / Fable 5 and later (from v2.1.233), because those models
  track multi-step work internally and the tool definitions cost context ✓.
  `03` compresses the two version events into one but the substance — "the
  scaffold was removed when the ceiling rose" — is correct and is a genuinely
  good data point for the rungs-of-lift idea.

---

## Not re-checked this pass (lower stakes, flagged for completeness)

- Compaction thresholds table (`03` §5b C): Gemini ~50%, Roo ~86–92%, Claude
  Code ~89%, Codex ~90%, OpenCode ~96–99%.
- Cline "memory resets completely between sessions" quote and the >50%
  memory-bank handoff.
- Aider repo-map internals (PageRank over the dependency graph, `--map-tokens`).
- "In one study they fused stages, dropped others, and replaced a classification
  stage with a fixed threshold in 5 of 6 trials" (`03` §5b, under F) — **source
  not locatable.** Chased the nearest candidate (VAT decomposition right-sizing
  pilot, arXiv:2608.23395) and ruled it out — that study varies decomposition
  manually and reports no emergent stage-fusing. Recommend **striking item 4**
  unless the user can name the source.
- GitBugs / the validity corpus / Debian BTS figures in `00-standing-position.md`
  E-corpus.

---

## Recommendation

**All corrections below applied to the design and thinking sets on 2026-09-05**
(the user authorised propagation). This section records what was done.

1. **A — "tangential success".** Reclassified everywhere from "ADaPT's
   documented, evaluated failure mode" to *a concern raised in informal writing,
   with no evaluation behind it*. The concept is kept (it motivates real
   structure in `02`); only its evidentiary status changed. ADaPT's *actual*
   limitation — models cannot reliably judge their own success — added to entry 9
   §4 and to `20-cognitive-architecture/08` open questions.
2. **B — CTXbench**, not "AGENTbench": corrected in `03` (×4) and entry 9 §3.
3. **C — developer-written effect** is **+2.4%, p≈0.21 (not significant)**, not
   "+4%": corrected in `03` and entry 9 §3.
4. **D — `01-use-cases.md` §3**: perception gap re-attributed from "LinearB,
   ~8.1M PRs" to **METR** (RCT, 16 devs, early-2025 tooling); LinearB kept for
   merge-rate / size / pickup only.
5. **E — "obedience trap"**: marked as coverage/project coinage, not the paper's
   term.
6. **F — ICLR 2026 workshop: NOT an error.** The paper was at the MemAgents ICLR
   2026 workshop (27 Apr 2026). `03` and entry 9 stand; my earlier flag is
   retracted.
7. **G — ARIES 4.12×**: reworded to "one synthetic task (sorting64); the
   aggregation-is-binding mechanism holds" in `03`, `02` (×3),
   `00-standing-position.md`, entry 9 §4.
8. **H — comprehension debt**: re-attributed from Agoda to **Addy Osmani /
   O'Reilly Radar** in `03` and entry 9 §5.
9. **Item 4 of `03` §5b** ("5 of 6 trials" stage-fusing) marked **unsourced**
   pending a citation.
10. **Entry 9 reliability marks** raised where this pass verified against primary
    or ≥2 independent sources (METR, Faros, CircleCI, LinearB, CodeRabbit, the
    33k- and 1.02M-PR studies, ETH incl. the redundancy correction, Sourcegraph,
    AGENTS.md adoption, TodoWrite/Tasks). Standing caveat narrowed to the
    "not re-checked" list.

## Which arguments this voids

Traced in `05-what-the-external-evidence-carries.md` → "Arguments that lose
support". Short version: **no design-set argument collapses.** One THINKING
argument is demoted — `02`'s "ADaPT's failure catalogue contains two modes this
account was missing" was an appeal to *evaluated prior art*; with "tangential
success" removed it becomes the project's *own reasoning* plus one narrow-domain
result (ARIES). The conclusions it fed (the integrated-system ceiling, the
objective-preservation operation, the depth-bound contribution) survive on that
weaker footing, and each is now marked accordingly.

## Output

Corrections folded in 2026-09-05. Companion analysis of what the evidence
actually carries: `05-what-the-external-evidence-carries.md`. OQ-1 remains open
only for the "not re-checked" list.
