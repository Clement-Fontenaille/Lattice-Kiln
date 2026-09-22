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

## What the layers are for

Stated by the operator, 2026-09-22. The three layers are steps in one sequence,
and the sequence ends somewhere none of them reach:

1. **Work out the boundary of what a model can be expected to provide.**
2. **Work out which roles are likely to help and which are not.**
3. **Actually test them** — not reason about which ought to work.
4. **See what sticks.**
5. **Assemble a system** out of what survived.
6. **Validate that the process raises the system+user ceiling.**

Steps 1 and 2 are what E5 and E4 are for. Step 3 is the folder's motto — *run
the arm you expect to lose*. Step 4 is why entries carry demotion criteria
written before the data. Step 5 is not an experiment and has no sheet.

### Step 6 is the fourth ceiling, and it is not satisfaction

The terminal quantity is `70-THINKING/02`'s **system+user ceiling**: *the
integrated system with the human operator in the loop — the grain the
operator-plus-system pair can still reach together.* It is measured in the
same unit as every other lift in this project, **rungs**, and it is the only
one of the four ceilings that has never been measured.

**It was briefly written here as "user satisfaction", and that was wrong in a
way worth recording.** Contentment is a byproduct of work being good, not the
target, and naming it as the target inverts the programme:

- A score that rewards satisfaction rewards **agreeableness**, which is H3 —
  the competing hypothesis this folder carries precisely because it cannot yet
  be told apart from a capability limit.
- `50-findings/14` measured the judge producing `unsound_request` in **zero of
  eight cells**. A satisfaction metric would score that failure as a success,
  because refusing is the unsatisfying move.
- The design stance is the opposite one: **be unpleasantly reluctant to carry
  out obviously erroneous requests.** A system that is pleasant about a bad
  premise is failing, and the whole false-premise apparatus — `decline_expected`,
  E5's S3, the `unsound_request` verdict — exists to catch exactly that.

So the quantity is the grain of work the pair can reach, not how the person
feels about reaching it.

### What is still unmeasured, and what the restructure cost

The **measure** exists and is in the project's own vocabulary. The
**instrument** does not.

Raising the system+user ceiling means varying the operator, and the sheet that
would have done it was `E5-population-spread` — dissolved on 2026-09-22 into a
blindness requirement on every layer. That dissolution was correct for what it
fixed and it removed the only sheet pointing at step 6, which is a consequence
of the restructure rather than a pre-existing gap.

It was blocked anyway, on the same thing it is still blocked on: an **operator
population**. `70-THINKING/01-use-cases.md` §2 is empty.

Two things follow, and they are separable:

- **Every score in this folder measures the assembly with the operator held
  constant**, which scores the system minus the person using it. The distance
  between that and the system+user ceiling is unmeasured rather than small.
- **Step 5's assembly cannot be validated by steps 1–4.** Passing every layer
  is consistent with an assembly that raises no ceiling once a person is in the
  loop.

**Owner: none.** The largest unowned gap in the evaluation programme, and it
needs an operator population before it needs a design.

## The three sweep layers

Reorganised 2026-09-22. E3, E4 and E5 no longer carry a theme each; they carry
a **layer** each, and the comparisons between them are the point.

| sheet | layer | subject | can it attribute? |
|---|---|---|---|
| [`E3`](E3-functional-requests.md) | 1 — functional | a whole system answering a request phrased as a user would phrase it | **no**, by design |
| [`E4`](E4-capability-sweep.md) | 2 — mechanism | one role's mechanism, the rest of the system held | to the mechanism |
| [`E5`](E5-skill-scales.md) | 3 — skill | one demand, everything else held | to the demand |

**The comparisons carry the result, not the layers.** Two of them, each with its
own name so neither gets called "the transfer test":

- **skill-to-mechanism transfer** — E5 exit rungs predicting E4 mechanism scores.
  A null says the candidate skill list is wrong, not that the mechanisms are.
- **mechanism-to-function transfer** — E4 mechanism scores predicting E3
  outcomes. A null says mechanism capability does not compose, and locates the
  constraint *between* mechanisms rather than inside any of them.

The second null is the more consequential, and `70-THINKING/02` predicts it if
aggregation rather than execution is what bounds the integrated system ceiling.

Terms that look generic — demand ladder, exit rung, item family, subject,
visible and held-out check — are defined once in
[`E5`](E5-skill-scales.md#terms-used-on-this-sheet) and used the same way in all
three sheets.

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
