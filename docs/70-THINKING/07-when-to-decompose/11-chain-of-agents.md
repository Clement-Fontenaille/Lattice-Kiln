# Chain of Agents: Large Language Models Collaborating on Long-Context Tasks

## Density

**Density: HIGH** — a short, tightly-argued paper in which nearly every section is load-bearing, and the load it bears is exactly the Subject's core question: a concrete splitting rule, a concrete recombination step, an ablation isolating the recombiner, and a head-to-head against two alternative decomposition topologies.

**Keywords (mine):** sequential worker chain; fixed-size input segmentation; running-state message passing; dedicated recombiner agent; bounded per-agent context; topology ablation (chain vs. tree vs. vote); reading-order sensitivity; long-context decomposition.

**Year:** 2024 (arXiv v1, 4 June 2024).
**Venue:** NeurIPS 2024 (Advances in Neural Information Processing Systems 37). Read here from the arXiv v1 HTML rendering (`arxiv.org/html/2406.02818`); the camera-ready may differ in minor detail.

**Authors:** Yusen Zhang (Penn State, work done as a student researcher at Google Cloud AI Research), Ruoxi Sun, Yanfei Chen, Tomas Pfister (Google Cloud AI Research), Rui Zhang (Penn State), Sercan Ö. Arık (Google Cloud AI Research; last author).

## Approach

Chain-of-Agents (CoA) is a training-free, prompt-only framework for long-context tasks. A sample is
`(x, y, q)`: input `x` of `n` tokens, output `y` of `m` tokens, optional query `q`. The backbone LLM
has a context window `k`, with `k ≪ n` assumed. Two stages.

**Stage 1 — worker chain.** `x` is split into `l` chunks `{c_1 … c_l}`, each short enough to fit in
`k`. One worker agent `W_i` per chunk. Workers run *sequentially*, and each one's input is the
concatenation of four things: a fixed worker instruction `I_W`, the message from the previous worker
(the "communication unit" `CU_{i-1}`), its own chunk `c_i`, and the query `q`. It emits `CU_i` for
the next worker:

    CU_i = LLM_{W_i}(I_W, CU_{i-1}, c_i, q)

**Stage 2 — manager.** A separate agent sees only the *last* communication unit plus a manager
instruction and the query, and produces the answer:

    Response = LLM_M(I_M, CU_l, q)

### How the input is segmented (Subject-relevant)

Segmentation is **positional and content-blind**: fixed-size contiguous chunks in source order, sized
to the agent window. There is no planner, no semantic boundary detection, no query-conditioned
selection of what to split off. Depth is not chosen — the *number* of agents is `⌈n/k⌉`, a pure
function of input length over window size, so it varies per sample (Table 3: 1.12 agents on average
for Qasper, 18.63 for BookSum). The decomposition is over *the input*, not over the *task*: every
worker gets the same instruction and the same query, and does the same kind of work. This is a flat
chain, depth 1, no recursion, no sub-agents spawning sub-agents.

### What each worker passes to the next (Subject-relevant)

Natural language only, and only to its immediate successor. The `CU` is not a fixed schema; its
content is task-shaped by the prompt (Appendix B, Tables 9–10): for QA it holds evidence for
answering `q`; for summarization, a running summary of everything read so far; for code completion, a
code summary with function/class names and explanations. The worker prompt literally asks the model
to "read current source text and summary of previous source text (if any) and generate a summary to
include them both" — so `CU_i` is a *rewritten running state*, not an append-only log. Each worker is
free to compress, keep, drop, or reorder what its predecessor wrote. The paper's own Figure 1 walkthrough
treats this as a feature: `W_3`, finding nothing relevant in its chunk, "directly rewrites `CU_2`" and
promotes the answer to the first token of `CU_3`.

The chain is what gives the framework its claimed "full receptive field": the last worker has, in
principle, seen a compressed trace of the entire input regardless of `n`, while no single agent ever
holds more than `k` tokens. The paper explicitly contrasts this with input reduction's
"read-then-process" and calls CoA "interleaved read-process."

### How the manager recombines (Subject-relevant)

Minimally, and this is the paper's most pointed design choice. The manager does **not** see all the
`CU_i`, and does not see any raw chunk. It sees exactly one artifact — `CU_l`, the final worker's
state — plus the instruction and query. Recombination is therefore *incremental and distributed along
the chain*, performed by the workers themselves as they rewrite state; the manager is a
read-out/answer-formatting step over an already-aggregated summary, not an aggregator over parallel
partial results.

