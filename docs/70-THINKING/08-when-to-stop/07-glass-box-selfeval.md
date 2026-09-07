# Self-Evaluation of Large Language Model based on Glass-box Features

## Density

**Density: MEDIUM** — the paper is a four-page Findings short paper with almost no padding, and essentially every paragraph carries either a feature definition or a result, but the amount of that signal which bears on the Subject is thin: it establishes one narrow correlational fact (a softmax-dispersion statistic tracks a GPT-4 quality score on 80-question chat benchmarks) and never tests calibration, abstention, stopping, or behaviour under confident error.

**Self-Evaluation of Large Language Model based on Glass-box Features.** Hui Huang, Yingqi Qu, Jing Liu, Muyun Yang, Bing Xu, Tiejun Zhao, Wenpeng Lu.

- **Year:** arXiv v1 March 2024, v2 September 2024. Published 2024.
- **Venue:** Findings of the Association for Computational Linguistics: EMNLP 2024 (peer-reviewed).
- **Code:** https://github.com/HuihuiChyan/SelfEval
- **Keywords (mine):** glass-box features; self-evaluation; softmax entropy; softmax variance; sentence probability; ensemble uncertainty; attention entropy; reference-based calibration; LLM-as-a-judge baseline; meta-evaluation by correlation.

# Approach

The paper asks whether an LLM can evaluate the quality of its own generation using signals that fall out of the forward pass itself — what the authors call *glass-box features*, "the useful information that can be extracted from the model as a by-product of generation" — instead of using an external judge model or a prompted self-critique. The whole method is unsupervised and training-free: each feature is computed as a single scalar per response, and that scalar is used directly as the predicted quality score. There is no probe, no classifier, no threshold, and no fitted regression anywhere in the paper.

Three feature groups are defined, in Section 2.

**1. Softmax distribution.** Computed over the decoder's output distribution at every decoding step of the generated response, across the full target vocabulary of size V. Three variants:
- `SentProb` — the plain product of token probabilities over the response, the factorised sentence probability. The authors explicitly flag this as biased, because "the model would always select from the most probable tokens during decoding regardless of their quality."
- `Softmax-Ent` — the entropy of the softmax distribution over the whole vocabulary at each step, averaged over the T response tokens: `−(1/T) Σ_t Σ_v p(y_t^v) log p(y_t^v)`. The stated intuition is that mass concentrated on few vocabulary items means the model is confident and the response is more likely accurate, whereas a near-uniform distribution predicts low quality.
- `Softmax-Var` — the variance of the per-token probabilities across the response, `E[P²] − (E[P])²` where `P = p(y_1), …, p(y_T)`. The motivation is that averaging destroys the dispersion information: how *unevenly* confident the model was across the response is itself informative. (Note the prose calls these "word-level log-probabilities" while the definition of P is in terms of probabilities, not log-probabilities — an internal inconsistency in the paper.)
- `Softmax-combo` — the normalised summation of `Softmax-Ent` and `Softmax-Var`.

**2. Uncertainty estimation** by ensembling forward passes. Because LLMs are typically served without dropout, randomness is injected two ways: *Decoding-based Ensemble* (random top-k decoding) and *Prompt-based Ensemble* (a system prompt drawn at random from a hand-designed prompt pool given in Appendix A.1). Over N forward passes the sentence-level probability SP is collected, and the expectation (`Unt-Exp`) and the variance (`Unt-Var`) across passes are used as the quality score. N is set to 10.

**3. Attention distribution.** Attention entropy `−(1/I) Σ_i Σ_j α_ji log α_ji` over the attention weights linking the I instruction tokens and the J response tokens. This is computed *per head and per layer* of the decoder, and then reduced to one number two ways: `AttnEnt-Min`, the minimum over all head/layer combinations, and `AttnEnt-Avg`, the plain mean over all H×L combinations. The authors state that it is not clear which head/layer combination would be best for quality prediction, and rather than searching for one they take these two summary statistics.

Notably, **hidden states are never used**. Despite the "glass-box" framing, the paper reads only the output softmax, the sentence probability under repeated sampling, and the attention weights. There is no layer selection, no residual-stream probe, and no position selection: the softmax features average over *all* generated token positions, and the attention features aggregate over *all* layers and heads.

