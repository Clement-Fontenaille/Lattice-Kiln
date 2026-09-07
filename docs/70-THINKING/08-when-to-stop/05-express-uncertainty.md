# Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs

## Density

**Density: HIGH** — Almost every section carries a measured number rather than restatement, and the whole paper is about the question of whether a model's stated confidence tracks its own correctness, which sits directly on the Subject; the main repetition is that §6 and Appendix D restate §5's findings in prose, and the appendix tables mostly deepen rather than duplicate.

## Name, keywords, year, venue

Miao Xiong, Zhiyuan Hu, Xinyang Lu, Yifei Li, Jie Fu, Junxian He, Bryan Hooi. "Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs." ICLR 2024 (peer-reviewed). arXiv:2306.13063; the version I read is v2, dated 17 March 2024, retrieved as arXiv HTML.

My keywords: verbalized confidence, black-box uncertainty estimation, confidence elicitation, calibration (ECE), failure prediction (AUROC/AUPRC), self-consistency, ensemble aggregation, overconfidence, round-number bias, Top-K prompting, self-probing.

## Approach

The paper attacks confidence elicitation in the setting where you have no logits, no embeddings, and no ability to fine-tune — that is, a commercial chat API. The authors argue that this setting is now the common one, and that token likelihood is in any case the wrong quantity, because it measures uncertainty over the next token rather than over the semantic claim being made (their example: "Chocolate milk comes from brown cows" has high per-token likelihood and is false).

Their contribution is organisational as much as empirical. They decompose every black-box confidence method they can find into three composable components, and then benchmark combinations of them:

1. **Prompting strategy** — how you ask for the confidence. Five options: *Vanilla* (answer plus a confidence number), *CoT* (zero-shot chain of thought, then answer plus confidence), *Self-Probing* (the answer is generated in one chat session; a second, independent session is shown the question and the answer and asked "How likely is the above answer to be correct?"), *Multi-Step* (break the problem into K steps, give a confidence C_i per step, and take the product ∏C_i as the overall confidence), and *Top-K* (give your K best guesses with a probability for each, from Tian et al. 2023). Every prompt appends the gloss "Note: The confidence indicates how likely you think your answer is true."
2. **Sampling strategy** — how you get M responses to the same question. Three options: *Self-Random* (same prompt M times at temperature 0.7), *Prompting* (paraphrase the question M ways), and *Misleading* (append a hint such as "Hint: I vaguely remember the answer is X", on the human analogy that a confident person holds their answer under contrary suggestion and an unsure person wavers).
3. **Aggregation strategy** — how M responses become one confidence. Three options: *Consistency* (fraction of the M samples agreeing with the chosen answer), *Avg-Conf* (consistency weighted by each sample's verbalized confidence: Σ 1{Ŷ_i = Ỹ}·C_i / Σ C_i), and *Pair-Rank* (for Top-K outputs only: treat the ordering within each Top-K list as pairwise comparisons, and fit a categorical distribution P by MLE under P(S_u ≻ S_v) = P(S_u)/(P(S_u)+P(S_v)); this is the paper's Proposition 3.1, proved in Appendix A by conditioning on the first position at which either answer is drawn, and solved by a softmax reparameterisation plus gradient descent).

The framing point is that existing named methods are cells in this grid — Top-K as published is (Top-K prompt, self-random with M=1, Avg-Conf), and self-consistency is (CoT, self-random, Consistency) — so the grid lets them ask which component actually carries the improvement.

Note the grid is not exhaustively run. They vary one axis at a time against a fixed setting of the others: five prompts at M=1 on two models (Fig. 3), three sampling strategies at M=5 with prompt and aggregator fixed to CoT + Consistency (Table 3), three aggregators on GPT-4 with prompt and sampling fixed to Top-K + Self-Random (Table 4), and a set of six named combinations in the appendix (Table 13). So the reported "combinations" are a sparse slice of 5×3×3, not the full 45.

## Models targeted and benchmarks used

Five models, chosen to span capability: **Vicuna 13B**, **GPT-3 175B**, **GPT-3.5-turbo**, **GPT-4**, and **LLaMA 2 70B Chat**. GPT-3 is used as the white-box comparison backbone because it exposes token probabilities.

