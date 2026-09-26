# Queue A — outsourceable development

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

## Explicitly not in this queue

Choosing between temperature 0.6 and 1.0; deciding whether recovery earns its
place; reading the matrix; auditing S1–S8. Those need judgement about what a
number means and live in Queue B.
