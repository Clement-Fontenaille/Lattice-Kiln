# 10 — M7: the static supervised workflow

**Milestone:** [M7 — Static supervised workflow](../40-roadmap/01-MILESTONES/completed/07-static-supervised-workflow.md)
**Closed:** 2026-09-14
**Verdict:** **confirms narrowly, and the instrument is the bigger result.**
**Artifacts:** `experiments/M7-static-workflow/` (`m7_workflow.py`, `PREDICTION.md`,
`compare_arms.py`, `stage_influence.jsonl`);
`experiments/M6-evaluation-suite/results/m7.{json,md}`
**Prediction:** recorded before the run in `experiments/M7-static-workflow/PREDICTION.md`,
unrevised.

## The evidence question

> On the M6 suite, which workflow strategy gives the best outcome-per-call against
> the plain monolith and the always-on super-pipeline, and does the chosen one
> degrade safely — no regressions, honest escalation — on the tasks it cannot do?

## What was run

One new arm, `m7`, on suite 0.1.0 through M6's existing runner — same harness, same
scoring, same tasks. Four stages per `10-technical/11-static-workflow.md`: an
**advisory** premise audit (always), a **conditional** concern split, implement, and
the test-gated incumbent-protected keeper.

| arm | pass | regressions | decline | false declines | wall |
|---|---|---|---|---|---|
| `monolith` | 18/30 | 7 | 0/5 | 0 | 4.3 min |
| `dloop` | 24/30 | 0 | 5/5 | 1 | 6.8 min |
| `staged` | 19/30 | 0 | 5/5 | **7** | 11.8 min |
| **`m7`** | **24/30** | **1** | **5/5** | **1** | 13.7 min |

## 1. Making the premise audit advisory works, and it is the one clean confirmation

**`staged`'s seven false declines became one.** That one is `wf3_refactor`, named in
the prediction in advance as inherited from `dloop` rather than caused here.

The six recovered are exactly the six predicted — `hf_csv`, `hf_json_field`,
`hf_json_serialize`, `hf_merge_config`, `hf_path_sanitize`, `hf_suppress` — all tasks
`staged` refused while they were genuinely unfinished. An advisory stage cannot
produce a terminal, so it cannot produce a false one. **This is the mechanism working
for the stated reason**, and it is the only claim here the run establishes cleanly.

The audit also became cheaper. `staged` used a K=3 majority vote; that quorum existed
to make a *gate* safer, because a wrong decline was terminal. Advice needs no quorum.
One call, parsed cleanly on **30/30**.

## 2. The totals say "no difference" and the pairing says four tasks moved

`m7` and `dloop` both score 24/30. The paired reading — which the suite exists to make
available — shows something the total cannot:

| task | `dloop` | `m7` |
|---|---|---|
| `hf_multi_recipient` | fail | **pass** |
| `wf2_retry` | fail | **pass** |
| `hf_cache_decorator` | pass | **fail** |
| `wf5_partial` | pass | **fail** |

**Two gained, two lost, net zero.** And none of the four is a task the added stages
touched — the concern split fired on three tasks, and none of these is among them.

So **a four-task churn is available from run-to-run variance alone at N=1.** Milestone
6 concluded that "where the 6-task fixture put the arms within noise, the 30-task
suite is decisive." This narrows that: it is decisive for the **large** differences it
was reporting — the monolith's 7 regressions, `staged`'s 7 false declines — and it is
**not** decisive for the one-to-two-task differences the M7 design was built to
produce. A design whose predicted effect is +1 task cannot be evaluated on this
instrument at this N.

This is the clearest motivation yet for
[E0](../40-roadmap/03-research-and-evaluation/E0-suite-construct-validation.md) and
for repetition, and it was produced by an arm that scored *the same* as its
predecessor.

## 3. The incumbent-protected keeper protects a count, not a set

The single regression is `wf6_multi`, and it is the most consequential thing in this
entry.

Entry 8 describes the keeper as rejecting *"any subtest regression, even for a
structural gain."* The implemented rule is:

```
s["sub"][0] >= best["s"]["sub"][0] and s["comb"] > best["s"]["comb"] and s["py"]
```

It compares **how many** subtests pass. The evaluation harness, independently, judges
a regression by the **set** of failing check labels: `fin["fails"] - base["fails"]`.

On `wf6_multi`, `m7` took subtests 2/6 → 5/6 while a check that passed at baseline —
`topo cycle` — began failing. The count went up by three, so the keeper accepted it;
the set gained a member, so the harness recorded a regression. Both are behaving as
written. The documented guarantee is stronger than the implemented one.

**Why no earlier arm found this, corrected.** The rule is byte-identical in `dloop`
and `m7`, so what differs is where each arm *stopped*, not how careful it was.

| arm | subtests | structural | combined | regression |
|---|---|---|---|---|
| `monolith` | 2/6 — 2/6 | 0/4, 0/3 | 2 | no |
| `dloop` | 2/6 — 2/6 | 0/4, 0/3 | 2 | no |
| `staged` | 2/6 — **6/6** | 0/4, 3/3 | 9 | no |
| `m7` | 2/6 — **5/6** | 3/4, 2/3 | 10 | **yes** |

**The trade is only visible from a partial position**, and the three zeros above have
three different causes:

- `monolith` and `dloop` changed nothing on this task, so nothing could regress.
- `staged` fixed **every** subtest. With none failing at the end, the set of failures
  is empty and nothing can have entered it. Zero by exhaustion.
- `m7` stopped at 5/6. That is the only position where a subtest fails at the end, and
  therefore the only one where it can be checked whether that subtest was passing at
  the start.

So `dloop`'s zero says mostly that it did not move, and `staged`'s says it finished.
Neither is evidence about the rule. **A rule is only tested where it is actually
asked to choose.**

*(Corrected 2026-09-14, same day as written. This paragraph first said `m7` "is the
first arm to reach combined 10 — further than `staged`'s 9 — and reaching further is
what exposed the gap." That is wrong: `staged` reached further on subtests, 6/6
against 5/6, and regressed nothing. The error is recorded rather than silently
replaced, because it is the same count-versus-set confusion this finding is about —
combined 10 against 9 is a count, and it decided nothing.)*

This does not weaken the case for the keeper, which prevented the monolith's seven
regressions. It corrects what the keeper promises.

## 4. The conditional concern split is not carried by this run

It fired on **3 of 30** tasks. What each firing did:

- `hf_json_serialize` — split into 3, **answered**, combined 2 → 7. A clean win.
- `wf6_multi` — split into 3, **blocked**, combined 2 → 10 (further than any other
  arm) and the regression above. 356 seconds, **43% of the arm's entire wall clock**.
- `hf_csv` — fired on the model signal alone, **answered** in 2 calls and 10 seconds.

That third one is a build finding. **The firing signal and the splitting mechanism are
decoupled**: the stage fires on either the syntactic signal (the objective enumerates
its parts) or the model's `multi_concern` flag, but segmentation is purely syntactic.
When the model fires alone, the stage fires and has nothing to split. It ran as a
no-op and the outcome was unaffected.

The two signals agreed on 29 of 30 tasks, so the model half currently earns nothing it
could not get from a regular expression.

**Cost is one task, not the design.** Median cost was **2 calls and 10 seconds per
task**. Excluding `wf6_multi`, `m7` costs roughly 7.7 minutes against `dloop`'s 6.8 —
close to the 8–10 minutes predicted. The reported 13.7 total is one pathological task,
and reporting it as a per-arm cost would have hidden that.

## 5. Stage influence, which is what makes retirement possible

Recorded per task in `stage_influence.jsonl`, per the specification's requirement that
a stage's influence be a property of the build.

- Stage 1's prose `concern` was non-empty on **11** tasks and **consumed on 8** — the
  escalation payloads. The prediction said five to seven. It earns its place.
- Stage 1's `multi_concern` flag was consumed by the firing rule on **3**.
- Stage 2 fired on **3**, and acted on **2**.

