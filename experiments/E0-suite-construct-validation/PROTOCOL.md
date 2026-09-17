# E0 Protocol — construct validation of the M6 suite

Paths are relative to the repository root. Four parts, independent of each other;
run them in this order because each is cheaper than the next. No model is called
at any point.

---

## Part 0 — The parsing trap, read before writing any code

`objective_pass` and the other booleans are stored **as strings** in some rows
(`'True'`, `'False'`) and as real booleans in others.

```python
bool('False')   # True  <-- this will silently invert your entire analysis
```

Every script in this folder must normalise through one helper and use it
everywhere:

```python
def as_bool(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        if v == 'True':
            return True
        if v == 'False':
            return False
    raise ValueError(f'not a boolean: {v!r}')
```

It raises rather than guessing. A silent `False` here would corrupt every number
downstream and would not look wrong.

---

## Part 1 — The untouched-source test (1 hour)

**The question:** for every task, does the **untouched source** fail the check?
Where it passes while the objective demands work, some part of the demand has no
mechanical witness.

**The data:** the `baseline` arm makes no model call and changes no file, so its
rows *are* the untouched source run against every check.
`experiments/M6-evaluation-suite/results/baseline.json`, 34 rows, 1 rep.

**Procedure:**

1. Load `baseline.json` and `tasks.json`.
2. For each task, record `objective_pass` (normalised via `as_bool`) and the
   task's `expect.objective_pass` from `tasks.json`.
3. Classify:

| baseline passes? | task demands work? | reading |
|---|---|---|
| no | yes | **correct** — the check has a witness |
| yes | no | **correct** — false-premise task, doing nothing *is* the answer |
| **yes** | **yes** | **DEFECT** — the demand has no witness. Name the task |
| no | no | check is wrong in the other direction — the untouched source fails a task it should pass. Name it |

"Task demands work" is read from `tasks.json`'s `expect` block, not from
judgement.

4. Write `results/untouched_source.md`: the four counts and, named individually,
   every task in the two defect rows.

**Expected:** `wf3_refactor` appears in the DEFECT row — it is the already-known
case, and its appearance is the check that this analysis works. If it does
**not** appear, the analysis is wrong, not the sheet. Stop and debug.

**What this test cannot do, and must say so in its own output:** it is
**necessary, not sufficient**. A task whose demand has three clauses, two
witnessed and one not, fails at baseline on the strength of the first two and
reports nothing wrong here. The sufficient form is per clause and is Part 2.

---

## Part 2 — What defect 1 actually costs (2 hours)

**The question:** if structural dimensions were folded into the gate, how many
published results change?

This does **not** decide the repair. It prices it, so the decision is made
against a number rather than an intuition.

**Procedure:**

1. For every arm file, for every row with a non-empty `struct`, compute:
   - `gated_pass` = `as_bool(objective_pass)` — what is published today.
   - `full_pass` = `gated_pass AND all(earned == total for earned, total in struct.values())`.
2. Report, per arm: rows compared, rows where the two disagree, and the
   disagreement rate.
3. Report, per task: which tasks account for the disagreements.
4. Recompute each arm's headline score both ways and put them side by side.

**Output:** `results/defect1_cost.md`, containing the table:

| arm | rows with struct | gated score | folded score | flipped |
|---|---|---|---|---|

**Read it against this, decided now:** if folding changes arm *ordering* — not
just scores — then every published arm comparison is contingent on a metric
choice nobody made deliberately, and the repair decision becomes urgent. If
ordering is unchanged, the repair is a clarity fix rather than a correctness one,
and can be scheduled rather than rushed.

**State the coverage limit in the output:** only ~6–10 tasks per arm carry
`struct`, so the folded score is computed on a third of the suite and is **not**
a corrected headline number. It is a sensitivity estimate.

---

## Part 3 — The item analysis (half a day)

This is the half the sheet was opened for. Standard item analysis, decided before
looking.

**Build the response matrix.** Rows = tasks (34). Columns = one attempt per
`(arm, rep)` across all 18 arms. Cell = `as_bool(objective_pass)`.

**Before computing anything, write this limitation into the output**, because it
determines what the numbers can mean:

> The "subjects" here are **scaffolds on one model**, not models of differing
> ability. Classical item analysis assumes subjects spanning an ability range.
> An item–total correlation computed over pipelines answers *"does this item
> separate pipelines"*, which is related to but not the same as *"does this item
> measure the construct"*. E4 is the experiment that would supply real ability
> spread; until it runs, every number in this part is about pipeline
> discrimination.

**The three measures:**

1. **Difficulty distribution** — per task, the fraction of attempts passing.
   Plot/report the histogram. Items at 0.0 or 1.0 discriminate nothing.
   Report counts at the floor and the ceiling by name.
2. **Item–total correlation** — per task, point-biserial correlation between that
   item's pass/fail and the attempt's total score across the other 33 items
   (exclude the item itself from the total — including it inflates the
   correlation mechanically). Flag any item with correlation ≤ 0: an item where
   *better* attempts do *worse* is almost always a broken check, not a subtle
   one.
3. **Dimensionality** — eigenvalues of the inter-item correlation matrix, with
   **parallel analysis** (compare observed eigenvalues against eigenvalues from
   random data of the same shape) to decide how many factors are real. Report
   the scree values, not just the count.

Then, and only then: do the `stresses` tags correspond to the recovered factors?
That is the sheet's candidate clustering and it is a **check on the tags**, not
on the factors.

**Output:** `results/item_analysis.md` and `results/item_analysis.json`.

---

## Part 4 — Write the decision the sheet is waiting on

Defect 1 has two available repairs and the sheet records that **neither has been
chosen**. After Part 2 has priced them, write the choice down — as a decision,
with its date and its reason:

- **Fold the dimensions into the exit code.** Changes what the suite gates on.
  Every prior comparison must be re-scored or explicitly marked as measuring the
  old metric.
- **Rename the metric and report dimensions alongside.** Changes nothing about
  the suite and everything about how its numbers read. Cheaper, and the sheet
  warns it is the easier one to get wrong quietly — because the old numbers keep
  circulating under a name that now means something narrower.

Record it in the sheet as an operator ruling with a date, the same way the
2026-09-14 remedy for defect 3 was recorded. **Not choosing is also a decision**
and should be written as one, with its reason, rather than left implicit.

---

## Done when

`results/untouched_source.md`, `results/defect1_cost.md` and
`results/item_analysis.md` exist; the sheet's status line reflects what ran; and
the defect-1 repair decision is written down with a date, even if the decision is
"deferred, because X".
