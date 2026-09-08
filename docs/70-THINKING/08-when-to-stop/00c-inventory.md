# Inventory and selection - Knowing When to Stop

## 1. Inventory

_Step 1 output - cite line, full abstract verbatim, flag (RELATED / ADJACENT / NOT RELATED) + one line of reason, per paper. Gathered 2026-09-07. Peer-reviewed 2023+ preferred; a few directly-central preprints are listed and marked, per the topic-07 precedent._

### 1. Large Language Models Cannot Self-Correct Reasoning Yet

Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, Denny Zhou. *Large Language Models Cannot Self-Correct Reasoning Yet.* 2023. ICLR 2024. arXiv:2310.01798 (2310.01798v2). https://arxiv.org/abs/2310.01798

**Abstract (verbatim).** Large Language Models (LLMs) have emerged as a groundbreaking technology with their unparalleled text generation capabilities across various applications. Nevertheless, concerns persist regarding the accuracy and appropriateness of their generated content. A contemporary methodology, self-correction, has been proposed as a remedy to these issues. Building upon this premise, this paper critically examines the role and efficacy of self-correction within LLMs, shedding light on its true potential and limitations. Central to our investigation is the notion of intrinsic self-correction, whereby an LLM attempts to correct its initial responses based solely on its inherent capabilities, without the crutch of external feedback. In the context of reasoning, our research indicates that LLMs struggle to self-correct their responses without external feedback, and at times, their performance even degrades after self-correction. Drawing from these insights, we offer suggestions for future research and practical applications in this field.

**Flag.** RELATED - Anchor. The foundational negative result on intrinsic self-correction: without external feedback an LLM cannot reliably judge or fix its own reasoning, and may degrade. Directly the self-report signal in the Subject.

### 2. When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs

Ryo Kamoi, Yusen Zhang, Nan Zhang, Jiawei Han, Rui Zhang. *When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs.* 2024. TACL 2024 (vol. 12, pp. 1417-1440). arXiv:2406.01297 (2406.01297v3). https://arxiv.org/abs/2406.01297

**Abstract (verbatim).** Self-correction is an approach to improving responses from large language models (LLMs) by refining the responses using LLMs during inference. Prior work has proposed various self-correction frameworks using different sources of feedback, including self-evaluation and external feedback. However, there is still no consensus on the question of when LLMs can correct their own mistakes, as recent studies also report negative results. In this work, we critically survey broad papers and discuss the conditions required for successful self-correction. We first find that prior studies often do not define their research questions in detail and involve impractical frameworks or unfair evaluations that over-evaluate self-correction. To tackle these issues, we categorize research questions in self-correction research and provide a checklist for designing appropriate experiments. Our critical survey based on the newly categorized research questions shows that (1) no prior work demonstrates successful self-correction with feedback from prompted LLMs, except for studies in tasks that are exceptionally suited for self-correction, (2) self-correction works well in tasks that can use reliable external feedback, and (3) large-scale fine-tuning enables self-correction.

**Flag.** RELATED - Anchor-grade critical survey of self-correction. Defines three distinct research questions, shows many prior positive results rest on oracle feedback or unfair evaluation. Sets the frame for the whole self-evaluation span.

**Review status.** reviewed -> sheet 01-self-correction-survey.md (round 1). Cross-paper discussion: pending.

### 3. Language Models (Mostly) Know What They Know

Saurav Kadavath, Tom Conerly, Amanda Askell, Tom Henighan, Dawn Drain, Ethan Perez, Nicholas Schiefer, Zac Hatfield-Dodds et al.. *Language Models (Mostly) Know What They Know.* 2022. arXiv 2022 (Anthropic; no peer-reviewed venue) - anchor. arXiv:2207.05221 (2207.05221v4). https://arxiv.org/abs/2207.05221

**Abstract (verbatim).** We study whether language models can evaluate the validity of their own claims and predict which questions they will be able to answer correctly. We first show that larger models are well-calibrated on diverse multiple choice and true/false questions when they are provided in the right format. Thus we can approach self-evaluation on open-ended sampling tasks by asking models to first propose answers, and then to evaluate the probability "P(True)" that their answers are correct. We find encouraging performance, calibration, and scaling for P(True) on a diverse array of tasks. Performance at self-evaluation further improves when we allow models to consider many of their own samples before predicting the validity of one specific possibility. Next, we investigate whether models can be trained to predict "P(IK)", the probability that "I know" the answer to a question, without reference to any particular proposed answer. Models perform well at predicting P(IK) and partially generalize across tasks, though they struggle with calibration of P(IK) on new tasks. The predicted P(IK) probabilities also increase appropriately in the presence of relevant source materials in the context, and in the presence of hints towards the solution of mathematical word problems. We hope these observations lay the groundwork for training more honest models, and for investigating how honesty generalizes to cases where models are trained on objectives other than the imitation of human writing.

**Flag.** RELATED - Anchor. P(IK) self-knowledge and calibration: larger models are reasonably calibrated on multiple-choice / true-false and can be trained to predict whether they know an answer.

### 4. Teaching Models to Express Their Uncertainty in Words

Stephanie Lin, Jacob Hilton, Owain Evans. *Teaching Models to Express Their Uncertainty in Words.* 2022. TMLR 2022 - anchor. arXiv:2205.14334 (2205.14334v2). https://arxiv.org/abs/2205.14334

**Abstract (verbatim).** We show that a GPT-3 model can learn to express uncertainty about its own answers in natural language -- without use of model logits. When given a question, the model generates both an answer and a level of confidence (e.g. "90% confidence" or "high confidence"). These levels map to probabilities that are well calibrated. The model also remains moderately calibrated under distribution shift, and is sensitive to uncertainty in its own answers, rather than imitating human examples. To our knowledge, this is the first time a model has been shown to express calibrated uncertainty about its own answers in natural language. For testing calibration, we introduce the CalibratedMath suite of tasks. We compare the calibration of uncertainty expressed in words ("verbalized probability") to uncertainty extracted from model logits. Both kinds of uncertainty are capable of generalizing calibration under distribution shift. We also provide evidence that GPT-3's ability to generalize calibration depends on pre-trained latent representations that correlate with epistemic uncertainty over its answers.

**Flag.** RELATED - Anchor. First demonstration that a model can be trained to verbalise calibrated uncertainty in words (CalibratedMath), rather than reading it from logits.

### 5. Do Large Language Models Know What They Don't Know?

Zhangyue Yin, Qiushi Sun, Qipeng Guo, Jiawen Wu, Xipeng Qiu, Xuanjing Huang. *Do Large Language Models Know What They Don't Know?.* 2023. Findings of ACL 2023. arXiv:2305.18153 (2305.18153v2). https://arxiv.org/abs/2305.18153

**Abstract (verbatim).** Large language models (LLMs) have a wealth of knowledge that allows them to excel in various Natural Language Processing (NLP) tasks. Current research focuses on enhancing their performance within their existing knowledge. Despite their vast knowledge, LLMs are still limited by the amount of information they can accommodate and comprehend. Therefore, the ability to understand their own limitations on the unknows, referred to as self-knowledge, is of paramount importance. This study aims to evaluate LLMs' self-knowledge by assessing their ability to identify unanswerable or unknowable questions. We introduce an automated methodology to detect uncertainty in the responses of these models, providing a novel measure of their self-knowledge. We further introduce a unique dataset, SelfAware, consisting of unanswerable questions from five diverse categories and their answerable counterparts. Our extensive analysis, involving 20 LLMs including GPT-3, InstructGPT, and LLaMA, discovering an intrinsic capacity for self-knowledge within these models. Moreover, we demonstrate that in-context learning and instruction tuning can further enhance this self-knowledge. Despite this promising insight, our findings also highlight a considerable gap between the capabilities of these models and human proficiency in recognizing the limits of their knowledge.

