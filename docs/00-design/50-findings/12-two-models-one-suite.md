# 12 — Two models on one suite: what varies with the model and what does not

**Subjects:** `qwen2.5-coder:7b-instruct-q4_K_M` and
`nemotron-gpu` (NVIDIA Nemotron Nano 9B v2, Q4_K_L, `num_gpu 99`)
**Recorded:** 2026-09-17 / 2026-09-18
**Artifacts:** `experiments/M6-evaluation-suite/results/` (qwen, N=3–5),
`experiments/M6-evaluation-suite/results_nemotron/` (Nemotron, N=1),
`experiments/M6-evaluation-suite/replay.py`
**Metric:** `objective_pass` under the 2026-09-18 ruling — the check's exit code
**and** every recorded dimension at full marks. `gate_pass` carries the exit-code-only
reading on the same rows.
**Scope:** eight arms complete on both models. Nemotron is a single rep per task;
qwen is collapsed by strict majority over its reps.

## Totals

Six tasks are excluded from every figure below: the five false-premise tasks and
`wf3_refactor`, which `baseline` passes under this metric. The remaining **28
tasks** are what an arm can earn.

| arm | Nemotron | qwen | difference |
|---|---|---|---|
| `staged` | 16 | 10 | **+6** |
| `judge_anchored` | 18 | 15 | +3 |
| `judge_bypass` | 15 | 15 | 0 |
| `m7f` | 16 | 16 | 0 |
| `monolith` | 13 | 13 | 0 |
| `test_synth` | 17 | 17 | 0 |
| `judge_fullctx` | 15 | 16 | −1 |
| `judge_staged` | 16 | 17 | −1 |
| **total** | **126** | **119** | |

Median wall per task across those arms: Nemotron 54.5 s, qwen 53.9 s.

## 1. The decline set is fixed by the suite, not by the model

Tasks a majority of reps terminated as `declined`, per arm × model cell:

**Seven, and the same seven, in 22 of 24 cells** — `hf_already_optimal`,
`hf_cache_nondeterministic`, `hf_dead_code`, `hf_remove_validation`,
`wf4_assumption`, `wf3_refactor`, `wf3_refactor_blindview`. The `declined` rate is
0.206 (7/34) in every judge arm for both models.

Three classes of exception, all accounted for:

| cell | count | why |
|---|---|---|
| `monolith`, both models | 0 | the arm emits `done` only; it has no decline terminal |
| qwen `dloop`, `m7`, `n5_dloop`, `n5_m7` | 6 | recorded on 30 tasks, before the suite gained `wf3_refactor_blindview` |
| **qwen `staged`** | **15** | see §2 |

Two models of different architecture, parameter count and training decline the
same seven tasks in the same arms. Five of those seven are the false-premise
class; the other two are `wf3_refactor` and its truncated-view twin.

## 2. qwen `staged` declines eight further tasks and changes no file on them

The eight: `hf_audit_perf`, `hf_csv`, `hf_json_field`, `hf_json_serialize`,
`hf_merge_config`, `hf_misfiled_bug`, `hf_path_sanitize`, `hf_suppress`.

Subtest counts before → after, all three qwen reps against Nemotron's one:

| task | qwen `staged` | Nemotron `staged` |
|---|---|---|
| `hf_csv` | `declined` 3→3/6 ×3 | `needs-change` 3→**5**/6 |
| `hf_json_field` | `declined` 2→2/5 ×3 | `resolved` 2→**5**/5 |
| `hf_json_serialize` | `declined` 2→2/5 ×3 | `needs-change` 2→**5**/5 |
| `hf_misfiled_bug` | `escalate`/`declined` 3→3/4 ×3 | `resolved` 3→**4**/4 |
| `hf_suppress` | `declined` 3→3/4 ×3 | `resolved` 3→**4**/4 |
| `hf_merge_config` | `declined` 3→3/6 ×3 | `escalate` 3→3/6 |
| `hf_path_sanitize` | `declined` 1→1/8 ×3 | `escalate` 1→1/8 |
| `hf_audit_perf` | `declined` 2→2/2 ×3 | `resolved` 2→2/2 |

