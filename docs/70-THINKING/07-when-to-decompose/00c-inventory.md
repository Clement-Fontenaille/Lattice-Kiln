# Inventory — When to Decompose, and How Deep

Collection-phase inventory. One block per paper: cite line, full abstract quoted
verbatim, and a RELATED / ADJACENT / NOT RELATED flag with a one-line reason.
Scope: peer-reviewed papers 2023 onward (journal, conference, or reviewed
workshop). arXiv-only preprints are listed under "Excluded pending publication"
when central. Pre-2023 work marked as anchor where later work repeatedly builds
on it.

---

## 1. Select-Then-Decompose
**Review status:** reviewed -> sheet `04` (round 1). Cross-paper discussion: done - F7-F12, partial F1, F9 (with `08`); feeds A1, I1, I2.


**Cite:** Shuodi Liu, Yingzhuo Liu, Zi Wang, Yusheng Wang, Huijia Wu, Liuyu Xiang, Zhaofeng He. "Select-Then-Decompose: From Empirical Analysis to Adaptive Selection Strategy for Task Decomposition in Large Language Models." 2025. Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing (EMNLP 2025), main track. DOI: 10.18653/v1/2025.emnlp-main.278. https://aclanthology.org/2025.emnlp-main.278/

**Abstract (verbatim):**
> Large language models (LLMs) have demonstrated remarkable reasoning and planning capabilities, driving extensive research into task decomposition. Existing task decomposition methods focus primarily on memory, tool usage, and feedback mechanisms, achieving notable success in specific domains, but they often overlook the trade-off between performance and cost. In this study, we first conduct a comprehensive investigation on task decomposition, identifying six categorization schemes. Then, we perform an empirical analysis of three factors that influence the performance and cost of task decomposition: categories of approaches, characteristics of tasks, and configuration of decomposition and execution models, uncovering three critical insights and summarizing a set of practical principles. Building on this analysis, we propose the Select-Then-Decompose strategy, which establishes a closed-loop problem-solving process composed of three stages: selection, execution, and verification. This strategy dynamically selects the most suitable decomposition approach based on task characteristics and enhances the reliability of the results through a verification module. Comprehensive evaluations across multiple benchmarks show that the Select-Then-Decompose consistently lies on the Pareto frontier, demonstrating an optimal balance between performance and cost. Our code is publicly available at https://github.com/summervvind/Select-Then-Decompose.

**Flag:** RELATED — directly studies when/how to decompose, taxonomises decomposition approaches, and centres the performance-vs-cost trade-off the Subject names.

---

## 2. ADaPT
**Review status:** reviewed -> sheet `05` (round 2). Cross-paper discussion: done - F17, F18, F19, F20, F21, F23.


**Cite:** Archiki Prasad, Alexander Koller, Mareike Hartmann, Peter Clark, Ashish Sabharwal, Mohit Bansal, Tushar Khot. "ADaPT: As-Needed Decomposition and Planning with Language Models." 2024. Findings of the Association for Computational Linguistics: NAACL 2024. DOI: 10.18653/v1/2024.findings-naacl.264. arXiv:2311.05772. https://aclanthology.org/2024.findings-naacl.264/

**Abstract (verbatim):**
> Large Language Models (LLMs) are increasingly being used for interactive decision-making tasks requiring planning and adapting to the environment. Recent works employ LLMs-as-agents in broadly two ways: iteratively determining the next action (iterative executors) or generating plans and executing sub-tasks using LLMs (plan-and-execute). However, these methods struggle with task complexity, as the inability to execute any sub-task may lead to task failure. To address these shortcomings, we introduce As-Needed Decomposition and Planning for complex Tasks (ADaPT), an approach that explicitly plans and decomposes complex sub-tasks as-needed, i.e., when the LLM is unable to execute them. ADaPT recursively decomposes sub-tasks to adapt to both task complexity and LLM capability. Our results demonstrate that ADaPT substantially outperforms established strong baselines, achieving success rates up to 28.3% higher in ALFWorld, 27% in WebShop, and 33% in TextCraft – a novel compositional dataset that we introduce. Through extensive analysis, we illustrate the importance of multilevel decomposition and establish that ADaPT dynamically adjusts to the capabilities of the executor LLM as well as to task complexity.

**Flag:** RELATED — the "split only on failed attempt" trigger and runtime-emergent recursion depth are exactly two of the Subject's axes.

---

## 3. Decomposed Prompting (DecomP)
**Review status:** reviewed -> sheet `16` (round 4). Cross-paper discussion: done - F25, F29, F30, F31, F32; reinforces F5, F14, F18, F20.


**Cite:** Tushar Khot, Harsh Trivedi, Matthew Finlayson, Yao Fu, Kyle Richardson, Peter Clark, Ashish Sabharwal. "Decomposed Prompting: A Modular Approach for Solving Complex Tasks." 2023. International Conference on Learning Representations (ICLR 2023). arXiv:2210.02406. https://openreview.net/forum?id=_nGgzQjzaRy

**Flag:** RELATED (2023 anchor) — canonical statement of modular decomposition into a library of sub-task prompts, with recursion on hard sub-tasks and on input length; later work repeatedly builds on it.

**Abstract (verbatim, arXiv):**
> Few-shot prompting is a surprisingly powerful way to use Large Language Models (LLMs) to solve various tasks. However, this approach struggles as the task complexity increases or when the individual reasoning steps of the task themselves are hard to learn, especially when embedded in more complex tasks. To address this, we propose Decomposed Prompting, a new approach to solve complex tasks by decomposing them (via prompting) into simpler sub-tasks that can be delegated to a library of prompting-based LLMs dedicated to these sub-tasks. This modular structure allows each prompt to be optimized for its specific sub-task, further decomposed if necessary, and even easily replaced with more effective prompts, trained models, or symbolic functions if desired. We show that the flexibility and modularity of Decomposed Prompting allows it to outperform prior work on few-shot prompting using GPT3. On symbolic reasoning tasks, we can further decompose sub-tasks that are hard for LLMs into even simpler solvable sub-tasks. When the complexity comes from the input length, we can recursively decompose the task into the same task but with smaller inputs. We also evaluate our approach on textual multi-step reasoning tasks: on long-context multi-hop QA task, we can more effectively teach the sub-tasks via our separate sub-tasks prompts; and on open-domain multi-hop QA, we can incorporate a symbolic information retrieval within our decomposition framework, leading to improved performance on both tasks. Datasets, Code and Prompts available at https://github.com/allenai/DecomP.

---

## 4. Least-to-Most Prompting

**Cite:** Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang, Dale Schuurmans, Claire Cui, Olivier Bousquet, Quoc Le, Ed Chi. "Least-to-Most Prompting Enables Complex Reasoning in Large Language Models." 2023. International Conference on Learning Representations (ICLR 2023). arXiv:2205.10625. https://openreview.net/forum?id=WZH7099tgfM

**Flag:** RELATED (2023 anchor) — foundational "decompose-then-solve-subproblems-sequentially" prompting scheme; depth is a fixed upfront list; heavily cited by later decomposition work.


**Abstract (verbatim, arXiv):**
> Chain-of-thought prompting has demonstrated remarkable performance on various natural language reasoning tasks. However, it tends to perform poorly on tasks which requires solving problems harder than the exemplars shown in the prompts. To overcome this challenge of easy-to-hard generalization, we propose a novel prompting strategy, least-to-most prompting. The key idea in this strategy is to break down a complex problem into a series of simpler subproblems and then solve them in sequence. Solving each subproblem is facilitated by the answers to previously solved subproblems. Our experimental results on tasks related to symbolic manipulation, compositional generalization, and math reasoning reveal that least-to-most prompting is capable of generalizing to more difficult problems than those seen in the prompts. A notable finding is that when the GPT-3 code-davinci-002 model is used with least-to-most prompting, it can solve the compositional generalization benchmark SCAN in any split (including length split) with an accuracy of at least 99% using just 14 exemplars, compared to only 16% accuracy with chain-of-thought prompting. This is particularly noteworthy because neural-symbolic models in the literature that specialize in solving SCAN are trained on the entire training set containing over 15,000 examples. We have included prompts for all the tasks in the Appendix.

---

## 5. Plan-and-Solve Prompting

**Cite:** Lei Wang, Wanyu Xu, Yihuai Lan, Zhiqiang Hu, Yunshi Lan, Roy Ka-Wei Lee, Ee-Peng Lim. "Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models." 2023. Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (ACL 2023), long papers. arXiv:2305.04091. https://aclanthology.org/2023.acl-long.147/

**Flag:** RELATED (2023 anchor) — zero-shot "devise a plan that divides the task into subtasks, then execute"; the minimal upfront-plan form of decomposition.


**Abstract (verbatim, arXiv):**
> Large language models (LLMs) have recently been shown to deliver impressive performance in various NLP tasks. To tackle multi-step reasoning tasks, few-shot chain-of-thought (CoT) prompting includes a few manually crafted step-by-step reasoning demonstrations which enable LLMs to explicitly generate reasoning steps and improve their reasoning task accuracy. To eliminate the manual effort, Zero-shot-CoT concatenates the target problem statement with "Let's think step by step" as an input prompt to LLMs. Despite the success of Zero-shot-CoT, it still suffers from three pitfalls: calculation errors, missing-step errors, and semantic misunderstanding errors. To address the missing-step errors, we propose Plan-and-Solve (PS) Prompting. It consists of two components: first, devising a plan to divide the entire task into smaller subtasks, and then carrying out the subtasks according to the plan. To address the calculation errors and improve the quality of generated reasoning steps, we extend PS prompting with more detailed instructions and derive PS+ prompting. We evaluate our proposed prompting strategy on ten datasets across three reasoning problems. The experimental results over GPT-3 show that our proposed zero-shot prompting consistently outperforms Zero-shot-CoT across all datasets by a large margin, is comparable to or exceeds Zero-shot-Program-of-Thought Prompting, and has comparable performance with 8-shot CoT prompting on the math reasoning problem. The code can be found at https://github.com/AGI-Edgerunners/Plan-and-Solve-Prompting.

---

## 6. Tree of Thoughts (ToT)

**Cite:** Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, Karthik Narasimhan. "Tree of Thoughts: Deliberate Problem Solving with Large Language Models." 2023. Advances in Neural Information Processing Systems 36 (NeurIPS 2023). arXiv:2305.10601. https://papers.nips.cc/paper_files/paper/2023/hash/271db9922b8d1f4dd7aaef84ed5ac703-Abstract-Conference.html

**Flag:** ADJACENT — decomposes a problem into intermediate "thought" steps with search/backtracking, but the split is a reasoning-path exploration structure rather than sub-objectives executed and recombined.


**Abstract (verbatim, arXiv):**
> Language models are increasingly being deployed for general problem solving across a wide range of tasks, but are still confined to token-level, left-to-right decision-making processes during inference. This means they can fall short in tasks that require exploration, strategic lookahead, or where initial decisions play a pivotal role. To surmount these challenges, we introduce a new framework for language model inference, Tree of Thoughts (ToT), which generalizes over the popular Chain of Thought approach to prompting language models, and enables exploration over coherent units of text (thoughts) that serve as intermediate steps toward problem solving. ToT allows LMs to perform deliberate decision making by considering multiple different reasoning paths and self-evaluating choices to decide the next course of action, as well as looking ahead or backtracking when necessary to make global choices. Our experiments show that ToT significantly enhances language models' problem-solving abilities on three novel tasks requiring non-trivial planning or search: Game of 24, Creative Writing, and Mini Crosswords. For instance, in Game of 24, while GPT-4 with chain-of-thought prompting only solved 4% of tasks, our method achieved a success rate of 74%. Code repo with all prompts: https://github.com/princeton-nlp/tree-of-thought-llm.

---

## 7. Graph of Thoughts (GoT)

**Cite:** Maciej Besta, Nils Blach, Ales Kubicek, Robert Gerstenberger, Michal Podstawski, Lukas Gianinazzi, Joanna Gajda, Tomasz Lehmann, Hubert Niewiadomski, Piotr Nyczyk, Torsten Hoefler. "Graph of Thoughts: Solving Elaborate Problems with Large Language Models." 2024. Proceedings of the AAAI Conference on Artificial Intelligence, 38(16):17682-17690. DOI: 10.1609/aaai.v38i16.29720. arXiv:2308.09687. https://ojs.aaai.org/index.php/AAAI/article/view/29720

**Flag:** ADJACENT — models thoughts as an arbitrary graph with aggregation/refinement nodes; touches recombination and cost but frames it as reasoning topology, not task-into-subtask delegation.


**Abstract (verbatim, arXiv):**
> We introduce Graph of Thoughts (GoT): a framework that advances prompting capabilities in large language models (LLMs) beyond those offered by paradigms such as Chain-of-Thought or Tree of Thoughts (ToT). The key idea and primary advantage of GoT is the ability to model the information generated by an LLM as an arbitrary graph, where units of information ("LLM thoughts") are vertices, and edges correspond to dependencies between these vertices. This approach enables combining arbitrary LLM thoughts into synergistic outcomes, distilling the essence of whole networks of thoughts, or enhancing thoughts using feedback loops. We illustrate that GoT offers advantages over state of the art on different tasks, for example increasing the quality of sorting by 62% over ToT, while simultaneously reducing costs by &gt;31%. We ensure that GoT is extensible with new thought transformations and thus can be used to spearhead new prompting schemes. This work brings the LLM reasoning closer to human thinking or brain mechanisms such as recurrence, both of which form complex networks.

---

## 8. HuggingGPT

**Cite:** Yongliang Shen, Kaitao Song, Xu Tan, Dongsheng Li, Weiming Lu, Yueting Zhuang. "HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face." 2023. Advances in Neural Information Processing Systems 36 (NeurIPS 2023). arXiv:2303.17580. https://papers.nips.cc/paper_files/paper/2023/hash/77c33e6a367922d003ff102ffb92b658-Abstract-Conference.html

**Flag:** RELATED — explicit LLM task-planning stage parses a request into a dependency-ordered task list dispatched to expert models, then recombines results; a fixed multi-stage pipeline instance.


**Abstract (verbatim, arXiv):**
> Solving complicated AI tasks with different domains and modalities is a key step toward artificial general intelligence. While there are numerous AI models available for various domains and modalities, they cannot handle complicated AI tasks autonomously. Considering large language models (LLMs) have exhibited exceptional abilities in language understanding, generation, interaction, and reasoning, we advocate that LLMs could act as a controller to manage existing AI models to solve complicated AI tasks, with language serving as a generic interface to empower this. Based on this philosophy, we present HuggingGPT, an LLM-powered agent that leverages LLMs (e.g., ChatGPT) to connect various AI models in machine learning communities (e.g., Hugging Face) to solve AI tasks. Specifically, we use ChatGPT to conduct task planning when receiving a user request, select models according to their function descriptions available in Hugging Face, execute each subtask with the selected AI model, and summarize the response according to the execution results. By leveraging the strong language capability of ChatGPT and abundant AI models in Hugging Face, HuggingGPT can tackle a wide range of sophisticated AI tasks spanning different modalities and domains and achieve impressive results in language, vision, speech, and other challenging tasks, which paves a new way towards the realization of artificial general intelligence.

---

## 9. Divide-or-Conquer? Which Part Should You Distill Your LLM?
**Review status:** reviewed -> sheet `10` (round 3). Cross-paper discussion: done - F18, F19, F21, F23.


**Cite:** Zhuofeng Wu, He Bai, Aonan Zhang, Jiatao Gu, VG Vinod Vydiswaran, Navdeep Jaitly, Yizhe Zhang. "Divide-or-Conquer? Which Part Should You Distill Your LLM?" 2024. Findings of the Association for Computational Linguistics: EMNLP 2024. DOI: 10.18653/v1/2024.findings-emnlp.145. arXiv:2402.15000. https://aclanthology.org/2024.findings-emnlp.145/


**Abstract (verbatim, arXiv):**
> Recent methods have demonstrated that Large Language Models (LLMs) can solve reasoning tasks better when they are encouraged to solve subtasks of the main task first. In this paper we devise a similar strategy that breaks down reasoning tasks into a problem decomposition phase and a problem solving phase and show that the strategy is able to outperform a single stage solution. Further, we hypothesize that the decomposition should be easier to distill into a smaller model compared to the problem solving because the latter requires large amounts of domain knowledge while the former only requires learning general problem solving strategies. We propose methods to distill these two capabilities and evaluate their impact on reasoning outcomes and inference cost. We find that we can distill the problem decomposition phase and at the same time achieve good generalization across tasks, datasets, and models. However, it is harder to distill the problem solving capability without losing performance and the resulting distilled model struggles with generalization. These results indicate that by using smaller, distilled problem decomposition models in combination with problem solving LLMs we can achieve reasoning with cost-efficient inference and local adaptation.

---

## 10. Chain of Agents
**Review status:** reviewed -> sheet `11` (round 3). Cross-paper discussion: done - F13, F16, F20, F22.


**Cite:** Yusen Zhang, Ruoxi Sun, Yanfei Chen, Tomas Pfister, Rui Zhang, Sercan Ö. Arık. "Chain of Agents: Large Language Models Collaborating on Long-Context Tasks." 2024. Advances in Neural Information Processing Systems 37 (NeurIPS 2024). arXiv:2406.02818. https://openreview.net/forum?id=LuCLf4BJsr


**Abstract (verbatim, arXiv):**
> Addressing the challenge of effectively processing long contexts has become a critical issue for Large Language Models (LLMs). Two common strategies have emerged: 1) reducing the input length, such as retrieving relevant chunks by Retrieval-Augmented Generation (RAG), and 2) expanding the context window limit of LLMs. However, both strategies have drawbacks: input reduction has no guarantee of covering the part with needed information, while window extension struggles with focusing on the pertinent information for solving the task. To mitigate these limitations, we propose Chain-of-Agents (CoA), a novel framework that harnesses multi-agent collaboration through natural language to enable information aggregation and context reasoning across various LLMs over long-context tasks. CoA consists of multiple worker agents who sequentially communicate to handle different segmented portions of the text, followed by a manager agent who synthesizes these contributions into a coherent final output. CoA processes the entire input by interleaving reading and reasoning, and it mitigates long context focus issues by assigning each agent a short context. We perform comprehensive evaluation of CoA on a wide range of long-context tasks in question answering, summarization, and code completion, demonstrating significant improvements by up to 10% over strong baselines of RAG, Full-Context, and multi-agent LLMs.

---

## 11. Measuring and Narrowing the Compositionality Gap (self-ask)
**Review status:** reviewed -> sheet `09` (round 3). Cross-paper discussion: done - F13, F14, F15.


**Cite:** Ofir Press, Muru Zhang, Sewon Min, Ludwig Schmidt, Noah A. Smith, Mike Lewis. "Measuring and Narrowing the Compositionality Gap in Language Models." 2023. Findings of the Association for Computational Linguistics: EMNLP 2023. DOI: 10.18653/v1/2023.findings-emnlp.378. arXiv:2210.03350. https://aclanthology.org/2023.findings-emnlp.378/


**Abstract (verbatim, arXiv):**
> We investigate the ability of language models to perform compositional reasoning tasks where the overall solution depends on correctly composing the answers to sub-problems. We measure how often models can correctly answer all sub-problems but not generate the overall solution, a ratio we call the compositionality gap. We evaluate this ratio by asking multi-hop questions with answers that require composing multiple facts unlikely to have been observed together during pretraining. In the GPT-3 family of models, as model size increases we show that the single-hop question answering performance improves faster than the multi-hop performance does, therefore the compositionality gap does not decrease. This surprising result suggests that while more powerful models memorize and recall more factual knowledge, they show no corresponding improvement in their ability to perform this kind of compositional reasoning. We then demonstrate how elicitive prompting (such as chain of thought) narrows the compositionality gap by reasoning explicitly. We present a new method, self-ask, that further improves on chain of thought. In our method, the model explicitly asks itself (and answers) follow-up questions before answering the initial question. We finally show that self-ask's structured prompting lets us easily plug in a search engine to answer the follow-up questions, which additionally improves accuracy.