**Flag.** RELATED - Self-knowledge of the boundary of one's own knowledge - the 'is this beyond me' judgement - with the SelfAware benchmark of unanswerable questions.

**Review status.** reviewed -> sheet 08-selfaware.md (round 2). Cross-paper discussion: pending.

### 6. The Internal State of an LLM Knows When It's Lying

Amos Azaria, Tom Mitchell. *The Internal State of an LLM Knows When It's Lying.* 2023. Findings of EMNLP 2023 (per ACL Anthology; not in arXiv metadata). arXiv:2304.13734 (2304.13734v2). https://arxiv.org/abs/2304.13734

**Abstract (verbatim).** While Large Language Models (LLMs) have shown exceptional performance in various tasks, one of their most prominent drawbacks is generating inaccurate or false information with a confident tone. In this paper, we provide evidence that the LLM's internal state can be used to reveal the truthfulness of statements. This includes both statements provided to the LLM, and statements that the LLM itself generates. Our approach is to train a classifier that outputs the probability that a statement is truthful, based on the hidden layer activations of the LLM as it reads or generates the statement. Experiments demonstrate that given a set of test sentences, of which half are true and half false, our trained classifier achieves an average of 71\% to 83\% accuracy labeling which sentences are true versus false, depending on the LLM base model. Furthermore, we explore the relationship between our classifier's performance and approaches based on the probability assigned to the sentence by the LLM. We show that while LLM-assigned sentence probability is related to sentence truthfulness, this probability is also dependent on sentence length and the frequencies of words in the sentence, resulting in our trained classifier providing a more reliable approach to detecting truthfulness, highlighting its potential to enhance the reliability of LLM-generated content and its practical applicability in real-world scenarios.

**Flag.** ADJACENT - Internal-state probe for truthfulness of a statement. Bears on the self-signal, but it targets factual correctness of an assertion, not loop progress; the internal-readout angle is also a separate review topic here.

### 7. SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models

Potsawee Manakul, Adian Liusie, Mark J. F. Gales. *SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models.* 2023. EMNLP 2023 (main). arXiv:2303.08896 (2303.08896v3). https://arxiv.org/abs/2303.08896

**Abstract (verbatim).** Generative Large Language Models (LLMs) such as GPT-3 are capable of generating highly fluent responses to a wide variety of user prompts. However, LLMs are known to hallucinate facts and make non-factual statements which can undermine trust in their output. Existing fact-checking approaches either require access to the output probability distribution (which may not be available for systems such as ChatGPT) or external databases that are interfaced via separate, often complex, modules. In this work, we propose "SelfCheckGPT", a simple sampling-based approach that can be used to fact-check the responses of black-box models in a zero-resource fashion, i.e. without an external database. SelfCheckGPT leverages the simple idea that if an LLM has knowledge of a given concept, sampled responses are likely to be similar and contain consistent facts. However, for hallucinated facts, stochastically sampled responses are likely to diverge and contradict one another. We investigate this approach by using GPT-3 to generate passages about individuals from the WikiBio dataset, and manually annotate the factuality of the generated passages. We demonstrate that SelfCheckGPT can: i) detect non-factual and factual sentences; and ii) rank passages in terms of factuality. We compare our approach to several baselines and show that our approach has considerably higher AUC-PR scores in sentence-level hallucination detection and higher correlation scores in passage-level factuality assessment compared to grey-box methods.

**Flag.** ADJACENT - Black-box hallucination detection via sampling consistency. A self-consistency signal, but framed around factual hallucination in free-form generation rather than the done/stalled/abandon decision.

### 8. Reflexion: Language Agents with Verbal Reinforcement Learning

Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao. *Reflexion: Language Agents with Verbal Reinforcement Learning.* 2023. NeurIPS 2023 (per proceedings; not in arXiv metadata) - anchor. arXiv:2303.11366 (2303.11366v4). https://arxiv.org/abs/2303.11366

**Abstract (verbatim).** Large language models (LLMs) have been increasingly used to interact with external environments (e.g., games, compilers, APIs) as goal-driven agents. However, it remains challenging for these language agents to quickly and efficiently learn from trial-and-error as traditional reinforcement learning methods require extensive training samples and expensive model fine-tuning. We propose Reflexion, a novel framework to reinforce language agents not by updating weights, but instead through linguistic feedback. Concretely, Reflexion agents verbally reflect on task feedback signals, then maintain their own reflective text in an episodic memory buffer to induce better decision-making in subsequent trials. Reflexion is flexible enough to incorporate various types (scalar values or free-form language) and sources (external or internally simulated) of feedback signals, and obtains significant improvements over a baseline agent across diverse tasks (sequential decision-making, coding, language reasoning). For example, Reflexion achieves a 91% pass@1 accuracy on the HumanEval coding benchmark, surpassing the previous state-of-the-art GPT-4 that achieves 80%. We also conduct ablation and analysis studies using different feedback signals, feedback incorporation methods, and agent types, and provide insights into how they affect performance.

**Flag.** ADJACENT - Verbal reinforcement learning: a loop that retries on self-reflection plus an external reward/failure signal. Primarily an agent-improvement method (closer to topic 07), but its self-evaluation-gated retry is on the edge of the Subject.

### 9. Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback

Katherine Tian, Eric Mitchell, Allan Zhou, Archit Sharma, Rafael Rafailov, Huaxiu Yao, Chelsea Finn, Christopher D. Manning. *Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback.* 2023. EMNLP 2023 (camera ready). arXiv:2305.14975 (2305.14975v2). https://arxiv.org/abs/2305.14975

**Abstract (verbatim).** A trustworthy real-world prediction system should produce well-calibrated confidence scores; that is, its confidence in an answer should be indicative of the likelihood that the answer is correct, enabling deferral to an expert in cases of low-confidence predictions. Recent studies have shown that unsupervised pre-training produces large language models (LMs) whose conditional probabilities are remarkably well-calibrated. However, the most widely-used LMs are fine-tuned with reinforcement learning from human feedback (RLHF-LMs), and some studies have suggested that RLHF-LMs produce conditional probabilities that are very poorly calibrated. In light of this perceived weakness, we conduct a broad evaluation of methods for extracting confidence scores from RLHF-LMs. For RLHF-LMs such as ChatGPT, GPT-4, and Claude, we find that verbalized confidences emitted as output tokens are typically better-calibrated than the model's conditional probabilities on the TriviaQA, SciQ, and TruthfulQA benchmarks, often reducing the expected calibration error by a relative 50%.

**Flag.** RELATED - Eliciting calibrated verbalised confidence from RLHF-tuned models; finds verbalised probabilities beat conditional logits for such models.

### 10. A Survey of Confidence Estimation and Calibration in Large Language Models

Jiahui Geng, Fengyu Cai, Yuxia Wang, Heinz Koeppl, Preslav Nakov, Iryna Gurevych. *A Survey of Confidence Estimation and Calibration in Large Language Models.* 2023. NAACL 2024 (ACL Anthology 2024.naacl-long.366; not in arXiv metadata). arXiv:2311.08298 (2311.08298v2). https://arxiv.org/abs/2311.08298

