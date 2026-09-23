# 15 — The output protocol is a variable, and nobody was varying it

**Subject:** `nemotron3-nano-4b` (NVIDIA Nemotron 3 Nano 4B, Q4_K_M,
`num_gpu 99`), one implementer prompt from `hf_retry_backoff`
**Recorded:** 2026-09-23
**Artifacts:** `evalkit_store/transcripts/`, the monolith run of the same date
**Scope:** n=4 per arm, **one prompt, one model.** Directional, not established.
**Verdict:** open — large enough to matter, small enough that it has not earned
its ground.

## The question

Every arm asks the model to answer in a format invented for this harness:

```
<<<FILE path=relative/name.py>>>
...the full new file content...
<<<ENDFILE>>>

<<<CONTROL>>>
{"terminal_state": ..., "summary": ..., "run": [...]}
<<<ENDCONTROL>>>
```

Nothing is trained on that. The operator asked how far it sits from a model's
training base, which is the right question and had never been asked here.

## The measurement

Same prompt, same model, same sampling — `temperature 0.2`, reasoning off,
`num_predict 1536`. Only the OUTPUT FORMAT section differs: the harness's
marker protocol, against fenced code blocks with the path on the fence line and
a `json` fence for the control object.

| response format | clean | degenerate | emitted code | emitted control |
|---|---|---|---|---|
| `<<<FILE>>>` (harness) | 2 | **2** | 4/4 | 3/4 |
| fenced blocks | **4** | **0** | 4/4 | **4/4** |

*Degenerate* means newlines collapsed to spaces — syntactically destroyed
Python — usually running to the token cap.

**Two of four degenerate under the harness protocol; none under fenced
blocks.** Control-block compliance goes 3/4 to 4/4 in the same swap.

## Two things it is not

Each checked rather than assumed:

- **Not the channel.** `/api/generate` sends the prompt raw; `/api/chat` has
  ollama apply the model's own `RENDERER nemotron-3-nano`. Four samples each:
  2 clean, 2 degenerate, **identically**. The chat scaffolding does not rescue
  it.
- **Not an invented marker.** An earlier note here claimed the model invented
  `<<<ENDFILE>>>`. It did not — the harness specifies it. The same note counted
  `<<<FILE path=ledger.py>>>` as a protocol slip when it is the **specified**
  form, and `<<<FILE prices.py>>>` as correct when it omits `path=`. That
  figure was backwards.

## Why it plausibly happens — and the claim unfolded

The shorthand used when this was first written was *"a fenced code block is the
nearest thing to a universal training base for emitting a file."* That is loose
in a way worth taking apart, because the sharper version makes a different and
checkable prediction.

### What a fence is actually the nearest base FOR

Ranked by how much text plausibly carries each, for the job of *handing over a
changed file*:

| format | where the training mass comes from | fit to this job |
|---|---|---|
| **unified diff** | every commit, every pull request, every patch mail | **best fit, and forbidden here** — the harness says *give the WHOLE file, never a diff* |
| **tool call** — `write_file(path, content)` | instruct and agent tuning; this model advertises `tools` | structurally exact: path and content as named arguments. Costs escaping every newline into a JSON string |
| **fenced code block** | markdown everywhere — READMEs, issues, answers, docs, chat logs | **partial.** Ubiquitous for *code*, weak for *whole files*, and it rarely carries a path |
| path as a heading, then a fence | tutorials, blog posts | common, but a convention rather than a format |
| **bespoke markers** — `<<<FILE path=...>>>` | this harness | none |

**So the fence is not the most-trained way to emit a file. The diff is.** What
the fence is nearest to is something narrower and, as it turns out, the thing
that was failing:

> A fence is the most ubiquitous wrapper for **code laid out as code**. Inside
> one, indentation and line breaks are overdetermined — the model has seen an
> enormous quantity of text where a fence opens and newline-structured source
> follows.

The observed failure was **lexical, not semantic**: newlines collapsing into
spaces, producing syntactically destroyed Python. That is exactly the layer a
fence constrains and `<<<FILE path=...>>>` does not. The marker says *a file
follows*; it carries no prior about how source is shaped, because no such prior
was ever formed for it.

### What the fine-tuning format actually is — read from the vocabulary

Pretraining mass was the wrong thing to reason about. What decides how a model
behaves when *instructed* is what post-training taught it to emit, and for this
model that is readable straight out of the GGUF's token table:

```
<unk>  </s>  [INST]  [/INST]  [AVAILABLE_TOOLS]  [/AVAILABLE_TOOLS]
[TOOL_RESULTS]  [/TOOL_RESULTS]  [TOOL_CALLS]  <|im_start|>  <|im_end|>
<think>  </think>  <tool_call>  </tool_call>  <tool_response>  </tool_response>
<SPECIAL_18> ... <SPECIAL_39>
```

**Vocabulary presence is not trained usage, and reading that list as the tuning
format was an error.** Probed directly with `raw: true`, so ollama's renderer is
bypassed and the model sees exactly the bytes sent:

| wire format offered | response |
|---|---|
| `[AVAILABLE_TOOLS]…[/AVAILABLE_TOOLS][INST]…[/INST]` | **2 tokens, empty** |
| `<|im_start|>role … <|im_end|>` | 110 tokens, a real answer |

`[INST]`, `[AVAILABLE_TOOLS]`, `[TOOL_RESULTS]` and `[TOOL_CALLS]` are
**inherited tokenizer slots the model was not tuned on** — in the table, dead in
use. The live interface is **ChatML**:

```
<|im_start|>user
Create hello.py containing a main() that prints 'hi'. Use the tool.<|im_end|>
<|im_start|>assistant
We need to create a file hello.py ... Use write_file tool.
</think>
{"path": "hello.py",
 "content": "def main():
    print('hi')
if __name__ == '__main__':
    main()"}
```

So what the tuning actually uses: **ChatML turn markers, `</think>` closing a
reasoning span, and tool arguments as JSON with content newline-escaped.**
NVIDIA's note that tool calling uses XML-style tags **"to reduce character
escaping"** describes `<tool_call>`, which ollama's parser decoded on the
rendered path but which this raw probe did not elicit — the tool-definition
injection format the renderer uses was not observed.

**`<<<` and `<FILE` do not appear.** The harness's delimiters are ordinary text,
several BPE pieces each, carrying no learned state change.

That gives three tiers rather than the two the earlier note implied:

| delimiter | status in this model | what it signals |
|---|---|---|
| `<|im_start|>`, `</think>` | **reserved token, verified live** — the model answers under it and is silent under the unused slots | a state change: what follows is of a known kind |
| ` ``` ` | ordinary text, enormous **pretraining** mass | a strong prior that code follows, laid out as code |
| `<<<FILE path=...>>>` | ordinary text, **no mass at either stage** | nothing |

**The harness's format is structurally right and lexically unknown.** It does
exactly what NVIDIA's design intends — a delimited region holding raw,
unescaped content — using delimiters the model has never been trained to treat
as a boundary. That is a narrower and more plausible account than "the format is
alien": the *shape* matches the tuning, the *tokens* do not.

**Consistent with the tool-call check.** Asked to write a file through its
native tool interface, the model produced a clean call with the content's
newlines correctly escaped in the JSON string — the exact structure that
collapses under `<<<FILE>>>`.

**Still inference.** That `<<<` is absent from the vocabulary is verified. That
its absence *causes* the degeneration is not; a delimiter can be unfamiliar
without being harmful, and the fence is unreserved too yet did not degenerate.
What the vocabulary establishes is that the three formats sit at three
different distances, which is what the comparison needs.

### The prediction this makes, which the measurement did not test

If the fence works by supplying **layout** rather than by explaining the task,
then swapping formats should:

- **remove the degeneration** — measured, 2 of 4 to 0 of 4;
- **improve protocol compliance** — measured, 3/4 to 4/4;
- **and leave the correctness of the change roughly alone.**

The third was **not measured.** `clean` means *not degenerate*, which is a
property of the text and not of the work. A model can emit beautifully
formatted code that fixes nothing. **If fencing lifts correctness too, this
explanation is wrong or incomplete**, and the cause is something broader than
layout.

That is the sharper falsifier, and it is cheaper than the cross-model one: run
the fenced variant through the real check on the real suite rather than
eyeballing the text.

### What the harness gave up

Forbidding diffs is a deliberate choice — a whole file is unambiguous to apply
and a diff can fail to apply, which on a fixture matters. The cost has not been
stated anywhere: **the format with by far the most training mass behind it is
excluded for harness convenience**, and every model is asked instead for whole
files in a wrapper that has none.

Whether that trade is worth it is now an open question rather than an
assumption, and it is answerable — apply-failure rate against degeneration
rate, both measurable.

### What cannot be verified

"Universal training base" is a claim about training data, and Nemotron's
composition is not public in the detail this would need. What is defensible is
narrower: **fenced code is ubiquitous in public text**, and whether it is
ubiquitous in *this model's* corpus is an inference from that, not an
observation.

The measurement stands on its own either way — the swap changed the outcome.
The explanation for why is where the assumption sits, and it is the part to
attack.

**This is a mechanism argument, not a measurement.** It is offered to be
falsified, and the obvious falsifier is another model: if qwen degenerates at
the same rate under both formats, the protocol is not the cause.

## Why it matters beyond one model

**The output protocol is part of what every arm measures, and it has been held
fixed and unexamined since M4.** A score under it is a joint measurement of
capability and of familiarity with a bespoke format, and the two cannot be
separated by any amount of repetition.

That has a direct consequence for cross-model comparison, which is what
`50-findings/12`, `/14` and the E4 sweep all rest on:

> A model whose training contained more agent-protocol text will score better
> for a reason that has nothing to do with the task. The comparison is not
> unfair in a way that averages out — it is biased toward whichever model has
> seen more of the harness's dialect.

It also bears on `40-roadmap/03-research-and-evaluation/E3`'s borrow-or-build
discussion from a direction that was missed there. Contamination was treated as
a property of the **task**. This is contamination of the **protocol**, and it
is the harness's own choice rather than something inherited from a corpus.

## What this does not establish

**n=4, one prompt, one model.** It does not establish a rate, and it does not
establish that the protocol is the cause rather than a correlate — only that
substituting a near-training-base format removed every degeneration in this
sample while improving compliance.

The standing rule applies to this sheet as much as to any other: *a number
earns its ground before it is interpreted.* This one has earned a direction and
an experiment, not a conclusion.

## What would settle it

1. **The same swap across models.** If qwen and nemotron 9B are insensitive and
   the 4B is not, it is a property of the smaller model rather than of the
   protocol.
2. **The same swap across the suite**, not one prompt, at n=5.
3. **A third and fourth format.** The model's native tool-calling interface,
   which it advertises as a capability and which is structurally exact for
   path-plus-content. And a **unified diff**, which carries the most training
   mass of any option and is currently forbidden by the harness rather than by
   any measurement.
4. **Correctness, not just cleanliness.** Every figure here is a property of
   the text. Run the fenced variant through the real check: if it lifts
   `objective_pass` as well, the layout explanation is incomplete.

Until then the protocol stays as it is, because changing it mid-programme would
put every existing row in a different regime from every new one — and unlike
sampling, the protocol is **not** in the setup key, so that change would be
invisible in the data.

**That last point is a defect in its own right.** `arm_sha` and `prompt_sha`
capture the arm's source and its prompts, so a protocol change inside an arm
would move them — but the protocol is shared boilerplate across arms, and
nothing records it as the variable it has now been shown to be.

---

## Addendum, 2026-09-23 — the protocol is now a keyed variable, and the tool
## path is not a drop-in

The sheet above closes by saying the protocol stays as it is, because changing
it mid-programme would put every new row in a different regime from every old
one **invisibly**, the protocol not being in the setup key. The operator then
asked for the swap directly. It has been built, and the invisibility was fixed
first rather than accepted.

### What is keyed now

`params.protocol` is `tools` or `markers`, recorded **unconditionally** on every
row — unlike `think`, `min_predict`, `temperature` and `top_p`, which are keyed
only when explicitly set. The protocol is not an optional departure from a
default; it is a choice every run makes.

Rows recorded before today carry no such key, and `params_match` reads an absent
one as `markers`. That is a **declared backfill of a fact**, not a wildcard: the
marker protocol was the only one that existed, every legacy row ran under it,
and a row that genuinely ran under tools always carries the key explicitly.
Without the backfill, keying the protocol would have orphaned the entire
existing corpus. Verified in both directions — a legacy row matches a `markers`
query and is refused by a `tools` query.

Two further gaps closed on the way, both the same defect as the one the sheet
names: `temperature` and `top_p` were made settable earlier today but were
**never added to `_eval_params`**, so the high-temperature Nemotron runs were
keyed identically to the runs they were meant to be compared against.

### Three things the build established that the measurement had not

**1. The tool protocol is inherently multi-turn. The marker protocol was not.**

Measured on `nemotron3-nano-4b`: turn one returns `write_file` and stops. It
does not emit `conclude` until a tool *result* has been appended and it is asked
again. A call is a turn boundary — that is how the format was tuned — so a
single-shot request gets one call and no conclusion.

This is the substantive structural difference, and it was not visible from the
vocabulary or from the one-shot probes. `run_processor` now drives a loop
(`MAX_TOOL_TURNS = 6`) that feeds back `"recorded"` per call and stops on
`conclude`. Nothing is realized inside the loop; every proposed effect still
goes through the gate afterwards, exactly as FILE blocks did. The model is told
its call was received, never that it was permitted.

**2. Ollama's parser is not uniformly reliable, and its failure looks exactly
like a model failure.**

`qwen2.5-coder:7b` emitted a **perfectly well-formed**
`{"name": "write_file", "arguments": {...}}` with correctly escaped newlines,
and Ollama returned it as plain `content` with `tool_calls` empty. The model
complied; the server-side extraction did not fire.

Scoring that as a model failure would be precisely the confusion this sheet is
about, so the client now recovers such calls from the text by brace-matching
(`_calls_from_text`). **This weakens the "native channel" framing**: the tool
path is a channel whose reliability varies per model *and per Ollama template*,
not a uniformly trained one. Anything comparing models across this protocol must
report the recovery rate, or it will attribute a template gap to a model.

**3. First directional evidence on the real check, not on cleanliness.**

The sheet's fourth open item was that every figure in it is a property of the
text rather than of the work. One matched pair, `monolith` / `wf2_retry` /
`nemotron3-nano-4b` / `min_predict 2048`:

| protocol | subtests base → final |
|---|---|
| markers | 0/5 → **0/5** |
| tools | 0/5 → **3/5** |

**n=1 per side. This earns nothing.** It is one draw on one task on the model
that was already known to sit at the floor, and it is reported here only because
it is the first figure in this sheet that touches `objective_pass` rather than
the shape of the text. If it survives the suite at n=5 it also *falsifies the
layout explanation* above — layout was predicted to leave correctness roughly
alone, and this moved it.

### What is not done

- **No cross-model run.** The falsifier the sheet asks for first.
- **The recovery rate is not recorded per row.** It should be, before any
  cross-model comparison uses this path.
- **The unified diff remains untested**, and still carries the most training
  mass of any option.
- **M5's `roles_v2.py` still hardcodes the marker protocol.** It is outside the
  M6/M7 arm path, so no live arm uses it, but it is a second copy of a format
  now known to be a variable.

---

## Addendum 2, 2026-09-23 — correction: Ollama did its job, qwen broke the
## contract

**Addendum 1's item 2 is wrong and is corrected here rather than edited out.**

It claimed: *"Ollama's parser is not uniformly reliable... The model complied;
the server-side extraction did not fire."* That reading survived because the
observable — a well-formed call sitting in `content` with `tool_calls` empty —
is consistent with both explanations, and only one of them was checked.

**Reading the template settles it.** `qwen2.5-coder`'s Ollama template renders:

```
For each function call, return a json object with function name and arguments
within <tool_call></tool_call> with NO other text.
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>
```

The wrapper is specified, in the prompt, by Ollama, in the model's own dialect.
The model emitted the JSON and omitted the wrapper. **The parser had nothing to
match.** Ollama rendered its half correctly; the model did not honour it.

### How far the non-compliance goes

Bare JSON, never wrapped, on every draw:

| variant | draws | wrapped |
|---|---|---|
| 7B q4, objective only | 3 | 0 |
| 7B q4, objective + this harness's PROTOCOL_TOOLS | 3 | 0 |
| 7B q4, bare objective, no role line | 3 | 0 |
| 7B q8 | 3 | 0 |
| 14B q4 | 3 | 0 |
| 3B q4 | 3 | 0 |

**18 of 18.** Not our prompt — it fails identically with no protocol text at
all. Not quantisation, and not size. It is a property of `qwen2.5-coder` as
packaged here.

### What actually renders and parses, all three models

Ollama 0.34.2. Render cost is prompt tokens for an identical one-word message
with and without the `tools` array — the difference IS the injected definition.

| model | family | render | parse | template demands wrapper |
|---|---|---|---|---|
| nemotron3-nano-4b | nemotron_h | +654 tok | **native** | no |
| nemotron-gpu (9B) | nemotron_h | +577 tok | **native** | no |
| qwen2.5-coder 7B | qwen2 | +313 tok | bare, recovered | **yes** |

Both Nemotrons go through Ollama's Go RENDERER/PARSER pair (`.Tools` absent from
their Go template); qwen goes through the legacy template path. All three
rendered. Two of three parsed.

### What this changes

**The correction runs in the opposite direction to the sheet's own thesis, and
that is why it is worth recording.** This sheet exists because a harness-side
format was being scored as a model property. Addendum 1 then scored a *model*
compliance failure as a *harness-side* one. Same error, mirrored — and it was
caught by reading the primary artifact, the template, rather than by a better
measurement.

The client's text recovery (`_calls_from_text`) stays, because the work is
correct and discarding it would lose a usable result. But it is now understood
as **compensating for a model that ignores its own tuned wrapper**, not for a
broken server. That distinction decides who to fix.

`tool_turns`, `tool_native` and `tool_recovered` are now recorded per row, so a
cross-model comparison over this protocol can state its recovery rate instead of
absorbing it. On present evidence qwen's rate is 100% and both Nemotrons' is 0%,
which is exactly the kind of systematic difference that would otherwise be read
as capability.

### Still standing from addendum 1

The multi-turn finding is unaffected and was directly observed: a call is a turn
boundary, and `conclude` does not arrive until a tool result has been appended.
So is the n=1 marker-vs-tools pair, which still earns nothing.

---

## Addendum 3, 2026-09-23 — all three models, and a renderer paired with the
## wrong model

Addendum 2 corrected one misattribution. Running the same probe across all
three subjects turned up a second, in the opposite direction again: a failure
that looked like the model was **ours**.

### `nemotron-gpu` runs a parser built for a different model

`nemotron-gpu` is **Nemotron Nano 9B v2**. Ollama pairs it with
`RENDERER nemotron-3-nano` and `PARSER nemotron-3-nano` — the pair for the
**4B Nemotron 3**. Different generation, different tool-call dialect.

Under that mismatch the 9B splits its own contract across two formats **in a
single turn**: `write_file` arrives as a real parsed tool call, and `conclude`
arrives as tags the parser does not recognise. Two shapes, captured verbatim:

```
<conclude>
<terminal_state>answered</terminal_state>
<summary>...</summary>
</conclude>
```

```
conclude
<parameter=terminal_state>
answered
</parameter>
```

The second also leaks `<|im_end|><|im_start|>assistant` into the content —
generation did not stop at the turn boundary, which is what a wrong template
looks like from outside.

**The obvious fix was tried and failed.** The hypothesis was that our raw-GGUF
import had lost the model's chat template. A tag was built from the bartowski
GGUF, which ships the real Jinja template with its own tool rendering.
Identical on every measure: same +577-token injection, same `.Tools` absent
from the Go template, same split. **Ollama assigns RENDERER/PARSER from the
architecture (`nemotron_h`), not from the source template**, so no Modelfile
can reach this. The tag was removed; `modelfiles/Modelfile.nemotron-gpu-v2`
is kept as the record of a ruled-out cause.

What was done instead: `_calls_from_xml` recovers both shapes, keyed to the
names actually offered so an XML-looking span in a file body cannot be mistaken
for a call. Recovery now runs **even when some calls parsed natively**, because
this model proves that a native call in a turn is not evidence the turn was
understood.

### All three, after the fix

| model | render | `write_file` | `conclude` | verdict |
|---|---|---|---|---|
| nemotron3-nano-4b | +654 tok | native | native | OK, native end to end |
| nemotron-gpu (9B) | +577 tok | native | native **or XML** | OK, variable |
| qwen2.5-coder 7B | +313 tok | recovered | recovered | OK, model ignores its wrapper |

Every one completes the contract. **None of the three does it the same way**,
and two of three need client-side recovery to do it at all.

The 9B is genuinely variable rather than consistently broken: across draws it
returned both calls natively, `write_file` native with `conclude` as XML, and
once nothing at all. That is why `tool_native` and `tool_recovered` are counted
per row and not per model.

### End to end through the real harness

`monolith`, `wf2_retry`, `min_predict 2048`, tools protocol, one rep each:

| model | subtests |
|---|---|
| nemotron3-nano-4b | 0/5 |
| nemotron-gpu (9B) | **5/5** |
| qwen2.5-coder 7B | 0/5 |

**n=1. These are not results.** The 4B returned 3/5 on this same task earlier
today and 0/5 here, which is the whole point: single draws on one task are
noise, and the table is here only to show the path runs on all three.

### What the three-model picture actually establishes

Not a ranking. **A methodological problem with the tools protocol itself.**

The marker protocol was uniform: every model got the same bytes and was parsed
by the same regex. The tool protocol is not. Each model gets a *different*
rendered prompt, costing a different number of tokens, and is read by a
*different* parser — one of which is paired with the wrong model. A
cross-model comparison over this protocol is comparing three different
pipelines, and the differences are systematic rather than noise.

That does not make it worse than the markers. It makes it **differently
biased**, and the bias is now measurable — `tool_native` against
`tool_recovered`, per row — where the marker protocol's bias was invisible.
Which was the original complaint.
