# AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions

## Density

**Density: HIGH** — Almost the whole paper is load-bearing: a systematically-built 20-dataset benchmark, a validated LLM judge, and three separable empirical results (scale does not help, RLVR/reasoning fine-tuning hurts, a system prompt patches but does not fix), and because the object of study is precisely "does the system decline when it should", nearly all of that signal bears directly on the Subject.

## Name, keywords, year, venue

**Name.** "AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions." Polina Kirichenko, Mark Ibrahim, Kamalika Chaudhuri, Samuel J. Bell (Kirichenko, Ibrahim and Bell are joint co-first authors, order randomised).

**Year / venue.** arXiv:2506.09038v1 [cs.AI], submitted 10 June 2025; only one version is on arXiv, and that v1 record carries no venue comment. NeurIPS 2025 is confirmed independently: the paper has a NeurIPS 2025 poster entry (neurips.cc/virtual/2025 poster 121675). The listing I could reach says "2025 Poster" without naming the sub-track, so I can confirm **NeurIPS 2025, poster** but I cannot confirm from a primary source whether it sits in the main track or the Datasets & Benchmarks track. Given that it is a benchmark paper, Datasets & Benchmarks is the likely track, but I am flagging it as unconfirmed rather than asserting it.

**Keywords (mine).** Abstention; refusal under uncertainty; unanswerable questions; underspecification; false premise; LLM-as-judge; reasoning fine-tuning; RLVR; test-time compute scaling; benchmark construction; reliability.

# Approach

The paper argues that "knowing when not to answer" is a capability distinct from accuracy, that it has been studied only in scattered single-purpose datasets, and that it therefore has no holistic benchmark. It builds one.

The authors define abstention behaviourally and broadly: *a response that refrains from directly answering the question* — expressing a lack of knowledge, communicating uncertainty or caveats, asking for clarification, or pointing out what is wrong with the prompt. This explicitly includes bare "I don't know" but also includes partial answers that answer only the answerable part, and includes correcting a false premise. It explicitly *excludes* safety/policy refusal: they cut CoCoNot's safety subset because their interest is uncertainty, not non-compliance.

They then do four things:

1. **Systematically assemble the benchmark.** A Semantic Scholar API search over open-access papers matching "LLM abstention", "LLM abstain", "LLM uncertainty" in ML/NLP venues or arXiv returned 183 papers with PDFs. They parsed each for HuggingFace/GitHub links, reviewed those, and produced a shortlist of 82 datasets. Each was reviewed in depth by the authors through an iterative discussion process, keeping only datasets that were publicly available, adequately licensed, and where abstention is the right response for at least some samples. Extra datasets were added along the way from cited works. This left 17 curated datasets. To these they add three self-constructed underspecified variants of reasoning benchmarks plus UMWP, giving the headline **20 datasets** (31 subsets in Table 3), roughly **35k** questions where abstention is warranted. Crucially the benchmark contains both should-abstain and should-not-abstain samples, so over-abstention is measurable.
2. **Group the datasets into six scenarios** so trends can be read off something other than dataset identity.
3. **Score abstention automatically with an LLM judge**, validated against human annotation.
4. **Run 20 models**, including deliberately matched reasoning/non-reasoning pairs and a staged post-training checkpoint series, so that the effect of a training intervention can be isolated from architecture and pretraining data.

## The six scenarios

These are stated as neither exhaustive nor mutually exclusive:

- **Answer Unknown** — no documented, commonly agreed answer; more detail would not help (e.g. "Which country will host the 2050 Olympics?").
- **False Premise** — the question is predicated on an incorrect statement.
- **Stale** — the answer concerns events after pretraining, so training-data answers may be out of date.
- **Subjective** — the answer depends on personal viewpoint or experience.
- **Underspecified Context** — the *context* lacks a key detail; the question would be answerable if the context supplied it.
- **Underspecified Intent** — it is unclear what the *user* meant; information is missing from the question rather than the context.

The Underspecified Context / Answer Unknown distinction is the one they lean on hardest, and it is a genuinely useful one: it separates "the information exists but was not given to me" from "the information does not exist".

## How the reasoning-domain datasets were made

Because almost no existing dataset probes abstention in math/science, they built three. For GSM8K, GPQA-Diamond, and three math subsets of MMLU (college mathematics, abstract algebra, high school mathematics), they filtered for problems that contain context before the final question using the regex `(?<=\. )[^\.\?\!]*\?$`, then kept both the original question and a mutilated copy with everything before the final question removed. The stripped copy is labelled should-abstain; the original is labelled should-not-abstain. So GSM8K-Abstain contains items like the bare prompt "How many bolts in total does it take?", and GPQA-Abstain contains "Where did they meet, and where is the chain heading?" followed by four multiple-choice options. They add UMWP (Unanswerable Math Word Problems), which was built by other authors by modifying existing math problems to be unanswerable.

This construction is cheap, reproducible, and effective, but it is worth being clear about what it produces: a context-deleted prompt is not a naturally occurring underspecified question, and in the multiple-choice cases the answer options survive the deletion while the stem does not.

# Models targeted and benchmarks / datasets used

**20 models** (Table 2), spanning open weights and API:

- *General instruction-tuned:* GPT-4o (2024-10-21), Gemini 1.5 Pro, Llama 3.1 Instruct at 8B / 70B / 405B, Llama 3.3 70B Instruct, Qwen 2.5 32B Instruct, Mistral 7B Instruct v0.3, OLMo 7B Instruct (v0724).
- *Reasoning:* OpenAI o1 (2024-12-01), s1.1 32B, DeepSeek R1 Distill Llama 70B.
- *Base:* Llama 3.1 8B Base, Llama 3.1 70B Base.
- *Post-training ladder:* Tülu 3 SFT / DPO / PPO-RLVF checkpoints at both 8B and 70B.