**qwen `staged` moves no subtest on any of the eight, in any rep.** Nemotron
`staged` moves five of the eight. On the three where neither moves
(`hf_merge_config`, `hf_path_sanitize`, `hf_audit_perf`) the two models still
record different terminals.

Median wall on `staged`: qwen **22.1 s**, Nemotron **54.8 s** — against 53.9 s and
54.5 s overall. `staged` is the only arm where qwen's wall falls to a third of its
own median.

The eight extra declines account for the whole `staged` difference in the totals
table. qwen's 10/28 on `staged` is its lowest earned score of any arm.

## 3. The judge arms match on score and differ on intermediate state

Terminal distribution, as a fraction of executed rows:

| arm | model | `answered` | `blocked-partial` | `blocked-no-progress` | `declined` |
|---|---|---|---|---|---|
| `judge_bypass` | Nemotron | 0.441 | **0.059** | **0.294** | 0.206 |
| | qwen | 0.451 | **0.167** | **0.176** | 0.206 |
| `m7f` | Nemotron | 0.471 | **0.029** | **0.294** | 0.206 |
| | qwen | 0.471 | **0.135** | **0.194** | 0.200 |
| `test_synth` | Nemotron | 0.500 | **0.059** | **0.235** | 0.206 |
| | qwen | 0.524 | **0.112** | **0.159** | 0.206 |
| `judge_fullctx` | Nemotron | 0.441 | **0.088** | **0.265** | 0.206 |
| | qwen | 0.500 | **0.124** | **0.171** | 0.206 |
| `judge_staged` | Nemotron | 0.471 | **0.029** | **0.294** | 0.206 |
| | qwen | 0.510 | **0.118** | **0.167** | 0.206 |

`answered` differs by at most 0.059. `declined` is identical to three decimals in
four of five arms. **`blocked-partial` is 0.029–0.088 for Nemotron against
0.112–0.167 for qwen, in all five arms, with no overlap between the two ranges.**
`blocked-no-progress` runs the other way, 0.235–0.294 against 0.159–0.194, also
with no overlap.

The five arms are separate runs of separate scaffolds. The direction is the same
in every one.

## 4. `judge_anchored`: eleven tasks differ, seven one way and four the other

| Nemotron passes, qwen does not | Nemotron terminal | qwen terminal |
|---|---|---|
| `hf_csv` | `answered` 6/6 | `blocked-partial` 5/6 |
| `hf_misfiled_bug` | `answered` 4/4 | `blocked-no-progress` 3/4 |
| `hf_rename` | `answered` 6/6 | `blocked-no-progress` 4/6 |
| `hf_timeout_param` | `answered` 6/6 | `blocked-no-progress` 2/6 |
| `wf2_retry` | `answered` 5/5 | `blocked-partial` 3/5 |
| `wf5_partial` | `answered` 7/7 | `blocked-partial` 5/7 |
| `wf6_multi` | `answered` 6/6 | `blocked-partial` 6/6 |

| qwen passes, Nemotron does not | Nemotron terminal | qwen terminal |
|---|---|---|
| `hf_extract_fn` | `blocked-no-progress` 5/5 | `blocked-no-progress` 5/5 |
| `hf_merge_config` | `blocked-no-progress` 3/6 | `answered` 6/6 |
| `hf_path_sanitize` | `blocked-no-progress` 1/8 | `answered` 8/8 |
| `hf_retry_backoff` | `blocked-no-progress` 2/4 | `answered` 4/4 |

Net +3 to Nemotron. `hf_extract_fn` is the one row where both models reach the
same terminal and the same subtest count and the verdict still differs: qwen's
`STRUCTSCORE` is 3/3 in three of five reps, Nemotron's is 1/3.

## 5. `wf3_refactor` and its pair

`wf3_refactor` is declined by a majority in every arm on both models, and is one
of the six tasks excluded from the totals. Its witnessed twin
(`wf3_refactor_witnessed`) records `STRUCTSCORE 3/3` on every rep of every
scaffolded arm for both models. The blind and witnessed readings diverge in one
place only: qwen `monolith`, blind 3/3 against witnessed 1/3.

