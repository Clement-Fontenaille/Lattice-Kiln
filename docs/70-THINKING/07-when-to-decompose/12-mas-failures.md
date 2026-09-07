# Why Do Multi-Agent LLM Systems Fail?

## Density

**Density: MEDIUM** — the paper is almost entirely load-bearing (a taxonomy, a 1642-trace annotated corpus, an annotator validation, two intervention studies, with little padding), but only part of that signal touches the Subject: it gives a well-grounded vocabulary and prevalence estimates for coordination and verification failures, yet never treats decomposition itself as a variable — depth, split policy, and the cost of splitting are nowhere measured.

**Keywords (mine):** failure taxonomy · multi-agent LLM systems · grounded theory · trace annotation · LLM-as-a-judge · inter-agent misalignment · verification failure · handoff loss · coordination overhead · system design over model capability

**Year:** 2025 (arXiv v3, 26 Oct 2025; v1 March 2025). **Venue:** NeurIPS 2025 (peer-reviewed). **arXiv:** 2503.13657 [cs.AI], CC BY-NC-ND 4.0.

**Authors:** Mert Cemri, Melissa Z. Pan, Shuyi Yang, Lakshya A. Agrawal, Bhavya Chopra, Rishabh Tiwari, Kurt Keutzer, Aditya Parameswaran, Dan Klein, Kannan Ramchandran, Matei Zaharia, Joseph E. Gonzalez, Ion Stoica (UC Berkeley; one author affiliated with Intesa Sanpaolo).

## Approach

The paper is a diagnostic study, not a method paper. It asks why multi-agent LLM systems (MAS) fail and answers with three artefacts: a taxonomy, a dataset, and an automated annotator.

