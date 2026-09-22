# Research and Evaluation

One file per experiment, plus the register of what could become one.

> **Motto:** Run the arm you expect to lose.

## What is here

- [`00-questions.md`](00-questions.md) — open questions that could be settled by an
  experiment, and the standing rules for how this project runs them. Not every
  question here has a sheet; a question earns one when it is circumscribed enough to
  state what would falsify it.
- One sheet per experiment, `E0` onward. A sheet exists when the experiment is
  defined well enough to run, whether or not it has been run.
- [`hypotheses.md`](hypotheses.md) — the project's standing hypotheses and what each
  would take to overturn. What the experiments are ultimately for.

## What a sheet carries

**The question**, in one sentence. **What would falsify it**, written before any data
exists. **The design** — arms, what is held constant, what varies. **What a null
means**, which is not the same for every experiment and is the thing most often left
unstated. **Cost and gating.** **Status**, and where the result went if it has run.

## The three sweep layers

Reorganised 2026-09-22. E3, E4 and E5 no longer carry a theme each; they carry
a **layer** each, and the comparisons between them are the point.

| sheet | layer | subject | can it attribute? |
|---|---|---|---|
| [`E3`](E3-functional-requests.md) | 1 — functional | a whole system answering a request phrased as a user would phrase it | **no**, by design |
| [`E4`](E4-capability-sweep.md) | 2 — mechanism | one role's mechanism, the rest of the system held | to the mechanism |
| [`E5`](E5-skill-scales.md) | 3 — skill | one demand, everything else held | to the demand |

**The comparisons carry the result, not the layers.** E5 against E4 asks whether
skill capability predicts mechanism capability; E4 against E3 asks whether
mechanism capability composes into a system that serves a request. A null on the
second is the more interesting one, and `70-THINKING/02` predicts it if
aggregation rather than execution is what bounds the assembly.

**Each sheet states what it holds constant and is therefore blind to.** That
requirement is what survives of `E5-population-spread`, whose real argument was
general: *every experiment that holds the operator constant scores the system
minus the person using it.*

Two sheets were dissolved into this structure rather than deleted.
`E3-first-ladder` became E5 entire, because a graded ladder is the instrument of
the skill layer rather than a theme of its own. `E5-population-spread` became
the blindness requirement above. The former E4's size-and-tuning constraint now
applies at layers 2 and 3 alike, and its preparation sections — preflight, what
travels, what is collected, the specification contract — are shared by all
three and live in E4.

## The standing rule about order

Every ordering in this folder is a **claim, not a schedule**. Running only the top of
a ranked list confirms the ranking without ever risking it, and the ranking becomes an
unexamined premise.

Where testing the whole set is affordable, test the whole set: the entries predicted
to fail are what make an ordering falsifiable, and the one ranked last is often the
only one that can overturn the framework. Where it is not affordable, say so and
record the ranking as an untested assumption rather than letting it pass as a result.
