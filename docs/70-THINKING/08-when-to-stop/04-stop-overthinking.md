# Stop Overthinking: A Survey on Efficient Reasoning for Large Language Models

## Density

**Density: MEDIUM** — the paper is a well-organised, genuinely comprehensive map of a fast-moving literature, but the body text is overwhelmingly one-or-two-sentence restatement of each cited paper's own abstract, it reports almost no numbers (two quantitative claims in the whole document) and adjudicates no disagreements; of its ~20 pages of body, roughly two (Section 4.2.1 and a paragraph of Section 5.2) bear directly on the Subject, and they name the stopping signals without evaluating any of them.

## Name, keywords, year, venue

- **Full title.** "Stop Overthinking: A Survey on Efficient Reasoning for Large Language Models."
- **Authors.** Yang Sui, Yu-Neng Chuang, Guanchu Wang, Jiamu Zhang, Tianyi Zhang, Jiayi Yuan, Hongyi Liu, Andrew Wen, Shaochen (Henry) Zhong, Na Zou, Hanjie Chen, Xia Hu. (The arXiv author block includes Na Zou, who is not in the brief's citation.)
- **Venue.** Transactions on Machine Learning Research (TMLR), 2025. The arXiv abstract page comment reads "Accepted by TMLR 2025", so the peer-review status given in the brief is confirmed against the primary source.
- **Version read.** arXiv:2503.16419v4 [cs.CL], 21 August 2025, licensed CC BY 4.0. This matters: v1 dates from March 2025 and the version I read has been repeatedly extended, mostly by adding names to the taxonomy figure rather than by adding prose.
- **Companion artifact.** A continuously updated GitHub repository, `Eclipsess/Awesome-Efficient-Reasoning-LLMs`, which the authors describe as the living form of the survey.
- **My keywords.** efficient reasoning; overthinking; long chain-of-thought; large reasoning models (LRMs); test-time scaling; length reward; early exit; confidence-based adaptive reasoning; consistency-based truncation; query routing; token budget.

## Approach — what they did

The authors claim the first structured survey of "efficient reasoning": the problem of reducing the length of generated reasoning while preserving reasoning accuracy. The framing premise is the **overthinking phenomenon** — that reasoning-trained models (OpenAI o1, DeepSeek-R1, QwQ-32B) emit thousands of tokens on trivial inputs, and that this verbosity costs latency and money and can occasionally cost accuracy by accumulating errors.

The organising move is to classify each method by **which part of the LLM pipeline it intervenes on**, which the authors treat as following "the inherent mechanism of LLMs":

1. **Model-based efficient reasoning** (Section 3) — change the weights.
   - 3.1 RL with a length-based reward added to the accuracy/format reward.
   - 3.2 SFT on variable-length CoT data, split into how the short-CoT dataset is *constructed* (post-reasoning compression vs obtaining compressed traces during reasoning) and how the model is then *fine-tuned* (standard, progressive, model merging).
2. **Reasoning output-based efficient reasoning** (Section 4) — change what the model emits at inference.
   - 4.1 Compressing reasoning steps into fewer *latent* representations (Coconut, CODI, CCoT, Heima, Token Assorted, looped transformers, SoftCoT).
   - 4.2 Dynamic reasoning paradigms during inference — **this is the early-exit / stopping-criterion family**, split into explicit criteria (reward-guided, confidence/certainty-based, consistency-based) and summarisation-based (LightThinker, InftyThink).
3. **Input prompts-based efficient reasoning** (Section 5) — change or triage the input.
   - 5.1 Prompt-guided conciseness (token budgets in the prompt, Chain of Draft, CCoT).
   - 5.2 Routing by question attributes: send easy queries to a cheap/non-reasoning path and hard ones to the expensive one.
4. **Efficient data and small models** (Section 6) — less training data (LIMO, s1), distillation, pruning, quantisation.
5. **Evaluation and benchmarks** (Section 7), then **applications and discussion** (Section 8: autonomous driving, embodied AI, healthcare, recommender systems, agentic AI).

Deliverables are: the taxonomy figure (Figure 3), five comparison tables, and per-method prose paragraphs. There is no new method, no experiment, and no reproduction. It is a map, explicitly and by design.

## Models targeted, scope, and what is / is not covered

- **Models.** The survey is about the class of *large reasoning models* — DeepSeek-R1 and its distillations, OpenAI o1, QwQ-32B, Kimi k1.5, s1-32B, Claude 3.7 Sonnet (cited as a deployed example of user-controlled thinking budget) — plus the base models (LLaMA, Qwen) that the surveyed methods fine-tune. The authors do not run any of them.
- **Benchmarks named** (as used by the surveyed work, not by the authors): GSM8K, MATH-500, AIME24, AQuA, StrategyQA, HotpotQA, ProntoQA, Game of 24, BlocksWorld, and the planning tasks of Sys2Bench; plus overthinking-specific benchmarks (S1-Bench, the agentic-overthinking trajectory study, Bag of Tricks).
- **Explicitly out of scope.** The authors draw a boundary against classical efficiency work: quantisation, KV-cache compression, and general model compression aimed at *smaller* inference, as opposed to *shorter* reasoning. (Section 6.2 then partially re-admits distillation/pruning/quantisation as a secondary topic, which is a mild inconsistency.)
- **Scope of the taxonomy figure vs the prose.** This is the single most important structural fact about the paper. Figure 3 lists roughly **160 methods** by name-plus-citation. The dynamic-reasoning leaf alone (the branch containing the stopping criteria) lists about **60** — Speculative Rejection, DPTS, Certaindex, Dynasor-CoT, ST-BoN, RSD, FastMCTS, More is Less, Self-Calib, CISC, ESC, DSC, RASC, AdaptiveStep, LightThinker, INFTYTHINK, CAR, AlphaOne, FlashThink, AnswerConvergence, NOWAIT, ASC, MUR, CGRS, ThinkLess, TrimR, Plan-and-Budget, and more. The prose of Section 4.2 discusses **ten** of them. Names such as FlashThink, AnswerConvergence, NOWAIT, S-GRPO, SEAL and THOUGHTTERMINATOR appear exactly once in the entire document — in the figure and the bibliography — with no description at all. For a reader who came for early exit specifically, the figure is a reading list and the prose is a sample of it.
- **Not covered.** Calibration as a research area in its own right (no reliability diagrams, no ECE, no discussion of whether the confidence signals these methods threshold on are actually calibrated); abstention and refusal; hallucination; multi-agent stopping; and — decisively for the Subject — the stopping of *tool-using, state-changing loops*, which is confined to two paragraphs (Section 7's "Evaluating Overthinking" and Section 8.2's "Efficient LLMs for Agentic AI").

## Author incentive

The authors are at **Rice University** (the DATA Lab orbit around Xia Hu) and the **University of Houston**; the contact addresses are `yang.sui@rice.edu` and `xia.hu@rice.edu`. No funding statement, no industrial sponsor, and no competing-interest declaration appears in the arXiv version. The visible incentives are academic and reputational rather than commercial: the paper stakes a first-mover claim ("the first structured survey") on naming and partitioning a field, and it is coupled to an "Awesome-" GitHub list whose value grows with citations and stars. That incentive is legible in the paper's shape — the taxonomy is maximally inclusive and grows version to version, and no surveyed method is ever criticised, ranked, or excluded. A survey competing to be *the* index of a field has a structural reason to be comprehensive and a structural reason not to make enemies; both show here.

## Measurement methodology — brushed

For a survey the relevant questions are how papers were selected and how competing claims were adjudicated, and the honest answer is that **neither is described**.

- **Selection protocol.** None stated. There is no search string, no database, no date cut-off, no inclusion/exclusion criteria, no count of papers screened versus retained, and no PRISMA-style flow. Coverage appears to be curated by hand and synchronised with the authors' GitHub list. Recency is the de facto criterion: nearly everything cited is 2024-2025 arXiv, much of it not peer reviewed, and the survey does not distinguish peer-reviewed work from preprints anywhere.
- **Dependent variable.** There is no shared one. Each surveyed paper is reported in its own terms (its own model, its own benchmark, its own baseline), so "token reduction" and "accuracy preserved" are never placed on a common axis. The survey never normalises, never re-plots, and never constructs a single accuracy-versus-token frontier.
- **N, controls, significance.** Not applicable and not attempted — no meta-analysis, no effect sizes, no variance, no significance treatment of any kind. The five tables are *qualitative*: Table 1 and Table 2 tabulate reward and policy-optimisation *formulas*; Table 3 compares dataset-construction *strategies*; Table 4 compares dynamic-reasoning methods on three columns — "Training-free?", "Baseline and Its Drawbacks", "Method Description"; Table 5 lists *prompt strings*. Not one table has a results column.
- **Adjudication.** None. Where surveyed papers disagree — most sharply, whether shortening reasoning is accuracy-neutral, mildly harmful, or sometimes *helpful* — the survey reports each claim as its author stated it and moves on. Claims are attributed, never weighed.
- **Quantitative content of the whole document.** Two numbers, by my count. The observation that LoRA adapts a model to short reasoning with "less than 1% of the parameters tuned" (Section 3.2.2), and the agentic-overthinking result imported from Cuadron et al. [29]: selecting solutions with lower overthinking scores improved performance by **30%** while reducing computational overhead by **43%**. Everything else is qualitative: "substantially reduces", "improves both accuracy and efficiency", "nearly lossless".

## Key findings, and the authors' own reading of them

**1. Overthinking is framed as a training artefact, not a bug.** The authors' sharpest observation is in Section 2.3: efficiency is hard to obtain *because the recipes that create reasoning ability reward length*. They cite DeepSeek-R1-Zero, where response length rises with training duration in step with benchmark score, and note that increasing length is routinely read as a proxy for successful reasoning training. Their conclusion is that "improving inference efficiency requires working against certain pretraining objectives". The motivating example is a model spending 19 seconds (QwQ-32B) or 42 seconds (DeepSeek-R1) on "which is larger, 0.9 or 0.11?", and the cost anchor is o1 at $60 per million generated tokens.

**2. The failure mode has two halves, and the paper mostly attends to one.** Overthinking is defined as wasted tokens, with a secondary clause that "in worse cases, excessive reasoning steps introduce errors or obscure logical clarity, leading to incorrect answers". So longer reasoning is presented as usually harmless-but-expensive and occasionally harmful. The authors' interest is squarely in the cost.

**3. There is an optimal reasoning length, and it is task- and model-dependent.** Two surveyed results carry this. *More is Less* / Length-filtered Vote [193] argues mathematically for an optimal CoT length set by model capability and task difficulty, with accuracy first rising and then falling through error accumulation. *Token Complexity* [83] finds a "universal trade-off between reasoning length and accuracy" — different prompt-based compression strategies land on the *same* accuracy-compression curve, each task has an intrinsic minimum token count, and existing prompt-based methods sit far from the information-theoretic limit. This second finding is the most useful thing in the survey for anyone reasoning about budget: it says that how you ask for brevity matters much less than how much brevity you ask for.

**4. Efficiency and self-checking trade off against each other.** Section 8.2 states that safety and efficiency "pull in opposite directions": self-correction, verification and adversarial robustness all consume tokens, so "prioritizing efficiency by minimizing token usage... may reduce the reasoning ability to self-reflect, verify its outputs, or defend against adversarial manipulations". This is the paper's only explicit statement of what stopping early costs, and it is asserted rather than measured.

**5. Models do not know when to give up.** MiP-Overthinking [43] is cited for the finding that when reasoning models are given questions with a **missing premise**, they loop and re-think rather than declaring the problem unanswerable, and that current training pushes long repetitive reasoning instead of recognising unsolvable problems and stopping. This is the single most on-Subject result in the paper, and it gets three sentences.

**6. Overthinking is worse in agentic settings than in single-chain settings.** Cuadron et al. [29] examined 4,018 agentic trajectories and named three failure patterns — **Analysis Paralysis**, **Rogue Actions**, and **Premature Disengagement** — where models prefer extended internal reasoning over environment interaction. Their overthinking score correlates strongly with lower task performance, and selecting low-overthinking solutions bought +30% performance at -43% compute. Note the shape of this: it names both stopping too late (analysis paralysis) and stopping too early (premature disengagement) as observed agent failures.

**7. Compression tolerance is asymmetric.** Quantisation preserves reasoning "remarkably well"; pruning "leads to severe degradation", disrupting multi-step logic. Smaller models suffer a "Small Model Learnability Gap" and struggle to absorb long CoT traces from larger ones.

**8. The authors decline to rank RL against SFT.** Section 8.2 concludes the comparison is "unclear", RL being creative but unstable and data-hungry, SFT being controllable but brittle off-distribution, with a combination speculated to be best. This is characteristic of the paper's stance throughout.

## The early-exit / stopping-criterion family (Section 4.2 — focus)

This is the part of the taxonomy the Subject cares about, and it is worth being precise about how much is here. Section 4.2 is roughly two pages. It contains Table 4 (seven methods, three qualitative columns), Figure 8 (two BoN variants), and four prose paragraphs. The authors' framing sentence is that "the key during inference is choosing the proper criterion to guide the reasoning strategy", and they split the criteria three ways.

### The signals, method by method

**Reward-guided — an external scorer judges a partial trace.**
- *Speculative Rejection* [165] — training-free. Runs Best-of-N with a deliberately large initial batch until memory is nearly exhausted, then periodically scores partial generations with a **reward model** and kills the low scorers. The halting signal is a reward model's estimate of a partial generation's eventual quality. It stops *branches*, not the run.
- *Reward-Guided Speculative Decoding (RSD)* [100] — training-free (given a PRM). A cheap draft model generates; a **Process Reward Model** scores intermediate outputs; high-scoring outputs are accepted directly, low-scoring ones are escalated to the large target model. It deliberately abandons speculative decoding's exact-match unbiasedness guarantee in exchange for compute — an escalation criterion rather than a stop criterion.

**Confidence / certainty-based — the model's own certainty is the trigger.**
- *Dynamic Parallel Tree Search (DPTS)* [38] — training-free. A "Search and Transition" mechanism uses **confidence-based criteria** to decide, per node, whether to keep expanding (Deep Seek) or abandon (Early Stop); "the system cuts off uncertain paths to save time".
- *FastMCTS* [89] — training-free. Prioritises **high-confidence traces** for deeper expansion and scales tree expansion with problem complexity. Its actual purpose is data synthesis, not serving; it is a sampler, and its inclusion here stretches the category.
- *Certaindex / Dynasor* [50] — training-free. **Certaindex** is a scalar measure of reasoning progress computed from **semantic entropy**, **reward-model scores**, or a combination. The stated semantics are the important part: "a higher certaindex indicates that further reasoning steps are unlikely to change the final answer, allowing early termination". Note this is a *stability* claim (the answer has stopped moving), not a *correctness* claim. Dynasor is the serving system that reallocates the freed compute to harder queries — the interesting design being that it treats stopping as a **scheduling** decision across a queue rather than a per-request one.
- *Dynasor-CoT* [51] — training-free. **This is the entire treatment of the reasoning-probing-exit paradigm**: one sentence, "Dynasor-CoT [51] uses a probing scheme to exit early if the model is confident enough." What the probe is, where it is injected, what it asks, how its output is read, and how the confidence threshold is chosen are all absent. The brief asks how the probe threshold is set; the survey does not say, for this or for any other method in the section.
- *Self-Calib* [70] — trained (self-calibration). Confidence-driven adaptive test-time scaling, including an **early-stopping rule for Best-of-N** and confidence-calibrated self-consistency.
- *CISC* [170] — training-free. **Model-derived confidence scores** weight a majority vote, reaching the same answer with substantially fewer samples. This stops *sampling*, not reasoning.
- *Length-filtered Vote / More is Less* [193] — training-free. Groups sampled answers by CoT length and picks the group with lowest **prediction uncertainty**, discarding chains that are too short or too long. Length itself is treated as a proxy signal for reliability.

**Consistency-based — agreement across parallel samples is the signal.**
- *Self-Truncation Best-of-N (ST-BoN)* [188] — training-free. Generates N candidates only part-way, embeds the partial traces (a "Chain-of-Embedding"), computes **pairwise consistency of latent embeddings**, and truncates all but the most mutually-consistent path. The stated premise is "the closer a sample is to others, the more likely its path will lead to the correct answer". Its selling point against Speculative Rejection is that it needs **no reward model** — the signal is internal geometry, not an external judge.

**Summarisation-based — not stopping, but bounding.**
- *LightThinker* [231] — **trained**. Learns *when and how* to compress intermediate thoughts into "gist tokens", with a sparse attention mask at inference. This is the one method in the section where the decision of when to cut is itself learned rather than thresholded.
- *InftyThink* [209] — **trained**. Interleaves reasoning with summarisation and discards everything but the latest summary, giving unbounded reasoning depth within a fixed context window. Notably this is the opposite move to early exit: it makes *not stopping* affordable.

### Trained versus training-free

The survey's own Table 4 answers this cleanly, and it is the one column where it commits to a fact: everything in the explicit-criteria branch — Speculative Rejection, RSD, DPTS, Certaindex/Dynasor, FastMCTS, Length-filtered Vote, ST-BoN — is marked **training-free**. Only the summarisation methods, LightThinker and InftyThink, are marked as requiring training. Self-Calib and Self-Ref require fine-tuning but are not in the table. So the field as surveyed is dominated by **threshold-on-an-existing-signal** methods that can be bolted onto a frozen model, and there is almost nothing here in the shape of a *learned stopping controller*. The nearest thing to one appears outside the taxonomy entirely, in Section 8.2: **Meta-Reasoner** [164], which runs a contextual multi-armed bandit over per-step "progress reports" to choose a guidance strategy and discard unpromising avenues early. That is the closest the paper comes to describing a learned progress judge, and it appears in the discussion as a way to *improve* reasoning rather than as a stopping criterion.

### Evidence, thresholds, and trade-offs — what is missing

Three absences matter more than anything present.

1. **No evidence is reported for any method in this section.** Not one accuracy figure, token count, latency number, or baseline comparison. Table 4's three columns are Training-free?, the baseline's drawbacks, and a description. The support for each method is its own authors' summary claim, restated.
2. **No threshold is ever specified or discussed.** Every method here reduces to comparing a scalar against a cut-off — reward score, certaindex, embedding consistency, vote confidence. How any of those cut-offs is chosen, whether it transfers across models, tasks or difficulty levels, and how sensitive the accuracy-token trade-off is to it, is never raised. This is the survey's largest analytical gap relative to its own subject matter.
3. **The cost of stopping too early versus too late is not characterised in this section.** The asymmetry is discussed only elsewhere and only qualitatively — the safety/efficiency tension in Section 8.2, the optimal-length results in Sections 5.1 and 7, and Premature Disengagement in the agentic study. Section 4.2 itself treats early exit as free money.

Also worth recording: the signals in use are **weaker than they look**. Certaindex is semantic entropy or a reward score; ST-BoN is embedding proximity between samples; CISC is verbalised or logit confidence. Every one of them measures **agreement or stability**, and the survey nowhere asks whether those track correctness — the calibration question the Subject cares about is not posed. And there is no method here whose signal is drawn from the *trajectory* in the agentic sense (no state change, repeated actions, a tool returning the same result twice); attention or trajectory features appear only as the internal-embedding geometry of ST-BoN.

## How much of this bears on stopping an agentic loop

Very little, and the paper is honest enough about its own framing that this is not a hidden flaw so much as a scope boundary. The unit of analysis throughout Sections 3-6 is a **single chain of thought, or a fan of parallel samples of one** — the question is always how many tokens are spent between a prompt and one final answer. What gets "stopped" in Section 4.2 is a sampling branch, a tree node, or a decode loop, on a task (a maths problem) that is stateless, verifiable in one shot, and free to abandon and retry. An agent loop is none of those things: its steps have external effects, its budget is measured in tool calls and wall-clock as well as tokens, and abandoning it has a cost that a discarded BoN branch does not.

Agentic material appears in exactly three places:
- **Section 7, "Evaluating Overthinking"** — the 4,018-trajectory study [29] with Analysis Paralysis / Rogue Actions / Premature Disengagement and the overthinking score. This is real, on-Subject evidence about agent loops, and it is imported wholesale in five sentences.
- **Section 8.2, "Efficient LLMs for Agentic AI"** — a paragraph naming planning-tree merging [69], hierarchical memory management [68], CoA [139], and DOWN [42], which triggers multi-agent debate only when an agent's initial confidence is low. Confidence-gated escalation, again, rather than stopping.
- **Section 5.2 routing** — query-level triage: Self-Ref [25] fine-tunes uncertainty-specialised tokens so a model can decide to hand off to a stronger model, and Confident-or-Seek-Stronger [24] builds calibrated data for that decision. This is the survey's closest analogue to *handing off*, but the decision is made **before** work starts, from the prompt, not from a stalled trajectory.

The transferable ideas, then, are conceptual rather than operational: that a stability signal ("further steps are unlikely to change the answer") can license termination; that stopping is better modelled as a scheduling decision across a queue than as a per-request one (Dynasor); that consistency across parallel attempts is a cheap proxy for confidence when no verifier exists (ST-BoN); and that an optimum exists and both sides of it are costly. None of them arrives with a threshold, a calibration curve, or an agentic evaluation.

## Open questions the paper itself raises

The authors are sparing with these; most are single sentences at the end of a subsection.

- **What criterion should decide a prompt's attributes?** Section 5.2 opens by naming this as "the key question" for routing — how to judge difficulty before committing compute — and then does not answer it. Claude 3.7 Sonnet is cited precisely because its routing criterion is undisclosed, which the authors flag as an open box rather than a solved problem.
- **RL or SFT for efficient reasoning?** Explicitly left "unclear", with a combination proposed as a guess.
- **How to balance safety against efficiency?** Named as "a challenging yet crucial area of investigation", with the no-free-lunch framing and no proposal.
- **How far below the information-theoretic compression limit are we?** Inherited from [83]: existing prompt-based compression "falls far short" of the computed limits, "indicating significant room for improvement".
- **Why can small models not absorb long CoT?** The Small Model Learnability Gap is presented as an open obstacle; compression alone is called "insufficient" because compressed models lose instruction-following.
- **Whether efficient reasoning generalises beyond maths and code.** Implied rather than stated: essentially every surveyed evaluation is a maths or coding benchmark, and Sys2Bench is cited for the finding that no single inference-time technique wins across reasoning categories.

Questions the paper does **not** raise, which its own material invites: whether the confidence signals being thresholded are calibrated; how any threshold should be chosen or transferred; what early exit costs on the hard tail of a distribution; and whether any of this survives contact with a loop that has side effects.

## Appreciation

**Mechanism — what this paper genuinely gives you.** A clean, defensible partition of an unruly literature by *point of intervention*: weights, output, input. That axis is the paper's real intellectual contribution, and it is a good one, because it maps onto what a practitioner can actually change. Within the branch the Subject cares about, the survey supplies a usable vocabulary of halting signals — external reward on a partial trace, semantic entropy / certainty, cross-sample embedding consistency, vote confidence, length-as-proxy — plus one genuinely clarifying semantic distinction that it states almost in passing: certainty-based exit licenses stopping because **the answer has stopped changing**, not because it is right. It also supplies the Dynasor reframing of stopping as queue-level scheduling, the Table 4 training-free column, and, in Figure 3, an exhaustive index of about 160 methods that is a better reading list than most literature searches would produce. Sections 2.3 and 8.2 contribute two arguments that are the authors' own: that verbosity is *manufactured* by length-correlated training signals, and that token thrift and self-verification are in direct tension.

**Magnitude — what it does not give you.** Almost no quantities at all. Two numbers in twenty pages, both borrowed. No results table, no common axis, no reproduction, no ranking, no adjudication of conflicting claims, no error bars, no thresholds. Every method's efficacy is reported at the level of "substantially reduces" or "improves both accuracy and efficiency", in the voice of the method's own authors. So the mechanism inventory is trustworthy and the magnitude claims are not evidence at all — they are pointers to evidence held elsewhere. Reading this paper tells you accurately *what kinds of stopping signal exist*; it tells you nothing reliable about *how well any of them works*, and it would be a mistake to carry any of its efficiency claims forward as findings rather than as leads.

The gap between the two is wide enough to be worth a warning. A reader skimming Section 4.2 comes away with the impression that early exit is a solved, cheap, training-free win. Nothing in the section supports that impression, and Sections 7 and 8.2 quietly contradict it.

## How it could serve a harness-design effort — limitations and major concerns

**Where it helps.**
- As a **map and reading list** it is efficient. Figure 3's dynamic-reasoning leaf is, in effect, a pre-assembled bibliography of about sixty stopping and adaptive-compute methods, and the GitHub repository keeps it current. For the collect phase of a review this is its highest-value content, and it is content the prose does not duplicate.
- The **signal taxonomy** (reward / certainty / consistency / summarisation) is a reasonable set of buckets for classifying any halting rule, including ones designed for loops rather than chains.
- The **training-free column** of Table 4 is directly relevant to a harness that cannot fine-tune: it says most of this family is bolt-on.
- Three specific framings are portable: stopping as scheduling across concurrent work; stability-of-answer as a termination licence; and the observation that a system trained to be thorough will resist being told to stop.
- The **agentic overthinking vocabulary** — Analysis Paralysis, Rogue Actions, Premature Disengagement — is a usable set of named failure modes for a loop, though it belongs to [29] and not to this paper.

**Limitations and concerns, in order of severity.**
1. **Domain mismatch with agentic stopping.** The surveyed unit is a stateless, one-shot-verifiable maths problem where abandoning a branch costs nothing. A harness stopping a loop faces side effects, partial progress, and irreversible actions. Almost none of the surveyed criteria have been evaluated in that setting, and the survey never flags the gap.
2. **No thresholds anywhere.** Every method reduces to a scalar-versus-cut-off comparison and not one cut-off, selection procedure, or sensitivity analysis is reported. A harness designer cannot implement anything from this paper without going to the primary sources.
3. **The calibration question is skipped entirely.** The survey thresholds on model confidence throughout without once asking whether that confidence tracks correctness. Given that its own cited MiP-Overthinking result shows models failing to recognise unanswerable problems, the omission is significant.
4. **Asymmetric cost is not analysed.** Stopping too late is priced (tokens, dollars, latency). Stopping too early is mentioned only as a safety trade-off and as one of three agent failure patterns, never measured. For a harness, the early-stop error is the expensive one, and this paper will not help estimate it.
5. **No quality filter on sources.** Peer-reviewed work and same-month preprints are cited identically, claims are relayed unexamined, and the taxonomy grew across versions by accretion. Roughly sixty methods in the branch of interest are names with no description; anything drawn from the figure is an unverified pointer.
6. **Padding.** Section 8.1 (autonomous driving, embodied AI, healthcare, recommender systems) is four paragraphs of generic benefit-assertion with almost no citations and no efficiency measurements; the conclusion adds algorithmic trading, which appears nowhere in the body. This is the clearest instance of restatement over signal.
7. **Self-citation.** Self-REF [25], the uncertainty-token routing method in Section 5.2, is co-authored by two of this survey's authors including the senior author. It is presented without that being noted. It is one instance and the treatment is not obviously inflated, but it should be recorded.
8. **Version instability.** What is true of v4 (21 Aug 2025) is not true of v1. Any citation of this survey should pin the version.

**Bottom line for a harness effort.** Use it as an index, not as evidence. It is the fastest route to the names in the early-exit literature and it supplies a decent vocabulary for the signals; it supplies no numbers, no thresholds, no calibration, and no agentic evaluation, and the methods it indexes were built to shorten a chain of thought rather than to stop a loop.

## Five citations worth chasing next

1. **[29] Cuadron et al., "The Danger of Overthinking: Examining the Reasoning-Action Dilemma in Agentic Tasks" (2025).** The only genuinely agentic evidence in the survey — 4,018 trajectories, an overthinking score correlated with task failure, and the Analysis Paralysis / Rogue Actions / Premature Disengagement taxonomy, with +30% performance and -43% compute from low-overthinking selection. Closest thing in the whole reference list to the Subject.
2. **[51] Fu et al., "Reasoning without Self-Doubt: More Efficient Chain-of-Thought through Certainty Probing" (ICLR 2025 Workshop on Foundation Models in the Wild).** This is Dynasor-CoT, the reasoning-probing-exit method the survey compresses into one sentence. It is where the probe design and its threshold must actually be documented. Pair it with **[50] Fu et al., "Efficiently Serving LLM Reasoning Programs with Certaindex"** for the certainty metric (semantic entropy / reward score) and the scheduling system built on it.
3. **[43] Fan, Li, Sun, Zhou, "Missing Premise Exacerbates Overthinking: Are Reasoning Models Losing Critical Thinking Skill?" (arXiv:2504.06514).** Directly on abstention: models given under-specified problems loop instead of declaring them unanswerable. The failure a stopping criterion most needs to catch.
4. **[188] Wang et al., "Sampling-Efficient Test-Time Scaling: Self-Estimating the Best-of-N Sampling in Early Decoding" (arXiv:2503.01422).** ST-BoN — halting on cross-sample latent-embedding consistency with no reward model and no training. The cheapest signal in the family, and the one most plausibly portable to a setting with no verifier.
5. **[83] Lee, Che, Peng, "How Well do LLMs Compress Their Own Chain-of-Thought? A Token Complexity Approach" (arXiv:2503.01141).** The accuracy-versus-token trade-off the survey gestures at but never plots: a universal compression curve, per-task intrinsic token complexity, and information-theoretic limits showing current methods fall far short.

*Runner-up worth noting:* **[117] Liu and Wang, "Answer Convergence as a Signal for Early Stopping in Reasoning" (2025)** — the answer-convergence halting signal named in the brief. It appears in this survey **only** in the taxonomy figure and the bibliography, with no description whatsoever, so the survey establishes that it exists and nothing more.
