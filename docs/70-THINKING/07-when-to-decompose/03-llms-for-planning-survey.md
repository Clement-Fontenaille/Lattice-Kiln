# Review: Large Language Models for Planning: A Comprehensive and Systematic Survey

*Collect-phase review. Descriptive; no cross-paper conclusions.*

## Density

**Density: MEDIUM.** Dense as an index - 300+ papers, a three-branch method taxonomy, a six-attribute dataset grid, a five-family metric taxonomy - but thin on synthesis (long chains of "X et al. propose Y"), and its one comparative verdict is unsupported by its own tables. On-Subject payload: the Global-vs-Iteration decomposition axis, and the admission that decomposition quality is the binding constraint and is unmeasured.

## Name, keywords, year, venue

**Name.** Pengfei Cao, Tianyi Men, Wencan Liu, Jingwen Zhang, Xuzhao Li, Xixun Lin,
Dianbo Sui, Yanan Cao, Kang Liu, Jun Zhao. "Large Language Models for Planning: A
Comprehensive and Systematic Survey." arXiv:2505.19683v1 [cs.AI], 26 May 2025.

**Venue.** arXiv preprint, no venue stated on v1. Formatted in an ACM template
("Report GitHub Issue" HTML wrapper aside, the running style is ACM
`acmart`-flavoured), so it reads as targeted at an ACM survey venue (e.g. ACM
Computing Surveys), but nothing in the paper claims acceptance. Licence: arXiv
perpetual non-exclusive. Companion resource: a GitHub list of 300+ planning
papers, `Quester-one/Awesome-LLM-Planning`.

**Year.** 2025.

**My keywords** (not the paper's): survey; taxonomy paper; LLM planning; agent
planning; task decomposition; symbolic planner integration (PDDL); memory-augmented
agents; imitation learning on trajectories; process vs outcome reward; tree search
(ToT / MCTS / A*); world models; decoding-time planning; benchmark catalogue;
evaluation-metric catalogue; mechanistic interpretability of planning; no new
experiments.

## Approach

This is a pure literature survey. The authors make no new system, run no new
experiments of their own (their "performance comparison" section is a compilation
of numbers reported by other papers), and contribute instead: (a) a formal
definition of the planning problem and three orthogonal categorisations of it;
(b) a three-branch taxonomy of LLM-based planning *methods*; (c) a catalogue of
evaluation datasets and metrics plus a reported-numbers comparison; (d) a short
survey of work probing the *mechanism* by which LLMs plan; (e) six future
directions; (f) an open paper list.

They position the paper against prior surveys explicitly: Huang et al. (2024a) is
called non-exhaustive, stops at February 2024, and omits evaluation and
interpretability; Aghzal et al. (2025), Tantakoun et al. (2025) and Wei et al.
(2025b) are called insufficiently comprehensive or insufficiently fine-grained;
broader agent surveys (Wang et al. 2024k; Luo et al. 2025; Li et al. 2024e) treat
planning only in part. Comprehensiveness plus fine-grained categorisation plus
coverage of evaluation and mechanism is therefore the stated gap they fill.

**The formal frame.** A planning problem is the tuple `(S, A, T, s_init, S_goal)`;
a solution is an action sequence `π = (a_0 … a_{n-1})` carrying `s_init` into
`S_goal` under `T`. LLM planning is written `π = Planning(S, A, T, s_init, S_goal; Θ)`
with `Θ` the model parameters. On top of this they lay three binary axes:

- **MDP vs POMDP** — whether the environment is fully observable. POMDP adds an
  observation space `O` and observation function `Z: S × A → O`.
- **High-level vs low-level** — high-level planning is written as the *decomposition*
  `P_H → [P_M1, …, P_Mn]` (a task into medium sub-tasks); low-level planning is
  `P_Mi → [a_1^(i), …, a_mi^(i)]` (a sub-task into primitive actions); the final
  plan is the concatenation of the low-level sequences. Decomposition is thus
  written into the *definitional* layer of the survey, not only the method layer.
- **Open-loop vs closed-loop** — whether the action sequence is chosen once from
  `s_0` (`argmax p_θ(a_{0:n-1} | s_0)`) or step-by-step conditioned on the observed
  state history (`a_i = argmax p_θ(a_i | s_{0:i})`).

## Taxonomy in detail

The organising claim: every LLM planning method either bolts something onto the
model, changes the model's weights, or changes what the model does at inference
time. Hence three principal branches, each with sub-branches, each closed by an
explicit bulleted "Summary of …" box that names the branch's limitation.

**1. External Module Augmented Methods** — LLM plus an outside component.

- *Planner Enhanced.* The LLM is used as a **translator**, not a planner: natural
  language → a formal representation, which a sound external solver then solves.
  LLM+P (NL → PDDL → classical planner → back to NL), LLM-DP (PDDL goals plus world
  state monitoring), TRIP-PAL (travel), LLM+ASP (atomic facts → answer-set
  programming solver), Hao et al. (multi-constraint problems → SMT solver), TTG
  (→ MILP solver). Because generated PDDL is error-prone, a sub-line works on
  repairing it: Guan et al. (validation tools + human experts in the loop),
  PDDLEGO (recursive fall-back to a sub-goal when the file is underspecified),
  Mahdavi et al. (multiple candidates ranked by an exploration-walk metric),
  Gundawar et al. (symbolic verifiers that trigger reprompting on failure),
  Kambhampati et al.'s LLM-Modulo framing (LLM generates approximate knowledge,
  external verifiers certify it). And a sub-line that just *measures* translation:
  Xie et al. (2023) report LLMs are markedly better at translating to PDDL than at
  planning; Proc2Pddl, Planetarium, AutoPlanBench are the benchmarks built for it.
  Stated limitation: capped by code-conversion quality, and the solver's scope caps
  generality.
