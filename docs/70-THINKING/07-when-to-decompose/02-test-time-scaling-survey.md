# Review: Test-time Scaling of LLMs: A Survey from A Subproblem Structure Perspective

*Collect-phase review. Descriptive; no cross-paper conclusions.*

## Density

**Density: MEDIUM.** Conceptually dense - a clean topology axis, the two tree-types distinction, per-shape concern/mitigation triples - but it measures nothing: no accuracy, cost, or scaling number in the paper is citable, and it is a v1 preprint with editing defects in load-bearing sentences. The signal is framing, not evidence.

## Name, keywords, year, venue

**Name.** Zhuoyi Yang, Xu Guo, Tong Zhang, Huijuan Xu, Boyang Li. "Test-time Scaling
of LLMs: A Survey from A Subproblem Structure Perspective." arXiv:2511.14772v1
[cs.CL], stamped 01 Nov 2025, licensed CC BY 4.0.

**Year.** 2025 (preprint; the arXiv identifier is 2511, i.e. November 2025).

**Venue.** None. arXiv preprint, not marked as accepted anywhere. The reference
formatting (ACL-style author-year, "Proceedings of ... Association for
Computational Linguistics" entries, an `\ThanksLink`-style shared correspondence
address) and the cs.CL primary class suggest an *ACL Anthology venue is the
target*, but no venue is claimed in the paper itself.

