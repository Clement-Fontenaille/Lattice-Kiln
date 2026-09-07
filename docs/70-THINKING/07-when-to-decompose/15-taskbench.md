# TaskBench: Benchmarking Large Language Models for Task Automation

## Density

**Density: MEDIUM-HIGH** — the paper is a benchmark-construction paper with little padding, and its central object (a graph-structured reference decomposition, plus metrics that score the decomposition's *structure* separately from tool naming and parameter filling) sits directly on the Subject; what pulls it below HIGH is that decomposition is operationalised as one-shot plan emission scored by ROUGE against a synthetic reference, so the paper measures a model's ability to *produce* a decomposition, never the cost or benefit of *executing* one.

- **Keywords (mine):** graph-structured reference plan; tool dependency graph; node/edge F1; reverse-generated benchmark data; decomposition-as-prediction; three-stage automation pipeline; synthetic-reference validity; complexity scaling of plan accuracy.
- **Year:** arXiv v1 Nov 2023; v4 Nov 2024. **Venue:** NeurIPS 2024, Datasets and Benchmarks Track.
- **Authors:** Yongliang Shen, Kaitao Song, Xu Tan, Wenqi Zhang, Kan Ren, Siyu Yuan, Weiming Lu, Dongsheng Li, Yueting Zhuang.

## Approach

TaskBench frames "task automation" as an explicit three-stage pipeline —
**task decomposition → tool selection → parameter prediction** — and builds
both a dataset and a metric suite that score each stage separately from a
*single* model output.

**The Tool Graph.** The paper's organising object is a Tool Graph
`G = {T, D}`: `T` is a set of tools (nodes), `D` a set of directed
dependency edges `(t_a, t_b)` meaning `t_a` depends on `t_b`. Two dependency
kinds are modelled: **resource** dependencies (an edge exists iff the output
type of one tool matches the input type of the other) and **temporal**
dependencies (an edge asserts an ordering between two tools). The authors
contrast this with the taxonomy *trees* used by prior tool benchmarks — a
tree can group tools by category but cannot state that one tool's output
feeds another's input.

Three domain graphs are built by hand from tool inventories:
- **Hugging Face tools** — 23 nodes, 225 edges (resource dependencies, from HF task input/output types).
- **Multimedia tools** — 40 nodes, 449 edges (resource dependencies; user-facing tools like downloaders, video editors).
- **Daily Life APIs** — 40 nodes, 1,560 edges (predominantly *temporal* dependencies; the near-complete graph density follows from that — almost any two APIs can be ordered).

**A decomposed task = a subgraph.** This is the key representational move.
A task instance's reference decomposition is literally a sampled subgraph
`G_s = {T_s, D_s}` of the domain Tool Graph, drawn by
`Sample(G, mode, size) → G_s` where `mode ∈ {node, chain, DAG}` and
`size ∈ {1..10}` is the number of tools. The three modes correspond to
three decomposition shapes (the taxonomy is inherited from HuggingGPT):
- **node** — no decomposition; a single tool answers the request;
- **chain** — sequential decomposition, each sub-task feeding the next;
- **DAG** — branching decomposition, a sub-task depending on several
  predecessors or feeding several successors.

Sampling ratios are fixed at node:chain:DAG = 3:7:8, with subgraph sizes
drawn from `{0.1, 0.2, 0.3, 0.2, 0.1, 0.05, 0.025, 0.025, 0.025}` over sizes
1..9+. So the benchmark's difficulty distribution is a *design choice*, set
before any model is run.

**Back-Instruct.** The dataset is generated backwards, from structure to
language, in two conceptual steps issued as one GPT-4 prompt:
1. `BackInstruct_1(G_s = (T_s, D_s)) → I` — given the sampled subgraph's
   nodes *and edges*, synthesise a natural user instruction `I` that would
   require exactly those tools in exactly those dependencies.
2. `BackInstruct_2(G_s, I) → {P, Ḡ}` — given the subgraph and the
   instruction, emit the natural-language **task-decomposition steps** `P`
   and the fully parameterised **tool invocation graph** `Ḡ` (the skeleton
   `G_s` with arguments filled in: literal user text, a placeholder resource
   filename like `example.jpg`, or a `<node-j>` reference to an upstream
   node's output).

The prompt (Appendix A.5) hard-constrains the mapping: *"The number of task
steps must equal the number of nodes. Each tool node can only be used once…
The dependencies among task steps must be consistent with the edges of both
the tool graph and the tool invoking graph."* One step ≡ one node, by fiat.

**Quality control** is three-layered: (i) an **LLM-based self-critic** — a
`check_by_teacher` field inside the same JSON response, in which the model
role-plays a strict teacher judging whether its invocation graph is
"Executable" and "Correct" (Correct = strictly the same nodes and edges as
the sampled subgraph); (ii) a **rule-based critic** that mechanically
compares node and edge sets of the produced graph against the sampled
subgraph; (iii) **human verification** by calibrated expert reviewers.
Retention: the rule-based critic keeps 82.7–87.7%, the LLM critic 74.0–79.6%,
both together 69.2–76.0%, and after human revision/filtering 61.76% /
62.71% / 60.42% of generated samples across the three domains. Final released
scale is 17,331 samples (12,217 HF / 8,904 Multimedia / 7,150 Daily Life
before human filtering), averaging ~3.5–3.8 nodes and ~2.5–2.8 links per
sample.

**TaskEval.** Inference uses one standardised prompt (Appendix A.6) listing
all tools in the domain with descriptions and parameter fields, and asking
for a single strict-JSON object containing `task_steps`, `task_nodes` (tool
name + arguments) and `task_links` (source/target pairs). Every stage is
scored from that one response, so the three stages are separated *by metric*,
not by separate model calls.

## Models targeted

Proprietary: **gpt-4**, **gpt-3.5-turbo**, **text-davinci-003**,
**gemini-pro**, **claude-2**. Open-source: **mistral-7b-v0.3**,
**codellama-13b** and **codellama-7b**, **vicuna-13b-v1.5** and
**vicuna-7b-v1.5**, **nous-hermes-13b**, **wizardlm-13b**,
**llama-2-13b-chat** and **llama-2-7b-chat**, **llama-3-8b-instruct**,
**baichuan-13b-chat**, **internlm-chat-7b** (the last several appear only in
the Appendix A.7 tables). GPT-4 is additionally the *data engine* that
generates every reference instruction, reference decomposition and reference
invocation graph.

## Benchmarks / datasets used

Only TaskBench itself — the three domains constructed here (Hugging Face
Tools, Multimedia Tools, Daily Life APIs). No external benchmark is run; the
comparison to APIBench, ToolBench, MetaTool and API-Bank (Table 1) is a
qualitative feature table, not a shared-task evaluation. The internal
generation baselines are **Back-Instruct w/o edges** (nodes only in the
prompt) and **Self-Instruct** (model picks its own tools from descriptions).

## Author incentive

Zhejiang University, Microsoft Research Asia, and Fudan University; the first
author was an MSRA intern. The artefact ships inside **microsoft/JARVIS**,
the HuggingGPT repository — and HuggingGPT is both cited as motivation and
the source of the node/chain/DAG taxonomy the benchmark is built on. The
benchmark therefore measures a decomposition formalism that one of the
sponsoring groups already proposed, using GPT-4 (an OpenAI/Microsoft-adjacent
model) as the reference generator, and GPT-4 comes first in nearly every
table. No funding statement is given in the retrieved version. Stake is
positional and infrastructural (establishing TaskBench/TaskEval as *the*
standard for task automation) rather than commercial.

## Measurement methodology

**Dependent variables**, one family per stage, all computed from the same
single JSON generation:

1. **Task decomposition — ROUGE-1 / ROUGE-2 / ROUGE-L** between the model's
   emitted `task_steps` text and the reference steps `P`. It is a
   *surface-overlap text metric*: nothing structural is checked at this
   stage, only n-gram agreement with GPT-4's wording of the steps.

2. **Tool selection — Node F1, Edge F1, NED.**
   - **Node F1 (n-F1):** treat the predicted `task_nodes` as a set of tool
     IDs and the reference `T_s` as another set; a predicted node counts
     positive if its ID matches any ground-truth node label. Standard F1
     over precision/recall of that set match. It measures *which* tools —
     i.e. how many sub-tasks and of what kind — with no ordering.
   - **Edge F1 (e-F1):** the same set-F1, but over *edges*. A predicted edge
     `(source, target)` counts positive only if **both** endpoints exactly
     match a reference edge's endpoints. This is the metric that actually
     scores the *shape* of the decomposition — the dependency structure,
     what feeds what, what may run in parallel. It is set-based (not
     graph-isomorphism, not longest-common-subgraph), so a plan with all the
     right tools but the wrong wiring scores high n-F1 and near-zero e-F1.
     Because both endpoints must match, one wrong node destroys every edge
     incident to it: e-F1 is doubly penalised by node errors, which is part
     of why it sits so far below n-F1 everywhere.
   - **NED (Normalized Edit Distance):** reported for *chain* structures
     only — the normalised number of edit operations to turn the predicted
     sequence into the reference sequence; a sequential-order metric, lower
     is better.

3. **Parameter prediction — t-F1 / v-F1.** t-F1 is F1 over (task, parameter
   *name*) pairs; v-F1 over (task, parameter name, parameter *value*)
   triples. Argument-level, and the strictest of the metrics.

**How decomposition is separated from selection and parameters.** The
separation is purely metric-level, applied post hoc to one output: ROUGE
scores the prose plan, n-F1/e-F1 score the graph, t-F1/v-F1 score the
arguments. There is no ablation in which a model is given a correct
decomposition and asked only to select tools, or given correct tools and
asked only to fill parameters. Errors therefore propagate: a model that
decomposes into the wrong sub-tasks cannot score well on any downstream
metric, so the three stages are *reported* separately but not *isolated*
experimentally. Node F1 vs Edge F1 is the one place where a genuine
decomposition-internal separation exists — "did you find the right
sub-tasks?" against "did you get the dependencies right?".

**Controls.** A single fixed prompt template across all models; identical
tool lists per domain; results broken out by structure type (Node / Chain /
DAG) and by domain; Appendix A.4.1 breaks GPT-4 out by number of tool nodes
(1..10). Appendix A.4.2 varies shots (0/1/2) on Daily Life APIs.

**N.** Dataset: 17,331 generated samples across three domains; GPT-4's
per-node-count analysis reports 6,281 supports (the Multimedia both-critics
set). Human evaluation of *data quality*: 50 anonymised samples rated 1–5 by
3 experts on Naturalness / Complexity / Alignment. Dataset error audit: 148
randomly sampled instances, 18 found erroneous (~12%). LLM prediction error
analysis: 50 predictions, 3 models. Ranking consistency with human evaluation:
Kendall's τ and Spearman's ρ over model rankings, average τ = 0.89, ρ = 0.78.

**Significance.** None. No confidence intervals, no variance across seeds, no
significance tests anywhere; every number is a single point estimate from a
single run at unstated temperature. Rank-correlation coefficients are
reported without p-values or the n they are computed over.

## Key findings

**1. Getting the dependency structure right is far harder than getting the
sub-task set right.** Across all models, e-F1 trails n-F1 by roughly 20
points, and often far more. Hugging Face overall: gpt-4 n-F1 81.54 / e-F1
54.70; gpt-3.5-turbo 69.49 / 33.36; mistral-7b 65.96 / 21.91; vicuna-13b
50.82 / 7.28; llama-2-13b-chat 48.47 / 7.30. Multimedia: gpt-4 90.90 / 69.27;
gemini-pro 81.54 / 52.07. Daily Life: gpt-4 96.91 / 80.53; nous-hermes-13b
73.45 / **3.50**; llama-2-13b-chat 55.77 / 17.02. The authors' reading:
"understanding tool relationships is more complex than identifying individual
tools."

**2. The n-F1/e-F1 gap widens as models get weaker — the collapse is
structural, not lexical.** Several 13B models reach 70–82 n-F1 on Daily Life
APIs while scoring single-digit e-F1 (nous-hermes 71.17 n-F1 / 3.55 e-F1 on
chains; vicuna-13b 73.74 / 13.24). They name the right sub-tasks and then
fail to wire them. That is the paper's sharpest observation about
decomposition ability: *listing* sub-tasks and *ordering/relating* them are
separable capabilities that come apart cleanly at scale.

**3. Performance degrades monotonically with the number of sub-tasks.**
GPT-4, Multimedia (Table 10, n = 6,281): node-set accuracy 96.16 → 86.33 →
67.93 → 64.29 → 54.03 → 50.34 → 49.66 → 35.00 → 38.18 → 39.06 for 1..10
tools; graph accuracy (exact match of the whole decomposition) 96.16 → 84.53
→ 60.39 → 54.37 → 41.58 → 39.31 → 36.42 → 25.00 → 21.81 → 31.25. Overall
graph accuracy 67.25. So even the strongest model produces an exactly correct
5-node decomposition under half the time, and an exactly correct 8-node one a
quarter of the time. The sharpest drop is 2 → 3 tools.

**4. Structure type matters as much as size.** For most models, chain
performance exceeds DAG performance on edges (gpt-4 Daily Life: chain e-F1
83.47 vs DAG e-F1 42.01; claude-2 80.68 vs 41.04; gpt-3.5 70.66 vs 30.85).
Branching decompositions are markedly harder than sequential ones. Note the
Daily Life graph is temporal-dependency-based and very dense (1,560 edges over
40 nodes), which likely makes "the right DAG" much less determined than "the
right chain".

**5. Task decomposition (ROUGE) rankings differ from structural rankings.**
GPT-4 leads on R1/R2 by ~10 points on HF and Multimedia (HF: 52.42/30.38/47.21
RL; Multimedia 60.84/40.08/56.22). But on Daily Life APIs **codellama-13b
beats every model** (R1 89.86, R2 83.27, RL 86.12) against gpt-4's 85.07 /
72.36 / 82.16 — while codellama's e-F1 in that domain is 24.61 against gpt-4's
80.53. The authors read this as code pre-training helping "understand
structured task sequences." It equally shows that ROUGE-on-steps and
structural correctness are close to decoupled: a model can reproduce the
reference *wording* of a plan while getting the plan's dependencies wrong.

**6. Contributing factors, per the authors.** Reasoning ability and
instruction-following both track task-automation scores; code pre-training
gives an average +4.45% on tool prediction and +12.76% on parameter
prediction; RLHF-aligned models generalise better than open-source
counterparts.

**7. Demonstrations help a lot.** Daily Life APIs, 0→2 shots: codellama-13b
+20.78% n-F1 and +21.82% v-F1; text-davinci-003 e-F1 50.75 → 72.37; gpt-3.5
R-L 48.72 → 89.07. GPT-4's e-F1 moves 34.52 → 50.56 → 52.49. (Note the
oddity that GPT-4's *zero-shot* e-F1 of 34.52 in this table is below
gpt-3.5-turbo's 51.77 and far below GPT-4's 80.53 in Table 3 — the few-shot
table is evidently a different subset or configuration, and the paper does
not reconcile them.)

**8. Back-Instruct beats the alternatives on data quality.** Human ratings
(50 samples, 3 experts, 1–5): Back-Instruct 3.89 naturalness / 4.01
complexity / 3.66 alignment (overall 3.85); Back-Instruct w/o edges 3.44 /
3.27 / 3.62 (3.44); Self-Instruct 2.18 / 2.01 / 3.64 (2.61). The authors read
the w/o-edges ablation as proof that *edge information in the Tool Graph is
what produces natural, complex multi-step instructions* — dependency
structure is the generative source of task complexity, not an afterthought.
Alignment is essentially flat across all three methods (3.62–3.66), so the
gain is in naturalness and complexity only.

**9. Benchmark validity claim.** TaskEval's model ranking correlates with a
human ranking at Kendall's τ = 0.89 (0.89 / 0.83 / 0.94 by domain) and
Spearman's ρ = 0.78 (0.78 / 0.62 / 0.93). The authors treat this as
confirmation that the automated metrics capture what humans mean by task
automation quality.

**10. The authors' own error audit of their dataset.** 148 samples, 18
errors (~12%), in five categories: incomplete instructions, impractical
instructions, mismatched parameter types, incorrect parameter values, and
**incorrect tool dependency** (wrong linking/sequencing in the reference
graph itself). Model-side, over 50 predictions: gpt-4 makes 0 missing-tool /
2 dependency / 3 parameter errors; gpt-3.5-turbo 2 / 8 / 11; codellama-13b
4 / 9 / 13 — dependency errors are the most common class across models.

## Open questions the paper itself raises

In the paper's own framing:

- **Reference-data correctness is not guaranteed.** Stated plainly in A.2.1:
  "we admit that it is challenging to guarantee the correctness of all
  generated samples," with the ~12% measured error rate. Among the error
  classes is *Incorrect Tool Dependency* — errors in the reference
  decomposition structure, the very thing e-F1 scores against.
- **Better prompts and more criteria are needed.** The authors conclude the
  error analysis by proposing "a more elaborate prompt (e.g., more detailed
  tool-use specification and demonstrations)" for generating invocation
  graphs, and "more high-quality criteria to continuously improve our dataset
  in addition to our rule-based and LLM-based critics."