**Abstract (verbatim).** Large language models (LLMs) have demonstrated remarkable capabilities across a wide range of tasks in various domains. Despite their impressive performance, they can be unreliable due to factual errors in their generations. Assessing their confidence and calibrating them across different tasks can help mitigate risks and enable LLMs to produce better generations. There has been a lot of recent research aiming to address this, but there has been no comprehensive overview to organize it and outline the main lessons learned. The present survey aims to bridge this gap. In particular, we outline the challenges and we summarize recent technical advancements for LLM confidence estimation and calibration. We further discuss their applications and suggest promising directions for future work.

**Flag.** RELATED - Survey of confidence estimation and calibration in LLMs - calibration is named in the Subject.

### 11. Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs

Miao Xiong, Zhiyuan Hu, Xinyang Lu, Yifei Li, Jie Fu, Junxian He, Bryan Hooi. *Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs.* 2023. ICLR 2024. arXiv:2306.13063 (2306.13063v2). https://arxiv.org/abs/2306.13063

**Abstract (verbatim).** Empowering large language models to accurately express confidence in their answers is essential for trustworthy decision-making. Previous confidence elicitation methods, which primarily rely on white-box access to internal model information or model fine-tuning, have become less suitable for LLMs, especially closed-source commercial APIs. This leads to a growing need to explore the untapped area of black-box approaches for LLM uncertainty estimation. To better break down the problem, we define a systematic framework with three components: prompting strategies for eliciting verbalized confidence, sampling methods for generating multiple responses, and aggregation techniques for computing consistency. We then benchmark these methods on two key tasks-confidence calibration and failure prediction-across five types of datasets (e.g., commonsense and arithmetic reasoning) and five widely-used LLMs including GPT-4 and LLaMA 2 Chat. Our analysis uncovers several key insights: 1) LLMs, when verbalizing their confidence, tend to be overconfident, potentially imitating human patterns of expressing confidence. 2) As model capability scales up, both calibration and failure prediction performance improve. 3) Employing our proposed strategies, such as human-inspired prompts, consistency among multiple responses, and better aggregation strategies can help mitigate this overconfidence from various perspectives. 4) Comparisons with white-box methods indicate that while white-box methods perform better, the gap is narrow, e.g., 0.522 to 0.605 in AUROC. Despite these advancements, none of these techniques consistently outperform others, and all investigated methods struggle in challenging tasks, such as those requiring professional knowledge, indicating significant scope for improvement. We believe this study can serve as a strong baseline and provide insights for eliciting confidence in black-box LLMs.

**Flag.** RELATED - Empirical evaluation of black-box confidence-elicitation methods (prompting, sampling, aggregation); finds LLMs are overconfident when verbalising and elicitation only partly fixes it.

**Review status.** reviewed -> sheet 05-express-uncertainty.md (round 2). Cross-paper discussion: pending.

### 12. Are You Sure? Challenging LLMs Leads to Performance Drops in The FlipFlop Experiment

Philippe Laban, Lidiya Murakhovs'ka, Caiming Xiong, Chien-Sheng Wu. *Are You Sure? Challenging LLMs Leads to Performance Drops in The FlipFlop Experiment.* 2023. Preprint (no venue in arXiv metadata). arXiv:2311.08596 (2311.08596v2). https://arxiv.org/abs/2311.08596

**Abstract (verbatim).** The interactive nature of Large Language Models (LLMs) theoretically allows models to refine and improve their answers, yet systematic analysis of the multi-turn behavior of LLMs remains limited. In this paper, we propose the FlipFlop experiment: in the first round of the conversation, an LLM completes a classification task. In a second round, the LLM is challenged with a follow-up phrase like "Are you sure?", offering an opportunity for the model to reflect on its initial answer, and decide whether to confirm or flip its answer. A systematic study of ten LLMs on seven classification tasks reveals that models flip their answers on average 46% of the time and that all models see a deterioration of accuracy between their first and final prediction, with an average drop of 17% (the FlipFlop effect). We conduct finetuning experiments on an open-source LLM and find that finetuning on synthetically created data can mitigate - reducing performance deterioration by 60% - but not resolve sycophantic behavior entirely. The FlipFlop experiment illustrates the universality of sycophantic behavior in LLMs and provides a robust framework to analyze model behavior and evaluate future models.

**Flag.** RELATED - The FlipFlop experiment: challenged with 'Are you sure?', models flip answers ~46% of the time and lose ~17% accuracy. Directly the confirm-or-revise self-judgement, and how sycophancy corrupts it. Preprint - noted, central.

### 13. R-Tuning: Instructing Large Language Models to Say `I Don't Know'

