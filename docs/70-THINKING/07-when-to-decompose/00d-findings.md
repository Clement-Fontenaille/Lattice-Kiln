# Cross-paper discussion — findings

*The collect phase produced eight review sheets (`01`–`08`). This file is where
they are taken up against each other, and against the project's own questions,
finding by finding. Nothing here is settled. Entries are of two kinds: a
**finding** is a conclusion drawn from the sheets when they are cross-examined; a
**candidate argument** is a project-originated hypothesis parked here to be tested
against the literature in a later pass.*

## Findings

### F1 — Decomposition buys two things, and only one of them decays with model capability

Sheet `07` (Madhwal et al.) shows that a correct, hand-verified decomposition is
worth roughly +25 accuracy points at 8B–72B and flattens to slightly negative at
frontier scale, with the stated mechanism that a capable model has internalised
the reasoning chains, so the external scaffold becomes first redundant and then
interfering. Sheet `08` (Wu et al.) reports the same directional shape from the
chain-of-thought-length side: the optimal number of steps falls as capability
rises.

The distinction this forces:

- **Accuracy lift** from decomposition decays as the base model improves, and can
  invert. A design that leans on decomposition *to be more correct* is leaning on
  a gap that is closing.
- **Working-memory and context discipline** do not decay. A larger, better model
  still has a finite context window, still accumulates state across a long task,
  and still benefits from each sub-call carrying a bounded working set. This is
  the value [[A1]] is about.

Consequence for the project: if decomposition is used for context management
rather than for accuracy, the frontier-capability trend is much less threatening.
That has to be a deliberate, recorded design choice rather than an unexamined
assumption, because a decomposition built for the accuracy reason and one built
for the context reason are not necessarily the same shape, and the first one has
an expiry date.

Scope: the capability-decay evidence is from closed-book factual multi-hop QA
(sheet `07`) and from math and logic reasoning (sheet `08`). Whether the same
decay shape holds for task families where sub-tasks differ qualitatively from the
parent — long-horizon work, tool use, code, tasks that exceed a context window —
is untested. Topic 15 is where that trend gets assessed properly.

## Candidate arguments (unassessed)

### A1 — Fresh-context decomposition as the space-reusing form of divide-and-conquer

**Provenance.** This argument arose in discussion while reading sheet `06`
(Merrill & Sabharwal, *The Expressive Power of Transformers with Chain of
Thought*), set beside the classical complexity result that divide-and-conquer can
trade time for space by solving sub-problems sequentially and reusing scratch
space between them — Savitch's theorem is the textbook instance. It was then
connected to the project's premise of operating under a fixed and modest context
budget. It is a project-originated hypothesis, not a claim extracted from any
reviewed paper.

**The claim.** If a task is solved by separate model calls, each given a fresh
context that holds only what that sub-call needs, and each sub-result is
compressed before it is carried forward, then the peak context any single call
has to hold is bounded by the largest individual sub-problem rather than by the
sum of the whole task's working material. The working set then tracks the depth
of the decomposition rather than its total size. For a system whose premise is
staying effective under a fixed context budget, this is a structural reason to
prefer decomposition over one long reasoning stream, and it is independent of any
accuracy argument.

**The price.** The approach pays in repeated calls and repeated prompt overhead,
which is the time-for-space side of the trade. It also pays in redundant work
whenever sub-problems share structure that a single pass would have computed once.

**The failure mode.** A sub-call that cannot see its siblings or the full parent
context can make a choice that is locally sound and globally wrong, and the
summary step can drop the information that would let a later stage catch the
error.

**What a pass needs to check.**

- Whether the Merrill & Sabharwal result actually licenses a claim about working
  memory, or only a claim about model size. Sheet `06` notes that their space
  bound *grows* with the step count rather than shrinking.
- Whether any reviewed paper treats peak working memory or context size as a
  dependent variable, rather than reporting only token counts or accuracy.
- Whether the recombination failure mode named above is the same one that sheets
  `01`, `03`, `04`, `07` and `08` each raise from their own angle, and if so what
  magnitude those papers put on it.
- Whether the literature contains competing arguments, for or against
  fresh-context decomposition, that did not originate with the project.

---

*Further candidate arguments are added here as they surface, then assessed in a
later pass.*