- **Coverage.** The conclusion commits to expanding to more domains.
- **Metrics.** The conclusion commits to developing "more advanced metrics" —
  an implicit admission that ROUGE / set-F1 do not exhaust what should be
  measured.
- **Dependency types.** Only resource and temporal dependencies are modelled;
  the paper explicitly notes environment dependencies "and so on" exist and
  are out of scope.

Notably *not* raised by the authors as limitations: the circularity of using
GPT-4 as both data engine and top-ranked evaluand; the assumption that a
reference decomposition is unique; the absence of execution.

## Appreciation

**MECHANISM — what transfers as an argument.**

- *Representing a decomposition as a labelled DAG over a tool inventory, and
  scoring nodes and edges as separate F1s, is a genuinely reusable
  measurement idea.* It gives an operational answer to "how good was the
  split?" that does not require running anything: n-F1 asks whether the right
  sub-tasks were identified, e-F1 whether they were correctly related. The
  split isolates two failure modes that a single end-to-end success metric
  would confound.
- *The finding that node identification and edge wiring dissociate* — models
  at 70–80 n-F1 with 3–13 e-F1 — is a mechanism claim that should survive
  changes of setup. Producing a *list* of sub-tasks is cheap; producing a
  correct *dependency structure* over them is the expensive capability.