---

## 12. LLMCompiler

**Cite:** Sehoon Kim, Suhong Moon, Ryan Tabrizi, Nicholas Lee, Michael W. Mahoney, Kurt Keutzer, Amir Gholami. "An LLM Compiler for Parallel Function Calling." 2024. Proceedings of the 41st International Conference on Machine Learning (ICML 2024). arXiv:2312.04511. https://proceedings.mlr.press/v235/kim24y.html


**Abstract (verbatim, arXiv):**
> The reasoning capabilities of the recent LLMs enable them to execute external function calls to overcome their inherent limitations, such as knowledge cutoffs, poor arithmetic skills, or lack of access to private data. This development has allowed LLMs to select and coordinate multiple functions based on the context to tackle more complex problems. However, current methods for function calling often require sequential reasoning and acting for each function which can result in high latency, cost, and sometimes inaccurate behavior. To address this, we introduce LLMCompiler, which executes functions in parallel to efficiently orchestrate multiple function calls. Drawing inspiration from the principles of classical compilers, LLMCompiler enables parallel function calling with three components: (i) a Function Calling Planner, formulating execution plans for function calling; (ii) a Task Fetching Unit, dispatching function calling tasks; and (iii) an Executor, executing these tasks in parallel. LLMCompiler automatically generates an optimized orchestration for the function calls and can be used with both open-source and closed-source models. We have benchmarked LLMCompiler on a range of tasks with different patterns of function calling. We observe consistent latency speedup of up to 3.7x, cost savings of up to 6.7x, and accuracy improvement of up to ~9% compared to ReAct. Our code is available at https://github.com/SqueezeAILab/LLMCompiler.

---

## 13. DELTA

**Cite:** Yan Liu, Yaoxian Song, Xiaofeng Gao, Kai Xu, et al. "DELTA: Decomposed Efficient Long-Term Robot Task Planning using Large Language Models." 2025. IEEE International Conference on Robotics and Automation (ICRA 2025). arXiv:2404.03275. https://ieeexplore.ieee.org/document/11127838


**Abstract (verbatim, arXiv):**
> Recent advancements in Large Language Models (LLMs) have sparked a revolution across many research fields. In robotics, the integration of common-sense knowledge from LLMs into task and motion planning has drastically advanced the field by unlocking unprecedented levels of context awareness. Despite their vast collection of knowledge, large language models may generate infeasible plans due to hallucinations or missing domain information. To address these challenges and improve plan feasibility and computational efficiency, we introduce DELTA, a novel LLM-informed task planning approach. By using scene graphs as environment representations within LLMs, DELTA achieves rapid generation of precise planning problem descriptions. To enhance planning performance, DELTA decomposes long-term task goals with LLMs into an autoregressive sequence of sub-goals, enabling automated task planners to efficiently solve complex problems. In our extensive evaluation, we show that DELTA enables an efficient and fully automatic task planning pipeline, achieving higher planning success rates and significantly shorter planning times compared to the state of the art. Project webpage: https://delta-llm.github.io/

---

## 14. Self-Planning Code Generation

**Cite:** Xue Jiang, Yihong Dong, Lecheng Wang, Zheng Fang, Qiwei Shang, Ge Li, Zhi Jin, Wenpin Jiao. "Self-Planning Code Generation with Large Language Models." 2024. ACM Transactions on Software Engineering and Methodology (TOSEM), 33(7):182. DOI: 10.1145/3672456. arXiv:2303.06689. https://dl.acm.org/doi/10.1145/3672456


**Abstract (verbatim, arXiv):**
> Although large language models (LLMs) have demonstrated impressive ability in code generation, they are still struggling to address the complicated intent provided by humans. It is widely acknowledged that humans typically employ planning to decompose complex problems and schedule solution steps prior to implementation. To this end, we introduce planning into code generation to help the model understand complex intent and reduce the difficulty of problem-solving. This paper proposes a self-planning code generation approach with large language models, which consists of two phases, namely planning phase and implementation phase. Specifically, in the planning phase, LLM outlines concise and formatted planning steps from the intent. Subsequently, in the implementation phase, the model generates code step by step, guided by the preceding planning steps. We conduct extensive experiments on various code-generation benchmarks across multiple programming languages. Experimental results show that self-planning code generation achieves a relative improvement of up to 25.4% in Pass@1 compared to direct code generation, and up to 11.9% compared to Chain-of-Thought code generation. Moreover, our self-planning approach also enhances the quality of the generated code with respect to correctness, readability, and robustness, as assessed by humans.

---

## 15. TaskBench
**Review status:** reviewed -> sheet `15` (round 4). Cross-paper discussion: done - F26; reinforces F16, F23.


**Cite:** Yongliang Shen, Kaitao Song, Xu Tan, Wenqi Zhang, Kan Ren, Siyu Yuan, Weiming Lu, Dongsheng Li, Yueting Zhuang. "TaskBench: Benchmarking Large Language Models for Task Automation." 2024. Advances in Neural Information Processing Systems 37 (NeurIPS 2024), Datasets and Benchmarks Track. arXiv:2311.18760. https://proceedings.neurips.cc/paper_files/paper/2024/hash/085185ea97db31ae6dcac7497616fd3e-Abstract-Datasets_and_Benchmarks_Track.html


**Abstract (verbatim, arXiv):**
> In recent years, the remarkable progress of large language models (LLMs) has sparked interest in task automation, which involves decomposing complex tasks described by user instructions into sub-tasks and invoking external tools to execute them, playing a central role in autonomous agents. However, there is a lack of systematic and standardized benchmarks to promote the development of LLMs in task automation. To address this, we introduce TaskBench, a comprehensive framework to evaluate the capability of LLMs in task automation. Specifically, task automation can be divided into three critical stages: task decomposition, tool selection, and parameter prediction. To tackle the complexities inherent in these stages, we introduce the concept of Tool Graph to represent decomposed tasks and adopt a back-instruct method to generate high-quality user instructions. We propose TaskEval, a multi-faceted evaluation methodology that assesses LLM performance across these three stages. Our approach combines automated construction with rigorous human verification, ensuring high consistency with human evaluation. Experimental results demonstrate that TaskBench effectively reflects the capabilities of various LLMs in task automation. It provides insights into model performance across different task complexities and domains, pushing the boundaries of what current models can achieve. TaskBench offers a scalable, adaptable, and reliable benchmark for advancing LLM-based autonomous agents.

---

## 16. TPTU-v2

**Cite:** Yilun Kong, Jingqing Ruan, Yihong Chen, Bin Zhang, Tianpeng Bao, Shiwei Shi, Guoqing Du, Xiaoru Hu, Hangyu Mao, Ziyue Li, Xingyu Zeng, Rui Zhao, Xueqian Wang. "TPTU-v2: Boosting Task Planning and Tool Usage of Large Language Model-based Agents in Real-world Systems." 2024. Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: Industry Track (EMNLP 2024). DOI: 10.18653/v1/2024.emnlp-industry.27. arXiv:2311.11315. https://aclanthology.org/2024.emnlp-industry.27/


**Abstract (verbatim, arXiv):**
> Large Language Models (LLMs) have demonstrated proficiency in addressing tasks that necessitate a combination of task planning and the usage of external tools that require a blend of task planning and the utilization of external tools, such as APIs. However, real-world complex systems present three prevalent challenges concerning task planning and tool usage: (1) The real system usually has a vast array of APIs, so it is impossible to feed the descriptions of all APIs to the prompt of LLMs as the token length is limited; (2) the real system is designed for handling complex tasks, and the base LLMs can hardly plan a correct sub-task order and API-calling order for such tasks; (3) Similar semantics and functionalities among APIs in real systems create challenges for both LLMs and even humans in distinguishing between them. In response, this paper introduces a comprehensive framework aimed at enhancing the Task Planning and Tool Usage (TPTU) abilities of LLM-based agents operating within real-world systems. Our framework comprises three key components designed to address these challenges: (1) the API Retriever selects the most pertinent APIs for the user task among the extensive array available; (2) LLM Finetuner tunes a base LLM so that the finetuned LLM can be more capable for task planning and API calling; (3) the Demo Selector adaptively retrieves different demonstrations related to hard-to-distinguish APIs, which is further used for in-context learning to boost the final performance. We validate our methods using a real-world commercial system as well as an open-sourced academic dataset, and the outcomes clearly showcase the efficacy of each individual component as well as the integrated framework.

---

## 17. To CoT or not to CoT?
**Review status:** reviewed -> sheet `01` (round 1). Cross-paper discussion: done - F14, F16, F18.


**Cite:** Zayne Sprague, Fangcong Yin, Juan Diego Rodriguez, Dongwei Jiang, Manya Wadhwa, Prasann Singhal, Xinyu Zhao, Xi Ye, Kyle Mahowald, Greg Durrett. "To CoT or not to CoT? Chain-of-thought helps mainly on math and symbolic reasoning." 2025. International Conference on Learning Representations (ICLR 2025). arXiv:2409.12183. https://openreview.net/forum?id=w6nlcS8Kkn


**Abstract (verbatim, arXiv):**
> Chain-of-thought (CoT) via prompting is the de facto method for eliciting reasoning capabilities from large language models (LLMs). But for what kinds of tasks is this extra ``thinking'' really helpful? To analyze this, we conducted a quantitative meta-analysis covering over 100 papers using CoT and ran our own evaluations of 20 datasets across 14 models. Our results show that CoT gives strong performance benefits primarily on tasks involving math or logic, with much smaller gains on other types of tasks. On MMLU, directly generating the answer without CoT leads to almost identical accuracy as CoT unless the question or model's response contains an equals sign, indicating symbolic operations and reasoning. Following this finding, we analyze the behavior of CoT on these problems by separating planning and execution and comparing against tool-augmented LLMs. Much of CoT's gain comes from improving symbolic execution, but it underperforms relative to using a symbolic solver. Our results indicate that CoT can be applied selectively, maintaining performance while saving inference costs. Furthermore, they suggest a need to move beyond prompt-based CoT to new paradigms that better leverage intermediate computation across the whole range of LLM applications.

---

## 18. Parsel

**Cite:** Eric Zelikman, Qingxuan Huang, Gabriel Poesia, Noah D. Goodman, Nick Haber. "Parsel: Algorithmic Reasoning with Language Models by Composing Decompositions." 2023. Advances in Neural Information Processing Systems 36 (NeurIPS 2023), spotlight. arXiv:2212.10561. https://proceedings.neurips.cc/paper_files/paper/2023/hash/6445dd88ebb9a6a3afa0b126ad87fe41-Abstract-Conference.html


**Abstract (verbatim, arXiv):**
> Despite recent success in large language model (LLM) reasoning, LLMs struggle with hierarchical multi-step reasoning tasks like generating complex programs. For these tasks, humans often start with a high-level algorithmic design and implement each part gradually. We introduce Parsel, a framework enabling automatic implementation and validation of complex algorithms with code LLMs. With Parsel, we automatically decompose algorithmic tasks into hierarchical natural language function descriptions and then search over combinations of possible function implementations using tests. We show that Parsel can be used across domains requiring hierarchical reasoning, including program synthesis and robotic planning. We find that, using Parsel, LLMs solve more competition-level problems in the APPS dataset, resulting in pass rates over 75\% higher than prior results from directly sampling AlphaCode and Codex, while often using a smaller sample budget. Moreover, with automatically generated tests, we find that Parsel can improve the state-of-the-art pass@1 performance on HumanEval from 67\% to 85\%. We also find that LLM-generated robotic plans using Parsel are more than twice as likely to be considered accurate than directly generated plans. Lastly, we explore how Parsel addresses LLM limitations and discuss how Parsel may be useful for human programmers. We release our code at https://github.com/ezelikman/parsel

---

## 19. Why Do Multi-Agent LLM Systems Fail?
**Review status:** reviewed -> sheet `12` (round 3). Cross-paper discussion: done - F13, F15, F17, F20, F22, F23.


**Cite:** Mert Cemri, Melissa Z. Pan, Shuyi Yang, Lakshya A. Agrawal, Bhavya Chopra, Rishabh Tiwari, Kurt Keutzer, Aditya Parameswaran, Dan Klein, Kannan Ramchandran, Matei Zaharia, Joseph E. Gonzalez, Ion Stoica. "Why Do Multi-Agent LLM Systems Fail?" 2025. Advances in Neural Information Processing Systems 38 (NeurIPS 2025). arXiv:2503.13657. https://neurips.cc/virtual/2025/poster/121528


**Abstract (verbatim, arXiv):**
> Despite enthusiasm for Multi-Agent LLM Systems (MAS), their performance gains on popular benchmarks are often minimal. This gap highlights a critical need for a principled understanding of why MAS fail. Addressing this question requires systematic identification and analysis of failure patterns. We introduce MAST-Data, a comprehensive dataset of 1600+ annotated traces collected across 7 popular MAS frameworks. MAST-Data is the first multi-agent system dataset to outline the failure dynamics in MAS for guiding the development of better future systems. To enable systematic classification of failures for MAST-Data, we build the first Multi-Agent System Failure Taxonomy (MAST). We develop MAST through rigorous analysis of 150 traces, guided closely by expert human annotators and validated by high inter-annotator agreement (kappa = 0.88). This process identifies 14 unique modes, clustered into 3 categories: (i) system design issues, (ii) inter-agent misalignment, and (iii) task verification. To enable scalable annotation, we develop an LLM-as-a-Judge pipeline with high agreement with human annotations. We leverage MAST and MAST-Data to analyze failure patterns across models (GPT4, Claude 3, Qwen2.5, CodeLlama) and tasks (coding, math, general agent), demonstrating improvement headrooms from better MAS design. Our analysis provides insights revealing that identified failures require more sophisticated solutions, highlighting a clear roadmap for future research. We publicly release our comprehensive dataset (MAST-Data), the MAST, and our LLM annotator to facilitate widespread research and development in MAS.

---

## 20. A Survey of Task Planning with Large Language Models

**Cite:** Wenshuo Zhai, Jinzhi Liao, Ziyang Chen, Bolun Su, Xiang Zhao. "A Survey of Task Planning with Large Language Models." 2025. Intelligent Computing (Science Partner Journal / AAAS), Vol. 4, Article 0124. DOI: 10.34133/icomputing.0124. https://spj.science.org/doi/10.34133/icomputing.0124


**Abstract (verbatim, Crossref/publisher):**
> This paper presents a comprehensive survey of the current status and opportunities for large language models (LLMs) in task planning, a sophisticated process of reasoning and decision-making that organizes a sequence of actions to accomplish predefined goals. Task planning centers on identifying suitable solutions for a task, with a specific emphasis on ensuring its successful completion. Although task planning plays a crucial role in enabling systems to function effectively in dynamic and complex environments, there is a lack of systematic reviews on this topic. We explore the theories, methodologies, and applications related to task planning with LLMs, highlighting the burgeoning development in this field and the interdisciplinary approaches that enhance their ability to complete tasks. This survey aims to systematize and clarify the fragmented literature, provide a systematic review that underscores the importance of task planning as a critical capability, and offer insights into future research directions and potential improvements. We hope to help researchers gain a clear understanding of the field and spark greater interest in this highly impactful research direction. A continuously updated resource is available in our GitHub repository at https://github.com/ZhaiWenShuo/Survey-of-Task-Planning .

---

## 21. MapCoder

**Cite:** Md. Ashraful Islam, Mohammed Eunus Ali, Md Rizwan Parvez. "MapCoder: Multi-Agent Code Generation for Competitive Problem Solving." 2024. Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (ACL 2024), long papers. DOI: 10.18653/v1/2024.acl-long.269. arXiv:2405.11403. https://aclanthology.org/2024.acl-long.269/

**Abstract (verbatim, arXiv):**
> Code synthesis, which requires a deep understanding of complex natural language problem descriptions, generation of code instructions for complex algorithms and data structures, and the successful execution of comprehensive unit tests, presents a significant challenge. While large language models (LLMs) demonstrate impressive proficiency in natural language processing, their performance in code generation tasks remains limited. In this paper, we introduce a new approach to code generation tasks leveraging multi-agent prompting that uniquely replicates the full cycle of program synthesis as observed in human developers. Our framework, MapCoder, consists of four LLM agents specifically designed to emulate the stages of this cycle: recalling relevant examples, planning, code generation, and debugging. After conducting thorough experiments, with multiple LLM ablations and analyses across eight challenging competitive problem-solving and program synthesis benchmarks, MapCoder showcases remarkable code generation capabilities, achieving new state-of-the-art results (pass@1) on HumanEval (93.9%), MBPP (83.1%), APPS (22.0%), CodeContests (28.5%), and xCodeEval (45.3%). Moreover, our method consistently delivers superior performance across various programming languages and varying problem difficulties. We open-source our framework at https://github.com/Md-Ashraful-Pramanik/MapCoder.

---

## 22. Successive Prompting

**Cite:** Dheeru Dua, Shivanshu Gupta, Sameer Singh, Matt Gardner. "Successive Prompting for Decomposing Complex Questions." 2022. Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing (EMNLP 2022). DOI: 10.18653/v1/2022.emnlp-main.81. arXiv:2212.04092. https://aclanthology.org/2022.emnlp-main.81/

**Abstract (verbatim, arXiv):**
> Answering complex questions that require making latent decisions is a challenging task, especially when limited supervision is available. Recent works leverage the capabilities of large language models (LMs) to perform complex question answering in a few-shot setting by demonstrating how to output intermediate rationalizations while solving the complex question in a single pass. We introduce ``Successive Prompting'', where we iteratively break down a complex task into a simple task, solve it, and then repeat the process until we get the final solution. Successive prompting decouples the supervision for decomposing complex questions from the supervision for answering simple questions, allowing us to (1) have multiple opportunities to query in-context examples at each reasoning step (2) learn question decomposition separately from question answering, including using synthetic data, and (3) use bespoke (fine-tuned) components for reasoning steps where a large LM does not perform well. The intermediate supervision is typically manually written, which can be expensive to collect. We introduce a way to generate a synthetic dataset which can be used to bootstrap a model's ability to decompose and answer intermediate questions. Our best model (with successive prompting) achieves an improvement of ~5% absolute F1 on a few-shot version of the DROP dataset when compared with a state-of-the-art model with the same supervision.

**Flag:** ANCHOR (pre-2023) — iterative "break off one simple sub-question, answer it, repeat"; separates decomposition supervision from answering; later decomposition-prompting work builds on it.

---

## 23. Self-Discover

**Cite:** Pei Zhou, Jay Pujara, Xiang Ren, Xinyun Chen, Heng-Tze Cheng, Quoc V. Le, Ed H. Chi, Denny Zhou, Swaroop Mishra, Huaixiu Steven Zheng. "Self-Discover: Large Language Models Self-Compose Reasoning Structures." 2024. Advances in Neural Information Processing Systems 37 (NeurIPS 2024). arXiv:2402.03620. https://proceedings.neurips.cc/paper_files/paper/2024/hash/e41efb03e20ca3c231940a3c6917ef6f-Abstract-Conference.html