Eight datasets in five task families:
- Commonsense: StrategyQA, Sports Understanding (both BigBench)
- Arithmetic: GSM8K, SVAMP
- Symbolic: Date Understanding, Object Counting (BigBench)
- Professional knowledge: Professional Law (MMLU)
- Ethical knowledge: Business Ethics (MMLU)

All are fixed-form or free-form QA with a single ground-truth answer; the paper is explicit that summarisation and open-ended QA are out of scope.

## Author incentive

Five of the seven authors are at the National University of Singapore, with one at EPFL and two at HKUST (Jie Fu, Junxian He); Bryan Hooi and Junxian He are the equal advisors. Funding is Singapore's Ministry of Education Academic Research Fund Tier 1 (FY2023) — public academic money, no industrial sponsor named. There is no product being sold here and no proprietary model being defended; the models evaluated are other people's. The visible stake is a methodological one: the paper positions itself against a concurrent paper (Tian et al. 2023) by claiming a broader method space and a wider model range, and it proposes the framework and the Pair-Rank aggregator as its own artefacts. The first author's prior work on calibration and trustworthiness (Xiong et al. 2022, 2023; Deng et al. 2023) is cited, which is a normal continuity of research agenda rather than a conflict. Code is released publicly.

## Measurement methodology (brushed)

The dependent variables are four, computed over a dataset of questions where each question yields (predicted answer, confidence score) and correctness is scored against ground truth:
- **ECE** (Expected Calibration Error) for calibration — the bin-wise gap between stated confidence and observed accuracy.
- **AUROC** for failure prediction — can the confidence score separate correct from incorrect answers.
- **AUPRC-Positive** and **AUPRC-Negative**, added explicitly because accuracy varies a great deal across these datasets and a raw AUROC hides class imbalance; PR-P asks whether correct samples are identified, PR-N whether incorrect ones are.

The paper is careful about one thing that matters: it treats calibration and failure prediction as *orthogonal* tasks, and it demonstrates why. Their Table 2 caption fixes thresholds for "significant deviation from ideal" borrowed from BIG-bench (Srivastava et al. 2023): ECE > 0.25, or any of AUROC / AUPRC-P / AUPRC-N < 0.6.

What is controlled: one axis varied at a time with the other two pinned, as described above. M = 5 responses throughout the main sampling and aggregation experiments; temperature 0.7 for Self-Random, following Wang et al. 2022; the Top-K candidate set fixed at K = 4, justified in B.7 as the efficiency/performance balance.

Significance is treated lightly. Most tables are single-run point estimates with no confidence intervals, no seeds reported, and no statistical test. The two exceptions are Table 4, which reports a variance alongside the mean over datasets, and Figure 7, where for each number of misleading hints they resample the query set five times and plot mean ± variance for ECE and AUROC. N per dataset is not stated in the version I retrieved — the implementation-details paragraph (E.4) is truncated in the arXiv HTML mid-sentence after the temperature setting — so the per-cell sample size, and hence the noise floor on differences of a few points, is not recoverable from the text. Given that many of the between-strategy gaps the paper discusses are 2–5 points of ECE or AUROC, this is a real gap in the evidence.

There is also a subtlety in the comparison that the authors handle honestly: the prompting strategies change the model's *accuracy* as well as its confidence, so a lower ECE can come entirely from accuracy rising to meet an unchanged confidence distribution. They say so themselves and give the decisive example (see below).

## Key findings

### 1. Verbalized confidence is badly overconfident, and the shape of the failure is human-like

Table 2 gives vanilla verbalized confidence across five models and eight datasets. Average ECE by model: GPT-3 **0.520**, Vicuna 13B **0.461**, LLaMA 2 70B **0.436**, GPT-3.5 **0.377**, GPT-4 **0.180**. The worst single cell is GPT-3 on GSM8K at **0.827** — the model states roughly 90% confidence on a task where it is right a small fraction of the time. Date Understanding for GPT-3 is 0.821. The authors' own summary is that GPT-3, GPT-3.5 and Vicuna all exceed the BIG-bench threshold with average ECE above 0.377 and are therefore "poorly calibrated".

