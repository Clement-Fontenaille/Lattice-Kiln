# m7c — the independent judge, expected effect recorded before the run

_2026-09-14, before `m7c_workflow.py` was executed. Not revised afterwards._

## The hypothesis being tested

`50-findings/07` measured a 7B panel added to a deterministic gate and found it made
things **worse**: 9/10 alone, **6/10** with the panel. Its verdict was that a 7B does
the doing and cannot do the judging, and that the gap is not a prompt away.

That panel **shared the context of the work it judged.** The operator's hypothesis is
that sharing the context was the variable, not the judging. m7c isolates it: the judge
sees the request, the premise audit's note, and the diff — and **no check output, no
implementer text, no retry hint**.

## What the judge is not allowed to do

**It has no authority and that is the experiment.** Its verdict is recorded and scored
against the check afterwards; no terminal reads it, and the arm behaves identically
with the judge and without it.

Wiring it in before measuring it would rebuild `staged`, which is the arm that scored
19/30 by letting a model probe produce terminals. `11-static-workflow.md` forbids it in
so many words: no lone model probe may flip a terminal state.

## The methodological trap, stated before it can be fallen into

**Roughly a third of this suite's tasks will end with an empty diff** — the five
false-premise tasks the arm correctly declines, plus whatever it fails to move.

On an empty diff, `not_met` is *trivially* correct for any task demanding work, and
the judge needs no judgement to get there. **If the judge scores well overall and its
accuracy vanishes once empty diffs are excluded, it is not judging — it is detecting
emptiness, which `len()` does for nothing.**

So the judge is scored **twice**: over all tasks, and over the non-empty-diff subset
alone. **The second number is the result.** The first is a floor anyone could reach.

## The second trap: is it echoing the audit?

The judge is handed the premise audit's note. The audit found 2 of 5 false premises
and raised 9 spurious concerns (`50-findings/10`, finding 6).

**If the judge returns `unsound_request` mostly where the note is non-empty**, it is
not judging the request, it is repeating an earlier reader whose precision is 18%.
That is measurable: cross-tabulate the verdict against whether the note was empty, and
against the truth. Independence from the worker is worthless if it is dependence on
the audit instead.

## The prediction

**1. Overall agreement with the check: 60–75%.** Inflated by the empty-diff cases.

**2. On the non-empty-diff subset: 50–65%**, which is near chance for a three-way
verdict weighted the way this suite is. This is the honest prediction and it follows
from `07`'s second failure mode: the panel emitted confident-wrong `not_met` on
correct code, miscounting what the code did. **Misreading code is not a context
problem, and isolating the context does not fix it.**

**3. The judge gets `wf3_refactor` right where the check cannot.** The truncated task
passes its check while the work was not done; the judge sees *extract a shared helper*
against an empty diff and should say `not_met`. **This is the one place the judge holds
information the check lacks**, and it is also an empty-diff case, so it proves less
than it looks.

**4. `wf3_refactor_witnessed` gets the same verdict from the judge as its twin.** The
pair differs only in the check, and the judge never sees a check. **If the two verdicts
differ, the judge is reading something it was not given** and the isolation leaks.

**5. Bias toward `met`.** `07` recorded that no reviewer framing beats an approval
bias at 7B. Independence removes the worker's advocacy from the context, so this is
the prediction most likely to be overturned — and overturning it would be the first
real evidence for the operator's hypothesis.

**6. Cost: one call per task**, about 31 calls, a few minutes.

## What would make this worth wiring in

Not overall accuracy. **Precision on `not_met` over non-empty diffs** — how often the
judge says the work is unfinished and is right. That is the number a workflow could
act on, because it is the one that decides whether to keep iterating.

Below roughly 80% it is not usable as a gate, and `07`'s arithmetic says why: adding a
noisy verdict to a gate that is already right most of the time subtracts.

## What this run cannot settle

Whether a judge helps. It has no authority, so it cannot help or harm. It settles
whether the verdict is **worth** authority, which is the question that must come first
and did not, last time.

---

# Addendum: the judge variants, and what separates them

Three arms now differ **only in the judge's prompt and how its text is folded in**.
The judge's inputs are identical throughout — the request, the audit's note, the diff,
and no check output — and the keeper is mechanical and blind to the verdict in all
three.

| arm | the judge's text | how it is folded in | orientation |
|---|---|---|---|
| `m7c` | a **critique** (`why`) | *"A reviewer ... objects: ... Address it or show it does not apply."* | none |
| `m7e` | an **instruction**, imperative | `Also: {instruction}`, beside the mechanical hint | none |
| `m7f` | the same instruction | the same | **five worked examples + what produced the inputs** |

## What each pair isolates

**`m7c` against `m7e` — register.** findings-log entry 6 names the trigger as
conversational text and the failure as narration instead of writing. A critique is one
of the three cases it names. An instruction is the register the implementer already
receives. *If both behave alike, the harm is model prose as such and `register` is my
gloss describing nothing.*

**`m7e` against `m7f` — orientation.** Operator's point: the judge has no intuitive
grasp of what produced its inputs. It does not know a 7B wrote the diff in a loop, that
an empty diff is ambiguous between *could not* and *correctly refused*, or that the
note it is handed has 18% precision. `m7f` says all three and shows five examples.

## Predictions

**1. `m7f` separates `unsound_request` from `not_met` better than `m7e`.** This is the
one distinction the diff cannot carry — both look like an empty diff, and only the
request tells them apart. Two of the five examples exist for exactly this, so if
orientation buys anything it should show here first. **Measured on the five
false-premise tasks**, where the correct verdict is `unsound_request`.

**2. `m7f` echoes the note less.** Told the note is unreliable, it should agree with it
less often than `m7e` does. If the echo rate is unchanged, being told is not enough.

**3. The `met` bias survives in all three.** `50-findings/07` found no reviewer framing
beats approval bias at 7B, and neither register nor examples is a framing it did not
try. Overturning this would be the first real evidence for the operator's hypothesis
that context independence was the missing variable.

**4. Cost rises slightly with `m7f`** — 800 extra prompt tokens per judge call, up to
a dozen calls per task.

## What would make the whole line negative

If `m7f` is no better than `m7e`, and `m7e` no better than `m7c`, then none of
register, orientation or examples moves a 7B judge — and `07`'s verdict stands wider
than it was stated: not *this framing fails* but *framing is not the variable*.

That is a real possible outcome and it is worth as much as the positive one, because it
would close a line of work rather than leave it open and untried.