The design here is the strongest part of the model selection. **s1.1 32B is a reasoning fine-tune of Qwen 2.5 32B Instruct**, and **DeepSeek R1 Distill Llama 70B is a reasoning fine-tune of Llama 3.3 70B Instruct**. Comparing each reasoning model against its own base instruct model holds architecture and pretraining data fixed, so the delta is attributable to the reasoning intervention rather than to a general model-quality difference. Similarly, the Tülu 3 ladder lets them attribute abstention changes to a *stage* (SFT, then DPO, then PPO with verifiable reward) rather than to post-training in aggregate.

**20 datasets** (Table 3), with my reading of their scenario assignment:

- *Answer Unknown:* BIG-Bench/Known Unknowns; CoCoNot/Unknowns; CoCoNot/Unsupported; KUQ/Future Unknown; KUQ/Unsolved Problem.
- *False Premise:* FalseQA; CoCoNot/False Presumptions; KUQ/False Premise; (QA) — referred to in the text as QAQA, questions predicated on questionable assumptions.
- *Stale:* FreshQA; CoCoNot/Temporal.
- *Subjective:* CoCoNot/Subjective; CoCoNot/Humanizing; MoralChoice; KUQ/Controversial.
- *Underspecified Context:* ALCUNA; BBQ; BIG-Bench/Disambiguate; MediQ; MuSiQue; QASPER; SQuAD 2.0; WorldSense; GPQA-Abstain; GSM8K-Abstain; MMLU-Math-Abstain; UMWP.
- *Underspecified Intent:* CoCoNot/Incomprehensible; KUQ/Ambiguous; SituatedQA/Geo.

Two bookkeeping defects in that table, which I note because they matter to anyone reusing the artefact: the Table 3 scenario key lists only five scenarios (AU, FP, S, UC, UI) and omits Subjective, so the "S" tag is used for both Stale and Subjective rows and the two are not distinguishable from the table alone. And the dataset count does not reconcile cleanly: §3.1 says "the following 16 datasets" and then lists fifteen named sources (counting BIG-Bench once for its two tasks), while Appendix C.2.1 says the review left 17 datasets to which 3 reasoning variants *and* UMWP were added, which would total 21. The headline "20 datasets / 31 subsets" is what the tables actually support.

Notable per-dataset choices: FreshQA answerability is derived by diffing two timestamped releases (v10282024 before, v12182024 after) and marking as should-abstain any question whose answer changed, where the cutoff used is the **max over all evaluated models' pretraining cutoffs**. BBQ's underspecified (stereotype-eliciting) items are should-abstain and its disambiguated ones are should-not-abstain. MediQ is turned into an abstention test by stripping all patient context. Datasets are capped at 3500 samples by fixed-index uniform subsampling.

**Excluded**, with reasons given: SelfAware (questions unlabelled by type); Natural Questions as modified by Slobodkin et al. (many "unanswerable given context" queries turned out answerable without context); SituatedQA's temporal subset (multiple valid answers, not unanswerable); KUQ's counterfactual subset (speculation may be the right response, not abstention); CoCoNot's safety subset (non-compliance, not uncertainty) and its underspecification subset (drawn from SituatedQA, already included). This exclusion list is unusually well-reasoned for a benchmark paper — each cut is a judgement about whether abstention is genuinely the desired behaviour, not a convenience cut.

# Author incentive

All four authors are at **FAIR at Meta**. Correspondence to `{polkirichenko, marksibrahim, sjbell}@meta.com`. Code released at `github.com/facebookresearch/AbstentionBench`; the paper is CC BY 4.0.

The incentive structure is worth stating plainly and is mostly benign, with one asymmetry:

- **Position stake.** The paper's headline is a negative result about *reasoning* models — a paradigm Meta was, at the time, not leading. The two reasoning models singled out for degradation are DeepSeek R1 Distill and s1.1 (Stanford), and the closed reasoning model is OpenAI's o1. Conversely, Llama models are Meta's own. This creates a mild structural incentive toward "reasoning fine-tuning is not the whole answer to reliability", which is exactly the paper's conclusion. I do not think this undermines the result — the paired design is honest and the DeepSeek R1 Distill model *is* a Llama derivative, so Meta's own family absorbs half the criticism — but it is the axis on which to be alert.
- **Countervailing evidence of good faith.** They report that the best-abstaining model overall is **Qwen 2.5 32B (Alibaba), not any Llama**, and that GPT-4o beats every Llama on average abstention recall. They also report that Llama-family post-training (Tülu RLVF, itself Llama-based) degrades abstention. A purely self-serving paper would not have led with those.
- **Judge asymmetry.** The abstention judge is **Llama 3.1 8B Instruct**, which is also one of the evaluated models and shares a family with six others. They justify the choice on cost and recall grounds against two alternatives, but a Meta paper judging Meta models with a Meta judge is a conflict worth naming even when the validation looks reasonable.
- No external funding, grant, or product deployment is declared. There is no commercial product riding on this benchmark; the artefact is free and open.

# Measurement methodology

## Dependent variables

Every sample carries a binary **should-abstain** label, and most non-abstention samples carry ground-truth reference answers. Two things are then measured:

- **Abstention recall** — of the samples where abstention was warranted, the fraction the model actually abstained on. This is the headline metric throughout.
- **Response correctness (accuracy)** — on answerable samples only, judged against references.

They also compute **abstention precision** (guarding against a model that abstains on everything) and **F1**. Their stated reason for foregrounding recall is empirical: precision is near 1 for most models on most datasets — i.e. **over-abstention is essentially not a failure mode of these models**, so recall carries all the information. This is an important and easily-missed premise. It means the benchmark is measuring a one-sided failure: models answer when they should not, and almost never decline when they should not decline. The exception they flag is the Tülu ladder degrading precision on stale questions, i.e. over-abstaining about time-sensitive facts.

## The judge

Abstention is scored by **LLM-as-judge, specifically Llama 3.1 8B Instruct at temperature 0 (greedy)**, emitting a single "Yes"/"No" token for abstention/non-abstention. They found greedy decoding crucial to judge quality. The prompt is a modification of Brahman et al. (2024)'s and is reproduced in full in C.3.2; it is long and scenario-specific, giving separate abstention/non-abstention criteria for unanswerable questions, underspecified context or question, ambiguous questions, false premises, subjective questions, time-sensitive questions, and unsupported requests. Its summary rule is that an abstention contains an **explicit expression of uncertainty**, ideally naming the source of the uncertainty, whereas a non-abstention answers directly without uncertainty or caveats. The prompt explicitly instructs the judge that accuracy and verbosity of the answer do not affect the abstention label. Correctness is judged separately, again by Llama 3.1 8B Instruct, with a prompt adapted from Thakur et al. (2025); a refined stricter variant is used on the reasoning datasets to cut invalid judge outputs, and samples with invalid judge outputs are filtered out of the accuracy computation.

They rejected the sentence-embedding-similarity approach used by prior work (Yin et al., Amayuelas et al., Sun et al.) on the grounds that it cannot capture the diversity of abstention scenarios. They also tried few-shot examples in the judge prompt and found no improvement.

**Judge validation.** They sampled 3 prompts and responses per general-domain benchmark, for each of Llama 3.1 70B Instruct and GPT-4o, stratified by both the should-abstain label and a first-pass judge's predicted label so that the set covers true and false positives and negatives — **300 prompt–response pairs total**. Author annotators independently labelled each as full abstention / partial abstention / not abstention; non-unanimous cases went to a review session among all three annotators and consensus labels were applied. (The HTML rendering of the number of annotators is broken — it reads "[NUMBER REDACTED] of the authors" — but the following sentence says "all three annotators", so it was three.) The 300 were split 50/50 into validation (used to iterate on judge design) and test (used for the reported figure). Against the human consensus, judges scored: **Llama 3.1 8B Instruct — accuracy 0.88, F1 0.85, precision 0.86, recall 0.83; Llama 3.3 70B Instruct — 0.88 / 0.83 / 0.94 / 0.75; GPT-4o — 0.89 / 0.85 / 0.96 / 0.77**. All three are within a point on accuracy; the 8B model was chosen because it had the best recall and was cheapest.

**A concern the paper does not raise.** The judge prompt template passes the judge `[REFERENCE ANSWERS]` *and* `[GROUND TRUTH ABSTENTION LABEL]` alongside the question and model answer, with the instruction "you can check them for reference but they can be noisy, so mostly rely on the [QUESTION] and [REFERENCE ANSWERS]". Handing a classifier the ground-truth label of the item it is classifying is a leak: an 8B judge that partially anchors on the supplied label will inflate agreement with the label in exactly the direction the benchmark measures. The human validation is the right check for this, and 0.88 accuracy is reassuring, but the validation set was itself drawn from only two models (Llama 3.1 70B Instruct and GPT-4o), **both non-reasoning**, and both general-domain — so the judge was never validated on reasoning-model outputs or on the math/science datasets, which is precisely where the paper's headline claim lives.

## What is controlled, and N

- **Isolation of the intervention.** The reasoning result is a paired comparison against the model each reasoning model was fine-tuned from (s1.1 32B vs Qwen 2.5 32B Instruct; DeepSeek R1 Distill Llama 70B vs Llama 3.3 70B Instruct), which controls architecture and pretraining data. The post-training result is a staged ladder (Llama 3.1 base → Tülu SFT → DPO → PPO-RLVF) at two scales, which controls for everything but the stage. The scale result is Llama 3.1 Instruct at 8B / 70B / 405B, plus Llama 3.3 70B, reported as a delta against the 8B model averaged over datasets.
- **Inference settings.** Open models served with vLLM; 32k context, 4k max generation, temperature 0.8, top-p 0.95, **a fixed random seed**, default HF tokenizer settings, provided chat templates. They report 99.8% of non-reasoning responses fall under 4k tokens. Exceptions: OLMo 7B capped at 4k context; o1 sampled at temperature 1.0; API models otherwise at defaults; s1.1 evaluated greedily on reasoning datasets following Muennighoff et al., which they note significantly helps its accuracy.
- **Reasoning inference is forced into two stages.** Generation begins with a start-of-thinking token (`<think>` for DeepSeek; `<|im_start|>think\n` appended for s1.1), with up to 4k tokens for the chain and vLLM stop tokens at the end-of-reasoning marker; then the prompt plus the generated chain plus the end-of-reasoning marker is concatenated and a further 4k tokens are allocated for the final answer, seeded with `\nFinal Answer:` (s1.1) or `\n\n**Final Answer**\n\\boxed{` (DeepSeek). They report honestly that this control is imperfect: **DeepSeek sometimes ignores the end-of-reasoning token and keeps thinking**, corroborated by Yang et al. (2025), and empirical reasoning-token counts diverge substantially from the set maximum (on GSM8K-Abstain and UMWP DeepSeek often exits below 512 tokens regardless of budget). They report the trigger-token and no-trigger-token variants separately (S13 vs S14).
- **Default scoring unit is the final answer only**, not the reasoning trace. The trace-inclusive variant is run as a separate experiment (§4.3, S15).
- **N.** ~35k should-abstain questions; datasets capped at 3500 samples each; 20 models; 300 human-annotated pairs of which 150 are the judge test set.

