# 16 — The runaway is a decoding loop, and which tasks trigger it is a property of the model

**Subject:** `nemotron3-nano-4b`, `qwen2.5-coder:7b`, `nemotron-gpu` (9B v2)
**Recorded:** 2026-09-24
**Artifacts:** `evalkit_store/transcripts/` (637 long outputs),
`probe_implementer_tail.py`, `probe_temperature_tail.py`
**Verdict:** the mechanism is established; the cause is not yet.

## What was called "a model that will not stop thinking"

A `judge_anchored` run truncated at 8192 tokens having produced 25,141
characters of reasoning and no answer. That was read three times over the
course of a day as the model being unable to terminate.

It is not. Read out of the transcript, the first ~700 characters are coherent
work on the retry semantics; the model reaches a real ambiguity about what
`self.calls` should count, and then emits the same ~150-character block
verbatim until the cap:

> So they want 2? That's retries? So they want retries? That's 2. So they got
> 1, which is retries-1. So maybe they think calls = retries-1? ...

**Degenerate repetition. A decoding failure, not deliberation.**

## The distribution is bimodal, which the quantiles hid

Per-call `eval_count` on the implementer stage, every value, sorted:

```
control       462 500 512 753 820 843 872 1026 1035 1046 1078 1243 1736 1956
              2013 2084 2147 | 4285 | 8192x8
first_pass    516 588 619 679x2 707 777 938 1085 1169 1269 1318 1375 1654 1764
              1810 | 4856 | 8192x4
answer_first  330 389 401 465 486 525 659 720 727 770 812 813 820 823 913 1140
              1240 1308 1324 1475 1536 1625 2486 3103 | 4460 | 8192x3
```

Nothing finishes between roughly 4900 and the cap. A call either converges
under ~3000 tokens or enters the loop and never returns. **There is no tail to
shorten** — the earlier account, "the nudge shortens the tail", was wrong about
the shape. What a nudge changes is the probability of entering the mode.

A quantile table cannot show this and a median cannot detect it. The medians
across those three arms differ by 14%.

## Only one stage fails

Per-call `eval_count`, by pipeline stage, capped calls counted:

| stage | control | first_pass | answer_first |
|---|---|---|---|
| audit | 0/10 | 0/10 | 0/10 |
| **implementer** | **8/26** | **4/21** | **3/28** |
| impl tool-turn | 0/19 | 1/17 | 1/17 |
| judge | **0/17** | **0/20** | **0/30** |

The judge never truncated: 67 calls, three arms, nothing above 582 tokens.
`judge_anchored` names the arm, not the stage that fails.

**This invalidates an earlier probe rather than merely improving on it.**
`probe_think_nudge` tested six nudges against the JUDGE prompt — a stage with
no failure mode. Its non-replication was attributed to noise; at least part of
it was measuring the wrong stage.

## Susceptibility is a task×model interaction

Degeneracy detected by compression ratio (`zlib` under 0.12) over every stored
output of 3000+ characters. The distribution is bimodal — p25 0.070, p75 0.352 —
so the threshold sits in a gap rather than on a slope, and samples either side
were checked by eye.

Conditioned on model and protocol, so this is not a mix of configurations:

```
qwen2.5-coder / markers            nemotron3-nano-4b / markers
  wf3_refactor      30/30 100%       hf_wrong_spec     27/27 100%
  wf1_crossfile     13/13 100%       hf_suppress        5/6   83%
  hf_already_optimal 5/6   83%       hf_retry_backoff  33/40  82%
  wf6_multi        54/164  33%       hf_cache_decorator 19/24 79%
  hf_retry_backoff   0/11   0%       wf6_multi          1/18   6%
  hf_extract_fn      0/19   0%       wf2_retry          0/5    0%
  hf_rename          0/9    0%       hf_rename          0/6    0%
```

**The susceptible set differs by model.** `hf_retry_backoff` is 0/11 for qwen
and 33/40 for the 4B. `wf6_multi` is 33% for qwen and 6% for the 4B. They do
not loop on the same items.

Shared floor: `hf_rename`, `hf_extract_fn` and `hf_merge_config` never loop for
either model. Those are the mechanical, single-answer refactors.

Two labels that do NOT predict it, both checked rather than assumed:
`decline_expected` is False for every task in the table, and `trap` type does
not separate — `behaviour-preserving` appears at 94%, 83%, 71%, 56%, 38%, 0%
and 0%.

## Why this matters to every cross-model number in the programme

> A per-task score difference between two models is partly a difference in
> which items trigger each model's decode pathology. That is not capability,
> and it does not average out — it is systematic per item.

`50-findings/12` and `/14` compare models per task. This is a contamination of
the same kind as the output protocol in `/15`, arriving through the sampler
rather than through the prompt.

## The leading suspect, and it is ours

Every arm hardcodes `temperature 0.2` while reasoning is ON — `LATTICE_THINK`
is unset, so no `think` key is sent and the model's own default applies.

NVIDIA pair **0.2 with reasoning OFF** and **0.6 or higher with reasoning ON**.
The model's own Modelfile ships `temperature 1, top_p 1`. So the corpus was
gathered five times below the value the model was packaged with, in the pairing
the vendor warns against.

`50-findings/15` already recorded the same monotone pattern and did not connect
it: *"temperature 0.0 degenerated 5 times out of 5, 0.2 four times, 0.6
twice."* That was newlines collapsing into spaces; this is a sentence
repeating. **Same family, read as two unrelated findings.**

## What would settle it

`probe_temperature_tail.py` holds the prompt, the cap and the nudge fixed and
moves only the sampler: 0.2 as shipped, 0.6/0.95 per NVIDIA, 1.0/1.0 per the
Modelfile, and **0.2 with `repeat_penalty` 1.3**. The last arm is the one that
matters for the explanation rather than the cure: "low temperature causes
loops" and "loops are merely unpenalised" predict the same remedy from raising
temperature, and different results from penalising repetition at 0.2.

If the cap rate collapses at 0.6, the nudge programme was treating a symptom —
and, separately, the whole corpus was gathered under a sampling
misconfiguration.

## What this does not establish

The mechanism is verbatim repetition and that is directly observed. The CAUSE
is not: temperature is a hypothesis supported by one prior observation and the
vendor's own guidance, nothing more.

The task×model table is conditioned on model and protocol but not on
`num_predict`, and it conditions on outputs already 3000+ characters long — so
it reports *given the model generated a lot, was it degenerate*, rather than an
unconditional rate. A task whose answers are always short cannot appear in it.
