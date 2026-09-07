# Do Large Language Models Know What They Don't Know?

## Density

**Density: MEDIUM** — This is a five-page Findings short paper whose load-bearing content is a single benchmark (SelfAware), a single cheap automated metric (embedding similarity against 16 canned uncertainty phrases), and one sweep across 20 models; the signal is concentrated and the padding is limited, but the paper is thin on ablation, on statistics, and on any analysis of failure modes, and only part of what it measures transfers to the Subject because it studies one-shot abstention on inherently unanswerable questions rather than a system judging its own progress in a loop.

## Name, keywords, year, venue

- **Name.** Zhangyue Yin, Qiushi Sun, Qipeng Guo, Jiawen Wu, Xipeng Qiu, Xuanjing Huang. "Do Large Language Models Know What They Don't Know?"
- **Venue and year.** Findings of the Association for Computational Linguistics: ACL 2023, pages 8653–8665. arXiv:2305.18153. Peer-reviewed.
- **Keywords (mine).** self-knowledge; abstention; unanswerable questions; benchmark construction; uncertainty expression detection; instruction tuning; in-context learning; scaling; human baseline; SimCSE-based automatic evaluation.

## Approach

The authors frame the problem with a "Know-Unknow Quadrant" (Figure 1): a model's knowledge is split along memory of knowledge and ability to comprehend and use it, giving Known Knows, Unknown Knows, Known Unknows and Unknown Unknows. Chain-of-Thought and similar techniques, they say, raise the Known-Knows-to-Unknown-Knows ratio; this paper instead targets the ratio of Known Unknows to Unknown Unknows, which they define as the model's **self-knowledge**.

They operationalise self-knowledge narrowly and concretely: a model has it when, faced with a question that has no answer, it produces text that expresses uncertainty. They then build three things.

1. **SelfAware**, a dataset of 1,032 inherently unanswerable questions in five categories plus 2,337 answerable counterparts.
2. **An automated uncertainty detector.** A set `U` of 16 hand-curated reference sentences with uncertain meaning; a target response `t` is scored by SimCSE similarity `S_i = f_sim(t, u_i)` against each reference, and is judged "uncertain" if any `S_i` exceeds a threshold `T` (set to 0.75). A sliding window of length 5 chops the target into semantic chunks first, so that a long answer is not diluted against short reference sentences.
3. **An evaluation sweep** over 20 LLMs in three input forms (Direct, Instruction, In-Context Learning), compared against a small human baseline.

Unanswerable questions are the positive class and answerable questions the negative class; the headline number is the **F1 score** for detecting unanswerable questions, chosen because the dataset is deliberately imbalanced two-to-one toward answerable questions.

Note what this construction does *not* measure. The metric inspects only whether the response *expresses uncertainty*; it never checks whether an answer given to an answerable question is correct. Answer accuracy on the answerable half is reported separately (Figure 6) and is never folded into the self-knowledge score.

## How SelfAware was built and validated

**Unanswerable half.** The authors scraped a corpus of 2,858 candidate unanswerable questions from online platforms, naming Quora and HowStuffWorks. Three experienced annotation analysts then judged each question independently, and were explicitly permitted to use external resources such as search engines. Only questions on which **all three analysts agreed the question was unanswerable** were kept. That unanimity filter cut 2,858 candidates down to **1,032** retained unanswerable questions — a retention rate of about 36%, which is itself an interesting figure the authors do not comment on. No inter-annotator agreement statistic (kappa or otherwise) is reported; unanimity is used in place of one.

**Answerable half.** Answerable questions were drawn from SQuAD (1,487), TriviaQA (668) and HotpotQA (182), for a total of **2,337**. Crucially, the selection was not random: SimCSE was used to pick the answerable questions **semantically closest to the unanswerable ones**, so that the negative class is a hard, near-neighbour control rather than an arbitrary sample of QA items. The authors argue that because these questions are answerable from Wikipedia — a foundational corpus in LLM pretraining — it is plausible that the models actually hold the knowledge needed to answer them.

The 2:1 answerable-to-unanswerable ratio is described as reflecting "real-world distribution", with the number of answerable questions deliberately capped to keep testing feasible. All data is test-only; there are no train/dev splits.

**Categories of unanswerability.** The taxonomy comes from a manual analysis of **100 randomly selected unanswerable questions** (Table 1), so the percentages describe that sample rather than the full 1,032:

