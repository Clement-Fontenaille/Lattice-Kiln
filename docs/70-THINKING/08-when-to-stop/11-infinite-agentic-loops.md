# When Agents Do Not Stop: Uncovering Infinite Agentic Loops in LLM Agents

## Density

**Density: MEDIUM-HIGH** — The paper is a compact software-engineering security paper with little padding, and the conceptual core (the definition of an unbounded agentic feedback path, and the distinction between an exit condition and an *effective bound*) bears directly on the Subject; the bulk of the page count, however, goes to static-analysis engineering that is only indirectly about how agents judge their own stopping.

## Name

Xinyi Hou, Shenao Wang, Yanjie Zhao, Haoyu Wang. "When Agents Do Not Stop: Uncovering Infinite Agentic Loops in LLM Agents." arXiv:2607.01641v1 [cs.SE], submitted 2 July 2026.

**Venue.** Preprint on arXiv, not peer-reviewed. The cs.SE classification, the RQ1/RQ2/RQ3 structure, the manual-review protocol with inter-rater agreement, and the IEEE-style formatting all indicate it is written for a software-engineering or security conference (ICSE/FSE/S&P family).

**Keywords (mine).** Non-termination; agentic feedback path; effective bound; bound coverage; static analysis of agent frameworks; model-controlled termination; cost exhaustion; strongly connected components; framework-induced control flow; termination as a program property rather than a model judgement.

## Approach — what they did

The paper does three things in sequence.

First, it *names and defines* a failure class. An Infinite Agentic Loop (IAL) failure is defined as "a structural execution failure where an agentic feedback path repeatedly triggers costly or state-growing actions without an effective stopping bound." The authors are explicit that an IAL is not merely a loop: it arises when model outputs, tool results, external observations, or delegation decisions can keep a path active while no strong bound covers it. The paper insists throughout that "the key issue is not the presence of a loop, but whether an effective bound covers its feedback path."

Second, it builds a detector, **IAL-Scan**, a static analyzer for downstream (application-level, not framework-level) Python agent projects. The pipeline has three stages:

1. **Agent IR construction.** Source code and framework behavior are normalized into a framework-independent intermediate representation. The IR is a set of typed facts — `ExecutionUnit`, `Controller` (loops, routers, retry logic, termination predicates), `Invocation` (model calls, tool calls, agent runs, workflow runs, subprocesses), `StateUpdate` (changes that persist across iterations), `Bound`, and `ExitRecord` — plus local relations (`owns`, `calls`, `updates`, `guards`, `exits`, `constrains`, `transitions`, `dispatches`, `aliases`). Facts are extracted from ASTs in the form ⟨kind, loc, scope, guard, target, attrs⟩ after lightweight name and attribute resolution, deliberately avoiding whole-program points-to analysis. A separate *framework behavior modeling* step then adds the execution relations that never appear as source-level calls: tool registration followed by later dispatch, LangGraph conditional edges, OpenAI Agents SDK handoffs and `Agent.as_tool(...)` reentry, CrewAI delegation, and configuration limits such as `max_turns`, `max_iterations`, `max_retry`, and `recursion_limit`, which are attached to the runtime scope they actually constrain. Unresolvable targets are preserved as an "unresolved" attribute rather than being turned into a precise edge.

2. **Agentic Loop Dependence Graph (ALDG) construction.** From the IR, a directed attributed graph is built over four retained fact classes — controllers, costly invocations, growing state updates, and execution scopes — mapped to 12 node kinds, connected by 10 edge kinds grouped as execution, exit, framework, and feedback edges. Loop-back, recursion, agent reentry, and exception-retry relations become feedback edges; exits become CONDITIONAL_TRUE / CONDITIONAL_FALSE edges. Each controller node is annotated with loop properties (`body_cost_kinds`, `state_growth`, `exit_kinds`, `guard_source`, `bound_sources`). Critically, these annotations are not yet decisions: an exit whose predicate depends on model output is recorded as a *model-dependent exit*, explicitly not as a deterministic bound.