Hanning Zhang, Shizhe Diao, Yong Lin, Yi R. Fung, Qing Lian, Xingyao Wang, Yangyi Chen, Heng Ji et al.. *R-Tuning: Instructing Large Language Models to Say `I Don't Know'.* 2023. NAACL 2024. arXiv:2311.09677 (2311.09677v3). https://arxiv.org/abs/2311.09677

**Abstract (verbatim).** Large language models (LLMs) have revolutionized numerous domains with their impressive performance but still face their challenges. A predominant issue is the propensity for these models to generate non-existent facts, a concern termed hallucination. Our research is motivated by the observation that previous instruction tuning methods force the model to complete a sentence no matter whether the model knows the knowledge or not. When the question is out of the parametric knowledge, it will try to make up something and fail to indicate when it lacks knowledge. In this paper, we present a new approach called Refusal-Aware Instruction Tuning (R-Tuning). This approach is formalized by first identifying the disparity in knowledge encompassed by pre-trained parameters compared to that of instruction tuning data. Then, we construct the refusal-aware data based on the knowledge intersection, to tune LLMs to refrain from responding to questions beyond its parametric knowledge. Experimental results demonstrate R-Tuning effectively improves a model's ability to answer known questions and refrain from answering unknown questions. Furthermore, when tested on out-of-domain datasets, the refusal ability was found to be a meta-skill that could be generalized to other tasks. Further analysis surprisingly finds that learning the uncertainty results in better calibration and an improved ability to estimate the uncertainty than uncertainty-based testing. Our code is available at https://github.com/shizhediao/R-Tuning.

**Flag.** RELATED - R-Tuning: instruction-tuning a model to say 'I don't know' on questions outside its parametric knowledge - a training route to abstention.

### 14. Calibrating Long-form Generations from Large Language Models

Yukun Huang, Yixin Liu, Raghuveer Thirukovalluru, Arman Cohan, Bhuwan Dhingra. *Calibrating Long-form Generations from Large Language Models.* 2024. Findings of EMNLP 2024 (ACL Anthology 2024.findings-emnlp.785; not in arXiv metadata). arXiv:2402.06544 (2402.06544v2). https://arxiv.org/abs/2402.06544

**Abstract (verbatim).** To enhance Large Language Models' (LLMs) reliability, calibration is essential -- the model's assessed confidence scores should align with the actual likelihood of its responses being correct. However, current confidence elicitation methods and calibration metrics typically rely on a binary true/false assessment of response correctness. This approach does not apply to long-form generation, where an answer can be partially correct. Addressing this gap, we introduce a unified calibration framework, in which both the correctness of the LLMs' responses and their associated confidence levels are treated as distributions across a range of scores. Within this framework, we develop three metrics to precisely evaluate LLM calibration and further propose two confidence elicitation methods based on self-consistency and self-evaluation. Our experiments, which include long-form QA and summarization tasks, demonstrate that larger models don't necessarily guarantee better calibration, that calibration performance is found to be metric-dependent, and that self-consistency methods excel in factoid datasets. We also find that calibration can be enhanced through techniques such as fine-tuning, integrating relevant source documents, scaling the temperature, and combining self-consistency with self-evaluation. Lastly, we showcase a practical application of our system: selecting and cascading open-source models and ChatGPT to optimize correctness given a limited API budget. This research not only challenges existing notions of LLM calibration but also offers practical methodologies for improving trustworthiness in long-form generation.

**Flag.** RELATED - Calibration for long-form generation; confidence elicited via self-consistency and self-evaluation, with new long-form calibration metrics.

### 15. Self-Evaluation of Large Language Model based on Glass-box Features

Hui Huang, Yingqi Qu, Jing Liu, Muyun Yang, Bing Xu, Tiejun Zhao, Wenpeng Lu. *Self-Evaluation of Large Language Model based on Glass-box Features.* 2024. Findings of EMNLP 2024. arXiv:2403.04222 (2403.04222v2). https://arxiv.org/abs/2403.04222

**Abstract (verbatim).** The proliferation of open-source Large Language Models (LLMs) underscores the pressing need for evaluation methods. Existing works primarily rely on external evaluators, focusing on training and prompting strategies. However, a crucial aspect, model-aware glass-box features, is overlooked. In this study, we explore the utility of glass-box features under the scenario of self-evaluation, namely applying an LLM to evaluate its own output. We investigate various glass-box feature groups and discovered that the softmax distribution serves as a reliable quality indicator for self-evaluation. Experimental results on public benchmarks validate the feasibility of self-evaluation of LLMs using glass-box features.

**Flag.** RELATED - Self-evaluation of an LLM's own output using glass-box features (softmax distribution) as a quality indicator - the internal self-signal for 'is this good enough'.

**Review status.** reviewed -> sheet 07-glass-box-selfeval.md (round 2). Cross-paper discussion: pending.

### 16. Calibrating the Confidence of Large Language Models by Eliciting Fidelity

Mozhi Zhang, Mianqiu Huang, Rundong Shi, Linsen Guo, Chong Peng, Peng Yan, Yaqian Zhou, Xipeng Qiu. *Calibrating the Confidence of Large Language Models by Eliciting Fidelity.* 2024. EMNLP 2024 (main). arXiv:2404.02655 (2404.02655v2). https://arxiv.org/abs/2404.02655

**Abstract (verbatim).** Large language models optimized with techniques like RLHF have achieved good alignment in being helpful and harmless. However, post-alignment, these language models often exhibit overconfidence, where the expressed confidence does not accurately calibrate with their correctness rate. In this paper, we decompose the language model confidence into the \textit{Uncertainty} about the question and the \textit{Fidelity} to the answer generated by language models. Then, we propose a plug-and-play method to estimate the confidence of language models. Our method has shown good calibration performance by conducting experiments with 6 RLHF-LMs on four MCQA datasets. Moreover, we propose two novel metrics, IPR and CE, to evaluate the calibration of the model, and we have conducted a detailed discussion on \textit{Truly Well-Calibrated Confidence}. Our method could serve as a strong baseline, and we hope that this work will provide some insights into the model confidence calibration.

**Flag.** RELATED - Decomposes confidence into question-uncertainty and answer-fidelity; a plug-in calibration method for overconfident post-RLHF models, with new metrics IPR and CE.

### 17. Large Language Models Can Self-Correct with Key Condition Verification

Zhenyu Wu, Qingkai Zeng, Zhihan Zhang, Zhaoxuan Tan, Chao Shen, Meng Jiang. *Large Language Models Can Self-Correct with Key Condition Verification.* 2024. EMNLP 2024 (camera ready). arXiv:2405.14092 (2405.14092v3). https://arxiv.org/abs/2405.14092

**Abstract (verbatim).** Intrinsic self-correct was a method that instructed large language models (LLMs) to verify and correct their responses without external feedback. Unfortunately, the study concluded that the LLMs could not self-correct reasoning yet. We find that a simple yet effective verification method can unleash inherent capabilities of the LLMs. That is to mask a key condition in the question, add the current response to construct a verification question, and predict the condition to verify the response. The condition can be an entity in an open-domain question or a numeric value in a math question, which requires minimal effort (via prompting) to identify. We propose an iterative verify-then-correct framework to progressively identify and correct (probably) false responses, named ProCo. We conduct experiments on three reasoning tasks. On average, ProCo, with GPT-3.5-Turbo as the backend LLM, yields $+6.8$ exact match on four open-domain question answering datasets, $+14.1$ accuracy on three arithmetic reasoning datasets, and $+9.6$ accuracy on a commonsense reasoning dataset, compared to Self-Correct. Our implementation is made publicly available at https://wzy6642.github.io/proco.github.io/.

**Flag.** RELATED - Self-correction gated on the model first verifying a 'key condition' of the problem; a study of when self-correction actually helps versus hurts.

### 18. To Believe or Not to Believe Your LLM

Yasin Abbasi Yadkori, Ilja Kuzborskij, András György, Csaba Szepesvári. *To Believe or Not to Believe Your LLM.* 2024. NeurIPS 2024 (per proceedings; not in arXiv metadata). arXiv:2406.02543 (2406.02543v2). https://arxiv.org/abs/2406.02543

**Abstract (verbatim).** We explore uncertainty quantification in large language models (LLMs), with the goal to identify when uncertainty in responses given a query is large. We simultaneously consider both epistemic and aleatoric uncertainties, where the former comes from the lack of knowledge about the ground truth (such as about facts or the language), and the latter comes from irreducible randomness (such as multiple possible answers). In particular, we derive an information-theoretic metric that allows to reliably detect when only epistemic uncertainty is large, in which case the output of the model is unreliable. This condition can be computed based solely on the output of the model obtained simply by some special iterative prompting based on the previous responses. Such quantification, for instance, allows to detect hallucinations (cases when epistemic uncertainty is high) in both single- and multi-answer responses. This is in contrast to many standard uncertainty quantification strategies (such as thresholding the log-likelihood of a response) where hallucinations in the multi-answer case cannot be detected. We conduct a series of experiments which demonstrate the advantage of our formulation. Further, our investigations shed some light on how the probabilities assigned to a given output by an LLM can be amplified by iterative prompting, which might be of independent interest.

**Flag.** RELATED - Information-theoretic separation of epistemic and aleatoric uncertainty via iterative prompting; detects when only epistemic uncertainty is high, i.e. when the output should not be trusted.

**Review status.** reviewed -> sheet 02-believe-or-not.md (round 1). Cross-paper discussion: pending.

### 19. Semantic Entropy Probes: Robust and Cheap Hallucination Detection in LLMs

Jannik Kossen, Jiatong Han, Muhammed Razzak, Lisa Schut, Shreshth Malik, Yarin Gal. *Semantic Entropy Probes: Robust and Cheap Hallucination Detection in LLMs.* 2024. NeurIPS 2024 (per venue listing; not in arXiv metadata). arXiv:2406.15927 (2406.15927v1). https://arxiv.org/abs/2406.15927

**Abstract (verbatim).** We propose semantic entropy probes (SEPs), a cheap and reliable method for uncertainty quantification in Large Language Models (LLMs). Hallucinations, which are plausible-sounding but factually incorrect and arbitrary model generations, present a major challenge to the practical adoption of LLMs. Recent work by Farquhar et al. (2024) proposes semantic entropy (SE), which can detect hallucinations by estimating uncertainty in the space semantic meaning for a set of model generations. However, the 5-to-10-fold increase in computation cost associated with SE computation hinders practical adoption. To address this, we propose SEPs, which directly approximate SE from the hidden states of a single generation. SEPs are simple to train and do not require sampling multiple model generations at test time, reducing the overhead of semantic uncertainty quantification to almost zero. We show that SEPs retain high performance for hallucination detection and generalize better to out-of-distribution data than previous probing methods that directly predict model accuracy. Our results across models and tasks suggest that model hidden states capture SE, and our ablation studies give further insights into the token positions and model layers for which this is the case.

**Flag.** ADJACENT - Semantic entropy probes: approximate semantic entropy from one generation's hidden states. An uncertainty signal, but framed for factual hallucination detection rather than the loop-stopping decision.

### 20. Know Your Limits: A Survey of Abstention in Large Language Models

Bingbing Wen, Jihan Yao, Shangbin Feng, Chenjun Xu, Yulia Tsvetkov, Bill Howe, Lucy Lu Wang. *Know Your Limits: A Survey of Abstention in Large Language Models.* 2024. TACL 2024. arXiv:2407.18418 (2407.18418v3). https://arxiv.org/abs/2407.18418

**Abstract (verbatim).** Abstention, the refusal of large language models (LLMs) to provide an answer, is increasingly recognized for its potential to mitigate hallucinations and enhance safety in LLM systems. In this survey, we introduce a framework to examine abstention from three perspectives: the query, the model, and human values. We organize the literature on abstention methods, benchmarks, and evaluation metrics using this framework, and discuss merits and limitations of prior work. We further identify and motivate areas for future research, such as whether abstention can be achieved as a meta-capability that transcends specific tasks or domains, and opportunities to optimize abstention abilities in specific contexts. In doing so, we aim to broaden the scope and impact of abstention methodologies in AI systems.

**Flag.** RELATED - Survey of abstention in LLMs across query / model / human-values perspectives; asks whether abstention can be a task-transcending meta-capability. Abstention is named in the Subject.

### 21. On Verbalized Confidence Scores for LLMs

Daniel Yang, Yao-Hung Hubert Tsai, Makoto Yamada. *On Verbalized Confidence Scores for LLMs.* 2024. Preprint (no venue in arXiv metadata). arXiv:2412.14737 (2412.14737v2). https://arxiv.org/abs/2412.14737

**Abstract (verbatim).** The rise of large language models (LLMs) and their tight integration into our daily life make it essential to dedicate efforts towards their trustworthiness. Uncertainty quantification for LLMs can establish more human trust into their responses, but also allows LLM agents to make more informed decisions based on each other's uncertainty. To estimate the uncertainty in a response, internal token logits, task-specific proxy models, or sampling of multiple responses are commonly used. This work focuses on asking the LLM itself to verbalize its uncertainty with a confidence score as part of its output tokens, which is a promising way for prompt- and model-agnostic uncertainty quantification with low overhead. Using an extensive benchmark, we assess the reliability of verbalized confidence scores with respect to different datasets, models, and prompt methods. Our results reveal that the reliability of these scores strongly depends on how the model is asked, but also that it is possible to extract well-calibrated confidence scores with certain prompt methods. We argue that verbalized confidence scores can become a simple but effective and versatile uncertainty quantification method in the future. Our code is available at https://github.com/danielyxyang/llm-verbalized-uq.

**Flag.** RELATED - Benchmark of verbalised confidence scores across datasets, models and prompts; reliability depends heavily on how the model is asked, but well-calibrated scores are extractable with some prompts. Preprint - noted.

### 22. Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge

Jiayi Ye, Yanbo Wang, Yue Huang, Dongping Chen, Qihui Zhang, Nuno Moniz, Tian Gao, Werner Geyer et al.. *Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge.* 2024. ICLR 2025 (per publication listing; not in arXiv metadata). arXiv:2410.02736 (2410.02736v2). https://arxiv.org/abs/2410.02736

**Abstract (verbatim).** LLM-as-a-Judge has been widely utilized as an evaluation method in various benchmarks and served as supervised rewards in model training. However, despite their excellence in many domains, potential issues are under-explored, undermining their reliability and the scope of their utility. Therefore, we identify 12 key potential biases and propose a new automated bias quantification framework-CALM-which systematically quantifies and analyzes each type of bias in LLM-as-a-Judge by using automated and principle-guided modification. Our experiments cover multiple popular language models, and the results indicate that while advanced models have achieved commendable overall performance, significant biases persist in certain specific tasks. Empirical results suggest that there remains room for improvement in the reliability of LLM-as-a-Judge. Moreover, we also discuss the explicit and implicit influence of these biases and give some suggestions for the reliable application of LLM-as-a-Judge. Our work highlights the need for stakeholders to address these issues and remind users to exercise caution in LLM-as-a-Judge applications.

**Flag.** RELATED - CALM framework quantifying 12 biases in LLM-as-a-Judge; bears on using a model to judge output, including its own (position, verbosity, self-preference, etc.).

**Review status.** reviewed -> sheet 06-judge-biases.md (round 2). Cross-paper discussion: pending.

### 23. Stop Overthinking: A Survey on Efficient Reasoning for Large Language Models

Yang Sui, Yu-Neng Chuang, Guanchu Wang, Jiamu Zhang, Tianyi Zhang, Jiayi Yuan, Hongyi Liu, Andrew Wen et al.. *Stop Overthinking: A Survey on Efficient Reasoning for Large Language Models.* 2025. TMLR 2025. arXiv:2503.16419 (2503.16419v4). https://arxiv.org/abs/2503.16419

**Abstract (verbatim).** Large Language Models (LLMs) have demonstrated remarkable capabilities in complex tasks. Recent advancements in Large Reasoning Models (LRMs), such as OpenAI o1 and DeepSeek-R1, have further improved performance in System-2 reasoning domains like mathematics and programming by harnessing supervised fine-tuning (SFT) and reinforcement learning (RL) techniques to enhance the Chain-of-Thought (CoT) reasoning. However, while longer CoT reasoning sequences improve performance, they also introduce significant computational overhead due to verbose and redundant outputs, known as the "overthinking phenomenon". In this paper, we provide the first structured survey to systematically investigate and explore the current progress toward achieving efficient reasoning in LLMs. Overall, relying on the inherent mechanism of LLMs, we categorize existing works into several key directions: (1) model-based efficient reasoning, which considers optimizing full-length reasoning models into more concise reasoning models or directly training efficient reasoning models; (2) reasoning output-based efficient reasoning, which aims to dynamically reduce reasoning steps and length during inference; (3) input prompts-based efficient reasoning, which seeks to enhance reasoning efficiency based on input prompt properties such as difficulty or length control. Additionally, we introduce the use of efficient data for training reasoning models, explore the reasoning capabilities of small language models, and discuss evaluation methods and benchmarking. Project website: https://github.com/Eclipsess/Awesome-Efficient-Reasoning-LLMs

**Flag.** RELATED - Survey of efficient reasoning - when to stop thinking (reasoning length), including trajectory-signal and confidence-based early exit. Overlaps the exhausted-budget / no-progress signals in the Subject.

**Review status.** reviewed -> sheet 04-stop-overthinking.md (round 1). Cross-paper discussion: pending.

### 24. AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions

Polina Kirichenko, Mark Ibrahim, Kamalika Chaudhuri, Samuel J. Bell. *AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions.* 2025. NeurIPS 2025 (per venue listing; not in arXiv metadata). arXiv:2506.09038 (2506.09038v1). https://arxiv.org/abs/2506.09038

**Abstract (verbatim).** For Large Language Models (LLMs) to be reliably deployed in both everyday and high-stakes domains, knowing when not to answer is equally critical as answering correctly. Real-world user queries, which can be underspecified, ill-posed, or fundamentally unanswerable, require LLMs to reason about uncertainty and selectively abstain -- i.e., refuse to answer definitively. However, abstention remains understudied, without a systematic evaluation framework for modern LLMs. In this work, we introduce AbstentionBench, a large-scale benchmark for holistically evaluating abstention across 20 diverse datasets, including questions with unknown answers, underspecification, false premises, subjective interpretations, and outdated information. Evaluating 20 frontier LLMs reveals abstention is an unsolved problem, and one where scaling models is of little use. While recent reasoning LLMs have shown impressive results in complex problem solving, surprisingly, we find that reasoning fine-tuning degrades abstention (by $24\%$ on average), even for math and science domains on which reasoning models are explicitly trained. We find that while a carefully crafted system prompt can boost abstention in practice, it does not resolve models' fundamental inability to reason about uncertainty. We release AbstentionBench to foster research into advancing LLM reliability.

**Flag.** RELATED - AbstentionBench: 20-dataset benchmark for abstention on unanswerable / underspecified / false-premise questions. Finds abstention unsolved, scale does not help, and reasoning fine-tuning degrades it by ~24%.

**Review status.** reviewed -> sheet 03-abstentionbench.md (round 1). Cross-paper discussion: pending.

### 25. Answering the Unanswerable Is to Err Knowingly: Analyzing and Mitigating Abstention Failures in Large Reasoning Models

Yi Liu, Xiangyu Liu, Zequn Sun, Wei Hu. *Answering the Unanswerable Is to Err Knowingly: Analyzing and Mitigating Abstention Failures in Large Reasoning Models.* 2025. AAAI 2026. arXiv:2508.18760 (2508.18760v3). https://arxiv.org/abs/2508.18760

**Abstract (verbatim).** Large reasoning models (LRMs) have shown remarkable progress on complex reasoning tasks. However, some questions posed to LRMs are inherently unanswerable, such as math problems lacking sufficient conditions. We find that LRMs continually fail to provide appropriate abstentions when confronted with these unanswerable questions. In this paper, we systematically analyze, investigate, and resolve this issue for trustworthy AI. We first conduct a detailed analysis of the distinct response behaviors of LRMs when facing unanswerable questions. Then, we show that LRMs possess sufficient cognitive capabilities to recognize the flaws in these questions. However, they fail to exhibit appropriate abstention behavior, revealing a misalignment between their internal cognition and external response. Finally, to resolve this issue, we propose a lightweight, two-stage method that combines cognitive monitoring with inference-time intervention. Experimental results demonstrate that our method significantly improves the abstention rate while maintaining the overall reasoning performance.

**Flag.** RELATED - Analyses and mitigates abstention failures in large reasoning models; finds they have an internal sense of solvability but fail to express abstention.

### 26. Self-Reflection in LLM Agents: Effects on Problem-Solving Performance

Matthew Renze, Erhan Guven. *Self-Reflection in LLM Agents: Effects on Problem-Solving Performance.* 2024. FLLM 2024 (IEEE, 2nd Intl. Conf. on Foundation and Large Language Models, pp. 476-483; DOI 10.1109/FLLM63129.2024.10852493). arXiv:2405.06682 (2405.06682v3). https://arxiv.org/abs/2405.06682

**Abstract (verbatim).** In this study, we investigated the effects of self-reflection in large language models (LLMs) on problem-solving performance. We instructed nine popular LLMs to answer a series of multiple-choice questions to provide a performance baseline. For each incorrectly answered question, we instructed eight types of self-reflecting LLM agents to reflect on their mistakes and provide themselves with guidance to improve problem-solving. Then, using this guidance, each self-reflecting agent attempted to re-answer the same questions. Our results indicate that LLM agents are able to significantly improve their problem-solving performance through self-reflection ($p < 0.001$). In addition, we compared the various types of self-reflection to determine their individual contribution to performance. All code and data are available on GitHub at https://github.com/matthewrenze/self-reflection

**Flag.** ADJACENT - Self-reflection improves re-answering of questions the harness already knows were wrong. Because the wrong-answer trigger is an oracle, it does not test the detect-your-own-failure decision the Subject centres on.

### 27. Reliability without Validity: A Systematic, Large-Scale Evaluation of LLM-as-a-Judge Models Across Agreement, Consistency, and Bias

Justin D. Norman, Michael U. Rivera, D. Alex Hughes. *Reliability without Validity: A Systematic, Large-Scale Evaluation of LLM-as-a-Judge Models Across Agreement, Consistency, and Bias.* 2026. Preprint (no venue in arXiv metadata). arXiv:2606.19544 (2606.19544v1). https://arxiv.org/abs/2606.19544

**Abstract (verbatim).** LLM-as-a-Judge has become the dominant evaluation paradigm for language models, but judge validation in practice relies on exact-match agreement, a metric that does not correct for chance and systematically overstates discriminative ability. We present the largest systematic evaluation of LLM-as-a-Judge to date: 21 judges from nine providers across MT-Bench, JudgeBench, and RewardBench, evaluated under three protocols (agreement, consistency, bias audit) over 118 runs and approximately 541,000 individual judgments. Four findings emerge, consistent across the full cohort, including the April 2026 frontier: kappa deflation between exact match and Cohen's kappa is universal (33--41 pp on MT-Bench), judge rankings shift by up to 14 positions across benchmarks, high test--retest reliability (>0.95) coexists with severe position bias (>0.10) in two production-deployed judges (instantiating a consistency--bias paradox), and verbosity bias is small (<0.011) across our cohort under a single pairwise rubric. We distill these into a Minimum Viable Validation Protocol.

**Flag.** RELATED - Large-scale evaluation of LLM-as-a-Judge on agreement, consistency and bias; argues high agreement does not imply valid scores. The Subject names the reliability of a model as a judge of its own output. Preprint - noted, central.

### 28. Semantic Early-Stopping for Iterative LLM Agent Loops

Sahil Shrivastava. *Semantic Early-Stopping for Iterative LLM Agent Loops.* 2026. Preprint (no venue in arXiv metadata). arXiv:2606.27009 (2606.27009v1). https://arxiv.org/abs/2606.27009

**Abstract (verbatim).** Multi-agent large language model (LLM) loops, for example a Writer that drafts and a Critic that revises, are almost always terminated by a fixed iteration cap (max_iterations). This is a syntactic kill-switch: it is blind to whether the answer is still improving, so it over-spends tokens on easy inputs and truncates hard ones. We study semantic early-stopping: the loop halts when consecutive draft embeddings stop changing in meaning (cosine distance with a patience window) and the answer's measured quality stops improving. Our work makes three contributions. First, an honest theoretical footing: we prove deterministic termination and well-definedness and machine-check these claims, while treating the convergence of the distance sequence as an empirically tested conjecture rather than a (previously over-claimed) Banach contraction. Second, a judge-efficient evaluation protocol: we generate each question's full trajectory once, replay every stopping policy over the identical drafts, and cache every LLM-judge call, yielding a strictly paired efficiency-versus-quality comparison at low cost; we further separate operational tokens (charged to a policy) from evaluation tokens (a measurement instrument). Third, an empirical study on multi-hop retrieval-augmented question answering (HotpotQA). On the 60-question test split, a judge-free semantic stopper reduces operational tokens by 38% relative to max_iterations at parity quality (Delta-IS = -0.004, p = 0.81), whereas the full quality-gated variant is counter-productive because its per-round judging dominates cost. An oracle that selects the best round attains +0.115 Information Score over every practical policy (p ~ 4e-11), reframing the problem from "when to stop" (easy) to "which round is best" (open).

**Flag.** RELATED - Semantic early-stopping for iterative agent loops: halt when consecutive draft embeddings stop changing in meaning and measured quality plateaus, with termination guarantees. Directly a stopping criterion. Preprint - noted, central.

### 29. When Agents Do Not Stop: Uncovering Infinite Agentic Loops in LLM Agents

Xinyi Hou, Shenao Wang, Yanjie Zhao, Haoyu Wang. *When Agents Do Not Stop: Uncovering Infinite Agentic Loops in LLM Agents.* 2026. Preprint (no venue in arXiv metadata). arXiv:2607.01641 (2607.01641v1). https://arxiv.org/abs/2607.01641

**Abstract (verbatim).** LLM agents increasingly rely on iterative execution to solve tasks through planning, tool use, state updates, and agent collaboration. While this design enables flexible automation, it also creates a new class of failures: an agent may repeatedly execute model calls, tools, workflow transitions, or agent handoffs when the feedback path is not effectively bounded. We call this problem Infinite Agentic Loops (IALs). IALs are not ordinary programming loops; they arise from the interaction between agent logic, framework semantics, runtime observations, and termination mechanisms. Such failures can amplify a single request into long running model and tool execution, causing cost exhaustion, model denial of service, context growth, and repeated external side effects. We propose IAL-Scan, a static analysis tool for detecting IAL failures in real-world LLM agent projects. IAL-Scan abstracts heterogeneous agent code into a framework independent Agent IR, builds an Agentic Loop Dependence Graph (ALDG) to recover explicit and framework induced feedback paths, and checks whether these paths can repeatedly reach costly or state growing operations without an effective bound. We evaluate IAL-Scan on 6,549 LLM agent repositories. It reports 74 potential findings, among which manual review confirms 68 IAL failures across 47 projects, achieving 91.9% precision.

**Flag.** RELATED - Characterises infinite agentic loops - the failure of an agent that never decides to stop. Preprint - noted, central.

### 30. Verify, Repair, Repeat, or Stop? Robust Stopping for Noisy Verify-Repair Loops in LLM Agents

Yitao Wu, Si Shen, Rui Yang, Hong Peng, Bin Hu. *Verify, Repair, Repeat, or Stop? Robust Stopping for Noisy Verify-Repair Loops in LLM Agents.* 2026. Preprint (no venue in arXiv metadata; under review). arXiv:2607.17641 (2607.17641v1). https://arxiv.org/abs/2607.17641

**Abstract (verbatim).** Verify-repair loops are a standard means for large language model (LLM) agents to correct faulty plans in code generation, mathematical reasoning, and tool use. When both the verifier and the repairer are noisy, repair can damage already-correct plans, and reported acceptance keeps rising while true validity falls, so existing methods lack a principled basis for deciding when repair should stop. We propose VRR-Stop, a robust stopping framework for noisy verify-repair-repeat (VRR) loops. A four-parameter noise model separates verifier false acceptance and false rejection from the repair and damage behavior of the repairer. Belief filtering turns repeated verification votes into an estimate of committed validity, and the loop commits or repairs according to the sign of the true marginal gain, which requires only sign identifiability rather than accurate recovery of all parameters. When verifier discrimination approaches zero, calibration itself fails and estimation error can flip the stopping sign, so we pair VRR-Stop with VRR-Guard, an estimation-free fallback that replaces the incumbent candidate only under a sufficient verification margin. On a GSM8K stress setting, VRR-Stop improves final true validity by 60.6 percentage points over fixed five-round repair at an average cost of 0.72 repair rounds. Across settings, stopping reliability is governed jointly by verifier discrimination and the decision margin rather than by the absolute size of estimation error.

**Flag.** RELATED - Robust stopping for noisy verify-repair loops: separates verifier false-accept / false-reject from repair damage and stops on the true marginal gain of continued repair. Directly the Subject. Preprint - noted, central.

### 31. Detecting hallucinations in large language models using semantic entropy

Sebastian Farquhar, Jannik Kossen, Lorenz Kuhn, Yarin Gal. *Detecting hallucinations in large language models using semantic entropy.* 2024. Nature 630, 625-630. DOI 10.1038/s41586-024-07421-0. https://www.nature.com/articles/s41586-024-07421-0

**Abstract (verbatim).** Retrieved from nature.com 2026-09-09 (booth 20); superscript reference numerals removed, wording otherwise unaltered. "Large language model (LLM) systems, such as ChatGPT or Gemini, can show impressive reasoning and question-answering capabilities but often 'hallucinate' false outputs and unsubstantiated answers. Answering unreliably or without the necessary information prevents adoption in diverse fields, with problems including fabrication of legal precedents or untrue facts in news articles and even posing a risk to human life in medical domains such as radiology. Encouraging truthfulness through supervision or reinforcement has been only partially successful. Researchers need a general method for detecting hallucinations in LLMs that works even with new and unseen questions to which humans might not know the answer. Here we develop new methods grounded in statistics, proposing entropy-based uncertainty estimators for LLMs to detect a subset of hallucinations—confabulations—which are arbitrary and incorrect generations. Our method addresses the fact that one idea can be expressed in many ways by computing uncertainty at the level of meaning rather than specific sequences of words. Our method works across datasets and tasks without a priori knowledge of the task, requires no task-specific data and robustly generalizes to new tasks not seen before. By detecting when a prompt is likely to produce a confabulation, our method helps users understand when they must take extra care with LLMs and opens up new possibilities for using LLMs that are otherwise prevented by their unreliability."

**Flag.** RELATED (anchor) - the canonical uncertainty-based 'do not trust this output' signal that the later probe and early-stopping work builds on; abstract pending verbatim capture.

## 2. Selected for review

_Step 2 output - four picks, one line each on why. Select for spread, not fit.
Selected 2026-09-07. All four are peer-reviewed; the dedicated agentic-loop
stopping literature is 2026 preprints (entries 27-30) and is left out of this
round per the topic scope rule._

- **Round 1, booth 01 - Kamoi et al., "When Can LLMs Actually Correct Their Own
  Mistakes? A Critical Survey of Self-Correction" (TACL 2024).** A skeptical
  meta-analysis: it re-frames the whole self-judged stop-or-repeat question,
  separates the research questions prior work conflated, and argues intrinsic
  self-correction from prompted LLMs essentially never works. Picked as the
  frame-setting critical view.
- **Round 1, booth 02 - "To Believe or Not to Believe Your LLM" (NeurIPS 2024).**
  A method/theory paper: an information-theoretic metric from iterative prompting
  that separates epistemic from aleatoric uncertainty and flags when an output
  should not be trusted. Picked for a principled mechanism, distinct in kind from
  the surveys and benchmarks.
- **Round 1, booth 03 - "AbstentionBench: Reasoning LLMs Fail on Unanswerable
  Questions" (NeurIPS 2025).** A large frontier benchmark for the decline / abandon
  / hand-off end of the Subject, with a sharp negative result: scaling does not
  help and reasoning fine-tuning degrades abstention by ~24%.
- **Round 1, booth 04 - "Stop Overthinking: A Survey on Efficient Reasoning for
  Large Language Models" (TMLR 2025).** The one peer-reviewed entry covering
  stopping criteria for iterative generation - reasoning-length control, early
  exit, confidence- and trajectory-based halting. Picked to cover a sub-area the
  other three do not touch.

**Review status.** Booths 01-04 fired 2026-09-07 (all four at once); all four read, sheets imported, cross-paper discussion pending.

### Round 2 (selected 2026-09-07)

Spread across sub-areas round 1 did not touch: black-box confidence elicitation,
model-as-judge bias, the white-box (internal) self-signal, and the
self-knowledge boundary.

- **Booth 05 - Xiong et al., "Can LLMs Express Their Uncertainty? An Empirical
  Evaluation of Confidence Elicitation in LLMs" (ICLR 2024).** The canonical
  empirical benchmark of black-box confidence: a grid of prompting × sampling ×
  aggregation strategies scored on calibration and failure detection. Picked for
  the measured version of "the model's own report" signal.
- **Booth 06 - "Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge"
  (ICLR 2025).** The Subject names the reliability of a model as a judge of its
  own output; round 1 did not cover it. CALM framework, 12 named biases,
  perturbation that isolates each while holding quality constant - including
  self-preference.
- **Booth 07 - "Self-Evaluation of Large Language Model based on Glass-box
  Features" (Findings of EMNLP 2024).** The white-box self-signal: softmax /
  entropy features of the model's own generation as a quality indicator, distinct
  in kind from verbalised confidence and from an external judge.
- **Booth 08 - Yin et al., "Do Large Language Models Know What They Don't Know?"
  (Findings of ACL 2023).** The self-knowledge boundary - the SelfAware benchmark
  of unanswerable questions plus an automated unanswerability metric. The "is this
  beyond me" judgement in isolation.

**Review status.** Booths 05-08 fired 2026-09-07; all four read, sheets imported. Cross-paper discussion for sheets 01-08 done 2026-09-08 -> `00e-buffer.md` (candidate findings CF-1..CF-15, proposed ideas PI-1..PI-6).

### Rounds 3 and 4 (selected 2026-09-08)

The user authorised two more rounds. The peer-reviewed corpus does not cover the
agentic-loop stopping decision itself; the dedicated papers are 2026 preprints
(inventory #25, #27, #28, #29, #30). Following the topic-07 precedent for central
preprints, rounds 3 and 4 read those alongside the peer-reviewed anchors they
build on. Spread over the two rounds: loop-stopping mechanisms, the
loop-non-termination failure mode, the canonical self-reflection loop, the
white-box self-knowledge anchor, a peer-reviewed large-reasoning-model abstention
paper, the sycophancy-under-challenge effect, and a large-scale judge-reliability
audit.

- **Round 3, booth 09 - "Semantic Early-Stopping for Iterative LLM Agent Loops"**
  (#28, arXiv:2606.27009). Embedding-convergence plus quality-plateau stop rule
  with a termination proof; the "which round is best" reframe.
- **Round 3, booth 10 - "Verify, Repair, Repeat, or Stop?" (VRR-Stop)**
  (#30, arXiv:2607.17641). Four-parameter noise model separating verifier
  false-accept / false-reject from repair damage; stop on the sign of the true
  marginal gain.
- **Round 3, booth 11 - "When Agents Do Not Stop: Uncovering Infinite Agentic
  Loops"** (#29, arXiv:2607.01641). Static analysis of unbounded feedback paths;
  the non-termination failure characterised directly.
- **Round 3, booth 12 - Shinn et al., "Reflexion"** (#8, arXiv:2303.11366,
  NeurIPS 2023). The canonical self-reflection-gated retry loop; peer-reviewed;
  untouched by rounds 1-2.
- **Round 4, booth 13 - Kadavath et al., "Language Models (Mostly) Know What
  They Know"** (#3, arXiv:2207.05221, 2022 anchor). P(True) and P(IK); the
  white-box counterweight to the "self-report is useless" convergence.
- **Round 4, booth 14 - Liu et al., "Answering the Unanswerable Is to Err
  Knowingly"** (#25, arXiv:2508.18760, AAAI 2026). Large reasoning models have an
  internal sense of solvability but do not express abstention.
- **Round 4, booth 15 - Laban et al., "Are You Sure? The FlipFlop Experiment"**
  (#12, arXiv:2311.08596). Challenged with "Are you sure?", models flip ~46% and
  lose ~17% accuracy; sycophancy corrupting the confirm-or-revise judgement.
- **Round 4, booth 16 - Norman et al., "Reliability without Validity"**
  (#27, arXiv:2606.19544). 21 judges, ~541k judgments; kappa deflation; the
  consistency-versus-bias paradox; a Minimum Viable Validation Protocol.

**Review status.** Booths 09-16 (rounds 3-4) all read and imported as sheets
`09`-`16` on 2026-09-08 (booth 14 resumed once from a session rate limit).
Cross-paper discussion for rounds 3-4 done 2026-09-08 -> `00e-buffer.md`
(candidate findings CF-16..CF-25, proposed ideas PI-7, PI-8).

### Gap-closing candidates from search (2026-09-08)

Two targeted searches for angles the inventory was thin on. All 2026 preprints;
verbatim abstracts not yet captured. Staged in `00e-buffer.md` section 3.

- Value-of-computation stopping: "Knowing When to Quit" (arXiv:2604.18419);
  "Agentic Abstention: Do Agents Know When to Stop Instead of Act?"
  (arXiv:2606.28733); "Doomed from the Start" early-abort probe cascade
  (arXiv:2607.06503); Meta-Reasoner (arXiv:2502.19918).
- Runtime stall / repeated-action detection: "Early Diagnosis of Wasted
  Computation ... via Failure-Aware Observability" (arXiv:2606.01365); "When
  Agentic Executions Fail ... Runtime Faults from Telemetry" (arXiv:2608.14680);
  "MIRAGE-Bench" agent hallucination (arXiv:2507.21017).

### Round 5 (selected 2026-09-09)

Narrow pass targeting the gap the rounds 1-4 sheets all flag in their limitations
— single-turn, not measured in a trajectory — plus the decision-theoretic
framing none of the 16 carry, plus the semantic-entropy anchor.

- **Booth 17 — "Knowing When to Quit: A Principled Framework for Dynamic
  Abstention in LLM Reasoning"** (arXiv:2604.18419, preprint). Halt when a
  value-function estimate falls below an abstention-reward threshold — "is the
  next step worth its cost".
- **Booth 18 — "Agentic Abstention: Do Agents Know When to Stop Instead of
  Act?"** (arXiv:2606.28733, preprint). Abstention measured in a multi-step
  agentic setting.
- **Booth 19 — "Meta-Reasoner: Dynamic Guidance for Optimized Inference-time
  Reasoning"** (arXiv:2502.19918, preprint). A contextual bandit over per-step
  progress reports — the nearest thing to a learned progress judge (sheet 04
  named it).
- **Booth 20 — Kuhn, Gal, Farquhar, "Semantic Uncertainty" (ICLR 2023,
  arXiv:2302.09664)** as primary, with a note on the Nature 2024 follow-up
  (inventory #31, abstract still to capture).

**Review status.** Booths 17-20 read and imported as sheets `17`-`20` on
2026-09-09 (no rate limits). Booth 17's paper is ICML 2026 (PMLR 306), not a
preprint — brief was out of date. Farquhar Nature 2024 abstract captured via
booth 20 into inventory entry 31. Round-5 cross-paper pass done 2026-09-09 ->
`00e-buffer.md` (CF-31..CF-35; CF-34 recommended merge into F4; F4 updated with
semantic-entropy evidence).

## Findings graduated (running)

- **F1** <- CF-1 (self-report cannot site the stop decision).
- **F2** <- CF-29 (validation trust runs inverse to work-context continuity).
- **F3** <- CF-30 (draft-independent vs draft-dependent check resources).
- **F4** <- CF-2 (resample-agreement; stability not correctness folded in).
- **F5** <- CF-4 (verifiable-reward optimisation erodes willingness to decline).
- CF-3 cut (fold the stability caveat inline, no indirection).