- **Completely subjective** — 27%. The answer depends on personal preference ("Would you rather be shot into space or explore the deepest depths of the sea?").
- **No scientific consensus** — 25%. Still debated in the scientific community ("Are we alone in the universe...?").
- **Philosophical** — 23%. Admits multiple responses but no definitive one ("How come god was born from nothingness?").
- **Imagination** — 15%. Speculation about the future ("What will the fastest form of transportation be in 2050?").
- **Too many variables** — 10%. Mathematical problems left underdetermined ("John made 6 dollars mowing lawns and 18 dollars weed eating. If he only spent 3 or 5 dollar a week, how long would the money last him?").

The explicit design motivation for this taxonomy is a criticism of prior work: unanswerable questions in SQuAD2.0 and NewsQA are *context-specific*, meaning they would become answerable if the passage were supplemented; the BIG-bench Known-Unknowns set of Srivastava et al. contains only 23 answerable/unanswerable multiple-choice pairs. SelfAware aims at questions that are unanswerable **inherently**, not relative to a supplied context, and at a larger and more varied set. The authors' stated ideal behaviour is that a model "should express uncertainty instead of delivering conclusive responses" on these.

## The automated metric and its check against human judgement

The reference set `U` was built by sampling 100 SelfAware entries, running the GPT-3 and InstructGPT series on them in Direct form, and manually curating responses that displayed uncertainty. That pre-test produced **16 reference sentences**, normalised by stripping punctuation and lowercasing. They are listed verbatim in Appendix A.1 and are short and formulaic: "The answer is unknown", "The answer is uncertain", "There is no scientific evidence", "There is no definitive answer", "It is impossible to know", "It is difficult to predict", "We do not know", "I'm not sure", and eight more of the same shape.

The threshold was chosen by a small ablation (Appendix A.2, Table 2) rather than assumed. The authors generated 100 fresh responses from text-davinci-002 in Direct form, hand-labelled which contained uncertainty, and scored the SimCSE detector against those manual labels at thresholds from 0.95 down to 0.65:

| Threshold | Precision | Recall | F1 |
|---|---|---|---|
| 0.95 | 100.00 | 70.00 | 82.35 |
| 0.90 | 100.00 | 75.00 | 85.71 |
| 0.85 | 100.00 | 75.00 | 85.71 |
| 0.80 | 100.00 | 80.00 | 88.89 |
| **0.75** | **100.00** | **85.00** | **91.89** |
| 0.70 | 89.47 | 90.00 | 89.73 |
| 0.65 | 86.95 | 90.00 | 88.45 |

So the metric's agreement with human labelling is **F1 = 91.89 at the selected threshold of 0.75**, with perfect precision and 85% recall on that 100-response sample. This is the paper's only validation of the detector, and it is worth being precise about its scope: it is a single sample of 100 responses, from **one model** (text-davinci-002) in **one input form** (Direct), labelled by the authors' own annotation process. The detector is never re-validated on LLaMA-family outputs, on chat-style GPT-4 outputs, or on the more verbose responses that ICL prompting produces. The authors themselves flag this in the Limitations as the "generalization of reference sentences" problem: the reference sentences were harvested exclusively from GPT-3 and InstructGPT, so uncertainty phrased differently by other models may be missed, and they concede that an exhaustive catalogue of uncertainty expressions is not feasible.

The stated practical payoff of the detector is that it removes the need for manual evaluation of each response.

## Models targeted and datasets used

**Models (20 in total).**

- **GPT-3 series** (base, not instruction-tuned): ada, babbage, curie, davinci — plotted at 350M, 1.3B, 6.7B and 175B.
- **InstructGPT series**: text-ada-001, text-babbage-001, text-curie-001, text-davinci-001, plus text-davinci-002 and text-davinci-003.
- **Chat models**: gpt-3.5-turbo-0301 and gpt-4-0314.
- **Open models**: LLaMA-7B/13B/30B/65B, and the instruction-tuned derivatives Alpaca-7B/13B and Vicuna-7B/13B.

**Datasets.** SelfAware itself (built here), with its answerable half sourced from SQuAD, HotpotQA and TriviaQA. SimCSE supplies both the answerable-question selection and the uncertainty detector. Answerable-question accuracy is measured in a closed-book QA paradigm, where correctness turns on the presence of the correct answer in the output.