The distributional signature (Figure 2, expanded in Figure 5 over four models and five datasets) is the part of the paper I found most striking: verbalized confidences land almost entirely in the **80%–100%** band and are almost always **multiples of 5**. The authors read this as imitation — the models are reproducing how humans talk about confidence in the training corpus, citing Zhou et al. 2023 for the same pattern in the corpus. Round-number bias and ceiling-clustering are therefore both confirmed, and they are confirmed as a property of the *expression*, not of the underlying epistemic state.

Insensitivity to difficulty follows from the same figures: within the 100%-confidence bar there is a large mass of incorrect predictions, and the confidence distribution barely moves between easy and hard datasets even though accuracy moves a great deal.

### 2. Failure prediction is near chance, and it is a separate problem from calibration

This is the finding that matters most for the Subject. Average AUROC for vanilla verbalized confidence: GPT-3 **51.3**, Vicuna **52.5**, GPT-3.5 **55.1**, LLaMA 2 **56.4**, GPT-4 **62.7**. Random guessing is 50. The improvement from GPT-3 to GPT-4 is about 22.2% relative, so scale does help, but GPT-4's 62.7 is still, in the authors' word, "suboptimal". AUPRC-Negative — the ability to identify the *wrong* answers, which is the quantity an abstention mechanism needs — is worst exactly where accuracy is highest: GPT-4 averages **34.2** PR-N, below every weaker model, because when accuracy is high the incorrect class is small and hard to isolate.

The decisive demonstration that ECE and AUROC come apart: with CoT prompting on GSM8K, **GPT-4 reaches 93.6% accuracy and a near-optimal ECE of 0.064 by assigning 100% confidence to every single sample**. The calibration number looks excellent, and the confidence carries literally zero information about which answers are wrong. The authors state this explicitly and repeat the warning in Appendix D.2: a good ECE does not imply the confidence represents correctness, so ECE must always be read alongside AUROC and the confidence distribution plot.

### 3. Human-inspired prompting reduces ECE, mostly by raising accuracy, and helps failure prediction only modestly

Across five prompting strategies on GPT-3.5 and GPT-4 over five datasets (Figure 3), the human-inspired prompts consistently beat vanilla on accuracy and ECE, with only modest AUROC gains. **No single prompt wins everywhere**: Self-Probing is the most consistent gain on GPT-4, Top-K is the best on GPT-3.5. Gains diminish as model capacity rises.

The authors' own reading, stated in §5.2 and again in D.3, is deflationary about their own method: the ECE reduction is "largely due to these prompt strategies enhancing the model's accuracy, which narrows the gap between average confidence and actual accuracy, rather than a significant boost in their ability to differentiate between correct and incorrect samples". The confidence output distribution stays in the 80–100% band throughout.

Multi-Step (Table 9, GPT-3.5) is genuinely mixed and sometimes harmful: on GSM8K it lowers accuracy 80.3 → 76.2 and worsens ECE 0.10 → 0.22 while nudging AUROC 55 → 60; on Date Understanding it costs 10 accuracy points (73.2 → 63.6) but lifts AUROC 57 → 72. Multiplying per-step confidences buys discrimination at the cost of accuracy and calibration.

A negative result worth recording (B.2): persona prompts do essentially nothing. Prefixing "You are a confident GPT" versus "You are a cautious GPT" to the CoT prompt changes accuracy, ECE and AUROC only minimally.

### 4. Variance across multiple responses is where the real failure-detection signal lives

This is the largest effect in the paper. With prompt and aggregator fixed to CoT + Consistency and M = 5 (Table 3, GPT-3.5), moving from a single verbalized confidence to consistency over five samples takes average ECE from 25.0 to **18.7** (Self-Random) or **17.3** (Misleading), and average AUROC from 56.4 to **73.0** (Self-Random) or 69.6 (Misleading). On GSM8K specifically, AUROC goes from **54.8 — indistinguishable from chance — to 92.7**. Arithmetic is where the gain concentrates, which fits the mechanism: sampling approximates the model's answer distribution, and on arithmetic wrong answers scatter while right ones agree.

