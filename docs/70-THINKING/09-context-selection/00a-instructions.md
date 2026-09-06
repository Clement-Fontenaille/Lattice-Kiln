# What Goes in the Window

*A literature review of how LLM-based agent systems decide what to put in the context.*

**State:** OPEN
**Opened:** 2026-09-05
**Part of:** a nine-topic literature review (files 07-15). Third topic.

> **Insulation rule.** This review is deliberately sealed off from the rest of
> this repository. The Subject section is the *only* context the reviewer is
> given. Do not read, cite, or reconcile against any other document in this
> project, and do not shape findings to fit any position held elsewhere in it.
> The point of the review is to see the literature on its own terms.

## Subject

Every model call is preceded by a decision about what to place in the context:
which files, passages, tool outputs, prior turns, and instructions, at what
length and level of detail. Approaches range from including everything that might
be relevant, through retrieval over an index, to summarisation, structural
abstraction (maps, signatures, skeletons), and aggressive pruning or compaction.
They differ on what is selected (whole documents, passages, summaries,
structure), how much (a fixed budget or a dynamic one), and when (once up front,
or refreshed each turn). A recurring question is whether adding more relevant
material keeps helping or begins to hurt, and whether the operative variable is
volume, relevance, redundancy, or level of abstraction. The topic sits within the
wider bodies of work on retrieval-augmented generation, long-context modelling,
and context engineering.

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

Each of the four picks gets its own sheet in this folder: `01-<slug>.md` …
`04-<slug>.md`. The sheet format lives in `00b-template.md` (shared, identical
across all nine topics), and it opens with a one-line **density** flag. The
inventory and the four picks are recorded in `00c-inventory.md`; the cross-paper
discussion, when it happens, goes in `00d-findings.md`.