- *DAG decompositions are harder than chains* and *exact-plan accuracy decays
  steeply with sub-task count* are directional claims that read as robust:
  the shape of the curve (a cliff between 2 and 3 sub-tasks, exact-graph
  accuracy roughly halving by 5 sub-tasks) is more informative than its
  levels.
- *The w/o-edges ablation is the paper's cleanest causal result on the
  Subject*: withholding dependency edges from the generator degrades rated
  complexity from 4.01 to 3.27 and naturalness from 3.89 to 3.44, while
  alignment stays flat. Dependency structure is what makes a synthesised
  multi-step task genuinely multi-step rather than a list of unrelated
  errands.
- *Errors concentrate in dependencies, not tool names.* Both the model error
  audit (dependency errors the largest class in all three models) and the
  n-F1/e-F1 gap point the same way.

**MAGNITUDE — numbers valid only inside this setup.**

- Every absolute score is relative to a GPT-4-authored reference. ROUGE
  decomposition scores in particular measure *agreement with GPT-4's phrasing
  of the steps*, and GPT-4 is scored against its own output distribution.
  GPT-4's ~10-point lead on R1/R2 cannot be separated from self-preference.
- The domain spread is enormous and setup-driven: identical models score
  ~55 e-F1 (HF) and ~80 e-F1 (Daily Life). The Daily Life graph has 1,560
  edges over 40 nodes, so many edges are near-trivially guessable; HF's
  type-matched graph is sparser and stricter. "Edge F1 = 54.70" is a fact
  about that tool graph's density, not a portable difficulty level.