The three sampling strategies differ little from each other; the authors pick Self-Random for simplicity. Within the Misleading strategy, the *weak* hint phrasings ("I vaguely remember the answer is…") outperform strong claims and external-source claims (B.6, Table 12), because a confidently phrased misleading hint can actually flip a correct answer given with moderate confidence, contaminating the signal.

Returns to M saturate: sweeping M = 1 to 13 (Figure 7) improves ECE and AUROC with clearly marginal gains at the top end, against cost linear in M. The Top-K candidate count K behaves similarly — larger K improves AUROC and reduces its variance, while the ECE-optimal K is dataset-dependent; they settle on K = 4.

### 5. Verbalized confidence is worth keeping *inside* the aggregator

Aggregators on GPT-4 with Top-K + Self-Random fixed (Table 4): **Pair-Rank gives the best calibration** — average ECE **6.90 ± 0.2** against Consistency 12.0 and Avg-Conf 14.8, with individual cells as low as 0.028 (Sports) and 0.035 (StrategyQA). **Avg-Conf is the better failure predictor**, beating the others on AUROC in five of six datasets, though its *average* AUROC (66.9 ± 1.7) ties Consistency and trails Pair-Rank (67.6) because one cell collapses: Avg-Conf on GSM8K scores **41.0 AUROC, below chance**. That instability is visible in its variance and is not discussed in the text.

The mechanistic explanation the authors give is convincing and worth keeping. Consistency alone at M = 5 can only emit six values (0, 0.2, … 1.0), which is too coarse to calibrate well; verbalized confidence, imprecise as it is, still tracks the model's uncertainty *tendency* and supplies fine-grained values to break ties. So the two signals are complementary, and combining them beats either — which is the paper's titular answer in its most positive form: the verbalized number is not useless, it is just not usable alone.

The appendix bake-off (Table 13, GPT-3.5, five datasets) makes the winner concrete. Average across datasets: Top-K M=1 gives ECE 24.6 / AUROC 65.9; CoT M=1 gives 25.0 / 56.4; Self-Random + Consistency M=5 gives 18.7 / 73.0; **Self-Random + Avg-Conf M=5 gives 14.8 / 74.5 / PR-P 80.6 / PR-N 61.9**, the best on three of four metrics; Misleading + Avg-Conf edges it on ECE at 14.2 but is worse on the rest. **The combination the paper recommends is Top-K prompt + Self-Random sampling + Avg-Conf or Pair-Rank aggregation** — Pair-Rank when you need the confidence value itself (expected-risk computations), Avg-Conf when you need failure detection (factual error detection). Top-K is preferred over the equally strong Self-Probing on GPT-4 purely on cost, since Self-Probing needs two inference passes.

### 6. White-box access helps less than you would expect

Against three token-probability methods on GPT-3 (sequence probability, length-normalised sequence probability, key-token probability), the white-box methods do win, but the whole field sits in the same narrow band: the headline comparison is **0.522 to 0.605 AUROC**, and B.1 notes that nearly all methods on all datasets fall between 0.5 and 0.6. Length-normalised and key-token probability are the best of them. The authors' conclusion is that uncertainty estimation in LLMs is unresolved regardless of access level, and that logit-based signals miss semantic uncertainty by construction.

### 7. Hard-knowledge tasks defeat everything

Professional Law is the consistent worst case across every table. Under vanilla verbalized confidence GPT-4 gets 60.9 AUROC there; the best ensemble methods reach only ~65. The authors' own summary answer to "are current algorithms satisfactory?" is "Not quite" — best-case ECE can reach 0.028, but failure prediction remains poor precisely on the tasks that need professional knowledge.

## Answers to the specific questions the brief raised