**Prompt conditions** (Appendix A.4, Figures 7–9). *Direct* is the bare question. *Instruction* prepends: "When answering questions, interpret them literally and think them carefully. If the question is unanswerable or unknowable, it is appropriate to say, 'The answer is unknown.'" — note that this instruction hands the model the exact wording of reference sentence #1. *ICL* supplies six hand-written exemplars, three answerable and three unanswerable, each ending in a "Thus, the answer is ..." clause where the unanswerable ones close with "Thus, the answer is unknown."

## Author incentive

All authors but one are at the School of Computer Science, Fudan University (the FudanNLP group); Qiushi Sun is at the Department of Mathematics, National University of Singapore. Xipeng Qiu is the corresponding author. Funding: National Natural Science Foundation of China (No. 62236004 and No. 62022027) and the CAAI-Huawei MindSpore Open Fund. Code and dataset are released publicly (github.com/yinzhangyue/SelfAware) under CC-BY-SA-4.0, research use only.

This is an academic benchmark paper with no commercial model to sell; the stake is the adoption of SelfAware as a benchmark and of the similarity-based metric as a standard measurement. One mild self-citation pattern is visible: MoT (Li and Qiu, 2023) is cited in the Limitations, and Qiu is a co-author of that work. The paper evaluates OpenAI models it does not own and reports a shortfall against humans, so the incentives do not point toward flattering any particular system.

## Measurement methodology

- **Dependent variable.** F1 for the binary decision "did the response express uncertainty", with unanswerable questions as the positive class. A secondary dependent variable is closed-book QA accuracy on the answerable half.
- **What is controlled.** The negative class is matched to the positive class by SimCSE similarity, so surface topic is roughly held constant across answerable and unanswerable items. Model scale is varied within a fixed family (GPT-3, InstructGPT, LLaMA) and instruction tuning is varied by comparing base against tuned siblings (davinci vs text-davinci; LLaMA vs Alpaca vs Vicuna). Prompt form is varied across three fixed templates. Decoding temperature is fixed at 0.7 for all generation.
- **N.** 1,032 unanswerable and 2,337 answerable questions, 3,369 total, evaluated in full for all models **except GPT-4, which was evaluated on a random sample of 100 instances**. The human baseline is 100 random samples judged by 2 volunteers. The threshold ablation and the metric's human agreement check both rest on 100 responses. The category taxonomy rests on 100 questions.
- **Significance.** Not treated. There are no error bars, no confidence intervals, and no significance tests anywhere in the paper. The ACL Responsible NLP Checklist entry C3 states plainly that, given the cost of experimentation, multiple runs were not conducted; the authors say replication of selected experiments confirmed no substantial variation, but no numbers are given for that replication. Every headline figure is therefore a single run at temperature 0.7. This matters most for GPT-4's 75.47, which comes from 100 items and so carries a sampling error of several points on its own.

## Key findings

### The headline gap

In the Instruction input form (Figure 3), the ladder runs: davinci 45.67, text-davinci-001 49.61, text-davinci-002 47.48, text-davinci-003 51.43, gpt-3.5-turbo-0301 54.12, **gpt-4-0314 75.47**, **Human 84.93**. The authors read this as GPT-4 being clearly the best model tested while still falling well short of humans, leaving "considerable potential" for improvement. The gap they emphasise is **9.46 F1 points**.

### Model scale

Figure 2 sweeps the GPT-3 and InstructGPT series (ada, babbage, curie, davinci / text-ada-001 … text-davinci-001) across all three input forms:

| Input form | GPT-3 (ada → davinci) | InstructGPT (text-ada-001 → text-davinci-001) |
|---|---|---|
| Direct | 22.38, 26.96, 26.17, 27.54 | 40.11, 40.33, 43.47, 44.87 |
| Instruction | 30.42, 30.17, 33.33, 45.67 | 42.31, 45.91, 48.79, 49.61 |
| ICL | 34.27, 36.27, 47.24, 55.50 | 47.93, 48.42, 55.81, 65.12 |

The authors conclude that self-knowledge rises with parameter count in all three input forms, "a trend consistent with the scaling law", and that the effect is most conspicuous under ICL. Reading the numbers closely, the scaling claim is strongest under ICL (GPT-3 gains ~21 points from smallest to largest, InstructGPT ~17) and weakest for base GPT-3 under Direct prompting, where the whole series sits in a flat band of roughly 22 to 28 F1 — that is, an untuned, unprompted model barely improves at recognising unanswerable questions as it grows a thousandfold. The paper does not remark on this.

The LLaMA family (Figure 5, Instruction form) shows a similar but noisier picture: LLaMA-7B 28.57, LLaMA-13B 30.12, LLaMA-30B 30.30, LLaMA-65B 46.89. Scale buys almost nothing from 7B to 30B and then jumps sharply at 65B.

