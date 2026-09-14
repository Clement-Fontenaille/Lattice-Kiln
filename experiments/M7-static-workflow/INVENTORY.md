# M7 workflow — strengths, weaknesses, remediation candidates

_2026-09-14, from the N=1 run (30 tasks), `dloop` at N=5 (150 runs), and
`stage_influence_n1.jsonl`. Every line is tied to a measurement; nothing here is
tied to intent._

## Strengths

| | evidence |
|---|---|
| **Advisory premise audit** | `staged`'s 7 false declines → 1, at **one** call instead of three, parsed 30/30 |
| **Incumbent-protected keeper** | `monolith` 7 regressions/30; `dloop` **0 across 150 runs** |
| **Mechanical decline** | 5 false-premise tasks declined 5/5 in every rep of `dloop`'s 150. No model judgement in the path |
| **Escalation stricter than the metric** | says `blocked` on `hf_extract_fn` / `hf_dict_dispatch` where `objective_pass` says True, because it reads `STRUCTSCORE` and the harness discards it |
| **Stage-influence record** | it is what found weakness 2. Without it that defect is invisible |

## Weaknesses

**1. The keeper compares counts, not sets.** One accepted losing trade on `wf6_multi`:
subtests 2/6 → 5/6 while `topo cycle`, green at baseline, went red.

**2. The concern split's model signal can only trigger a no-op.** Firing is
syntactic-or-model; segmentation is syntactic only. The two agreed on 29/30, so the
model half reproduces a regular expression.

**3. No cost governor.** One task took **43% of the arm's wall clock** and 11 calls.
Only a hand-set `TASK_CALL_CAP` bounds it, and nothing escalates on cost.

**4. The arm cannot detect an unwitnessed clause.** `wf3_refactor` false-declines
5/5, deterministically, because the refusal comes from the check's shape rather than
from a model.

**5. `blocked` conflates two situations that want opposite remedies.**

| | tasks | combined |
|---|---|---|
| no progress at all | `hf_extract_fn`, `hf_dict_dispatch`, `hf_rec_to_iter`, `hf_cache_decorator`, `hf_misfiled_bug` | unchanged |
| progressed, then stalled | `wf5_partial` 0→5, `wf6_multi` 2→10, `hf_timeout_param` 2→5 | rose |

The first group asks the operator *is this objective reachable?*; the second asks
*this specific remainder is unmet*. One terminal cannot carry both questions.

**6. The audit's classification is consumed by nothing.** 30 produced — 7 `bugfix`,
9 `feature`, 12 `refactor`, 2 `perf` — and **zero consumers**. Only `multi_concern`
is read, on 3 tasks. The cleanest retirement candidate the influence record has
produced.

## The audit is bad at what it is asked, and the inventory said otherwise

_Corrected 2026-09-14, same day, after an operator question: did the audit flag that
`wf3_refactor`'s objective has no witness?_

It did not, and it was never asked to — the prompt asks what looks wrong about the
**premise**, and `wf3_refactor`'s premise is entirely true. Checking that turned up
something worse.

**Scored against its nominal job, on the N=1 run:**

| | found | missed |
|---|---|---|
| 5 false-premise tasks | **2** | **3** |

Missed: `wf4_assumption` (O(log n) over unsorted data — impossible), `hf_already_optimal`,
`hf_dead_code` (the function "with no callers" has callers). Found, with correct
reasoning: `hf_remove_validation`, `hf_cache_nondeterministic`.

**And on the 25 sound tasks it raised 9 concerns**, all spurious — `wf1_crossfile`,
`hf_return_shape`, `hf_json_field`, `hf_cache_decorator`, `hf_csv`, `hf_path_sanitize`,
`hf_merge_config`, `hf_suppress`, `hf_json_serialize`.

**Eleven concerns emitted, two correct. Precision 18%, recall 40%.**

### The error this corrects, which is mine

The first inventory said the `concern` field "earns its place" because it was consumed
on 8 tasks. **Consumption is not correctness.** I counted that something was read, not
that it was right — the exact failure the influence record exists to prevent. The
record measures consumption; it cannot measure value, and reading it as value is a
mistake available to anyone using it.

Nine of the eleven concerns travel into an escalation payload addressed to a human and
point at a problem that does not exist. **A wrong concern is worse than none**: it
sends the operator looking in the wrong place.

### Strength 1 was two claims wearing one sentence

- **Making the audit advisory works.** Seven false declines became one. True, measured
  — and the value comes from **removing its authority**, not from the quality of its
  output.
- **The audit works.** False. 2 of 11.

The consequence is sharp: **5/5 decline accuracy comes from the mechanical rule, not
from the audit.** The system works *despite* it. An audit with this precision holding
decline authority is exactly what `staged` was.

### Two further candidates

**R7 — retire the premise half.** At 18% precision the `concern` field degrades the
escalation payload. The call can survive for segmentation, which is a different job and
is where `m7b` already moved it.

**R8 — ask it the question nobody asks.** *Is the completion of this objective
observable from this check?* — showing it `test_task.py`, which it does not currently
see.

This stays legitimate under the project's own position because **it decides nothing**.
It is the one use `50-findings/07` found for a panel: given a known failing check it
writes a correct, cited explanation — a reporting aid, not a decision aid. An audit
saying *I do not see how the check observes clause 2*, routed to escalation, is the
same shape. It does not repair the objective; it tells a person to.

## Remediation candidates

| | remedy | cost | expected effect |
|---|---|---|---|
| **R1** | keeper compares **sets** | trivial | removes the regression; **may reduce progress** on multi-dimension tasks |
| **R2** | per-task cost governor, escalate on exceeding | trivial | bounds the worst case; may lose `wf6` |
| **R3** | split `blocked` into *no-progress* / *partial* | trivial | no score effect; changes the escalation payload |
| **R4** | split: have the audit emit **segments**, or drop the model signal | low | removes the no-op |
| **R5** | retire the classification, or find it a consumer | trivial | no call saved — it rides the same call |
| **R6** | unwitnessed clause | — | **outside the arm.** A formulation repair, not code |

**R1 carries a warning rather than being a free correction.** It is strictly more
conservative and will reject candidates the current arm accepts. On `wf6_multi` the
arm reached combined 10 **by accepting the losing trade**; comparing sets rejects that
candidate and leaves it at 2. So R1 removes the regression *and* may move that task
from *progressed-then-stalled* to *no progress*. That is a real trade between
**not breaking things** and **getting further**, and it should be measured rather than
assumed benign.