- **Confidence in the answer vs. in the reasoning.** Predominantly the answer. The scored target throughout is final-answer correctness. Two designs touch reasoning: Multi-Step elicits a confidence per reasoning step and multiplies them, and Self-Probing scores an answer from a fresh session as if it were someone else's. Neither is evaluated against step-level ground truth — there is no per-step correctness label anywhere — so the paper never measures whether a model can tell which *step* went wrong.
- **Is elicited confidence actionable for selective prediction or abstention?** **Not demonstrated.** Selective generation is named as a motivation in the introduction (citing Ren et al. 2022) and never operationalised. There is no abstention experiment, no risk-coverage curve, no threshold study, no accuracy-under-rejection number. AUPRC-Negative is the closest proxy, and it is the metric on which the strongest model does worst (GPT-4 at 34.2 for vanilla). The paper's own practitioner guidance in D.2 says dependence on this confidence for real-world applications "requires careful checking".
- **Model-dependent vs strategy-dependent.** Both, and they interact. Model capacity sets the ceiling — the ECE ladder from GPT-3 (0.520) to GPT-4 (0.180) and the AUROC ladder from 51.3 to 62.7 are monotone in capability, and prompting gains shrink as the model gets better. But the biggest single intervention in the paper is strategic, not model-based: sampling plus aggregation moves GSM8K AUROC by nearly 38 points on a fixed model. Which *prompt* wins is model-dependent (Top-K on GPT-3.5, Self-Probing on GPT-4), while the sampling-and-aggregation finding holds across the models tested. So: prompt choice is model-dependent, the ensemble principle is not.

## Open questions the paper itself raises

1. **Scope of task.** They restrict to QA with a unique ground-truth answer, and explicitly leave summarisation and open-ended generation to future work. Consistency-based aggregation depends on exact answer matching, so it does not obviously transfer to open-ended output.
2. **Hybrid white/black-box.** They suggest combining black-box methods with whatever limited internals are available (e.g. logits exposed by some APIs) as a promising direction.
3. **Why verbalized confidence is bad at all.** They hypothesise that it is inherited inaccuracy from human uncertainty expressions in the training data (citing Garthwaite et al. 2005 on humans exaggerating priors), and treat it as an open research gap whether models could learn to do better.
4. **Whether sampling fails because of poor internal calibration or too few samples.** D.3 offers both as candidate explanations for cases where consistency does not help, without separating them.
5. **Professional-knowledge tasks** are flagged as unsolved by any method examined.

## Appreciation

**MECHANISM.** The three-axis decomposition is the durable contribution, and it is genuinely clarifying: it turns a scatter of named methods into cells of a grid and lets you ask which component does the work. The answer it produces — that the *inter-sample variance* carries most of the failure-detection signal while the *verbalized number* carries fine-grained value information useful only as a weighting term — is a clean mechanistic result, and the coarse-granularity argument for why Consistency alone calibrates badly (six possible values at M = 5) is the kind of explanation that predicts new cases. The GPT-4/GSM8K example, where perfect-looking ECE arises from assigning 100% to everything, is a small but permanently useful demonstration that calibration and discrimination are different properties; I would keep that example even if every number in the paper aged out. Pair-Rank is a real piece of method design with a proof behind it, extracting a distribution from ranking information on the argument that the model's *ordering* is more trustworthy than its stated numbers.

**MAGNITUDE.** The magnitudes are what date fastest and should be held loosely. Absolute numbers are tied to models from 2023 (GPT-3, GPT-3.5-turbo, Vicuna 13B) and to eight fairly small academic QA sets, with no N reported, single runs, and no significance testing, so differences under ~5 points should not be relied on. What is likely to be robust is the *ordering and rough scale* of the effects: near-chance failure prediction from a bare verbalized number (AUROC in the 50s), a very large gain from sampling on arithmetic-style tasks where wrong answers scatter, a modest gain from prompt engineering, and a narrow white-box/black-box gap. The 80–100% clustering and multiples-of-5 signature is an artefact of a training distribution and could shift with post-training practice; it should be re-measured rather than assumed. The single most transferable magnitude claim is the negative one: no combination tested reaches a level where the confidence could be trusted unexamined.

## How it could serve a harness-design effort; limitations; major concerns