- The 20-point n-F1/e-F1 gap is partly an artefact of the metric's
  construction: exact both-endpoint matching means every node error voids all
  its incident edges. The gap's *existence* is mechanism; its *size* is
  metric design.
- Ranking correlations (τ = 0.89, ρ = 0.78) rest on ranking a handful of
  models; with n models this small, τ is coarse and no significance is
  offered. Spearman's ρ = 0.62 on Multimedia is materially weaker than the
  headline average suggests.
- Few-shot numbers cannot be read alongside Table 3 (GPT-4 zero-shot Daily
  Life e-F1 is 34.52 in Table 11 and 80.53 in Table 3).
- Single runs, no variance, no temperature disclosed: differences of a few
  points between adjacent models should not be read as ordering.

**On back-instruct validity — how do they know the reference decomposition is
correct?** This is the paper's structural weak point, and it deserves stating
carefully because the paper's whole claim to measure decomposition rests on
it.

The reference decomposition is correct **by construction, not by
verification**. The subgraph is sampled *first*; the instruction is then
written *to fit* it. So the guarantee the pipeline actually provides is
"there exists a reading of instruction I under which subgraph G_s solves it,"
because I was authored with G_s in hand. What it does not establish is the
converse and much stronger property the benchmark needs: *that G_s is the
only, or the best, decomposition of I*. Both critics check the same
direction — the rule-based critic compares node and edge sets of the
generated graph against the *sampled* subgraph, and the LLM critic's
`check_by_teacher` field defines "Correct" as "strictly consistent (with
strictly same nodes and same edges) with the given tool graph." Neither asks
whether a different valid decomposition of the same instruction exists. So a
model that produces a correct-but-different plan — a shorter route, a
different valid ordering of independent branches, the same work split at a
different granularity — is scored as wrong, and it will be scored wrong most
severely on e-F1, the decomposition metric. In dense temporal graphs like
Daily Life APIs, where any two APIs may be legitimately ordered, this
concern is at its worst.