## What is not established here

- Nemotron is **N=1**. A single rep per task carries the rep-to-rep variance that
  `50-findings/…` E7 measured at 6 of 16 paired cells on the M4/M5 fixture. The
  qwen column is a majority over 3–5 reps and is therefore filtered where the
  Nemotron column is not.
- Eight arms of sixteen. `dloop`, `m7`, `m7b`, `m7c`, `m7e`, `judge_caveat` and
  `test_synth_retry` were still running or incomplete on one side when these
  figures were taken.
- Every difference except `staged` (+6) is one or two tasks out of 28.
- The two subjects differ in parameter count (7B / 9B), architecture
  (transformer / hybrid Mamba-2), quantisation (Q4_K_M / Q4_K_L) and training
  lineage simultaneously. Nothing here attributes a difference to any one of them.

## Addendum, 2026-09-18 — Nemotron ran with two of its three stages dark

Everything above was produced with Nemotron's **premise-audit stage and judge
stage returning empty text on every call, in every arm.**

### The measurement

Structured-output parse rates, per arm, with each Nemotron block verified
against its results file by terminal match (34/34, or 22/22 for `m7b`):

| arm | audit parsed, Nemotron | audit parsed, qwen | judge parsed, Nemotron | judge parsed, qwen |
|---|---|---|---|---|
| `judge_anchored` | **0/34** | 160/190 | **0/34** | 174/189 |
| `judge_bypass` | **0/34** | 273/311 | **0/34** | 204/220 |
| `judge_caveat` | **0/34** | 84/102 | **0/34** | 102/102 |
| `judge_fullctx` | **0/34** | 150/170 | **0/34** | 169/170 |
| `judge_staged` | **0/34** | 89/102 | 0/34 | 0/102 |
| `m7f` | **0/34** | 148/170 | 3/34 | 170/170 |
| `m7b` | **0/22** | 100/114 | — | — |
| `test_synth` | **0/34** | 155/239 | — | — |

No exception was recorded on any of them: `error` is `None` and `parsed` is
`False`, so `re.compile(r"\{.*\}", re.S)` found no object in the returned text.

### The cause

`NVIDIA-Nemotron-Nano-9B-v2` is a reasoning model. Ollama returns its reasoning
in a separate `thinking` field and leaves `response` empty until the model exits
the thinking block. `ollama_client.generate()` reads `payload["response"]`.

Reproduced directly against the `judge_anchored` audit prompt:

| `num_predict` | `done_reason` | `thinking` | `response` | `{…}` present |
|---|---|---|---|---|
| 200 | `length` | 922 chars | **0 chars** | no |
| 800 | `length` | 3439 chars | 266 chars | no |
| 1536 | `stop` | 1345 chars | 565 chars | **yes** |

The audit and judge calls are issued at `num_predict=200` and `220`
(`judge_anchored_workflow.py`, and the same two values in `judge_bypass`,
`judge_caveat`, `judge_fullctx`, `m7e`, `m7f`, `m7b`). At those budgets the model
is still inside its thinking block when generation is cut, so `response` is the
empty string.

The implementer calls use `generate()`'s default `num_predict=1536` and are
unaffected. That is why work still lands: **every Nemotron figure in this
document was produced by the implementation stage alone.**

### What this does to the sections above

- **§3 stands and is sharpened.** The judge arms match on `answered` within
  0.059 and on `declined` to three decimals — with qwen's judge parsing 92–100%
  and Nemotron's parsing 0%. The judge stage was not merely unhelpful on one
  model; it was absent, and the scores did not move.
- **§1 stands.** The seven-task decline set is produced without the audit stage
  on the Nemotron side, so it is not audit-driven.
- **§4 is not a comparison of judging.** `judge_anchored` +3 compares qwen with
  a working judge against Nemotron with none.
- **§2 is unaffected by this.** `staged` is an `m6_arms` arm; the eight extra
  qwen declines and the unmoved subtest counts do not depend on the audit or
  judge stages.
