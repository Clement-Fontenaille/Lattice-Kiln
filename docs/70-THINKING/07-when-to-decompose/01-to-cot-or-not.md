# To CoT or not to CoT? Chain-of-thought helps mainly on math and symbolic reasoning

*Review — collect phase. Source read: arXiv:2409.12183v3 [cs.CL], 07 May 2025 (full HTML, main body + Appendices A-J).*

## Density

**Density: HIGH.** Two independent evidence streams - a 110-paper / 1,218-comparison meta-analysis and a 20-dataset x 14-model first-party run - plus a plan/execute mechanistic probe; heavy verified appendices, almost no filler. Sits on the Subject's lower boundary: the cheapest possible "split into steps" intervention, measured wide, with the finding that its benefit is narrow.

## Name, keywords, year, venue

- **Name.** "To CoT or not to CoT? Chain-of-thought helps mainly on math and symbolic reasoning."
- **Authors.** Zayne Sprague, Fangcong Yin, Juan Diego Rodriguez, Dongwei Jiang, Manya Wadhwa, Prasann Singhal, Xinyu Zhao, Xi Ye, Kyle Mahowald, Greg Durrett.
- **Year / venue.** ICLR 2025 (arXiv v3, May 2025). Code: github.com/Zayne-sprague/To-CoT-or-not-to-CoT; prompts and per-model outputs on HuggingFace (TAUR-Lab collection).
- **Keywords (mine, not the paper's).** chain-of-thought; scope-of-benefit study; meta-analysis of a prompting technique; symbolic vs non-symbolic tasks; plan/execute separation; tool-augmented solving; inference-cost selectivity; single-forward-pass reasoning; negative-result-shaped survey.

## One-line thesis

Prompt-based chain-of-thought buys a large accuracy gain almost exclusively on tasks with a symbolic core (math, formal logic, algorithmic manipulation), where the gain comes specifically from *executing and tracking* symbolic steps — and even there an external solver beats it, so CoT is best understood as a universal but poor approximation of a solver rather than a general-purpose "think harder" lever.

## Approach

Two independent evidence streams, plus a third mechanistic probe.

1. **Meta-analysis of the published literature.** All 4,642 papers from ICLR 2024, EACL 2024 and NAACL 2024 (incl. Findings and Workshops) were filtered automatically for >=2 mentions of "CoT"/"chain-of-thought"/"chain of thought" -> 516 papers; then manually filtered to those reporting a like-for-like CoT-vs-direct-answer comparison -> **110 papers, 1,218 experimental comparisons, 264 datasets**. Excluded: multimodal models, CoT-fine-tuned models, any "CoT" method using multiple forward passes (self-consistency, tree-of-thought), and tool-augmented systems. Where several prompts were reported, the best-performing prompt was taken for *both* arms. Each comparison was hand-assigned to one of 14 task categories, assigned from the task description alone, without looking at system performance.

2. **First-party evaluation.** Zero-shot and few-shot direct-answer vs CoT prompts, run over **20 datasets x 14 models**, with each dataset assigned to one of five reasoning categories (Commonsense, Knowledge, Soft Reasoning, Symbolic, Mathematical). Greedy decoding, vLLM for open models, APIs for closed ones; dataset-and-model-tailored answer extractors, with the answer's average position in the output tracked to confirm direct-answer prompts really do answer early (Appendix F.3).

3. **Planning/execution decomposition (Section 5).** For symbolic tasks, the pipeline is split into a *planning* stage (map the question into a formal specification — a Python program for math, first-order logic for logic datasets) and an *execution* stage (solve the specification). Five settings are compared: few-shot direct answer; few-shot CoT; **Plan + Direct Solver** (LLM writes the plan, then answers directly from it); **Plan + CoT Solver** (LLM writes the plan, then works through it step by step); **Plan + Tool Solver** (LLM writes the plan, a Python interpreter or the Z3 SMT solver executes it — i.e. PAL for GSM8K, SatLM for logic). Unparseable plans get a random guess on multiple choice, otherwise count as wrong.

The paper deliberately scopes itself to *single-inference* prompting. Decomposed prompting, multi-agent debate, self-consistency and tree-of-thought are explicitly excluded from the analysis; tool augmentation appears only as the comparison arm in Section 5.

## Models targeted

Contemporary instruction-tuned models only; no base models, no reasoning-trained models (the paper predates widely available o1-style models in its evaluation set). Open: Llama 2 7B Chat, Mistral 7B Instruct v0.3, Llama 3.1 8B Instruct, Llama 3.1 70B Instruct, Gemma 2 9B It, Phi-3 Small 8k Instruct, Qwen 7B Instruct, Qwen 72B Instruct. Closed (API): gpt-4o-mini-2024-07-18, gpt-4o-2024-08-06, Gemini 1.5 Flash, Gemini 1.5 Pro, claude-3-haiku-20240307, claude-3-5-sonnet-20240620. Llama 2 7B and Gemma 2 9B are run at a 4k context window (a vLLM constraint for Gemma). Closed models cannot take a prefilled assistant turn, so their CoT prompts differ slightly — "let's think step by step" cannot be used to warm-start the completion.

## Benchmarks / datasets used

Twenty datasets, categorised by the reasoning they require:

- **Commonsense:** CommonsenseQA, StrategyQA, SiQA, PIQA, WinoGrande.
- **Knowledge:** ARC-Easy, ARC-Challenge, MMLU, MMLU Pro.
- **Soft Reasoning:** AGIEval LSAT, BiGGen Bench (free response, LLM-as-judge on a 1-5 scale with GPT-4o-mini), MuSR, MuSiQue (short answer, GPT-4o used to judge span equivalence).
- **Symbolic:** BIG-Bench Hard, FOLIO, ContextHub (levels 1 and 2).
- **Mathematical:** GPQA, GSM8K, GSM8K-Hard, MATH.

Section 5's plan/execute comparison runs on GSM8K, GSM8K-Hard, ContextHub and FOLIO. Answer formats span multiple choice, true/false/unknown, short answer and free response; few-shot counts per dataset range 0-8 (SiQA, PIQA, WinoGrande, ARC, MuSiQue and BBH have no few-shot setting). Hardware: 8xA40 or 4xQuadro RTX 8000 for local models.

## Author incentive

Academic, and mostly UT Austin: eight of ten authors at UT Austin (Greg Durrett's group), plus Johns Hopkins and Princeton. Funding acknowledged: NSF CAREER IIS-2145280 (Durrett), NSF CAREER 2339729 (Mahowald), the NSF AI Institute for Foundations of Machine Learning (IFML), a Sloan Research Fellowship, and a grant from Open Philanthropy. No lab or vendor stake in any model or product evaluated, and no method of their own being sold — the paper's contribution is a scoping/negative result about a technique nobody in particular owns. Two mild reflexivity notes worth recording rather than resolving: MuSR (Sprague et al., 2024) and ContextHub are used as evaluation datasets and MuSR is a first-author dataset; and the paper's framing pushes toward "move beyond prompt-based CoT to search, interacting agents, or fine-tuned models," which is the direction the authors' own subsequent research agenda would naturally sit in.

## Measurement methodology (brushed)

- **Dependent variable.** Throughout, the *CoT delta*: accuracy (or task metric, normalised 0-100) under a CoT prompt minus the same metric under a direct-answer prompt, for a matched (model, dataset) pair. BiGGen Bench is scored as the rate of LLM-judge scores >= 4.
- **What is controlled.** Same model, same dataset, same extractor within a format; prompts held constant across models except where a closed API forbids assistant prefill. Prompt sensitivity is checked separately (Appendix D: 4 zero-shot CoT prompt variants x 7 datasets on Llama 3.1 8B — variation is small and no variant dominates). Few-shot vs zero-shot is checked separately (Appendix E: the *set* of datasets that benefit does not change; magnitudes shift somewhat on symbolic datasets; only MuSR Team Allocation flips). Answer position in the output is tracked to verify the direct arm is genuinely direct. Decoding is greedy, so single-sample, no ensembling.
- **What is explicitly *not* controlled: compute.** The paper says so itself — CoT spends more tokens than direct answering, and "a truly fair comparison should match the compute of the two methods, e.g. ensembling across multiple prompts." It does not run that matched-compute comparison; it uses the observation to discount small positive deltas rather than to correct them.
- **N.** Meta-analysis: 1,218 comparisons, 110 papers, 264 datasets, 14 hand-assigned categories, aggregated per-paper-per-category (blue points in Fig. 2) so that a single prolific paper cannot dominate a category. Experiments: 20 datasets x 14 models across zero-shot and few-shot; per-dataset item counts are not centrally tabulated in the main text (Appendix G reports slice-level N for MMLU, e.g. 378 items for elementary_mathematics, 1,350 for MMLU Pro math).
- **Significance.** Treated in one place only, and treated well there: for the 13 datasets in the Knowledge / Soft Reasoning / Commonsense categories, paired bootstrapping over model-dataset pairs with a Bonferroni correction for 14 models x 13 datasets, giving alpha = 0.00027. Result: ~32% (59) of the positive comparisons in those categories reach significance, and 26 of those 59 are MMLU / MMLU Pro. Elsewhere — the meta-analysis, the math and symbolic categories, and Section 5's five-setting comparison — differences are reported as means and medians with no significance testing, which is defensible given the size of the effects there but is worth naming.
- **Attribution instrument for MMLU.** A deliberately crude proxy: bin each question by whether an "=" appears in the question text *or* in the model's generated response. Coarse (a generated "=" is partly an effect of the CoT arm itself, not only a property of the question), but it is doing the work of a subject-level breakdown and Appendix G corroborates it with the actual MMLU subject slices — 6 of the top-12 CoT-benefiting slices are literally named math/mathematics, and the authors argue the remainder are mathematical in content.

## Key findings

**Finding 1 — the benefit is concentrated on symbolic tasks, in both evidence streams.**
In the literature meta-analysis the three top categories by median CoT delta are symbolic/algorithmic (+14.2), math (+12.3) and logical reasoning (+6.9); average accuracy across those three is 56.9 with CoT vs 45.5 without. Across *all other* categories combined the average is 56.8 with CoT vs 56.1 without — a 0.7-point difference the authors decline to call a win, on the compute-parity argument above. Their own experiments reproduce the shape: on Commonsense and Knowledge datasets the CoT and direct curves sit on top of each other; on Mathematical the gap is enormous (Table 6 zero-shot category averages: e.g. GPT-4o 36.5 -> 63.3, Llama 3.1 8B 16.0 -> 47.8, Claude 3 Haiku 18.1 -> 48.2), with per-dataset gains as large as +41.6 on MATH and +66.9 on GSM8K; Symbolic gains ~10-13 points; Soft Reasoning small and uneven.

**Finding 1b — the apparent exceptions are symbolic underneath.** The top-10 outlier papers with large non-math CoT deltas are examined one by one and largely re-explained: BBH is mostly algorithmic/arithmetic/logical; BIG-Bench Navigate reduces to counting steps; BIG-Bench Temporal needs deduction; MMLU Moral Scenarios is a symbolic conjunction of two independent questions. A few genuinely do not fit the trend and are named as such (ScienceQA, a proprietary dialogue-evaluation set, Commitment Bank, verbalized confidence). On MMLU, as much as **95% of the total CoT gain is attributable to questions where an "=" appears in the question or the response**; for the non-math remainder, the authors report finding *no* feature that predicts when CoT will help.

**Finding 1c — answer format is not the hidden variable.** MuSiQue (short answer, semi-symbolic, multi-hop) shows no CoT gain; BiGGen Bench (free response, with a "plan before you answer" prompt and only the answer shown to the judge) shows only mild improvement. The authors read this as a hint that *pre-planning alone* may be insufficient to unlock reasoning — and explicitly say future work is needed to establish it.

**Finding 2 — the mechanism is execution, not planning, and a solver does execution better.**
In the five-setting comparison: having a plan alone (Plan + Direct Solver) does not recover most of the gain over direct answering; you need step-tracking (CoT, or Plan + CoT Solver) for strong performance; but **Plan + Tool Solver dominates both CoT and Plan + CoT Solver in most settings**. The authors' own reading: CoT helps exactly when the solution steps require substantial tracing and computation, and in that regime "CoT appears to be a poor (but universal) approximation" to a symbolic solver. Their normative conclusion is that LLMs should be paired with symbolic solvers at inference time whenever the task admits one.

**The authors' reading of the whole.** CoT's utility is "circumscribed by tool augmentation": where CoT helps, better tools already exist; where no tool exists (soft reasoning, commonsense), CoT gives little. Two implications they draw. (i) *Selective application* — CoT is unnecessary for many problems where it is currently applied by default, so it can be switched off to save inference cost with no accuracy loss. (ii) *Move beyond prompt-based CoT* — toward search, interacting agents, or models more heavily fine-tuned for CoT, if intermediate computation is to pay off outside math and symbols. They are careful to say CoT remains a powerful technique, and they nod at theory (Transformers are fundamentally augmented by CoT) and at work on internalising CoT as evidence that explicit intermediate tokens are not yet used to their full potential.

## Open questions the paper itself raises

In its own framing (Section 6 "Limitations", Section 6 discussion, and Appendix I):

- **Long-horizon planning is not covered** (BiGGen Bench aside). Two stated reasons: the authors care about tasks conveyed in language, and language-only tasks show less complex planning; and there is already a large, unsettled pro/anti literature on CoT for planning that they decline to re-adjudicate.
- **Dataset contamination is unaddressed** directly. They argue the conclusions survive it for four reasons: a range of model scales including small models with less memorisation capacity; datasets with poor direct-answer performance (GSM8K-Hard) are unlikely to be memorised; recent datasets (MuSR, BiGGen Bench) are included; and the meta-analysis spans papers using older LLMs.
- **Why only symbolic tasks?** They ask, and leave open, whether non-symbolic tasks could be helped by explicitly instilling other modes of deliberation (their example: process of elimination for multiple choice), or whether there is a fundamental limit imposed by pre-training data.
- **Is pre-planning enough?** The BiGGen Bench result "could imply that pre-planning is insufficient for unlocking reasoning capabilities" — flagged explicitly as needing future work to prove.
- **Can CoT be improved?** Multi-inference methods help but cost much more compute, and careful benchmarking sometimes finds naive techniques as good as iterative ones; theory says CoT fundamentally augments Transformers; internalised-CoT results suggest explicit tokens are underexploited. All three are left as directions, not claims.
- **No feature predicts CoT benefit on non-math MMLU questions** — stated as an open negative result.

## Appreciation

*Keeping mechanism separate from magnitude.*

**What transfers as an argument (mechanism).**

1. *The default is wrong.* The most durable contribution is not a number but the demolition of a background belief the paper names outright: that "think step by step" helps on nearly all reasoning problems. Two independent streams — other people's published numbers, and their own runs — agree on the shape. That agreement is the strong part of the design; neither stream alone would carry it.
2. *Planning and execution are separable, and they are not equally valuable.* The Section 5 decomposition is the paper's best idea and the one most portable outside it. Producing a plan is cheap and, on its own, buys little; the accuracy lives in faithfully executing and tracking the plan; and execution is precisely the part a deterministic tool does better than token generation. That is a mechanism claim, not a benchmark artefact.
3. *"CoT as a poor but universal approximation of a solver."* A genuinely useful framing: it predicts *where* CoT should help (tasks with a formal system to approximate) and *where* it should be swapped out (tasks where a real solver exists), and it explains the soft-reasoning null result without appealing to model weakness.
4. *Verbosity is not deliberation.* Free-response results (BiGGen Bench, MuSiQue) suggest that adding a planning preamble to a generation task is not the same intervention as adding intermediate computation to a symbolic one — even though both look like "make it think first" in prompt space.
5. *Selectivity is a legitimate design axis.* "Apply CoT conditionally, save the tokens" follows from the evidence rather than from taste.

**What is a number valid only inside this setup (magnitude).**

1. *Every specific delta is bound to a model cohort that has since moved.* The evaluation is instruction-tuned, non-reasoning-trained models of the 2024 generation (Llama 2/3.1, Gemma 2, Mistral 7B, GPT-4o family, Gemini 1.5, Claude 3/3.5). The paper is careful that it studies *prompt-based* CoT; nothing in it measures models post-trained to reason by default, and the +40-to-+67-point math gaps in particular are a statement about the direct-answer arm of *these* models.
2. *The category means (+14.2 / +12.3 / +6.9, 56.8 vs 56.1) inherit the meta-analysis's construction.* Best-prompt-for-both-arms selection, hand-assignment of 264 datasets into 14 categories, per-paper aggregation, and publication bias in what gets reported at all. The authors are transparent about the procedure; the ranking of categories is more trustworthy than the exact magnitudes.
3. *"95% of the MMLU gain comes from '=' questions"* is a proxy statistic, and the proxy is partly downstream of the treatment (an "=" in the *generated response* is something CoT itself produces). Appendix G's subject-slice breakdown supports the direction; the 95% figure should travel as "overwhelmingly concentrated on math slices," not as a precise fraction.
4. *The compute asymmetry is uncorrected.* Every reported delta compares a short output against a long one. This cuts *toward* the paper's thesis for the small non-symbolic gains (they would look worse still at matched compute) and *against* nothing in the symbolic case, but it means no number here is a matched-budget number.
5. *Plan + Tool Solver's margin is scoped to four datasets* (GSM8K, GSM8K-Hard, ContextHub, FOLIO) and to two specific tool pipelines (PAL/Python, SatLM/Z3), with unparseable plans handled by random guessing on multiple choice. It establishes that a solver can beat CoT on solver-shaped tasks; it does not measure how often real tasks are solver-shaped.
6. *The significance testing covers only the 13 soft/knowledge/commonsense datasets.* The strongest claims (math, symbolic) rest on effect sizes large enough not to need it, but the asymmetry in statistical treatment is real.

## How it could serve a harness-design effort — limitations, major concerns

*Stemming the discussion, not resolving it.*

- **It is a boundary paper for the Subject, not a decomposition paper.** The scope is explicitly single-forward-pass prompting: decomposed prompting, multi-agent debate, self-consistency and tree-of-thought are excluded by construction from both the meta-analysis and the experiments. So it does not measure task decomposition as the Subject defines it. What it does supply is a floor: the cheapest possible "split the work into steps" intervention, measured across a wide task space, with the answer that its benefit is narrow. Any argument that heavier splitting pays off has to explain what the heavier machinery adds that this floor does not.
- **The planning/execution split is a decomposition schema with an empirical verdict attached.** Section 5 is the part a harness designer would actually reuse: it names two stages, measures each, and finds the value concentrated in execution. If that generalises, it argues for harnesses that spend their budget on *executing* sub-steps reliably (tools, verification, state tracking) rather than on producing ever-richer plans. Open: it is measured on four solver-shaped datasets; whether the same asymmetry holds when the sub-steps are non-symbolic is exactly what the paper cannot say.
- **"Where a real solver exists, prefer it" as a routing rule.** The paper's own recommendation — pair LLMs with symbolic solvers at inference time when the task admits one — is a harness-level claim disguised as a prompting result. It raises but does not answer: who decides a task is solver-shaped, at what cost, and what happens on the misroutes (their own fallback for unparseable plans is a random guess).
- **Conditional deliberation as a cost lever.** "CoT can be applied selectively, maintaining performance while saving inference costs" is the most directly actionable line for a harness, and it is also the least supported operationally: the paper reports that on non-math MMLU questions it found *no* feature predicting when CoT helps. A selectivity policy is asserted to be valuable and shown to be hard to build in the same paper.
- **A caution about pre-planning.** BiGGen Bench and MuSiQue hint that adding a plan-first step to a generation or multi-hop task is not the same intervention as adding intermediate computation to a symbolic one. For a harness whose default is "plan, then act," this is a hint that the plan step may be paying for itself less often than assumed — the authors themselves label it a hint needing proof.
- **Main concerns about leaning on it.** (i) The model cohort predates reasoning-trained models, so the size (though probably not the shape) of every effect is dated. (ii) No compute-matched baseline anywhere, which the paper concedes. (iii) The meta-analysis measures *the literature*, so it inherits what people chose to publish and to compare. (iv) Long-horizon planning — the regime closest to agent harnesses — is explicitly out of scope, which is precisely where a harness effort would most want data. (v) A minor internal inconsistency worth noting when citing specifics: the model list in Table 3 names Phi-3 Small while Table 5 lists Qwen 7B/72B instead, and the count of models is given as 14 in the abstract against 13 rows in Table 5.

## Five citations worth chasing next

1. **Ye et al., 2023 — SatLM: Satisfiability-Aided Language Models.** The logic half of the Plan + Tool Solver arm, and the source of the planning prompts. The clearest instance in the paper of "LLM writes a formal specification, a non-LLM component solves it."
2. **Gao et al., 2023 — PAL: Program-Aided Language Models.** The math half of the tool arm, and the origin of GSM8K-Hard. Directly relevant to whether the execution stage should ever be an LLM.
3. **Khot et al., 2023 — Decomposed Prompting.** Named in the paper only to be *excluded* from scope (footnote 3). That exclusion is where the Subject's territory actually begins, so it is the obvious next read.
4. **Merrill & Sabharwal, 2024 — on the expressive power of chain-of-thought / intermediate tokens.** The theoretical counterweight the authors invoke: Transformers are fundamentally augmented by CoT, which is why they argue the empirical ceiling here is about *prompt-based* CoT rather than intermediate computation as such.
5. **Olausson et al., 2024** (cited for the finding that careful benchmarking sometimes shows naive techniques are as good as iterative ones). The paper leans on this in one sentence to discount multi-inference methods; for a decomposition review that single sentence is load-bearing and deserves to be checked at the source.

Runners-up, noted but not chosen: Nye et al., 2022 (Scratchpads, the pre-history of the math/symbolic finding); Wang et al., 2023b / Sun et al., 2024 (plan-and-solve style separations); Valmeekam et al., 2023 (the planning debate the paper deliberately sidesteps).
