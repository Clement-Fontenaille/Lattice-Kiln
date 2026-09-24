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

---

## Addendum, 2026-09-24 — there are two degeneracy modes, and the protocol
## decides which channel absorbs it

The sheet above treats degeneracy as one phenomenon detected by one compression
threshold. Asked directly whether qwen really loops, the flagged outputs were
read rather than trusted, and they are not the same failure.

Classified by whether the repeated span is copied from the prompt (a 60-char
sliding window, >50% of the output matching the prompt) and by which channel
carries it:

| model / protocol | mode | share |
|---|---|---|
| qwen2.5-coder / markers | **echoes the PROMPT**, in output | 107/141 = 76% |
| nemotron3-nano-4b / markers | repeats **its own** output text | 103/130 = 79% |
| nemotron3-nano-4b / tools | repeats **its own reasoning**, in thinking | **17/17 = 100%** |

Qwen's characteristic failure is copying the input back instead of generating.
A sample, repeating to the cap:

```
```python
# OBJECTIVE
Modify the `staff_price` function to use the shared helper.
OUTPUT FORMAT - follow it exactly.
For every file you create or change, emit one block (give the WHOLE new file...)
```python
# OBJECTIVE
Modify the `staff_price` function to use the shared helper.
...
```

That is not deliberation failing to terminate. It is the model failing to leave
the prompt. qwen2.5-coder has no thinking channel at all, so output is the only
place it can degenerate.

### The sharper claim

**The protocol does not change whether degeneration happens. It changes which
channel absorbs it.** The same 4B degenerates in its OUTPUT under markers and
in its THINKING under tools, 17 of 17. Under the tool protocol the output is a
structured call, so the only free-text channel left is the reasoning trace, and
that is where the loop goes.

This matters for anything that reads only one channel. A harness watching
`content` sees a clean tool call and a healthy-looking response while the model
burns its entire budget looping out of sight — which is precisely what happened
here, and why the failure was read for a day as "cannot stop thinking" rather
than as the same degeneration already recorded in `/15`.

### What it costs the earlier table

The task×model table above pools both modes. It is still a true statement about
where degeneration occurs, but "susceptibility" is now two questions: which
tasks make a model echo its prompt, and which make it circle its own text.
Those may have different causes and the table cannot separate them.

---

## Addendum 2, 2026-09-24 — SETTLED: it is the temperature, and the corpus was
## gathered at the wrong one

The sheet above names temperature as the leading suspect and says the cause is
not established. It is now.

Same verbatim prompt, same cap, no nudge, only the sampler moving. The prompt
is the SECOND implementer call — the retry, after the judge has rejected the
work — because that is where 13 of 15 pipeline truncations happen. Every value,
sorted, n=20:

```
t0.2 (as shipped)      cap  9/20   1058 1115 1751 1807 2148 2782 2953 3605 4145
                                   6151 6387 | 8192x9
t0.6 p0.95 (NVIDIA)    cap  2/20   884 1008 1078 1124 1126 1306 1320 1616 1639
                                   1666 1713 1894 1993 2181 3114 3575 4195 5326
                                   | 8192x2
t1.0 p1.0 (Modelfile)  cap  0/20   1469 1559 1578 1725 1731 1804 1839 1881 2024
                                   2061 2174 2258 2303 2903 2980 3037 3329 3499
                                   5053 6837
t0.2 + rep_pen 1.3     cap  7/18   2795 5431 5639 5902 6206 6677 6742 6886 7356
                                   7404 7935 | 8192x7
```

**45% → 10% → 0%.** At the temperature the model actually ships with, it does
not loop at all in twenty attempts.

The probe is calibrated: `t0.2` gives 9/20 against the pipeline's 8/26, the
same regime. An earlier version of this probe used the FIRST implementer call
and saw 0/20 — it could not reproduce the failure, and only the calibration arm
revealed that. A probe without one would have reported "temperature makes no
difference".

### repeat_penalty is refuted twice

7/18 on the failing prompt, and on a prompt where every other arm capped 0/20 it
capped 6/18. Its convergent calls also start at 2795 where every other arm
starts near 1000. **A repetition penalty does not stop a loop, it stops
TERMINATION** — ending a generation re-uses tokens the penalty is suppressing.
The obvious remedy for a repetition loop makes it worse, in both directions.

### What this costs the existing corpus

Every row was gathered at temperature 0.2 with reasoning ON, which is NVIDIA's
reasoning-OFF pairing and five times below the model's own Modelfile default.
On retry-shaped calls that is a **45% collapse rate**.

So `50-findings/12` and `/14`, and every arm score in the store, are measured
under a sampling regime that manufactures failures — unevenly, because the
task×model table above shows the collapse lands on different items for
different models. That is not a correction to apply afterwards. It is a reason
to re-gather, and it should be settled before the H100 sweep rather than
inherited by it.

### What it does to the nudge programme

The nudges were treating a symptom, and that is now measured rather than
suspected. Their separate value stands and is unaffected: on convergent calls
`answer_first` cut implementer decode ~13%, which is a real efficiency lever
whatever causes the loops. But it was never going to fix this, and the marginal
p=0.046 fought over earlier is a nudge slightly perturbing the odds of falling
into a sampling artifact.

### Still open

Only the 4B, only one task's retry prompt, only Ollama. Whether 0.6 or 1.0 is
the right setting is not answered here either: 1.0 never looped but ran longer
(median ~2120 against 0.6's ~1690), so the cheaper and the safer setting are
not the same one.