3. **Detection.** The analyzer takes the subgraph of cycle-relevant edges (excluding exit edges and bound attributes, since those describe stopping rather than repetition), computes strongly connected components, and keeps non-trivial SCCs including self-loops. Each retained SCC is a candidate feedback region. A candidate survives only if it is reachable from an agent entry point and its feedback path reaches agentic actions, costly invocations, or growing state. Known-benign cycle shapes — stream consumers, parsers, pagination loops, lifecycle loops, test scaffolding — are filtered out. For each surviving candidate the analyzer selects the *continuation controller* and classifies it as deterministic, model-controlled, tool-controlled, external-state-controlled, exception-controlled, or mixed. It then runs the bound-coverage check and reports a finding only when three conditions hold together: there is an agentic feedback path, the path reaches costly or state-growing operations, and the repetition is not covered by an effective bound.

Third, it evaluates the detector on a 6,549-repository corpus, with an ablation, a baseline comparison against LLM-based analysis, and repeatability/model-sensitivity runs.

An optional **LLM-assisted pruning** pass sits at the end. For an ambiguous candidate the analyzer builds a bounded slice (feedback witness, controller condition, guard definitions, candidate bounds, relevant call chain, source snippets) and lets an LLM act *only as a negative filter*, suggesting pruning predicates such as `strong_finite_bound`, `non_agentic_loop`, `test_only_code`, or `deterministic_exit`. A predicate is accepted only if the slice supports it and it does not contradict the static properties of the candidate.

## What counts as an *effective* bound

This is the paper's design lever, so it is worth isolating. A `Bound` fact records kind, value, source, strength, and target, but the paper's position is that a bound "is effective only when it constrains the repeated path itself." The check asks whether a bound applies to the controller, to its runtime scope, or to the feedback path that controller drives. The paper's sharpest illustration: "an inner turn cap on a nested agent call does not cover an outer evaluator feedback cycle unless it dominates the outer feedback path."

The resulting status lattice (Listing 3) is:

- **Covered** — `verified_bound`, `framework_default_bound`, `config_dependent_bound`.
- **UncoveredOrWeak** — `missing_bound`, `weak_bound`, `disabled_bound`, `ineffective_bound`, `bypassed_bound`.

Two things follow from this framing, both directly on the Subject. First, a *visible exit is not a bound*: in the motivating example the loop does exit when the model stops emitting tool calls, and the analyzer still flags it, because "the exit is controlled by model output and is not a deterministic bound." Second, the property being checked is *coverage*, not *existence*: developers who set `max_iterations` somewhere in the program have not thereby bounded the cycle that matters. The paper states the detection requirement as "reasoning about bound coverage rather than merely checking whether a limit or exit condition exists."

## Models targeted and datasets used

**Frameworks targeted (the real object of study).** Eight: LangChain, LangGraph, CrewAI, AutoGen, LlamaIndex, OpenAI Agents SDK, Google ADK, Semantic Kernel. The subjects are *downstream applications* built on these, not the frameworks themselves.

**Corpus.** 6,549 Python LLM-agent repositories with at least one GitHub star, identified by dependency declarations, imports, API uses, and orchestration patterns, then filtered so each retained repository is an application or product rather than a framework implementation, tutorial, or isolated example, and contains concrete agent logic (agent/workflow construction, runtime invocation, tool registration, orchestration). Totals: 246,748 Python files, 33.41M lines of Python. An evaluation subset of 264 projects — those producing the full static candidate set — is used for RQ2 and RQ3.

**LLMs used.** Only as instruments, never as the subject. `gpt-5.5` is the default pruning model; sensitivity is measured against `gpt-5.4-mini`, `deepseek-v4-pro`, and `gemini-2.5-flash`. Baselines use `gpt-5.5` as well, one via Codex as a coding agent and one via direct API calls file-by-file.

**Hardware.** One Ubuntu 24.04.3 server, two AMD EPYC 9554 CPUs, 256 logical cores, six A100 80GB GPUs.

## Author incentive

All four authors are at Huazhong University of Science and Technology, Wuhan; Haoyu Wang is corresponding author. No funding statement, industrial sponsor, or product is disclosed in the retrieved text. The group has a visible line of work in LLM-application security — the introduction's first citation is their own S&P 2025 paper on the (in)security of LLM app stores — so the incentive is the ordinary academic one: establish priority over a named failure class and its first dedicated detector. The tool is positioned as a research artifact (prompts are said to be released in artifacts), not as a commercial offering. The acknowledgement discloses that ChatGPT and Codex assisted with language polishing and code refinement, with ideas and experiments claimed as the authors' own. One incentive worth naming plainly: the value of the contribution rises with how common and how consequential IALs turn out to be, and the authors both define the category and adjudicate its instances.

