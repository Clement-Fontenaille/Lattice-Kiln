# THINKING

## TL;DR

Open exploration that is not yet a design position. Threads here may be
half-formed, mutually contradictory, imported wholesale from someone else, or
later abandoned. Nothing in this folder constrains anything.

> **Motto:** Nothing here is load-bearing.

## Why this folder exists

The design set (`00-design/`) documents convergence. The specification set
(`10-technical/`) documents commitments. The progress set (`50-PROGRESS/`)
documents execution. All three are written to be *cited*.

There was no surface for the step before that: the question being turned over,
the impression that has not yet earned a claim, the position held only until the
next piece of evidence arrives, the thing someone else said that might matter.

Without such a surface, exploratory work either gets written into the design set
prematurely — where it acquires an authority it has not earned — or it stays
conversational and is lost.

## What belongs here

- Questions the design set does not currently ask.
- Impressions from actually using the thing, before they are evidence.
- External input: community practice, prior art, other projects' positions,
  someone's offhand remark that landed.
- Positions taken provisionally, and the record of them being adjusted.
- Framings tried and discarded, with why.

## What does not belong here

Anything that has converged. The moment a thread produces a position the project
intends to hold, that position is written where positions live — the design set,
the open-questions register, or a milestone — and this thread records where it
went.

Findings do not belong here either. A finding is earned from a reconstructable
run and belongs in `00-design/50-findings/`.

## Relationship to `00-design/90-notes/`

`90-notes/` is *about the design set* — what pass to run next, what to name
things. It is housekeeping for a body of work that already exists.

`70-THINKING/` is *upstream of the design set*. It holds material that may never
become design at all.

## Structure

- `NN-<topic>.md` — one document per thread.
- `ideas.md` — a running register of unvetted ideas thrown off by the threads
  (experiments, methods, design moves). An idea that matures graduates out to a
  committed surface and its entry records where it went.
- `NN-<topic>/` — a folder, where a thread is a structured literature review.
  Files 07–15 are the nine-topic review and take this form. Each folder holds
  `00a-instructions.md` (insulation rule, Subject, Task), `00b-template.md` (the
  per-paper review sheet format — identical across all nine, opens with a density
  flag), `00c-inventory.md` (Step 1 inventory + Step 2 selection), `00d-findings.md`
  (cross-paper discussion, written only after the collect phase), and one
  `NN-<slug>.md` sheet per reviewed paper.

Each thread carries a **state** (`OPEN`, `CONVERGED`, `ABANDONED`) and, when it
closes, a line naming where its output went. Closed threads are retained, not
deleted — the record of a discarded framing is worth keeping.

## Reading rule

If you are looking for what the project believes, this is the wrong folder. Read
`00-design/`. If a document here contradicts one there, the one there wins by
construction, and the contradiction is either a thread that has not landed yet or
a design document that needs revisiting — but never a fact about the project.