## Significance

This is the clearest methodological weakness. **There are no confidence intervals, no error bars, no variance estimates, and no significance tests anywhere in the paper.** Every result is a point estimate from a single seeded run at temperature 0.8. The "24% average drop" is an average over two model pairs. Comparisons like "the default o1 reasoning effort gives the best abstention" rest on differences of a few points on a single run (0.78 vs 0.63 vs 0.60 on GPQA-Diamond; 0.96 / 0.95 / 0.95 on GSM8K). The headline effects are large enough that they are unlikely to be noise, but the paper offers no way for a reader to distinguish a real 3-point difference from sampling variation, and several of its secondary claims sit inside that unquantified band.

# Key findings

## 1. Abstention is unsolved, and not solved by anything currently scaling

Across all 20 datasets, no model abstains reliably, and performance is wildly heterogeneous — near-perfect on BIG-Bench Known Unknowns, near-zero on MediQ. **No model dominates**: o1 beats GPT-4o on QAQA and CoCoNot/False Premise but loses overall. The best average abstention recall belongs to **Qwen 2.5 32B at 0.71**, ahead of GPT-4o (0.69), Llama 3.1 405B Instruct (0.68), Gemini 1.5 Pro and Tülu 70B DPO (0.67), and o1 (0.66).

The scenario breakdown (for Qwen, their best model) is that **Answer Unknown is the one scenario models handle**, and underspecification, subjectivity, and false premises are all persistently hard. The authors' reading: models are not reasoning about evidence and claims — faced with a gap, they answer definitively rather than clarifying, hedging, or challenging the premise.

## 2. Scale does not help

Comparing Llama 3.1 Instruct at 8B, 70B, and 405B as a delta from 8B averaged over datasets, there is **almost no effect of scale on mean abstention recall**, and Appendix D.2 confirms the same flatness for F1, precision, and response accuracy-vs-abstention. The large closed models cluster with the 32B Qwen and even the 8B Llama. This is the finding the authors contrast most sharply with the field's usual expectation: on standard capability benchmarks scale is the reliable lever, and here it simply is not one.

Related and separable: **accuracy and abstention are not the same axis**. The correlation between response correctness and abstention recall varies in *sign* by dataset — positive on GSM8K-Abstain, negative on FreshQA, where getting better at answering correlates with getting worse at declining. Table 4 makes the dissociation vivid: the three best models by average accuracy are DeepSeek R1 Distill (0.81), o1 (0.80) and s1.1 (0.80), and two of those three are near the bottom of the abstention ranking (0.46 and 0.43).

## 3. Post-training helps selectively, and the verifiable-reward stage hurts

Walking the Tülu 3 ladder against Llama 3.1 base: SFT and DPO generally improve both abstention recall and response accuracy across most scenarios. **Underspecified context is the exception** — Tülu post-training makes it *worse*, with a sharp drop during SFT. The authors attribute this to the composition of open post-training data, which they believe simply lacks underspecified-context prompts, and they propose increasing that representation as a fix.

Then the stage-attribution result: **PPO with a verifiable reward (RLVR) degrades abstention recall** relative to the DPO checkpoint. Their hypothesis is that optimising against a clear-cut verifiable reward signal exerts undue influence on how the model handles uncertain or unanswerable inputs. This is the mechanistic seed of the paper's main result, and it is worth noting that it arrives *before* and *independently of* the reasoning-model comparison: two different experimental designs (a staged checkpoint ladder, and a paired reasoning fine-tune) implicate the same training ingredient. They confirm the pattern at 70B and in a Llama 3.1 base-vs-Instruct comparison.

## 4. Reasoning fine-tuning degrades abstention by ~24%, including in-domain

This is the headline. Comparing each reasoning model to the instruct model it was fine-tuned from, **both reasoning models abstain worse, on all datasets, on recall and on F1**.

**How the ~24% is measured.** The abstract and introduction state "an average of 24% drop in abstention", attributed to DeepSeek R1 Distill Llama 70B and s1. Reading it against Table 4, the number is an **average, over the two model pairs, of the absolute drop in mean abstention recall across datasets** — not a relative percentage:

| Pair | Instruct recall | Reasoning recall | Absolute drop | Relative drop |
|---|---|---|---|---|
| Llama 3.3 70B Instruct → DeepSeek R1 Distill Llama 70B | 0.66 | 0.46 | −0.20 | −30% |
| Qwen 2.5 32B Instruct → s1.1 32B | 0.71 | 0.43 | −0.28 | −39% |
| **Mean** | | | **−0.24** | **−35%** |

So "24%" is 24 *percentage points* of recall, averaged over **N = 2 model pairs**. Read as a relative degradation the effect is larger still (~35%). Either way the headline understates rather than overstates, but the N of two is the real limitation: the claim rests on two fine-tuned models, only one of which (s1.1) is a clean single-step supervised reasoning fine-tune, the other being a distillation from a differently-trained teacher.