**Nothing here is retired yet, and one thing is close.** Stage 2's model signal is
consumed three times, agrees with a regular expression on 29 of 30, and can only ever
trigger a no-op when it fires alone. The stage's *syntactic* half is doing the work.

## 6. The audit's own accuracy, which finding 1 did not measure

*(Added 2026-09-14, same day, after an operator question. It corrects finding 5
below, which counted consumption and called it value.)*

Finding 1 says making the premise audit advisory works, and it does. It says nothing
about whether the audit is any good, and scored against its nominal job it is not:

| | found | missed |
|---|---|---|
| the 5 false-premise tasks | **2** | **3** |

Missed `wf4_assumption` (O(log n) over unsorted data), `hf_already_optimal` and
`hf_dead_code`. On the 25 sound tasks it raised **9 spurious concerns**. Eleven
emitted, two correct: **precision 18%, recall 40%.**

**So the two claims inside finding 1 must be kept apart.** *Making the audit advisory
works* — seven false declines became one, and the value comes from removing its
authority. *The audit works* — it does not. **The 5/5 decline accuracy is the
mechanical rule's, not the audit's, and the system performs despite the stage rather
than because of it.** An audit at this precision holding decline authority is
precisely what `staged` was.

### What this corrects in finding 5

Finding 5 reported the `concern` field "non-empty on 11, consumed on 8 — it earns its
place." **Consumption is not correctness.** Nine of those eleven travel into an
escalation payload addressed to a human and point at a problem that does not exist,
and a wrong concern is worse than none because it sends the operator to the wrong
place.

The influence record measures whether an output was read. It cannot measure whether
the output was right, and reading consumption as value is a mistake the record invites
rather than prevents. That limit belongs beside the record wherever it is specified.

### What it adds to the candidates

**Retire the premise half of the audit**; the call survives for segmentation, which is
a different job. And **ask it the question nobody asks** — *is the completion of this
objective observable from this check?* — showing it the check, which it never sees.
That stays inside `50-findings/07`'s one demonstrated use for a model panel: a
reporting aid, not a decision aid. It decides nothing and tells a person to look.

## Where the prediction was wrong, and where it was right

| Predicted | Actual |
|---|---|
| 25/30 (range 24–26) | **24/30** — in range, at the bottom |
| +1 from `wf6_multi` | **wrong** — `wf6_multi` did not pass, and the reasoning behind the prediction misread entry 8's "2/6 → 6/6" as a pass when `DOCSCORE` kept the check failing |
| 0 regressions | **wrong — 1**, and it is finding 3 |
| 5/5 decline, 6th on `wf3_refactor` | **right**, exactly |
| six tasks recovered from `staged` | **right**, exactly those six |
| 8–10 min | **13.7** — wrong as stated, right excluding one task |
| stage 1 `concern` consumed on 5–7 | **8** |

Two of the three misses are more useful than the hits. Recording the prediction
beforehand is what makes that legible instead of retrofitted.

## What this changes

- **`10-technical/11-static-workflow.md`** — the keeper rule MUST be stated as a
  set comparison rather than a count, and the per-task call budget of 4 cannot
  survive a concern split (the figure came from `dloop`, which never splits).
- **Entry 8's keeper claim** is narrowed by finding 3. Per the append-only rule, this
  entry is that correction and entry 8 is not edited.
- **[E0](../40-roadmap/03-research-and-evaluation/E0-suite-construct-validation.md)**
  gains a direct motivation from finding 2, and repetition stops being optional for
  any comparison whose expected effect is one or two tasks.
- **M7's front half** remains unspecified and M9-gated. Nothing here bears on it.

## What was not tested

Scope checking. The workflow runs unscoped, which `10-technical/05` G4 classes as an
invalidity rather than a shortfall; a human supervised every run. **This is also the
last arm that can be compared cleanly against M4 and M5 on cost** — once
[M17](../40-roadmap/01-MILESTONES/17-mandate-chain.md) puts a model call in front of
every tool call, every arm pays something no earlier arm paid.