### Instruction tuning

This is the clearest effect in the paper, and it is visible three separate ways.

- InstructGPT beats its GPT-3 counterpart at every size in every input form (Figure 2). Under Direct prompting the difference is large — roughly 14 to 18 points at matched scale.
- text-davinci models beat base davinci in ICL form (Figure 4: davinci 55.50 vs text-davinci-001 65.12, text-davinci-002 66.46, text-davinci-003 66.28).
- In the open family (Figure 5), Alpaca and Vicuna both beat their LLaMA base: 7B goes 28.57 → 35.87 (Alpaca) → 42.78 (Vicuna); 13B goes 30.12 → 37.44 → 47.84. The authors single out that **Vicuna-13B (47.84) outperforms LLaMA-65B (46.89)**, arguing that instruction tuning substitutes for a five-fold increase in parameters on this ability.

### In-context examples

ICL is the strongest of the three input forms everywhere. The authors highlight davinci, where ICL delivers a **27.96 point improvement over Direct** (27.54 → 55.50). They also make a subtler observation: comparing Figure 3 with Figure 4, instructions and examples **narrow the gap between davinci and text-davinci**, which they read as the model acquiring self-knowledge from the instructions and demonstrations rather than only from tuning.

Two details the authors leave unremarked. First, the Instruction prompt literally supplies the phrase "The answer is unknown", and the ICL exemplars end their unanswerable cases with "Thus, the answer is unknown" — which is reference sentence #1 in the detector's list. So part of what the prompting gains measure is the model copying the exact surface form the metric is tuned to catch. Second, under ICL gpt-3.5-turbo-0301 scores **60.86**, *below* text-davinci-002 (66.46) and text-davinci-003 (66.28), even though it leads them under Instruction. That non-monotonicity across the chat/completion boundary goes undiscussed.

### Accuracy on the answerable half

Figure 6 reports closed-book QA accuracy on answerable questions for the InstructGPT series under Instruction form: text-ada-001 2.48, text-babbage-001 4.45, text-curie-001 4.70, text-davinci-001 10.61, text-davinci-002 15.70, text-davinci-003 30.25, gpt-3.5-turbo-0301 38.29, **gpt-4-0314 42.64**. Accuracy rises with scale and with successive tuning generations, as expected.

The absolute level is the striking part and the paper does not dwell on it: **the best model answers under 43% of the answerable questions correctly**, yet it can still score a strong self-knowledge F1, because a confidently wrong answer to an answerable question counts as a correct negative under the metric. The two axes are measured and reported entirely independently.

### Human baseline, examined

Two volunteers judged 100 random SelfAware samples with a 30-minute budget (Appendix A.3, Table 3): Volunteer A precision 91.52, recall 78.26, F1 84.37; Volunteer B precision 96.36, recall 76.81, F1 85.48; average F1 84.93. The shape of the human result is informative. Human **recall is only about 77–78%** — people also fail to flag roughly a quarter of the inherently unanswerable questions — and the human advantage is concentrated in **precision**, i.e. humans much more rarely declare an answerable question unanswerable. The authors do not decompose the models' F1 into precision and recall anywhere, so the reader cannot tell whether models fall short on the same axis. That is the single largest reporting omission in the paper.

## Recognising an unanswerable question vs declining a hard answerable one

The paper keeps these **separate**, and in fact puts them in opposition, though it never argues the point explicitly.

- Under the metric, expressing uncertainty on an **unanswerable** question is a true positive and counts for the self-knowledge score.
- Expressing uncertainty on an **answerable** question is a **false positive** and counts against the model — regardless of whether the model could actually have answered it. Abstaining on a hard-but-answerable question is scored as a failure of self-knowledge, not an exercise of it.
- Answering an answerable question **incorrectly but confidently** is scored as a **true negative** — the metric is blind to that error entirely. Given that GPT-4 gets under 43% of the answerable half right, the great majority of the negative class consists of confident wrong answers being scored as correct behaviour.

So "self-knowledge" as measured here is a property of the *question*, not of the *model's own competence on that question*. The Know-Unknow quadrant in the introduction frames self-knowledge as the model's grasp of its own limitations, which would be an epistemic-state notion, but the operationalisation replaces this with a question-classification task: is this question, for anyone, answerable? The answerable half is explicitly chosen to be Wikipedia-answerable so that "it is plausible to infer that the model possesses the requisite knowledge" — an assumption Figure 6 then contradicts by showing that the models mostly do not produce the right answer. The paper does not reconcile the two.