**Abstract (verbatim, arXiv):**
> We introduce SELF-DISCOVER, a general framework for LLMs to self-discover the task-intrinsic reasoning structures to tackle complex reasoning problems that are challenging for typical prompting methods. Core to the framework is a self-discovery process where LLMs select multiple atomic reasoning modules such as critical thinking and step-by-step thinking, and compose them into an explicit reasoning structure for LLMs to follow during decoding. SELF-DISCOVER substantially improves GPT-4 and PaLM 2's performance on challenging reasoning benchmarks such as BigBench-Hard, grounded agent reasoning, and MATH, by as much as 32% compared to Chain of Thought (CoT). Furthermore, SELF-DISCOVER outperforms inference-intensive methods such as CoT-Self-Consistency by more than 20%, while requiring 10-40x fewer inference compute. Finally, we show that the self-discovered reasoning structures are universally applicable across model families: from PaLM 2-L to GPT-4, and from GPT-4 to Llama2, and share commonalities with human reasoning patterns.

---

## 24. RAP (Reasoning with Language Model is Planning with World Model)

**Cite:** Shibo Hao, Yi Gu, Haodi Ma, Joshua Jiahua Hong, Zhen Wang, Daisy Zhe Wang, Zhiting Hu. "Reasoning with Language Model is Planning with World Model." 2023. Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP 2023). DOI: 10.18653/v1/2023.emnlp-main.507. arXiv:2305.14992. https://aclanthology.org/2023.emnlp-main.507/

**Abstract (verbatim, arXiv):**
> Large language models (LLMs) have shown remarkable reasoning capabilities, especially when prompted to generate intermediate reasoning steps (e.g., Chain-of-Thought, CoT). However, LLMs can still struggle with problems that are easy for humans, such as generating action plans for executing tasks in a given environment, or performing complex math, logical, and commonsense reasoning. The deficiency stems from the key fact that LLMs lack an internal $\textit{world model}$ to predict the world $\textit{state}$ (e.g., environment status, intermediate variable values) and simulate long-term outcomes of actions. This prevents LLMs from performing deliberate planning akin to human brains, which involves exploring alternative reasoning paths, anticipating future states and rewards, and iteratively refining existing reasoning steps. To overcome the limitations, we propose a new LLM reasoning framework, $\underline{R}$easoning vi$\underline{a}$ $\underline{P}$lanning $\textbf{(RAP)}$. RAP repurposes the LLM as both a world model and a reasoning agent, and incorporates a principled planning algorithm (based on Monto Carlo Tree Search) for strategic exploration in the vast reasoning space. During reasoning, the LLM (as agent) incrementally builds a reasoning tree under the guidance of the LLM (as world model) and task-specific rewards, and obtains a high-reward reasoning path efficiently with a proper balance between exploration $\textit{vs.}$ exploitation. We apply RAP to a variety of challenging reasoning problems including plan generation, math reasoning, and logical inference. Empirical results on these tasks demonstrate the superiority of RAP over various strong baselines, including CoT and least-to-most prompting with self-consistency. RAP on LLAMA-33B surpasses CoT on GPT-4 with 33% relative improvement in a plan generation setting.

---

## 25. Compound AI Systems Optimization: A Survey

**Cite:** Yu-Ang Lee, Guan-Ting Yi, Mei-Yi Liu, Jui-Chao Lu, Guan-Bo Yang, Yun-Nung Chen. "Compound AI Systems Optimization: A Survey of Methods, Challenges, and Future Directions." 2025. Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing (EMNLP 2025), main track. DOI: 10.18653/v1/2025.emnlp-main.1463. arXiv:2506.08234. https://aclanthology.org/2025.emnlp-main.1463/

---

## 26. Problem Decomposition Guided by Reasoning Utility

**Cite:** Yaxin Guo, Hongye Tan, Ru Li, Xiaoli Li, Xinyi Sun, Pengpeng Qiang, Hu Zhang. "Problem decomposition guided by reasoning utility for complex reasoning in LLMs." 2026. Information Processing & Management, vol. 63, article 104509. DOI: 10.1016/j.ipm.2025.104509. https://doi.org/10.1016/j.ipm.2025.104509

**Abstract:** not machine-retrievable — Elsevier paywall (ScienceDirect 403; absent from Crossref and Semantic Scholar). Needs manual retrieval.

---

## 27. Enhancing Long-Form QA via Reflection with Question Decomposition

**Cite:** Junjie Xiao, Wei Wu, Jiaxu Zhao, Meng Fang, Jianxin Wang. "Enhancing long-form question answering via reflection with question decomposition." 2025. Information Processing & Management, vol. 62, no. 6, article 104274. DOI: 10.1016/j.ipm.2025.104274. https://doi.org/10.1016/j.ipm.2025.104274

**Abstract:** not machine-retrievable — Elsevier paywall (ScienceDirect 403; absent from Crossref and Semantic Scholar). Needs manual retrieval.

---

<!-- second gather round, 2026-09-06: widened to skeptic/boundary vocabulary (over-decomposition, CoT length, error compounding, aggregation depth). Preprints admitted for this slice, flagged. -->

## 28. Faith and Fate: Limits of Transformers on Compositionality
**Review status:** reviewed -> sheet `13` (round 4). Cross-paper discussion: done - F24, F25, F26, F29, F30; reinforces F16.


**Cite:** Nouha Dziri, Ximing Lu, Melanie Sclar, Xiang Lorraine Li, Liwei Jiang, Bill Yuchen Lin, Peter West, Chandra Bhagavatula, Ronan Le Bras, Jena D. Hwang, Soumya Sanyal, Xiang Ren, Allyson Ettinger, Zaid Harchaoui, Yejin Choi. "Faith and Fate: Limits of Transformers on Compositionality." 2023. Advances in Neural Information Processing Systems 36 (NeurIPS 2023). arXiv:2305.18654. https://proceedings.neurips.cc/paper_files/paper/2023/hash/deb3c28192f979302c157cb653c15e90-Abstract-Conference.html

**Abstract (verbatim, arXiv):**
> Transformer large language models (LLMs) have sparked admiration for their exceptional performance on tasks that demand intricate multi-step reasoning. Yet, these models simultaneously show failures on surprisingly trivial problems. This begs the question: Are these errors incidental, or do they signal more substantial limitations? In an attempt to demystify transformer LLMs, we investigate the limits of these models across three representative compositional tasks -- multi-digit multiplication, logic grid puzzles, and a classic dynamic programming problem. These tasks require breaking problems down into sub-steps and synthesizing these steps into a precise answer. We formulate compositional tasks as computation graphs to systematically quantify the level of complexity, and break down reasoning steps into intermediate sub-procedures. Our empirical findings suggest that transformer LLMs solve compositional tasks by reducing multi-step compositional reasoning into linearized subgraph matching, without necessarily developing systematic problem-solving skills. To round off our empirical study, we provide theoretical arguments on abstract multi-step reasoning problems that highlight how autoregressive generations' performance can rapidly decay with\,increased\,task\,complexity.

---

## 29. When More is Less: Understanding Chain-of-Thought Length in LLMs
**Review status:** reviewed -> sheet `08` (round 2). Cross-paper discussion: done - F1, F3, F4, F6, F9 (with `04`); qualifier F5.


**Cite:** Yuyang Wu, Yifei Wang, Ziyu Ye, Tianqi Du, Stefanie Jegelka, Yisen Wang. "When More is Less: Understanding Chain-of-Thought Length in LLMs." 2025. arXiv:2502.07266 (preprint; venue unconfirmed). https://arxiv.org/abs/2502.07266

**Status:** PREPRINT — not confirmed peer-reviewed. Admitted in the widened round as central to the depth/cost boundary.

**Abstract (verbatim, arXiv):**
> Large Language Models (LLMs) employ Chain-of-Thought (CoT) reasoning to deconstruct complex problems. While longer CoTs are often presumed superior, this paper challenges that notion, arguing that longer is not always better. Drawing on combined evidence from real-world observations, controlled experiments, and theoretical analysis, we demonstrate that task accuracy typically follows an inverted U-shaped curve with CoT length, where performance initially improves but eventually decreases as the number of CoT steps increases. With controlled experiments, we further uncover the scaling behaviors of the optimal CoT length: it increases with task difficulty but decreases with model capability, exposing an inherent simplicity bias where more capable models favor shorter, more efficient CoT reasoning. This bias is also evident in Reinforcement Learning (RL) training, where models gravitate towards shorter CoTs as their accuracy improves. To have a deep understanding of these dynamics, we establish a simple theoretical model that formally proves these phenomena, including the optimal length's scaling laws and the emergence of simplicity bias during RL. Guided by this framework, we demonstrate significant practical benefits from training with optimally-lengthed CoTs and employing length-aware filtering at inference. These findings offer both a principled understanding of the "overthinking" phenomenon and multiple practical guidelines for CoT calibration, enabling LLMs to achieve optimal reasoning performance with adaptive CoTs tailored to task complexity and model capability.

---

## 30. How does Chain of Thought decompose complex tasks?

**Cite:** "How does Chain of Thought decompose complex tasks?" 2026. arXiv:2604.08872 (preprint). https://arxiv.org/abs/2604.08872

**Status:** PREPRINT — not peer-reviewed. Admitted as the theoretical statement of the decompose-depth threshold.

**Abstract (verbatim, arXiv):**
> Many language tasks can be modeled as classification problems where a large language model (LLM) is given a prompt and selects one among many possible answers. We show that the classification error in such problems scales as a power law in the number of classes. This has a dramatic consequence: the prediction error can be reduced substantially by splitting the overall task into a sequence of smaller classification problems, each with the same number of classes ("degree"). This tree-structured decomposition models chain-of-thought (CoT). It has been observed that CoT-based predictors perform better when they "think", i.e., when they develop a deeper tree, thus decomposing the problem into a larger number of steps. We identify a critical threshold for the degree, below which thinking is detrimental, and above which there exists an optimal depth that minimizes the error. It is impossible to surpass this minimal error by increasing the depth of thinking.

---

## 31. ARIES: Autonomous Reasoning with LLMs on Interactive Thought Graph Environments

**Cite:** Pedro Gimenes, Zeyu Cao, Jeffrey Wang, Yiren Zhao. "ARIES: Autonomous Reasoning with LLMs on Interactive Thought Graph Environments." 2025. arXiv:2502.21208 (preprint; OpenReview submission, decision unconfirmed). https://arxiv.org/abs/2502.21208

**Status:** PREPRINT — decision unconfirmed. Central: its failure analysis is depth-of-decomposition vs aggregation error.

**Abstract (verbatim, arXiv):**
> Recent research has shown that LLM performance on reasoning tasks can be enhanced by scaling test-time compute. One promising approach, particularly with decomposable problems, involves arranging intermediate solutions as a graph on which transformations are performed to explore the solution space. However, prior works rely on pre-determined, task-specific transformation schedules which are subject to a set of searched hyperparameters. In this work, we view thought graph transformations as actions in a Markov decision process, and implement policy agents to drive effective action policies for the underlying reasoning LLM agent. In particular, we investigate the ability for another LLM to act as a policy agent on thought graph environments and introduce ARIES, a multi-agent architecture for reasoning with LLMs. In ARIES, reasoning LLM agents solve decomposed subproblems, while policy LLM agents maintain visibility of the thought graph states, and dynamically adapt the problem-solving strategy. Through extensive experiments, we observe that using off-the-shelf LLMs as policy agents with no supervised fine-tuning (SFT) can yield up to $29\%$ higher accuracy on HumanEval relative to static transformation schedules, as well as reducing inference costs by $35\%$ and avoid any search requirements. We also conduct a thorough analysis of observed failure modes, highlighting that limitations on LLM sizes and the depth of problem decomposition can be seen as challenges to scaling LLM-guided reasoning.

---

## 32. CARD: Complexity Agnostic Recursive Decomposition of Thoughts

**Cite:** "Complexity Agnostic Recursive Decomposition of Thoughts." 2025. arXiv:2601.04210 (preprint; 4 pages). https://arxiv.org/abs/2601.04210

**Status:** PREPRINT — not peer-reviewed, short paper. Admitted as pre-generation complexity estimation to set decomposition depth/budget.

**Abstract (verbatim, arXiv):**
> Large language models often fail on multi-step reasoning due to fixed reasoning strategies that ignore problem specific difficulty. We introduce CARD (Complexity Agnostic Recursive Decomposition), a framework that predicts problem complexity before generation and adapts decomposition accordingly. Our system comprises MRCE (Multi-dimensional Reasoning Complexity Estimator), a 0.6B Qwen model predicting 30 fine-grained features from question text and a two-stage recursive solver: (1) hierarchical decomposition into K steps based on task profile and (2) per-step thought budget allocation (1, 5-9, or 10 thoughts) via recursive MRCE profiling. Evaluated on three reasoning models (Qwen3-0.6B, DeepSeek-R1-Distill-Qwen-1.5B, Qwen3-1.7B), CARD achieves 81.4% to 89.2% accuracy on GSM8K while reducing token cost by 1.88x to 2.40x compared to fixed decomposition baselines. On MATH-500, CARD reaches 75.1 to 86.8% accuracy using 1.71x to 5.74x fewer tokens. Our results demonstrate that preemptive complexity estimation enables both higher accuracy and significant efficiency gains.

---

<!-- third gather round, 2026-09-06: over-planning collapse, depth/width error-propagation equivalence, aggregation methods. -->

## 33. Limited Reasoning Space: The Cage of Long-Horizon Reasoning in LLMs (Halo)

**Cite:** "Limited Reasoning Space: The cage of long-horizon reasoning in LLMs." 2026. arXiv:2602.19281 (preprint). https://arxiv.org/abs/2602.19281

**Status:** PREPRINT — not peer-reviewed. Admitted: over-planning collapse and an optimal compute/planning range are the boundary question stated directly.

**Abstract (verbatim, arXiv):**
> The test-time compute strategy, such as Chain-of-Thought (CoT), has significantly enhanced the ability of large language models to solve complex tasks like logical reasoning. However, empirical studies indicate that simply increasing the compute budget can sometimes lead to a collapse in test-time performance when employing typical task decomposition strategies such as CoT. This work hypothesizes that reasoning failures with larger compute budgets stem from static planning methods, which hardly perceive the intrinsic boundaries of LLM reasoning. We term it as the Limited Reasoning Space hypothesis and perform theoretical analysis through the lens of a non-autonomous stochastic dynamical system. This insight suggests that there is an optimal range for compute budgets; over-planning can lead to redundant feedback and may even impair reasoning capabilities. To exploit the compute-scaling benefits and suppress over-planning, this work proposes Halo, a model predictive control framework for LLM planning. Halo is designed for long-horizon tasks with reason-based planning and crafts an entropy-driven dual controller, which adopts a Measure-then-Plan strategy to achieve controllable reasoning. Experimental results demonstrate that Halo outperforms static baselines on complex long-horizon tasks by dynamically regulating planning at the reasoning boundary.

---

## 34. Recursive Self-Aggregation Unlocks Deep Thinking in LLMs (RSA)

**Cite:** "Recursive Self-Aggregation Unlocks Deep Thinking in Large Language Models." 2025. arXiv:2509.26626 (preprint). https://arxiv.org/abs/2509.26626

**Status:** PREPRINT — not peer-reviewed. ADJACENT: an aggregation method (recombining candidate chains), touches recombination-as-lever but proposes rather than studies the failure surface.

**Abstract (verbatim, arXiv):**
> Test-time scaling methods improve the capabilities of large language models (LLMs) by increasing the amount of compute used during inference to make a prediction. Inference-time compute can be scaled in parallel by choosing among multiple independent solutions or sequentially through self-refinement. We propose Recursive Self-Aggregation (RSA), a test-time scaling method inspired by evolutionary methods that combines the benefits of both parallel and sequential scaling. Each step of RSA refines a population of candidate reasoning chains through aggregation of subsets to yield a population of improved solutions, which are then used as the candidate pool for the next iteration. Empirically, RSA delivers substantial performance gains with increasing compute budgets across diverse tasks, model families and sizes. Notably, RSA with Gemini 3 Flash attains performance near the top of the ARC-AGI-2 public leaderboard. RSA also enables Qwen3-4B-Instruct-2507 to achieve competitive performance with larger reasoning models, including DeepSeek-R1 and o3-mini (high), outperforming purely parallel and sequential scaling strategies across AIME-25, HMMT-25, Reasoning Gym, LiveCodeBench-v6, and SuperGPQA. We further propose a novel aggregation-aware reinforcement learning approach that yields significant performance gains by training the model to combine solutions.

---

<!-- fourth gather round, 2026-09-06: broad sweep — QA question-decomposition, planning benchmarks, CoT-power theory, multi-agent role decomposition, embodied/long-horizon planning, reasoning topologies, base agent loops. -->