The authors defend this against the obvious alternatives in a footnote to §3.2, and they are
alternatives worth recording: (i) letting the last worker `W_l` emit the final answer directly "leads
to a performance drop" (quantified later in the Table 7 ablation); (ii) feeding the manager *all*
`CU_i`, or the subset of `CU`s that workers flagged as answer-relevant, "also hurts the performance
because of confusion led by conflicting `CU_i`." So the paper's position is that giving the recombiner
more material actively makes it worse — the bottleneck through a single `CU_l` is load-bearing, not
an economy measure.

**Algorithm 1** is the whole method: split, loop `CU_i ← LLM_{W_i}(I_W, CU_{i-1}, c_i, q)`, return
`LLM_M(I_M, CU_l, q)`. Same backbone model for every `W_i` and for `M` unless stated otherwise,
though the framework permits heterogeneous models.

## Models targeted

Six LLMs, all served through Google Vertex model garden:

- **PaLM 2**: `text-bison@001`, `text-unicorn@001` — 8k window. These set the default: CoA's standard
  configuration is 8k because that is what bison/unicorn allow.
- **Gemini 1.0**: `gemini-ultra` — 32k window.
- **Claude 3**: `claude-3-haiku`, `claude-3-sonnet`, `claude-3-opus` — 200k window, used as the
  "long context model" (LCM) comparison arm.

No open-weights models, no GPT-4. Max generation 2048 tokens for gemini-ultra, 1024 for the rest;
temperature 0 everywhere except the self-consistency multi-path setting.

## Benchmarks / datasets

Nine datasets across three task families, drawn from LongBench and SCROLLS, with average input length
and average agent count (at 8k) in parentheses:

- **QA (5):** HotpotQA (10.6k words, 2.35 agents), MuSiQue (13.0k, 2.88), NarrativeQA (71.8k, 12.45),
  Qasper (4.2k, 1.12), QuALITY (4.9k, 1.31). HotpotQA and MuSiQue are multi-hop; MuSiQue is the harder
  of the two (more hops, unanswerable questions, harder distractors).
- **Summarization (3):** QMSum (12.5k, 2.57, query-based), GovReport (9.2k, 2.03, *no* query — a
  pseudo-query is synthesized for RAG only), BookSum book-level (108.5k, 18.63, no query).
- **Code (1):** RepoBench-P (7.1k, 1.69) — next-line completion given a repository context.

Metrics: geometric mean of ROUGE for summarization, code similarity score for RepoBench-P, exact match
for QuALITY, F1 for the remaining QA sets — i.e. the metric conventions of the source benchmarks.

Note for later: three of the nine datasets average **fewer than two agents**, so on Qasper, QuALITY
and RepoBench-P a large share of samples are single-worker cases where "the chain" barely exists.

## Author incentive

Five of six authors are Google Cloud AI Research; the first author was a Google student researcher at
the time; the last author (Arık) is Google. No external funding is declared and no ethics/funding
statement appears in the arXiv v1 text. The direct stakes are visible and worth naming: the framework
is evaluated on Google-served models via Google's own Vertex API, and its headline claim is that a
prompt-only orchestration over **small-window** models beats a **200k-window competitor model**
(Claude 3) — a claim that is favourable to a cloud provider selling orchestration and cheap
small-window inference, and unfavourable to the "just buy a bigger window" purchase. It also cuts
against Google's own long-context positioning at the time, so the incentive is not simply
one-directional. The Broader Impacts appendix notes the framework "will greatly increase the
efficiency of individuals or companies," which reads as product framing. There is no released code
link in the v1 text.

## Measurement methodology (brushed)

- **Dependent variable:** per-dataset benchmark score (F1 / EM / ROUGE-geomean / code similarity). No
  aggregate score, no human evaluation, no LLM-judge scoring of final answers (the LLM judge appears
  only *inside* the multi-path variant as a selection mechanism, not as a metric).
- **What is controlled:** the window size `k` is the central controlled variable and the whole rhetorical
  device. Comparisons are labelled with an explicit budget — CoA (8k) vs. Vanilla (8k) vs. RAG (8k) vs.
  Vanilla (32k) vs. Vanilla (200k) — so the strong claim is "CoA at 8k beats Vanilla at 200k on the
  same backbone." Backbone model is held fixed within each comparison row. Prompts follow LongBench and
  SCROLLS task-specific requirements. Temperature 0 makes single-path runs deterministic.
