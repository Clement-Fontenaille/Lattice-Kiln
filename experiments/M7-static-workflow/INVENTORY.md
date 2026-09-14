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
