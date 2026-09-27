# Queue A — outsourceable development

> **DISCHARGED 2026-09-27.** A1a, A3's fetch, A4–A8, A10–A15 are merged and on
> `main`; A11–A13 exist as code that has never executed. What is still open moved
> into [`00-backlog.md`](00-backlog.md) — P0 for the model-facing contract, which
> inherits A1b and A2, and P2 for the rest. **This file is the record of how the
> queue was framed, not a live list.** Do not add to it; add to the backlog.

**What belongs here:** work whose acceptance is a test, not a judgement. An
agent picking this up cold should be able to finish an item and *know* it is
finished, without reading results or deciding what a number means.

**What does not belong here:** anything whose output is an interpretation. That
is [Queue B](09-queue-research.md).

**Standing rules for anyone working this queue**

- Every item below names a **done-when** that is mechanically checkable. If you
  cannot make it pass, stop and say so rather than widening the item.
- **Do not change what the model sees** without moving a key. Model-facing text
  feeds `processor.adapter_fingerprint()`; sampling and protocol feed
  `run_suite._eval_params()`. A change that reaches the model and moves no key
  silently pools two populations — see `50-findings/15`.
- **Do not interpret results.** If an item surfaces a surprising number, record
  it and move on; Queue B reads it.
- `findings/` is append-only. Corrections are appended as addenda, never edited
  in place.

---

## A1 — Route the client through the backend seam *(hard blocker)*

`experiments/M4-ephemeral-processors/backends.py` exists, is verified equivalent
to the live path, and **is imported by nothing**. Until the client routes
through it, nothing can run off this machine, and the H100 has no Ollama.

**Do:** make `ollama_client.generate()` / `chat()` delegate transport to
`backends.get(BACKEND)`, keeping the meter, the transcript sink, the recovery
layers and the truncation guard exactly where they are. Those are model
behaviour, not transport.

**Done when:** `seam_equiv`-style checks pass on `/api/generate` and
`/api/chat`+tools at temperature 0 — same text, same `prompt_eval_count`, same
tool calls — and a full `run_suite --arm monolith --tasks wf2_retry --reps 1`
produces a row indistinguishable from one taken before the change.

**Do not:** move `_calls_from_text`, `_calls_from_xml`, `_calls_from_bare_args`
or `_repair_json` into the backend. They are model traits and travel with the
weights, not with the server.

## A2 — Finish the OpenAI-compatible backend against a real server

`OpenAICompatible` in `backends.py` is written but never executed.

**Do:** stand up `llama-server --jinja` locally, point `LATTICE_BACKEND=openai`
at it, and exercise: plain completion, tools, a tool-result turn, and a
truncation. Fix what breaks. `gen_s` stays 0 on this path — do not fill it with
a wall clock that includes queueing.

**Done when:** the same four cases that pass on Ollama pass here, and
`probe_tool_channel.py` runs end to end against it.

## A3 — Supply chat templates matching each model's reserved tokens

On vLLM and llama.cpp the chat template is ours. Choose it from the model's own
tokenizer rather than authoring one.

**Do:** for each of the three models, dump the reserved special tokens, fetch
the official `chat_template.jinja` from its HF repo, and store both under
`evalkit_store/model_contracts/<model>/`. Where the official template exists,
use it verbatim.

**Done when:** each model has its template and token table on disk, and
`reconstruct_ollama_prompt.py`-style verification shows the rendered prompt from
our supplied template matches the official one by token count on four message
shapes.

**Why this shape:** Ollama's renderer turned out to be a byte-identical
transcription of NVIDIA's own template. Reading the source first would have
short-circuited a week. Do the same here.

## A4 — Make every probe persist its raw values

`probe_implementer_tail.py` now writes `evalkit_store/probe_runs/*.json`. The
others do not, and a summary is a lossy encoding chosen before the question is
known. A `-22%` median already cost a 74-minute rerun because the values were
gone.

**Done when:** `probe_tool_channel`, `probe_temperature_tail`,
`probe_action_nudge`, `probe_recovery_live` and `probe_slot_bleed` each write
their per-call measurements to `evalkit_store/probe_runs/`.

## A5 — Tolerate partial transcript tails everywhere

