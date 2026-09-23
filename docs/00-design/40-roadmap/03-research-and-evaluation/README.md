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

## Standing rules

Accumulated across the sheets, gathered here so they are applied rather than
rediscovered. Each was adopted after something went wrong.

| rule | why it exists |
|---|---|
| **Write the null before the data.** | Every entry on every sheet carries what a flat result would mean. Written afterwards, a null becomes a reason to rebuild the instrument. |
| **State what you hold constant, and therefore what you are blind to.** | The former `E5-population-spread`'s real argument, generalised: holding the operator constant scores the assembly minus the person using it. Each layer now answers it. |
| **A candidate awkward for the framework gets written down, not left out.** | Decomposition, aggregation and ceiling self-location were each cut once for being hard to probe. That is a judgement about the designer, not the candidate. |
| **Transfer is the criterion, not narrowness.** | There is no positive definition of skill and none is needed. A candidate earns the name when its level on one item family predicts another. A subdivision that buys no transfer is a task feature. |
| **Roles run in position. Nothing is stubbed.** | `70-THINKING/02`'s standing assumption forbids isolating an operation. What varies is what the assembly hands the role, never whether the role is there. |
| **No difficulty dials at the functional layer.** | Grading a demand while holding everything else constant is what `E4` and `E5` do. An `E3` item is as hard as the situation it came from; two drafts wrongly dialled directions 5 and 7. |
| **Borrow the task, author the check.** | A check that travels with a task has usually been seen alongside it. |
| **Data is eligible only if its setup was recorded, never inferred.** | Recovering setup by joining on `wall_s` put one cell at +22.7 points where the answer was +4.3. |
| **Report false rejection and false acceptance separately.** | `50-findings/14` found them moving in opposite directions under one variable. A combined correctness figure hides the entire effect. |
| **A number earns its ground before it is interpreted.** | Operator, 2026-09-23, named as a methodology principle. Once a script exists, extracting a figure is free and interpreting it is the path of least resistance — it arrives formatted, comparable, and looking like evidence. What it cost to compute says nothing about what it measures. Seven figures were misread in one session and every correction came from reading the underlying artifact, never from a better statistic. **This is what the feedback loops depend on:** a number fed into a firing rule without earning its ground is how an assembly degrades itself, confidently. |
| **Run the arm you expect to lose.** | The folder's motto, and the reason an ordering is a claim rather than a schedule. |

## Status, 2026-09-23

| sheet | layer | state |
|---|---|---|
| [`E0`](E0-suite-construct-validation.md) | — | **answered 2026-09-17.** Two factors, not unidimensional. Defect 1 open, repair undecided. Gates `E4`. |
| [`E1`](E1-context-pathology-probe.md) | — | first move run, **negative**. Probe battery blocked on an unspecified feature space. |
| [`E2`](E2-grain-versus-quantity.md) | — | forecast move run, **prediction failed**. Token-matched design not buildable yet. |
| [`E3`](E3-functional-requests.md) | 1 functional | **8 directions**, borrow/build settled, direction 3 has a worked example. Per-direction specs not written. |
| [`E4`](E4-capability-sweep.md) | 2 mechanism | **10 roles, ~22 mechanisms**, each with its null. R10 added late. Shared preparation for all three layers lives here. |
| [`E5`](E5-skill-scales.md) | 3 skill | **WIP with 4 convergence conditions.** 8 entries in three kinds — laddered, mapped, derived. No ladder built. |
| [`E6`](E6-corpus-digestion.md) | — | not run, gated on M8 having something to run. |
| [`E7`](E7-paired-reanalysis.md) | — | run over recorded data. |

**Nothing at any of the three layers has been run.** The preparation is the
work done so far.

## What is outstanding

Ordered by whether it blocks something else.

1. **Preflight** (`E4`) — run the 34 existing tasks once on the largest model.
   One run, and it decides whether the M6 evaluation suite still discriminates
   at that scale. Everything downstream assumes it does.
2. **`E5` revision after the mechanism unfold completes.** Two gaps have run
   upward from `E4` already — R1.1 breadth of correct execution has no partner,
   and R10.1 reading through alarming noise is not S2 with a bigger
   denominator. Two in a row suggests `E5` was drafted top-down. **Do not patch
   it entry by entry; finish unfolding and revise once.**
3. **The 3-and-8 split in `E3`**, left open when direction 3's worked example
   turned out to have both halves. Two readings recorded, neither adopted.
4. **An operator population.** Blocks the system+user ceiling, which is step 6
   of the arc and the only one of `70-THINKING/02`'s four ceilings never
   measured. `70-THINKING/01-use-cases.md` §2 is empty. **Unowned.**
5. **A compiled-language fixture family.** Direction 3's worked example is a
   heap overflow under one compiler and not another; every M6 fixture is
   Python, where the class does not exist. New ground, not an extension.
6. **The identifiability literature** (`70-THINKING/02` OQ-B), which `E5`'s
   convergence depends on and which is reading rather than building.

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