**What it supports.** For a system that must decide whether its current attempt succeeded, this paper is close to a direct instruction not to ask the model. A bare "how confident are you?" gives you a number in the 80–100% band regardless of whether the work is right, with discrimination near a coin flip; a harness that gates retry, escalation or hand-off on such a number is gating on noise. What the paper *does* support is treating **agreement across independently sampled attempts** as the primary intrinsic signal: it is black-box, needs no internals, and on the task family where answers are checkable it moved AUROC from 54.8 to 92.7. The design consequence is concrete — budget for M ≈ 5 parallel attempts rather than one attempt plus a self-assessment, expect saturating returns past that, and use the stated confidence only as a weight inside the aggregation, never as the decision variable. Pair-Rank versus Avg-Conf gives a principled split by purpose: use calibration-oriented aggregation if you want to compute expected risk, discrimination-oriented aggregation if you want to catch failures. The instrumentation advice generalises too: never report a single calibration number, always pair it with a discrimination metric and the confidence histogram, or you will ship a system whose ECE looks fine because it says 100% to everything.

**Limitations that bound the transfer.** The setting is single-turn QA with one correct answer, scored by exact match. An agent loop is multi-turn, its "answer" is a trajectory of actions, and there is often no unique ground truth — so *Consistency*, the mechanism that carries most of the signal here, has no obvious definition. Sampling M attempts is cheap for a one-shot QA and expensive for a long agentic run, and the paper's linear-cost caveat becomes a much harder constraint there. Nothing in the paper addresses stopping, progress, or stall detection over time; confidence is measured once, on a finished answer, against a static label. And self-assessment of an already-produced answer (Self-Probing) is the only "critique" variant tested, evaluated only as a confidence number, not as an error localisation.

**Major concerns.** (a) The absent N and single-run design mean many of the finer comparisons — which prompt ranks first, the 2–3 point ECE differences between aggregators — are not really supported by the evidence presented, even though the paper's *large* effects clearly are. (b) The grid is described as a framework but explored one axis at a time, so interactions are mostly untested; the recommended combination (Top-K + Self-Random + Avg-Conf/Pair-Rank) is assembled from separate one-axis winners rather than selected by running the grid. (c) Avg-Conf's below-chance 41.0 AUROC on GSM8K sits inside a table whose caption calls Avg-Conf the AUROC winner, and the collapse is not explained; a harness that adopted the recommendation would inherit an unexplained failure mode on exactly the task family where the ensemble signal is otherwise strongest. (d) The selective-prediction claim is motivational only, and a reader in a hurry could easily carry away an actionability claim the paper does not make. (e) Two arithmetic/consistency problems I found by recomputing the tables. In Table 4 the Avg-Conf ECE row (10.0, 14.4, 7.70, 10.6, 5.90, 20.2) averages to 11.5, but the reported mean is 14.8 — the Consistency row (12.0) and the Pair-Rank row (6.90) both reproduce correctly, so this cell appears wrong, and it happens to be the number that makes Avg-Conf look worse than Consistency on calibration. And the Top-K (M=1) baseline is reported twice with different values: Table 3 gives GSM8K ECE 19.6 and DateUnd 26.1, while Table 13 gives 39.8 and 40.1 for what is described as the same configuration on the same model, with the other three datasets matching exactly; the AUROC cells differ slightly too. One of the two runs is mislabelled, and the choice changes Top-K's average ECE from 17.8 to 24.6.

## Five citations worth chasing next

1. **Kadavath et al. 2022, "Language models (mostly) know what they know."** The white-box counterpart: P(True) self-evaluation and calibration on multiple-choice, and the strongest existing claim that models have usable internal knowledge of their own correctness.
2. **Tian et al. 2023, "Just ask for calibration: strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback."** The concurrent work this paper positions against and borrows Top-K from; needed to see how much of the prompting result is independently replicated.
3. **Kuhn et al. 2023, "Semantic uncertainty: linguistic invariances for uncertainty estimation in natural language generation."** The semantic-equivalence clustering approach — the principled fix for the exact-match brittleness that limits Consistency aggregation on open-ended output.
4. **Lin et al. 2022, "Teaching models to express their uncertainty in words."** Origin of verbalized confidence, and the fine-tuned alternative to zero-shot elicitation.
5. **Ren et al. 2022, "Out-of-distribution detection and selective generation for conditional language models."** The selective-prediction machinery this paper cites as motivation but never runs — the place to find the risk-coverage evaluation that would make elicited confidence actionable for abstention.