1. **Grounded-theory trace analysis.** Six expert annotators read 150+ execution traces (each averaging >15,000 lines) drawn from five MAS frameworks (HyperAgent, AppWorld, AG2, ChatDev, MetaGPT) over programming and math tasks, selected by theoretical sampling. They used open coding, constant comparative analysis, memoing and theorising, iterating until theoretical saturation — no predefined hypotheses. Over 20 hours of annotation per expert at this stage.
2. **MAST, the taxonomy.** The emergent labels are consolidated into 14 failure modes in 3 categories, each mode mapped to the execution stage (pre-execution / execution / post-execution) where its root cause typically arises:
   - **FC1 System Design Issues** — FM-1.1 disobey task specification; FM-1.2 disobey role specification; FM-1.3 step repetition; FM-1.4 loss of conversation history (unexpected context truncation, reverting to an earlier conversational state); FM-1.5 unaware of termination conditions.
   - **FC2 Inter-Agent Misalignment** — FM-2.1 conversation reset; FM-2.2 fail to ask for clarification; FM-2.3 task derailment; FM-2.4 information withholding (an agent holds data that would change another agent's decision and does not pass it); FM-2.5 ignored other agent's input; FM-2.6 reasoning-action mismatch.
   - **FC3 Task Verification** — FM-3.1 premature termination; FM-3.2 no or incomplete verification; FM-3.3 incorrect verification.
   Definitions were hardened through three rounds of inter-annotator agreement (three annotators, five randomly drawn traces per round, disagreements resolved in discussion, ~10 hours of resolution alone), refining, merging and adding modes until Cohen's κ = 0.88.
3. **LLM-as-a-judge annotator.** An o1-based pipeline is prompted with a trace, the MAST definitions, and few-shot examples from the human-annotated set, and emits per-mode labels plus a textual reason. Validated against held-out human labels, then re-validated on two unseen systems (OpenManus, Magentic-One) and two unseen benchmarks (MMLU, GAIA), κ = 0.79 with no taxonomy changes.
4. **MAST-Data.** The validated annotator is run at scale to produce 1642 annotated traces across 7 frameworks and four model families, released publicly, alongside MAST-Data-human (21 human-annotated traces from the IAA studies) and a `pip install agentdash` library wrapping the annotator.
5. **Interventions.** Two case studies apply "tactical" fixes (prompt restructuring with an explicit verification section; role respecialisation into Problem Solver / Coder / Verifier where only the Verifier may terminate; and for ChatDev, enforcing that only superior agents close a conversation, plus a DAG→cyclic topology change gated on CTO sign-off with an iteration cutoff), then re-run MAST to show which failure modes moved.

Framing throughout: MAS failures are treated as **organisational** rather than purely model-capability problems, with an explicit analogy to high-reliability-organisation theory — even organisations of capable individuals fail if the structure is flawed.

## Models targeted and benchmarks / datasets used

**Models.** GPT-4, GPT-4o, GPT-4o-mini; Claude-3.7-Sonnet; Qwen2.5-Coder-32B-Instruct and CodeLlama-7b-Instruct-hf (open-source arm, Appendix I); OpenAI o1 as the annotator model. Four model families in total.

**MAS frameworks (7), with the architectures the paper assigns them.**

| Framework | Architecture (paper's label) | Shape of the decomposition |
| --- | --- | --- |
| MetaGPT | Assembly line | SOP-encoded roles in a software company, fixed pipeline |
| ChatDev | Hierarchical workflow | design / coding / testing phases, each split into sub-tasks; each sub-task is an orchestrator–assistant pair holding a multi-turn conversation terminated by a sentinel |
| HyperAgent | Hierarchical workflow | Planner decomposes into subtasks published to queues; Navigator / Editor / Executor child agents consume them asynchronously and in parallel; Planner→child messages use a fixed two-field schema (Context, Request) |
| AppWorld | Star topology | supervisor holds user credentials and converses one-on-one with per-service tool agents that must ask it for what they need |
| AG2 (formerly AutoGen), MathChat scenario | agentic framework, flexible patterns | Student + code-executing Assistant; in the intervention, Problem Solver / Coder / Verifier |
| Magentic-One | Star topology | generalist orchestrator over web/file agents |
| OpenManus | Hierarchical | open-source generalist agent framework |

Manus is examined as a closed-source system (60% success on ProgramDev by human evaluation) but excluded from MAST-Data: the underlying model is undisclosed and full traces are unavailable, so fine-grained annotation is infeasible.

**Benchmarks.** ProgramDev (30 authored coding tasks — Tic-Tac-Toe, Chess, Sudoku and similar, deliberately easy so that failure dynamics rather than task difficulty dominate), ProgramDev-v2 (100 tasks, used for the model/architecture comparisons), ProgramDev-v0 (32 tasks, ChatDev case study), SWE-Bench Lite, AppWorld Test-C, GSM-Plus (adversarially perturbed GSM8K), OlympiadBench, MMLU, GAIA, HumanEval.

**Trace budget.** 7×30 = 210 traces with human evaluation, human annotation and LLM annotation; 700 LLM-annotated traces on ProgramDev-v2 across model/framework cells (100 each); 732 traces on AG2/Magentic-One across OlympiadBench (206), GSM-Plus (193), MMLU (168) and GAIA (165) with human-evaluated task completion plus LLM annotation. Total 1642. Measured failure rates of the seven systems run 41%–86.7%.

## Author incentive

Twelve of the thirteen authors are UC Berkeley, including a cluster of senior systems and ML faculty (Stoica, Gonzalez, Zaharia, Klein, Keutzer, Parameswaran, Ramchandran); one author is at Intesa Sanpaolo. No funding statement appears in the arXiv HTML.

The stake is positional rather than commercial-in-paper. Three things are being claimed: **priority** ("the first empirically grounded taxonomy of MAS failures", "the first multi-agent system dataset"), **a standard** — MAST is offered as the shared vocabulary the field should annotate in, shipped as a pip package (`agentdash`) and a HuggingFace dataset to make adoption cheap — and **a thesis**: that MAS reliability is primarily a systems-design problem, not a base-model problem. That last one is the house view of a systems lab, and it is the conclusion the paper's own evidence is arranged to support; the alternative reading (that failures are dominated by model limits and will erode with capability) is acknowledged in one paragraph and set aside as conjecture ("we conjecture that improvements in the base model capabilities will be insufficient").

Mitigating factors: none of the seven evaluated frameworks is the authors' own, so the finding that they fail 41–86.7% of the time is not self-favouring; the artefacts are released; and the paper repeatedly declines to claim exhaustiveness ("we do not claim it covers every potential failure pattern"). Two of the systems-y references in the intro (Gorilla, MemGPT) are co-authors' own work, which is normal self-citation rather than a load-bearing conflict.

## Measurement methodology (brushed)

**Dependent variable.** Not performance. The primary DV is the *presence of each of 14 failure-mode labels in an execution trace*, assigned by annotators (human or LLM) reading the trace. A secondary DV, task success, is human-evaluated ("HE") for the 210-trace core and for the four larger AG2/Magentic-One cells, and is used in the interventions and in the fatality analysis.

**N.** 1642 traces for MAST-Data. But the numbers do different work at different scales, and the taxonomy's credibility rests on much smaller Ns than the headline: the taxonomy itself emerges from 150 traces read by 6 experts; the definitional agreement κ = 0.88 comes from 3 annotators over 3 rounds of 5 traces (15 traces total); MAST-Data-human is 21 traces; the out-of-domain generalisation check (κ = 0.79) is one further IAA round on unseen systems. Everything above ~200 traces is LLM-annotated.

**What is controlled.** Comparisons are one-factor-at-a-time within a fixed cell: model held fixed while framework varies (MetaGPT vs ChatDev, both GPT-4o, ProgramDev-v2); framework held fixed while model varies (MetaGPT with GPT-4o vs Claude-3.7-Sonnet); framework and model held fixed while benchmark varies (AG2/GPT-4o over GSM, MMLU, Olympiad). What is *not* controlled is the cross-system comparison a reader most wants: the paper states outright that Figure 4's per-system profiles are drawn on different benchmarks and are "not intended to serve as a performance comparison across MAS", and Figure 5's failure rates carry the same disclaimer. So framework identity and task difficulty are confounded everywhere except inside those three designed contrasts.

**How the prevalence percentages are constructed.** The headline per-mode figures (FM-1.3 15.7%, FM-2.6 13.2%, FM-1.5 12.4%, FM-1.1 11.8%, FM-3.3 9.10%, FM-3.2 8.20%, FM-2.3 7.40%, FM-2.2 6.80%, FM-3.1 6.20%, FM-1.4 2.80%, FM-2.1 2.20%, FM-2.5 1.90%, FM-1.2 1.5%, FM-2.4 0.85%) sum to ~100 across the 14 modes, as do the category shares (FC1 ≈ 44%, FC2 ≈ 32%, FC3 ≈ 24%). They are therefore **shares of annotated failure-mode instances across 1642 traces, not the fraction of traces exhibiting each mode**. That matters: the percentages support statements of the form "of everything that goes wrong, this much is coordination", and do not support "X% of runs suffer this". Appendix J reports per-trace occurrence rates for a small subset (ChatDev/MetaGPT, success vs failure), and there FM-1.1 alone runs 16.7–33.3% of traces — a different scale entirely.

**Annotator reliability.** Human–human κ = 0.88 after refinement; human–LLM κ = 0.77 with accuracy 0.94, recall 0.77, precision 0.833, F1 0.80 (few-shot o1; zero-shot is markedly worse at κ = 0.58, recall 0.62). Two consequences the paper is partly candid about. First, accuracy 0.94 is flattered by class imbalance over 14 mostly-absent binary labels; recall 0.77 is the number that governs prevalence estimates, and it implies systematic undercounting. Second, Appendix E reports inter-*mode* correlations up to 0.63 for symptomatically similar modes, and the paper concedes this "might lead automated evaluators to conflate distinct root causes" — precisely the modes (1.4 context loss vs 2.4 withholding vs 2.5 ignoring input) whose distinction carries the coordination argument. Category-level correlations are low (0.17–0.32), which supports the three-way split but not the fine-grained one.

**Significance.** Treated seriously in exactly one place: the AG2 case study, 200 GSM-Plus problems, 6 repetitions, Wilcoxon signed-rank — improved prompt beats baseline with GPT-4 (84.75±1.94 → 89.75±1.44), the new topology does not (85.50±1.18, p = 0.4, explicitly reported as not significant), while with GPT-4o both interventions reach p = 0.03. The ChatDev results (ProgramDev-v0 25.0 → 34.4 → 40.6; HumanEval 89.6 → 90.3 → 91.5) are single-run point estimates with no test and no error bars. All taxonomy prevalence numbers, all model/architecture comparisons, and all the failure-distribution figures are descriptive: no confidence intervals, no tests, no multiple-comparison correction over 14 modes.

**Annotation cost**, reported for reproducibility: $1.8 average per trace with the o1 annotator, from $0.374 (AppWorld) to $4.14 (OpenManus), scaling with trace length.

## Key findings

**1. The seven systems fail most of the time.** Measured failure rates of 41%-86.7% across the seven SOTA open-source MAS on their respective benchmarks. The paper opens from the premise — citing Agentless and Kapoor et al. rather than measuring it itself — that MAS gains over single-agent or best-of-N baselines are often minimal.

**2. Failures partition roughly 44 / 32 / 24 across design, coordination, and verification.** By share of annotated failure instances: FC1 System Design ≈ 44%, FC2 Inter-Agent Misalignment ≈ 32%, FC3 Task Verification ≈ 24%. Category correlations are low (0.17-0.32), which the authors read as evidence the three capture genuinely distinct things.

**3. Which modes bear on splitting, passing, and recombining — the Subject's angle.** Reading the 14 modes against decomposition mechanics rather than the paper's own three-way grouping:

- *Handing work down (the split itself).* FM-1.1 disobey task specification (11.8%) and FM-1.2 disobey role specification (1.5%) are, in the authors' analysis, not mere instruction-following weakness — they trace them to how the system apportions roles and interprets a high-level objective. The ChatDev Wordle example is the demonstration: the system produces a fixed word bank; sharpening the *user* prompt to forbid a fixed bank produces code with a fixed list plus new errors. The defect is in the system's interpretation-and-delegation machinery, not in the wording of the request. Improving role specification alone bought +9.4% success.
- *Redundant or wasted split work.* FM-1.3 step repetition is the single largest mode at 15.7% — agents redoing work already done. This is the closest thing in the paper to a direct measurement of coordination waste, and it is the top failure mode overall.
- *Passing information between agents.* FM-2.4 information withholding (0.85%), FM-2.5 ignored other agent's input (1.90%), FM-2.2 fail to ask for clarification (6.80%), FM-2.1 conversation reset (2.20%), FM-1.4 loss of conversation history (2.80%) — about 14.6% of failure instances are strictly about state crossing an agent boundary and not arriving, or arriving and being disregarded. Add FM-2.3 task derailment (7.40%), the gradual drift of a sub-agent off the objective it was handed, and it is ~22%.
- *Putting results back together / accepting them.* All of FC3 (~24%): FM-3.1 premature termination (6.20%) — the run ends before the information needed has been exchanged; FM-3.2 no or incomplete verification (8.20%); FM-3.3 incorrect verification (9.10%). Plus FM-1.5 unaware of termination conditions (12.4%), the mirror image: not recognising the work is done. Termination-boundary errors in both directions total ~18.6%.
- *Neither.* FM-2.6 reasoning-action mismatch (13.2%) is largely a single-agent pathology that the taxonomy files under coordination.

So on a decomposition reading, roughly two-thirds of annotated failure instances sit at seams — delegation, handoff, drift, termination, acceptance — rather than in an agent's local competence at its own sub-task.

**4. Prevalence and fatality are different things (Appendix J).** With task success withheld from the annotator: failures appear in *successful* traces too, but at lower frequency. FM-1.5 (unaware of termination conditions) and FM-2.4 (information withholding) appear almost exclusively in failed runs — rare but close to fatal. FM-3.2 and FM-3.3 (the verification modes) appear frequently in *successful* runs — common, systemic, but survivable on any given task. The rarest mode in the taxonomy, FM-2.4 at 0.85%, is the one the paper chose for its illustrative figure (a Phone Agent never tells the Supervisor the username format; the Supervisor never asks; logins fail repeatedly and the task dies) — the authors clearly regard low frequency and low importance as unrelated.

**5. Architecture shapes the failure profile, and the trade is not free.** MetaGPT vs ChatDev, both GPT-4o, same benchmark: MetaGPT has 60-68% fewer FC1 and FC2 failures but 1.56x more FC3. The authors attribute this to MetaGPT encoding adherence through SOPs while ChatDev spends architecture on explicit review and testing phases. Model choice moves the profile too (GPT-4o vs Claude-3.7-Sonnet in MetaGPT: 39% fewer FC1 for GPT-4o), but FC3 stays high for both — verification is the residue no model choice removes. System-specific profiles are legible and idiosyncratic: AppWorld's star topology with no predefined workflow yields premature terminations; OpenManus repeats steps; HyperAgent repeats steps and mis-verifies.

**6. Harder benchmarks fail more, and differently.** AG2/GPT-4o across GSM to MMLU to Olympiad: FC1 0.53, 1.06, 1.19 and FC3 0.37, 0.60, 0.67 per trace. FC2 is flat-to-inverted (1.33, 1.01, 1.21), with GSM showing the *most* inter-agent misalignment per trace despite being the easiest benchmark.

**7. Open-source models fail far more, and unevenly.** Over 400 traces, Qwen2.5-Coder-32B is substantially more robust than CodeLlama-7b, and both trail GPT-4o and Claude-3.7. The gap is not uniform across modes: CodeLlama's context-loss (46 and 23 per 100 traces) and conversation-reset (50 and 9) counts are an order of magnitude above Qwen's (1/0 and 2/0) — weaker models fail at the handoff specifically, not just globally.

**8. Interventions help and do not suffice.** Prompt and topology fixes give up to +15.6% (ChatDev, adding high-level objective verification) and +9.4% (role hierarchy — only superior agents may close a conversation); AG2's re-topology is significant with GPT-4o and not with GPT-4 (p = 0.4). Post-intervention MAST re-annotation shows failure counts falling across modes, and the authors judge topology changes more effective than prompt changes for both systems.

### The authors' own reading

They read the whole picture as evidence for **the primacy of system design over model capability**: many failures "arise from the challenges in organizational design and agent coordination rather than the limitations of individual agents", and they conjecture base-model improvement will not close MAST. Their supporting move is the organisational analogy — capable individuals in a badly structured organisation fail catastrophically, and high-reliability-organisation theory says structure can prevent it.

On FC2 specifically they make a sharper claim: since the misalignments they observe occur *between agents inside one framework speaking natural language to each other*, protocol standardisation (MCP, A2A) addresses the wrong layer. They name the underlying problem as a collapse of theory of mind — agents failing to model what other agents need to know — and expect it to need both architectural change and model-level training, since base LLMs are not pre-trained for inter-agent dynamics.

On FC3 they are blunt that existing verifiers do superficial work despite being prompted otherwise (compilation checks, leftover TODOs), and that a verifier's presence is no silver bullet: a ChatDev chess program passes review and is unplayable because nothing checks it against the rules of chess. Their prescription borrows from software practice — external knowledge, testing output collected throughout generation, multi-level checks against both low-level correctness and high-level objectives.

They also position MAST as a *development tool*, not only an analysis: aggregate success rates hide which intervention did what, and a per-mode breakdown shows both what an intervention fixed and what it traded away.

## Open questions the paper itself raises

The paper has no dedicated Limitations section; its caveats are distributed and stated in passing, which is itself worth noting. Collected in its own framing:

- **The taxonomy is not claimed exhaustive.** Stated three separate times: MAST is "a foundational first step", "we do not claim it covers every potential failure pattern", derived by saturation over one sample of systems and two task families.
- **Fine-grained modes may be beyond automated annotation.** The authors flag that inter-mode correlations up to 0.63 for symptomatically similar modes "might lead automated evaluators to conflate distinct root causes", i.e. their own scaling instrument may be blurring exactly the distinctions the taxonomy exists to draw.
- **Tactical fixes are inconsistent and insufficient.** Repeatedly: interventions "do not constitute substantial improvements", their effectiveness "varies based on factors such as the underlying LLM", "not all failure modes are resolved, and task completion rates still remain low". They call for structural redesign and combinatorial changes spanning organisation and model level (their Table 4 maps strategies onto categories).
- **Universal verification is an open problem.** They state that no universal verification mechanism exists, that even in coding full edge-case coverage is hard for experts, and that verification is domain-shaped (test coverage for code, certified data for QA, symbolic validation for reasoning) — "adapting verification across domains remains an ongoing research challenge".
- **Communication needs more than a protocol.** Standardised message formats are named as necessary but not sufficient; the open item is the *content* of agent messages and agents' ability to infer another agent's informational needs, possibly via targeted training. They flag graph-attention, attentional-communication and learned selective-communication work, and RL fine-tuning for role adherence (MAPPO, SHPPO, Optima), as directions rather than results.
- **Uncertainty quantification is untried here.** Proposed, not tested: confidence thresholds gating action, agents pausing to gather information below threshold, adaptive thresholds.
- **Memory and state management is single-agent-shaped.** They note most work (MemGPT, TapeAgents) targets single agents and that the multi-agent case is open.
- **Closed-source systems cannot be studied this way.** Undisclosed models and unavailable traces make fine-grained annotation infeasible, so the corpus is structurally biased toward open systems.
- **No one-size-fits-all.** Because profiles are system-specific, they explicitly decline to prescribe a single remedy.

## Appreciation

### Mechanism — what transfers as an argument

- **The seams are where multi-agent systems break, and the failure vocabulary for seams is now specific.** The strongest transferable contribution is that "coordination cost" can be decomposed into named, separately observable defects: work redone (1.3), state not passed (2.4), state passed and ignored (2.5), state lost (1.4, 2.1), ambiguity not resolved (2.2), sub-goal drift (2.3), stopping too early (3.1), not knowing to stop (1.5), and accepting bad output (3.2, 3.3). Anyone reasoning about whether to split a task now has a checklist of what splitting costs, and the list was derived bottom-up from traces rather than posited.
- **Termination is a two-sided failure and both sides are common.** That not-knowing-to-stop (12.4%) and stopping-too-soon (6.2%) are separately large is a genuinely useful structural point: a decomposition scheme needs an explicit completion predicate, and getting it wrong in either direction is roughly as likely as any other single failure.
- **Verification is a residue that model quality does not remove.** FC3 stays high across GPT-4o, Claude-3.7, and both open-source models, and the framework that spends architecture on verification (ChatDev) buys fewer FC3 failures at the cost of more FC1/FC2. That trade — you can move failures between categories by moving architecture, but not obviously reduce the total — is the paper's most interesting mechanism claim, and it is visible in the design that holds model fixed.
- **Rarity does not imply harmlessness.** The fatality analysis (some modes appear almost only in failed runs; verification modes appear in successful ones) is methodologically the right move and should discipline how any prevalence table is used.
- **Prompt-sharpening does not repair a delegation defect.** The Wordle example is a small but clean mechanism demonstration: making the user request more explicit produced the same violation plus new errors, which locates the defect in how the objective is decomposed and handed on.
- **Weak models fail at the seam disproportionately.** The CodeLlama-vs-Qwen split on context loss and conversation reset supports a claim the paper does not itself make: coordination overhead is not a fixed tax, it scales with how weak the participating agents are.

### Magnitude — numbers valid only inside this setup

- **Every percentage in the taxonomy figure.** They are shares of failure instances in one corpus whose composition (which framework, which benchmark, how many traces each) was set by convenience and by the availability of open traces, not by any sampling frame over deployed systems. FC1 44% / FC2 32% / FC3 24% describes MAST-Data, not multi-agent systems.
- **Anything sensitive to annotator recall.** Recall 0.77 means roughly a quarter of true instances go unlabelled, and there is no reason to think that loss is uniform across modes — modes whose evidence is diffuse across a long trace (withholding, drift) are exactly the ones a judge is likeliest to miss. FM-2.4 at 0.85% is indistinguishable from annotator noise.
- **All cross-framework comparisons.** The paper says so itself twice. The 41-86.7% range mixes SWE-Bench Lite, GAIA, AppWorld and a bespoke 30-task coding set.
- **The intervention deltas.** +15.6% and +9.4% are single-configuration, mostly single-run point estimates on small bespoke benchmarks (32 and 30 tasks); the one place a proper test is run, one intervention fails significance outright (p = 0.4) and flips to significant when the model changes. Treat these as existence proofs that structural change moves the needle, not as effect sizes.
- **"Topology changes beat prompt changes."** Asserted from post-intervention failure-count figures, with the AG2 accuracy table pointing the other way for GPT-4 (improved prompt 89.75 vs new topology 85.50). Not established.
- **The 39% / 60-68% / 1.56x model and architecture contrasts.** Ratios of small annotated counts in single cells, no intervals.

### On the paper's central thesis

"System design over model capability" is well-motivated but not tested. The evidence offered for it is that interventions holding the model fixed produce gains — which shows design *matters*, not that it dominates. The counter-evidence sits in the paper's own appendices: swapping CodeLlama for Qwen moves failure counts far more than any intervention does, and GPT-4o vs Claude-3.7 shifts FC1 by 39% with the architecture unchanged. A fair reading of their own data is that model and structure both move failures substantially, and the paper does not have a design that separates their contributions.

## How it could serve a harness-design effort — limitations, major concerns

*Stemming the discussion rather than resolving it.*

**What it can be used for.**

- **As an instrument, not a result.** The most directly usable output is the annotator: a released pipeline that reads a trace and returns per-mode labels with justifications, at ~$1.8/trace, validated at κ = 0.77 against experts and shown to hold on two systems it was not developed on. A harness effort that wants to know whether its own decomposition is leaking at the seams can measure that on its own traces rather than importing this paper's percentages. The paper's own case studies model the loop: annotate, intervene, re-annotate, read the per-mode delta including what got worse.
- **As a design checklist for a split.** Each mode implies a question to ask of any decomposition scheme before building it: is there a completion predicate the sub-agent can evaluate (1.5, 3.1)? does the handoff carry the state the receiver needs, and does the sender know what that is (2.4, 2.2)? can a sub-agent tell it is drifting from the parent objective (2.3)? what detects that two agents did the same work (1.3)? who is allowed to declare the work done, and can a subordinate do it unilaterally (1.2, the ChatDev CEO/CPO fix)? what checks the recombined result against the original objective rather than against surface properties (3.2, the chess program that compiles and is unplayable)?
- **As evidence that the acceptance step deserves its own architecture.** FC3 is the category that survives model improvement, and the paper's largest single intervention gain (+15.6%) came from adding a high-level objective verification step. If a harness treats recombination as concatenation plus a light review pass, this paper is a direct argument that the review pass will be superficial by default even when instructed otherwise.
- **As a caution against protocol-level solutions.** The observation that misalignment persists among agents in one framework sharing a message format suggests that schema work (typed handoffs, structured envelopes) is necessary but will not by itself fix what the paper calls the theory-of-mind collapse. Open question: whether the HyperAgent-style fixed two-field message (Context, Request) helps measurably — the paper describes that design but never isolates its effect.

**Limitations that bound the transfer.**

- **It never varies decomposition.** No arm compares depths of splitting, split policies, or a single agent against the same work decomposed. The frameworks in the corpus embody fixed decomposition choices as part of their identity, and identity is confounded with benchmark. So the paper cannot say whether splitting caused these failures, only that they occur in systems that split. For the Subject's central question — the size of the coordination cost and whether it is offset — the paper inherits its premise ("gains are often minimal") from Agentless and Kapoor et al. rather than measuring it.
- **The corpus is 2024-25 framework-shaped.** ChatDev's phase pipeline, MetaGPT's SOPs, AppWorld's supervisor-plus-service-agents: these are elaborate role-play architectures. How much of FC1 and FC2 is intrinsic to splitting work versus an artefact of asking a model to impersonate a CEO is not separable here, and a leaner harness (a parent agent spawning narrow, short-lived sub-agents with explicit returns) may not inherit the same distribution.
- **Trace-derived labels are symptom labels.** Despite root-cause language, what an annotator sees is a behaviour in a transcript. The paper's own correlation analysis concedes that different root causes produce similar surface behaviour, and its example of the difficulty — distinguishing withholding from ignoring from context loss — is the coordination cluster.
- **The prevalence table invites misuse.** It is a share-of-instances distribution over a convenience corpus. Quoting "32% of MAS failures are coordination failures" as a general fact would be a misreading of the paper's own construction.
- **Failure counts are not a cost model.** Nothing here prices the extra calls, latency, or tokens that splitting adds; the only cost figure in the paper is the annotator's API bill. A harness effort weighing whether to split still has no magnitude for the overhead side of the ledger from this source.

**Concerns to keep live.** Whether MAST's three categories are the right cut or merely a legible one (FM-2.6 reasoning-action mismatch sitting under inter-agent misalignment is a visible strain). Whether an LLM judge with recall 0.77 should be the substrate for a field-wide standard vocabulary. Whether the "primacy of system design" thesis will survive stronger models, given that the paper's own model-swap contrasts move failures at least as much as its interventions do. And whether a taxonomy built to be actionable by design — the authors say they deliberately focused on failures where system design has room to help, setting aside hallucination and instruction-following — thereby guarantees the conclusion that system design is where the leverage is.

## Five citations worth chasing next

1. **Kapoor, Stroebl, Siegel, Nadgir, Narayanan — "AI Agents That Matter" (arXiv:2407.01502).** The load-bearing source for the paper's opening premise that agentic complexity buys little over simple baselines, and the one that takes cost seriously as an axis. Directly on the coordination-cost question this paper leaves inherited.
2. **Xia, Deng, Dunn, Zhang — "Agentless: Demystifying LLM-based Software Engineering Agents" (arXiv:2407.01489).** The cited counter-case that an unagentic, undecomposed pipeline matches or beats multi-agent systems on the same tasks — the natural control arm missing here.
3. **Zhang et al. — the Who&When dataset and MAS debugger (cited as [42]).** The closest neighbour: attributing a failure to a specific agent and error step rather than to a category. Failure *attribution* versus failure *classification* is a distinction worth resolving before adopting either.
4. **Hong et al. — MetaGPT (cited as [52]).** The system whose SOP-encoded assembly-line decomposition produces the best FC1/FC2 profile in the paper's own architecture contrast, at the cost of FC3. Worth reading for what an explicit, fixed decomposition actually specifies.
5. **TapeAgents (cited as [80]).** Named as the multi-agent-relevant memory/state work: a structured, replayable log used to document and refine agent actions and to support dynamic task decomposition — i.e. an attempt at the state-management substrate whose absence shows up as FM-1.4 and FM-2.1. (Agent Workflow Memory, arXiv:2409.07429, is the alternate pick in the same slot.)