Three further validity notes:
- The "one step = one node, each node used once" constraint is imposed by
  the generation prompt. Decomposition granularity is therefore fixed to the
  tool inventory's granularity: a benchmark instance can never require
  splitting one tool call into two reasoning steps, or several calls into one
  sub-task. This makes the benchmark measure *plan-to-tool-graph mapping*
  rather than decomposition in the open sense of the Subject.
- The instructions are back-derived from subgraphs sampled at a
  pre-set node:chain:DAG ratio of 3:7:8, so 80% of instances are multi-tool
  by design. This distribution is a stipulation about what task automation
  looks like, not an observation of it.
- Human verification retains ~61% of samples, and the residual error rate on
  a released sample was ~12% — including dependency errors in the gold
  graphs. The floor of e-F1 measurement noise is therefore non-trivial and
  unquantified.

## How it could serve a harness-design effort / limitations / major concerns

*Stemming the discussion, not resolving it.*

**What it offers a harness effort.**

- A concrete, cheap-to-compute instrumentation scheme for a planning stage:
  emit the plan as `{nodes, edges}`, and score node set and edge set
  separately against a reference. Any harness that produces an explicit plan
  before executing it can be measured this way without executing anything.
  The n-F1/e-F1 pair maps onto two distinct harness questions: is the split
  into sub-tasks right, and is the dependency graph between sub-tasks right?