## Measurement methodology (brushed)

**Dependent variables.** The primary one is the count of confirmed IAL failures, together with the precision of the alert stream (confirmed / reported). Secondary ones are true-positive coverage (`#TP Cov.`), false-positive count, average token usage per project, and average wall-clock analysis time per project.

**The ground truth is human, and it is the authors.** There is no pre-existing labelled dataset — the paper says outright that "there is no existing tool dedicated to detecting IAL failures." Ground truth is produced by the manual review protocol: the first two authors independently inspect each case and label it a confirmed IAL failure, a false positive, or a missed case. The confirmation criterion has three clauses, mirroring the detector's own three conditions: a repeated feedback path involving model, tool, agent, or workflow execution; continuation that depends on runtime outputs; and no strong bound covering the repeated path. Disagreements go to discussion, with a third author consulted when needed.

**Reliability reporting substitutes for significance testing.** There are no confidence intervals, no hypothesis tests, and no p-values anywhere in the paper — appropriate for a detection-tool paper, but worth stating. What stands in for them is inter-rater agreement: 94.6% on the 74 RQ1 findings, and 92.1% on the 239 unique baseline-only locations reviewed for false negatives. Repeatability is reported as run-to-run variation rather than as a statistic.

**N.** 6,549 repositories scanned end-to-end; 264 projects (the ones yielding the 340 static candidates) form the subset used for ablation, baselines, and stability; 74 alerts and 68 confirmations at the top of the funnel; 239 baseline-only locations reviewed for misses.

**What is controlled.** The ablation disables one component at a time (framework modeling, agentic gate, bound coverage, benign-loop filtering, LLM pruning) while holding everything else fixed. The baseline comparison fixes the base model (`gpt-5.5`) and the per-project timeout (180s) across all three methods. The LLM-sensitivity experiment fixes the input to the same 340 static candidates, so that it measures filtering behaviour only, not candidate discovery — a clean separation the authors call out explicitly.

**Acknowledged handicaps to the baselines.** To control cost the LLM baselines are capped at 80 Python files per project and 3,000 characters per file; on the 264-project subset the pure-LLM baseline reads 12,958 of 34,634 files, 9,233 of them in full. The authors state this bound openly and argue the conclusion survives it, but the comparison is not like-for-like on input access.

**Recall is estimated, not measured.** False negatives are found only by reviewing alerts the *baselines* produced that IAL-Scan did not. Anything neither IAL-Scan nor either baseline flagged is invisible to the study. The 7 confirmed false negatives are therefore a lower bound on misses, not a recall figure, and the paper does not report recall as such.

## Key findings

**RQ1 — real-world prevalence.** Across 6,549 repositories, IAL-Scan reports 74 potential findings; manual review confirms 68 IAL failures and 6 false positives, giving 91.9% end-to-end precision. The 68 failures span 47 projects and all eight modelled framework families.

*What repeats* (the taxonomy of failure patterns, Table II): retry feedback without bound, 17 (25.0%); tool-call iteration without bound, 16 (23.5%); multi-agent chat without turn bound, 14 (20.6%); workflow loop without effective bound, 9 (13.2%); message reentry without bound, 7 (10.3%); runner, delegation, or evaluator feedback, 5 (7.4%). The first three account for 47 findings (69.1%), and the authors note these "often arise when parser errors, validator failures, repeated tool requests, or generated agent messages redirect execution to model, tool, or agent actions" — that is, the repeat is usually triggered by something the system read as a *failure signal*.

*Where it repeats* (frameworks): LangGraph 23 findings across 16 projects (33.8%), AutoGen AgentChat 22 across 15 (32.4%), LlamaIndex 6, LangChain AgentExecutor 5, CrewAI 4, OpenAI Agents SDK 4, Google ADK 3, Semantic Kernel 1. The authors' reading: LangGraph and AutoGen contribute 66.2% because "both frameworks encode feedback through APIs rather than visible loop syntax" — the cycle is invisible to anyone (or any tool) looking for a `while`.