Section 3 adds two optional strategies for the case where a reference answer is available:
- **In-context illustration** — prefix the prompt with the instruction and its reference answer as a demonstration, then force the model to generate the candidate answer, on the theory (citing Wang et al. 2023a on ICL as information flow) that the model will imitate the reference's softmax distribution, so the resulting distribution encodes the divergence between candidate and reference.
- **Probability calibration** — score the reference itself with `SentProb-Ref` and subtract it from the candidate's score, to cancel the evaluator's bias toward superficial properties such as complexity. (The formula printed for `SentProb-Ref` is `−(1/T) Σ_t p(ỹ_t) log p(ỹ_t)`, which is an entropy expression, while the surrounding prose calls it "the log-probability of reference answer" — a second formula/prose mismatch.)

# Models targeted and benchmarks / datasets

**Models under self-evaluation:** two 7B instruction-tuned open models — **Vicuna-7B** (Chiang et al. 2023) and **LLaMA2-7B-Chat** (Touvron et al. 2023). Both generate the responses and both compute the glass-box features on their own outputs. No larger models are tested; the limitations section names this.

**Benchmarks:** **MT-Bench** (Zheng et al. 2023) and **Vicuna-Bench** (Chiang et al. 2023). Each contains 80 questions across diverse areas; MT-Bench is multi-turn and prompt templates for both single- and multi-turn evaluation are given in the appendix. Responses are produced under MT-Bench's default settings.

**Gold labels:** not human. To avoid annotation cost, the "golden labels" are the scores produced by each benchmark's official evaluator, **GPT-4**, prompted with the templates in Appendix A.3. Every correlation number in the paper is therefore agreement with GPT-4, not agreement with a human.

**Baselines compared on the same outputs:** **GPT-3.5-Turbo** carefully prompted as a judge (closed-source external judge); **Auto-J** (Li et al. 2023a), an open model fine-tuned specifically as an evaluator; and **Self-Generation**, which prompts the model under test to score its own response on a 1–10 scale — this is the paper's stand-in for verbalised confidence / prompted self-critique.

# Author incentive

Five of the seven authors are at the Faculty of Computing, Harbin Institute of Technology; two (Yingqi Qu, Jing Liu) are at **Baidu Inc.**, Beijing; one (Wenpeng Lu) is at Qilu University of Technology / Shandong Computer Science Center. Funding is Chinese public science funding: NSFC grants 62276077, 62376075, U1908216, 62376076, the Key R&D Program of Yunnan, and a Shenzhen College Stability Support Plan grant.

The visible stake is academic rather than commercial: this is an incremental follow-on to the first author's own prior work. The introduction motivates the paper by citing Huang et al. (2024), the same first author's study arguing that fine-tuned judge models "severely underperform GPT-4 on generalizability and fairness" — a self-citation used to clear the ground for the proposed alternative. There is a mild institutional incentive in the framing around API judges: the paper argues against external proprietary evaluators on grounds of privacy leakage, reproducibility, and opacity, which suits an open-model, non-US-API research setting. Nothing suggests a product being sold; code is released openly.

# Measurement methodology

This is a **meta-evaluation by correlation**, not a decision experiment.

- **Dependent variable:** the correlation between a feature's scalar value over a set of responses and the GPT-4 quality score for those same responses. The headline metric is **Pearson**; **Spearman** and **Kendall's tau** are reported as secondary. The paper adds a footnote conceding that ranking coefficients are "not fair" to its own methods, because a continuous glass-box score cannot predict ties while the GPT-4 gold scale (integers 1–10) is full of them.
- **Unit of analysis and N:** 80 questions per benchmark, two benchmarks, two models. MT-Bench is multi-turn, and single- and multi-turn prompt templates are both provided, so the MT-Bench response count is plausibly 160 rather than 80, but the paper never states the exact number of scored responses. Either way each correlation coefficient rests on order-100 points.
- **What is controlled:** the responses are held fixed across all methods — GPT-3.5-Turbo, Auto-J, Self-Generation, and every glass-box feature score the same generations, produced under MT-Bench default decoding. Model and benchmark are crossed (2 × 2), and each of 11–13 methods is reported in each cell.
- **What is not controlled or reported:** there is **no significance testing of any kind** — no confidence intervals, no bootstrap, no p-values, no seeds, no repeated runs, and no correction for the fact that dozens of correlations are compared and the maximum is then declared the winner. Decoding hyperparameters for the top-k ensemble are not given; only N = 10 forward passes is stated. There is no ablation over which layers or heads contribute to attention entropy, no ablation over token position, and no sensitivity analysis on the normalisation used for `Softmax-combo`.
- **A structural caveat on the dependent variable:** because gold labels are GPT-4 scores, "outperforming GPT-3.5-Turbo" strictly means "agreeing with GPT-4 more closely than GPT-3.5 does." It is a statement about agreement with one particular proprietary judge, not about tracking response quality as a human would see it. The authors name this in the limitations.
- **Fitting:** none. Every glass-box feature is a closed-form statistic of the forward pass, so nothing is trained and no train/test split exists. The only quasi-fitted object is the normalisation inside `Softmax-combo`, whose procedure is not specified.