Readers crash on a `.jsonl.gz` still being written, which happens whenever a
sweep runs concurrently with analysis. This has bitten twice.

**Done when:** a shared helper reads a transcript, stops cleanly at a truncated
final line, and every analysis script uses it. `transcripts.py` already has the
tolerance — lift it out rather than reimplementing.

## A6 — A matrix reader

`report_nudge_sweep.py` reads one arm by adapter fingerprint. The matrix is
3 models × 11 arms and there is no reader for it.

**Done when:** one command prints, from the store and not from logs, per
model × arm: n, objective pass, run_ok, crashes, regressions, and the
`tool_native` / `tool_recovered` / `tool_repaired` / `tool_malformed` counters —
with **consistent denominators**, deduplicated on `(cell_id, rep)`. Job logs
under-report because `--store-resume` skips cells; the store is the source.

## A7 — Paired-comparison tooling

Backlog P2 calls this the cheapest experimental improvement available, needing
no new runs: which tasks *flip* between two arms carries more than 16/34 against
24/34, because it names a condition rather than a magnitude.

**Done when:** given two `(model, arm)` pairs, one command emits the flip table —
tasks passing in A and not B, B and not A, both, neither — plus the counts, read
from the store.

## A8 — Surface the recovery and tool counters in the run report

They are on the row and absent from the markdown `run_suite` prints, so a reader
sees a score with no indication of how much help it took.

**Done when:** the per-arm report shows interventions, native/recovered/repaired
counts, and the escalation count beside the pass rate. Beside it — never folded
into it.

## A9 — The bootstrap occupancy test

Backlog P2: runnable now, depends on nothing, M0-shaped, and answers both
remaining rows of `STATUS.md`'s blocking-holes table. It is
[M17](01-MILESTONES/17-mandate-chain.md)'s first work package and blocks the
rest of that milestone.

**Done when:** the measurement is run and recorded per that milestone's spec.

## A10 — Annotate the `[TOOL_CALLS]` overclaim in Findings 15

The sheet says `[INST]`, `[AVAILABLE_TOOLS]`, `[TOOL_CALLS]` are "dead in use".
They were probed once, under Mistral-style framing that contradicted the
model's in-context instructions. A reserved token that produced nothing in one
contradictory context is not a dead token.

**Done when:** an addendum states what is actually supported — those tokens are
not used by Ollama's renderer, and their status under a consistent framing is
untested. Append; do not edit the original claim.

---

## A11 — `monolith_test`: the worker decides when to probe the gate

**The variable is not "can the worker see tests".** `dloop` already answers
that, and answers it maximally: `_dloop_core` scores the workspace every round
and feeds the failing subtest **names** straight back into the prompt —
`m6_arms.py:102-106`, `f"Current state still fails:\n{hint}"`. 184 rows were
collected that way. The harness does the probing, every round, unasked.

The open variable is **who decides when to probe**. `monolith_test` is
`monolith` plus a `run_tests` tool the model calls at its own discretion. Paired
against `dloop`, that is one variable: model-driven probing against
harness-driven probing, with the model-driven side also paying turns for it.

**Do:** add `run_tests` to a **per-arm tool set**, granted to this arm only.
Report the gate — exit status and the subtest fraction. Withhold the structural
dimensions, which `run_suite.py:314-316` already keeps separate from the gate
and which `objective_pass` alone measures. Cap the number of invocations per
task and record the count on the row beside the score, never folded into it.

**Done when:** the arm runs a full suite; the row carries the invocation count;
and — the part that is easy to get wrong — `processor.adapter_fingerprint()` for
every **other** arm is byte-identical to its value before the change. Default
`TOOLS` in `roles.py` is untouched. Check this by computing the fingerprint
before and after and diffing, not by reading the diff.

**Do not** put the arm in `run_suite.py` or `m6_arms.py`. `arm_source_path()`
hashes the whole file, so a new arm in either one moves `arm_sha` for
`baseline`/`monolith`/`monolith_recovery` or for `dloop`/`staged`, and silently
detaches them from every row already collected. New file, new entry in
`_M6_ARM_FILES`.