*Consequences* (note the categories overlap): API cost exhaustion, 65 findings (95.6%) across 44 projects; model denial of service, 65 (95.6%); context window exhaustion, 19 (27.9%); external tool rate-limit exhaustion, 5 (7.4%).

*Root causes* (also overlapping): missing strong bound, 68 (100%) — by construction, since it is the defining condition; tool-controlled retry, 28 (41.2%); model-controlled termination, 26 (38.2%); missing exit, 23 (33.8%); workflow cycle without verified bound, 21 (30.9%); state growth amplifier, 19 (27.9%); agent tool reentry, 17 (25.0%).

**What a confirmed IAL looks like concretely.** Three worked examples, all of which are recognisable stopping-judgement failures rather than exotic bugs.

- *The motivating example* (`dataelement/bisheng`): a custom LangChain-compatible model wrapper whose outer loop continues while `finish_reason` is `None` or `"tool_calls"`. Each iteration calls the model, and when the model requests a `$web_search` tool call the code appends both the model message and a `ToolMessage` to `messages`, sending an enlarged history into the next call. There *is* an exit — the loop ends when the model stops emitting tool calls — but it is model-controlled, and no local `max_tool_calls`, `max_iterations`, or timeout covers the path. An inner `break` exits only the tool iteration, not the outer loop. The repetition is hidden inside a model wrapper rather than exposed as an agent graph.
- *Retry loop* (`2456868764/LiteRAG`): nested `while not success` loops repeatedly ask the LLM for a plan. Parser failures are swallowed, and rejected plans reset `success` to `False`, sending execution back to the same LLM call. No retry cap, timeout, or token budget covers the path, so malformed or repeatedly rejected outputs drive unbounded model invocation.
- *Tool-call iteration* (`NVIDIA-AI-Blueprints/ai-virtual-assistant`): a `while True` loop binds tools to the LLM and invokes or streams it; the continuation check turns on whether the model returned tool calls or usable text, and if the output is empty or malformed the code appends a corrective prompt to `state["messages"]` and retries. Model output feeds message-state growth, which feeds the next model call.

**RQ2 — ablation.** Full configuration: 340 static candidates, 74 alerts, 68 TP, 6 FP, 4.2K tokens, 31.2s per project. Removing framework modeling raises static candidates 340 to 910 and alerts 74 to 276 while *dropping* TP coverage 68 to 61, so modelling framework semantics buys recall as well as precision. Removing the agentic gate produces the largest candidate blow-up (340 to 1,453) and a ten-fold token increase (4.2K to 40.4K); the authors read it as principally a cost control. Removing bound coverage lowers TP to 60 and raises FP to 10, hurting both directions. Removing benign-loop filtering takes alerts to 103 and tokens to 16.3K. Removing LLM pruning retains all 68 TPs but reports all 340 candidates, i.e. 272 false positives — the static stage is deliberately recall-favouring and depends on the pruning stage to be reviewable.

**RQ2 — baselines.** The pure LLM API baseline covers 23 of 68 confirmed failures with 183 alerts, 18.1K tokens, 34.4s. The Codex coding-agent baseline covers 50 of 68 with 140 alerts, but hits timeout or an error limit in 75 of 264 projects, at 141.9K tokens and 116.0s per project. IAL-Scan covers all 68 with 74 alerts at 4.2K tokens and 31.2s. The authors' reading: general LLM analysis is not a substitute for structural bound-coverage reasoning — though note that IAL-Scan's 68/68 is partly definitional, since the confirmed set was drawn from its own alerts plus baseline-only review.

**RQ2 — error analysis.** All 6 false positives contain a genuine agentic feedback path; each turns out to have an effective bound that is hard to resolve statically because it is indirect or framework-dependent — `max_steps` or fallback counters outside the loop body, a default `max_iterations=3` in an OpenAI Agents supervisor, a `max_tool_calls=2` cap on a LangGraph tool loop, a retry budget combined with `asyncio` timeouts, a bounded two-turn AutoGen exchange. The authors conclude these come "from subtle bound configurations rather than spurious loop matches," and say the tool conservatively keeps such cases rather than risk misses. The 7 confirmed false negatives are mainly LangGraph workflow or tool cycles with unrecognised bounds, handwritten tool-call loops, framework-adjacent orchestration loops, and multi-agent conversations missing turn or termination bounds.