# Key findings

**1. Softmax-derived features are the only group that works, and they beat both external judges on average.** Reading the Average column of Table 1 (which is the mean of the two Pearson values):

| method | LLaMA2-7B-Chat | Vicuna-7B |
|---|---|---|
| Auto-J (fine-tuned judge) | 0.5129 | 0.5838 |
| GPT-3.5-Turbo (prompted judge) | 0.5519 | 0.5879 |
| Self-Generation (verbalised score) | 0.1454 | 0.1811 |
| SentProb | 0.3502 | 0.3478 |
| Softmax-Ent | 0.4198 | 0.5535 |
| Softmax-Var | **0.6059** | 0.5389 |
| Softmax-combo | 0.6044 | **0.6107** |
| DecEnsem-Exp | 0.4856 | 0.4809 |
| DecEnsem-Var | 0.3020 | 0.2669 |
| PrmEnsem-Exp | 0.4812 | 0.4656 |
| PrmEnsem-Var | 0.1508 | 0.2191 |
| AttnEnt-Min | 0.1313 | 0.1312 |
| AttnEnt-Avg | 0.1169 | 0.1305 |

The authors read this as verifying "the strong association between the confidence represented by the softmax distribution and the response quality," with the explicit causal story that "when the instruction exceeds the LLM's capability scope, the model would generate the response with low confidence, resulting in a sparse log-probability distribution."

The margin over the external judges is real on averages but modest, and it is not uniform per cell: on Vicuna-Bench with Vicuna-7B, GPT-3.5-Turbo scores 0.6946 Pearson against Softmax-combo's 0.6856, so the external judge wins that cell.

**2. Which softmax feature is best is not stable.** On LLaMA2-7B-Chat, `Softmax-Var` (0.6059) leads and `Softmax-Ent` trails badly (0.4198). On Vicuna-7B the ordering reverses (Ent 0.5535 > Var 0.5389) and the combination leads. The paper does not comment on this instability; it reports only that adding entropy and variance together "can achieve further improvement," which holds on one model and not the other.

**3. Plain sentence probability is weak.** `SentProb` sits around 0.35 on both models, well below the dispersion statistics computed from the same distributions and below both judges. This is the paper's own predicted failure mode: decoding always picks high-probability tokens, so the selected-token probability is compressed and uninformative, while the *shape* of the distribution over the vocabulary still carries signal.

**4. Ensemble uncertainty underperforms and is judged impractical.** Expectation-based ensembling reaches about 0.48 and variance-based ensembling collapses to 0.15–0.30. The authors attribute this to N = 10 forward passes being "inadequate to quantify model uncertainty," and conclude that because multiple forward passes are "overly time-consuming," ensembled uncertainty estimation "is less practical for self-evaluation." That is a cost argument, not a demonstration that the signal is absent.

**5. Attention entropy fails outright** (0.12–0.13 average Pearson, and near zero on MT-Bench with Vicuna-7B: 0.0355 Pearson for AttnEnt-Avg). The authors explain the gap against Fomicheva et al. (2020), where attention entropy worked for unsupervised MT quality estimation, by arguing that encoder-decoder MT emits one or two tokens per source position while open-ended LLM generation does not, so "a dispersed attention across multiple positions, leading to a low attention entropy, does not necessarily indicate a poor response."

**6. Prompted self-scoring — the verbalised-confidence comparator — collapses, but for a stated mechanical reason.** Self-Generation reaches only 0.1454 and 0.1811. The paper's own explanation is that "the model fails to comprehend the instruction to generate a score between 1 to 10 in most cases." The authors turn this into a selling point for glass-box features: the method "is not limited by the capabilities of the evaluated model and can be effectively applied to 7B-sized models." That reading of the comparison is fair, but it also means the experiment shows a 7B model failing at the *output format* of self-scoring, rather than showing a well-formed verbalised confidence being poorly calibrated.