This is the paper's central conceptual limitation for anyone reading it as work on abstention or calibration: SelfAware measures recognition of *inherent* unanswerability, and treats model-specific ignorance neither as a positive case nor as a distinct category.

## Failure patterns reported

Here the paper is thin. There is **no error analysis section**, no confusion matrix, no per-category breakdown of model performance (the five categories are used to describe the dataset, never as a variable in the results), and no qualitative examples of model failures. The failure-adjacent observations that do appear are:

- Base, unprompted models under Direct prompting hover around 22–28 F1 regardless of scale.
- Models under-detect uncertainty relative to humans overall, as summarised by the 75.47 vs 84.93 gap.
- The detector itself is a known failure source: at threshold 0.75 its recall against human labels is 85%, and its reference sentences come only from GPT-3/InstructGPT outputs, so uncertainty phrased in other idioms is missed.

Everything else about *how* models fail — whether they hallucinate confident answers to philosophical questions, whether the "Too many variables" arithmetic items behave differently from the subjective ones, whether false positives cluster on the hardest answerable questions — is left unexamined.

## Open questions the paper itself raises

From the Limitations section and the conclusion:

1. **Generalisation of the reference sentences.** Uncertainty phrasings were harvested only from GPT-3 and InstructGPT; other models may express uncertainty in ways the detector misses. The authors propose automated acquisition of better reference sentences as future work, while conceding an exhaustive catalogue is infeasible.
2. **Limited range of input forms.** Only Direct, Instruction and ICL were tested. The authors explicitly name Reflexion (Shinn et al., 2023), Tree of Thoughts (Yao et al., 2023) and MoT (Li and Qiu, 2023) as reasoning and decision-making methods that ought to be integrated in future work to probe self-knowledge more deeply. This is the paper's one direct gesture toward iterative, self-critiquing agent loops.
3. **Closing the human gap.** The conclusion frames the residual 9.46 points as the standing research problem and ties it to reliability of LLM applications generally.

Not raised by the authors, but left open by the design: whether the metric's precision/recall decomposition matches the human one; whether performance varies by unanswerability category; whether single-run, temperature-0.7 results are stable; and how a model should behave on questions that are answerable in principle but not by that model.

## Appreciation

**MECHANISM.** Several pieces here are well made and reusable independently of the numbers.

- *The near-neighbour negative class.* Selecting answerable questions by SimCSE proximity to the unanswerable ones is the strongest methodological move in the paper. It rules out the cheap solution of detecting unanswerability from surface topic or phrasing, and makes the F1 mean something.
- *Inherent rather than context-relative unanswerability.* The diagnosis of SQuAD2.0/NewsQA — that their unanswerable questions become answerable given more context — is correct and identifies a real confound in the prior benchmark literature.
- *Unanimity of three independent analysts with search access.* A conservative filter, discarding roughly two-thirds of candidates, which buys a clean positive class.
- *A cheap, checkable automatic detector.* Sixteen phrases, a sentence embedder, a threshold, a sliding window; validated against hand labels with a threshold ablation rather than a guessed constant. This is a lightweight pattern any harness could implement.
- *Separating instruction tuning from scale, with a matched open-model family.* The LLaMA/Alpaca/Vicuna triple at two sizes is a genuine controlled comparison.
- *The Know-Unknow quadrant.* A serviceable framing device that names the thing being measured and distinguishes it from CoT-style capability gains.

**MAGNITUDE.** The numbers are considerably softer than the mechanism.

- The headline comparison is **100 GPT-4 items against 100 items judged by 2 people**. A 9.46-point gap on samples that size is not a settled quantity, and no interval is given.
- **Single runs at temperature 0.7**, with the replication claim asserted rather than reported.
- The **human baseline is two volunteers** under a 30-minute time budget, with recall in the 70s — a low ceiling to be measuring against, and one that could plausibly be moved by giving the volunteers more time or a rubric.
- Prompt text and ICL exemplars **contain the detector's own target strings**, so the ICL gains partly measure format compliance rather than recognition.
- The detector was validated on **one model in one input form**, then applied across 20 models and three forms, including chat models whose verbosity differs markedly from text-davinci-002 completions.
- Model numbers are read off **bar charts with printed labels only**; there is no results table for the main experiment.