## 35. Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions
**Cite:** Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, Ashish Sabharwal. "Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions." 2022. ACL 2023 (Long Papers). arXiv:2212.10509. https://arxiv.org/abs/2212.10509
**Abstract (verbatim, arXiv):**
> Prompting-based large language models (LLMs) are surprisingly powerful at generating natural language reasoning steps or Chains-of-Thoughts (CoT) for multi-step question answering (QA). They struggle, however, when the necessary knowledge is either unavailable to the LLM or not up-to-date within its parameters. While using the question to retrieve relevant text from an external knowledge source helps LLMs, we observe that this one-step retrieve-and-read approach is insufficient for multi-step QA. Here, \textit{what to retrieve} depends on \textit{what has already been derived}, which in turn may depend on \textit{what was previously retrieved}. To address this, we propose IRCoT, a new approach for multi-step QA that interleaves retrieval with steps (sentences) in a CoT, guiding the retrieval with CoT and in turn using retrieved results to improve CoT. Using IRCoT with GPT3 substantially improves retrieval (up to 21 points) as well as downstream QA (up to 15 points) on four datasets: HotpotQA, 2WikiMultihopQA, MuSiQue, and IIRC. We observe similar substantial gains in out-of-distribution (OOD) settings as well as with much smaller models such as Flan-T5-large without additional training. IRCoT reduces model hallucination, resulting in factually more accurate CoT reasoning. Code, data, and prompts are available at \url{https://github.com/stonybrooknlp/ircot}
**Flag:** RELATED — interleaves decomposition (CoT steps) with retrieval; each step is a sub-question grounded before the next.

---

## 36. Reasoning over Hierarchical Question Decomposition Tree for Explainable Question Answering
**Cite:** Jiajie Zhang, Shulin Cao, Tingjia Zhang, Xin Lv, Jiaxin Shi, Qi Tian, Juanzi Li, Lei Hou. "Reasoning over Hierarchical Question Decomposition Tree for Explainable Question Answering." 2023. Findings of ACL 2023. arXiv:2305.15056. https://arxiv.org/abs/2305.15056
**Abstract (verbatim, arXiv):**
> Explainable question answering (XQA) aims to answer a given question and provide an explanation why the answer is selected. Existing XQA methods focus on reasoning on a single knowledge source, e.g., structured knowledge bases, unstructured corpora, etc. However, integrating information from heterogeneous knowledge sources is essential to answer complex questions. In this paper, we propose to leverage question decomposing for heterogeneous knowledge integration, by breaking down a complex question into simpler ones, and selecting the appropriate knowledge source for each sub-question. To facilitate reasoning, we propose a novel two-stage XQA framework, Reasoning over Hierarchical Question Decomposition Tree (RoHT). First, we build the Hierarchical Question Decomposition Tree (HQDT) to understand the semantics of a complex question; then, we conduct probabilistic reasoning over HQDT from root to leaves recursively, to aggregate heterogeneous knowledge at different tree levels and search for a best solution considering the decomposing and answering probabilities. The experiments on complex QA datasets KQA Pro and Musique show that our framework outperforms SOTA methods significantly, demonstrating the effectiveness of leveraging question decomposing for knowledge integration and our RoHT framework.
**Flag:** RELATED — builds an explicit hierarchical question-decomposition tree and reasons over it; decomposition structure + recombination.

---

## 37. Decomposed Prompting Does Not Fix Knowledge Gaps, But Helps Models Say "I Don't Know"
**Review status:** reviewed -> sheet `07` (round 2). Cross-paper discussion: done - F1, F2, F3.

**Cite:** Dhruv Madhwal, Lyuxin David Zhang, Dan Roth, Tomer Wolfson, Vivek Gupta. "Decomposed Prompting Does Not Fix Knowledge Gaps, But Helps Models Say "I Don't Know"." 2026. Findings of ACL 2026. arXiv:2602.04853. https://arxiv.org/abs/2602.04853
**Abstract (verbatim, arXiv):**
> Large language models often struggle to recognize their knowledge limits in closed-book question answering, leading to confident hallucinations. While decomposed prompting is typically used to improve accuracy, we investigate its impact on reliability. We evaluate three task-equivalent prompting regimes: Direct, Assistive, and Incremental, across different model scales and multi-hop QA benchmarks. We find that although accuracy gains from decomposition diminish in frontier models, disagreements between prompting regimes remain highly indicative of potential errors. Because factual knowledge is typically stable while hallucinations are stochastic, cross-regime agreement provides a precise signal of internal uncertainty. We leverage this signal to implement a training-free abstention policy that requires no retrieval or fine-tuning. Our results show that disagreement-based abstention outperforms standard uncertainty baselines as an error detector, improving both F1 and AUROC across settings. This demonstrates that decomposition-based prompting can serve as a practical diagnostic probe for model reliability in closed-book QA.
**Flag:** RELATED (skeptic) — controlled test: decomposed prompting does NOT close knowledge gaps; its main effect is better abstention.

---

## 38. PlanBench: An Extensible Benchmark for Evaluating Large Language Models on Planning and Reasoning about Change
**Cite:** Karthik Valmeekam, Matthew Marquez, Alberto Olmo, Sarath Sreedharan, Subbarao Kambhampati. "PlanBench: An Extensible Benchmark for Evaluating Large Language Models on Planning and Reasoning about Change." 2022. NeurIPS 2023 Datasets & Benchmarks. arXiv:2206.10498. https://arxiv.org/abs/2206.10498
**Abstract (verbatim, arXiv):**
> Generating plans of action, and reasoning about change have long been considered a core competence of intelligent agents. It is thus no surprise that evaluating the planning and reasoning capabilities of large language models (LLMs) has become a hot topic of research. Most claims about LLM planning capabilities are however based on common sense tasks-where it becomes hard to tell whether LLMs are planning or merely retrieving from their vast world knowledge. There is a strong need for systematic and extensible planning benchmarks with sufficient diversity to evaluate whether LLMs have innate planning capabilities. Motivated by this, we propose PlanBench, an extensible benchmark suite based on the kinds of domains used in the automated planning community, especially in the International Planning Competition, to test the capabilities of LLMs in planning or reasoning about actions and change. PlanBench provides sufficient diversity in both the task domains and the specific planning capabilities. Our studies also show that on many critical capabilities-including plan generation-LLM performance falls quite short, even with the SOTA models. PlanBench can thus function as a useful marker of progress of LLMs in planning and reasoning.
**Flag:** RELATED — planning benchmark from the classical-planning community; plan generation, cost-optimal planning, plan verification.

---

## 39. NATURAL PLAN: Benchmarking LLMs on Natural Language Planning
**Cite:** Huaixiu Steven Zheng, Swaroop Mishra, Hugh Zhang, Xinyun Chen, Minmin Chen, Azade Nova, Le Hou, Heng-Tze Cheng, Quoc V. Le, Ed H. Chi, Denny Zhou. "NATURAL PLAN: Benchmarking LLMs on Natural Language Planning." 2024. preprint (venue unconfirmed). arXiv:2406.04520. https://arxiv.org/abs/2406.04520
**Abstract (verbatim, arXiv):**
> We introduce NATURAL PLAN, a realistic planning benchmark in natural language containing 3 key tasks: Trip Planning, Meeting Planning, and Calendar Scheduling. We focus our evaluation on the planning capabilities of LLMs with full information on the task, by providing outputs from tools such as Google Flights, Google Maps, and Google Calendar as contexts to the models. This eliminates the need for a tool-use environment for evaluating LLMs on Planning. We observe that NATURAL PLAN is a challenging benchmark for state of the art models. For example, in Trip Planning, GPT-4 and Gemini 1.5 Pro could only achieve 31.1% and 34.8% solve rate respectively. We find that model performance drops drastically as the complexity of the problem increases: all models perform below 5% when there are 10 cities, highlighting a significant gap in planning in natural language for SoTA LLMs. We also conduct extensive ablation studies on NATURAL PLAN to further shed light on the (in)effectiveness of approaches such as self-correction, few-shot generalization, and in-context planning with long-contexts on improving LLM planning.
**Flag:** RELATED — natural-language planning benchmark (trip/meeting/calendar) stressing constraint satisfaction over decomposed steps.

---

## 40. Tree-Planner: Efficient Close-loop Task Planning with Large Language Models
**Cite:** Mengkang Hu, Yao Mu, Xinmiao Yu, Mingyu Ding, Shiguang Wu, Wenqi Shao, Qiguang Chen, Bin Wang, Yu Qiao, Ping Luo. "Tree-Planner: Efficient Close-loop Task Planning with Large Language Models." 2023. ICLR 2024. arXiv:2310.08582. https://arxiv.org/abs/2310.08582
**Abstract (verbatim, arXiv):**
> This paper studies close-loop task planning, which refers to the process of generating a sequence of skills (a plan) to accomplish a specific goal while adapting the plan based on real-time observations. Recently, prompting Large Language Models (LLMs) to generate actions iteratively has become a prevalent paradigm due to its superior performance and user-friendliness. However, this paradigm is plagued by two inefficiencies: high token consumption and redundant error correction, both of which hinder its scalability for large-scale testing and applications. To address these issues, we propose Tree-Planner, which reframes task planning with LLMs into three distinct phases: plan sampling, action tree construction, and grounded deciding. Tree-Planner starts by using an LLM to sample a set of potential plans before execution, followed by the aggregation of them to form an action tree. Finally, the LLM performs a top-down decision-making process on the tree, taking into account real-time environmental information. Experiments show that Tree-Planner achieves state-of-the-art performance while maintaining high efficiency. By decomposing LLM queries into a single plan-sampling call and multiple grounded-deciding calls, a considerable part of the prompt are less likely to be repeatedly consumed. As a result, token consumption is reduced by 92.2% compared to the previously best-performing model. Additionally, by enabling backtracking on the action tree as needed, the correction process becomes more flexible, leading to a 40.5% decrease in error corrections.
**Flag:** RELATED — samples a plan-level 'tree' once then does grounded closed-loop selection; decomposition + re-planning with an explicit cost argument.

---

## 41. Chain of Thought Empowers Transformers to Solve Inherently Serial Problems
**Cite:** Zhiyuan Li, Hong Liu, Denny Zhou, Tengyu Ma. "Chain of Thought Empowers Transformers to Solve Inherently Serial Problems." 2024. ICLR 2024. arXiv:2402.12875. https://arxiv.org/abs/2402.12875
**Abstract (verbatim, arXiv):**
> Instructing the model to generate a sequence of intermediate steps, a.k.a., a chain of thought (CoT), is a highly effective method to improve the accuracy of large language models (LLMs) on arithmetics and symbolic reasoning tasks. However, the mechanism behind CoT remains unclear. This work provides a theoretical understanding of the power of CoT for decoder-only transformers through the lens of expressiveness. Conceptually, CoT empowers the model with the ability to perform inherently serial computation, which is otherwise lacking in transformers, especially when depth is low. Given input length $n$, previous works have shown that constant-depth transformers with finite precision $\mathsf{poly}(n)$ embedding size can only solve problems in $\mathsf{TC}^0$ without CoT. We first show an even tighter expressiveness upper bound for constant-depth transformers with constant-bit precision, which can only solve problems in $\mathsf{AC}^0$, a proper subset of $ \mathsf{TC}^0$. However, with $T$ steps of CoT, constant-depth transformers using constant-bit precision and $O(\log n)$ embedding size can solve any problem solvable by boolean circuits of size $T$. Empirically, enabling CoT dramatically improves the accuracy for tasks that are hard for parallel computation, including the composition of permutation groups, iterated squaring, and circuit value problems, especially for low-depth transformers.
**Flag:** RELATED (theory) — proves intermediate generation (decomposition into steps) adds serial computational power; the positive counterpart to compounding-error limits.

---

## 42. The Expressive Power of Transformers with Chain of Thought
**Review status:** reviewed -> sheet `06` (round 2). Cross-paper discussion: done - F16, F21; spawned candidate argument A1.

**Cite:** William Merrill, Ashish Sabharwal. "The Expressive Power of Transformers with Chain of Thought." 2023. ICLR 2024. arXiv:2310.07923. https://arxiv.org/abs/2310.07923
**Abstract (verbatim, arXiv):**
> Recent theoretical work has identified surprisingly simple reasoning problems, such as checking if two nodes in a graph are connected or simulating finite-state machines, that are provably unsolvable by standard transformers that answer immediately after reading their input. However, in practice, transformers' reasoning can be improved by allowing them to use a "chain of thought" or "scratchpad", i.e., generate and condition on a sequence of intermediate tokens before answering. Motivated by this, we ask: Does such intermediate generation fundamentally extend the computational power of a decoder-only transformer? We show that the answer is yes, but the amount of increase depends crucially on the amount of intermediate generation. For instance, we find that transformer decoders with a logarithmic number of decoding steps (w.r.t. the input length) push the limits of standard transformers only slightly, while a linear number of decoding steps, assuming projected pre-norm (a slight generalization of standard pre-norm), adds a clear new ability (under standard complexity conjectures): recognizing all regular languages. Our results also imply that linear steps keep transformer decoders within context-sensitive languages, and polynomial steps with generalized pre-norm make them recognize exactly the class of polynomial-time solvable problems -- the first exact characterization of a type of transformers in terms of standard complexity classes. Together, this provides a nuanced framework for understanding how the length of a transformer's chain of thought or scratchpad impacts its reasoning power.
**Flag:** RELATED (theory) — characterises how much the expressive power of a transformer grows with the amount of chain-of-thought / intermediate steps.

---

## 43. MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework
**Cite:** Sirui Hong, Mingchen Zhuge, Jiaqi Chen, Xiawu Zheng, Yuheng Cheng, Ceyao Zhang, Jinlin Wang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, Chenyu Ran, Lingfeng Xiao, Chenglin Wu, Jürgen Schmidhuber. "MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework." 2023. ICLR 2024 (Oral). arXiv:2308.00352. https://arxiv.org/abs/2308.00352
**Abstract (verbatim, arXiv):**
> Remarkable progress has been made on automated problem solving through societies of agents based on large language models (LLMs). Existing LLM-based multi-agent systems can already solve simple dialogue tasks. Solutions to more complex tasks, however, are complicated through logic inconsistencies due to cascading hallucinations caused by naively chaining LLMs. Here we introduce MetaGPT, an innovative meta-programming framework incorporating efficient human workflows into LLM-based multi-agent collaborations. MetaGPT encodes Standardized Operating Procedures (SOPs) into prompt sequences for more streamlined workflows, thus allowing agents with human-like domain expertise to verify intermediate results and reduce errors. MetaGPT utilizes an assembly line paradigm to assign diverse roles to various agents, efficiently breaking down complex tasks into subtasks involving many agents working together. On collaborative software engineering benchmarks, MetaGPT generates more coherent solutions than previous chat-based multi-agent systems. Our project can be found at https://github.com/geekan/MetaGPT
**Flag:** RELATED — encodes software-team SOPs as roles; hierarchical task decomposition across Product/Architect/Engineer/QA agents with a recombination pipeline.

---

## 44. AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation
**Cite:** Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang, Shaokun Zhang, Jiale Liu, Ahmed Hassan Awadallah, Ryen W White, Doug Burger, Chi Wang. "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation." 2023. COLM 2024. arXiv:2308.08155. https://arxiv.org/abs/2308.08155
**Abstract (verbatim, arXiv):**
> AutoGen is an open-source framework that allows developers to build LLM applications via multiple agents that can converse with each other to accomplish tasks. AutoGen agents are customizable, conversable, and can operate in various modes that employ combinations of LLMs, human inputs, and tools. Using AutoGen, developers can also flexibly define agent interaction behaviors. Both natural language and computer code can be used to program flexible conversation patterns for different applications. AutoGen serves as a generic infrastructure to build diverse applications of various complexities and LLM capacities. Empirical studies demonstrate the effectiveness of the framework in many example applications, with domains ranging from mathematics, coding, question answering, operations research, online decision-making, entertainment, etc.
**Flag:** ADJACENT — a framework for composing multi-agent conversations; enables role decomposition but does not study when or how deep to split.

---

## 45. ChatDev: Communicative Agents for Software Development
**Cite:** Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan Dang, Jiahao Li, Cheng Yang, Weize Chen, Yusheng Su, Xin Cong, Juyuan Xu, Dahai Li, Zhiyuan Liu, Maosong Sun. "ChatDev: Communicative Agents for Software Development." 2023. ACL 2024. arXiv:2307.07924. https://arxiv.org/abs/2307.07924
**Abstract (verbatim, arXiv):**
> Software development is a complex task that necessitates cooperation among multiple members with diverse skills. Numerous studies used deep learning to improve specific phases in a waterfall model, such as design, coding, and testing. However, the deep learning model in each phase requires unique designs, leading to technical inconsistencies across various phases, which results in a fragmented and ineffective development process. In this paper, we introduce ChatDev, a chat-powered software development framework in which specialized agents driven by large language models (LLMs) are guided in what to communicate (via chat chain) and how to communicate (via communicative dehallucination). These agents actively contribute to the design, coding, and testing phases through unified language-based communication, with solutions derived from their multi-turn dialogues. We found their utilization of natural language is advantageous for system design, and communicating in programming language proves helpful in debugging. This paradigm demonstrates how linguistic communication facilitates multi-agent collaboration, establishing language as a unifying bridge for autonomous task-solving among LLM agents. The code and data are available at https://github.com/OpenBMB/ChatDev.
**Flag:** RELATED — decomposes software development into fixed phases (design/code/test/doc) run by role agents via chat chains.

---

## 46. AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors
**Cite:** Weize Chen, Yusheng Su, Jingwei Zuo, Cheng Yang, Chenfei Yuan, Chi-Min Chan, Heyang Yu, Yaxi Lu, Yi-Hsin Hung, Chen Qian, Yujia Qin, Xin Cong, Ruobing Xie, Zhiyuan Liu, Maosong Sun, Jie Zhou. "AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors." 2023. preprint (under review at time of posting). arXiv:2308.10848. https://arxiv.org/abs/2308.10848
**Abstract (verbatim, arXiv):**
> Autonomous agents empowered by Large Language Models (LLMs) have undergone significant improvements, enabling them to generalize across a broad spectrum of tasks. However, in real-world scenarios, cooperation among individuals is often required to enhance the efficiency and effectiveness of task accomplishment. Hence, inspired by human group dynamics, we propose a multi-agent framework \framework that can collaboratively and dynamically adjust its composition as a greater-than-the-sum-of-its-parts system. Our experiments demonstrate that \framework framework can effectively deploy multi-agent groups that outperform a single agent. Furthermore, we delve into the emergence of social behaviors among individual agents within a group during collaborative task accomplishment. In view of these behaviors, we discuss some possible strategies to leverage positive ones and mitigate negative ones for improving the collaborative potential of multi-agent groups. Our codes for \framework will soon be released at \url{https://github.com/OpenBMB/AgentVerse}.
**Flag:** ADJACENT — a platform for multi-agent collaboration and emergent behaviour; role decomposition as infrastructure, not the split decision.

---

## 47. CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society
**Cite:** Guohao Li, Hasan Abed Al Kader Hammoud, Hani Itani, Dmitrii Khizbullin, Bernard Ghanem. "CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society." 2023. NeurIPS 2023. arXiv:2303.17760. https://arxiv.org/abs/2303.17760
**Abstract (verbatim, arXiv):**
> The rapid advancement of chat-based language models has led to remarkable progress in complex task-solving. However, their success heavily relies on human input to guide the conversation, which can be challenging and time-consuming. This paper explores the potential of building scalable techniques to facilitate autonomous cooperation among communicative agents, and provides insight into their "cognitive" processes. To address the challenges of achieving autonomous cooperation, we propose a novel communicative agent framework named role-playing. Our approach involves using inception prompting to guide chat agents toward task completion while maintaining consistency with human intentions. We showcase how role-playing can be used to generate conversational data for studying the behaviors and capabilities of a society of agents, providing a valuable resource for investigating conversational language models. In particular, we conduct comprehensive studies on instruction-following cooperation in multi-agent settings. Our contributions include introducing a novel communicative agent framework, offering a scalable approach for studying the cooperative behaviors and capabilities of multi-agent systems, and open-sourcing our library to support research on communicative agents and beyond: https://github.com/camel-ai/camel.
**Flag:** ADJACENT — role-playing two-agent decomposition of a task into a guided dialogue; a decomposition pattern, not a study of its limits.

---

## 48. LLM-Planner: Few-Shot Grounded Planning for Embodied Agents with Large Language Models
**Cite:** Chan Hee Song, Jiaman Wu, Clayton Washington, Brian M. Sadler, Wei-Lun Chao, Yu Su. "LLM-Planner: Few-Shot Grounded Planning for Embodied Agents with Large Language Models." 2022. ICCV 2023. arXiv:2212.04088. https://arxiv.org/abs/2212.04088
**Abstract (verbatim, arXiv):**
> This study focuses on using large language models (LLMs) as a planner for embodied agents that can follow natural language instructions to complete complex tasks in a visually-perceived environment. The high data cost and poor sample efficiency of existing methods hinders the development of versatile agents that are capable of many tasks and can learn new tasks quickly. In this work, we propose a novel method, LLM-Planner, that harnesses the power of large language models to do few-shot planning for embodied agents. We further propose a simple but effective way to enhance LLMs with physical grounding to generate and update plans that are grounded in the current environment. Experiments on the ALFRED dataset show that our method can achieve very competitive few-shot performance: Despite using less than 0.5% of paired training data, LLM-Planner achieves competitive performance with recent baselines that are trained using the full training data. Existing methods can barely complete any task successfully under the same few-shot setting. Our work opens the door for developing versatile and sample-efficient embodied agents that can quickly learn many tasks. Website: https://dki-lab.github.io/LLM-Planner
**Flag:** RELATED — hierarchical: LLM decomposes a natural-language goal into subgoals with closed-loop re-planning on perception feedback.

---

## 49. Describe, Explain, Plan and Select: Interactive Planning with Large Language Models Enables Open-World Multi-Task Agents
**Cite:** Zihao Wang, Shaofei Cai, Guanzhou Chen, Anji Liu, Xiaojian Ma, Yitao Liang. "Describe, Explain, Plan and Select: Interactive Planning with Large Language Models Enables Open-World Multi-Task Agents." 2023. NeurIPS 2023. arXiv:2302.01560. https://arxiv.org/abs/2302.01560
**Abstract (verbatim, arXiv):**
> We investigate the challenge of task planning for multi-task embodied agents in open-world environments. Two main difficulties are identified: 1) executing plans in an open-world environment (e.g., Minecraft) necessitates accurate and multi-step reasoning due to the long-term nature of tasks, and 2) as vanilla planners do not consider how easy the current agent can achieve a given sub-task when ordering parallel sub-goals within a complicated plan, the resulting plan could be inefficient or even infeasible. To this end, we propose "$\underline{D}$escribe, $\underline{E}$xplain, $\underline{P}$lan and $\underline{S}$elect" ($\textbf{DEPS}$), an interactive planning approach based on Large Language Models (LLMs). DEPS facilitates better error correction on initial LLM-generated $\textit{plan}$ by integrating $\textit{description}$ of the plan execution process and providing self-$\textit{explanation}$ of feedback when encountering failures during the extended planning phases. Furthermore, it includes a goal $\textit{selector}$, which is a trainable module that ranks parallel candidate sub-goals based on the estimated steps of completion, consequently refining the initial plan. Our experiments mark the milestone of the first zero-shot multi-task agent that can robustly accomplish 70+ Minecraft tasks and nearly double the overall performances. Further testing reveals our method's general effectiveness in popularly adopted non-open-ended domains as well (i.e., ALFWorld and tabletop manipulation). The ablation and exploratory studies detail how our design beats the counterparts and provide a promising update on the $\texttt{ObtainDiamond}$ grand challenge with our approach. The code is released at https://github.com/CraftJarvis/MC-Planner.
**Flag:** RELATED — Describe/Explain/Plan/Select: iterative decomposition with a selector that ranks candidate subgoals by estimated completion cost.