**7. Reference augmentation gives small gains, which the text describes as large.** Table 2 (Vicuna-Bench only; MT-Bench is not reported for this experiment) shows: LLaMA2 `Softmax-Ent` 0.3730 → 0.3678 with illustration (a *decrease*) and → 0.3930 with calibration; LLaMA2 `Softmax-Var` 0.6506 → 0.6580 / 0.6617; Vicuna-7B `Softmax-Ent` 0.6379 → 0.6375 (again a slight decrease) / 0.6441; Vicuna-7B `Softmax-Var` 0.6146 → 0.6247 / 0.6526. The largest single gain is +0.038 Pearson, and two of the eight deltas are negative. The text nevertheless asserts that "both the two strategies can enhance the evaluation accuracy by a large margin," and concludes that calibration beats illustration and that "the references is a pivotal information for response evaluation." The direction of the calibration result is consistent across all four rows, which is the defensible part of the claim; the magnitude claim is not supported by the table.

**8. The authors' framing of what this is for.** The conclusion positions self-evaluation as a control signal for downstream loops: the model "can rely on self-evaluation results to decide whether to perform self-reflection" (citing Xie et al. 2024) "or to select preferred data for reward modeling" (citing Lee et al. 2024). Both are named as future work; neither is implemented or measured here.

# Open questions the paper itself raises

From the Limitations section, in the authors' own terms:

1. Gold labels came from GPT-4 rather than human annotators; "including human evaluators would enhance the credibility of our proposed self-evaluation methods."
2. Experiments are confined to 7B models; larger models should be included for a thorough evaluation.
3. The downstream applications are unvalidated: self-evaluation "can be applied to various applications," and validating it inside self-reflection or reward modelling "would further bolster its utility."

From the body, raised but not closed:

4. Which head and layer combination of attention would best predict quality is stated as unknown, and is finessed with min and average summaries rather than investigated.
5. Whether ensemble uncertainty would work with a forward-pass count larger than 10 is left open; the method is dropped on cost grounds, not on evidence.

# Appreciation

**MECHANISM.** The genuinely useful idea, and the one that transfers as an idea rather than as a number, is the separation between *which token was selected* and *what the distribution looked like*. `SentProb` reads only the selected path and is compressed by decoding; `Softmax-Ent` reads the full vocabulary distribution at each step; `Softmax-Var` reads how much the per-token confidence fluctuates along the response. Those are three different questions asked of the same forward pass, and the experiment shows they behave very differently — the dispersion statistics roughly double the correlation achieved by the sentence probability. Second, the mechanism is *free*: these are by-products of a generation that is happening anyway, and they require no second model, no second call, no annotation, and no training, which puts them in a different cost class from an LLM judge entirely. Third, the negative results carry real diagnostic value: attention entropy, transplanted from a setting where it worked, fails here, and the paper states clearly why the two settings differ.

**MAGNITUDE.** The numbers are small-sample, single-run, and unaccompanied by any uncertainty estimate. A Pearson of about 0.60 on roughly 80 to 160 points, compared against about 0.55 for GPT-3.5-Turbo, is not a result I would treat as establishing an ordering between methods; the gap sits well inside what sampling noise at that N could produce, with no repeats and no confidence intervals, and the winning feature was selected after the fact from a table of roughly a dozen candidates scored on the same data. The identity of the best feature flips between the two models. The reference-augmentation gains (+0.006 to +0.038, with two negatives) are called "a large margin" and are not one. And the whole scale is anchored to GPT-4 agreement, so a correlation of 0.60 means "matches GPT-4's opinion moderately," not "detects bad answers reliably." I would carry the mechanism forward and treat every specific figure as an existence proof at 7B on chat benchmarks, and nothing more.

# How it could serve a harness-design effort / limitations / major concerns

**What is usable.** For a loop that must decide whether an attempt is going well, this paper supplies a candidate signal that costs nothing extra to obtain: mean vocabulary-level softmax entropy and the variance of per-token probability, computed over the tokens the model has just emitted, with no probe to train and no labels to collect. It is available at generation time, it is local to the model doing the work, and it degrades gracefully in the sense that a small model which cannot articulate a self-score still has a usable distribution. The failure of `SentProb` is the practical warning attached: a harness that logs mean token log-probability as its confidence proxy is logging the weakest of the three signals tested here.

**Concerns, roughly in order of how much they would bite.**

