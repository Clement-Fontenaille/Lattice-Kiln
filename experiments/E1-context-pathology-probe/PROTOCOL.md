# E1 Protocol — first move: does context blur generalise past `wf6`?

Paths are relative to the repository root. No model is called. The parsing trap
from `E0-suite-construct-validation/PROTOCOL.md` Part 0 applies here too —
booleans are stored as strings in some rows; normalise through a helper that
**raises** on anything unexpected.

---

## Step 1 — Fix the claim so it can fail (read before coding)

The claim being tested, in the form that can lose:

> Under higher load, **low-salience requirements are dropped preferentially**
> while the core deliverable holds.

Two distinct outcomes that are **not** this claim, and must not be reported as it:

| observation | what it actually is |
|---|---|
| everything degrades together as load rises | ordinary overload. Real, but not *selective* — the blur mechanism is not needed to explain it |
| low-salience requirements are low-scoring **at every load level** | a constant, not a load effect. Means those requirements are simply harder or less often attempted |

The claim requires an **interaction**: the gap between core-deliverable
performance and low-salience-requirement performance must **widen** with load. A
main effect alone does not support it.

**Salience is assigned now, before looking at any score**, to avoid labelling
whatever dropped as "low-salience" after the fact:

| tier | dimensions |
|---|---|
| **core** | `SUBTESTS`, `final_sub` — the gating dimension, what the task is nominally *for* |
| **low-salience** | `doc`, `todo`, `DOCSCORE`, `TODOSCORE` — declared in `wf6_multi`'s own docstring as quality signals that do not gate |
| **ambiguous — excluded** | `STRUCTSCORE`, `PERFSCORE`, `AUDITSCORE` and any other domain dimension. These are neither the gate nor obviously peripheral. **Excluding them is a choice; record it** |

Write this table into the output. If a later reader disagrees with the
assignment, they can recompute — but they can see what was decided in advance.

---

## Step 2 — Part A: the anecdote, checked properly (1 hour)

**Source:** `experiments/M5-intelligent-orchestration/pipeline_lab/results/results.json`
(12 rows, 6 `wf*` tasks × 2 reps).

1. For every row, extract `final_sub` (core), `doc` and `todo` (low-salience),
   and `total_calls`.
2. Tabulate per task: core score, doc score, todo score.
3. Answer three questions, in this order:
   - Is `wf6_multi`'s 0/4 and 0/3 reproduced from the data? **If not, stop** —
     the anecdote that motivates this whole line is wrong, and that is the
     finding.
   - Do the other five `wf*` tasks that carry `doc`/`todo` show the same
     direction (low-salience below core)?
   - Is `wf6_multi` the task with the **most** simultaneous requirements? If yes,
     that is the load story's one supporting data point. If no, the load story
     is weakened at its own origin.

**Output:** `results/blur_partA.md` — the per-task table and the three answers.

**Six tasks, two reps. State it:** this part cannot establish a trend. It can
only confirm or kill the anecdote and show whether its direction is shared.

---

## Step 3 — Part B: does it hold across the M6 corpus? (3 hours)

**Source:** `experiments/M6-evaluation-suite/results/<arm>.json`, all 18 arms.
Exclude `results_nemotron_llamacpp/` — a different model confounds this, and
reading it would also break E2's pre-registration (see
`../E2-grain-versus-quantity/PROTOCOL.md` Step 0).

1. Keep only rows where `struct` is non-empty.
2. For each row compute:
   - `core_rate` = `final_sub[0] / final_sub[1]`
   - `low_rate` = mean of `earned/total` over `struct` keys in the
     **low-salience** tier; skip the row if it has none.
   - `gap` = `core_rate − low_rate`.
3. Build the load proxy. **Use all three, report all three separately** — do not
   average them into one index, which would hide disagreement between them:

| proxy | computed as | weakness to state in the output |
|---|---|---|
| **L1 — requirement count** | number of distinct dimensions the task is scored on (`len(struct)` + 1 for subtests) | conflates "more to do" with "more to hold" |
| **L2 — worker view** | `worker_view` field: `full` vs. narrowed | binary, and confounded with scaffold design |
| **L3 — context budget** | 16384 for arms run before the 2026-09-15 cut, 8192 after (documented in `M4-ephemeral-processors/ollama_client.py`) | **the arms differ in scaffold as well**, so this is not a clean dose |

4. For each proxy, regress `gap` on the proxy. Report the slope, its sign, and a
   scatter — **not** a p-value alone. With this sample, an eyeball on the scatter
   is worth more than a significance test, and a significance test invites
   reading noise as structure.

**The decision rule, fixed now:**

| result | reading |
|---|---|
| `gap` **widens** with load on ≥2 of 3 proxies | the blur claim survives its first real check. Motivates a controlled experiment; still not a controlled result |
| `gap` **flat** across proxies | no selectivity. The `wf6` observation does not generalise; report as such |
| `gap` **narrows** | against the claim. Report loudly — a predicted effect running backwards is worth more than a confirmation |
| proxies **disagree** | report the disagreement as the result. Do not pick the proxy that worked |

**Output:** `results/blur_partB.md` and `results/blur.json`.

---

## Step 4 — Write down what this does and does not license

Into `results/blur.md`, and then into the sheet. Required statements, not
optional caveats:

1. Whether `wf6`'s anecdote reproduced.
2. Whether the pattern generalised, per proxy.
3. That **no controlled load axis exists** in this data, so this is observational.
4. That `struct` covers ~6–10 tasks per arm, so Part B's corpus is a third of the
   suite at most.
5. If the result is positive: the **next** experiment is a controlled dose —
   same task, same scaffold, systematically varied irrelevant-context volume —
   and that experiment does not exist yet.

---

## Step 5 — The blocking gap, recorded not solved

Whatever this returns, append to the sheet the gap found on 2026-09-16:

> **E1's probe has no specified feature space.** The sheet says "probe"
> throughout without stating whether it reads attention weights, hidden-state
> activations, or output-level logprobs. The battery cannot be designed until
> this is decided, and it is a design decision rather than something further
> reading will settle.

Record it as an open decision with a date. It blocks the rest of E1 regardless of
what the first move returns.

---

## Done when

`results/blur_partA.md`, `results/blur_partB.md` and `results/blur.md` exist; the
sheet carries the outcome with its five required statements; and the feature-space
gap is recorded as an open decision.