- **What is not controlled:** token cost and wall-clock latency are *not* held constant across arms and
  are not measured at all (see below). The RAG arm uses a specific retriever (C-Pack/BGE) with 300-word
  chunks and top-n filling of the window; no retriever sweep. The chunking granularity for CoA is not
  varied except in Appendix D's window-size sweep.
- **N:** the full evaluation-set sizes of the nine benchmarks are never stated. The lost-in-the-middle
  replication uses an explicit N = 500 randomly selected samples. The Claude 3 tables split samples
  into "No Trun." / "Trun." bins by whether the source exceeds 200k tokens, but do not give bin counts;
  the NarrativeQA RAG-position analysis reports per-bin sample *ratios* in Figure 3 but not counts.
- **Significance:** effectively untreated. The word "significant"/"significantly" is used throughout in
  the informal sense. There are no confidence intervals, no error bars, no seeds, no repeated runs, and
  no statistical tests anywhere in the paper. The single exception is §5.3, which reports a performance
  *range* with a ± figure (Vanilla 6.13 ±2.17 vs. CoA 4.89 ±1.91) — and that is a spread across gold-answer
  positions, not a sampling error bar. Every headline number is a single deterministic run.

## Key findings

**1. CoA (8k) beats both Vanilla (8k) and RAG (8k) on all eight main-table datasets, on all three
backbones.** Largest reported per-model gains: +13.30 on NarrativeQA (text-bison), +12.82 on MuSiQue
(text-unicorn), +22.00 on QuALITY (gemini-ultra). Representative absolute numbers (text-bison,
Vanilla / RAG / CoA): NarrativeQA 11.96 / 14.20 / 25.26; Qasper 26.56 / 27.20 / 37.17; GovReport
20.60 / 20.83 / 26.11. For gemini-ultra, Vanilla (32k) improves on Vanilla (8k) but still loses to
CoA (8k).

**2. Bounded per-agent context beats a 200k window on the same backbone.** Table 5, Claude 3, average
scores. NarrativeQA — Vanilla (200k) 7.17 / 5.15 / 6.56 for haiku / sonnet / opus, vs. CoA (8k) 18.80 /
16.51 / 23.96. BookSum — Vanilla (200k) 12.04 / 12.10 / 14.00, vs. CoA (8k) 13.70 / 14.96 / 17.47.
Crucially the gain holds on the "No Trun." subset, where the whole source *did* fit in the 200k window,
so this is not merely CoA seeing text the baseline had truncated away. The margin over Vanilla (200k)
grows with model strength (NarrativeQA: 11.63 / 11.36 / 17.4 haiku to opus), which the authors read as
CoA benefiting from stronger backbones.

**3. Gains grow with input length.** Section 5.2 / Figure 2, Claude 3 on BookSum: CoA's own score
*increases* with source length, and the improvement over Vanilla (200k) reaches "around 100%" beyond
400k tokens.

**4. Chain > tree > vote: the topology comparison.** This is the paper's most direct evidence on
decomposition structure (Table 6, text-bison 8k). Against Vanilla (8k) as the reference:

| | HotpotQA | MuSiQue | NarrativeQA | Qasper | QuALITY | QMSum | GovReport | RepoBench-P |
|---|---|---|---|---|---|---|---|---|
| Vanilla (8k) | 45.57 | 26.87 | 11.96 | 26.56 | 61.86 | 15.45 | 20.60 | 56.30 |
| Merge (8k) | 42.96 | 26.66 | 11.27 | 26.78 | 59.30 | 9.42 | 25.38 | 33.66 |
| Hierarchical (8k) | 50.62 | 29.40 | 17.04 | 31.39 | 64.20 | 15.19 | 16.54 | 27.96 |
| CoA (8k) | **53.62** | **37.09** | **25.26** | **37.17** | **65.42** | **16.77** | **26.11** | **58.25** |