---

## 50. SwiftSage: A Generative Agent with Fast and Slow Thinking for Complex Interactive Tasks
**Cite:** Bill Yuchen Lin, Yicheng Fu, Karina Yang, Faeze Brahman, Shiyu Huang, Chandra Bhagavatula, Prithviraj Ammanabrolu, Yejin Choi, Xiang Ren. "SwiftSage: A Generative Agent with Fast and Slow Thinking for Complex Interactive Tasks." 2023. NeurIPS 2023 (Spotlight). arXiv:2305.17390. https://arxiv.org/abs/2305.17390
**Abstract (verbatim, arXiv):**
> We introduce SwiftSage, a novel agent framework inspired by the dual-process theory of human cognition, designed to excel in action planning for complex interactive reasoning tasks. SwiftSage integrates the strengths of behavior cloning and prompting large language models (LLMs) to enhance task completion performance. The framework comprises two primary modules: the Swift module, representing fast and intuitive thinking, and the Sage module, emulating deliberate thought processes. The Swift module is a small encoder-decoder LM fine-tuned on the oracle agent's action trajectories, while the Sage module employs LLMs such as GPT-4 for subgoal planning and grounding. We develop a heuristic method to harmoniously integrate the two modules, resulting in a more efficient and robust problem-solving process. In 30 tasks from the ScienceWorld benchmark, SwiftSage significantly outperforms other methods such as SayCan, ReAct, and Reflexion, demonstrating its effectiveness in solving complex interactive tasks.
**Flag:** ADJACENT — fast/slow dual-process agent; the slow module plans/decomposes but the contribution is the switching, not the depth rule.

---

## 51. Language Models as Zero-Shot Planners: Extracting Actionable Knowledge for Embodied Agents
**Cite:** Wenlong Huang, Pieter Abbeel, Deepak Pathak, Igor Mordatch. "Language Models as Zero-Shot Planners: Extracting Actionable Knowledge for Embodied Agents." 2022. ICML 2022. arXiv:2201.07207. https://arxiv.org/abs/2201.07207
**Abstract (verbatim, arXiv):**
> Can world knowledge learned by large language models (LLMs) be used to act in interactive environments? In this paper, we investigate the possibility of grounding high-level tasks, expressed in natural language (e.g. "make breakfast"), to a chosen set of actionable steps (e.g. "open fridge"). While prior work focused on learning from explicit step-by-step examples of how to act, we surprisingly find that if pre-trained LMs are large enough and prompted appropriately, they can effectively decompose high-level tasks into mid-level plans without any further training. However, the plans produced naively by LLMs often cannot map precisely to admissible actions. We propose a procedure that conditions on existing demonstrations and semantically translates the plans to admissible actions. Our evaluation in the recent VirtualHome environment shows that the resulting method substantially improves executability over the LLM baseline. The conducted human evaluation reveals a trade-off between executability and correctness but shows a promising sign towards extracting actionable knowledge from language models. Website at https://huangwl18.github.io/language-planner
**Flag:** ANCHOR (pre-2023) — first to show LLMs zero-shot decompose high-level tasks into action sequences for embodied agents; foundational for the whole line.

---

## 52. Skeleton-of-Thought: Prompting LLMs for Efficient Parallel Generation
**Cite:** Xuefei Ning, Zinan Lin, Zixuan Zhou, Zifu Wang, Huazhong Yang, Yu Wang. "Skeleton-of-Thought: Prompting LLMs for Efficient Parallel Generation." 2023. ICLR 2024. arXiv:2307.15337. https://arxiv.org/abs/2307.15337
**Abstract (verbatim, arXiv):**
> This work aims at decreasing the end-to-end generation latency of large language models (LLMs). One of the major causes of the high generation latency is the sequential decoding approach adopted by almost all state-of-the-art LLMs. In this work, motivated by the thinking and writing process of humans, we propose Skeleton-of-Thought (SoT), which first guides LLMs to generate the skeleton of the answer, and then conducts parallel API calls or batched decoding to complete the contents of each skeleton point in parallel. Not only does SoT provide considerable speed-ups across 12 LLMs, but it can also potentially improve the answer quality on several question categories. SoT is an initial attempt at data-centric optimization for inference efficiency, and showcases the potential of eliciting high-quality answers by explicitly planning the answer structure in language.
**Flag:** RELATED — decomposes an answer into a 'skeleton' of independent points expanded in parallel; explicit parallel decomposition targeting latency.

---

## 53. Buffer of Thoughts: Thought-Augmented Reasoning with Large Language Models
**Cite:** Ling Yang, Zhaochen Yu, Tianjun Zhang, Shiyi Cao, Minkai Xu, Wentao Zhang, Joseph E. Gonzalez, Bin Cui. "Buffer of Thoughts: Thought-Augmented Reasoning with Large Language Models." 2024. NeurIPS 2024 (Spotlight). arXiv:2406.04271. https://arxiv.org/abs/2406.04271
**Abstract (verbatim, arXiv):**
> We introduce Buffer of Thoughts (BoT), a novel and versatile thought-augmented reasoning approach for enhancing accuracy, efficiency and robustness of large language models (LLMs). Specifically, we propose meta-buffer to store a series of informative high-level thoughts, namely thought-template, distilled from the problem-solving processes across various tasks. Then for each problem, we retrieve a relevant thought-template and adaptively instantiate it with specific reasoning structures to conduct efficient reasoning. To guarantee the scalability and stability, we further propose buffer-manager to dynamically update the meta-buffer, thus enhancing the capacity of meta-buffer as more tasks are solved. We conduct extensive experiments on 10 challenging reasoning-intensive tasks, and achieve significant performance improvements over previous SOTA methods: 11% on Game of 24, 20% on Geometric Shapes and 51% on Checkmate-in-One. Further analysis demonstrate the superior generalization ability and model robustness of our BoT, while requiring only 12% of the cost of multi-query prompting methods (e.g., tree/graph of thoughts) on average. Notably, we find that our Llama3-8B+BoT has the potential to surpass Llama3-70B model. Our project is available at: https://github.com/YangLing0818/buffer-of-thought-llm
**Flag:** ADJACENT — retrieves and instantiates reusable 'thought-templates'; a decomposition-structure store rather than a when/how-deep rule.

---

## 54. Cumulative Reasoning with Large Language Models
**Review status:** reviewed -> sheet `14` (round 4). Cross-paper discussion: done - F24, F27, F28; reinforces F13, F17.

**Cite:** Yifan Zhang, Jingqin Yang, Yang Yuan, Andrew Chi-Chih Yao. "Cumulative Reasoning with Large Language Models." 2023. TMLR. arXiv:2308.04371. https://arxiv.org/abs/2308.04371
**Abstract (verbatim, arXiv):**
> Recent advancements in large language models (LLMs) have shown remarkable progress, yet their ability to solve complex problems remains limited. In this work, we introduce Cumulative Reasoning (CR), a structured framework that enhances LLM problem-solving by emulating human-like iterative and cumulative thought processes. CR orchestrates LLMs in three distinct roles: Proposer, Verifier(s), and Reporter, to systematically decompose tasks, generate and validate intermediate reasoning steps, and compose them into a solution by building a dynamic Directed Acyclic Graph (DAG) of verified propositions. This approach substantially enhances problem-solving capabilities. We demonstrate CR's advantage through several complex reasoning tasks: it outperforms existing methods in logical inference tasks with up to a 9.3% improvement, achieving 98.04% accuracy on the curated FOLIO wiki dataset. In the Game of 24, it achieves 98% accuracy, marking a 24% improvement over previous methods. In solving MATH problems, CR achieves a 4.2% increase from previous methods and a 43% relative improvement in the most challenging level 5 problems. When incorporating a code environment with CR, we further harness LLMs' reasoning capabilities and outperform the Program of Thought (PoT) method by 38.8%.
**Flag:** RELATED — accumulates verified intermediate subresults to guide subsequent decomposition steps; decomposition + recombination with a correctness filter.

---

## 55. ReAct: Synergizing Reasoning and Acting in Language Models
**Cite:** Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao. "ReAct: Synergizing Reasoning and Acting in Language Models." 2022. ICLR 2023. arXiv:2210.03629. https://arxiv.org/abs/2210.03629
**Abstract (verbatim, arXiv):**
> While large language models (LLMs) have demonstrated impressive capabilities across tasks in language understanding and interactive decision making, their abilities for reasoning (e.g. chain-of-thought prompting) and acting (e.g. action plan generation) have primarily been studied as separate topics. In this paper, we explore the use of LLMs to generate both reasoning traces and task-specific actions in an interleaved manner, allowing for greater synergy between the two: reasoning traces help the model induce, track, and update action plans as well as handle exceptions, while actions allow it to interface with external sources, such as knowledge bases or environments, to gather additional information. We apply our approach, named ReAct, to a diverse set of language and decision making tasks and demonstrate its effectiveness over state-of-the-art baselines, as well as improved human interpretability and trustworthiness over methods without reasoning or acting components. Concretely, on question answering (HotpotQA) and fact verification (Fever), ReAct overcomes issues of hallucination and error propagation prevalent in chain-of-thought reasoning by interacting with a simple Wikipedia API, and generates human-like task-solving trajectories that are more interpretable than baselines without reasoning traces. On two interactive decision making benchmarks (ALFWorld and WebShop), ReAct outperforms imitation and reinforcement learning methods by an absolute success rate of 34% and 10% respectively, while being prompted with only one or two in-context examples. Project site with code: https://react-lm.github.io
**Flag:** ANCHOR — ReAct: interleaves reasoning traces and actions; the base agent loop most later decomposition/agent work builds on.

---

## 56. Reflexion: Language Agents with Verbal Reinforcement Learning
**Cite:** Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao. "Reflexion: Language Agents with Verbal Reinforcement Learning." 2023. NeurIPS 2023. arXiv:2303.11366. https://arxiv.org/abs/2303.11366
**Abstract (verbatim, arXiv):**
> Large language models (LLMs) have been increasingly used to interact with external environments (e.g., games, compilers, APIs) as goal-driven agents. However, it remains challenging for these language agents to quickly and efficiently learn from trial-and-error as traditional reinforcement learning methods require extensive training samples and expensive model fine-tuning. We propose Reflexion, a novel framework to reinforce language agents not by updating weights, but instead through linguistic feedback. Concretely, Reflexion agents verbally reflect on task feedback signals, then maintain their own reflective text in an episodic memory buffer to induce better decision-making in subsequent trials. Reflexion is flexible enough to incorporate various types (scalar values or free-form language) and sources (external or internally simulated) of feedback signals, and obtains significant improvements over a baseline agent across diverse tasks (sequential decision-making, coding, language reasoning). For example, Reflexion achieves a 91% pass@1 accuracy on the HumanEval coding benchmark, surpassing the previous state-of-the-art GPT-4 that achieves 80%. We also conduct ablation and analysis studies using different feedback signals, feedback incorporation methods, and agent types, and provide insights into how they affect performance.
**Flag:** ADJACENT — verbal self-reflection loop over trials; an iterate-until-better mechanism that neighbours the stop/depth question.

---

## 57. GenDec: A robust generative Question-decomposition method for Multi-hop reasoning
**Cite:** Jian Wu, Linyi Yang, Yuliang Ji, Wenhao Huang, Börje F. Karlsson, Manabu Okumura. "GenDec: A robust generative Question-decomposition method for Multi-hop reasoning." 2024. preprint (venue unconfirmed). arXiv:2402.11166. https://arxiv.org/abs/2402.11166
**Abstract (verbatim, arXiv):**
> Multi-hop QA (MHQA) involves step-by-step reasoning to answer complex questions and find multiple relevant supporting facts. However, Existing large language models'(LLMs) reasoning ability in multi-hop question answering remains exploration, which is inadequate in answering multi-hop questions. Moreover, it is unclear whether LLMs follow a desired reasoning chain to reach the right final answer. In this paper, we propose a \textbf{gen}erative question \textbf{dec}omposition method (GenDec) from the perspective of explainable QA by generating independent and complete sub-questions based on incorporating additional extracted evidence for enhancing LLMs' reasoning ability in RAG. To demonstrate the impact, generalization, and robustness of Gendec, we conduct two experiments, the first is combining GenDec with small QA systems on paragraph retrieval and QA tasks. We secondly examine the reasoning capabilities of various state-of-the-art LLMs including GPT-4 and GPT-3.5 combined with GenDec. We experiment on the HotpotQA, 2WikihopMultiHopQA, MuSiQue, and PokeMQA datasets.
**Flag:** RELATED — a generative question-decomposition model for multi-hop reasoning aimed at robustness of the decomposition itself.

---

## 58. FSM: A Finite State Machine Based Zero-Shot Prompting Paradigm for Multi-Hop Question Answering
**Cite:** Xiaochen Wang, Junqing He, Zhe yang, Yiru Wang, Xiangdi Meng, Kunhao Pan, Zhifang Sui. "FSM: A Finite State Machine Based Zero-Shot Prompting Paradigm for Multi-Hop Question Answering." 2024. preprint (venue unconfirmed). arXiv:2407.02964. https://arxiv.org/abs/2407.02964
**Abstract (verbatim, arXiv):**
> Large Language Models (LLMs) with chain-of-thought (COT) prompting have demonstrated impressive abilities on simple nature language inference tasks. However, they tend to perform poorly on Multi-hop Question Answering (MHQA) tasks due to several challenges, including hallucination, error propagation and limited context length. We propose a prompting method, Finite State Machine (FSM) to enhance the reasoning capabilities of LLM for complex tasks in addition to improved effectiveness and trustworthiness. Different from COT methods, FSM addresses MHQA by iteratively decomposing a question into multi-turn sub-questions, and self-correcting in time, improving the accuracy of answers in each step. Specifically, FSM addresses one sub-question at a time and decides on the next step based on its current result and state, in an automaton-like format. Experiments on benchmarks show the effectiveness of our method. Although our method performs on par with the baseline on relatively simpler datasets, it excels on challenging datasets like Musique. Moreover, this approach mitigates the hallucination phenomenon, wherein the correct final answer can be recovered despite errors in intermediate reasoning. Furthermore, our method improves LLMs' ability to follow specified output format requirements, significantly reducing the difficulty of answer interpretation and the need for reformatting.
**Flag:** RELATED — casts zero-shot multi-hop decomposition as a finite-state-machine traversal, one sub-question per state.

---

<!-- fifth gather round, 2026-09-06: dedicated systematic reviews / comparative surveys of decomposition approaches. -->

## 59. Understanding the planning of LLM agents: A survey
**Cite:** Xu Huang, Weiwen Liu, Xiaolong Chen, Xingmei Wang, Hao Wang, Defu Lian, Yasheng Wang, Ruiming Tang, Enhong Chen. "Understanding the planning of LLM agents: A survey." 2024. preprint (widely cited; venue unconfirmed). arXiv:2402.02716. https://arxiv.org/abs/2402.02716
**Abstract (verbatim, arXiv):**
> As Large Language Models (LLMs) have shown significant intelligence, the progress to leverage LLMs as planning modules of autonomous agents has attracted more attention. This survey provides the first systematic view of LLM-based agents planning, covering recent works aiming to improve planning ability. We provide a taxonomy of existing works on LLM-Agent planning, which can be categorized into Task Decomposition, Plan Selection, External Module, Reflection and Memory. Comprehensive analyses are conducted for each direction, and further challenges for the field of research are discussed.
**Flag:** RELATED (survey) — first systematic taxonomy of LLM-agent planning; Task Decomposition is category 1, split into decomposition-first vs interleaved.

---

## 60. Test-time Scaling of LLMs: A Survey from A Subproblem Structure Perspective
**Review status:** reviewed -> sheet `02` (round 1). Cross-paper discussion: done - F13, F16, F17, F22.

**Cite:** Zhuoyi Yang, Xu Guo, Tong Zhang, Huijuan Xu, Boyang Li. "Test-time Scaling of LLMs: A Survey from A Subproblem Structure Perspective." 2025. preprint. arXiv:2511.14772. https://arxiv.org/abs/2511.14772
**Abstract (verbatim, arXiv):**
> With this paper, we survey techniques for improving the predictive accuracy of pretrained large language models by allocating additional compute at inference time. In categorizing test-time scaling methods, we place special emphasis on how a problem is decomposed into subproblems and on the topological organization of these subproblems whether sequential, parallel, or tree-structured. This perspective allows us to unify diverse approaches such as Chain-of-Thought, Branch-Solve-Merge, and Tree-of-Thought under a common lens. We further synthesize existing analyses of these techniques, highlighting their respective strengths and weaknesses, and conclude by outlining promising directions for future research
**Flag:** RELATED (survey) — organises test-time-scaling methods explicitly by how a problem is decomposed into subproblems and their topology (sequential/parallel/tree); unifies CoT, Branch-Solve-Merge, ToT and synthesises their analyses.

---

## 61. Large Language Models for Planning: A Comprehensive and Systematic Survey
**Review status:** reviewed -> sheet `03` (round 1). Cross-paper discussion: done - F13, F14, F18, F19, F22.

**Cite:** Pengfei Cao, Tianyi Men, Wencan Liu, Jingwen Zhang, Xuzhao Li, Xixun Lin, Dianbo Sui, Yanan Cao, Kang Liu, Jun Zhao. "Large Language Models for Planning: A Comprehensive and Systematic Survey." 2025. preprint. arXiv:2505.19683. https://arxiv.org/abs/2505.19683
**Abstract (verbatim, arXiv):**
> Planning represents a fundamental capability of intelligent agents, requiring comprehensive environmental understanding, rigorous logical reasoning, and effective sequential decision-making. While Large Language Models (LLMs) have demonstrated remarkable performance on certain planning tasks, their broader application in this domain warrants systematic investigation. This paper presents a comprehensive review of LLM-based planning. Specifically, this survey is structured as follows: First, we establish the theoretical foundations by introducing essential definitions and categories about automated planning. Next, we provide a detailed taxonomy and analysis of contemporary LLM-based planning methodologies, categorizing them into three principal approaches: 1) External Module Augmented Methods that combine LLMs with additional components for planning, 2) Finetuning-based Methods that involve using trajectory data and feedback signals to adjust LLMs in order to improve their planning abilities, and 3) Searching-based Methods that break down complex tasks into simpler components, navigate the planning space, or enhance decoding strategies to find the best solutions. Subsequently, we systematically summarize existing evaluation frameworks, including benchmark datasets, evaluation metrics and performance comparisons between representative planning methods. Finally, we discuss the underlying mechanisms enabling LLM-based planning and outline promising research directions for this rapidly evolving field. We hope this survey will serve as a valuable resource to inspire innovation and drive progress in this field.
**Flag:** ADJACENT (survey) — comprehensive LLM-planning survey; decomposition is one component of a broader planning taxonomy.