**Do not** give `run_tests` the scoring command as-is. The worker would be
iterating against the instrument that grades it, and `gate_pass` would stop
measuring anything. `objective_pass` is what survives contamination here; that
is why both readings are recorded side by side.

## A12 — `author`: the audit yields or writes the worker's brief

Stage 1 of the judge-anchored family already produces `expected` — 2 to 5
observable conditions, written before any work exists — and `expected` reaches
the judge in three arms and the implementer in **zero**. This arm turns that
stage from a reporter into an author.

**Do:** a new M7 workflow, `author_workflow.py`. Stage 1 produces one of three
outcomes: yield for missing context, decline an unsound request, or write the
worker's brief. Then the implementer runs against that brief. No judge.

Note that this **grants the stage authority the current prompt explicitly
denies it** — `judge_anchored_workflow.py:194-195` reads "You do NOT decide
whether the task should be attempted." That sentence goes. It is a role change,
not a config change, and the prompt is rewritten rather than patched.

**Done when:** the arm registers, appears in `_M7_ARMS`, runs a full suite, and
each run records which of the three outcomes stage 1 took.

## A13 — `author_judge`: the same, with a judge

A12 plus a judge, so the briefing effect is separable from the judging effect.

**Use `judge_fullctx`.** Operator decision 2026-09-27, and it has a structural
reason rather than a score behind it: `judge_fullctx` uses **no conditions at
all** -- no `expected`, no `checked`, no `n_conditions`, one call producing one
verdict. `50-findings/18` shows the condition-checklist judges fail by
compounding 11% per-condition noise through an `all(yes)` rule into 33% verdict
noise, at a rate set by how many conditions the auditor wrote. `judge_fullctx`
cannot fail that way, because there is no conjunction to compound.

**This promotes A14 to a hard prerequisite for this item.**
`judge_fullctx_workflow.py` records neither `model` nor `results_subdir`, which
is exactly why B9 could not be read for it. An arm built from that workflow
inherits the gap and will be as unreadable as its parent. Fix the tagging
first, or this arm produces another unattributable pile.

**Name the thing that changes underneath it.** `judge_fullctx` is defined as a
judge "holding the same material the worker held". In this arm that material
now includes the authored brief, so the judge checks the work against the same
brief that produced it. That is a coherent design -- it asks whether the worker
did what it was told -- but it is no longer the independence test the arm was
built for, and the run record should say which of the two is being run.

**Done when:** as A12, plus the judge's verdict recorded per task.

**The control for both** is the existing `judge_caveat`: same audit stage, same
judge, differing only in whether the worker is briefed.

## A14 — Bring the untagged workflows up to `judge_caveat`

**Narrowed by the addendum to `50-findings/17`.** This is not "add cell ids to a
broken pile". `judge_caveat_workflow.py:690,693` already records `model` and
`results_subdir`, and `judge_bypass` does too — each has 34 cleanly
attributable matrix records, which is what made a clean judge read possible
without this item. `judge_fullctx`, `m7*` and `test_synth` lack those two lines,
and `judge_fullctx` therefore has nothing to attribute its 286 records by.

`stage_influence_*.jsonl` is append-only across every sweep ever run and carries
no cell id. `judge_caveat` holds 1446 records over 170 distinct `(task, rep)`
keys — up to 13 per key — across three models, with 458 carrying no model at
all. `judge_fullctx` carries a model on **zero** of its 286 records. Any join
against `results/*.json`, which is one sweep, silently crosses models. See
`50-findings/17`.

**Do:** have every workflow write `LATTICE_CELL` and `LATTICE_REP` onto its
stage record. `run_suite.run_task` already computes and exports both
(`run_suite.py:255-258`); nothing needs deriving.

**Done when:** a reader can group stage records by cell id and every group is
single-model, single-protocol, single-sampling; and a join to the store on cell
id returns the same n as the group size. Old records stay as they are — they are
unrecoverable, and that is the finding.

**Do not** backfill the existing pile by guessing. Records that predate the
change are not attributable and must read as such.

---

## Explicitly not in this queue

Choosing between temperature 0.6 and 1.0; deciding whether recovery earns its
place; reading the matrix; auditing S1–S8. Those need judgement about what a
number means and live in Queue B.