*Merge* = each worker answers its own chunk independently, majority vote over answers. *Hierarchical* =
each worker judges whether its chunk is useful and if so emits a CU; all surviving CU_i go to the
manager (a tree, modelled on Chen et al.'s memory-maze work). CoA wins on all eight. The two parallel
designs are not merely worse than CoA — both fall *below the single-agent Vanilla baseline* on several
datasets, catastrophically so on RepoBench-P (Merge 33.66, Hierarchical 27.96, vs. 56.30 for doing
nothing). The authors' reading: parallel workers cannot communicate, so each is confined to its own
chunk, "which blocks the understanding of the whole text."

**5. The manager is load-bearing.** Table 7 ablation, "w/o Manager" (last worker emits the answer
directly): drops on every dataset, e.g. MuSiQue 37.09 to 26.79, Qasper 37.17 to 29.66, HotpotQA
53.62 to 48.58. The recombination step is worth roughly 5–10 points even though it sees strictly less
information than the worker it replaces.

**6. Reading order matters, but not overwhelmingly, and not always in CoA's favour.** Right-to-Left
is worse than left-to-right across the board (e.g. MuSiQue 29.77 vs 37.09). Random Permutation is
close to left-to-right and actually *beats* it on HotpotQA (56.05 vs 53.62), Qasper (37.42 vs 37.17)
and RepoBench-P (58.43 vs 58.25). The authors claim left-to-right is best "on most of the datasets,"
which is fair but weaker than the framing suggests.

**7. Multi-path ensembling helps, and the oracle gap is large.** Section 5.6 runs several chains in
different orders and selects among them by majority vote or an LLM judge. 5-way Permutation with judge
gives the best realized gains (HotpotQA 59.17, MuSiQue 42.37). But the *oracle* (pick the best-scoring
path post hoc) is far higher — HotpotQA 75.73, MuSiQue 60.16, QuALITY 79.80 — a 15–20 point headroom
over any realizable selector. Voting is notably brittle on long-generation tasks (QMSum 8.31,
RepoBench-P 35.44 with vote, vs. 17.81 / 52.45 with judge).

**8. CoA's advantage concentrates where RAG fails.** Section 5.1 bins NarrativeQA samples by the rank
of the chunk containing the gold answer. RAG degrades as the gold chunk falls further down the
re-ranking; CoA's gain over RAG is largest exactly in those bins. The authors read this as CoA being
insensitive to retrieval quality because it reads everything.

**9. CoA reduces, but does not eliminate, lost-in-the-middle.** Section 5.3, N=500 from the Liu et al.
setup: Vanilla's score varies by 6.13 (+/-2.17) across gold-document positions, CoA's by 4.89 (+/-1.91).

**10. Robustness to agent window size.** Appendix D, Claude 3 Haiku on NarrativeQA at
4k/8k/16k/32k/64k/128k: performance rises from 4k to 16k, then plateaus around 20. Chunk size is not a
knife-edge hyperparameter above ~16k.

### Coordination and communication cost — what is and isn't measured

The paper addresses cost **only analytically, and only for attention FLOPs**. Section 3.3 and Appendix A
give a decoder-only operation count: Full-Context encoding is `O(n^2)` (summing `1+2+...+n`), while CoA
encodes `ceil(n/k)` chunks of `k` tokens for `O(k^2 * n/k) = O(nk)`; decoding is `O(nr)` for both. Since
`k << n`, CoA is presented as *cheaper* than Full-Context, and the paper calls itself "cost-effective"
on that basis.

What that accounting omits is the whole of the coordination cost the Subject is asking about. It does
not count the `l` separate API round-trips, the `l` copies of the worker instruction, the query re-sent
to every worker, or — most significantly — the CU tokens, which are *generated* by every worker and
then *re-encoded* by the next, so the communication payload is paid twice per hop. Decode cost is
treated as identical to Full-Context (`O(nr)`), which quietly concedes that CoA generates `ceil(n/k)`
responses where Full-Context generates one; the asymptotics absorb this but the constant is the entire
practical coordination overhead. There are **no measured** numbers anywhere in the paper for tokens
consumed, dollar cost, wall-clock latency, or API calls per sample — and CoA is strictly sequential, so
its latency cannot be parallelized away the way Merge's or Hierarchical's could. The authors do
acknowledge this obliquely: the Limitations name "cost and latency" as a target for future reduction
via model routing, and Broader Impacts concedes the framework "may increase the number of the calls for
API, causing higher network traffic and higher latency for user pools." So the coordination cost is
admitted in prose and excluded from every table.

### Error propagation — how it is handled and discussed

Not measured, not named as a risk, and structurally central. The chain is a single point-to-point path
with no redundancy: `W_i` sees only `CU_{i-1}`, never `CU_{i-2}` or any raw earlier chunk, and the
manager sees only `CU_l`. Any fact a worker drops, garbles, or hallucinates is unrecoverable
downstream — nothing later in the pipeline can go back to the source. The design deliberately *doubles
down* on this: the Section 3.2 footnote reports that giving the manager all CU_i (which would provide
exactly the redundancy that could catch a mid-chain error) *hurts* performance through "confusion led
by conflicting CU_i." The paper reads conflicting evidence as noise to be avoided rather than as signal
about where the chain broke.

The nearest thing to error-propagation evidence is indirect and lives in Section 5.6: the fact that
different reading orders produce genuinely different answers, and that an oracle over five permutations
gains 15–20 points, is a direct measure of chain fragility — the same content, reordered, propagates
differently and often better. The paper frames this positively as ensembling headroom rather than as
variance from error accumulation. The Appendix C examples show the benign version of the mechanism: on
HotpotQA, CU_1 to CU_2 to CU_3 accretes detail and the answer emerges; on RepoBench-P, Worker 1's CU
contains a verbatim duplicated paragraph and Worker 2 silently cleans it — an unremarked instance of a
worker repairing its predecessor's output. Nowhere does the paper report a failure trace, an error rate
per hop, a study of how degradation scales with chain length (which would be the natural experiment
given BookSum averages 18.63 workers), or any mechanism for a worker to flag low confidence.

### The authors' own reading

They present CoA as simultaneously training-free, task-agnostic, length-agnostic, interpretable and
cost-effective, and attribute its performance to two things working together: **full receptive field**
(unlike input reduction, no part of the source is unseen) and **short per-agent context** (unlike
window extension, no agent has to focus inside a huge prompt). Their framing of the multi-agent
comparison is that *communication* is the active ingredient — the chain beats the tree and the vote
specifically because sibling workers can pass state. They read the multi-hop case study (Section 5.4,
Figure 5) as showing something RAG structurally cannot do: the first-hop evidence often has low
semantic similarity to the query, so a retriever never surfaces it, whereas a chain that reads
everything in order picks it up before it knows why it matters.

## Open questions the paper itself raises

Stated in the Conclusion's Limitations paragraph, plus a few raised in passing elsewhere. In the
authors' own framing:

1. **Communication is not optimized for machines.** "Communication effectiveness can be further
   improved via finetuning or in-context learning because current LLMs are aligned with human norms
   which is not optimal for communication between LLMs." The CU format is prose written the way a human
   would summarize; the authors suspect that is the wrong protocol for agent-to-agent transfer.
2. **Only one communication topology is explored.** "CoA does not explore other forms of communication
   approaches, such as debating or complex discussions." The chain is asserted, and compared against a
   tree and a vote, but not against interactive or bidirectional protocols.
3. **Cost and latency are unreduced.** "The cost and latency of running CoA can be further reduced,
   such as replacing some LLMs with more effective models via model routing." Note this frames cost as
   a thing to be reduced later, not a thing measured now.
4. **Multi-path selection is unsolved (Section 5.6).** "There is large space to improve because oracle
   is much higher than either w/ judge or w/ vote," and they explicitly "leave the direction of
   multi-path reasoning to future study."
5. **Prompt portability (Appendix E).** "Similar to all prompt based approaches, this framework requires
   careful prompt design for unseen large language models; users may not get optimal solution on certain
   newly proposed LLMs."

## Appreciation

Separating what transfers as an argument from what is a number valid only inside this setup.

### MECHANISM — the parts that transfer

- **Bounded per-agent context can beat unbounded context on the same model.** This is the paper's real
  contribution and it is cleanly demonstrated on the "No Trun." subset, where the baseline had the whole
  document inside its 200k window and still lost to a chain of 8k agents. That controls away the obvious
  confound (CoA seeing more text) and leaves a genuine claim: decomposition can buy *attention quality*,
  not just *coverage*. This is the strongest single argument in the paper and it does not depend on the
  particular models.
- **Sequential state-passing dominates parallel-independent partitioning when sub-results are
  interdependent.** Table 6 is a real controlled comparison — same chunks, same instructions, same
  backbone, only the topology differs — and both parallel designs lose, often below the do-nothing
  baseline. The mechanism the authors name for this is sound and generalizes: if the sub-tasks are not
  actually independent (multi-hop reasoning, narrative continuity, cross-file code), partitioning
  without communication destroys precisely the dependency the task needs. The paper's Figure 5 case
  study articulates the sharpest version: first-hop evidence has low similarity to the query, so it is
  invisible to any selection-based decomposition, and only sequential reading recovers it.
- **A separate recombiner beats letting the last executor answer.** The w/o-Manager ablation is a small,
  clean, general result about role separation: the agent that has been maintaining state is worse at
  producing the final artifact than a fresh agent given that state. That transfers to any pipeline
  design.
- **Narrowing the recombiner's input can help.** The claim that feeding the manager all CU_i *hurts*,
  through conflict between them, is a genuinely counterintuitive and useful mechanism claim — but see
  below, because it is the least-evidenced assertion in the paper.
- **Decomposition depth as a function of input size, not of task structure.** CoA's `ceil(n/k)` rule is
  worth naming as a design point precisely because it is so mechanical: no planner, no judgment call, no
  runtime depth decision. It shows that a useful decomposition need not involve any planning at all when
  the split axis is the input rather than the task.

### MAGNITUDE — numbers valid only inside this setup

- **"Up to 10%" / the specific deltas.** All of the headline gains are single deterministic runs on
  2024-era models (PaLM 2 bison/unicorn, Gemini 1.0, Claude 3), with no seeds, no repeats, no error
  bars, no significance testing, and unstated evaluation-set sizes. The direction of the effect is
  credible because it is consistent across nine datasets and six models; the size of it is not
  portable.
- **The "8k beats 200k" margins specifically.** These are largest on NarrativeQA, where the Vanilla
  (200k) scores are startlingly low in absolute terms (5.15–7.17 F1 for Claude 3 Opus/Sonnet on a QA
  set). Scores that low suggest the baseline prompt was doing badly for reasons beyond context focus —
  possibly formatting or answer-length mismatch against the F1 metric — and CoA's manager stage,
  which produces a short direct answer, may be partly winning on output *form* rather than on
  comprehension. The paper never inspects baseline failure modes, so the margin is not decomposable.
- **The 2x improvement past 400k tokens.** Read off a figure, on one dataset, one model family.
- **The lost-in-the-middle mitigation (6.13 to 4.89 range).** N=500, one setup, and the improvement is
  modest and reported as a spread rather than with an uncertainty estimate. The direction is plausible
  and mechanistically motivated; the magnitude is one data point.
- **The reading-order result.** Left-to-right wins on most datasets but loses to random permutation on
  three of seven, on differences of 0.2–2.4 points that are well inside plausible run-to-run noise for
  an unrepeated experiment. I would not carry "natural reading order is best" forward as established.
- **The footnote claim about conflicting CU_i.** This is the paper's most interesting mechanism claim
  and it appears *only in a footnote*, with no table, no numbers, and no example of a conflict. Given
  the manager-input design turns on it, it is under-evidenced relative to its load.

### Things I would flag as weaknesses on the paper's own terms

- Three of nine datasets average under two agents. On Qasper (1.12), QuALITY (1.31) and RepoBench-P
  (1.69), most samples involve one or two workers, so CoA there is closer to "summarize then answer"
  than to a chain — yet Qasper shows one of the largest gains (26.56 to 37.17). That suggests a
  meaningful share of CoA's benefit comes from the *summarize-then-answer two-stage prompt*, not from
  multi-agent chaining at all. The paper never runs the obvious control: a single agent that summarizes
  its own (fitting) input and then answers from the summary.
- Chain length is never treated as an independent variable. With BookSum at 18.63 agents and Qasper at
  1.12 in the same table, the paper had the material to plot performance against chain depth and did
  not.
- No cost table, as detailed above.
- No code release in v1.

## How it could serve a harness-design effort — limitations and major concerns

Stemming the discussion rather than resolving it.

**What it offers a harness designer.** A concrete, minimal, and empirically defended template for one
whole family of decomposition: *input-partitioned, sequentially-chained, single-recombiner*. Three of
its design decisions are directly actionable as defaults worth testing: (a) split on the input when the
input is what exceeds the budget, and let depth fall out of `ceil(n/k)` rather than asking a planner;
(b) give sub-agents a channel to their predecessor's state rather than isolating them, whenever the
sub-tasks might be interdependent; (c) separate the agent that accumulates state from the agent that
produces the final artifact. The Table 6 result is a genuine warning against the naive default —
fan-out to independent workers and merge — which loses to *doing nothing at all* on several tasks here.
Appendix D's plateau is also practically useful: chunk size is forgiving above ~16k, so it is not a
parameter that needs careful tuning.

**Where it does not reach.** The task here is *homogeneous* — every worker does the same job on a
different slice of one document. Nothing in the paper speaks to heterogeneous sub-tasks, to agents with
different tools or roles, to depth beyond one level, or to a decomposition decided at runtime by a
planner. The Subject's axes of "what decides whether to split" and "what sets the depth" are answered
here in the most degenerate possible way (input length; arithmetic), so the paper is evidence about
what a *fixed pipeline* can do, not about planning.

**Concerns a harness designer should carry forward, unresolved.**

- *The cost question is open, not answered.* The `O(nk)` vs `O(n^2)` result is about attention FLOPs
  inside a hypothetical self-hosted decoder, and says nothing about the metric an orchestrator actually
  pays: billed tokens, API calls, and serial latency. On those, CoA is plainly *more* expensive than a
  single call — `ceil(n/k)` sequential round-trips, each re-encoding the previous CU — and the paper
  neither measures nor denies this. Any transfer of "CoA is cost-effective" into a harness argument
  needs that number supplied from elsewhere.
- *The chain is a single point of failure with no error handling.* No confidence signals, no retry, no
  path back to the source, no cross-checking. A worker that drops a fact 4 hops from the end has silently
  destroyed it, and the manager cannot tell. For a harness that must degrade gracefully, this is the
  most serious structural gap — and the paper's footnote argues *against* the redundancy that would fix
  it, which is a claim worth testing before adopting.
- *Sequential means unparallelizable.* CoA's advantage over Merge/Hierarchical is exactly the property
  that forbids running workers concurrently. Any harness weighing latency against quality faces this
  tradeoff directly, and this paper gives one side of it only.
- *The oracle gap suggests high per-run variance.* A 15–20 point gap between oracle and realizable
  selection over five permutations means individual chains are unreliable in ways the mean scores hide.
  For a harness, that reads as a variance problem to be characterized, not just as ensembling headroom.
- *Attribution between "two-stage prompting" and "multi-agent chaining" is unresolved* (see the
  low-agent-count datasets above). Before adopting the chain, a harness effort should run the control
  the paper skipped.

## Five citations worth chasing next

1. **Chen, Pasunuru, Weston, Celikyilmaz (2023), "Walking Down the Memory Maze: Beyond Context Limit
   through Interactive Reading," arXiv:2310.05029** — [ref 9]. The paper names this as the closest prior
   work and derives its Hierarchical baseline from it. It is the tree-structured, interactive-navigation
   alternative to a linear chain, and directly relevant to the depth/topology axis of the Subject.
2. **Khot, Trivedi, Finlayson, Fu, Richardson, Clark, Sabharwal (2022), "Decomposed Prompting: A Modular
   Approach for Solving Complex Tasks," arXiv:2210.02406** — [ref 27]. Task-level (not input-level)
   decomposition with typed modules and *recursive* further decomposition — the axis CoA deliberately
   does not touch.
3. **Liu, Lin, Hewitt, Paranjape, Bevilacqua, Petroni, Liang (2024), "Lost in the Middle: How Language
   Models Use Long Contexts," TACL 12:157–173** — [ref 38]. The phenomenon that supplies CoA's entire
   motivation for bounding per-agent context; Section 5.3 replicates its setup.
4. **Guo, Chen, Wang, Chang, Pei, Chawla, Wiest, Zhang (2024), "Large Language Model based Multi-Agents:
   A Survey of Progress and Challenges," arXiv:2402.01680** — [ref 19]. The survey CoA positions itself
   inside; the fastest route to the rest of the topology/coordination literature.
5. **Zhou, Scharli, Hou, Wei, Scales, Wang, Schuurmans, Bousquet, Le, Chi (2022), "Least-to-Most
   Prompting Enables Complex Reasoning in Large Language Models," arXiv:2205.10625** — [ref 85]. Cited in CoA's Complex Task Reasoning related work as the canonical sequential
   sub-question decomposition that stays within one context window — the single-agent limit case that
   CoA claims to extend past.

*(Runner-up worth noting: Shnitzer et al., "Large Language Model Routing with Benchmark Datasets,"
arXiv:2309.15789 [ref 56] — the paper's own proposed remedy for its unmeasured cost problem.)*
