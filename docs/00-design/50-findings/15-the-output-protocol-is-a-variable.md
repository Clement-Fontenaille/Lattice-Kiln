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