**RQ3 — stability.** The static stage is fully deterministic: all three end-to-end runs yield exactly the same 340 candidates. The LLM pruning stage is not: the three runs report 74, 73, and 70 alerts covering 68, 64, and 60 true positives. Token cost stays at 4.2K; time ranges 31.2 to 39.3s. Model sensitivity, holding the 340 candidates fixed: `gpt-5.5` gives 74 alerts / 68 TP; `gpt-5.4-mini` gives 136 alerts but only 41 TP; `deepseek-v4-pro` gives 78 alerts / 54 TP at higher cost; `gemini-2.5-flash` gives 131 alerts / 47 TP. The authors' explicit reading is that "retaining more candidates does not necessarily improve coverage; the model must correctly interpret whether the feedback path is feasible and effectively bounded." This is why the LLM is confined to a negative-filter role and why RQ1 rests on manual review of one run.

**Authors' own implications.** For framework designers: enforce bounds at the runtime scope where feedback is created, not as optional local parameters; propagate budgets across the feedback path; report uncovered cycles at compile or run time; and expose guards for state growth, since context can be exhausted before execution limits bite. For framework users, stated as bluntly as anything in the paper: "Developers should not rely on the model to eventually stop producing tool calls, valid plans, or termination messages." Every agent run should carry turn or step limits, every retry or repair path a cap and a timeout, and every message history or workflow state a size limit.

## Open questions the paper itself raises

The paper's Limitations section names four, and the scope statement names a fifth.

1. **Static over-approximation.** As a static analyzer it approximates possible dependencies rather than predicting one trace, so false positives are structural, not incidental.
2. **Coverage of languages and frameworks.** Python only, eight frameworks; unsupported languages, unsupported frameworks, or incomplete framework models yield false negatives. The 7 confirmed misses already include "framework-adjacent" orchestration the models did not capture.
3. **Custom semantics.** Project-specific schedulers, external-state-based stopping logic, and "semantic checks over natural-language outputs" are poorly handled — an explicit admission that stopping decisions made *in natural language* are outside the method.
4. **LLM pruning instability.** The LLM filter is optional and used only negatively, yet its judgements "may still be incomplete or unstable for ambiguous cases," as RQ3 quantifies.
5. **Excluded from scope entirely** (Threat Model): high-volume network DoS, infrastructure-level resource exhaustion, prompt sponge attacks, malicious framework modification, and — most relevant to the Subject — "purely semantic no-progress behavior that cannot be inferred statically." An agent that loops forever while making a syntactically fresh but substantively useless move each iteration is, by the paper's own boundary, out of reach.

## Appreciation

### Mechanism

The mechanism is the durable part of this paper, and it is largely independent of the tool.

**Separating the *exit* from the *bound*.** The paper's central conceptual move is to treat a loop's exit condition and a loop's bound as different objects with different trust properties. An exit is any predicate that can end the loop; a bound is a predicate that *must* end it within a finite number of iterations regardless of what the model, tools, or environment produce. In the paper's vocabulary the exit in the motivating example is real, reachable, and correct-looking, and it is still not a bound, because `finish_reason` is written by the model. This distinction lets the authors classify continuation controllers by their trust source — deterministic, model-controlled, tool-controlled, external-state-controlled, exception-controlled, mixed — and that classification is the load-bearing idea for the Subject.

**Coverage as a scope-dominance property.** The second mechanism is that a bound has a scope, and the question is whether that scope dominates the feedback path. "An inner turn cap on a nested agent call does not cover an outer evaluator feedback cycle unless it dominates the outer feedback path." This reframes a limit from a value you set to a relation between two program regions, and it explains why systems that appear well-instrumented still run away: the caps sit on the wrong cycle.

**Making framework-induced control flow first-class.** The Agent IR exists because the cycle often has no syntactic loop at all. A tool is registered in one place and dispatched elsewhere; a graph edge executes a node with no call; a handoff transfers control to another agent; `Agent.as_tool(...)` makes an agent reenter itself as a callable. The empirical payoff is direct: the two frameworks that hide feedback behind APIs, LangGraph and AutoGen, account for two thirds of the confirmed findings, and turning framework modeling off costs the detector seven true positives while nearly tripling its candidate set.

