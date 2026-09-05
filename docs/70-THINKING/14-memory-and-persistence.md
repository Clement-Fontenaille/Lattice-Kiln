# What the System Keeps

*A literature review of how LLM-based agent systems carry knowledge across sessions.*

**State:** OPEN
**Opened:** 2026-09-05
**Part of:** a nine-topic literature review (files 07-15). Eighth topic.

> **Insulation rule.** This review is deliberately sealed off from the rest of
> this repository. The Subject section is the *only* context the reviewer is
> given. Do not read, cite, or reconcile against any other document in this
> project, and do not shape findings to fit any position held elsewhere in it.
> The point of the review is to see the literature on its own terms.

## Subject

An agent system that runs across many sessions must decide what to retain, in
what form, and how to bring it back. Mechanisms range from raw transcript logs,
through user-curated notes and files, to structured memory stores with retrieval,
and pipelines that extract, summarise, or promote durable knowledge from episodic
experience. Work here covers what to write, when to write it, how to retrieve it,
how to handle staleness and contradiction, and whether a memory of past
experience measurably improves later performance. Recurring concerns include
memory that grows until it competes with the work it supports, provenance, and
forgetting. The topic sits within the wider bodies of work on long-term memory
for agents, retrieval-augmented generation, and continual learning.

## Task

Characterise the recent research literature on the Subject. Collect and describe
only — do not test the literature against any expectation, and do not connect
anything to material outside this file. **No conclusion is expected in this pass:
no synthesis across papers, no ranking, no answer to any question.** Each paper is
described on its own; the cross-paper discussion happens later, separately,
finding by finding. (This protocol is copied into each topic file so the file is
self-contained.)

### Step 1 — inventory

Collect **every peer-reviewed paper (2023 onward)** on the Subject — published or
accepted at a journal, conference, or reviewed workshop. arXiv-only preprints are
out of scope unless otherwise published; if one is clearly central, note it in a
single line as excluded-pending-publication and move on. For each in-scope paper,
record in this file: the cite line (authors, title, year, venue, DOI/arXiv,
link), **the full abstract quoted verbatim**, and a flag — **RELATED** /
**ADJACENT** / **NOT RELATED** to the Subject — with one line of reason. Do not
review or paraphrase
yet. The inventory is the audit trail for what was and was not looked at, and the
abstracts are the material Step 2 selects from.

Pre-2023 work is in scope only where the later papers repeatedly build on it;
list it and mark it as an anchor.

### Step 2 — select four

From the RELATED set, pick **four papers** to review in full, working from the
collected abstracts. **Select for spread, not fit** — four papers that span
approach, method, and claim, not the four that sit closest to the Subject's
framing. Record one line per pick saying why it was chosen.

### Step 3 — review each of the four

Primary sources only: read the actual paper; do not rely on summaries or
secondary coverage. Write in **full sentences**, close to what the paper reports,
**away from editorialising**. This is the **collect** phase — do not draw
conclusions across the four papers; that comes afterward, finding by finding.

The format below is **proposed, not required**. Some papers carry more material
than others; explore each as far as it deserves.

- **Name** — and **keywords** (the reviewer's own, not the paper's), **year**,
  **venue**.
- **Approach** — what they did.
- **Model(s) targeted** and **benchmarks used**.
- **Author incentive** — affiliation, funding, product or position stake.
- **Measurement methodology** — brushed, not exhaustive: the dependent variable,
  what is controlled, N, how significance is treated.
- **Key findings** — including **the authors' own reading** of them.
- **Open questions the paper itself raises** — its stated limitations and
  future-work, in its own framing.
- **Appreciation** — the reviewer's assessment, keeping **MECHANISM separate from
  MAGNITUDE**: which findings transfer as an argument, which are numbers valid
  only inside the paper's own setup.
- **How it could serve a harness-design effort / limitations / major concerns** —
  stem the discussion, do not resolve it.
- **Five citations** worth chasing for the next round.

---

## 1. Inventory

_Step 1 output goes here — cite line, full abstract, flag + reason, per paper._

## 2. Selected for review

_Step 2 output goes here — four picks, one line each on why._

## 3. Reviews

_Step 3 output goes here — one entry per selected paper._