- **The confidently-wrong case is never tested, and the method's core assumption is precisely that this case does not arise.** The paper's mechanism story is "when the instruction exceeds the LLM's capability scope, the model would generate the response with low confidence." A fluent, low-entropy, wrong answer — a confident hallucination — is by construction scored as high quality by every feature in this paper. There is no hallucination benchmark here, no factuality set, no adversarial or misleading-premise condition, and no error analysis of the high-confidence tail. MT-Bench and Vicuna-Bench are open-ended chat-quality benchmarks scored 1–10 by GPT-4, which is a smoothly varying "how good is this answer" axis rather than a correctness axis where the confident-and-wrong failure would surface. So on the specific question of whether the softmax signal survives when the model is confidently wrong, the paper does not answer it, and its own framing gives reason to expect that it would not.
- **There is no calibration analysis and no operating point.** Everything is correlation. There is no reliability diagram, no ECE, no threshold, no accept-or-reject decision, and no precision and recall for flagging bad responses. A harness needs a cut point — below this value, retry or escalate — and the paper never converts a correlation into one, nor reports what fraction of bad responses a given threshold would catch.
- **Scores are not comparable across items or across models.** Softmax entropy and probability variance depend on response length (both are averaged over T, but the underlying distributions shift with length), on decoding settings, on vocabulary size, and on how sharp the model's distribution is in general. Nothing in the paper establishes that a score of *x* means the same thing on two different prompts, let alone on two different models. The two models already disagree about which feature is best. Any threshold would have to be re-established per model and probably per task family, which the paper neither does nor discusses.
- **Transfer across tasks and models is untested.** Because nothing is fitted, there is technically nothing to transfer, but that is a semantic escape rather than evidence. The correlations themselves vary substantially by cell — `Softmax-Ent` ranges from 0.3730 to 0.6379 Pearson across the four model-by-benchmark cells — so the *strength* of the signal is clearly setting-dependent even though the *formula* is universal. Two models, both 7B, both LLaMA-family instruction-tuned, both evaluated on 80-question English chat benchmarks, form a narrow basis for a generality claim.
- **The method requires logit access.** It needs the full vocabulary distribution at every step, and the attention features need per-head weights. That rules out any harness stage backed by a closed API which returns only top-k logprobs or none at all. This is a strength for local open-weight components and a hard limit elsewhere, and the paper never spells out the deployment constraint.
- **Label dependence, stated precisely.** The method itself needs no labels. The *evidence that the method works* needs labels, and here those labels are GPT-4 outputs. Anyone adopting this would have to validate the signal on their own task with their own labels before trusting a threshold, so the labelling cost reappears at the validation step even though it is absent at inference.
- **The verbalised-confidence comparison is weak evidence.** Self-Generation loses badly, but the paper's own explanation is format failure at 7B rather than miscalibration. That does not license a conclusion that internal features beat verbalised confidence in general; at a scale where models can reliably emit a 1–10 score, the comparison would have to be rerun.
- **The reference-augmented variants presume that a reference exists,** which is not the situation an agent loop is usually in.
- **Two formula-versus-prose mismatches** (`Softmax-Var` is described over log-probabilities but defined over probabilities; `SentProb-Ref` is described as a log-probability but printed as an entropy expression) mean the exact quantities would have to be recovered from the released code rather than from the paper.

# Five citations worth chasing next

1. **Fomicheva et al. (2020), "Unsupervised quality estimation for neural machine translation," TACL 8:539–555.** The direct ancestor of this paper's whole feature set — softmax entropy, sentence probability, and attention entropy as unsupervised quality predictors — and the source of the attention-entropy result that fails to replicate here. Worth reading for how the same signals were validated against human judgements in a setting where correctness is well defined.
2. **Malinin and Gales (2021), "Uncertainty estimation in autoregressive structured prediction."** The theoretical basis for the ensemble uncertainty branch that this paper implements at N = 10 and then abandons on cost grounds. It separates knowledge uncertainty from data uncertainty for sequence models, and that distinction is exactly what the confidently-wrong problem turns on.
3. **Xie et al. (2024), "Self-evaluation guided beam search for reasoning," NeurIPS 36.** Cited in the conclusion as the intended downstream use, where a self-evaluation score steers a search or reflection loop rather than merely correlating with quality. This is the paper that actually closes the loop the present work only gestures at.
4. **Huang et al. (2024), "An empirical study of LLM-as-a-judge for LLM evaluation: fine-tuned judge models are task-specific classifiers."** The first author's companion study, used here to justify discarding fine-tuned judges. It is the load-bearing premise of the introduction, and it should be read to check whether the generalisation failure it reports is as broad as this paper assumes.
5. **Zheng et al. (2023), "Judging LLM-as-a-judge with MT-Bench and Chatbot Arena."** The source of the benchmark, the prompt templates, and the GPT-4 gold labels against which every number in this paper is measured, including its documentation of GPT-4-as-judge biases, which bounds how far any agreement score reported here can be trusted.

*(Also noted for the abstention and bias thread, though outside the five: Wang et al. 2023b, "Large language models are not fair evaluators," and Rikters and Fishel 2017, "Confidence through attention," which is the original attention-as-confidence proposal.)*