---


> **Import note (2026-09-06).** This inventory was assembled in a throwaway
> gather repo over five rounds. Entries 35-59 had originally captured a broken
> title (the abstract-fetch script grabbed the Atom feed's query `<title>`
> instead of the entry title). Those 25 titles were re-fetched from the arXiv
> API and repaired in place on 2026-09-06; IDs, authors, venues, links and the
> verbatim abstracts were unaffected.


<!-- sixth gather round, 2026-09-07: targeted at narrowing ideas I1-I5 and deepening findings F13-F32 (cost, error recovery, verifier reliability, plan-structure metrics, HTN aggregation, code-domain decomposition, frontier-model decomposition). Preprints admitted and flagged. -->

## 62. AI Agents That Matter

**Cite:** Sayash Kapoor, Benedikt Stroebl, Zachary S. Siegel, Nitya Nadgir, Arvind Narayanan. "AI Agents That Matter." 2024. arXiv:2407.01502 (preprint; widely cited). https://arxiv.org/abs/2407.01502

**Targets:** F22 / I1 - cost as a co-equal metric to accuracy; argues SOTA agents are needlessly complex because benchmarks ignore cost; implements a joint cost-accuracy optimisation. Flagged by sheet 12 as its inherited premise.

**Abstract (verbatim, arXiv):**
> AI agents are an exciting new research direction, and agent development is driven by benchmarks. Our analysis of current agent benchmarks and evaluation practices reveals several shortcomings that hinder their usefulness in real-world applications. First, there is a narrow focus on accuracy without attention to other metrics. As a result, SOTA agents are needlessly complex and costly, and the community has reached mistaken conclusions about the sources of accuracy gains. Our focus on cost in addition to accuracy motivates the new goal of jointly optimizing the two metrics. We design and implement one such optimization, showing its potential to greatly reduce cost while maintaining accuracy. Second, the benchmarking needs of model and downstream developers have been conflated, making it hard to identify which agent would be best suited for a particular application. Third, many agent benchmarks have inadequate holdout sets, and sometimes none at all. This has led to agents that are fragile because they take shortcuts and overfit to the benchmark in various ways. We prescribe a principled framework for avoiding overfitting. Finally, there is a lack of standardization in evaluation practices, leading to a pervasive lack of reproducibility.

---

## 63. Agentless: Demystifying LLM-based Software Engineering Agents
**Review status:** reviewed -> sheet 19-agentless.md (round 5). Cross-paper discussion: pending.


**Cite:** Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, Lingming Zhang. "Agentless: Demystifying LLM-based Software Engineering Agents." 2024. arXiv:2407.01489 (preprint). https://arxiv.org/abs/2407.01489

**Targets:** F22 / F9 / code domain - a fixed 3-phase localise/repair/validate pipeline (no autonomous planning) beats complex agents on SWE-bench Lite at $0.70; the do-less baseline for decomposition-in-software. Flagged by sheet 12.

**Abstract (verbatim, arXiv):**
> Recent advancements in large language models (LLMs) have significantly advanced the automation of software development tasks, including code synthesis, program repair, and test generation. More recently, researchers and industry practitioners have developed various autonomous LLM agents to perform end-to-end software development tasks. These agents are equipped with the ability to use tools, run commands, observe feedback from the environment, and plan for future actions. However, the complexity of these agent-based approaches, together with the limited abilities of current LLMs, raises the following question: Do we really have to employ complex autonomous software agents? To attempt to answer this question, we build Agentless -- an agentless approach to automatically solve software development problems. Compared to the verbose and complex setup of agent-based approaches, Agentless employs a simplistic three-phase process of localization, repair, and patch validation, without letting the LLM decide future actions or operate with complex tools. Our results on the popular SWE-bench Lite benchmark show that surprisingly the simplistic Agentless is able to achieve both the highest performance (32.00%, 96 correct fixes) and low cost ($0.70) compared with all existing open-source software agents! Furthermore, we manually classified the problems in SWE-bench Lite and found problems with exact ground truth patch or insufficient/misleading issue descriptions. As such, we construct SWE-bench Lite-S by excluding such problematic issues to perform more rigorous evaluation and comparison.

---

## 64. When Does Divide and Conquer Work for Long Context LLM? A Noise Decomposition Framework
**Review status:** reviewed -> sheet 17-divide-conquer-noise.md (round 5). Cross-paper discussion: pending.


**Cite:** Zhen Xu, Shang Zhu, Jue Wang, Junlin Wang, Ben Athiwaratkun, Chi Wang, James Zou, Ce Zhang. "When Does Divide and Conquer Work for Long Context LLM? A Noise Decomposition Framework." 2026. ICLR 2026. arXiv:2506.16411. https://arxiv.org/abs/2506.16411

**Targets:** A1 / F16 / F13 / I3 - a theory that splits long-context failure into cross-chunk dependence (task noise), length-induced confusion (model noise), and imperfect integration (aggregator noise); derives when chunk-and-aggregate lets a weaker model beat a stronger single-shot one.

**Abstract (verbatim, arXiv):**
> We investigate the challenge of applying Large Language Models (LLMs) to long texts. We propose a theoretical framework that distinguishes the failure modes of long context tasks into three categories: cross-chunk dependence (task noise), confusion that grows with context size (model noise), and the imperfect integration of partial results (aggregator noise). Under this view, we analyze when it is effective to use multi-agent chunking, i.e., dividing a lengthy sequence into smaller chunks and aggregating the processed results of each chunk. Our experiments on tasks such as retrieval, question answering, and summarization confirm both the theoretical analysis and the conditions that favor multi-agent chunking. By exploring the accelerated decay of model fidelity with input length, we also explain why, for large inputs, a weaker model configured with chunk-based processing can surpass a more advanced model like GPT4o applied in a single shot. Overall, we present a principled understanding framework and our results highlight a direct pathway to handling long contexts in LLMs with carefully managed chunking and aggregator strategies.

---

## 65. Question Decomposition Improves the Faithfulness of Model-Generated Reasoning

**Cite:** Ansh Radhakrishnan, Karina Nguyen, Anna Chen, Carol Chen, Carson Denison, Danny Hernandez, Esin Durmus, Evan Hubinger, et al. (Anthropic). "Question Decomposition Improves the Faithfulness of Model-Generated Reasoning." 2023. arXiv:2307.11768 (preprint). https://arxiv.org/abs/2307.11768

**Targets:** F25 / F30 / F5 - answering sub-questions in SEPARATE contexts markedly improves the faithfulness of stated reasoning over CoT while keeping some of the gain; a direct argument that execution-across-contexts is a different thing from one narrated stream. Named in sheet 07's citation list.

**Abstract (verbatim, arXiv):**
> As large language models (LLMs) perform more difficult tasks, it becomes harder to verify the correctness and safety of their behavior. One approach to help with this issue is to prompt LLMs to externalize their reasoning, e.g., by having them generate step-by-step reasoning as they answer a question (Chain-of-Thought; CoT). The reasoning may enable us to check the process that models use to perform tasks. However, this approach relies on the stated reasoning faithfully reflecting the model's actual reasoning, which is not always the case. To improve over the faithfulness of CoT reasoning, we have models generate reasoning by decomposing questions into subquestions. Decomposition-based methods achieve strong performance on question-answering tasks, sometimes approaching that of CoT while improving the faithfulness of the model's stated reasoning on several recently-proposed metrics. By forcing the model to answer simpler subquestions in separate contexts, we greatly increase the faithfulness of model-generated reasoning over CoT, while still achieving some of the performance gains of CoT.

---

## 66. Probabilistic Soundness Guarantees in LLM Reasoning Chains (ARES)
**Review status:** reviewed -> sheet 18-ares-soundness.md (round 5). Cross-paper discussion: pending.


**Cite:** Weiqiu You, Anton Xue, Shreya Havaldar, Delip Rao, Helen Jin, Chris Callison-Burch, Eric Wong. "Probabilistic Soundness Guarantees in LLM Reasoning Chains." 2025. EMNLP 2025. arXiv:2507.12948. https://arxiv.org/abs/2507.12948

**Targets:** F24 / I3 - scores each reasoning step using only previously-VERIFIED premises, giving a graded per-step soundness score with statistical guarantees rather than a brittle binary; excels specifically at detecting propagated errors on long chains.

**Abstract (verbatim, arXiv):**
> In reasoning chains generated by large language models (LLMs), initial errors often propagate and undermine the reliability of the final conclusion. Current LLM-based error detection methods often fail to detect propagated errors because earlier errors can corrupt judgments of downstream reasoning. To better detect such errors, we introduce Autoregressive Reasoning Entailment Stability (ARES), a probabilistic framework that evaluates each reasoning step based solely on previously-verified premises. This inductive method yields a nuanced score for each step and provides certified statistical guarantees of its soundness, rather than a brittle binary label. ARES achieves state-of-the-art performance across four benchmarks (72.1% Macro-F1, +8.2 points) and demonstrates superior robustness on very long synthetic reasoning chains, where it excels at detecting propagated errors (90.3% F1, +27.6 points).

---

## 67. Branch-Solve-Merge Improves Large Language Model Evaluation and Generation

**Cite:** Swarnadeep Saha, Omer Levy, Asli Celikyilmaz, Mohit Bansal, Jason Weston, Xian Li. "Branch-Solve-Merge Improves Large Language Model Evaluation and Generation." 2024. NAACL 2024. arXiv:2310.15123. https://arxiv.org/abs/2310.15123

**Targets:** F16 - genuine parallel decomposition (branch into different sub-tasks, solve independently, merge), as opposed to sample-and-vote; the merge step is explicit. Named in sheet 02's citation list as the parallel exemplar.

**Abstract (verbatim, arXiv):**
> Large Language Models (LLMs) are frequently used for multi-faceted language generation and evaluation tasks that involve satisfying intricate user constraints or taking into account multiple aspects and criteria. However, their performance can fall short, due to the model's lack of coherence and inability to plan and decompose the problem. We propose Branch-Solve-Merge (BSM), a Large Language Model program (Schlag et al., 2023) for tackling such challenging natural language tasks. It consists of branch, solve, and merge modules that are parameterized with specific prompts to the base LLM. These three modules plan a decomposition of the task into multiple parallel sub-tasks, independently solve them, and fuse the solutions to the sub-tasks. We apply our method to the tasks of LLM response evaluation and constrained text generation and evaluate its effectiveness with multiple LLMs, including Vicuna, LLaMA-2-chat, and GPT-4. BSM improves the evaluation correctness and consistency for each LLM by enhancing human-LLM agreement by up to 26%, reducing length and pairwise position biases by up to 50%, and allowing LLaMA2-chat to match or outperform GPT-4 on most domains. On a constraint story generation task, BSM improves the coherence of stories while also improving constraint satisfaction by 12%.

---

## 68. BeamAggR: Beam Aggregation Reasoning over Multi-source Knowledge for Multi-hop Question Answering

**Cite:** Zheng Chu, Jingchang Chen, Qianglong Chen, Haotian Wang, Kun Zhu, Xiyuan Du, Weijiang Yu, Ming Liu, et al. "BeamAggR: Beam Aggregation Reasoning over Multi-source Knowledge for Multi-hop Question Answering." 2024. ACL 2024. arXiv:2406.19820. https://arxiv.org/abs/2406.19820

**Targets:** F16 - the HTN-style (aggregate-all-leaves) tree that sheet 02 said the field lacks: parse the question into a tree of atom + composite questions, reason bottom-up, and at composite nodes combine beam candidates by probabilistic aggregation.

**Abstract (verbatim, arXiv):**
> Large language models (LLMs) have demonstrated strong reasoning capabilities. Nevertheless, they still suffer from factual errors when tackling knowledge-intensive tasks. Retrieval-augmented reasoning represents a promising approach. However, significant challenges still persist, including inaccurate and insufficient retrieval for complex questions, as well as difficulty in integrating multi-source knowledge. To address this, we propose Beam Aggregation Reasoning, BeamAggR, a reasoning framework for knowledge-intensive multi-hop QA. BeamAggR explores and prioritizes promising answers at each hop of question. Concretely, we parse the complex questions into trees, which include atom and composite questions, followed by bottom-up reasoning. For atomic questions, the LLM conducts reasoning on multi-source knowledge to get answer candidates. For composite questions, the LLM combines beam candidates, explores multiple reasoning paths through probabilistic aggregation, and prioritizes the most promising trajectory. Extensive experiments on four open-domain multi-hop reasoning datasets show that our method significantly outperforms SOTA methods by 8.5%. Furthermore, our analysis reveals that BeamAggR elicits better knowledge collaboration and answer aggregation.

---

## 69. MASAI: Modular Architecture for Software-engineering AI Agents

**Cite:** Daman Arora, Atharv Sonwane, Nalin Wadhwa, Abhav Mehrotra, Saiteja Utpala, Ramakrishna Bairi, Aditya Kanade, Nagarajan Natarajan. "MASAI: Modular Architecture for Software-engineering AI Agents." 2024. NeurIPS 2024. arXiv:2406.11638. https://arxiv.org/abs/2406.11638

**Targets:** F9 / F18 / code domain - decomposition by software-engineering sub-problem (localise / fix / rank ...) with a dedicated sub-agent per stage, each with its own strategy and context; explicitly motivated by avoiding long trajectories that inflate cost.

**Abstract (verbatim, arXiv):**
> A common method to solve complex problems in software engineering, is to divide the problem into multiple sub-problems. Inspired by this, we propose a Modular Architecture for Software-engineering AI (MASAI) agents, where different LLM-powered sub-agents are instantiated with well-defined objectives and strategies tuned to achieve those objectives. Our modular architecture offers several advantages: (1) employing and tuning different problem-solving strategies across sub-agents, (2) enabling sub-agents to gather information from different sources scattered throughout a repository, and (3) avoiding unnecessarily long trajectories which inflate costs and add extraneous context. MASAI enabled us to achieve the highest performance (28.33% resolution rate) on the popular and highly challenging SWE-bench Lite dataset consisting of 300 GitHub issues from 11 Python repositories. We conduct a comprehensive evaluation of MASAI relative to other agentic methods and analyze the effects of our design decisions and their contribution to the success of MASAI.

---

## 70. Beyond the Answer Key: Robustness Evaluation of Large Language Models for Step-Level Mathematical Verification
**Review status:** reviewed -> sheet 20-verifier-robustness.md (round 5). Cross-paper discussion: pending.


**Cite:** Fateme Mazdarani, Carlos Toxtli. "Beyond the Answer Key: Robustness Evaluation of Large Language Models for Step-Level Mathematical Verification." 2026. IEEE ICMLA 2026. arXiv:2608.28725. https://arxiv.org/abs/2608.28725

**Targets:** F27 / F17 - measures the LLM-as-verifier directly: models that grade canonical solution traces well collapse on perturbed-but-equivalent traces (false-rejection 75.6-85.3%). Evaluator robustness must be measured separately from solver accuracy. Echoes sheet 07's invariance failure.

**Abstract (verbatim, arXiv):**
> Large language models (LLMs) are increasingly used as graders, verifiers, and process auditors, but most mathematical evaluations still emphasize final-answer accuracy. This can obscure whether a model can verify a non-canonical but valid solution trace. We introduce a controlled linear-equation benchmark for evaluating LLMs in the evaluator role. Each instance asks the model to judge final-answer correctness, step-level trace correctness, and the first incorrect step. Our evaluation of state-of-the-art open LLMs reveals a significant robustness gap: models that accurately evaluate canonical solutions often fail when presented with perturbed but logically equivalent variants. Across GPT-OSS 20B, Qwen3-14B, and Phi-4-Reasoning, base models perform well on canonical traces but degrade substantially on perturbed traces, especially for error localization. On valid perturbed traces, base-model false-rejection rates reach 75.6-85.3%, showing strong sensitivity to canonical solution form. Supervised fine-tuning, distillation, and test-time compute improve robustness in some settings, but gains are model dependent and can trade off against canonical performance. The results show that reliable process-level verification remains challenging, and evaluator robustness should be measured separately from solver accuracy, even in a simple algebraic domain with exact ground truth.

---

## 71. TinyV: Reducing False Negatives in Verification Improves RL for LLM Reasoning

**Cite:** Zhangchen Xu, Yuetai Li, Fengqing Jiang, Bhaskar Ramasubramanian, Luyao Niu, Bill Yuchen Lin, Radha Poovendran. "TinyV: Reducing False Negatives in Verification Improves RL for LLM Reasoning." 2025. arXiv:2505.14625 (preprint). https://arxiv.org/abs/2505.14625

**Targets:** F27 - quantifies verifier unreliability from the other side: over 38% of correct model outputs in a 'verified' math dataset are wrongly rejected; false negatives starve training of gradient signal. A concrete false-reject magnitude for the accept/reject port.

**Abstract (verbatim, arXiv):**
> Reinforcement Learning (RL) has become a powerful tool for enhancing the reasoning abilities of large language models (LLMs) by optimizing their policies with reward signals. Yet, RL's success relies on the reliability of rewards, which are provided by verifiers. In this paper, we expose and analyze a widespread problem--false negatives--where verifiers wrongly reject correct model outputs. Our in-depth study of the Big-Math-RL-Verified dataset reveals that over 38% of model-generated responses suffer from false negatives, where the verifier fails to recognize correct answers. We show, both empirically and theoretically, that these false negatives severely impair RL training by depriving the model of informative gradient signals and slowing convergence. To mitigate this, we propose tinyV, a lightweight LLM-based verifier that augments existing rule-based methods, which dynamically identifies potential false negatives and recovers valid responses to produce more accurate reward estimates. Across multiple math-reasoning benchmarks, integrating TinyV boosts pass rates by up to 10% and accelerates convergence relative to the baseline.

---

## 72. CoRefine: Confidence-Guided Self-Refinement for Adaptive Test-Time Compute

**Cite:** Chen Jin, Ryutaro Tanno, Tom Diethe, Philip Teare. "CoRefine: Confidence-Guided Self-Refinement for Adaptive Test-Time Compute." 2026. arXiv:2602.08948 (preprint). https://arxiv.org/abs/2602.08948

**Targets:** F24 / I3 - a tiny frozen-LLM controller reads full-trace confidence to decide halt / re-examine / switch approach; 92.6% precision when it confidently halts, and it is pitched as a modular recovery primitive for 'agentic settings with imperfect verifiers'.

**Abstract (verbatim, arXiv):**
> Large Language Models (LLMs) often rely on test-time scaling via parallel decoding (for example, 512 samples) to boost reasoning accuracy, but this incurs substantial compute. We introduce CoRefine, a confidence-guided self-refinement method that achieves competitive accuracy using a fraction of the tokens via a lightweight 211k-parameter Conv1D controller atop a frozen LLM. The controller consumes full-trace confidence to decide whether to halt, re-examine, or try a different approach, enabling targeted self-correction with an average of 2.7 refinement steps per problem and roughly 190-fold token reduction relative to 512-sample baselines. Across diverse reasoning benchmarks and three open-source models, the controller achieves 92.6 percent precision when it confidently halts, indicating that confidence dynamics reliably signal correctness without ground-truth verification. We extend this to CoRefine-Tree, a hybrid sequential-parallel variant that adaptively balances exploration and exploitation, with easy serving integration and verifier compatibility. By treating confidence as a control signal rather than a correctness guarantee, CoRefine provides a modular primitive for scalable reasoning and agentic settings with imperfect verifiers.