- **The totals table is not a model comparison at equal footing.** It is
  qwen-with-three-stages against Nemotron-with-one.

### Open

No figure here establishes what Nemotron scores with its audit and judge stages
functioning. Raising `num_predict` on those two calls, or reading the `thinking`
field, would produce that; neither has been done.

## Addendum 2, 2026-09-18 — the reproduction, and two separate constraints

Probe: `experiments/M6-evaluation-suite/probe_reasoning_budget.py`,
results in `experiments/M6-evaluation-suite/results/reasoning_budget.json`.
The audit prompt is read from `judge_anchored_workflow.py` rather than retyped,
and the objectives and sources come from the suite fixtures.

### The answer exists; the budget never reaches it

Eight real objectives, `num_predict=2048`, Nemotron:

| task | `done_reason` | eval tokens | thinking chars | response chars | `{…}` |
|---|---|---|---|---|---|
| `wf1_crossfile` | `stop` | 330 | 867 | 574 | yes |
| `hf_csv` | `stop` | 620 | 1900 | 742 | yes |
| `wf5_partial` | `stop` | 868 | 2500 | 631 | yes |
| `hf_timeout_param` | `stop` | 735 | 2608 | 631 | yes |
| `hf_merge_config` | `stop` | 713 | 2111 | 995 | yes |
| `hf_path_sanitize` | `stop` | 774 | 2437 | 903 | yes |
| `hf_rename` | `stop` | 817 | 2759 | 603 | yes |
| `wf4_assumption` | `stop` | 1105 | 4892 | 440 | yes |

**Eight of eight produce valid JSON when allowed to finish.** The arms allow 200.

### The requirement is not a constant

Same prompt (`hf_timeout_param`), same temperature 0.3, ten reps at
`num_predict=4096`:

```
eval_count: min 609  median 1166  max 2635  mean 1348
```

A 4.3× spread on identical input. Completion rate by cap, over those ten:
**200 → 0/10, 800 → 3/10, 1536 → 7/10, 2048 → 8/10.** Raising the cap does not
make this reliable; the reasoning expands to use what it is given.

### `/no_think` does not work through this path

At the arm's own cap, three variants:

| variant | `done_reason` | thinking | response |
|---|---|---|---|
| baseline | `length` | 884 | **0** |
| `/no_think` as system message | `length` | 836 | **0** |
| `/no_think` as prompt prefix | `stop` | 729 | **0** |

The prefix changes the stop reason and still returns nothing.

### qwen control

Same prompt, `qwen2.5-coder:7b-instruct-q4_K_M`: `thinking` is 0 chars at both
200 and 1536, response 820/839 chars, JSON found at the arm's own cap. **The
prompts are not the problem.**

### Two constraints, not one

**Ollama's API-level `think` parameter turns the reasoning channel off**, which
neither `/think` control token did:

| request | `done_reason` | thinking | response |
|---|---|---|---|
| default | `length` | 926 | `''` |
| `"think": false` | `stop` | **0** | `{"ok": true}` |
| `"think": true` | `stop` | 435 | `{"ok": true}` |

With reasoning off, a second constraint appears: **the answer alone overruns
200 tokens.** At `think=false, cap=200`, five of eight runs still return
`done_reason=length` with 715–872 chars of response truncated mid-object — 3/8
parse. The audit answer for this prompt costs a median of 212 tokens.

Raising the cap with reasoning off is reliable:

| setting | parsed |
|---|---|
| `think=false`, cap 300 | **8/8** |
| `think=false`, cap 400 | **8/8** |
| `think=false`, cap 600 | **8/8** |

Against 0/34 in production.

### The invisible part

`ollama_client.generate()` checks `if "response" not in payload: raise`. The key
*is* present; its value is the empty string. Nothing in the harness distinguishes
"the model returned nothing" from "the model returned something unparseable", so
thirteen arms recorded `parsed: False, error: None` and were read as a model
that judges badly.

`done_reason == "length"` with an empty `response` is an unambiguous signature of
truncation before any answer, and is available on every call.