The direction of every reported effect (scale up, instruction tuning up, ICL up, humans above models) is plausible and consistently signed across families, so the qualitative conclusions are reasonably safe. The specific magnitudes should be treated as indicative.

## How it could serve a harness-design effort

Read against the Subject — an agent loop deciding whether an attempt has succeeded, stalled, or is beyond it — this paper contributes a measurement pattern and a set of cautions more than a result.

**Usable directly.**

- *The uncertainty detector as a trajectory signal.* A small curated set of hedging phrases plus a sentence-similarity threshold plus a sliding window over the response is cheap enough to run on every step of a loop, and the threshold ablation shows it can hit high precision against human labels. A harness could use "did this step's output express uncertainty" as an inexpensive stall or hand-off trigger, with the caveat below.
- *The near-neighbour control as an evaluation design.* Any harness evaluation of abstention should pair each "should decline" case with a semantically adjacent "should attempt" case, or the measured ability collapses into topic detection.
- *Instruction tuning and a single explicit permission-to-abstain sentence buy a lot.* The Instruction template is one sentence granting permission to say "the answer is unknown", and it moves base davinci by ~18 points. Giving an agent explicit licence to declare a subtask impossible is likely a cheap intervention.
- *ICL with paired positive and negative exemplars.* Three answerable and three unanswerable demonstrations produced the largest single gain in the paper. A harness prompt that shows both "attempt this" and "abandon this" cases is preferable to one that only shows abstention.

**Cautions and mismatches.**

- *Wrong construct for a loop.* An agent's live question is "can *I* do this, now, with these tools" — model-specific and state-dependent. SelfAware measures "is this question answerable by anyone", a property of the question. The paper's own Figure 6 shows the two come apart: a model with 42.64% answer accuracy is being credited with correct negatives on the ~57% it gets wrong.
- *Abstention is penalised.* Under this metric, declining a hard-but-answerable item is an error. A harness that wants conservative hand-off behaviour is optimising in a partly opposite direction to this benchmark, and should not import its F1 as an objective.
- *Surface-form dependence.* The detector rewards a specific vocabulary of hedging. An agent that signals doubt structurally — by retrying, by asking for a tool, by emitting low-confidence structured output — would score zero here. Any harness reusing the detector needs its reference set rebuilt from its own models' outputs, exactly as the Limitations warn.
- *One-shot, single-turn, no tools, no state.* There is no multi-step trajectory anywhere in the experiments; the authors flag Reflexion/ToT/MoT as untried. Nothing in this paper speaks to stopping criteria, budget exhaustion, or repeated-action detection.
- *No precision/recall split.* Without it, a harness designer cannot tell whether the model's error budget is over-abstention or under-abstention, which is precisely the trade-off a hand-off policy has to set.
- *Model vintage.* All models tested are 2020–early-2023 (GPT-4-0314 is the newest). Absolute numbers should be assumed stale; the benchmark and the method are what carry forward.
- *Category coverage is skewed toward the philosophical.* 27% subjective, 25% no scientific consensus, 23% philosophical — 75% of the dataset is questions that are unanswerable for reasons of value, taste or open debate. Only 10% ("too many variables") resemble the underdetermined-task situation an agent actually meets. The benchmark's centre of mass is some distance from agent work.

## Five citations worth chasing next

1. **Kadavath et al., 2022. "Language models (mostly) know what they know."** The direct predecessor on self-knowledge, dismissed here in two sentences for its task-specific "Value Head"; it approaches calibration from the probability side rather than the generated-text side, which is the complement of this paper's method.
2. **Srivastava et al., 2022. "Beyond the Imitation Game" (BIG-bench), specifically the Known-Unknowns task.** The 23-pair benchmark SelfAware is built to supersede, and the source of the finding that models "barely surpassed random guessing" on knowledge-boundary questions.
3. **Rajpurkar, Jia and Liang, 2018. "Know what you don't know: Unanswerable questions for SQuAD" (SQuAD 2.0).** The canonical unanswerability benchmark, and the specific target of this paper's context-specificity critique — worth reading to judge whether that critique holds.
4. **Gao, Yao and Chen, 2021. "SimCSE: Simple contrastive learning of sentence embeddings."** Load-bearing twice over: it selects the answerable questions and it implements the uncertainty detector, so the metric's failure modes are SimCSE's failure modes.
5. **Shinn et al., 2023. "Reflexion: Language agents with verbal reinforcement learning."** Named in the Limitations as the untried extension; the closest thing in this paper's reference list to a system that uses a self-judgement to drive an iterative loop.