---

## 73. Adaptive Stopping for Multi-Turn LLM Reasoning (MiCP)

**Cite:** Xiaofan Zhou, Huy Nguyen, Bo Yu, Chenxi Liu, Lu Cheng. "Adaptive Stopping for Multi-Turn LLM Reasoning." 2026. arXiv:2604.01413 (preprint). https://arxiv.org/abs/2604.01413

**Targets:** F21 - a conformal-prediction framework that allocates a distinct error budget per turn so the loop can stop early with an overall coverage guarantee; a formal alternative to heuristic stopping rules and fixed turn budgets.

**Abstract (verbatim, arXiv):**
> Large Language Models (LLMs) increasingly rely on multi-turn reasoning and interaction, such as adaptive retrieval-augmented generation (RAG) and ReAct-style agents, to answer difficult questions. These methods improve accuracy by iteratively retrieving information, reasoning, or acting, but introduce a key challenge: When should the model stop? Existing approaches rely on heuristic stopping rules or fixed turn budgets and provide no formal guarantees that the final prediction still contains the correct answer. This limitation is particularly problematic in high-stakes domains such as finance and healthcare, where unnecessary turns increase cost and latency, while stopping too early risks incorrect decisions. Conformal prediction (CP) provides formal coverage guarantees, but existing LLM-CP methods only apply to a single model output and cannot handle multi-turn pipelines with adaptive stopping. To address this gap, we propose Multi-Turn Language Models with Conformal Prediction (MiCP), the first CP framework for multi-turn reasoning. MiCP allocates different error budgets across turns, enabling the model to stop early while maintaining an overall coverage guarantee. We demonstrate MiCP on adaptive RAG and ReAct, where it achieves the target coverage on both single-hop and multi-hop question answering benchmarks while reducing the number of turns, inference cost, and prediction set size.

---

## 74. Composition Collapse: Stable Factual Knowledge Does Not Imply Compositional Reasoning

**Cite:** Zhe Yu, Wenpeng Xing, Yunzhao Wei, Jie Chen, Hongzhi Wang, Xuyang Teng, Meng Han. "Composition Collapse: Stable Factual Knowledge Does Not Imply Compositional Reasoning." 2026. arXiv:2605.26789 (preprint). https://arxiv.org/abs/2605.26789

**Targets:** F13 / F25 - recipes with indistinguishable atomic knowledge differ by 40+ points on composition, and aggregate metrics hide it; a 'double-gate' protocol conditions on stable atomic access and finds much of the residual failure is generation-time computation constraint, not permanent inability.

**Abstract (verbatim, arXiv):**
> Post-training is routinely evaluated through aggregate benchmark scores that treat multi-hop reasoning as a single capability -- as if a model that answers more questions correctly must be better at assembling facts. We show that this assumption can be misleading: recipes with statistically indistinguishable atomic knowledge produce composition behaviour separated by over 40 percentage points, a phenomenon we call composition collapse: the systematic failure to assemble stably-known facts into chains, invisible to aggregate metrics. We introduce a double-gate protocol that changes the estimand from an aggregate compositionality gap to residual composition failure conditioned on stable atomic access, decomposing post-training gains into three independent channels: atomic stability, residual composition, and critical depth. On a benchmark of temporal factual chains spanning depths 2--11 across four post-training recipes, this decomposition reveals that post-training objectives shift composition capability in directions that aggregate metrics mask, and suggests that claims about multi-hop reasoning improvement should be accompanied by atomic-gate-controlled composition metrics. Diagnostic probes further show that a substantial share of measured composition failure reflects generation-time computation constraints rather than permanent inability to compose.

---

## 75. Multi-Hop Knowledge Composition is Bound by Pretraining Exposure

**Cite:** Yannis Karmim, Luis Marti, Djame Seddah, Valentin Barriere. "Multi-Hop Knowledge Composition is Bound by Pretraining Exposure." 2026. arXiv:2606.09338 (preprint). https://arxiv.org/abs/2606.09338

**Targets:** F13 / F25 - a controlled follow-up to the compositionality gap: composition failure persists at 97% 1-hop accuracy, and data augmentation transfers composition only to individuals that appeared in compositional pretraining contexts - never to a held-out population.

**Abstract (verbatim, arXiv):**
> Large Language Models fail at implicit multi-hop reasoning: a model answers "When was X born?" and "Who is Y's closest friend?" correctly but fails on "When was Y's closest friend born?" in a single forward pass, even when both facts are perfectly memorized and individually retrievable. We study this failure in a controlled natural language setting with a strict separation between individuals exposed to compositional contexts during pretraining and those that never appear in any such context. We confirm that compositional failure persists even at 97% 1-hop accuracy, establishing the gap as a pretraining failure rather than a knowledge absence. We propose and test nine data-centric augmentation formats and find that compositional pretraining transfers to unseen questions for exposed individuals, but never to individuals absent from compositional pretraining, suggesting that exposure to compositional contexts during pretraining is a necessary condition for implicit multi-hop reasoning.

---

## 76. Hallucination Cascade: Analyzing Error Propagation in Multi-Agent LLM Systems

**Cite:** Saeid Jamshidi, Arghavan Moradi Dakhel, Kawser Wazed Nafi, Foutse Khomh. "Hallucination Cascade: Analyzing Error Propagation in Multi-Agent LLM Systems." 2026. arXiv:2606.07937 (preprint). https://arxiv.org/abs/2606.07937

**Targets:** F24 - tracks claim-level factual inconsistency across sequential agent hops: 500 cascades, 3-agent chains show net ATTENUATION of hallucination (0.422 -> 0.272) at a small cost in factual accuracy - a measured recovery-vs-preservation trade-off, i.e. an empirical read on c and epsilon.

**Abstract (verbatim, arXiv):**
> Large Language Models (LLMs) generate fluent text but remain vulnerable to hallucinations, producing unsupported, inconsistent, and factually incorrect claims. Most prior work treats hallucination as a static property of isolated outputs. In multi-agent LLM systems, however, responses are exchanged across agents, revised through sequential stages, and reused as context for later reasoning. Hallucination, therefore, becomes a dynamic process shaped by interaction history, cascade depth, and model heterogeneity. This paper analyzes hallucination dynamics in multi-agent LLM cascades by tracking claim-level factual inconsistencies across sequential agent interactions. We conduct 500 cascade experiments across 10 knowledge domains using GPT-5.3, DeepSeek-V3, and LLaMA-3-70B-Instruct, yielding 1,250 evaluated responses. Results show that deeper cascades reduce the normalized hallucination score from 0.422 at the first agent to 0.272 at the final agent in 3-agent chains, with an amplification factor of 0.644, indicating net attenuation. This reduction is accompanied by a decline in factual accuracy from 0.789 to 0.769, revealing a trade-off between hallucination suppression and factual preservation. Transition-level analysis shows that each agent-to-agent refinement reduces hallucination by an average of 0.072, with small but consistent losses in factual consistency and response quality.

---

## 77. Token Economics for LLM Agents: A Dual-View Study from Computing and Economics

**Cite:** Yuxi Chen, Junming Chen, Chenyu He, Yiwei Li, Yicheng Ji, Yifan Wu, Dingyu Yang, Lansong Diao, et al. "Token Economics for LLM Agents: A Dual-View Study from Computing and Economics." 2026. arXiv:2605.09104 (survey preprint). https://arxiv.org/abs/2605.09104

**Targets:** F22 / I1 (survey) - a four-level taxonomy (single agent / multi-agent / ecosystem / security) of the output-quality-vs-token-cost trade-off; the closest thing to a systematic map of what is known about the cost side.

**Abstract (verbatim, arXiv):**
> As LLM agents evolve, tokens have emerged as the core economic primitives of Agentic AI. However, their exponential consumption introduces severe computational, collaborative, and security bottlenecks. Current surveys remain fragmented across system optimization, architecture design, and trust, lacking a unified framework to evaluate the fundamental trade-off between output quality and economic cost. To bridge this gap, this survey presents the first comprehensive survey of Token Economics. By unifying computer science and economics, we conceptualize tokens as production factors, exchange mediums, and units of account. We synthesize existing literature across a four-dimensional taxonomy: (1) Micro-level (Single Agent): Optimizing budget-constrained factor substitution via neoclassical firm theory. (2) Meso-level (Multi-Agent Systems): Minimizing collaboration friction using transaction cost and principal-agent theories. (3) Macro-level (Agent Ecosystems): Addressing congestion externalities and pricing via mechanism design. (4) Security: Internalizing adversarial threats as endogenous economic constraints. Finally, we outline frontier directions, including differentiable token budgets and dynamic markets.

---

## 78. Cut the Crap: An Economical Communication Pipeline for LLM-based Multi-Agent Systems (AgentPrune)

**Cite:** Guibin Zhang, Yanwei Yue, Zhixun Li, Sukwon Yun, Guancheng Wan, Kun Wang, Dawei Cheng, Jeffrey Xu Yu, et al. "Cut the Crap: An Economical Communication Pipeline for LLM-based Multi-Agent Systems." 2024. arXiv:2410.02506 (preprint). https://arxiv.org/abs/2410.02506

**Targets:** F22 - names and measures 'communication redundancy' in multi-agent pipelines and prunes it: comparable results at $5.6 vs $43.7, with 28-73% token reduction. A concrete decomposition-coordination cost number and a lever on it.

**Abstract (verbatim, arXiv):**
> Recent advancements in large language model (LLM)-powered agents have shown that collective intelligence can significantly outperform individual capabilities, largely attributed to the meticulously designed inter-agent communication topologies. Though impressive in performance, existing multi-agent pipelines inherently introduce substantial token overhead, as well as increased economic costs, which pose challenges for their large-scale deployments. In response to this challenge, we propose an economical, simple, and robust multi-agent communication framework, termed AgentPrune, which can seamlessly integrate into mainstream multi-agent systems and prunes redundant or even malicious communication messages. Technically, AgentPrune is the first to identify and formally define the communication redundancy issue present in current LLM-based multi-agent pipelines, and efficiently performs one-shot pruning on the spatial-temporal message-passing graph, yielding a token-economic and high-performing communication topology. Extensive experiments across six benchmarks demonstrate that AgentPrune (I) achieves comparable results as state-of-the-art topologies at merely $5.6 cost compared to their $43.7, (II) integrates seamlessly into existing multi-agent frameworks with 28.1%-72.8% token reduction, and (III) successfully defends against two types of agent-based adversarial attacks with 3.5%-10.8% performance boost.

---

## 79. D-CORE: Incentivizing Task Decomposition in Large Reasoning Models for Complex Tool Use

**Cite:** Bowen Xu, Shaoyu Wu, Hao Jiang, Kai Liu, Xin Chen, Lulu Hu, Bin Yang. "D-CORE: Incentivizing Task Decomposition in Large Reasoning Models for Complex Tool Use." 2026. arXiv:2602.02160 (preprint). https://arxiv.org/abs/2602.02160

**Targets:** F1 / F30 - claims current large reasoning models LACK sub-task decomposition in complex tool use ('Lazy Reasoning') and have to be trained back into it; the counter-signal to 'decomposition benefit just decays with capability'.

**Abstract (verbatim, arXiv):**
> Effective tool use and reasoning are essential capabilities for large reasoning models (LRMs) to address complex real-world problems. Through empirical analysis, we identify that current LRMs lack the capability of sub-task decomposition in complex tool use scenarios, leading to Lazy Reasoning. To address this, we propose a two-stage training framework D-CORE (Decomposing tasks and Composing Reasoning processes) that first incentivize the LRMs' task decomposition reasoning capability via self-distillation, followed by diversity-aware reinforcement learning (RL) to restore LRMs' reflective reasoning capability. D-CORE achieves robust tool-use improvements across diverse benchmarks and model scales. Experiments on BFCLv3 demonstrate superiority of our method: D-CORE-8B reaches 77.7% accuracy, surpassing the best-performing 8B model by 5.7%. Meanwhile, D-CORE-14B establishes a new state-of-the-art at 79.3%, outperforming 70B models despite being 5x smaller.

---

## 80. PLANET: A Collection of Benchmarks for Evaluating LLMs' Planning Capabilities

**Cite:** Haoming Li, Zhaoliang Chen, Jonathan Zhang, Fei Liu. "PLANET: A Collection of Benchmarks for Evaluating LLMs' Planning Capabilities." 2025. arXiv:2504.14773 (preprint). https://arxiv.org/abs/2504.14773

**Targets:** F26 / I4 - a survey/audit of planning benchmarks across embodied, web, scheduling, games, and everyday automation; maps which testbeds exist and where the gaps are for evaluating a plan/decomposition rather than an outcome.

**Abstract (verbatim, arXiv):**
> Planning is central to agents and agentic AI. The ability to plan, e.g., creating travel itineraries within a budget, holds immense potential in both scientific and commercial contexts. Moreover, optimal plans tend to require fewer resources compared to ad-hoc methods. To date, a comprehensive understanding of existing planning benchmarks appears to be lacking. Without it, comparing planning algorithms' performance across domains or selecting suitable algorithms for new scenarios remains challenging. In this paper, we examine a range of planning benchmarks to identify commonly used testbeds for algorithm development and highlight potential gaps. These benchmarks are categorized into embodied environments, web navigation, scheduling, games and puzzles, and everyday task automation. Our study recommends the most appropriate benchmarks for various algorithms and offers insights to guide future benchmark development.

---

## 81. AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering

**Cite:** Rajesh Kumar, Waqar Ali, Junaid Ahmed, Najma Imtiaz Ali, Shaban Usman. "AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering." 2026. arXiv:2604.13120 (preprint). https://arxiv.org/abs/2604.13120

**Targets:** F17 / F27 / F9 / code domain - makes sandboxed execution a precondition for propagating any sub-result ('execution-grounded verification'); ablations claim execution feedback and role decomposition each independently drive the gain. Preprint, unproven venue.

**Abstract (verbatim, arXiv):**
> Large language models generate plausible code but cannot verify correctness. Existing multi-agent systems simulate execution or leave verification optional. We introduce execution-grounded verification as a first-class principle: every code change must survive sandboxed execution before propagation. We instantiate this principle in AGENTFORGE, a multi-agent framework where Planner, Coder, Tester, Debugger, and Critic agents coordinate through shared memory and a mandatory Docker sandbox. We formalize software engineering with LLMs as an iterative decision process over repository states, where execution feedback provides a stronger supervision signal than next-token likelihood. AGENTFORGE achieves 40.0% resolution on SWE-BENCH Lite, outperforming single-agent baselines by 26-28 points. Ablations confirm that execution feedback and role decomposition each independently drive performance.

---

## 2. Selected for review

Four picks, chosen for **spread across approach and claim**, not proximity to the
Subject's framing. Each has its own sheet in this folder.

1. **`01` — To CoT or not to CoT? (Sprague et al., ICLR 2025).** Inventory entry
   17, flagged ADJACENT — picked deliberately over closer papers as *the* boundary
   case: a two-stream meta-analysis of the cheapest possible "split into steps"
   intervention, finding its benefit narrow. Read as an invitation to reconsider
   the angle rather than confirm it.
2. **`02` — Test-time Scaling of LLMs: A Survey from A Subproblem Structure
   Perspective (Yang et al., 2025).** Inventory entry 60. A lens paper: organises
   the whole inference-time design space by subproblem *topology* (sequential /
   parallel / tree). No measurement — chosen for the framing, and for spread away
   from the method papers.
3. **`03` — Large Language Models for Planning: A Comprehensive and Systematic
   Survey (Cao et al., 2025).** Inventory entry 61. The widest catalogue in the
   set; taxonomy cut by *what gets changed* (external module / finetuning /
   inference procedure), with decomposition placed both definitionally and as one
   inference-time family. Chosen for coverage and for its different organising
   axis from `02`.
4. **`04` — Select-Then-Decompose (Liu et al., EMNLP 2025).** Inventory entry 1.
   The one paper that measures the *decide-to-split* decision itself, with token
   and API cost promoted to a co-equal dependent variable. Method + empirical
   analysis; the closest to the Subject, included as the on-target anchor of the
   spread.

### Round 2

Chosen to fill what round 1 left thin: the **how-deep** half of the title, the
**failure-triggered** split rule, a **formal** account of what steps buy, and a
**skeptical** frontier-model read. Drawn from the inventory and from citations the
round-1 sheets flagged for chasing (ADaPT was named by both `03` and `04`).

5. **`05` — ADaPT: As-Needed Decomposition and Planning (Prasad et al., Findings
   of NAACL 2024).** Inventory entry 2. Recursive decomposition triggered only
   when the executor *fails* a sub-task; depth emerges from task complexity and
   executor capability. The method anchor — the conditional-split rule round 1
   never reviewed. Cited as a next-read by `03` and `04`.
6. **`06` — The Expressive Power of Transformers with Chain of Thought (Merrill &
   Sabharwal, ICLR 2024).** Inventory entry 42. Complexity-theory: how a decoder's
   expressive power scales with the *number* of intermediate steps (log ≈ little;
   linear → regular languages; polynomial → P). The formal how-deep ceiling, and
   a proof rather than a benchmark — maximum spread. Round 1 leaned on this class
   of result without checking it.
7. **`07` — Decomposed Prompting Does Not Fix Knowledge Gaps, But Helps Models Say
   "I Don't Know" (Madhwal et al., Findings of ACL 2026).** Inventory entry 37.
   Controlled three-regime comparison: decomposition's accuracy gain *diminishes*
   in frontier models, but cross-regime disagreement is a precise uncertainty
   signal usable for training-free abstention. The strongest "decomposition does
   not do what you think" claim in the set; spread on claim, complements `01`.
8. **`08` — When More is Less: Understanding Chain-of-Thought Length in LLMs (Wu
   et al., preprint).** Inventory entry 29, flagged PREPRINT. Task accuracy
   follows an inverted-U in CoT length; the optimal length grows with task
   difficulty and shrinks with model capability. The most central inventory item
   on the how-deep axis — admitted with its status noted.

### Round 3

Chosen to fill the two axes eight sheets left at zero coverage: **recombination**
(how sub-results are put back together, flagged as under-addressed by nearly every
sheet) and **coordination / sub-agent cost** (the Subject names deep sub-agent
hierarchies; no sheet touches them).

9. **`09` — Measuring and Narrowing the Compositionality Gap (Press et al.,
   Findings of EMNLP 2023).** Inventory entry 11. Defines and measures the
   *compositionality gap*: how often a model answers every sub-question correctly
   yet fails to compose the final answer. The recombination-failure measurement
   the set is missing. Older model cohort (GPT-3 family) — read for the construct,
   not the magnitudes.
10. **`10` — Divide-or-Conquer? Which Part Should You Distill Your LLM? (Wu et
    al., Findings of EMNLP 2024).** Inventory entry 9. Splits reasoning into a
    decomposition phase and a solving phase, distils each separately, and measures
    reasoning outcome *and* inference cost. Directly on the cheap-planner /
    strong-executor question ([[F1]] territory, sheet `04` Takeaway III) and on
    [[F9]].
11. **`11` — Chain of Agents (Zhang et al., NeurIPS 2024).** Inventory entry 10.
    Segments a long input across sequential worker agents, then a manager agent
    synthesises their contributions — sub-agent decomposition with an explicit
    recombination stage and a per-agent bounded context, which is close to the
    [[A1]] shape.
