# Attractor census — findings (M5 follow-up, wide first pass)

**Date:** 2026-09-01
**Model:** `qwen2.5-coder:7b-instruct-q4_K_M` (the M0 working default), temp 0.4,
K=3 per cell, 39 probes / 117 calls / 10 min.
**Why:** "keep tuning the bad static system." Instead of cataloguing where the 7B
*fails*, catalogue where it reliably *goes* for each role-relevant task shape, and
which framings move that motion. Input to the `+ground` judge experiment
(`../judge_lab/`) and to the goal re-evaluation.

Raw table: `summary.md`. Transcripts: `runs/<probe>__k<n>.txt`. Probe matrix:
`probes.py`.

> The census scores *motion*, not correctness — it says where to point a role and
> where to read the transcript. Correctness claims below are from reading the
> transcripts, not from the observation counts (the regexes under-count file
> emission; see "envelope" below).

---

## Doer currents

### 1. "Complete the fix" is a strong, correct current — indirection does not break it

`fix_indirection` (wf1: symptom in `orders.py`, root cause in `pricing.line_price`).
All three bare samples wrote the fix in **`pricing.py`** with the correct
`unit_price * qty` — none patched the symptom site. `fix_local` (cause named in
the objective) likewise 3/3. The M4/M5 worry that cross-file indirection defeats
the doer is **not** borne out on this task; the "find the real cause and emit the
whole corrected file" motion is reliable here.

### 2. Conversational context did *not* suppress file emission here

`plan_prose` and `critique_prose` framings (a plan / a critique in a labelled
section before the objective) produced **cleaner** file emission than `bare`
(1.3 vs 0.3 parsed blocks) and 3/3 correct file. This partially walks back
findings-log entry 6's "a 7B implementer is degraded by *any* conversational
context": the degradation in M5 was specific to how the processor pipeline
injected `extra_input` (unlabelled, mid-context), not to prose per se. A plan in
a **named, structured** section is fine — and `critique_prose`, which states the
answer ("the fix belongs in `pricing.line_price`"), trivially steers it there.

### 3. The one clean blind spot: false premises

`false_premise` (wf4: "rewrite `find()` to O(log n)" — impossible, the list is
unsorted). **3/3 implemented binary search. 0/3 noticed the precondition.** Every
sample opened with "To achieve O(log n) we need binary search" and emitted it,
`verdict: approve`. `here_is_file` framing: identical. The doer executes the
objective's surface; it does not test the objective's premise.

### 4. Multi-concern overloads it

`multi_concern` (wf6: algorithm + docstrings + `NOTES.md` + TODO gardening).
1/3 addressed all three concerns; file emission degraded (fence-wrapped, no
second file). The single-concern splits each landed their one concern but
**echoed the other concerns' stale state back unchanged** (e.g. `one_concern_algo`
returned the file with all three original `# TODO` lines intact). The model does
one thing well and is blind to the rest of the file's intent.

### 5. The output envelope is noisy — parse permissively, don't tighten the spec

The model borrows whichever file delimiter is most salient in its context:
~2/3 of doer samples wrapped the answer in a ```` ```python ```` fence and used
the **context's** `<<file: X>>` marker (or a `# FILE path=X` comment) instead of
the protocol's `<<<FILE path=X>>>`. The content inside was correct. Tightening
the marker spec fights this; a permissive parser (accept fenced bodies, `#`-form
and context-form markers) does not.

---

## Judge currents — no framing fixes the 7B judge

`review_wf3_broken` is the diagnostic: a shared-helper dedupe that **rounds**,
so `staff_price(1.567)` regresses `1.2536 → 1.25`. A real correctness defect.
Every framing rubber-stamped it 3/3:

| framing | motion | wf3_broken |
|---|---|---|
| `is_correct` ("is the objective met?") | asserts "without changing return values" | **approve ×3** |
| `predict_failure` ("name the input it fails on, else PASS") | outputs `PASS` — confidently, no trace attempted | **approve ×3** |
| `criteria_first` ("list what a correct solution must do, then check") | **reverse-engineers the criteria from the buggy code** — criterion #2 became "the helper must return the price *rounded to the nearest cent*", read off the candidate's own docstring — then declares them met | **approve ×3** |
| `strongest_reason` ("strongest reason it fails, or NO DEFECT FOUND") | "NO DEFECT FOUND" + assertion (the summary table's `approve:1` was a parse artifact — missing CONTROL blocks scored as `None`, not as rejections) | **approve ×3** |

`criteria_first` is not neutral, it is **harmful**: on the *correct* simple fix
(`review_wf1_correct`) it invented a qty-handling criterion and falsely rejected
2/3. Structured self-generated criteria give the model more surface to hallucinate
a spec that matches whatever code it is looking at.

Contrast the correct cases: `review_wf3_correct` and `review_wf1_correct` under
plain `is_correct` were approved 3/3 and 2/3. So the judge is not random — it is
**systematically biased toward approval**, and it approves broken and correct code
alike by asserting the property it was asked to check.

---

## The useful contrast: the planner engages the judgment the implementer suppresses

Same model, same task, "what should change and why" stance instead of "do it":

| probe | implementer stance | planner stance |
|---|---|---|
| wf4 false premise | 0/3 flag the unsorted precondition | **2/3 flag it** (`plan_false_premise__plan_bare`, `mentions_sorted_precond`) |
| wf6 multi-concern | 1/3 keep all three concerns | **3/3 keep all three** (`plan_multi__plan_bare`) |

The 7B's critical read is available — it switches on under a planning framing and
off under an execution framing. `plan_bare` ("3–6 imperative steps") beat
`whats_missing` ("list what does not exist yet"): the crisp step list held all
three wf6 concerns 3/3; the open framing collapsed to one item 2/3.

`plan_indirection` did not make the orders-only scoping mistake (0/3
`touches_orders_only`), but naming `pricing.py` explicitly was inconsistent —
the planner is better at *spotting a problem* than at *localising a fix*.

---

## What to ride, what to route around (next pass)

**Ride:**

- **Doer = objective + code in, whole corrected file out.** Keep its context free
  of unlabelled prose; a plan in a *named section* is acceptable, prose folded
  into the objective is best. Parse its output permissively.
- **One concern per doer pass**, over the file the previous pass produced. Not for
  tidiness — the model is structurally blind to concerns it wasn't handed.
- **A planner/analyst pre-pass** as the place a bad premise or a dropped concern
  gets caught — its *only* reliable critical faculty. Feed its output as a
  structured objective refinement, not as narration.

**Route around:**

- **Do not let the 7B vote on correctness.** No framing tested — neutral,
  adversarial, or structured — lifted it above "assert the property and approve".
  `criteria_first` made it worse. (Quantified in `../judge_lab/`.)
- **Do not ask the doer to judge its own premise.** That check belongs in the
  planner pass or in a deterministic precondition test.
- **Do not rely on `predict_failure` as a judgment prompt** — the 7B answers
  `PASS` with unearned confidence.