- *Memory Enhanced.* An external store of past states/experience. MemoryBank,
  Think-in-Memory (with a hashing scheme for retrieval efficiency), MemGPT (OS-style
  paging around the context limit), Rememberer (RL-updated long-term experience),
  MoT (pre-thought high-confidence thoughts as memory), CLIN (causal abstractions
  from reflection), EM2 (memory as a latent, EM updates), JARVIS-1 (multimodal
  memory of successful plans), Synapse (exemplar memory of successful trajectories),
  DT-Mem (parametric working memory). Structured variants: graph-form personal-device
  memory, graph-based context memory for embodied retrieval-augmented planning,
  memory-dependency pairs plus AttentionTuner for POMDPs. Stated limitation:
  dependent on retrieval accuracy; how to update memory is unsettled.

**2. Finetuning-based Methods** — change `Θ`.

- *Imitation Learning-based*, sorted by **data source**:
  - Expert demonstration: Auto-GUI (action chains; noted not to obey scaling laws),
    Agent-FLAN, FireAct, OpenCodeReasoning (736k Python samples from DeepSeek-R1
    over 28,904 competitive-programming problems), TAPIR (teacher selects hard tasks
    for the student), Retrieve-Plan-Generation, LTL-formula sampling for constraint
    compliance, CoPlanner (decompose and assign to different agents; behavioural
    cloning init plus difficulty-aware curriculum), Morishita et al.'s four synthetic
    -sample design principles.
  - Self-generated: KnowAgent (action knowledge base against planning hallucination),
    AUTOACT (synthesises data and *spawns a team of sub-agents* by division of
    labour), Stream-of-Search (train on heuristic-solver search trajectories),
    Dualformer and Lehnert et al. (train on A* traces; fast/slow modes), Synatra
    (indirect knowledge from web tutorials → direct demonstrations), AGENTGEN
    (auto-generate environments *and* tasks), Li et al. 2025 (multi-preference DPO
    ensemble + self-rewrite).
  - Hybrid: hierarchical mixture-of-experts over several LLMs, CAMPHOR (same but
    parameter-sharing and compression for latency/memory), robot planning + env
    feedback end-to-end, AutoWebGLM, world-knowledge-model self-synthesis.
  - Stated limitation: data acquisition cost/efficiency and generalisation to new
    dynamic scenarios.
