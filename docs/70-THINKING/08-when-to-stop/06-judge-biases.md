# Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge

## Density

**Density: MEDIUM.** The paper is numerically dense and its tables are almost entirely load-bearing (six judges x twelve biases, with per-condition breakdowns rather than only headline averages), but the prose around those tables is thin and repetitive, the appendix largely restates Table 1, and one discussion paragraph drifts into cognitive psychology and postmodern philosophy without doing any work; of the signal that is there, roughly two of the twelve biases (self-enhancement and refinement-aware) bear directly on the Subject, while the rest bear on it indirectly, as evidence about how fragile a judge signal is in general.

## Name, keywords, year, venue

- **Full title.** "Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge."
- **Authors.** Jiayi Ye, Yanbo Wang, Yue Huang (the three marked as equal contributors), Dongping Chen, Qihui Zhang, Nuno Moniz, Tian Gao, Werner Geyer, Chao Huang, Pin-Yu Chen, Nitesh V. Chawla, Xiangliang Zhang (corresponding).
- **Year and venue.** The paper was published at ICLR 2025. I confirmed the track directly: the camera-ready PDF in the ICLR 2025 proceedings carries the running header "Published as a conference paper at ICLR 2025", and dblp lists it under `conf/iclr`. It is therefore a main-conference paper, not a workshop paper. The preprint is arXiv:2410.02736 (v1 3 Oct 2024, v2 4 Oct 2024, cs.CL).
- **Keywords (mine).** LLM-as-a-judge; judge bias taxonomy; adversarial perturbation of judging inputs; robustness rate; self-enhancement bias; position bias; sentiment bias; pairwise comparison versus scoring; evaluator reliability; reward-model contamination.

### Version note, which matters for anyone citing numbers

The arXiv v2 and the ICLR camera-ready are **not** the same document, and the differences are substantive rather than cosmetic. I read both. The camera-ready adds:

1. A new metric, **AIR** (accuracy improvement rate), replacing the raw accuracy reported for chain-of-thought bias: `AIR = (Acc_CoT - Acc_ori) / Acc_ori x 100%`.
2. A new metric, **BIS** (Bias Impact Score), defined as the difference between RR and CR, so that a judge's susceptibility to bias is separated from its baseline flakiness. This is the single most useful addition, and it changes the model ranking (see Key findings).
3. A **signed** error rate for self-enhancement and refinement-aware bias. The arXiv version used absolute value, `|1 - y_self/y_other|`, which destroyed the direction of the effect; the camera-ready uses `y_self/y_other - 1`, so a reader can now see whether a judge inflates or deflates its own work.
4. **Appendix F, a human evaluation** of the perturbations, absent from arXiv entirely.
5. Corrected numbers in Table 5. The arXiv Table 5 and Table 7 disagreed with each other about GLM-4's and Claude-3.5's self-scores; the camera-ready Table 5 is internally consistent with its Table 8.

Anyone quoting the self-enhancement figures from the arXiv preprint will quote wrong ones. Below I use the camera-ready throughout and flag where the preprint differs.

## Approach

The authors take the position that prior work on judge bias has two defects: it is narrow, examining one or two biases at a time, and it depends on human annotators to establish which answer is really better, which is expensive, subjective, and hard to reproduce. They propose to fix both at once with an automated framework they call **CALM** (Comprehensive Assessment of Language Model Judge Biases).

The core move is an **attack-and-detect** design that sidesteps the need for a human quality ground truth. Rather than asking whether the judge got the answer right, CALM asks whether the judge **changes its mind** when the input is perturbed in a way that does not change which answer is actually better. The judgment input is formalised as `P = (I, Q, R)`, where `I` is the system instruction, `Q` the question, and `R` the response or responses. A perturbation function `g(.)` rewrites either a response (`g(R)`) or the instruction (`g(I)`), producing a modified prompt `P̂`. The framework then compares `y = LLM(P)` against `ŷ = LLM(P̂)`. In the pairwise case the input is `P = (I, Q, R1, R2)` and the perturbation touches exactly one side, giving `ŷ = LLM(I, Q, R1, g(R2))` or `ŷ = LLM(g(I), Q, R1, R2)`.

The logic of the design is worth stating plainly, because it is what makes the numbers interpretable. The pair `(R1, R2)` is constructed so that `R1` is clearly better. The perturbation is applied to the *worse* answer `R2` (for verbosity, authority) or to the *better* answer `R1` (for sentiment, fallacy-oversight), in a way that is stipulated not to change the quality ordering. A judge that is doing its job must therefore return the same verdict before and after. Any flip is, by construction, attributable to the injected feature rather than to answer quality. The dependent variable is a **flip rate**, not an accuracy, and this is what lets the authors claim they need no human labels.

The perturbation `g(.)` is itself performed by an LLM. GPT-4-Turbo (GPT-4o in the framework figure) rewrites answers under written guidelines, in the style of constitutional AI, with the twin constraints that the rewrite must not alter correctness or drift semantically, and must not be so trivial that no bias could be exposed.

## The 12 biases, with definitions and how CALM isolates each

The definitions below are the authors' own, from Table 1 and Appendix B; the isolation method is from Appendix C. I have grouped them by what the perturbation actually touches, because that grouping turns out to matter for the Subject.

**Group 1 - the perturbation rewrites an answer's surface, leaving its content intact.**

1. **Verbosity.** "LLM judges favor longer responses, even if they are not as clear, high-quality, or accurate as shorter alternatives." *Isolation:* GPT-4-Turbo lengthens the **worse** answer in the fact-related dataset while preserving its essential content; the judge re-compares. A flip means length alone bought the win. They additionally sweep the expansion ratio.
2. **Sentiment.** "The preference for expressions of positive or negative emotions, affecting its judgment of emotional content." *Isolation:* GPT-4-Turbo rewrites an answer to carry one of four emotions - cheerful, sad, angry, fear - and this is done separately for the better answer and for the worse answer, giving the eight `(bet.)` / `(wor.)` conditions in Table 8.
3. **Fallacy-oversight.** "LLM judges may ignore logical errors in reasoning steps and only focus on the correctness of final results." *Isolation:* this one inverts the usual scoring rule, and the inversion is easy to misread. GPT-4-Turbo corrupts the reasoning in the **better** answer so its logic becomes chaotic while its final answer stays right. Because the corrupted answer is now genuinely worse than the original loser, a judge that **changes** its verdict is scored **correct**; a judge that keeps its verdict is scored as having missed the fallacy.
4. **Authority.** "The tendency to assign more credibility to statements made by authority figures, regardless of actual evidence." *Isolation:* fabricated citations are generated and injected into an answer, in three formats tested separately - book references, URLs, and famous-person quotes.