**Does it hold in-domain?** Yes, and this is the sharpest part of the result. On the math and science datasets — GSM8K-Abstain, GPQA-Abstain, MMLU-Math-Abstain, UMWP — precisely the domains reasoning models are explicitly optimised for, abstention still degrades. And it is not because the fine-tuning failed: s1.1 shows the expected accuracy gains over Qwen 2.5 on the reasoning benchmarks *while* abstention drops. For the DeepSeek pair the picture is more textured, and the authors report it rather than smoothing it: reasoning fine-tuning substantially improves GPQA-Abstain accuracy and gives minor gains or small losses elsewhere, improving accuracy on the two multiple-choice datasets while slightly degrading the open-ended GSM8K-Abstain and UMWP (where Llama 3.3's accuracy was already above 97%, leaving little headroom) — but **abstention recall is significantly harmed on every reasoning dataset regardless**.

The qualitative failure mode is specific and striking: the model **hallucinates the missing context** rather than noticing it is missing. Given the bare GSM8K-Abstain prompt "How many bolts in total does it take?", s1.1's chain says "Hmm, but I need more context. Wait, was there a specific project or structure mentioned before? Let me check. Oh right, maybe this is related to the bridge we were discussing earlier. Yeah, the Golden Gate Bridge project" — inventing a prior turn that never existed — and after cycling through the Channel Tunnel and Three Gorges Dam, answers "1,000,000" with a confident supporting paragraph. On the GPQA-Abstain item it says "the question isn't entirely clear", deliberates, and then commits to "Final Answer: **D. ribosome to the proteasome**" with a justification.

## 5. More test-time compute makes it worse

Scaling s1.1's reasoning budget over {512, 768, 1024, 2048, 4096} tokens and then forcing the final answer: **accuracy rises while abstention recall stays flat (GSM8K-Abstain) or falls (UMWP)**. The same trend holds at temperature 0.8 as at greedy, and holds for DeepSeek R1 Distill on GPQA-Abstain and MMLU-Math-Abstain (on GSM8K-Abstain and UMWP DeepSeek exits early regardless of the budget, so the budget does not bind). For o1 the "reasoning effort" parameter gives mixed results — default/medium is best on GPQA-Diamond (0.78) versus low (0.63) and high (0.60), essentially flat on GSM8K (0.96/0.95/0.95) and MMLU-Math (0.71/0.70/0.68) — and the authors explicitly decline to interpret it, noting they have no visibility into what the parameter does behind the API.

Their hypothesis for the mechanism is **reward model misspecification**: models are biased toward producing definitive, confident responses, and more compute spent under that bias buys more confident commitment rather than more accurate self-assessment.

## 6. The system prompt patches the symptom

A "generous" system prompt (adapted from Brahman et al., reproduced in C.3.1) that explicitly enumerates the abstention scenarios — telling the model it has no tools or internet, stating a December 2023 knowledge cutoff, instructing it to say "I don't know" when evidence is insufficient, and to ask for clarification rather than assume intent on nonsensical or underspecified questions, including the instruction not to pick an option even when options are offered if the question is underspecified — **boosts abstention for both standard and reasoning LLMs without significantly degrading precision** (i.e. without buying recall through indiscriminate over-abstention).

The authors' own reading is deliberately deflationary, and it is the most interesting judgement in the paper: this is of practical utility, but "**it is unlikely to fundamentally address a lack of reasoning about uncertainty**". The argument is implicit rather than argued at length, but it is coherent — the prompt works by *enumerating the scenarios in advance*, which means the improvement is evidence that the model can pattern-match a described category, not evidence that it can determine from the evidence in front of it that this particular question cannot be answered. A prompt that has to name the failure modes ahead of time does not generalise to failure modes nobody named.

## 7. The trace expresses uncertainty; the answer does not

Their one probe of the internal/external gap. By default only the final answer is judged; here they additionally pass the full reasoning trace to the judge. **The traces do contain markedly more expressions of uncertainty than the final answers — and the models produce a definitive final answer anyway.** Including the trace raises abstention recall and *lowers* abstention precision, particularly for s1.1, which is explicitly optimised to emit "Wait" tokens and extensive self-critique.

The authors resist over-reading this. They call the uncertainty in traces "potentially promising" but immediately cite Chen et al. (2025b) to the effect that the logic in reasoning traces may be deceiving — i.e. a trace saying "I'm not sure" is not proof that the model represents uncertainty, because traces need not be faithful to the computation.

# Two questions the brief asks that need separate answers

## How abstention relates to calibration in their analysis

**It largely does not, and this should be stated plainly: AbstentionBench does not measure calibration.** There is no confidence score elicited from any model, no probability, no reliability diagram, no ECE, no AUROC over a confidence signal. Every measurement is a binary behavioural classification of a generated string by a judge. Calibration appears in the paper in three thin ways:

1. **In related work only**, as adjacent literature: verbalized uncertainty (Lin et al.; Tian et al.), the finding that it generalises poorly (Vashurin et al.; Xiong et al.), Kapoor et al. on fine-tuning to improve it, and Kadavath et al. on eliciting a correctness probability that becomes better calibrated with scale. They position their own work explicitly *against* this line: "In contrast to fine-tuning or uncertainty elicitation works, AbstentionBench evaluates **direct, out-of-the-box expressions of uncertainty**". Abstention here is what the model volunteers unprompted, not what can be extracted from it under a calibration-eliciting protocol.
2. **As a substitute analysis**, via the accuracy/abstention-recall correlation (fig. 4, S3). This is a coarse population-level proxy for the calibration question — does being right track knowing when you can be right — and its answer is that the relationship is dataset-dependent and can be negative. This is genuinely informative but it is a correlation between two aggregate rates, not calibration of a confidence signal against outcomes at the item level.
3. **As an implicit contrast with Kadavath et al.** that the authors do not draw but that sits in plain view: Kadavath found elicited correctness probability becomes *more* calibrated with scale; AbstentionBench finds volunteered abstention behaviour is *flat* with scale. These are compatible — a model may hold a well-calibrated internal signal and still not act on it — and the tension between them is arguably the most interesting unexamined thread in the paper.

## Do they separate "internally knows it cannot answer but does not say so" from "does not know"?

**Only partially, behaviourally, and they are appropriately careful not to claim they have settled it.**

The evidence they bring to bear is the reasoning-trace experiment (§4.3, fig. 8a, S15): traces contain elevated expressions of uncertainty while final answers remain definitive. That is a real and relevant dissociation, and it is the paper's one direct attempt at the distinction. It points toward "the representation is somewhere in the computation but does not reach the output".

But it does not establish that, for four reasons, three of which the authors acknowledge:

- **Trace faithfulness.** They cite Chen et al. (2025b) themselves: a chain of thought is a generated artefact, not a readout of internal state. "Wait, I'm not sure" in a trace can be a stylistic token pattern — and for s1.1, which is *explicitly trained to emit* "Wait" and self-critique, this is not a hypothetical worry. The paper names exactly this confound.
- **Precision falls when traces are included.** If the traces were tracking genuine uncertainty, judging on them should improve discrimination. Instead recall rises *and precision falls*, which is the signature of a source that expresses uncertainty more often in general — including on answerable questions — rather than one that expresses it more often *when warranted*. The authors report this; they do not draw the inference from it, but it materially weakens the "the model knows" reading.
- **No internal access is used at all.** There is no probing of hidden states, no logit or entropy analysis, no linear probe for answerability — despite the fact that they cite Slobodkin et al. (2023), whose entire contribution is finding answerability in the hidden states of overconfident LLMs. The tool for making this distinction properly is cited in their own related-work section and not applied.
- **The hallucinated-context failures cut against "it knows".** In the Golden Gate Bridge example, the model does not merely fail to voice a recognised gap; it registers the gap ("I need more context"), then *fabricates a plausible filler* for it and proceeds. That is better described as a repair reflex overriding a detected gap than as a silent internal representation — but distinguishing the two would require exactly the internal analysis they do not perform.

Their own framing in the discussion and broader-impacts sections leans toward the strong reading — "models do not know when not to answer", failure to abstain "may result from a fundamental inability to reason about uncertainty" — while the trace result gestures at the weaker one. **The paper therefore identifies the distinction as live and supplies suggestive behavioural evidence, but leaves it unresolved**, and its two framings are in mild tension with each other.

# Open questions the paper itself raises

Stated or clearly implied by the authors:

- **How do you teach a model to reason about evidence in order to decide when not to respond?** This is their closing statement of the open problem, and they are explicit that they do not know.
- **What post-training targets abstention directly?** They propose two concrete directions: post-training datasets covering different *types* of uncertainty, and explicitly incorporating uncertain scenarios into reasoning fine-tuning (i.e. not only verifiable-answer problems).
- **Increasing underspecified-context representation in SFT data** — offered as a specific, testable remedy for the one scenario post-training makes worse.
- **Is RLVR-style reward misspecification the mechanism?** They hypothesise that optimising a clear-cut verifiable reward biases models toward definitive responses, and that this explains both the RLVR stage effect and the test-time-compute effect. It is labelled a hypothesis and is not tested — no reward-shaping experiment is run.
- **What does o1's reasoning-effort parameter actually do?** Flagged as unanswerable from outside a closed API, with the mixed result reported rather than interpreted.
- **Can the uncertainty in reasoning traces be exploited?** Raised as "potentially promising" and immediately qualified by trace-unfaithfulness concerns.
- **Abstention beyond English**, and abstention scenarios not covered by their six.
- **Benchmark decay.** They note that because AbstentionBench is fully public with no held-out set, scores may inflate over time through reuse and overfitting, and suggest private or gated or dynamically-generated test sets as future work.

# Appreciation

## Mechanism

The mechanistic contributions are the durable part of this paper, and several of them survive independently of any number reported.

- **Abstention is separated from refusal.** Cutting CoCoNot's safety subset and stating that the object of study is uncertainty rather than policy non-compliance is a clarifying move. Much prior work conflates "the model declined" across two mechanisms that have nothing to do with each other — a trained safety reflex and an epistemic judgement — and the paper is right that only the second one tells you anything about whether a system can assess its own footing.
- **The Underspecified Context vs Answer Unknown distinction** is the taxonomy's real contribution: *the information exists but was not given to me* versus *the information does not exist*. These call for different responses (ask versus decline) and, empirically, they behave differently — post-training improves Answer Unknown and degrades Underspecified Context. A taxonomy that predicts a divergence in results is doing work.
- **The paired-fine-tune design.** Comparing s1.1 against Qwen 2.5 32B and DeepSeek R1 Distill against Llama 3.3 70B, rather than comparing reasoning models against unrelated non-reasoning models, is what turns "reasoning models abstain badly" from a correlation into an attribution. This is the single best methodological decision in the paper.
- **The staged post-training ladder corroborating it by a different route.** The RLVR finding and the reasoning finding are separate experiments implicating the same ingredient. Convergent evidence from two designs is worth much more than either alone, and the paper does not make enough of this.
- **Scoring recall while carrying should-not-abstain samples.** Building both polarities into every dataset means over-abstention is always measurable, which is what licenses their claim that precision is near-ceiling — a claim that, if true, sharply constrains what kind of problem abstention is.
- **The hallucinated-context failure mode**, as a qualitative object, is more informative than the aggregate numbers. A model that registers "I need more context", invents a prior conversational turn to supply it, and then answers confidently is exhibiting something much more specific than "poor calibration".
- **The systematic-review provenance and the reasoned exclusion list.** 183 papers → 82 datasets → 17, with each exclusion justified on the substantive question of whether abstention is genuinely desirable, is unusually disciplined benchmark hygiene.

## Magnitude

The magnitudes deserve more caution than the mechanisms.

- **"24% average drop" rests on N = 2 model pairs**, with no variance estimate, from single seeded runs. As a percentage-point figure it is arithmetically what Table 4 gives (−0.20 and −0.28 averaging to −0.24), so it is not inflated — but the phrasing "24%" invites reading as a relative drop, which would actually be ~35%. The direction is consistent (every dataset, both pairs, recall and F1), which is what makes it credible; the *number* is a two-sample mean.
- **Absolute abstention recall figures are judge-dependent.** Every headline number is mediated by an 8B judge at 88% accuracy against a 150-item test set, validated only on outputs from two non-reasoning general-domain models. An 88%-accurate measuring instrument applied to a claim about a ~24-point gap is probably adequate; applied to the many 3-to-5-point comparisons scattered through the results, it is not.
- **"Scale does not help" is the most robust magnitude claim**, because it is a null result over three scales and four metrics, and nulls are less fragile to judge noise than point comparisons.
- **The near-ceiling precision claim is load-bearing and lightly evidenced.** It justifies foregrounding recall, and hence the whole framing that models under-abstain rather than mis-abstain. It is supported by figures rather than a stated statistic.
- **The o1 reasoning-effort table should not be read as a magnitude at all** — differences of a few points, one run, closed API. The authors say as much.
- **The fast-subset validation is a nice touch and quietly informative**: recall is within 5% of the full benchmark for most scenarios, but *not* for Stale (0.74 vs 0.95) — a 21-point gap that hints at how much per-scenario numbers can move with sample composition.

# How it could serve a harness-design effort / limitations / major concerns

## What it offers a harness

Relative to the Subject — a system in a loop deciding whether it has succeeded, is stalling, or should abandon or hand off — this paper is about the single-turn, no-tools, question-answering special case. That is a narrower setting than an agentic loop, and nothing here is measured in a loop. But four things transfer, and one of them is a warning rather than a tool.

- **The strongest transferable claim is a negative one about where to put the judgement.** If a model's volunteered assessment of its own footing is near-chance on underspecified inputs, does not improve with scale, and gets *worse* with the training that makes it better at the task, then a harness cannot site its stop/continue/escalate decision in the model's self-report. The paper's evidence pushes the design toward external checks and trajectory signals — the other two sources named in the Subject — and away from asking the model whether it is stuck.
- **The RLVR result is the most directly actionable finding.** It says that optimising an agent against a verifiable reward — which is exactly what a harness with a test suite or a rule-based verifier does — has a measurable cost in the model's willingness to decline. A harness that trains or selects on "did the check pass" is applying the same pressure that this paper identifies as abstention-degrading. That is a real design tension: the verifier that makes the loop trustworthy also erodes the model's willingness to admit it cannot proceed.
- **The hallucinated-context failure mode is the specific behaviour to instrument against.** "How many bolts in total does it take?" → invent a prior turn about the Golden Gate Bridge → answer 1,000,000 confidently. In a loop, the analogue is an agent that, given a task missing a crucial parameter, fabricates the parameter and proceeds to a confident, well-formed, wrong result. This is worse than a stall, because it produces something that passes shape checks. It suggests a harness should treat *unrequested assumption-filling* as a first-class signal, distinct from error and distinct from no-progress.
- **The taxonomy's ask/decline split maps onto a harness's escalate/abandon split.** Underspecified Context (information exists, was not supplied) is the case where the right move is to hand off to a human or query a source; Answer Unknown (information does not exist) is the case where the right move is to stop. That models handle the second and fail the first is directly relevant: the failure is concentrated in exactly the case where a harness would want a clarification request.
- **The artefact itself is reusable.** MIT/CC-licensed, code released, a fast subset (100 questions per benchmark, 4× faster, under 5 minutes on one V100 with Llama 3.1 8B), a documented judge prompt, and a Hydra-style CLI. If a harness effort wants a regression check on whether a given model or prompt configuration declines appropriately, this is runnable off the shelf.
- **The system-prompt result is practically useful and epistemically limited in a way that matters.** It works — recall up, precision not meaningfully down — so a harness should absolutely carry an abstention-scenario system prompt. But the authors' deflationary reading is the right one to carry forward: it works by enumerating scenarios in advance, so it buys coverage of the failure modes you already thought of, and nothing for the ones you did not. For a harness this is the difference between a checklist and a capability.

## Limitations the authors state

They are candid, and their limitations section is substantive rather than perfunctory: coverage of the abstention space is necessarily incomplete; English only; **contamination** — the CoCoNot *train* split is part of the Tülu post-training data, which directly confounds the OLMo and Tülu results on the CoCoNot subsets, and CoCoNot supplies seven of the 31 subsets; the model set is finite; and the LLM judge is imperfect however carefully tuned. In broader impacts they add that judge noise could produce overconfidence in abstention capabilities and hence inappropriate deployment, and that a fully public benchmark with no gated split will inflate over time.

The contamination admission deserves emphasis because it is more damaging than they let on: the Tülu post-training ladder is one of their two designs for the RLVR claim, and CoCoNot appears in both the Tülu training data and the evaluation set. That specific confound sits inside a specific headline experiment.

## Major concerns of my own

- **No uncertainty quantification anywhere.** Single seed, temperature 0.8, no intervals, no significance tests. The large effects survive this; the many small comparisons do not, and the paper does not distinguish between them for the reader.
- **N = 2 for the headline.** "Reasoning fine-tuning degrades abstention by 24%" generalises from two fine-tuned models, one of which (DeepSeek R1 Distill) is a distillation rather than a direct reasoning fine-tune, so the two pairs are not the same kind of intervention.
- **Ground-truth label leakage into the judge prompt.** The judge is handed `[GROUND TRUTH ABSTENTION LABEL]` for the item it is classifying. Even hedged as "can be noisy", this is a route by which the measuring instrument can anchor on the answer.
- **Judge validated on the wrong population.** The 300 annotated pairs come from Llama 3.1 70B Instruct and GPT-4o only — both non-reasoning, both on general-domain datasets. The judge's behaviour on reasoning-model outputs on math/science data, where the headline claim lives, is unvalidated. Reasoning-model final answers have a distinctive form (`Final Answer:`, boxed expressions) that the judge never saw in validation.
- **Judge is family-related to most of the evaluated models.** Llama 3.1 8B Instruct judging seven Llama-family models, in a Meta paper. GPT-4o performed comparably as a judge; running the headline comparison under both judges would have cost little and settled the question.
- **The constructed reasoning datasets are artefacts.** Regex-stripping the context ahead of the final question produces prompts that are unanswerable but also unnatural — a bare "How many bolts in total does it take?" is not a question a user asks, and the model's inference that a prior turn must have existed is, in context, not unreasonable. Some of the measured failure may be a mismatch between the prompt's implicature (a conversational fragment implies prior context) and the label (should abstain). For GPQA-Abstain the problem is sharper: the four answer options survive the stripping, so the model is shown a well-formed multiple-choice apparatus and asked to abstain from it.
- **FreshQA's answerability is defined against the max cutoff over all models**, so for any model with an earlier cutoff the labels are systematically wrong in a known direction. This is a per-model measurement bias in one of only two Stale datasets.
- **Table 3 bookkeeping.** The scenario key omits Subjective and reuses "S", and the dataset count does not reconcile between §3.1 (16 general, but 15 listed) and C.2.1 (17 + 3 + UMWP = 21) against the headline 20.
- **The framing outruns the evidence in one place.** "Models do not know when not to answer" and "a fundamental inability to reason about uncertainty" are claims about internal states; every measurement in the paper is a behavioural classification of output text, and their own trace experiment suggests the internal and external stories may come apart. The weaker claim — models do not *say* when not to answer — is fully supported and would have cost them nothing.
- **Nothing is multi-turn, tool-using, or agentic.** For the Subject specifically, this is the largest gap: the paper measures a single-shot decision to decline, not a running judgement maintained across a trajectory. Whether these failures compound, self-correct, or are caught by external checks over multiple turns is entirely outside its scope.

# Five citations worth chasing next

1. **Slobodkin, Goldman, Caciularu, Dagan, Ravfogel (2023), "The Curious Case of Hallucinatory (Un)answerability: Finding Truths in the Hidden States of Over-Confident Large Language Models", EMNLP 2023.** The most important one for the unresolved question in this review. It looks for answerability in hidden states — exactly the internal-access method AbstentionBench cites but does not use — and so speaks directly to whether "knows but does not say" is separable from "does not know".
2. **Kadavath et al. (2022), "Language Models (Mostly) Know What They Know" (arXiv:2207.05221).** The counterweight. Elicited correctness probabilities that become *more* calibrated with scale, against AbstentionBench's finding that volunteered abstention is *flat* with scale. Whether these are reconcilable is the substantive open question the paper walks past.
3. **Brahman et al. (2024), "The Art of Saying No: Contextual Noncompliance in Language Models", NeurIPS 2024.** The direct ancestor: AbstentionBench's abstention judge prompt, its system prompt, and seven of its 31 subsets all derive from CoCoNot. Needed both to understand the instrument and to assess the contamination confound the authors flag.
4. **Wen, Yao, Feng, Xu, Tsvetkov, Howe, Wang (2025), "Know Your Limits: A Survey of Abstention in Large Language Models" (arXiv:2407.18418).** The authors' own pointer for the methods landscape. A survey is the efficient way to see what abstention *interventions* exist, which AbstentionBench deliberately does not evaluate — it measures out-of-the-box behaviour only.
5. **Chen et al. (2025b), on the unfaithfulness of reasoning traces** — cited by the authors precisely to caution against reading uncertainty in a chain of thought as evidence of represented uncertainty. This is the load-bearing caveat on finding #7, and the citation needed to judge how much weight the trace result can carry.

*Runner-up:* Lambert et al. (2025) on Tülu 3, for the composition of the post-training data — the paper's explanation for the underspecified-context degradation is a claim about what is and is not in that dataset, and it is asserted rather than verified.
