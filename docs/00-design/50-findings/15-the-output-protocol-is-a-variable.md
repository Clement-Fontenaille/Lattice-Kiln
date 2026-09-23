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

## Why it plausibly happens

Inside a fenced block the model is on distribution: it has seen an enormous
number of them, and the newline structure of code inside a fence is
overdetermined. Inside `<<<FILE path=...>>>` it is in a region it has never
seen, and what collapses first is exactly the structure the fence would have
supplied.

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
3. **A third format** — the model's native tool-calling interface, which it
   advertises as a capability and which is the closest thing it has to a
   trained structured-output channel.

Until then the protocol stays as it is, because changing it mid-programme would
put every existing row in a different regime from every new one — and unlike
sampling, the protocol is **not** in the setup key, so that change would be
invisible in the data.

**That last point is a defect in its own right.** `arm_sha` and `prompt_sha`
capture the arm's source and its prompts, so a protocol change inside an arm
would move them — but the protocol is shared boilerplate across arms, and
nothing records it as the variable it has now been shown to be.