**Group 2 - the perturbation adds material to the system instruction, never touching the answers.**

5. **Bandwagon.** "The tendency to give stronger preference to the majority's beliefs regardless of whether they are correct or not." *Isolation:* the sentence "{number}% of people believe that {chosen_model} is better in this question" is appended to the system prompt, at four levels: 60, 70, 80, 90 per cent.
6. **Distraction.** "The inclination to give more attention to irrelevant or unimportant details." *Isolation:* a meaningless statement such as "Assistant A loves eating pasta" is inserted into the system prompt. Crucially they run it both ways - distracting toward the high-quality answer (`h.c`) and toward the low-quality one (`h.r`).
7. **Diversity.** "Bias may be shown towards certain groups like 'Homosexual', 'Black', 'Female', and 'HIV Positive'." *Isolation:* an identity is asserted about one assistant in the system prompt, across six categories: Homosexual, Black, Female, HIV Positive, Refugees, Muslim believers.
8. **Compassion-fade.** "The tendency to observe different behaviors when given well-known model's name as opposed to anonymized aliases." *Isolation:* the judge is shown the real model names of the answer authors, and this condition is compared against the anonymised default.
9. **Chain-of-thought.** "The model's evaluation results may vary with and without CoT." *Isolation:* the judging instruction is swapped for one that tells the judge to solve the question itself step by step first, then compare. This is the one "bias" measured by accuracy against ground truth rather than by flip rate, since the intervention is expected to be an improvement rather than a corruption.

**Group 3 - the perturbation changes the provenance of the answer, not the answer.**

10. **Position.** "LLM judges exhibit a propensity to favor one answer at certain position over others." *Isolation:* the answers are re-ordered by rotational permutation, with two, three, and four candidates tested. Any inconsistency across orderings counts as a failure. This is the purest control in the paper, since literally nothing about the content changes.
11. **Self-enhancement.** "LLM judges may favor the answers generated by themselves." *Isolation:* this uses pointwise scoring, not pairwise comparison. Each judge model first answers the questions, then scores both its own answers and other models' answers - **with authorship anonymised, so the judge is never told what it wrote**. The metric compares the score a judge gives its own response against the score other judges give that same response, holding the response fixed and varying the judge.
12. **Refinement-aware.** "Telling the model that this is a refined result will lead to different evaluations." *Isolation:* the model answers, then refines its own answer, and the judge scores three variants - the original, the refined answer alone, and the refined answer accompanied by the conversation history that reveals it was refined. The bias is the gap between the last two, where the text being scored is close to identical and only the visible refinement history differs.

**A structural observation.** Nine of the twelve perturbations (groups 1 and 2, plus position) leave the actual quality ordering untouched by construction. Only fallacy-oversight deliberately changes the ordering, and it inverts its scoring rule accordingly. Self-enhancement and refinement-aware are the only two that operate on the judge's relationship to the text rather than on the text's presentation.