12. **`12` — Why Do Multi-Agent LLM Systems Fail? (Cemri et al., NeurIPS 2025).**
    Inventory entry 19, flagged ADJACENT. A failure taxonomy (MAST, 14 modes in 3
    categories) built from 1,600+ annotated multi-agent traces. The analysis-kind
    pick — where sub-agent decomposition breaks, and how coordination cost shows
    up as failure.

### Round 4

Chosen against the gaps F13-F23 leave open: recombination as a first-class problem
with a verifier, an instrument for decomposition quality, the empirical grounding
two sheets already lean on, and the canonical method never read.

13. **`13` - Faith and Fate: Limits of Transformers on Compositionality (Dziri et
    al., NeurIPS 2023).** Inventory entry 28, flagged ADJACENT. The empirical
    bridge sheets `05` and `06` both cite: transformers reportedly solve
    compositional tasks by "linearised subgraph matching," and accuracy decays
    with the depth of the computation graph. Grounds the compounding-error
    mechanism ([[F16]], [[F20]]) and the "why decompose at all" premise.
14. **`14` - Cumulative Reasoning with Large Language Models (Zhang et al., TMLR).**
    Inventory entry 54. Proposer / Verifier / Reporter over a DAG of
    verifier-passed propositions - filtered recombination as a built method, the
    constructive side of [[F13]] and [[F17]].
15. **`15` - TaskBench: Benchmarking LLMs for Task Automation (Shen et al., NeurIPS
    2024 Datasets & Benchmarks).** Inventory entry 15. Scores task decomposition
    as one of three explicit stages via a Tool Graph and Edge F1 - the instrument
    for decomposition quality that [[F17]] and sheet `03` say the field lacks.
16. **`16` - Decomposed Prompting: A Modular Approach for Solving Complex Tasks
    (Khot et al., ICLR 2023).** Inventory entry 3, a 2023 anchor. The canonical
    modular recursive decomposition, named as a next-read by sheets `01`, `04`,
    `09`, `11` and as ADaPT's direct predecessor. Recurses on hard sub-tasks and
    on input length - direct prior art for [[A1]].

### Round 5 (probably the last for now)

Chosen to close the highest-value gaps the F13-F32 findings leave: A1's aggregator
term, the recovery instrument F24 needs, the "do less" counter-case plus the code
domain, and the accept/reject port's reliability.

17. **`17` - When Does Divide and Conquer Work for Long Context LLM? A Noise
    Decomposition Framework (Xu et al., ICLR 2026).** Entry 64. A theory that
    splits failure into task / model / *aggregator* noise and derives when
    chunk-and-aggregate beats a strong single shot - the recombination-cost term
    [[A1]] and every recombination finding ([[F13]]) have lacked.
18. **`18` - Probabilistic Soundness Guarantees in LLM Reasoning Chains / ARES
    (You et al., EMNLP 2025).** Entry 66. Per-step soundness scored from only
    previously-verified premises, with statistical guarantees, strong on
    *propagated* errors - the concrete instrument for [[F24]] / [[I3]] (measuring
    and raising the recovery rate).
19. **`19` - Agentless: Demystifying LLM-based Software Engineering Agents (Xia et
    al., 2024).** Entry 63. A fixed three-phase pipeline with no autonomous
    planning beats decomposed SE agents at ~1/60th the cost - the sharpest "maybe
    do not decompose" case, in the project's own domain, on the cost axis
    ([[F22]], [[F1]], [[F10]]).
20. **`20` - Beyond the Answer Key: Robustness Evaluation of LLMs for Step-Level
    Mathematical Verification (Mazdarani & Toxtli, ICMLA 2026).** Entry 70.
    Measures the LLM-as-verifier directly: 75-85% false-rejection on
    equivalent-but-perturbed traces. The accept/reject port's reliability
    ([[F27]], [[F17]]), and a hard echo of sheet `07`'s invariance failure.

## 3. Labels (second pass)

Richer than the inventory's inline flag: each line adds a *kind* and a one-line
reason. Entries 1-58 from the labelling pass; 59-61 (surveys added in the fifth
gather round) appended here.

# Labels — When to Decompose, and How Deep

1 | RELATED | analysis | Empirically analyses what drives task-decomposition performance and cost and proposes an adaptive strategy for selecting a decomposition approach — squarely the Subject's decide-to-split and cost axes.
2 (ADaPT) | RELATED | method | Recursively decomposes sub-tasks only when the LLM fails to execute them, with depth emerging at runtime from task complexity and model capability — two of the Subject's core axes.
3 (DecomP) | RELATED | method | Decomposes a task into a library of modular sub-task prompts, recursing on hard sub-tasks and on long inputs — a canonical modular-decomposition method.
4 (Least-to-Most) | RELATED | method | Breaks a problem into an upfront ordered list of simpler subproblems solved in sequence with earlier answers fed forward — a foundational decompose-then-solve scheme.
5 (Plan-and-Solve) | RELATED | method | Zero-shot prompting that first devises a plan dividing the task into subtasks and then carries them out — the minimal upfront-plan form of decomposition.
6 (Tree of Thoughts) | ADJACENT | method | Splits solving into intermediate thought steps with search and backtracking, but as reasoning-path exploration rather than sub-objectives executed separately and recombined.
7 (Graph of Thoughts) | ADJACENT | method | Models reasoning as an arbitrary graph with aggregation and refinement nodes, touching recombination and cost but framed as reasoning topology rather than task-into-subtask delegation.
8 (HuggingGPT) | RELATED | method | An explicit LLM planning stage parses a request into a dependency-ordered task list dispatched to expert models and then summarised — a fixed multi-stage decomposition pipeline.
9 (Divide-or-Conquer) | RELATED | analysis | Separates a decomposition phase from a solving phase and studies distilling each, measuring effects on reasoning outcomes and inference cost — directly on the split/execute/cost structure.
10 (Chain of Agents) | RELATED | method | Segments a long input across sequential worker agents whose contributions a manager agent synthesises — splitting work among sub-agents with an explicit recombination step.
11 (self-ask) | RELATED | measurement | Defines and measures the compositionality gap between answering sub-problems and composing them, and introduces self-ask which decomposes a question into explicit follow-up sub-questions.
12 (LLMCompiler) | RELATED | method | A planner formulates an execution plan decomposing a task into function-calling sub-tasks dispatched in parallel, explicitly targeting the latency and cost of coordination.
13 (DELTA) | RELATED | method | Uses an LLM to decompose long-horizon goals into a sequence of sub-goals handed to automated task planners — decomposition and sub-goal sequencing in a robotics setting.
14 (Self-Planning Code Gen) | RELATED | method | A planning phase decomposes the intent into formatted steps that guide a separate implementation phase — a two-phase decompose-then-execute method for code generation.
15 (TaskBench) | RELATED | measurement | Benchmarks LLMs on task automation with task decomposition as one of three explicitly evaluated stages, using a Tool Graph representation and dedicated metrics.
16 (TPTU-v2) | ADJACENT | method | Improves task planning and tool usage in real systems via API retrieval, finetuning and demo selection, touching sub-task ordering but not the decision or depth of decomposition.
17 (To CoT or not to CoT) | ADJACENT | analysis | Meta-analysis of when added reasoning helps, separating planning from execution and arguing for selective use to save cost — the neighbouring when-is-extra-structure-worth-it question.
18 (Parsel) | RELATED | method | Decomposes algorithmic tasks into hierarchical natural-language function descriptions and searches over implementations validated by tests — explicit hierarchical decomposition with recombination.
19 (Why Do Multi-Agent LLM Systems Fail) | ADJACENT | analysis | Builds a failure taxonomy for multi-agent systems, bearing on the coordination cost and risks of sub-agent decomposition but not on when or how deep to split.
20 (Survey of Task Planning with LLMs) | ADJACENT | survey | Surveys LLM task planning broadly, the wider body the Subject sits within, treating decomposition as one component rather than the focus.
21 (MapCoder) | RELATED | method | Organises competitive code generation as a pipeline of specialised agents (retrieval, planning, coding, debugging) — a fixed multi-stage decomposition of the task across sub-agents.
22 (Successive Prompting) | RELATED | method | Iteratively breaks off one simple sub-question, answers it, and repeats, separating decomposition supervision from answering — a pre-2023 anchor for decomposition prompting.
23 (Self-Discover) | ADJACENT | method | Has the LLM self-compose a reasoning structure from atomic reasoning modules, which structures the reasoning rather than splitting into sub-objectives executed and recombined.
24 (RAP) | ADJACENT | method | Casts reasoning as planning with a world model and MCTS over reasoning steps — search-based planning that neighbours, but is not itself, task-into-subtask decomposition.
25 (Compound AI Systems Optimization Survey) | ADJACENT | survey | Surveys optimisation of compound AI systems, the broader family the Subject names, without centring the decomposition decision or its depth.
26 (Problem Decomposition Guided by Reasoning Utility) | RELATED | method | Decomposes complex reasoning problems using a reasoning-utility criterion to decide the decomposition — directly the Subject's what-decides-whether-to-split axis.
27 (Long-Form QA Reflection with Question Decomposition) | RELATED | method | Centres question decomposition, combined with a reflection step, to answer long-form questions — squarely a decomposition method in a QA setting.
28 (Faith and Fate) | ADJACENT | analysis | Studies transformer limits on compositional tasks that require breaking problems into sub-steps and synthesising them, with evidence and theory that accuracy decays as task complexity grows rather than addressing the split/recombine decision.
29 (When More is Less: CoT length) | RELATED | analysis | Shows task accuracy follows an inverted-U in chain-of-thought length with an optimal depth that grows with task difficulty and shrinks with model capability, directly the how-deep axis.
30 (How does CoT decompose complex tasks) | RELATED | theory | Models chain-of-thought as tree-structured decomposition and identifies a critical degree threshold below which splitting hurts and above which an optimal depth minimises error, squarely when-to-split and how-deep.
31 (ARIES) | RELATED | method | Multi-agent thought-graph system where reasoning agents solve decomposed subproblems while policy agents dynamically adapt the strategy, with a failure analysis pointing at the depth of problem decomposition.
32 (CARD) | RELATED | method | Predicts problem complexity before generation and adapts both the number of decomposition steps and a per-step thought budget, directly the what-sets-the-depth axis.
33 (Halo / Limited Reasoning Space) | RELATED | analysis | Argues over-planning collapses test-time performance and that there is an optimal compute/planning range, proposing dynamic regulation of planning at the reasoning boundary, the depth/cost boundary stated directly.
34 (RSA) | ADJACENT | method | A recursive self-aggregation scheme that recombines subsets of candidate reasoning chains across iterations, touching recombination as a lever but proposing a method rather than studying the split decision.
35 (IRCoT) | RELATED | method | Interleaves chain-of-thought decomposition steps with retrieval so each sub-question is grounded before the next, decomposition interleaved with execution.
36 (RoHT) | RELATED | method | Builds an explicit hierarchical question-decomposition tree and reasons over it root-to-leaf, aggregating heterogeneous knowledge at each level, decomposition structure plus recombination.
37 (Decomposition as reliability probe) | RELATED | analysis | Controlled comparison of direct vs decomposed prompting regimes finding the accuracy gains from decomposition vanish in frontier models and its main residual value is error detection and abstention, a skeptical read on when splitting pays.
38 (PlanBench) | ADJACENT | measurement | A planning benchmark from the classical-planning community covering plan generation, cost-optimal planning and verification, the wider planning body the Subject sits within rather than the split decision.
39 (NATURAL PLAN) | ADJACENT | measurement | A natural-language planning benchmark (trip/meeting/calendar) where performance collapses as constraint complexity grows, neighbouring planning evaluation rather than decomposition depth.
40 (Tree-Planner) | RELATED | method | Reframes planning as one plan-sampling call plus many grounded-deciding calls over an aggregated action tree, with an explicit token-cost and error-correction argument, decomposition granularity weighed against cost.
41 (Li et al. CoT expressiveness) | RELATED | theory | Proves that adding T intermediate reasoning steps lets constant-depth transformers solve anything computable by size-T circuits, the positive computational-power case for decomposing into steps.
42 (Merrill and Sabharwal CoT power) | RELATED | theory | Characterises how the computational power of a transformer grows with the number of chain-of-thought steps (log vs linear vs polynomial), the how-deep axis from an expressiveness angle.
43 (MetaGPT) | RELATED | method | Encodes software-team SOPs as agent roles, decomposing a complex task hierarchically across Product/Architect/Engineer/QA agents with a recombination pipeline and intermediate verification.
44 (AutoGen) | ADJACENT | other | A framework for composing multi-agent conversations that enables role decomposition as infrastructure but does not study when or how deeply to split.
45 (ChatDev) | RELATED | method | Decomposes software development into fixed waterfall phases (design/code/test) executed by role agents communicating via chat chains, a fixed multi-stage decomposition.
46 (AgentVerse) | ADJACENT | method | A multi-agent framework that dynamically adjusts group composition during a task, touching how many agents to involve but not the decision or depth of task splitting.
47 (CAMEL) | ADJACENT | method | Role-playing framework that splits a task between two communicating agents via inception prompting, a decomposition pattern rather than a study of its limits.
48 (LLM-Planner) | RELATED | method | Uses an LLM to decompose a natural-language goal into subgoals for an embodied agent with closed-loop re-planning on perception feedback, hierarchical decomposition with re-planning.
49 (DEPS) | RELATED | method | Iterative Describe/Explain/Plan/Select decomposition with a trainable selector that ranks candidate subgoals by estimated completion cost, decomposition plus cost-aware subgoal ordering.
50 (SwiftSage) | ADJACENT | method | Dual-process agent whose slow module does subgoal planning and decomposition; the contribution is the fast/slow switching rather than a depth rule.
51 (Huang et al. LLM zero-shot action planning) | RELATED | method | Pre-2023 anchor showing large LLMs zero-shot decompose high-level tasks into mid-level action sequences without training, foundational for the decomposition-for-agents line.
52 (Skeleton-of-Thought) | RELATED | method | Decomposes an answer into a skeleton of independent points expanded in parallel, explicitly targeting generation latency, parallel decomposition with a cost motivation.
53 (Buffer of Thoughts) | ADJACENT | method | Retrieves and instantiates reusable high-level thought-templates for reasoning, a store of decomposition structures rather than a when/how-deep rule.
54 (Cumulative Reasoning) | RELATED | method | Orchestrates Proposer/Verifier/Reporter roles to decompose a task, validate intermediate steps, and compose them into a solution via a DAG of verified propositions, decomposition plus filtered recombination.
55 (ReAct) | ADJACENT | method | Anchor agent loop interleaving reasoning traces and actions; the base pattern later decomposition work builds on rather than a decomposition scheme itself.
56 (Reflexion) | ADJACENT | method | A verbal self-reflection loop that retries a task using linguistic feedback across trials, an iterate-until-better mechanism neighbouring the stop/depth question.
57 (GenDec) | RELATED | method | A generative question-decomposition model that produces independent, complete sub-questions for multi-hop reasoning, aimed at the robustness of the decomposition itself.
58 (FSM) | RELATED | method | Casts zero-shot multi-hop decomposition as a finite-state-machine traversal, handling one sub-question per state with in-step self-correction, a controlled decomposition-depth mechanism.
59 (Huang et al., Understanding the Planning of LLM Agents) | RELATED | survey | First systematic taxonomy of LLM-agent planning; Task Decomposition is the lead category, split into decomposition-first vs interleaved.
60 (Test-time Scaling survey) | RELATED | survey | Organises test-time-scaling methods by how a problem decomposes into subproblems and their topology; unifies CoT, Branch-Solve-Merge, Tree-of-Thought under one lens.
61 (LLMs for Planning survey) | ADJACENT | survey | Comprehensive LLM-planning survey; decomposition is one component of a three-branch taxonomy cut by what the method changes.

Sixth-round entries (62-81), labelled 2026-09-07:

62 (AI Agents That Matter) | ADJACENT | analysis | Agent-benchmarking critique centred on cost vs accuracy; bears on decomposition's cost axis but is about evaluation practice, not the split decision.
63 (Agentless) | RELATED | analysis | A deliberately un-decomposed fixed localise/repair/validate pipeline that beats decomposed SE agents at ~1/60th the cost; the strongest "do less" counter-case for the split decision.
64 (Divide-and-Conquer Noise Decomposition) | RELATED | theory | Formal split of long-context failure into task / model / aggregator noise; derives when chunk-and-aggregate lets a weak model beat a strong single-shot one - directly the does-splitting-pay question, with an aggregator-error term.
65 (Question Decomposition Improves Faithfulness) | RELATED | analysis | Answering sub-questions in SEPARATE contexts vs one CoT stream; execution-across-contexts as a distinct intervention with a measured faithfulness payoff.
66 (ARES / Probabilistic Soundness) | RELATED | method | Per-step soundness scoring from only previously-verified premises, with statistical guarantees; the recovery/verification instrument the compounding-error findings call for.
67 (Branch-Solve-Merge) | RELATED | method | Explicit parallel decompose into different sub-tasks, independent solve, explicit merge - genuine parallel decomposition as opposed to sample-and-vote.
68 (BeamAggR) | RELATED | method | Atom/composite question tree, bottom-up probabilistic aggregation at composite nodes - the HTN-style aggregate-all-leaves tree.
69 (MASAI) | RELATED | method | Decomposition by software-engineering sub-problem with a dedicated per-stage sub-agent; a code-domain instance of nature-of-work decomposition.
70 (Beyond the Answer Key) | RELATED | measurement | Measures the LLM-as-verifier on step-level traces: models that grade canonical solutions well collapse on equivalent perturbed ones (75-85% false-reject); the accept/reject port's reliability, quantified.
71 (TinyV) | ADJACENT | analysis | Verifier false-negative rate (>38%) and its effect on RL reward signal; bears on the accept/reject port but framed for RL training, not decomposition control flow.
72 (CoRefine) | RELATED | method | A small controller reading full-trace confidence to decide halt / re-examine / switch approach; a recovery primitive explicitly for imperfect-verifier settings.
73 (MiCP / Adaptive Stopping) | RELATED | method | Conformal per-turn error budgets for when to stop a multi-turn loop, with an overall coverage guarantee - the depth/stop axis with a formal guarantee.
74 (Composition Collapse) | RELATED | analysis | Conditional composition failure invisible to aggregate metrics; a double-gate protocol isolating residual recombination failure from atomic knowledge.
75 (Multi-Hop Composition Bound by Pretraining Exposure) | RELATED | analysis | Controlled compositionality-gap follow-up; composition failure persists at 97% 1-hop accuracy, and transfers only to pretraining-exposed entities.
76 (Hallucination Cascade) | ADJACENT | analysis | Claim-level error dynamics across sequential agents - net attenuation at a small accuracy cost; a measured recovery/preservation trade-off, but in a refine-chain, not a task decomposition.
77 (Token Economics survey) | ADJACENT | survey | Maps the quality-vs-token-cost trade-off across single-agent / multi-agent / ecosystem levels; the cost axis broadly, not the split decision.
78 (AgentPrune / Cut the Crap) | RELATED | method | Defines and prunes inter-agent communication redundancy: comparable results at $5.6 vs $43.7; a concrete coordination-cost number and a lever on it.
79 (D-CORE) | RELATED | method | Trains sub-task decomposition back into large reasoning models that have stopped doing it ("Lazy Reasoning"); the counter-signal to decomposition-benefit-decays-with-capability.
80 (PLANET) | ADJACENT | survey | Audit of planning benchmarks and their gaps; instrumentation context for evaluating plans rather than a decomposition study.
81 (AgentForge) | ADJACENT | method | Execution-grounded verification plus role decomposition in an SE multi-agent system; on-topic, but a thin preprint with an unproven venue.