**Cost and state growth as the thing being repeated.** A cycle is only interesting when it repeatedly reaches an operation that costs money, occupies a model, grows context, or has an external side effect. That gate — not the cycle itself — is what makes the analysis tractable and the findings meaningful.

**Naming the failure trigger.** The most Subject-relevant empirical observation is that unbounded repetition is usually *initiated by a failure signal*: parser errors, validator rejections, malformed output, empty responses, repeated tool requests. The retry/repair path — precisely the machinery a system uses to recover from a detected problem — is the largest single source of non-termination, at 25% of confirmed findings, and 41.2% of findings involve tool-controlled retry. Error handling is where stopping goes wrong.

### Magnitude

The magnitude claims deserve more caution than the mechanism.

**The headline is precision, not prevalence.** 91.9% precision on 74 alerts is a strong result *for the tool*. But 68 failures across 47 of 6,549 repositories is 0.7% of projects — and the paper never frames it as a prevalence estimate, correctly, because recall is unknown. The number that would say how common IALs are is not in the paper, and given the 7 confirmed misses found by looking only at baseline alerts, the true count is certainly higher than 68 by an unknown factor. Do not read 68/6,549 as a rate.

**"Confirmed" means two of the authors agreed the code has that shape.** Confirmation is a static judgement about program structure by the people who defined the category, not a demonstration that any of these loops has ever actually run away. The paper cites community issue reports and a Reddit thread as evidence that IALs occur in deployment, which is real but anecdotal. No finding is accompanied by a reproduction, a trace, a bill, or a disclosure outcome. The impact figures — 95.6% API cost exhaustion, 95.6% model DoS, 27.9% context exhaustion — are consequences *inferred from structure*, not measured.

**The overlapping-category tables invite over-reading.** Both the impact and root-cause tables sum well past 100% because categories co-occur, so the percentages are per-finding attributes rather than a partition. And "missing strong bound, 100%" is the definition restated, not a discovery.

**The baseline comparison is favourable by construction.** IAL-Scan covers 68/68 partly because the confirmed set was assembled from IAL-Scan's own alerts plus a review of baseline-only alerts; the tool cannot lose on a set it largely defined. The baselines were additionally capped at 80 files and 3,000 characters per file. The comparison still supports the weaker and more interesting claim — that unstructured LLM inspection produces far more alerts at far higher cost with far lower agreement — but "coding agent covers 50 of 68" is not a clean recall measurement.

**RQ3 is the quietly important result.** Static candidate discovery is bit-for-bit deterministic across runs, while the LLM pruning stage swings from 68 to 60 true positives across three runs of the *same* model on the *same* 340 candidates, and from 68 down to 41 across models. On a task that is essentially "decide whether this loop is effectively bounded," a frontier model given a curated evidence slice is materially unreliable. That is a small, well-controlled, on-Subject measurement, and it is arguably worth more to the Subject than the 91.9% headline.

## How it could serve a harness-design effort

Read as design input rather than as a security paper, the contribution is a vocabulary and a checklist for the stopping layer of an agent harness.

**The classification of continuation control is directly reusable.** Every loop in a harness has a controller, and asking which of the six classes it belongs to — deterministic, model-controlled, tool-controlled, external-state-controlled, exception-controlled, mixed — separates the loops that stop on their own from the loops that stop only if something cooperates. The paper's blunt version of the design rule: do not rely on the model to eventually stop producing tool calls, valid plans, or termination messages. A harness can hold the invariant that every cycle has at least one deterministic bound in addition to whatever semantic exit it offers.

**Bound coverage is a checkable property, not a configuration value.** The useful discipline is to attach every budget to a *scope* and verify that the scope dominates the cycle it is meant to stop. The paper's recommendation to framework designers is the harness-level version: enforce bounds at the runtime scope where feedback is created, propagate them across the feedback path, and report uncovered cycles at build or start time. A harness that can enumerate its own cycles and prove each is dominated by a budget has turned a runtime hazard into a startup check.

**Budget the state, not only the turns.** The paper's observation that context can be exhausted before iteration limits bite (27.9% of findings) argues for separate guards on message-history and workflow-state size, distinct from step counts.