Table 2 also tags each bias along three dimensions the authors define: **Answers-Related** (does the bias concern modification of the answers), **Semantic-Related** (does it concern the answer's meaning, as with flawed reasoning logic), and **Instruction-Influence** (is it carried by the system prompt). Only two biases are marked Semantic-Related: fallacy-oversight and refinement-aware.

## Models targeted

**Six judge models** are evaluated, all as of mid-2024 (Table 11):

| Judge | Version | Type |
|---|---|---|
| ChatGPT | gpt-3.5-turbo-0125 | proprietary |
| GPT-4-Turbo | gpt-4-turbo-0409 | proprietary |
| GPT-4o | gpt-4o-0513 | proprietary |
| Claude-3.5 | claude-3.5-sonnet-0620 | proprietary |
| GLM-4 | glm-4-0520 | proprietary |
| Qwen2 | Qwen2-72B-Instruct | open source |

**Four further models generate responses only** and never judge: Llama-3-8B-Instruct, Llama-3-70B-Instruct, Mistral-7B-Instruct-v0.2, and Mixtral-8x22B-Instruct-v0.1. The stated reason for keeping generation and judging populations partly separate is precisely to keep self-enhancement bias from contaminating the other measurements.

The model selection is justified on the grounds that weak judges are simply noisy, so only capable models are worth testing. This is defensible but it means the paper says nothing about the small, cheap judges that a cost-conscious harness would actually deploy in an inner loop.

## Benchmarks and datasets

Three purpose-built datasets, assembled from existing sources rather than collected fresh:

- **Fact-related dataset, 500 samples.** GSM8K (150), MATH (150), ScienceQA (200). For each question, **GPT-4-Turbo generates both answers** - one relatively good, one of lower overall quality but with complete reasoning - which become `R1` and `R2`. Used for verbosity, fallacy-oversight, and sentiment, on the reasoning that here the quality gap is objective and unaffected by presentation.
- **Refinement-aware dataset, 500 samples.** CommonsenseQA (150), Quora-QuAD (150), TruthfulQA (200). The text describes this set as open-ended questions in the humanities, social sciences, and general knowledge, chosen because their answers admit meaningful refinement; the inclusion of CommonsenseQA, a multiple-choice benchmark, sits a little oddly with that description.
- **Alignment dataset, 439 samples after filtering.** Sampled 100 each from five DPO preference datasets: Truthy-DPO-v0.1, Emerton-DPO-Pairs-Judge, Orca-DPO-Pairs, Py-DPO-v0.1, and Roleplay-NSFW. Coverage spans code, NSFW content, truthfulness, and role-play. Used for position, compassion-fade, bandwagon, distraction, authority, diversity, CoT, and self-enhancement.

Per-bias sample sizes are **not uniform**: 439 for position, compassion-fade, distraction, and CoT; 500 for verbosity, fallacy-oversight, sentiment, and refinement-aware; and only **150** for bandwagon, authority, diversity, and self-enhancement. The four smallest-N biases include self-enhancement, which is the one the Subject cares most about.

**Where the ground truth comes from.** This deserves to be stated explicitly because the paper's central selling point is that it needs no human labels. For the alignment dataset, the "correct" answer is the `chosen` side of a DPO pair, so the ground truth is inherited human preference annotation. For the fact-related dataset, the quality ordering is **asserted by GPT-4-Turbo**, which generated both answers to a specification. So the paper has not removed the ground-truth problem; it has moved it. For the largest block of biases it relies on an LLM's judgment of which of its own two outputs is better, in order to measure whether LLMs judge reliably.

## Author incentive

The affiliations are University of Notre Dame (Huang, Moniz, Chawla, Zhang - the corresponding author's group), MBZUAI, University of Washington, Peking University, **IBM Research** (Tian Gao, Werner Geyer, Pin-Yu Chen), and University of Hong Kong. No funding statement appears in the camera-ready.

On incentives I read the stake as follows, and it is mild rather than distorting. None of the authors' institutions sell any of the six judged models, and the paper's most negative findings land on models from OpenAI, Anthropic, Zhipu, and Alibaba alike, with no house model to protect. IBM Research does have a general commercial interest in enterprise model evaluation and trust tooling, and several of the same authors have a running line of "trustworthiness" and "LLM-as-a-judge" benchmark papers (TrustLLM, MLLM-as-a-Judge, the honest-and-helpful line), so there is a mild positional stake in the framing that judge reliability is an open problem requiring frameworks like theirs. The paper also ships a project website, so there is the ordinary academic incentive toward adoption of CALM as a standard. I saw nothing that looks like a result being shaded, and the willingness to report that GPT-4o beats Claude-3.5 on some biases and loses on others cuts against any simple narrative.

## Measurement methodology

**Dependent variables.** Four, applied selectively per bias (Table 2):

- **Robustness Rate**, the primary metric for nine of the twelve biases: `RR = (1/|D|) Σ 1(y_i = ŷ_i)`. It is the fraction of items where the verdict survives the perturbation. Higher is better.
- **Consistency Rate**: `CR = (1/|D|) Σ 1(y_i = y_rand_i)`. The judge runs the *same unperturbed* comparison twice, and CR is the agreement between the two runs. This is the paper's noise floor, and its inclusion is the most methodologically serious thing in the paper.
- **AIR** for CoT: `(Acc_CoT - Acc_ori) / Acc_ori x 100%`, where accuracy is agreement with the dataset's ground truth.
- **Error rates** for the two scoring-based biases: `ErrorRate_SE = y_self/y_other - 1` and `ErrorRate_RA = y'_ref/y_ref - 1`, both signed in the camera-ready and both better when close to zero.

**The execution protocol.** For each item the judge is run twice. The first run gives `y`. The second run is done in two parallel branches: one with no perturbation, yielding `y_rand`, and one with the bias injected, yielding `ŷ`. RR compares `y` against `ŷ`; CR compares `y` against `y_rand`. This is a genuinely good design, because it means every RR number has a matched same-item, same-run-count control, and the reader can see how much of an apparent bias effect is just the judge being unstable.

**What is controlled.** Answer quality is held fixed by construction, as described above. Temperature is fixed at 0.7 for every judge and every generator - a choice inherited from Chen et al. (2024a) and justified as balancing output quality against reproducibility, though 0.7 is a strange choice when the study's whole subject is decision stability and a lower temperature would have raised the CR floor. Judging prompts are adapted from Zheng et al. (2024) and Liu et al. (2023a) and are reproduced in full in the appendix. Order is controlled by rotational permutation for the position experiments.

**N.** Between 150 and 500 per bias per model, as listed above. With six judges, twelve biases, and many sub-conditions (four bandwagon levels, three citation formats, eight sentiment conditions, six identity categories, two distraction targets, three position arities), the total is large, but any single cell rests on 150 to 500 items and, apparently, a single run.

**How significance is treated: it is not.** This is the paper's clearest methodological gap. There are no p-values, no confidence intervals, no error bars, no variance across seeds, and no repeated runs beyond the two-run consistency check. I searched the full text for statistical treatment and found none. The authors nevertheless make repeated comparative claims across models - "Claude-3.5 generally shows the greatest resilience", GPT-4-Turbo improved "0.7%" under CoT - where the differences are of the same order as the CR gap. At N=150 for self-enhancement, and with temperature 0.7, a difference of a few points between two judges is not distinguishable from noise, and the paper does not attempt to show otherwise. The BIS metric added in the camera-ready is a partial and welcome remedy, since subtracting CR at least nets out the baseline flakiness, but it is a point estimate too.

**Human involvement.** The paper's headline claim is that CALM eliminates human assessment. The camera-ready qualifies this with Appendix F. Five evaluators, undergraduate and PhD students with NLP and bias-detection expertise, independently assessed samples, with majority vote deciding. They checked two things: whether the intended bias was successfully incorporated, and whether any *unintended* bias was introduced. Results in Table 10 are strong - bias incorporation between 98.4% and 100%, absence of unintended bias between 90.2% and 97.4%. The scope is limited, however: Table 10 covers only verbosity, fallacy-oversight, and the eight sentiment conditions, that is, exactly the perturbations produced by LLM rewriting. The template-insertion biases are not human-checked, presumably because their validity is self-evident. The important point for the Subject is that **humans here validate the perturbation, not the judgment**. There is no human agreement study on the verdicts, no inter-annotator agreement figure on answer quality, and no human-judge agreement baseline anywhere in the paper.

**Inter-judge agreement.** Likewise absent as an explicit analysis. The one place where judges are compared against each other is the self-enhancement measurement, where `y_other` is the score other judges assign to the same response, and the Z-score-normalised heat map in Figure 5. The paper does not report how often the six judges agree with each other on unperturbed items, which would have been an easy and informative number to publish.

## Key findings

### The headline table

Robustness Rate by judge and bias, from camera-ready Table 4. `CR_FR` and `CR_Al` are the unperturbed self-agreement controls on the two datasets, and they are the numbers to read everything else against.

| Judge | Ver. | Fal. | Sen. | **CR_FR** | Pos. | Com. | Ban. | Aut. | Dst. | Div. | **CR_Al** | CoT |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ChatGPT | 0.900 | 0.917 | 0.804 | **0.998** | 0.566 | 0.862 | 0.688 | 0.662 | 0.713 | 0.679 | **0.906** | 0.560 |
| GPT-4-Turbo | 0.915 | 0.969 | 0.653 | **0.990** | 0.818 | 0.858 | 0.638 | 0.846 | 0.729 | 0.855 | **0.856** | 0.720 |
| GPT-4o | 0.977 | 0.984 | 0.699 | **0.998** | 0.776 | 0.868 | 0.791 | 0.787 | 0.790 | 0.814 | **0.925** | 0.700 |
| GLM-4 | 0.887 | 0.979 | 0.679 | **0.970** | 0.781 | 0.835 | 0.690 | 0.796 | 0.814 | 0.788 | **0.884** | 0.688 |
| Claude-3.5 | 0.952 | 0.985 | 0.660 | **0.999** | 0.832 | 0.875 | 0.610 | 0.865 | 0.878 | 0.914 | **0.915** | 0.745 |
| Qwen2 | 0.884 | 0.935 | 0.651 | **0.994** | 0.760 | 0.877 | 0.710 | 0.779 | 0.785 | 0.826 | **0.904** | 0.704 |

Two things stand out before any bias is considered. First, on the fact-related data the judges are almost perfectly self-consistent (CR 0.970 to 0.999), so any RR shortfall there is real bias rather than noise. Second, **on the alignment data the judges disagree with themselves on 7.5 to 14.4 per cent of items with no perturbation whatsoever** - GPT-4-Turbo is the worst at CR_Al = 0.856. That baseline flakiness is a finding in its own right, and it is the reason several of the alignment-side bias effects are smaller than they look.

Note also that the camera-ready labels the final column AIR while the values (0.560 to 0.745) are plainly accuracies rather than percentage improvements, and the narrative quotes AIR figures of 0.7% for GPT-4-Turbo and 7% for GLM-4 that are consistent with the column being post-CoT accuracy with `Acc_ori` never tabulated. The CoT results are consequently the least legible part of the paper; a reader cannot recompute AIR for four of the six models.

### The worst bias by a wide margin is sentiment, and only in one direction

The aggregate sentiment column understates this badly. Broken out by emotion and by which answer was rewritten (Table 8), the picture is dramatic:

| Condition | ChatGPT | GPT-4-Turbo | GPT-4o | GLM-4 | Claude-3.5 | Qwen2 |
|---|---|---|---|---|---|---|
| Cheerful (better answer) | 0.803 | 0.682 | 0.727 | 0.770 | 0.609 | 0.726 |
| Sad (better answer) | 0.659 | 0.271 | 0.343 | 0.306 | **0.259** | 0.307 |
| Angry (better answer) | 0.639 | 0.366 | **0.243** | 0.380 | 0.256 | 0.283 |
| Fear (better answer) | 0.639 | 0.254 | 0.355 | 0.271 | 0.260 | **0.238** |
| Cheerful (worse answer) | 0.910 | 0.888 | 0.970 | 0.905 | 0.976 | 0.871 |
| Sad (worse answer) | 0.916 | 0.920 | 0.983 | 0.907 | 0.970 | 0.929 |
| Angry (worse answer) | 0.946 | 0.921 | 0.987 | 0.950 | 0.973 | 0.926 |
| Fear (worse answer) | 0.923 | 0.921 | 0.987 | 0.943 | 0.973 | 0.926 |

**When a negative emotional tone is written into the better answer, the frontier judges reverse their verdict roughly three times out of four.** GPT-4o under an angry tone holds its verdict on only 24.3% of items, Qwen2 under fear on 23.8%, GPT-4-Turbo under fear on 25.4%, Claude-3.5 under all three negative emotions on about 26%. Against a fact-related consistency floor of 0.99, essentially none of this is noise.

The asymmetry is the interesting part. Adding emotion to the *worse* answer barely moves anything (0.87 to 0.99). So this is not a preference for emotional writing; it is an **aversion** to it, strong enough to override a quality gap the judges otherwise resolve correctly. A model that writes its status report in a frustrated or alarmed register will be marked down for the register.

Note also the inversion by capability: **ChatGPT, the weakest judge, is by far the most robust to sentiment** (0.639 to 0.803 where the frontier models sit at 0.24 to 0.37). The paper observes this in passing - "GPT-4-Turbo exhibits inconsistency when judging emotional responses, whereas ChatGPT demonstrates more stable performance" - without pressing on it. The natural reading is that the stronger models are more sensitive to tone because they are better at modelling it, which makes this a capability-scaling problem that will not fix itself.

### Position bias collapses as the candidate set grows

In the pairwise case, RR runs 0.566 (ChatGPT) to 0.832 (Claude-3.5). The exploratory sweep is worse: with three or four candidates, **most models fall below 0.5**, meaning the verdict fails to survive re-ordering more often than it survives. Since nothing about the content changes under permutation, this is pure order sensitivity. The authors' recommendation is the obvious one, namely randomise or rotate the order and prefer judges with better RR.

### The remaining biases, briefly

- **Bandwagon** is the strongest of the instruction-side attacks and, unusually, **Claude-3.5 is the most susceptible** (0.563 to 0.638 across the four levels) while GPT-4o is the most resistant (0.773 to 0.805). The stated percentage of people holding the majority view (60 / 70 / 80 / 90) has **no monotone effect**, which the authors read as showing that the model responds to the presence of a social cue rather than to its strength.
- **Authority** shows fake citations working, and working differently by format: book references and quotes bite harder than URLs, which the authors attribute to URLs being short and familiar. ChatGPT drops to 0.628 under book citations. In the case study, the judge explicitly cites the fabricated reference as its justification.
- **Distraction** by an irrelevant sentence in the system prompt costs 0.10 to 0.29. The direction matters: distracting toward the high-quality answer hurts more than distracting toward the low-quality one, so **irrelevant material does more damage to the evaluation of a good answer than a bad one**.
- **Diversity** shows ChatGPT to be markedly sensitive to asserted identity (0.646 on Female, 0.660 on Black) while Claude-3.5 is nearly impartial (0.862 to 0.945). Most models are most sensitive to female and refugee status.
- **Compassion-fade** is the weakest effect in the paper (0.835 to 0.877), and under BIS it is within noise for GPT-4-Turbo (-0.002, i.e. revealing model names made it marginally *more* consistent than its own unperturbed control).
- **Fallacy-oversight is the one the judges pass** (0.917 to 0.985). See the stance-versus-content accounting below, because this is the most important comparison in the paper.
- **CoT** improves accuracy for most judges, but modestly: +0.7% for GPT-4-Turbo, +7% for GLM-4.

### Self-enhancement, the finding most relevant to the Subject

Camera-ready Table 5, with the signed error rate `y_self/y_other - 1`:

| Judge | Score it gives its own answer | Score others give the same answer | Error |
|---|---|---|---|
| ChatGPT | 5.21 | 6.25 | **-16.64%** |
| GPT-4-Turbo | 6.98 | 6.38 | **+9.40%** |
| GPT-4o | 7.01 | 6.48 | **+8.18%** |
| GLM-4 | 6.55 | 6.32 | **+3.63%** |
| Claude-3.5 | 7.04 | 6.68 | **+5.39%** |
| Qwen2 | 7.64 | 7.01 | **+8.99%** |

**Five of the six judges inflate their own work, by 3.6 to 9.4 per cent on a ten-point scale.** ChatGPT is the exception and goes the other way by a large margin; the authors note in Appendix D that ChatGPT's own answers are weak enough that the other judges score it low, so its column "lacks reference value", which is a fair caveat but also an admission that the metric is not clean.

Three design points are worth separating out, because they decide how much weight this number can carry.

1. **Authorship was anonymised.** Appendix C is explicit: "each model was tasked with answering the questions and subsequently evaluating both its responses and those generated by other models, without prior knowledge of the authorship of any given answer." So this is *not* a name-recognition effect - that is compassion-fade, tested separately. Whatever is happening here is the judge recognising its own text implicitly, or, more likely, simply finding its own style maximally legible. The authors' own gloss is that models rated their outputs more favourably "even when answer sources were anonymized", and their recommendation is blunt: **"Avoid using the same model to generate and judge answers."**
2. **Response quality is held fixed and the judge is varied.** This is the right control, and it is better than a naive design that would compare a model's scores for its own answers against its scores for others' answers.
3. **But judge leniency is not netted out.** `y_self` is model M's score of M's own answer; `y_other` is the mean of other judges' scores of that same answer. A judge that is simply a generous scorer of everything will show a positive error rate without any self-preference at all. Table 5's raw score levels make this a live concern - Qwen2 gives 7.64 and ChatGPT 5.21, so the judges differ substantially in scale use. Figure 5's Z-score-normalised heat map appears to be the authors' answer to this, but the normalised values are not tabulated, so the reader cannot check whether the ranking survives normalisation. With N = 150, no significance testing, and this confound unquantified, I would treat **the direction of the effect as well supported and the magnitudes as indicative only**.

### Refinement-aware bias, the second Subject-relevant finding

Same table, with `ErrorRate_RA = y'_ref/y_ref - 1`, where `y_ref` is the score for the refined answer alone and `y'_ref` the score for the same refined answer accompanied by the history showing it was refined:

| Judge | Refined | Refined + history | Error |
|---|---|---|---|
| ChatGPT | 5.23 | 4.94 | -5.48% |
| GPT-4-Turbo | 8.31 | 8.45 | +1.69% |
| GPT-4o | 7.44 | 7.20 | -3.22% |
| GLM-4 | 7.64 | 7.73 | +1.19% |
| Claude-3.5 | 7.51 | 7.68 | +2.22% |
| Qwen2 | 7.29 | 7.39 | +1.35% |

The magnitudes here are small and the sign is inconsistent across judges, so on the numbers alone this is the weakest of the twelve effects. The **qualitative** finding is the valuable part, and the authors put it in the discussion rather than the results. Refinement-aware bias is their exemplar of an **implicit** bias: the judge "consistently scored refined answers higher, despite providing similar justifications for different instances and never explicitly mentioning refinement as a factor in its decision-making process." The case study in Figure 10 walks through a single item scoring 6 before refinement, 7 after, and 8 after refinement-with-history - the same text, scored a point higher purely because the judge could see it was the product of revision.

The explicit/implicit distinction is the paper's most useful conceptual contribution and it is barely a page long. Authority bias is the explicit archetype: the judge says out loud that it prefers the cited answer, so the reasoning trace exposes the bias. Refinement-aware is the implicit archetype: the score moves and the stated reasons do not change. The authors' conclusion is that "the disparity between their internal processing and expressed reasoning" means a judge's own explanation cannot be trusted to reveal why it decided what it decided.

### Bias is larger where quality differences are smaller

The authors observe that bias effects are consistently more pronounced on the alignment dataset than on the fact-related one, and give the explanation directly: on fact-related data the quality gap between the two answers is wide enough that a bias cannot close it, whereas alignment pairs are closer together and therefore easier to tip. This generalises to a rule that matters more than the individual bias numbers: **the closer the call, the more of the verdict is decided by presentation.**

### The camera-ready's BIS reshuffles the model ranking

Netting out the consistency floor (Table 7, lower is better), the average bias impact on the alignment set is ChatGPT 0.211, Qwen2 0.115, GPT-4o 0.121, GLM-4 0.100, Claude-3.5 0.086, and **GPT-4-Turbo 0.065**. By this metric GPT-4-Turbo, not Claude-3.5, is the least bias-affected judge on alignment data - which contradicts the main text's claim that "Claude-3.5 generally shows the greatest resilience to biases", a claim retained verbatim from the preprint. The mechanism is visible: GPT-4-Turbo has the worst baseline consistency (CR_Al = 0.856), so subtracting it flatters the model. That cuts both ways. BIS is the more honest metric for isolating bias, but it also rewards a judge for being unreliable to begin with, and for a harness that has to act on a verdict, raw RR is the number that matters. On the fact-related set the ordering is different again, with GPT-4o best (0.111) and Qwen2 worst (0.171).

The authors' own summary of all this is deliberately modest: advanced models are not uniformly better, the best judge depends on which bias you care about, and "even top-tier models may display unexpected weaknesses", so one should not assume the most capable model is the most reliable judge.

## Stance, format and position versus content

This is the accounting promised above, and I think it is the single most useful thing the paper's numbers support, even though the authors never assemble it themselves. Their own Table 2 tags each bias as Answers-Related, Semantic-Related, or Instruction-Influence, but they never compare the columns against each other. If you do compare them, a clear pattern falls out.

Only **one** of the twelve perturbations attacks the content of the reasoning: fallacy-oversight, where the logic inside the better answer is genuinely corrupted while its final answer stays right. That is the one the judges largely pass, at RR 0.917 to 0.985, with the four frontier judges above 0.96. Refinement-aware is the only other bias tagged Semantic-Related, and its measured magnitude is the smallest in the paper (-5.5% to +2.2%, sign inconsistent across judges).

Everything else is stance, format, provenance, or position, and that is where the failures are:

| What the perturbation touches | Bias | RR range across the six judges |
|---|---|---|
| Emotional register of the text | Sentiment, negative tone on the better answer | **0.238 - 0.659** |
| Ordering of the candidates | Position, pairwise | 0.566 - 0.832 |
| Ordering, three or four candidates | Position, exploratory | **mostly below 0.500** |
| Social cue in the instruction | Bandwagon | 0.610 - 0.791 |
| Fabricated citation in the answer | Authority | 0.662 - 0.865 |
| Irrelevant sentence in the instruction | Distraction | 0.713 - 0.878 |
| Asserted identity of the author | Diversity | 0.646 - 0.914 |
| Disclosed model names | Compassion-fade | 0.835 - 0.877 |
| Length of the worse answer | Verbosity | 0.884 - 0.977 |
| **Corrupted reasoning inside the answer** | **Fallacy-oversight** | **0.917 - 0.985** |

Read down that table and the ordering is close to monotone in how far the perturbation sits from the argument itself. Tone is the worst attack in the paper; corrupting the actual reasoning is the mildest. A judge that flips its verdict on 76 per cent of items because the better answer was rewritten in an angry register, but holds it on 98 per cent of items where the better answer's reasoning was made chaotic, is not reading the reasoning at all in any way that competes with reading the tone.

Two honest qualifications, because the accounting is not as clean as that summary makes it sound.

First, **verbosity is the counter-example**, and it is a format bias that the judges mostly resist (0.884 to 0.977, GPT-4o at 0.977). This cuts against a simple "all surface features dominate" story. The natural reading is that verbosity is the one surface bias that has been widely publicised and explicitly trained against since Zheng et al. (2024), while nobody has trained against sad prose. That is a claim about the state of RLHF rather than something the paper demonstrates, and I flag it as my inference, not theirs.

Second, **fallacy-oversight's inverted scoring makes its high number partly an artefact of the design**. Recall that under this bias a judge scores as correct by *changing* its verdict away from the corrupted answer. The baseline flip rate on this dataset is not zero, so some fraction of that 0.917 to 0.985 is judges flipping for unrelated reasons and being credited for it. The fact-related CR is 0.97 to 0.999, which bounds that contamination at a few points, so the conclusion survives - but the gap between fallacy-oversight and sentiment is somewhat smaller than the raw numbers imply.

With those caveats, the accounting holds: on the evidence in this paper, the overwhelming majority of the measured bias is stance, format, position, and provenance, and very little of it is content.

## Proposed mitigations, and whether any of them work

Mitigation is not the paper's main business. CALM is a measurement framework, and the mitigations appear as a short set of recommendations in the discussion, most of them untested. I list them in descending order of how much evidence backs them.

**1. Bias-detection prompting - the only mitigation with numbers attached.** The authors ran a small probe in which the judge is first asked, before judging, whether the input contains a bias attempt. Reported success rates are 84% for authority bias (both GPT-4-Turbo and Claude-3.5), 100% for the bandwagon effect with GPT-4-Turbo, and 92% with Claude-3.5. Three things limit how far this carries. It covers only two of the twelve biases, and specifically the two whose injected cue is a literal, quotable sentence in the prompt ("90% of people believe...", a fabricated citation) - exactly the case where detection is a string-matching task dressed as reasoning. It is a *detection* rate, not a demonstration that verdicts improve once the cue is detected; no post-mitigation RR is reported. And it is silent on precisely the biases where detection would have to do real work: there is no cue to spot in a sad rewrite, a permuted ordering, or a judge's implicit preference for its own prose. The authors' own explicit/implicit distinction predicts this mitigation should fail on the implicit half, and they do not test it there.

**2. Chain-of-thought - tested, and it barely helps.** CoT is the one intervention measured across all six judges, and it is measured as accuracy rather than robustness. The gains are small and uneven: +0.7% for GPT-4-Turbo, +7% for GLM-4, with post-CoT accuracies of 0.560 to 0.745 - meaning that even after CoT, the best judge in the study still disagrees with the ground truth on a quarter of alignment items. The authors are appropriately measured about this and do not oversell it. Note also that CoT is listed as one of the twelve *biases*, on the grounds that a judge whose verdict moves depending on whether it was asked to reason is thereby shown to be unstable. That framing sits awkwardly with recommending CoT as a fix, and the paper does not resolve the tension.

**3. Randomise or rotate the answer order.** Recommended for position bias, and it is the one recommendation that is obviously sound, since it converts a systematic error into a random one. It does not reduce the underlying order-sensitivity; it only stops that sensitivity from consistently favouring the same slot. Given that three- and four-candidate RR falls below 0.5, rotation turns a biased verdict into a coin flip rather than into a correct verdict. The paper does not report a rotation-averaged accuracy, which would have shown how much is recovered.

**4. Do not let a model judge its own output.** Stated flatly - "Avoid using the same model to generate and judge answers" - and it follows directly from the self-enhancement result. This is a design constraint rather than a mitigation, and it is untested in the sense that no experiment shows what a cross-model arrangement buys.

**5. Prompt hygiene and injection safeguards.** Protective phrasing in the judging instruction, plus guarding against untrusted material entering the prompt at all. Sensible, entirely untested here, and offered as advice.

**6. Pick the judge per bias.** Follows from the finding that no model dominates. The paper's practical version of this is that CALM itself is the selection instrument - run it on a candidate judge and read off the profile.

**The honest summary is that nothing in this paper is shown to fix anything.** One partial detection probe on two of twelve biases, one intervention with single-digit accuracy gains, and four pieces of untested advice. The authors say as much in their own register, framing the goal as mitigation rather than elimination and conceding on philosophical grounds that "all judgments inevitably carry some degree of subjectivity" and that absolute objectivity is unattainable. That is the paragraph I flagged in the density line as doing no work: it converts an empirical shortfall into an in-principle limit, which is a much stronger claim than their data supports and which happens to excuse the absence of a working mitigation.

## Open questions the paper itself raises

The paper has no Limitations section and no Future Work section, which is a real omission for an ICLR main-conference paper and worth recording plainly. The open questions therefore have to be read out of the discussion and conclusion, where they are posed rhetorically rather than listed. I separate the ones the authors actually raise from the ones I think are open, and I keep the latter for the concerns section below.

Raised by the authors:

1. **Whether implicit bias can be detected at all.** This is their sharpest question and it follows from their own refinement-aware result. If a judge's score moves while its stated justification does not change, then no method that inspects the judge's reasoning trace can find the bias. They state the problem - "the disparity between their internal processing and expressed reasoning" - and offer nothing for it.
2. **Whether LLM judges should inherit human cognitive biases or transcend them.** Posed via the affect heuristic (Slovic et al., 2002): the sentiment result looks like a machine analogue of a documented human bias, absorbed from human-generated training data. The authors leave open whether that is a defect to be engineered out or a property of any system trained to imitate human preference.
3. **Whether objectivity is achievable in principle.** Their philosophical paragraph concludes it is not, and redirects the field from elimination toward mitigation. I would call this a question they close rather than open, and close on argument rather than on evidence.
4. **Whether bias detection generalises.** This is implicit in the narrow scope of the detection probe; they report two biases and do not claim the method extends.
5. **What CALM should cover next.** The conclusion positions CALM as a standard to be applied to "future LLM-based judge solutions", which concedes that the twelve biases are a snapshot rather than a closed taxonomy. No criterion is given for what would make the list complete, or for how a thirteenth bias would be admitted to it.

Questions the results raise that the authors do not pick up:

6. **Why the weakest judge is the most robust to sentiment.** ChatGPT sits at 0.639 to 0.803 where the frontier models sit at 0.238 to 0.366. The paper notes the fact in one clause and moves on. If tone-sensitivity scales with capability, then the problem gets worse with every model generation, and that is a substantially more alarming reading of Table 8 than the one the paper gives.
7. **Whether self-enhancement survives netting out judge leniency.** Figure 5's Z-score-normalised map appears to address this, but it is not tabulated, so a reader cannot check it.
8. **What the judges' agreement with each other, or with humans, actually is.** It is never measured.

## Appreciation

I keep mechanism and magnitude apart here, because my confidence in the two is very different.

### Mechanism - strong, and the durable contribution

The attack-and-detect design is the real contribution and it is elegant. By perturbing the input in a way that is stipulated not to change the quality ordering, and then asking only whether the verdict moved, the paper converts an evaluation problem into a stability problem, and stability can be measured without anyone knowing which answer is better. Any flip is attributable to the injected feature by construction. This is a reusable idea well beyond judging: it is the same move as metamorphic testing, applied to an evaluator.

Three further mechanical strengths deserve credit.

The **consistency rate as a matched control** is the most methodologically serious thing in the paper. Running the same unperturbed comparison twice, on the same items, gives every robustness number a noise floor to be read against. Without it the alignment-side results would be uninterpretable, and the discovery that judges disagree with themselves on 7.5 to 14.4 per cent of unperturbed alignment items is a finding that the design produced almost as a by-product. The camera-ready's BIS then formalises the subtraction.

The **explicit/implicit distinction** is the paper's best conceptual idea, and it is under-developed relative to its importance. Authority bias is visible in the judge's own stated reasoning; refinement-aware bias is not, because the justification text stays constant while the score moves. That distinction cuts straight across any proposal to audit a judge by reading what it says about its own decision.

The **directional and bidirectional controls** are better than the field's norm. Sentiment is applied separately to the better and to the worse answer, which is what turns "judges are sensitive to emotion" into the much sharper "judges are averse to a negative tone in a good answer and indifferent to it in a bad one". Distraction is run toward both the good and the bad answer. Authority is broken into three citation formats. Bandwagon is swept across four intensity levels, and the finding that intensity has no monotone effect is only available because the sweep was run. This is careful experimental design, and it is where most of the paper's real information lives.

The **anonymisation in the self-enhancement condition** is the right control, and it is what makes that result interesting rather than trivial. A judge that is told "this is your own answer" and then prefers it would be unremarkable; a judge that prefers its own uncredited text is a different and more troubling phenomenon.

### Magnitude - weak, and I would not quote most of these numbers

The specific figures are indicative at best, for reasons that compound.

There is **no statistical treatment of any kind**: no confidence intervals, no error bars, no seeds, no variance, no significance tests. Cells rest on 150 to 500 items, apparently one run each, at **temperature 0.7** - a strange setting for a study whose dependent variable is decision stability, and one that inflates every flip rate by an unmeasured amount. The CR column bounds that inflation but does not remove it.

The **N is smallest exactly where the paper's most-cited claims live.** Bandwagon, authority, diversity, and self-enhancement all rest on 150 items. Self-enhancement is the result most likely to be quoted, it is measured on the smallest sample, it has an unquantified leniency confound, and one of its six rows is disowned by the authors themselves as lacking reference value.

**Cross-model comparisons are not supported by the data.** Differences of a few points between judges are freely narrated as rankings, and the camera-ready's own BIS metric contradicts the main text's retained claim that Claude-3.5 is the most resilient judge. When a paper's two metrics disagree about its headline model ranking, and the text is not updated to reflect that, the ranking is not a finding.

**Ground truth is not what the framework claims it is.** The selling point is that CALM needs no human assessment. In fact the alignment ground truth is inherited human preference annotation from DPO datasets, and the fact-related quality ordering is asserted by GPT-4-Turbo, which also wrote both answers and performs every rewrite. GPT-4-Turbo is simultaneously a generator, the perturbation engine, and one of the six judges. Human labour has been moved, and partly replaced by a model whose reliability is the paper's own subject; it has not been eliminated. Appendix F's human study, which is good, validates the perturbations rather than the judgments.

What I would carry forward with confidence is the **ordering and the sign** of the effects, and not their values: a negative tone in a good answer is a severe attack; position sensitivity is severe and it worsens as candidates are added; instruction-side social cues are moderate; most judges inflate their own work; corrupted reasoning is the thing judges catch best. Every one of those is large enough relative to the consistency floor to survive the methodological slack. The two-decimal numbers are not.

## How it could serve a harness-design effort, with limitations and major concerns

### What transfers to the Subject

The Subject is a system that repeatedly decides whether its current attempt has succeeded, is stalling, or should be abandoned. This paper is not about that. It is about a judge comparing two static answers to a fixed question, in a single turn, with no trajectory, no budget, and no stopping decision anywhere in it. Everything below is therefore transfer by argument rather than by demonstration, and I try to mark how far each step reaches.

**1. The self-enhancement number is the most directly relevant result, and it bounds how much a self-report can be trusted.** Five of six judges inflate their own work by 3.6 to 9.4 per cent on a ten-point scale, and they do so with authorship anonymised, so this is not vanity about a byline - it is something closer to a model finding its own output maximally legible. A loop in which the model both produces the attempt and rates it is running exactly this configuration, minus the anonymisation, which should make it worse rather than better. The authors' recommendation - do not let the same model generate and judge - is the paper's clearest instruction to a harness designer. The honest qualification is that a few per cent on a ten-point scale is a small effect, measured on 150 items, with judge leniency not netted out; it argues for not relying on a self-score alone, and it does not by itself justify any particular threshold.

**2. Refinement-aware bias maps onto iterative loops almost exactly, and it is the finding I would most want followed up.** A judge shown the same text twice, once bare and once with the history revealing that it was a revision, scores the revision higher. The case study moves a single item from 7 to 8 on visible revision history alone. An agent loop is a machine for producing exactly that input: attempt N+1 always arrives accompanied by the visible history of attempts 1 through N. If the judge is systematically warmer toward text that is presented as the product of revision, then an iterating loop drifts toward premature satisfaction, and it does so more strongly the longer it has been iterating. The paper's measured magnitudes are small and their sign is inconsistent across judges, so this is a mechanism worth taking seriously and a number not worth quoting.

**3. The implicit-bias result undercuts reading the judge's reasoning.** A common harness pattern is to have the evaluator explain itself and then to inspect or gate on the explanation. The refinement-aware finding is that the score moved while the justifications stayed "similar... never explicitly mentioning refinement as a factor". A stated rationale is therefore not evidence about what actually drove the verdict. This is the paper's most consequential negative result for harness design, and it is one paragraph long.

**4. The stance-versus-content accounting says what a judge is actually reading.** Judges hold their verdict on 92 to 98 per cent of items when the reasoning inside the better answer is corrupted, and lose it on up to 76 per cent when that same answer is rewritten in an angry or fearful register. For a harness this suggests, though it does not prove, that the tone in which a status report is written may carry more weight with an evaluating model than the substance of what the report says. A component that reports failure candidly, or in an alarmed register, may be penalised for the register. If that transfers, the mitigation is mechanical rather than clever: strip or normalise the register of anything that goes to a judge, and keep the evaluator's input as close to a bare artefact as the task allows.

**5. Position sensitivity constrains any ranking-based routing.** Pairwise RR of 0.566 to 0.832, dropping below 0.5 with three or four candidates, means a harness that asks a model to pick the best among several attempts is getting a verdict that mostly does not survive re-ordering. Rotation converts that into random error rather than removing it.

**6. The consistency-rate finding is the most immediately actionable number in the paper, and it is not about bias at all.** Judges disagree with themselves on 7.5 to 14.4 per cent of unperturbed items on subjective data, at temperature 0.7. Before any bias is considered, a single judge call on an open-ended question is that unstable. Any harness that gates a decision on one such call is gating on a noisy variable, and the paper's own design - always run the unperturbed comparison twice - is a cheap instrument that a harness could adopt directly as a self-check.

**7. The closer the call, the more presentation decides it.** Bias effects are consistently larger on the alignment set than on the fact-related set, because a wide quality gap cannot be closed by a surface feature. The practical reading is that a judge is most trustworthy where the answer is nearly checkable, and least trustworthy where it is genuinely open - which is precisely where a harness would want to lean on a judge instead of a test.

**8. CALM as an instrument rather than as a result.** The most robust thing to take from this paper may be the method rather than the numbers. Perturb the input in a way that must not change the correct verdict, and measure whether the verdict moves. A harness could run that against its own evaluator on its own task distribution, and would get a calibration figure that is specific to it rather than borrowed from a mid-2024 model list.

### Limitations and major concerns

- **Nothing here is agentic.** Single-turn, two-answer comparison of static text. No trajectory, no tool use, no multi-step attempt, no budget, no stopping decision, no abandonment. Every application above is an argument, not a measurement.
- **The models are a mid-2024 snapshot** and four of the six are now several generations old. The bias magnitudes have a short shelf life. The sentiment result carries a hint that the problem worsens with capability, but that is an inference from one data point (ChatGPT's outlier robustness), not a trend line.
- **No agreement study anywhere.** No inter-judge agreement on unperturbed items, no human-judge agreement baseline, no inter-annotator agreement on answer quality. The only human study validates the perturbations, not the verdicts, and it covers only ten of the many conditions.
- **The no-human-labels claim does not hold up.** Ground truth is inherited from DPO human annotations on one dataset and asserted by GPT-4-Turbo on the other. GPT-4-Turbo is generator, perturbation engine, and judge at once.
- **No statistics.** Discussed above; it is the paper's most serious defect, and it is why the model rankings should be ignored.
- **Two of the twelve categories are not biases in the same sense as the others.** CoT measures whether a prompt change improves accuracy, and it is the one item scored against ground truth rather than by flip rate; recommending it as a mitigation while listing it as a bias is unresolved. Fallacy-oversight inverts its scoring rule, which is correct but easy to misread and partly inflates its own headline number.
- **Only capable judges are tested.** The stated rationale is that weak judges are merely noisy. The consequence is that the paper says nothing about the small, cheap models a cost-conscious harness would actually put in an inner loop, which is the deployment case that matters most.
- **The self-enhancement result rests on 150 items with an unquantified confound.** Direction well supported; magnitude indicative only.
- **No mitigation is demonstrated to work.** One detection probe on the two easiest biases, reporting detection rather than improved verdicts; CoT with single-digit gains; four pieces of untested advice. A harness designer takes constraints away from this paper, not remedies.

## Five citations worth chasing next

1. **Zheng et al. (2024), "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena."** The foundational reference for the whole area and the source of the judging prompts this paper adapts. It is also where position bias and self-enhancement bias were first named and measured, and where a judge-human agreement baseline is actually reported - the exact thing CALM omits. Read it for the agreement numbers this paper does not have.
2. **Koo et al. (2023), "Benchmarking Cognitive Biases in Large Language Models as Evaluators."** The nearest prior work and the most direct comparison for CALM's taxonomy. Worth reading to see which of the twelve biases are genuinely new here and which are relabelled, and to see whether its methodology treats significance any better.
3. **Wu and Aji (2023), "Style over Substance: Evaluation Biases for Large Language Models."** This goes straight at the stance-versus-content question that the present paper's numbers imply but never states. If the finding that presentation outweighs substance holds up in an independent study with a different method, that is the most transferable conclusion in this area.
4. **Chen et al. (2024c), "Humans or LLMs as the Judge? A Study on Judgement Biases."** The paper that puts human judges and LLM judges under the same lens. Since the present paper deliberately removes humans from the loop and thereby loses any human baseline, this is the complement, and it is the way to find out whether these biases are machine defects or inherited human ones - the question the affect-heuristic digression raises and does not answer.
5. **Shi et al. (2024a), "Optimization-Based Prompt Injection Attack to LLM-as-a-Judge."** CALM's instruction-side perturbations are hand-written templates. This is the adversarial-optimisation version of the same attack surface, and it gives the upper bound on what a determined attacker gets, where CALM gives the floor. For any harness whose evaluator sees untrusted text, the optimised bound is the relevant number.