**Keywords** (mine, not the paper's): test-time scaling; inference-time compute;
task decomposition; subproblem topology; sequential / parallel / tree reasoning
paths; chain-of-thought; tree search over LLM states (A*, MCTS, beam); LLM-as-judge
node evaluation; retrieval-augmented generation as a fixed two-step decomposition;
multimodal reasoning pipelines; survey / taxonomy paper; no new experiments.

**Shape.** Short survey. Four numbered sections (Introduction; Task Decomposition;
Reasoning Paths; Future Directions and Conclusions), two figures, roughly 90
references, and no tables, no appendix, no experiments of its own.

## Approach

The paper is a survey. It contributes no method, no system, no measurements: its
product is a **two-axis taxonomy** of test-time scaling (TTS) techniques and a
synthesis of what other people have reported about the strengths and weaknesses of
each cell.

**Scope, as the authors define it.** TTS is "trading more computational resources
for more predictive accuracy at inference time." The survey deliberately fences off:

- methods that **do not alter the parameters of the main LLM** — but it *does* admit
  methods that finetune a small auxiliary model, e.g. a learned heuristic for tree
  search;
- methods that **trade compute for accuracy**, explicitly *not* inference
  acceleration;
- **structure over domain technique** — it surveys subtask organisation, not, say,
  retriever design inside RAG;
- TTS as distinct from neighbouring areas: reasoning can also be improved at
  *training* time (RL, DeepSeek-R1), and agentic LLMs contain topics (societal
  simulation) that are not TTS.

### Axis 1 — how the decomposition is produced (Section 2)

Categorised by *degree of automation*:

1. **Human-only decomposition.** The designer supplies a sufficiently detailed list
   or hierarchy of subtasks needing no further splitting. Suited to tasks with known
   processes and clear control flow — the canonical example is ChatDev (Qian et al.
   2024) adopting the waterfall process: design, coding, code completion, code
   review, testing. Claimed advantages: (a) a deterministic structure removes the
   need for the model to plan, improving inference efficiency and **reducing
   variance**; (b) it permits explicit steps that check for known LLM weaknesses the
   model may itself be oblivious to — a self-verification/safety screen (Xie et al.
   2023), a step that strips misleading irrelevant information (Deng et al. 2023),
   Self-Refine's critique-and-revise step, FLARE's low-confidence-token revision,
   Self-RAG's document-utility evaluation subtask. Claimed cost: **rigidity** — the
   hierarchy cannot be customised per input.
2. **LLM-assisted decomposition.** The model splits some or all subtasks at
   inference time. Suited to tasks needing question-specific structure or having no
   one-size-fits-all shape. Least-to-Most (Zhou et al. 2023) is the *explicit*
   representative; Chain-of-Thought is offered as the *implicit* case — no
   intermediate subproblem is named, but "these reasoning steps still reflect an
   underlying problem structure." Claimed cost: unstable or suboptimal
   decompositions — skipped necessary subtasks, irrelevant introduced steps, and the
   "well-known fact" that RL-trained CoT produces unnecessarily long thoughts.
3. **Hybrid** ("also popular"). Humans give the high-level outline; the LLM refines
   parts of it into detail at runtime. RAG variants are the exemplar: two fixed
   top-level tasks (Retrieve, then Generate), each of which the model may autonomously
   expand into multiple queries (RAG-Fusion) or iterative retrieval steps (IRCoT).

A footnote does load-bearing work here: **RAG is read as an enforced task
decomposition whose first subproblem is always retrieval.** That is what lets RAG be
carried as a third application column throughout Section 3.

### Axis 2 — the topology of the subtasks (Section 3, the "reasoning path")

The paper's organising claim: *the subproblem structure is critical to performance*,
a principle it grounds not in LLM results but in **theoretical computer science**
(Cormen et al., divide-and-conquer, dynamic programming). Three topologies, each
defined and then illustrated in three application columns — **unimodal**,
**multimodal**, **RAG** — and each closed with a "Common Concerns and Mitigation"
subsection. (Note: the sentence introducing them says "we identify four major types"
and then lists three; only three exist in the paper.)

**(a) Sequential.** Strict linear order; later steps depend on earlier results.
Figure 2 adds a precision: there *may* be branching decision points, but only one
path is visited and **there is no backtracking**. Unimodal: CoT (the model
spontaneously chooses granularity and method), then more controllable variants —
Program of Thoughts and Chain of Code translating subproblems into executable
programs, Parsel organising steps as trees of function-like elements — plus feedback
loops embedded in the chain (Self-Refine, Step-Back Prompting). Multimodal: PICa's
caption-then-answer two-step, targeted/question-relevant captioning (reported to beat
end-to-end Flamingo), Compositional CoT via scene graphs, IdealGPT's sub-questions,
Chameleon and ViperGPT/VisProg composing tool and module calls, MoReVQA's multi-stage
video pipeline. RAG: single-retrieval In-Context RALM, Rewrite-Retrieve-Read,
iterative Auto-RAG and IRCoT, and confidence-gated retrieval (Self-RAG, FLARE,
DRAGIN).
*Characteristic failure: error propagation.* Three mitigation families are named —
fix the **query** (Rephrase-and-Respond, Step-Back), let the model **self-correct**
(Self-Refine, Chain-of-Verification's independent verification questions), or
validate against **external** signal (QueryAgent's KB/interpreter feedback,
Self-Ask's separately checkable sub-questions).

**(b) Parallel.** Several paths instantiated at the beginning, each proceeding
independently **without further branching**, aggregated only at the end. Framed
explicitly as **ensemble learning**, with Breiman cited for the requirement that
members be *decorrelated*. Unimodal: Self-Consistency (majority vote over sampled
chains), Universal Self-Consistency (LLM picks the most consistent long-form answer),
Branch-Solve-Merge (an explicit split into parallel subproblems then a merge),
RR-MP (a reflection agent critiques each path), Hypothesis Search, MapCoder.
Multimodal: the modalities themselves supply decorrelation — VLP's separate visual
and language pathways, MVoT rendering textual thoughts as images, DietCoke's three
QA strategies, Mixture of Rationales' differently-focused descriptions, Cola
coordinating several VLMs. RAG: RAG-Fusion (many queries, one generation),
Speculative RAG (one query, many drafts, then verification).
*Characteristic failures: incoherence/conflict between paths, and resource
allocation.* Mitigations: consensus filtering — with the stated caveat that both
voting variants **assume correctness correlates with frequency**, which fails if
popular-but-spurious paths dominate; capability-conditional aggregation (VLP: let
strong models synthesise directly, give weak models a voting round); and cheap
pre-screening so the big model only runs on promising paths.

**(c) Tree.** Branching hierarchy, and the paper splits it in two:
- *Type 1 — path-finding trees* (Hart et al. 1968; ToT; SearChain). Each node is a
  partial solution; **children are competing solutions**; the answer is one
  root-to-leaf path; other branches are pruned. Declared the far more common type.
- *Type 2 — hierarchical-task-network trees* (Georgievski & Aiello; Tree of
  Clarifications). Leaves are subtasks that must be **combined**; all nodes are
  visited, so visit order does not matter much.

For type 1, **traversal is where the design lives**: DFS/BFS for small trees;
informed search (A*, MCTS) for large ones. The survey walks the mechanics — A*'s
g(·) historic cost and h(·) estimated future cost, "traditionally hand-crafted,
increasingly learned"; MCTS's selection/expansion/simulation/backpropagation — and
then shows how LLM papers instantiate them: Self-Evaluation Guided Beam Search
(top-K per level, score = LLM quality judgement + partial-thought probability),
ToT-BFS/ToT-DFS (threshold pruning), A*-Decoding (h = another LLM's evaluation of a
partial CoT, with g accumulating only *increases* in h to preserve optimality),
ToolChain* over API-call sequences, RAP (LLM generates both actions and resulting
states; reward from action likelihood + self-evaluation + hand-specified heuristics),
LATS (RAP plus a self-reflection stage whose failure explanation is fed back into
context, plus compiler feedback), and simulation-free variants (Monte Carlo Reasoner,
MC-NEST, I-MCTS). Multimodal trees vary what a node *is*: AVIS's API-call sequences
with backtracking, VisuoThink's Thought–Action–Observation nodes holding visual and
textual state, ZoomEye's node-as-zoomed-image-region, Retrieval-Augmented Perception's
progressive patch discarding under A*. RAG trees are called **under-investigated**;
only SearChain (backtrack when the LLM's own answer and the retrieved answer disagree
on a sub-question) and Tree of Clarifications are discussed.
*Characteristic failures:* **memory/space cost** of keeping nodes for backtracking
(mitigated by pruning and top-K expansion); **unreliable node evaluation** — LLM
judges carry biases, and using the generator as its own evaluator (RAP) invites
**self-preference bias**, while a separate evaluator (A*-Decoding) alleviates that
bias but not others (mitigations: external signals, ensembled evaluation, delaying
aggressive pruning until evidence accumulates); and the **cost of rollouts**
(replace with direct LLM evaluation, or lightweight approximations).

The claimed payoff of the taxonomy is *unification*: CoT, Branch-Solve-Merge and
Tree-of-Thought are shown to be the same design choice made three ways, and the
authors argue the identification and organisation of subproblems has implications
that hold **across** problem domains (unimodal vs multimodal) and LLM families
(direct generation vs retrieval-augmented).

## Models targeted and benchmarks / datasets used

**Directly: none.** The survey runs no experiments, so it targets no model and uses
no dataset. Everything below is inherited from the works it describes.

**Models named in passing, and what for.** The paper is written about "pretrained
LLMs and VLMs" generically. Named models appear only as instances inside surveyed
work: GPT4-V (as VLP's example of a model capable enough to skip the voting round),
Flamingo (as the end-to-end VLM that targeted-captioning pipelines are reported to
beat), DeepSeek-R1 (cited twice, once as evidence that TTS is live and once as the
*training-time* technique being excluded from scope). No model family is
systematically tracked across the surveyed methods, and there is no table pairing
technique to backbone.

**Benchmarks named.** Strikingly few, and never as results. ARC-AGI (Chollet) is
named once in the introduction as a task where TTS gains have been demonstrated.
Task *families* stand in for benchmarks throughout: numerical manipulation and
logical inference (with Sprague et al. cited for the finding that CoT helps mainly
on math and symbolic reasoning), multi-hop QA, STEM questions, visual question
answering, video question answering, geometry problems, code synthesis, API/tool
sequencing, ambiguous open-domain QA. Not a single benchmark score, accuracy figure,
compute measurement, or scaling curve appears anywhere in the paper.

**Coverage as the de facto unit.** What the survey does track is a matrix: three
topologies × three application columns (unimodal / multimodal / RAG). Roughly 90
references, drawn heavily from 2022–2025. The multimodal and RAG columns are its
distinguishing coverage; the tree×RAG cell is explicitly declared thin ("under-
investigated in the literature," two methods discussed).

## Author incentive

**Affiliations.** Two groups. Penn State (Dept. of Computer Science and Engineering):
Zhuoyi Yang, Huijuan Xu. NTU Singapore (School of Computer Science and Engineering):
Xu Guo, Tong Zhang, Boyang Li. Correspondence for all three NTU authors is listed as
boyang.li@ntu.edu.sg, which reads as Boyang Li being the senior/corresponding author.

**Funding.** No acknowledgements section, no funding statement, no grant numbers, no
conflict-of-interest declaration in the HTML version. Nothing to disclose or nothing
disclosed — the paper does not say which.

**Stake.** Purely academic, and the incentive structure is the ordinary one for a
survey preprint: **citation and framing capital**. The paper proposes a lens
("subproblem structure") and argues that lens unifies the field. If the taxonomy is
adopted, its authors own the vocabulary. That is a real incentive to *overstate the
unifying power* of the axis chosen and to present the three-way split as more
exhaustive and more natural than it might be — but it is not a commercial one. No
product, no system, no benchmark of their own is being sold, and no method of the
authors' is promoted within the taxonomy (I found no self-citation being placed at a
privileged position; the exemplars are the field's standard ones — CoT, ToT, BSM,
Self-Consistency, RAP).

**Timing.** A November 2025 preprint in a crowded area — test-time scaling surveys
were plentiful by then. The differentiator being staked out is the *organising axis*
(decomposition structure) rather than coverage completeness, plus the multimodal and
RAG columns. That is a positioning move against sibling surveys, and it explains the
paper's brevity: it is a lens paper, not a catalogue.

## Measurement methodology

Brushed, because there is almost nothing to brush: **the paper measures nothing.**

- **Dependent variable.** None of its own. The implicit one throughout is
  *predictive accuracy at fixed parameters*, with inference compute as the price;
  but no instance of either is quantified anywhere in the survey.
- **What is controlled.** Nothing empirically. The only thing held constant is
  conceptual: model parameters are fixed by definitional fiat (that is the scope
  boundary of TTS), and inference-acceleration work is excluded so that "more
  compute" always means "more accuracy sought."
- **N.** The survey's only N is its bibliography — roughly 90 references — and its
  coverage matrix of 3 topologies × 3 application settings. There is no stated
  inclusion criterion, no search protocol, no database query, no date cutoff, no
  count of papers screened versus included. It is a **narrative survey, not a
  systematic review**, and does not claim otherwise.
- **Significance.** Not treated. No statistics, no error bars, no aggregation of
  reported numbers across papers, no meta-analysis. Comparative claims are carried
  entirely by verbs: a method "yields stronger performance than" Flamingo,
  aggregation makes a "significant contribution to performance" in VLP, targeted
  captioning "improves" accuracy. Each of those is a *report of someone else's
  claim*, at that paper's own settings, and the survey does not requalify them.
- **What stands in for evidence.** Three things: (1) the argument from theoretical
  computer science that structure matters (divide-and-conquer, dynamic programming);
  (2) one genuine theory citation, Li et al. 2024d, that CoT tokens expand the class
  of problems solvable by a constant-depth Transformer — the paper's single
  formal-power claim; (3) accumulated per-technique reports collated into the
  "Common Concerns and Mitigation" subsections.
- **How the synthesis is actually done.** The real methodological move is the
  *concern-and-mitigation triple*: for each topology, name its characteristic
  failure mode, then list the surveyed mitigations against it. Error propagation for
  sequential; path conflict plus resource allocation for parallel; memory cost,
  evaluator reliability, and rollout cost for tree. This is the part of the paper
  that does analytical work rather than cataloguing, and it is qualitative
  throughout.

**Consequence for reading it.** Nothing in this paper licenses a claim that one
topology beats another on any task. The survey nowhere ranks the three; it argues
only that the *choice* is consequential and describes what each choice costs.

## Key findings — and the authors' own reading of them

The findings are claims about structure, not results. Stated as the paper states
them:

1. **Subproblem structure is the load-bearing design variable in TTS.** This is the
   central argument, offered as a principle imported from theoretical CS rather than
   demonstrated on LLMs. The authors' reading: it "is critical to performance," and
   its implications are shared across problem domains and LLM families — which is
   what justifies surveying by structure instead of by domain.
2. **The taxonomy unifies techniques normally filed apart.** CoT, Branch-Solve-Merge
   and Tree-of-Thought become one design decision made three ways; RAG becomes a
   decomposition with retrieval nailed to the first slot; multimodal pipelines become
   ordinary sequential or parallel structures whose nodes happen to hold pixels. The
   authors' reading: this is a "common lens" and a "unifying perspective ... a
   foundation" for future system design.
3. **Automation of decomposition is a genuine trade, not a ladder.** Human-only
   decomposition buys determinism, efficiency, **lower variance**, and the ability to
   insert corrective steps for weaknesses the model cannot see in itself; it pays in
   rigidity. LLM-assisted buys per-input flexibility; it pays in skipped or spurious
   subtasks and overlong chains. The authors' reading: hybrid is "popular" precisely
   because it harnesses "strengths of both approaches" — the closest the paper comes
   to a recommendation.
4. **Each topology has a signature failure mode, and the mitigation literature is
   organised around it.** Sequential → error propagation (fix the query, self-correct,
   or verify externally). Parallel → inter-path conflict and compute waste (consensus
   filtering, capability-conditional aggregation, cheap pre-screening). Tree → memory,
   evaluator reliability, rollout cost (pruning/top-K, external or ensembled
   evaluation with delayed pruning, simulation-free MCTS). The authors' reading: these
   are *unique* to each structure, which is itself evidence that the structural axis
   carves the field at a real joint.
5. **Voting-based aggregation rests on an assumption the authors flag as shaky.**
   Self-Consistency and its universal variant "assume correctness correlates with
   frequency, an assumption that may not hold if popular but spurious reasoning paths
   dominate." Universal Self-Consistency's contribution is narrower than it looks: it
   removes the *exact-match* requirement, not the frequency assumption.
6. **LLM node evaluation in trees is biased, and self-evaluation is worse.** Using
   the generator as its own evaluator (RAP) invites **self-preference bias** — the
   model favouring text it believes to have low perplexity; using a different LLM
   (A*-Decoding) "may alleviate this bias but not other types of biases." The authors'
   reading: mitigation should combine self-evaluation with external signal (execution
   feedback, retrieved evidence), ensemble evaluations, or **delay aggressive pruning
   until later stages when more evidence is available**.
7. **Tree structures dominate on flexibility, and pay for it.** They alone can decide
   dynamically which subtask to solve next, backtrack, and prune. The cost triple in
   (4) is the price, and the authors treat efficiency — not capability — as the
   binding constraint on multi-path methods.
8. **Coverage asymmetries are themselves a finding.** Tree-structured RAG is "under-
   investigated"; type-2 (aggregate-all-leaves, HTN-style) trees are rare, with
   "most tree-based methods" being type-1 path-finding; multimodal tree reasoning is
   "limited." The authors read these gaps directly into their future-work section.

## Open questions the paper itself raises

The paper has **no limitations section**. Its self-identified open problems live in
Section 4, "Future Directions and Conclusions," and are three, in its own framing:

1. **Meta-reasoning: learning to select reasoning strategies.** The paper states
   plainly that "subtask selection and discovery remain challenging, especially when
   inputs are diverse: it is unclear **whether to decompose, to what granularity, and
   whether the sequential, the parallel, or the tree-based structure provides the best
   performance.**" Note the scope of that admission — it is the survey conceding that
   its own organising axis comes with no selection rule. Existing work relies on
   zero-shot prompting or supervised fine-tuning (Least-to-Most is the example given);
   the proposed direction is **meta-learning, "learning to reason."**
2. **Efficient multi-path reasoning.** Parallel and tree methods buy robustness and
   accuracy with inference cost. Two partial answers are acknowledged — lightweight
   models on branches (Speculative RAG) and value estimation replacing rollouts
   (I-MCTS) — and the authors say flatly that "efficiency remains an important open
   problem."
3. **Tree-based reasoning in multimodal and RAG systems.** The flexibility of tree
   search is under-exploited in exactly the two application columns the survey went
   out of its way to include. Extending it there "could unlock richer subtask
   structures and more reliable inference."

Open questions raised *in passing*, inside the body, that the conclusion does not
collect:

- Whether aggregation strategy should be **conditioned on model capability** — VLP's
  proposal that strong models synthesise directly while weak ones need a voting
  round is reported with "the potential for further research" attached.
- Whether **frequency tracks correctness** at all in consensus methods.
- How to get a **trustworthy node evaluator**: the paper names self-preference bias
  and "other types of biases" without characterising the latter, and its mitigations
  (external signal, ensembling, delayed pruning) are listed, not evaluated against
  each other.
- What the **right granularity** of a subtask is — raised in (1) and nowhere resolved.
- Whether the RL-induced **overlong-CoT** phenomenon is a decomposition failure or a
  training artefact; the paper cites it as a cost of LLM-assisted decomposition
  without settling which.

## Appreciation

Keeping **mechanism** separate from **magnitude**.

### Mechanism — what transfers as an argument

- **The axis itself.** Sorting inference-time techniques by *subproblem topology*
  rather than by domain, model, or year is a genuinely clarifying move, and the paper
  makes it stick: once you accept the frame, CoT/BSM/ToT stop being three
  techniques and become three settings of one dial. That is a reusable frame, not a
  result, and it survives independent of any number in the literature.
- **The three-way topology, with Figure 2's precision.** The definitions are sharper
  than the labels suggest and the distinctions are the operative ones: *sequential*
  may branch at decision points but never backtracks; *parallel* fixes all paths at
  the start, forbids further branching, and aggregates only at the end; *tree* alone
  permits dynamic reordering, backtracking, and pruning. Framed that way the axis is
  really **when commitment happens and whether it can be undone**, which is a
  mechanism claim that transfers cleanly.
- **The two tree types.** Path-finding trees (children are *competing* solutions, one
  root-to-leaf path is the answer) versus HTN-style trees (leaves are *complementary*
  subtasks, all must be visited and combined). These are structurally different
  systems that the shared word "tree" hides, and the survey is right that visit order
  matters enormously in the first and hardly at all in the second. This distinction is
  the most portable thing in the paper.
- **The concern/mitigation triples.** Error propagation is the sequential tax; path
  conflict and compute waste are the parallel taxes; memory, evaluator reliability,
  and rollout cost are the tree taxes. As a checklist of *what each shape will cost
  you*, this is sound reasoning from structure and does not depend on any benchmark.
- **The self-preference-bias point.** That a generator scoring its own nodes is a
  biased evaluator is a mechanism argument with a cited basis, and it bites hardest
  exactly where trees need it most — at the pruning decision. The corollary the paper
  draws — **delay aggressive pruning until evidence accumulates** — follows from the
  mechanism rather than from measurement.
- **The frequency-correctness caveat.** "Correctness correlates with frequency" is an
  assumption, and naming it as one is an argument that transfers.
- **Decomposition automation as a variance trade.** Fixed human structure reduces
  variance and permits blind-spot correction; model-generated structure adapts per
  input and risks omission. This is a real trade and stated as one.

### Magnitude — numbers valid only inside their own setup, or absent

- **There are no magnitudes here at all.** The paper reports no accuracy, no compute,
  no scaling curve, no cost ratio. Anything quantitative must be fetched from the
  primary papers; nothing in this survey can be cited for a number.
- **Comparative verbs are inherited, not verified.** "Yields stronger performance
  than Flamingo," "significant contribution to performance," "scaling the number of
  captions improves accuracy," "improves inference efficiency" — every one of these
  is one paper's claim at that paper's models, prompts, and benchmarks, passed
  through without requalification. Several concern 2022–2023-era VLMs and may not
  survive a change of backbone.
- **"Structure is critical to performance"** is the thesis, and it is *argued from
  theoretical CS*, not measured on LLMs. Divide-and-conquer mattering for sorting
  algorithms is not evidence that topology dominates for a sampled language model.
  The one hard formal claim (Li et al. 2024d: CoT tokens extend what a constant-depth
  Transformer can solve) supports "serial computation buys expressivity" — a much
  narrower proposition than "the topology you choose is critical."
- **No topology is ranked.** The paper cannot be cited for sequential-vs-parallel-vs-
  tree superiority on anything. It says the choice matters and lists what each costs.

### Craft notes

Short and readable; the definitions are unusually careful for a survey. Against that:
"we identify **four** major types" introduces a list of three — an uncorrected
editing defect in the paper's most load-bearing sentence. Wei et al. 2022a and 2022b
are the same paper duplicated in the bibliography, cited in both forms. Rewrite-
Retrieve-Read and In-Context RALM are both attributed to "Ma et al. (2023)" in the
same paragraph, which reads as a citation collision. Section 2 and Section 3 overlap
substantially — Self-Refine, Step-Back, Self-RAG, FLARE, and Xie et al. are each
described twice — because the two axes are presented sequentially rather than
crossed, and there is no table crossing them. Figure 1 is said to categorise methods
by both reasoning path and decomposition method, so the cross-tabulation exists only
as an image, not as extractable text.

## How it could serve a harness-design effort — limitations, major concerns

Stemming the discussion, not resolving it.

**What it offers a harness designer.**

- A **vocabulary for the control-flow decision**. If a harness can split work, the
  question "sequential, parallel, or tree?" is exactly this paper's axis, and its
  definitions are precise enough to act on: does a step commit irrevocably (no
  backtracking, sequential); are all branches fixed at the start and merged at the end
  (parallel); or can the system reorder, abandon, and resume (tree)? Read as a
  *commitment/reversibility* question, this maps onto scheduler design directly.
- A **failure-mode checklist keyed to shape**. Choosing a shape means accepting its
  tax. Sequential harnesses need query repair, self-check, or external validation
  because errors propagate. Parallel harnesses need an aggregation policy and a
  budget policy, because paths conflict and compute is spent on all of them. Tree
  harnesses need node storage, a pruning policy, and — the sharp one — an evaluator
  they can trust.
- The **evaluator problem, stated crisply**. Any harness that prunes, ranks, or
  scores its own intermediate states is running an LLM judge, and the survey's point
  is that using the *same* model that generated the state introduces self-preference
  bias, while swapping in a different model removes only that bias. The mitigations
  it names — external execution/retrieval signal, ensembled evaluation, and delaying
  aggressive pruning until evidence accumulates — are design levers, and the last is
  a scheduling policy more than a model choice.
- The **decomposition-authorship trade**, stated as a variance question: a fixed
  human-specified pipeline reduces variance and lets the designer insert steps for
  weaknesses the model cannot see in itself; a model-authored decomposition adapts to
  the input and risks omitting or inventing steps. The hybrid pattern the paper calls
  popular — human outline, model refinement of the leaves — is the pattern a harness
  with a fixed skeleton and flexible interiors already instantiates.
- **RAG-as-decomposition** is a reframing worth having: any capability whose use is
  hardwired to a slot in the pipeline is a decomposition decision the designer
  already made, whether or not it was thought of that way.

**Limitations that bound how far it can be taken.**

- **No numbers, so no cost model.** The Subject's question of whether splitting's
  coordination cost is offset is precisely what this paper does not answer. It names
  cost as a concern for parallel and tree structures and calls efficiency an open
  problem; it quantifies nothing. Any budget decision needs the primary papers.
- **No selection rule** — and the paper says so itself, in its first future direction:
  whether to decompose, at what granularity, and which topology, are all unresolved.
  A designer gets a taxonomy, not a decision procedure.
- **Depth is barely addressed.** The Subject's axis of what sets recursion depth
  appears here only obliquely, as tree-growth restriction, beam width, and how much to
  prune. There is no treatment of hierarchy depth as a design variable in its own
  right, and no discussion of deep sub-agent hierarchies.
- **Recombination is thin.** For parallel structures the paper gets as far as voting
  versus LLM synthesis versus capability-conditional aggregation. For sequential
  structures the merge is implicit in the chain. For type-2 trees — where aggregation
  is the whole point — it discusses one method. If recombination is where a harness
  loses information, this survey is not where that is characterised.
- **Single-model framing.** The subject matter is one model given more compute, not a
  system of agents with separate contexts, tools, and memories. Coordination overhead
  between actors, context handoff, and state isolation are not this paper's concerns.
  ChatDev appears once as a decomposition example, not as an architecture.
- **Provenance of every comparative claim is one primary paper**, mostly small-scale
  and often on 2022–2024 backbones. Nothing was reproduced, aggregated, or
  meta-analysed for this survey.

**Major concerns.**

- The **central thesis is asserted, not demonstrated.** "Subproblem structure is
  critical to performance" is supported by an analogy to classical algorithms plus one
  expressivity theorem about serial tokens. A harness effort that treats topology as
  the dominant lever on the strength of this paper would be over-reading it — and the
  paper's own future-work section concedes it cannot say which topology wins when.
- The taxonomy risks becoming **a filing system that flattens real differences**.
  "Parallel" covers both Self-Consistency (same prompt, N samples, vote) and
  Branch-Solve-Merge (genuinely different subproblems, merged) — one is variance
  reduction, the other is division of labour, and the shared box implies a kinship
  that may not be operationally real.
- **Nothing here addresses when *not* to decompose.** Every technique surveyed is one
  that splits; a survey organised by splitting structure has no natural place for a
  finding that splitting hurt. Sprague et al. is cited for CoT helping mainly on math
  and symbolic reasoning, but that qualification is not carried into the taxonomy's
  conclusions.
- The **editing defects** ("four major types" introducing three; a duplicated
  bibliography entry; a citation collision) are minor individually but sit in the
  paper's load-bearing sentences, and this is a v1 preprint with no venue vetting.

## Five citations worth chasing next

1. **Li, Liu, Zhou, Ma (2024d), "Chain of thought empowers transformers to solve
   inherently serial problems," ICLR.** The survey's only formal-power result, and the
   nearest thing it has to evidence that structure changes what is computable rather
   than just what is accurate. Load-bearing under the whole thesis; worth checking
   what it actually proves and under what assumptions.
2. **Saha, Levy, Celikyilmaz, Bansal, Weston, Li (2024), "Branch-Solve-Merge improves
   large language model evaluation and generation," NAACL.** The paper's exemplar of
   *genuine* parallel decomposition — explicit split into different subproblems, then
   merge — as opposed to sampling-and-voting. The place to look for what the merge
   step actually costs and how it is implemented.
3. **Kim, Kim, Jeon, Park, Kang (2023), "Tree of Clarifications," EMNLP.** The
   survey's sole worked example of the *second* tree type, where all leaves must be
   aggregated rather than one path selected. If the HTN-style tree is the interesting
   structure for hierarchical task systems, this is the one instance the survey
   documents.
4. **Zhou, Schärli, Hou, Wei, Scales, Wang, Schuurmans, Cui, Bousquet, Le, Chi (2023),
   "Least-to-most prompting enables complex reasoning in large language models."**
   The canonical *explicit* LLM-assisted decomposition, named again in the future-work
   section as the state of the art in strategy selection. The reference point for what
   model-authored decomposition does and where it breaks.
5. **Wataoka, Takahashi, Ri (2025), "Self-preference bias in LLM-as-a-judge."** The
   basis for the survey's sharpest mechanism claim — that a model scoring its own
   intermediate states prefers text it finds low-perplexity. Directly relevant to any
   system that prunes or ranks its own work.

*Runners-up, noted:* Sprague et al. (2024), "To CoT or not to CoT?" — the boundary of
where sequential decomposition helps at all; and Wang et al. (2024b), Speculative RAG
— the survey's example of buying multi-path robustness at reduced cost.
