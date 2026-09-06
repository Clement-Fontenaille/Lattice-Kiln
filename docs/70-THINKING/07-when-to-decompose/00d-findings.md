# Cross-paper discussion — findings

*The collect phase produced eight review sheets (`01`–`08`). This file is where
they are taken up against each other, and against the project's own questions,
finding by finding. Nothing here is settled. Entries are of three kinds: a
**finding** is a conclusion drawn from the sheets when they are cross-examined; a
**qualifier** bounds how far a sheet or a finding can be carried; a **candidate
argument** is a project-originated hypothesis parked here to be tested against the
literature in a later pass.*

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
is untested. Topic 15 is where that trend gets assessed properly. Sheet `08`'s
contribution here is further limited by [[F5]]: it measures chain-of-thought
length, not new-prompt-per-step decomposition, so it corroborates the direction
only by analogy.

### F2 — Correct decomposition carries a "shortcut tax," and its size at constrained scale is unmeasured

Sheet `07` (Madhwal et al.) classifies its cross-regime disagreements into
Helped (Direct wrong, decomposed right), Hurt (Direct right, decomposed wrong),
and Both-wrong. For the two frontier models the split is roughly 16 / 16 / 67
percent of the inconsistent cases. The stated mechanism for the Hurt bucket is
the *shortcut hypothesis*: the Direct answer was right because the model
pattern-matched the question to an answer without holding the intermediate
facts, and forcing execution of the verified plan exposes that gap and produces
a wrong answer.

The mechanism is not in principle capability-specific — a weaker model also
answers some questions by shortcut — but the paper reports the Helped / Hurt /
Both breakdown *only for the frontier models*. For the sub-70B models it reports
only net accuracy deltas of about +25, with no bucket decomposition and no
matched-question analysis of what a weaker model did on the items where
decomposition hurt a stronger one.

So the net lift at constrained scale is an average over a helped set and a hurt
set of unknown relative sizes. Decomposition may carry a subtractive component
at every capability level; this paper establishes the mechanism and its frontier
magnitude, not its magnitude where the project operates.

Consequence for [[A1]]: a fresh-context decomposition design inherits this tax on
exactly the question class where a monolithic call would have shortcut to the
right answer. Whether the working-memory benefit is worth a measurable accuracy
cost on that subset is the open question, and this paper gives the mechanism but
not the magnitude at constrained scale.

What would close the gap: a Helped / Hurt / Both breakdown at 8B–70B, and a
matched-question comparison of what weaker models do on the frontier Hurt items.

Scope: closed-book factual multi-hop QA, where the shortcut being exposed is that
"the parent question is more trained-on than its parts." For task families where
decomposition genuinely lowers difficulty rather than relocating a knowledge
lookup, the mechanism may not apply.

### F3 — Sheets 07 and 08 bracket the fresh-context question without resolving it

Sheet `07` (Madhwal et al.) runs a step-wise regime in which each hop is issued in
a fresh context holding only the substituted sub-question — no parent question, no
sibling answers. That regime underperforms the full-context regime at frontier
scale. It is empirical evidence, in a closed-book QA setting with no
context-budget pressure, that stripping context from a sub-call costs accuracy.

Sheet `08` (Wu et al.) derives its benefit term — sub-answers get easier as the
chain is split more finely — under a model in which every step conditions on the
full accumulating history of prior steps. An isolated sub-agent call carries no
such history. The paper models neither the cost of dropping it nor the benefit,
and the sign is genuinely ambiguous: losing the history could make sub-answers
harder, which moves the optimum shallower, or it could shed an accumulating
burden the chain pays and a fresh call does not, which moves the optimum deeper
and makes the benefit larger than the chain shows.

So the two sheets bracket the question rather than answer it. Sheet `07` has
evidence that context-stripping hurt; sheet `08` has a mechanism whose benefit
term may be understated for a fresh-context design. Neither setting matches a
sensible fresh-context sub-call: `07` stripped everything and had no memory
pressure, `08` never modelled isolation at all.

What the [[A1]] pass must resolve: for the project's task families and its actual
context-budget pressure, does a fresh-context sub-call that passes down the goal
and a relevant summary — not a bare hop — land on the lost-disambiguating-context
side (`07`) or the shed-accumulating-history side (`08`).

### F4 — An observed-length-vs-accuracy curve carries a reverse-causation confound; the project must not repeat it