- The dissociation result argues that a harness should not treat "the model
  produced a plan with plausible steps" as evidence the plan is executable.
  Sub-task naming is the easy half. If a harness relies on the model to also
  state dependencies (for scheduling, parallelisation, or argument
  threading), that is the part which fails first and fails hardest on
  smaller models.
- The complexity curve suggests a budget-shaped design question: if
  exact-plan accuracy for the strongest model falls to ~40% at 5 sub-tasks
  and ~25% at 8, a harness that emits a large plan in one shot is betting on
  a low-probability event. Whether the answer is recursive re-planning,
  replanning after failure, or capping breadth is exactly the axis the
  Subject describes, and this paper supplies evidence about the cost of
  *not* doing so — but no evidence about what any of those remedies buy.
- The `<node-j>` argument convention is a small but reusable interface idea:
  making inter-sub-task data flow explicit in the plan's arguments means the
  dependency edges are checkable rather than implicit in prose.
- The w/o-edges ablation suggests something for synthetic-eval construction
  generally: if you generate test tasks from structure, withholding the
  structure's edges yields easier and less natural tasks.

**Limitations that bound its usefulness here.**

- **No execution, therefore no cost accounting.** Nothing in the paper runs
  a tool. There are no latency, token, call-count or failure-recovery
  measurements, and no comparison against a non-decomposing baseline. On the
  Subject's question of whether splitting pays for itself, this paper is
  silent by design — it measures whether a model can *state* a decomposition,
  never whether decomposing improved an outcome.