**Instrument the recovery paths first.** Since retry, repair, and validation feedback dominate the findings, the highest-value caps are on the paths that fire when something already went wrong — with a timeout as well as a count, since a retry can also block.

**The FP analysis is a warning about legibility.** All six false positives were *correctly bounded* systems whose bounds were invisible to analysis — counters outside the loop body, framework defaults, `asyncio` timeouts composed with retry budgets. A harness whose bounds are legible to a static check is a harness whose safety can be argued rather than assumed.

### Limitations and major concerns

1. **The paper's competence stops exactly where the Subject gets hard.** IAL-Scan detects *structural* non-termination — a cycle with no covering bound. It explicitly excludes "purely semantic no-progress behavior that cannot be inferred statically." An agent that consumes a 50-turn budget making distinct, well-formed, entirely useless moves and then reports success is invisible to this method, and that is the harder and more common version of the stopping problem. The paper's own defence against this class is a hard cap, which is a containment measure rather than a judgement.
2. **A hard bound turns non-termination into silent truncation.** The paper treats bound coverage as the goal and does not ask what happens at the boundary. `MaxTurnsExceeded` on turn 25 of an unfinished task is a different failure — an agent stopped without having succeeded, possibly without reporting that it did not succeed. Calibration, abstention, and honest failure reporting are outside the paper's frame, which measures only that repetition ends.
3. **Preprint, single-group, self-adjudicated.** No peer review; the category, the detector, the ground-truth labels, and the false-negative search are all produced by the same four people. Agreement statistics are reported, which helps, but there is no external validation and no independent replication of any finding.
4. **Recall is unknown and the search for misses is biased.** False negatives were sought only among baseline alerts. Failure modes that neither a static analyzer nor an LLM reading truncated files would notice are absent by construction.
5. **No dynamic confirmation.** Not one finding is shown actually looping. For a paper whose stated impacts are cost exhaustion and denial of service, the absence of a single reproduced runaway is a real gap.
6. **Version and scope fragility.** Python only, eight frameworks, with framework models that must track fast-moving APIs; the seven known misses already include "framework-adjacent" orchestration.
7. **The LLM component is load-bearing yet unstable.** Without pruning the tool emits 340 alerts for 68 true findings, so pruning is not really optional in practice — and RQ3 shows pruning loses up to 8 true positives run-to-run and up to 27 across models. The precision headline is one draw from a distribution the paper itself shows to be wide.

## Five citations worth chasing next

1. **Shinn et al. (2023), "Reflexion: Language Agents with Verbal Reinforcement Learning," NeurIPS 36** [31] — cited only in passing as a feedback-based agent, but it is the canonical design in which an agent's *own verbal self-critique* drives the next iteration. That makes it the archetype of the model-controlled continuation this paper says must never be trusted alone, and the direct point of contact with the Subject.
2. **Yao et al. (2023), "ReAct: Synergizing Reasoning and Acting in Language Models," ICLR 2023** [37, 38] — the paradigm the paper says created the failure class. Worth reading for how (or whether) the original formulation specified termination at all.
3. **Xavier et al. (2026), "AgentProof: Static Verification of Agent Workflow Graphs," CoRR abs/2603.20356** [36] — the nearest neighbour methodologically: static verification of structural properties over extracted agent workflow graphs. The comparison would show which termination-adjacent properties are verifiable versus merely detectable.
4. **Li et al. (2026), "Towards Security-Auditable LLM Agents: A Unified Graph Representation," CoRR abs/2605.06812** [15] — a competing unified graph representation of agent systems. Reading it against the Agent IR / ALDG would test whether the feedback-path abstraction here is the natural one or one of several.
5. **Zhang et al. (2026), "Agent Audit: A Security Analysis System for LLM Agent Applications," CoRR abs/2603.22853** [39] — the other end-to-end static analysis system for Python agent applications, covering dataflow, credentials, configuration, and privilege. Useful for judging what fraction of agent-reliability failure is reachable by static analysis in general.

*Also noted, though outside the top five:* the two community bug reports the paper leans on for real-world evidence — CrewAI issue #330 (`allow_delegation=True` leading to infinite loop) [2] and LangGraph issue #6731 (agent looping until the recursion limit) [14] — are the only field observations of the phenomenon in the whole paper, and would be the shortest route to seeing what an IAL looks like when it actually happens to someone.