Not a result from any sheet — a methodological caution drawn from how sheet `08`
measures its central curve. Sheet `08` plots accuracy against chain length. Any
such curve, whichever the x-axis (tokens or steps), is exposed to a confound the
paper does not name: within a single problem, the attempts that came out long are
disproportionately the attempts where the model was already failing —
backtracking, restarting, second-guessing — so length and error share an upstream
cause. Part of any observed "longer is worse" is then "the model was lost, which
made the output both long and wrong," not "depth caused the error."

Sheet `08`'s within-question design (vary length for a fixed question) removes the
across-question version of this — long questions being harder questions — but not
the within-question version, which operates across attempts at the same question.
Its synthetic leg does avoid the trap: there, depth is *commanded* by a control
token, not read off the output. The exposed claim is the observational one.

Carry-forward for the project: when the project measures decomposition depth
against outcome in its own evaluation, depth must be *set* — assigned,
controlled, commanded — rather than *observed* after the fact. An observed-length
curve cannot support a causal claim about depth. This constrains how [[I1]] and
any depth-tuning evaluation are designed.

### F6 — What sheet 08 carries in practice is a prompt-writing guideline

Read as chain-of-thought management inside one generation (per [[F5]]), sheet `08`
yields a set of guidelines rather than a decomposition result:

- There is an interior optimum for how much step-by-step working to elicit. Both
  "answer directly" and "narrate every micro-step" lose accuracy, not only
  tokens. Maximal granularity is not a safe default.
- Dial the elicited working *down* as the base model gets stronger. Scaffolding
  tuned on a weak model actively hurts a strong one, and the penalty grows with
  capability, so this is not a set-once choice — it comes down on model upgrades.
- Dial it *up* for harder items. A fixed instruction across a task mix is wrong
  for most of the mix; conditioning on difficulty, or letting the model
  self-pace, beats one template.
- Prefer steps that each do a real chunk of work over many trivial ones.
  Tentative — synthetic and theory only — but the direction is "do not
  over-atomize."
- Padding is pure cost. Instructions or exemplars that produce restatement and
  hedging add length with none of the benefit.
- If several candidates are sampled: length-filtered voting (bin by length, keep
  the low-answer-entropy bins, vote within) is worth trying. One-dataset
  proof of concept, not adopt-on-sight.
- Do not assume RL lengthens reasoning. Outcome-reward fine-tuning tends to
  shorten chains as accuracy improves.

Applications: a static prompt or context template; a dynamic prompt-tuning
mechanism that adapts per request or per model (the capability and difficulty
directions are exactly its inputs); and prompting practice in general.

Scope: the directions transfer, the numbers do not, and the last three points are
proof-of-concept strength.

## Qualifiers

### F5 — Do not lend sheet 08's results to decomposition findings

Sheet `08` studies the length of a chain of thought inside one model generation.
In its real-model leg, "steps" are newline-separated lines, and how many there are
is induced by few-shot exemplars written at three step granularities — a
writing-style intervention, closer in kind to "proceed step by step" than to task
decomposition. Its synthetic leg gives a step real structural content (a control
token, a fixed operator budget per step) but still inside one context, one set of
weights, with no new prompt issued per step and no recombination stage. Its theory
assumes every step conditions on the full prior history.

Explicit task decomposition is a different operation: the orchestrator issues a
*new prompt* per sub-task, often in a fresh context, and a recombination step
follows. None of sheet `08`'s three legs models that. Its mechanism — compounding
per-step reliability against a saturating benefit — is stated abstractly enough to
invite the extrapolation, and the paper claims in one sentence that least-to-most
and divide-and-conquer "fall in our analysis," but it never tests an
explicit-decomposition scheme.

What this qualifier guards:

- [[F1]] leans on sheet `08` as a second, independent construction of the
  capability-decay direction. With this qualifier, sheet `08` corroborates
  "optimal *chain length* falls with capability" — adjacent to, not identical
  with, "decomposition lift falls with capability." The direction survives; the
  identification is by analogy.
- [[F2]] is derived from sheet `07`'s explicit regimes and does not depend on
  sheet `08`. The temptation this blocks is *stacking* sheet `08`'s
  "over-decomposition hurts" on top of F2 as if the two were one reinforcing
  result. They are about different things: F2 is knowledge exposure under a
  correct plan; sheet `08` is per-step error accumulation in one narrated chain.
- [[F6]] is already scoped to chain-of-thought management and needs no further
  guard.

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
- The size of the shortcut tax from [[F2]] at 8B–70B scale — the accuracy cost
  this design pays on the question class a monolithic call would have shortcut,
  set against the working-memory benefit.
- Which side of [[F3]] a fresh-context sub-call lands on — lost disambiguating
  context, or shed accumulating-history burden — for the project's tasks.

---

*Further candidate arguments are added here as they surface, then assessed in a
later pass.*