- **Decomposition depth is flat.** Every reference plan is a one-level DAG
  over tool calls. There is no recursion, no sub-agent hierarchy, no
  runtime-determined depth — so the paper cannot speak to depth-setting
  policies at all.
- **Single-turn, upfront planning only.** The plan is emitted once, from the
  full tool list, with no observation of results and no opportunity to
  replan. Failure-triggered splitting and on-demand planning are outside the
  frame.
- **The reference is a synthetic single answer.** As above: correct-but-
  different plans are penalised, most heavily by the metric that matters most
  for decomposition. Any harness comparison run on TaskBench inherits that
  bias toward reproducing GPT-4's canonical split.
- **Full tool list in the prompt.** All 23–40 tools with descriptions and
  parameters are given at inference. A harness doing retrieval over a large
  tool corpus faces a different and harder problem that this setup abstracts
  away.
- **Model set is dated.** claude-2, text-davinci-003, gpt-3.5-turbo, llama-2.
  The absolute levels should be assumed stale; the shape of the findings is
  what survives.

**Major concerns.**

1. *Circularity.* GPT-4 authors the references and then tops the leaderboard
   on a surface-similarity metric (ROUGE) computed against its own text. The
   paper does not treat this as a threat to validity.
2. *Correctness of gold labels.* ~12% error rate, including dependency errors
   in the gold graphs, sets an unquantified ceiling on e-F1's reliability.
3. *Unreconciled numbers.* Table 3 and Table 11 disagree substantially on
   GPT-4's zero-shot Daily Life e-F1 without explanation.
4. *No uncertainty quantification anywhere.* Single runs, point estimates,
   no significance tests, rank correlations with no n or p.
5. *Domain-driven metric levels.* Absolute e-F1 depends heavily on tool-graph
   density; cross-domain comparison of scores is not meaningful, and the
   paper does not caution against it.

## Five citations worth chasing next

1. **HuggingGPT / JARVIS** — Shen et al., "HuggingGPT: Solving AI Tasks with
   ChatGPT and its Friends in Hugging Face" [8]. Source of the node/chain/DAG
   decomposition taxonomy TaskBench operationalises, and of the tool-graph
   framing; the closest thing to this paper's conceptual parent.
2. **ToolBench / ToolLLM** — Qin et al. [19]. The main prior tool benchmark;
   uses a taxonomy *tree* rather than a dependency graph, which is the
   contrast TaskBench defines itself against.
3. **Self-Instruct** — Wang et al. [29]. The generation method Back-Instruct
   inverts and is benchmarked against; needed to judge the data-generation
   claim on its own terms.
4. **MetaTool** [20] — the benchmark focused on *whether* a tool is needed at
   all, i.e. the decide-to-split question that TaskBench assumes away by
   construction.
5. **API-Bank** — Li et al. [23] — evaluates API-call correctness and
   response quality, the execution-side measurement TaskBench deliberately
   omits.