- *Feedback-based*, sorted by **feedback source**:
  - Environmental: self-play games, interpreters as verifiers for code, A3T
    (auto-annotate trajectory quality from observation + reward), contrastive
    failure-vs-expert trajectories, simulated trial-and-error for tool use, S2RCQL
    (Q-learning over spatial cues against spatial hallucination), difficulty-adaptive
    reasoning length, BDC for code.
  - Reward model: **outcome** reward models (WEBRL, SCoRe) are criticised in-line for
    binary signals that give no guidance on intermediate steps, which motivates
    **process** reward models (Wang et al. 2024e's step-quality PRM feeding Q-value
    training; Jiao et al.'s DPO over synthetic process rewards) — themselves called
    complex, compute-expensive, and data-costly. Then domain-specific reward design:
    cross-platform GUI, Actor2Reasoner (format / task / element-localisation rewards),
    perception-reasoning decoupling for embodied agents, ReTool (result-driven RL for
    tool calling), a game reward balancing accuracy / action legality / interpretability,
    and a code-patch-similarity continuous reward letting a 70B open model rival
    proprietary systems on software engineering.
  - Self-generated and external: SPIN (self-adversarial weak→strong), RefAug
    (append a reflection section to each training answer), SPPO, CPO and CPL
    (preferences harvested from tree-structured reasoning or search), then critique
    models — AutoMathCritique (step-level supervision), Wu et al. 2024a, and an
    adaptive error-classification framework with the MWPES-300K dataset.
  - Stated limitation: depends on high-quality feedback signals; a universal reward
    model across planning tasks is hard.

**3. Searching-based Methods** — leave the weights alone, change the inference
procedure. Three sub-branches, described in the section below and after.

- *Decomposition-based* (§3.3.1) — split the input task. See next section.
- *Exploration-based* (§3.3.2) — search the plan space. Five families:
  **ToT-based** (ToT itself: each thought a node, expand children, score, DFS/BFS;
  SearChain and AVIS fold retrieval/tool feedback into expansion; Tree-of-Mixed-Thought
  tries a direct plan first and only falls back to tree search — an explicit fast/slow
  switch; System-1.x adds a *controller that decomposes the task* and routes easy
  parts to System 1, hard parts to System 2; GoT generalises the tree to a graph with
  aggregating in-edges; TP's propose-solve-aggregate over analogous problems;
  Tree-Planner samples whole trajectories and merges common prefixes into an action
  tree for closed-loop robotics; AGoT recursively decomposes into a dynamic DAG,
  unifying chain/tree/graph to allocate compute).
  **MCTS-based** (selection / expansion / simulation / back-propagation; LLM-MCTS uses
  the LLM as both commonsense model and heuristic policy; THOUGHTSCULPT reflects at
  step level and revises earlier outputs; MC-DML uses in-trial and cross-trial memory
  to adjust action values; CoAT inserts an association stage between expansion and
  simulation; WebPilot decomposes globally into sub-tasks then runs adapted MCTS
  locally on each).
  **A\*-based** (ToolChain* with hand-defined cumulative and future cost functions;
  Koh et al. for multimodal web navigation; LLM-A* — LLM for global high-level plan,
  A* for low-level path search).
  **World-model-based** (motivated by real-world interaction being slow, unsafe and
  irreversible: RAP treats the LLM as world model predicting state transitions;
  WEBDREAMER simulates web-page state changes rather than acting; diffusion world
  model for robot manipulation; WorldCoder represents world knowledge as code;
  ReasonPlanner uses a temporal knowledge graph).
  **Reward-model-based** (freeze the policy, improve the scorer: QLASS trains a
  Q-value network over intermediate nodes; ARMAP builds positive/negative trajectory
  pairs).
  Stated limitation: search cost.
- *Decoding-based* (§3.3.3) — change the token-level search. Self-evaluation-guided
  stochastic beam search (Xie et al. 2024b); CoT-decoding (Wang and Zhou — CoT paths
  are recoverable from top-k alternative first tokens with *no prompt at all*,
  selected by confidence); lookahead families — MCTS-built value-guided decoding
  (Liu et al. 2024a), constrained decoding with a lookahead heuristic (Roy et al.),
  predictive decoding re-weighting the distribution by sampled foresight trajectories
  (Ma et al.); plus contrastive and grounded decoding. Stated limitation: bounded by
  the base model; weak on very complex planning.

## Where task decomposition sits

Decomposition appears at two distinct levels in this survey, and the distinction is
the paper's most useful structural move for anyone reading it *for* decomposition.

**As a definition.** §2.2.2 defines high-level planning as literally the map
`P_H → [P_M1, …, P_Mn]`, and low-level planning as `P_Mi → [actions]`. Decomposition
is therefore not an optional technique in the paper's ontology — it *is* what
high-level planning means, and any hierarchical method is by construction a
decomposing one.

**As one method family.** §3.3.1, Decomposition-based Methods, sits inside the
Searching-based branch — grouped with tree search and decoding, i.e. classed as an
*inference-time* strategy rather than an architectural or training one. The framing
sentence: "This approach first decomposes a complex task into several simpler
subtasks, and then plans for these subtasks individually." The split is by
**decomposition mode**, and the axis is *when* the split happens:

- **Global Decomposition** — the whole task is analysed and split up front, then the
  parts are addressed concurrently or sequentially "without requiring multiple rounds
  of interaction with the environment." Explicitly scoped to *fully observable*
  environments. Two shapes:
  - *Linear chain*: each sub-task consumes the previous one's output. Qiu et al.
    (abstract arrangement plan, then plan-enhanced reasoning); HRV (task → sub-tasks
    → executable atomic actions); Zhou et al. 2022 (least-to-most style: each
    sub-problem's solution depends on the earlier ones); Protrix (design a reasoning
    path, then route each step to program-based or text-based reasoning).
  - *Graph*: sub-tasks interconnected by logical and data dependencies, which permits
    parallelism and non-linear dependency. HuggingGPT (LLM as "brain" planning and
    dispatching, smaller expert models as executors — an inter-model cooperation
    protocol); UrbanLLM (city queries → sub-task graph → matched spatiotemporal
    models); Zheng et al. 2024c (decompose plan generation by differing selection
    logics); Li et al. 2024f (a **meta-agent** as brain decomposing a query and
    assigning sub-tasks to the agents able to solve them); Plan-RAG (a DAG of atomic
    dynamic sub-queries preserving conditional dependencies).
- **Iteration Decomposition** — the split is revised as execution proceeds; the paper's
  key phrase is "breaking down tasks into smaller components and then refining and
  executing them iteratively based on feedback." Three sub-groupings:
  - *Multistage with back-edges*: Yuan et al. 2023 (constrained language planning in
    two steps; if goal generation yields no executable script, the goal step is
    revised from the script step's feedback); RaDA (retrieval-augmented decomposition
    RaD, then retrieval-augmented action generation RaA; misaligned actions send
    control back to RaD to adjust the high-level sub-tasks); Xie and Zou (travel
    planning; new information can invalidate the outline and restart the stage chain).
  - *History-informed*: Zhang et al. 2023b (question-answer history predicts the next
    operation; wrong answers adjust the prediction algorithm); TCRG (a Task and
    Circuit Relation Graph making execution history structural and domain-specific);
    CR-Planner (iteratively selects and executes sub-goals with a **sub-goal critic**
    supplying rewards; a poor reward changes sub-goal selection); OSCAR (two-level —
    instructions → sub-tasks, then incremental actions per sub-task; a state machine
    detecting an unexpected transition can revise *both* the decomposition and the
    action generation).
  - *Dynamic planning*: TravelPlanner+ (splits into user-model generation and strategy
    development; execution inefficiency triggers re-evaluating the user model); TRIP
    (a failure to resolve non-cooperation can redesign the entire decomposition
    framework); **ADAPT** (chooses the decomposition strategy from the LLM's own
    *execution capability*, and recursively adjusts sub-tasks when execution proves
    difficult); Budget Planner (user feedback on the abstract plan triggers refinement).

Note two things the survey does structurally. First, decomposition also shows up
*outside* §3.3.1 — CoPlanner and AUTOACT (finetuning branch) decompose and assign to
sub-agents; System-1.x, WebPilot, LLM-A* and AGoT (exploration branch) decompose as
part of search; PDDLEGO (external-module branch) recursively falls back to sub-goals.
The paper does not cross-reference these, so decomposition is a *cross-cutting*
practice that its taxonomy only partly localises. Second, the survey's one-line
verdict on the family is deflationary: "such methods are limited by the task
decomposition ability of LLMs" — i.e. it treats the quality of the split as the
binding constraint, and offers no quantitative account of decomposition's own cost
(extra calls, coordination, recombination). Recombination in particular is barely
discussed: the graph methods assume dependency-respecting aggregation and GoT/TP name
aggregation as a step, but no section treats merging sub-results as a problem with
its own failure modes.

## Models targeted and benchmarks / datasets

**Models.** The survey targets no model of its own. Models appear only as the base
models of the surveyed systems, and in the two comparison tables. What is visible
there is a small-open-model world: Llama-2-7B/13B, Gemma-7B, Qwen2-VL and
Qwen2.5-VL-7B/72B, InternVL2-8B, LLaMA-3-8B, Molmo-7B, LLaVA-1.5, MiniCPM-V; GPT-4o
appears in the single search-based row of the web table. Proprietary frontier models
are discussed in the text (OpenAI o1 in the metrics section, DeepSeek-R1 as both a
trajectory generator and the motivating example for the RL future direction) but are
not the tables' subject. That composition is itself a finding: the table is dominated
by *finetuned* 7–8B vision-language models.

**Benchmark catalogue** (§4.1, Tables 1 and 2), organised by scenario into four
categories:

- **Digital**: *Web navigation* — WebShop, MiniWoB++, Mind2Web, WebArena,
  VisualWebArena, WebVoyager, WEBLINX. *Mobile* — AndroidWorld, PIXELHELP, META-GUI,
  AITW, ANDROIDCONTROL, Mobile-Env, A3. *Desktop* — OSWORLD, AgentStudio,
  TheAgentCompany, WindowsAgentArena, WorkArena.
- **Embodied**: *Household robot* — ALFWorld, ALFRED, VirtualHome, ScienceWorld,
  Watch&Help, LangSuit·E, ActPlan-1K, PARTNR, Embodied Agent Interface, LoTa-Bench,
  GOAT-Bench, BEHAVIOR-1K. *Manipulation* — VLMbench, VLABench, VIMA-Bench,
  EmbodiedBench, RoCoBench. *Minecraft* — MineDojo, Craftax, MinePlanner, TeamCraft,
  Plancraft, MINDAGENT, Overcooked-AI. *Autonomous driving* — PCA, MetaAD.
- **Everyday**: *Travel* — TravelPlanner, ChinaTravel, NATURAL PLAN. *Workflow* —
  FlowBench, Open Grounded Planning, HuggingGPT, TaskBench, TaskLAMA, WORFBENCH,
  WIKIPLAN, ISG-BENCH. *Tool calling* — ToolBench, AppWorld, Api-bank, ToolComp,
  Toolsandbox, Tooltalk. *Code generation* — SWE-Bench, SWE-Gym, HumanEval.
  *Game playing* — VSP, TextWorld, BabyAI, PlanBench.
- **Vertical**: MLE-bench (machine learning); ResearchArena, CYCLERESEARCHER (AI
  research); BIOPORT (biological protocols); AUCARENA (financial simulation);
  DStruct2Design, Tell2Design (interior design); AgentBench, VisualAgentBench
  (composite).

Each dataset is tabulated on six structural attributes — Env (is it an interactive
dynamic environment), MM (multimodal), Obs (MDP or POMDP), Loop (open / closed /
both), Output (action, plan, code, or multiple), and Metric. This grid, rather than
the list, is the section's contribution: it makes the definitional axes of §2 do
work as a benchmark-classification scheme. The authors note that datasets often span
several categories and are filed under one.

Two decomposition-relevant remarks in the dataset prose. *Workflow* is defined
outright as "decomposing a complex problem into a structured workflow, where
individual tasks are represented as nodes … interdependent, with each task relying on
the completion of previous ones", and is said to test the ability to decompose and to
identify logical dependencies among sub-tasks, plus local adjustment without breaking
overall consistency. The *Minecraft* and *composite* categories are described as
testing "hierarchical task decomposition" specifically. So the survey does treat
decomposition as a *measurable* capability, but only via whole-task success on
benchmarks that happen to require it — it names no metric that scores a decomposition
itself.

**Evaluation-metric taxonomy** (§4.2) — five families, and this is the survey's
tidiest original synthesis:

1. **Correctness and accuracy.** Success Rate, disambiguated into three kinds the
   literature confusingly all calls "SR":
   - *Response-based* — does the text answer match the reference (WebArena's `r_info`
     with exact_match / must_include / fuzzy_match).
   - *Action-based* — Step Success Rate (single predicted action vs expert
     annotation, Mind2Web) and Trajectory Success Rate (whole trajectory vs expert;
     FlowBench scores trajectory correctness with GPT-4 and a template).
   - *State-based* — introduced explicitly because the path to a goal is not unique:
     Final State Success Rate via programmatic end-state checkpoints (WebArena's
     `r_prog` inspecting the site database and pages), and Intermediate State Success
     Rate via mid-execution checkpoints (TheAgentCompany's Partial Completion Score).
2. **Efficiency and optimisation.** Execution Efficiency — action count (LangSuit·E's
   Average Steps, PARTNR's Simulation Steps), fewer being better. Plan Optimization —
   whether the chosen feasible plan minimises cumulative resource use (PlanBench, and
   work on o1).
3. **Consistency and rationality.** *Constraint satisfaction*: Environmental
   Constraint Adherence (ChinaTravel's Environmental Pass Rate; TravelPlanner's Hard
   Constraint Pass Rate) and Action Executability (Open Grounded Planning's
   executableness — do the plan's steps exist in the provided action library).
   *Cognitive coherence*: Commonsense Alignment (ActPlan-1K's Commonsense
   Satisfaction; TravelPlanner's Commonsense Pass Rate) and Logical Coherence
   (ChinaTravel's Logical Pass Rate; CaT-BENCH's Temporal Consistency).
4. **Tool usage.** Tool Invocation Precision, split into Tool Selection Accuracy
   (TaskBench's Node F1 and Edge F1 — note the *edge* metric scores the dependency
   structure between tool calls, the closest thing in the whole metric taxonomy to
   scoring a decomposition's shape) and Parameter Specification Accuracy (TaskBench's
   Parameter Name F1 and Parameter Name-Value Pair F1).
5. **Human-computer interaction.** Cognitive Load (NASA TLX, in Valmeekam et al.
   2023b) and Task Coordination (PARTNR's Task offloading — how efficiently work is
   distributed between human and AI).

Figure 8 maps metrics to datasets at three granularities.

## Author incentive

All ten authors are at Chinese public research institutes: the Key Laboratory of
Cognition and Decision Intelligence for Complex Systems at CASIA (Institute of
Automation, Chinese Academy of Sciences) with UCAS's School of AI (Cao, Men, Kang Liu,
Zhao — the senior CASIA NLP group), the Institute of Information Engineering, CAS
(Jingwen Zhang, Lin, Yanan Cao), Harbin Institute of Technology (Wencan Liu, Sui), and
Beijing Institute of Technology (Xuzhao Li). No funding statement, no acknowledgements,
no conflict-of-interest declaration, and no industrial affiliation appear in v1.

The visible stake is academic-positional rather than commercial. Two components of it:
(a) the survey competes directly with at least four other 2024–2025 planning surveys,
which it names and criticises in the introduction, so being *the* citable reference
survey is the payoff, reinforced by the 300+ paper GitHub list; (b) the authors' own
prior work is inside the object of survey — Men et al. (2024), on the look-ahead
planning mechanism and information flow, is cited in the introduction as evidence
that mechanism work exists and again as a centrepiece of §5's internal-interpretation
discussion. §5 is also one of the sections the authors claim rival surveys lack, so
the section that most distinguishes the paper is partly built on the authors' own
result. That is a mild self-citation incentive, not a hidden one; it is legible from
the reference list. There is no product, no system, no benchmark of their own being
promoted, and no method whose superiority the paper would benefit from showing.

## Measurement methodology

Brushed, as the format allows, because there is very little to brush: **the paper
runs no experiments and defines no dependent variable of its own.**

- **Selection of the corpus.** No systematic-review protocol is reported — no search
  strings, no databases queried, no inclusion/exclusion criteria, no date cut-off
  stated, no count of papers screened versus included. The word "systematic" in the
  title refers to the taxonomy's organisation, not to PRISMA-style methodology. The
  companion repository claims 300+ papers; the reference list is larger still, but
  the mapping between the two is not given. Coverage in practice runs to roughly May
  2025 (several cited works are dated 2025/5).
- **Dependent variables, borrowed.** §4.3's Tables 3 and 4 compile numbers *as
  reported by the original papers*. Web table (Table 3): Mind2Web = mean step success
  rate over the three subsets, WebArena = task success rate, AITW = step success rate
  of the subsets, ScreenSpot = step success rate. Embodied table (Table 4): ALFWorld
  and ScienceWorld, using either the mean of Seen and Unseen or the value the original
  paper reported — that "or" is stated in the caption, so the column is not internally
  homogeneous.
- **What is controlled: nothing.** Rows differ in base model (Llama-2-7B through
  Qwen2-VL-72B, LLaVA-1.5, GPT-4o), in modality, in date (2023/10 to 2025/5), and in
  whether the method finetunes or searches — the table annotates all four as columns
  rather than holding any fixed. Prompting, harness, and evaluation-harness version
  are uncontrolled. So the tables are a reported-numbers digest, not a comparison in
  the experimental sense.
- **N and significance.** N of runs is not reported for any cell; no variance,
  confidence interval, seed count, or significance test appears anywhere in the paper.
  No cost, latency, or token-count column exists in either table, so nothing in the
  survey's own measurement layer can speak to the *price* of a method — relevant given
  that search- and decomposition-based methods spend extra calls by construction.
- **Inference drawn from the tables** is correspondingly coarse and the authors keep
  it qualitative (three numbered observations, below).

The methodological substance of the paper is thus its *classification* work: the
six-attribute dataset grid and the five-family metric taxonomy, both of which are
defensible descriptive instruments, and neither of which is validated (no
inter-annotator agreement on the dataset attribute assignments, for instance).

## Key findings and the authors' own reading

Being a survey, its "findings" are of three kinds: the three explicit observations
drawn from the comparison tables, the per-branch summary verdicts, and the
mechanism section's imported results.

**The three stated observations from §4.3, in the authors' own reading:**

1. *Performance remains suboptimal, and unevenly so.* Recent methods exceed 80%
   success on ALFWorld, but Mind2Web step success rates are "typically less than 65%".
   Their reading: the gap is task-complexity-driven, and "more effective planning
   methods need to be designed for more complex tasks."
2. *Finetuning is the mainstream approach and the strongest one.* They say researchers
   increasingly favour finetuning because imitation-learning and feedback-based methods
   "significantly enhance planning performance compared to other types of methods,"
   whereas training-free methods (i.e. the whole searching-based branch, including
   decomposition) "are limited by the capabilities of the base model." This is the
   paper's single most consequential judgement: the authors read their own tables as
   ranking their three branches, with training-free inference-time strategies placed
   last.
3. *Multimodal agents are becoming dominant.* Agents move from text-only to visual or
   visual+text input, which the authors read as agents becoming "more and more
   human-like" — clicking icons, typing in fields as a person would.

**Per-branch verdicts** (the "Summary of …" boxes; each is a limitation claim, and
together they form the survey's actual comparative argument):

- Planner-enhanced: capped by code-conversion quality; the external planner's type and
  scope cap generality.
- Memory-enhanced: hostage to retrieval accuracy; memory *updating* is unsolved.
- Imitation learning: data acquisition cost and efficiency; generalisation to new
  dynamic scenarios.
- Feedback-based: needs high-quality feedback; a universal reward model across planning
  tasks is hard to train.
- Decomposition-based: "limited by the task decomposition ability of LLMs."
- Exploration-based: complex search algorithms raise computational cost — "practical
  challenges."
- Decoding-based: heavily reliant on the base model; weak on very complex planning.

**Imported mechanism findings (§5),** which the authors present as the field's current
understanding rather than as their own claims:

*External interpretation* — Bachmann and Nagarajan argue teacher-forced next-token
training induces problematic learning dynamics on lookahead tasks, and autoregressive
inference produces cascading errors. Xie et al. (2024d) identify "the limited role of
constraints and the diminishing impact of questions" as factors in planning
performance. Sprague et al. (2024) find prompt-based CoT helps predominantly on math
and logic, where it can trace intermediate steps. Stechly et al. find CoT on classical
planning (Blocksworld) relies heavily on *pattern matching* — effectiveness depends on
similarity between in-context examples and the query, so it does not generalise
easily. Wang et al. (2024n) find self-correction works in-context when the model's
self-assessment happens to be correct.

*Internal interpretation* — Wu et al. (2024c) test two hypotheses about whether
transformers think ahead: **pre-caching** (features computed now that are irrelevant
now but useful later) versus **breadcrumbs** (features most useful now happen also to
be most useful later); pre-caching is demonstrable on a synthetic dataset, while
smaller models tend to favour breadcrumbs. Men et al. (2024) locate look-ahead planning
in multi-head self-attention drawing decision-relevant information from goal-state and
recent-step spans, and propose a "look-ahead planning decision existence hypothesis":
middle and upper layers encode a few short-term future decisions. Wang et al. (2024l)
frame planning as network path-finding and show LLMs learn adjacency matrices and a
*limited* form of reachability matrices. Cabannes et al. find "iteration heads"
specialised for iterative reasoning, and "inner circuits" for multi-hop reasoning that
transfer to tasks with shared logical structure.

The authors' own reading of §5 is guarded: external analyses "cannot reveal the
internal mechanisms," and internal work is "preliminary," with "a systematic
understanding of the underlying processes remain[ing] lacking" — specifically the
origins and the transferability of planning ability.

## Open questions the paper itself raises

Stated limitations of the *field* (the paper states no limitations of *itself* — there
is no limitations section, and no reflexive note on survey scope, selection bias, or
the comparability of the compiled tables):

- **Mechanism.** Origins and transferability of planning ability are open; how CoT and
  self-correction work is unclear; whether models genuinely plan ahead is only
  partially answered (pre-caching vs breadcrumbs).
- **Decomposition quality.** Implicitly open — the family's binding constraint is named
  as "the task decomposition ability of LLMs," but no route to improving or measuring
  that ability is proposed.
- **Evaluation.** "A unified system of standards and evaluation methods has yet to be
  established" — said of the dataset landscape, and demonstrated by the three
  incompatible senses of "Success Rate" the metric section has to disentangle.

The six **future directions** of §6, in the paper's own framing:

1. **RL in LLM-based planning** — motivated by DeepSeek-R1. Three sub-problems:
   realistic and scalable environment simulation; reward models that reflect complex
   long-horizon objectives and goal alignment; adapting standard RL to LLM properties
   (high-dimensional trajectory spaces, context sensitivity, exploration/exploitation
   balance).
2. **Planning with environmental constraints**, especially under partial observability
   — intelligent state estimation from limited observations, integrating environmental
   priors (physical constraints, domain rules, structural regularities) to make
   planning robust and cut needless exploration; balancing accuracy, efficiency and
   scalability under incomplete information.
3. **Personalized planning systems** — continuously learning user goals, preferences
   and behaviour through interaction, via adaptive tuning or modular external memory;
   blocked on privacy preservation, user-data sparsity, and lifelong learning without
   catastrophic forgetting.
4. **Edge deployment** — lightweight planners for phones, drones, robots; the stated
   obstacle is that downsizing sharply degrades planning; compression and transfer
   learning nominated as tools.
5. **Pretraining of agent base models** — general-purpose agent backbones pretrained on
   synthetic trajectories; open problems are scalable, diverse, high-quality data
   synthesis pipelines and coverage of long-tail but safety-critical scenarios.
6. **Generalization** — most planners are task-specific and degrade on unseen
   scenarios; RL-trained LLMs generalise better, which prompts the paper's sharpest
   open question: *"can generalization in planning be driven more by enhanced
   reasoning, rather than by mere memorization of training data?"* The stated goal is a
   universal LLM-based planner across tasks, domains and environments.

## Appreciation (mechanism vs magnitude)

**What transfers as MECHANISM — arguments and distinctions that stand on their own,
independent of any number in this paper.**

- *The three-branch partition itself.* External module / finetuning / searching is
  cleanly cut by **what gets changed**: the surroundings, the weights, or the inference
  procedure. That is a real and portable distinction, and it is close to exhaustive for
  the object it covers. It transfers as a way of asking, of any planning technique,
  which of the three levers it pulls.
- *Decomposition classified by* when *the split happens.* Global (up front, one shot,
  requires full observability) versus Iteration (revised against feedback during
  execution) is a sharper axis than the usual "flat vs hierarchical" framing, because
  it ties the choice to an environmental property: the survey's claim that global
  decomposition is "suited for fully observable environments" is an argument, not a
  measurement, and it survives outside the paper.
- *Within global decomposition, linear chain versus graph.* The graph form's stated
  advantage — sub-tasks interconnected by logical and data dependencies, hence
  parallelism and non-linear dependency — is a structural claim about what a
  dependency-typed plan buys you.
- *ADAPT's principle*, as reported: choose the decomposition strategy from the
  executor's own capability, and recurse only when execution proves hard. That is a
  mechanism for setting depth (capability-driven, discovered at runtime) rather than
  fixing it.
- *The three senses of "Success Rate."* Response-based / action-based / state-based,
  with the explicit motivation for state-based metrics — the path to a goal is not
  unique, so trajectory-vs-expert comparison penalises correct alternative routes.
  This is a clean methodological point, and the intermediate-state checkpoint idea
  (partial completion scoring) transfers directly to any harness that wants credit
  assignment inside a long run.
- *Outcome vs process reward.* The stated asymmetry — binary outcome signals give no
  guidance on intermediate steps; process rewards do but are complex, expensive, and
  data-hungry — is a design trade-off, not a measurement.
- *The mechanism results in §5,* particularly Stechly et al.'s pattern-matching account
  of CoT on classical planning, Bachmann and Nagarajan on teacher forcing and cascading
  errors, and the pre-caching vs breadcrumbs pair. These transfer as *hypotheses with
  named evidence*, and are the most interesting content in the survey — though they
  are all imported, so the transfer credit belongs to the cited works.
- *The dataset attribute grid.* Env / MM / Obs / Loop / Output as a classification of
  what a benchmark actually demands is reusable as a specification checklist.

**What is MAGNITUDE only — numbers valid inside this paper's compilation and not
outside it.**

- Every cell of Tables 3 and 4. ">80% on ALFWorld", "<65% step success on Mind2Web",
  the specific ScreenSpot figures (88.2, 89.5, 87.8…), WKM/ETO at 70.5 on ALFWorld,
  AgentTuning at 84.0 — these are transcribed from source papers with no controls, no
  variance, no seed counts, mixed base models, an eighteen-month date spread, and (for
  Table 4) an explicitly heterogeneous averaging convention. They support the loose
  claim "performance is uneven across benchmark difficulty" and essentially nothing
  finer. Any ranking read off them is an artefact of which papers reported what.
- **Observation (2) is the one to be most careful with.** "Finetuning-based methods are
  mainstream and outperform others; training-free searching methods are limited by the
  base model" is presented as an empirical reading of the tables, but the tables cannot
  bear it. Table 3 contains exactly *one* search row (TREE SEARCH on GPT-4o, WebArena
  19.2) against a dozen finetuned rows, and it is the only WebArena entry, so nothing
  is being compared. The prevalence claim ("mainstream") is a claim about *publication
  counts in the authors' corpus*, which is a real observation about the field's
  attention; the *superiority* claim riding alongside it is not established by anything
  shown. Treat the popularity finding as magnitude-with-a-caveat and the superiority
  finding as unsupported.
- The scale statistics of individual cited systems (736k samples / 28,904 problems in
  OpenCodeReasoning; a 70B model matching proprietary systems on SWE tasks) are
  second-hand and carry their source's conditions with them.

**On the survey's craft.** The taxonomy is genuinely fine-grained and the summary boxes
make each branch's weakness explicit, which is more than most surveys do. Against
that: no review protocol, no limitations section, heavy reliance on paraphrase (many
subsections are a chain of "X et al. propose Y" with no synthesis between consecutive
sentences), and some looseness — a citation mismatch at "Zhang et al. (Zheng et al.,
2024c)", the Tree-of-Mixed-Thought and Tree-Planner entries sharing one citation key
while being described as different systems, and Figures 2/3/6/7 doing organisational
work that the running text does not fully restate.

## How it could serve a harness-design effort / limitations / concerns

Stemming the discussion rather than resolving it; the survey is an inventory, so what
it offers a harness builder is mostly vocabulary, a checklist, and a set of unanswered
questions made precise.

**What it supplies.**

- *A decision vocabulary for a decomposition policy.* Global vs Iteration maps onto a
  concrete harness question: is the split fixed at plan time or revisable at run time?
  The survey attaches a precondition to the first (full observability) that a harness
  can actually test against its own environment. Chain vs graph maps onto whether the
  harness represents sub-task dependencies at all, and whether it can run independent
  branches concurrently.
- *Named back-edge designs.* RaDA (misaligned actions return control to the
  decomposition stage), OSCAR (a state machine detecting an unexpected transition
  revises both decomposition and action generation), CR-Planner (a sub-goal critic whose
  reward gates sub-goal reselection), ADAPT (recursive adjustment triggered by execution
  difficulty). These are four distinct answers to "what evidence licenses re-splitting?"
  — a question a harness must answer explicitly, and the survey at least enumerates the
  options.
- *A depth/dispatch vocabulary.* Meta-agent-to-sub-agent assignment (Li et al. 2024f),
  brain-and-executors (HuggingGPT), global-decompose-then-local-search (WebPilot),
  high-level-LLM-plus-low-level-solver (LLM-A*), controller-routed fast/slow
  (System-1.x), DAG of atomic sub-queries (Plan-RAG).
- *A verification pattern.* The LLM-Modulo framing — model generates approximate
  knowledge, external verifiers certify, failures trigger reprompting (Gundawar et al.)
  — is directly implementable as a harness gate, and the reported result that LLMs
  translate to formal representations markedly better than they plan (Xie et al. 2023)
  is a design-relevant asymmetry.
- *An instrumentation checklist.* The five metric families, and specifically:
  intermediate-state checkpoints for partial credit; action executability against a
  declared action library; Edge F1 for scoring the dependency graph and not just the
  node set; step count as an efficiency measure; task-offloading as a human/system
  division measure.

**Limitations and concerns for that use.**

- *Cost is absent.* The survey never quantifies the price of splitting. Extra calls,
  coordination overhead, and the recombination step are acknowledged nowhere as
  measured quantities; the exploration-branch summary says only that search "can
  increase computational costs." No table has a token, latency, or dollar column. If
  the question is whether decomposition pays for itself, this paper does not contain
  the evidence — it contains the taxonomy of things one might measure.
- *Recombination is a blind spot.* Splitting and executing are covered in detail;
  merging is assumed. TP's "aggregate", GoT's aggregating in-edges, and the DAG methods'
  dependency-respecting composition are the only mentions, and none is treated as a
  failure source. A harness will find that its hardest bugs live exactly there.
- *Decomposition quality is unmeasured.* The survey concedes the family is bounded by
  "the task decomposition ability of LLMs," then offers no metric for that ability. Its
  own metric taxonomy scores outcomes, not plans-as-artefacts (Edge F1 is the lone
  near-exception). So the binding constraint the paper names is one it gives no
  instrument to observe.
- *The finetuning verdict cuts against inference-time harness work* and should not be
  accepted on the evidence given (see the appreciation section). It is nonetheless a
  live hypothesis worth stating: if capability is more cheaply bought by weight updates
  than by orchestration, a harness's value proposition narrows. The survey raises this;
  it does not settle it, and its tables cannot.
- *Domain skew.* The comparison tables are web/GUI navigation and embodied household
  simulation. Coding appears in the dataset catalogue (SWE-Bench, SWE-Gym, HumanEval)
  but in neither performance table. Transfer of any of this to a software-engineering
  harness is therefore untested within the paper.
- *Scope of "planning."* The formal frame is `(S, A, T, s_init, S_goal)` — a
  sequential-decision framing inherited from classical planning. Decomposition work
  that is not about action sequences (splitting a document, a corpus, a proof) does not
  fit the frame cleanly, and the survey does not discuss the fit.
- *Currency and coverage.* No stated protocol means unknown selection bias; coverage
  ends around May 2025.

## Five citations worth chasing

1. **Stechly, Valmeekam, Kambhampati — on the limits of Chain-of-Thought in classical
   planning (Blocksworld).** The survey's report that CoT-style planning works by
   pattern matching against in-context examples, and therefore does not generalise, is
   the single most load-bearing mechanism claim it relays. It bears directly on whether
   a decomposition produced by prompting is a plan or a retrieval.
2. **Prasad et al., ADAPT (2023).** The only method in the survey whose decomposition
   *depth and trigger* are set by the executor's demonstrated capability, with
   recursive adjustment on execution difficulty. Directly addresses "what sets the
   depth" — a question the Subject names and the survey otherwise leaves open.
3. **Zhou et al. (2022), least-to-most style sequential decomposition.** The base case
   the whole global-linear family is built on, and the natural baseline against which
   any more elaborate splitting scheme has to justify its cost.
4. **Wu et al. (2024c), pre-caching vs breadcrumbs.** The cleanest internal-mechanism
   test of whether transformers actually compute ahead, with the finding that smaller
   models lean toward breadcrumbs — i.e. a possible mechanistic reason why weaker
   models need *external* decomposition more.
5. **Kambhampati et al., LLM-Modulo.** The framing that separates approximate
   generation from external verification, with reprompting on verifier failure — the
   most directly implementable harness architecture named anywhere in the survey, and
   the counterweight to the paper's own finetuning-first reading.

*(Runners-up, if the list could be longer: Xie et al. 2023 on LLMs translating to PDDL
better than they plan; Li et al. 2024f's meta-agent decomposition-and-assignment; and
TaskBench, for Node F1 / Edge F1 as the only metric in the survey that scores a
decomposition's structure.)*
