# ADaPT: As-Needed Decomposition and Planning with Language Models

## Density

**Density: HIGH** — nearly every section is load-bearing on the Subject: the paper's entire contribution *is* a decomposition policy (when to split, what triggers the split, how deep to go), and it supplies both the mechanism and a cost/depth ablation directly addressing the axes the Subject names.

**Keywords (mine):** failure-triggered decomposition; recursive planner/executor split; depth budget as hyperparameter; self-generated success heuristic; And/Or sub-task composition; LLM program / controller; executor-capability-relative splitting; compositional text environment.

**Year:** 2024 (arXiv v1 Nov 2023, v2 Apr 2024).

**Venue:** Findings of the Association for Computational Linguistics: NAACL 2024. DOI 10.18653/v1/2024.findings-naacl.264. arXiv:2311.05772 [cs.AI].

**Authors:** Archiki Prasad, Alexander Koller, Mareike Hartmann, Peter Clark, Ashish Sabharwal, Mohit Bansal, Tushar Khot.

## Approach

ADaPT is a *controller* — a fixed, hand-written recursive program (the authors call the
overall pipeline an "LLM program", citing Schlag et al. and Dohan et al.) that wraps two
prompted LLM modules:

- **Executor.** A ReAct-style think/act/observe loop that interacts with the environment
  until the task is done or an iteration cap is hit. Crucially, the executor is prompted with
  in-context demonstrations of *atomic skills* for the environment (ALFWorld: put, take,
  clean/heat/cool, examine; WebShop: search, shortlist, match, buy; TextCraft: craft, fetch,
  inventory), not with whole-task gold trajectories (except two seed trajectories in ALFWorld
  and one in TextCraft). This keeps the executor low-level and lets the planner operate at a
  higher abstraction using the LLM's world knowledge.
- **Planner.** Prompted to emit a *short* plan, typically 3–5 steps, plus a logical operator
  string combining them. The authors deliberately reject long fine-grained upfront plans:
  in an unexplored environment a 10-step plan rests on assumptions (where the mug is) that
  cascade into error. Short plans are viable precisely *because* the recursion can split
  again later.
- **Composition logic.** Sub-tasks are joined with **And** (must all succeed, sequential) or
  **Or** (exploration/conditional — succeed if any does, later branches run only if earlier
  ones have not yet delivered). Appendix B: a deterministic parser handles non-homogeneous
  And/Or expressions by splitting them into homogeneous levels, each handed to ADaPT.

**The control flow (Algorithm 1)** is the paper's core claim, and it is small:

```
ADaPT(T, k):
  if k > d_max: return False              # depth budget is the only hard stop
  completed <- executor_LLM(T)            # TRY FIRST, at full task granularity
  if not completed:                       # split ONLY on observed failure
      P, logic <- planner_LLM(T)
      O <- { ADaPT(T_sub, k+1) for T_sub in P }
      completed <- logic(O)
  return completed
```

Two design commitments are worth naming separately, because they are what distinguish this
from both neighbours it positions against:

1. **Decomposition is failure-triggered, not type-triggered and not upfront.** Nothing is
   split until the executor has actually tried and reported it could not proceed. So the
   realized decomposition tree is a function of *the executor's capability on this instance*,
   not of the task's nominal structure. A sub-task an executor can do in one shot never gets
   a planner call.
2. **The failure signal is self-generated.** There is no environment reward at sub-task level.
   The executor prompt simply instructs the LLM to emit "task completed" or "task failed".
   The whole recursion is therefore driven by LLM self-assessment — the authors align this
   with the binary classifier in Reflexion and frame it as simulating intermediate rewards.

The **controller also carries inter-module state**, per environment: ALFWorld propagates the
last *successful* action forward (never failure text, unlike Reflexion; Or-siblings each get
the same context); WebShop propagates the currently visible page and the list of past failed
sub-tasks to the planner (rationales stripped), and a matched product ID forward to executors;
TextCraft propagates the current inventory. This is presented as a small point but it is the
recombination channel — sub-tasks are not independent, they are threaded.

## Models targeted

Everything is few-shot prompted; nothing is trained or fine-tuned.

- **GPT-3.5 is the default** for both planner and executor. Concretely (Appendix A):
  `text-davinci-003` for ALFWorld, `gpt-3.5-turbo` (chat) for WebShop,
  `gpt-3.5-turbo-instruct` for TextCraft. They justify preferring completion models over chat
  variants by citing prior reports that chat variants underperform on these agent tasks.
- **GPT-4** (Sec. 6.2, Fig. 6).
- **LLaMA-2-70B** (base checkpoint, HF) and **Lemur-70B-chat** (Sec. 6.2), plus
  LLaMA-2-70B-chat as executor in the mixed-model experiment (Sec. 6.4).

Executor environment-interaction budgets: 20 / 15 / 20 iterations for
ALFWorld / WebShop / TextCraft. The ReAct-only baseline is given `d_max`× that (60 / 45 / 60)
so the compute budget is nominally matched. `d_max` = 3 for ALFWorld and WebShop, 4 for
TextCraft (to accommodate depth-4 recipes).

## Benchmarks / datasets

- **ALFWorld** (Shridhar et al. 2021) — text version of embodied ALFRED in TextWorld;
  6 task types (pick, clean, heat, cool, look, pick2). Reported on the standard **134 unseen
  evaluation games**; dev = 10 games per task type from the seen split.
- **WebShop** (Yao et al. 2022) — 1.18M real products, purchase-matching-a-spec task.
  **100 test instructions** (following Reflexion's subset), 40-query dev set.
- **TextCraft** — *introduced by this paper*. A text-only Minecraft-crafting game built from
  v1.16.5 crafting-table recipes (shaped and shapeless), with three actions:
  `craft <item> using <ingredients>`, `get <item>`, `inventory`. Reward 1 when the target
  lands in inventory. Each task ships the gold recipe-tree commands **plus up to 10 distractor
  recipes** to keep context bounded. Test set = **200 tasks**: 77 of depth 2, 123 of depth 3,
  11 of depth 4; remaining depth-2 items form the dev set. The point of building it is that
  it has a *known, gradeable ground-truth decomposition depth* (the recipe tree), which no
  existing agent benchmark offered — this is what makes Sec. 6.3 possible at all.

## Author incentive

UNC Chapel Hill (Prasad, Bansal), Saarland University (Koller, Hartmann), and the Allen
Institute for AI (Clark, Sabharwal, Khot). Part of the work was an AI2 internship; partial
support from NSF-CAREER 1846185, NSF-AI Engage DRL-2112635, and DARPA Machine Commonsense
N66001-19-2-4031. No commercial product stake is declared; the artifact is an open method
plus a released benchmark under an AI2 project page. The intellectual stake worth flagging
is continuity rather than commerce: Khot is first author of Decomposed Prompting, and the
paper explicitly frames ADaPT as extending that line ("ADaPT extends the recursive and
hierarchical decomposition in Khot et al. (2023)"). The paper is thus a self-succeeding
step within a decomposition research programme, and its framing of the field — a two-way
split into "iterative executors" vs "plan-and-execute", with as-needed decomposition as the
resolution — is a framing that favours its own contribution. It is a fair framing, but it is
theirs.

## Measurement methodology

**Dependent variable.** Task **success rate** (binary, from the environment) — not WebShop's
soft score. Appendix D argues this explicitly and against prior practice: a naive
"search-the-query-and-buy-the-first-product" executor scores 58.3 while succeeding only 24%
of the time, and ADaPT's executors deliberately decline to buy when sub-goals fail, which
depresses score without touching success. So they optimize success and report score only in
the appendix. Worth noting the direction of this choice — on the score metric ADaPT (60.0)
sits *below* Reflexion (64.2) and LATS (75.9); on success rate it is above both (44.0 vs 35.0
vs 38.0). The metric argument is reasoned, but it is also the metric on which they win.

**What is controlled.** The strongest control in the paper: *all methods share the same
executor module and prompts*. ReAct, Plan-and-Execute, Try-Again and ADaPT differ only in the
controller above the executor. Baselines are also given comparable compute budgets (the ReAct
cap scaled by `d_max`), and Sec. 6.5 checks realized cost directly rather than assuming it —
Fig. 7 shows ADaPT's average LLM-call count is comparable to Try-Again and Reflexion. (The
authors note ReAct and Plan-and-Execute actually *use fewer* calls than allotted, because they
cannot exploit the budget once they fail — so the comparison is favourable-to-baselines in
allotment, unfavourable in realized usage. They read this as evidence gains are not bought
with calls; it is also true that ADaPT spends more than the two weakest baselines actually do.)

**Baselines.** Four families: (i) iterative executor only = ReAct, which is exactly ADaPT at
`d_max`=1; (ii) Plan-and-Execute, one fixed upfront plan, given *deliberately more detailed*
prompts so each step is executable without further splitting; (iii) Try-Again with ReAct,
`d_max` independent retries at temperature 0.7, best trial taken; (iv) Reflexion, full-trajectory
retry with verbal feedback in memory. LATS is quoted from Zhou et al. rather than re-run.

**N and significance.** N is the test-set size (134 / 100 / 200 tasks). **Significance is not
treated at all**: "Due to cost constraints, we report success rates for a single run of each
LLM." No seeds, no variance, no confidence intervals, no significance tests anywhere in the
paper. Several headline gaps are large enough (28.3, 27, 33 points) that this matters less;
several analysis-level gaps are not.

**Validation of the internal signal.** Appendix F compares the LLM's self-generated success
heuristic against gold environment reward. On ALFWorld and TextCraft the LLM *slightly*
over-estimates (the underlying state is objective — an item is in inventory or it is not).
On WebShop the self-assessment is **inflated by >30 points**, because match-to-spec is a matter
of degree. The authors state plainly that this imperfect feedback hurts ADaPT: the recursion
terminates believing it succeeded when further decomposition was needed.

## Key findings

**1. Headline success rates (GPT-3.5, test splits).**

ALFWorld (134 games, `d_max`=3), overall success %:

| Method | Pick | Clean | Heat | Cool | Look | Pick2 | **All** |
|---|---|---|---|---|---|---|---|
| ReAct | 33.3 | 67.7 | 43.5 | 33.3 | 55.6 | 11.8 | 43.3 |
| Plan-and-Execute | 29.2 | 61.3 | 47.8 | 38.1 | 61.1 | 11.8 | 43.3 |
| Try Again with ReAct | 50.0 | 51.6 | 60.8 | 47.6 | 61.1 | 5.9 | 47.8 |
| Reflexion | 70.8 | 61.3 | 61.0 | 66.7 | 61.1 | 5.9 | 57.5 |
| **ADaPT** | 87.5 | 80.6 | 60.8 | 76.2 | 61.1 | 52.9 | **71.6** |

WebShop (100 instructions) and TextCraft (200 tasks):

| Method | WebShop | TextCraft |
|---|---|---|
| ReAct | 32.0 | 19.0 |
| Plan-and-Execute | 17.0 | 27.0 |
| Try Again with ReAct | 30.0 | 15.0 |
| Reflexion | 35.0 | 32.0 |
| LATS (quoted) | 38.0 | — |
| **ADaPT** | **44.0** | **52.0** |

So: +28.3 over ReAct on ALFWorld, +27 over the best of ReAct/P&E/Try-Again on WebShop, +33
over ReAct on TextCraft; and +14.1 / +9 / +20 over Reflexion. Two structural details inside
these numbers are more informative than the headline. First, **Plan-and-Execute ties or loses
to plain ReAct** on ALFWorld (43.3 vs 43.3) and collapses on WebShop (17.0 vs 32.0) — an
upfront fixed plan is not merely weaker than adaptive splitting, it can be *worse than not
splitting at all*. Second, the `pick2` column: every baseline sits under 12% (Reflexion and
Try-Again at 5.9), ADaPT hits 52.9 — a >4× gain concentrated exactly on the task type that
requires composing two sub-tasks over a long action history.

**2. Depth is the active ingredient (Sec. 6.1).** Sweeping `d_max` ∈ {1,2,3} on dev splits,
success rises monotonically on all three datasets. `d_max`=1 *is* ReAct. The 1→2 jump is the
value of having a planner at all; the 2→3 jump is the paper's specific claim — that some
sub-tasks produced by a first split are themselves too hard, so recursion beyond one level
still pays. This is the ablation that separates ADaPT from a one-shot planner.

**3. The split adapts to executor capability (Sec. 6.2).** Holding the LLM fixed and varying
only the executor prompt on ALFWorld — task-specific gold trajectories (strong) / hybrid /
atomic skills only (weak) — ADaPT improves all three. The weak executor goes from **3.3% to
41.7%**, the largest relative move in the paper. Across models (Fig. 6) ADaPT helps GPT-3.5,
GPT-4, LLaMA-2-70B and Lemur-70B; even GPT-4, the strongest, gains up to 37 points on
TextCraft, while LLaMA gains up to 15. Appendix C repeats the main ALFWorld table on top of
the *stronger* task-specific ReAct executor and ADaPT still leads (79.8 vs 67.2 Reflexion,
+23.1 over that executor alone) — though there Plan-and-Execute becomes competitive (63.4),
which the authors themselves read as a stronger executor being able to swallow coarse steps.

**4. The realized depth tracks task complexity (Sec. 6.3).** On TextCraft, with the same
budget `d_max`=4, the mean maximum depth actually used to succeed (`k_max`) rises from **1.9
for recipe-depth-2 tasks to 2.8 for recipe-depth-3 tasks**, while success goes 26.9→78.2 and
1.8→38.7 versus ReAct. Note the ReAct number at depth 3: **1.8%**, essentially total failure.
Appendix D gives a second complexity knob on WebShop — widening the search page from 3 to 10
products drops ReAct (27.5→20.0) and ADaPT gains *more* in the harder setting (+20.0 vs +22.5).

**5. Planner and executor can be different models (Sec. 6.4).** On ALFWorld dev, GPT-3.5
executor alone 38.4 → 58.3 with a GPT-3.5 planner; LLaMA-2-70B executor alone 20.4 → **43.3
with a GPT-3.5 planner** (+22.9). Since the planner is invoked *sparingly* — only on failure —
the expensive model is used rarely, so a cheap/open executor plus an expensive planner is
presented as a cost lever.

**6. The gains are not bought with calls (Sec. 6.5).** ADaPT's average LLM-call count is
comparable to Try-Again and Reflexion.

**The authors' own reading.** They read all of this as establishing one thesis: decomposition
should be *as-needed*, i.e. conditioned on observed execution failure rather than decided in
advance, because task difficulty is not knowable upfront ("it is challenging to anticipate the
difficulty of such a sub-task in advance, as the executor could find a mug in the first attempt
or in an obscure location"). Their explanation for beating Reflexion is resource *targeting*
rather than resource *amount*: Reflexion reflects on and re-runs the whole trajectory even when
one sub-task failed, redundantly re-executing what already worked, whereas ADaPT "redirects more
resources... to the challenging sub-tasks." They read Fig. 5/6 as showing the method is
capability-relative (it repairs whatever the executor cannot do, whoever the executor is), and
Table 3 as showing it is complexity-relative (depth used scales with true recipe depth). They
position related work — Reflexion, Self-Refine, tree search (LATS, ToT) — as *complementary*
rather than rival: those could be dropped inside the planner or executor module.

## Open questions the paper itself raises

The formal Limitations section is short and singular, and it names the load-bearing weakness
correctly:

- **The whole method rests on LLM self-evaluation.** The recursion is driven by the executor's
  own "task completed / task failed". They argue that for decision-making tasks with objective
  environment feedback this heuristic is reliable (Appendix F), but they cite the work arguing
  LLMs cannot reliably self-correct or self-evaluate (Huang et al. 2023a; Stechly et al. 2023)
  and concede the limit. Proposed remedies: external verifiers (Lightman et al.), theory-of-mind
  strategies across multiple LMs (Saha et al.), calibration/self-evaluation techniques
  (Kadavath et al.).
- **Extension beyond decision-making is gated on that same signal.** They state that applying
  ADaPT to non-decision-making tasks such as QA would need better self-evaluation first —
  i.e. the method's portability is limited by where a cheap, honest success signal exists.
- **WebShop specifically is degraded by the bad signal** (Appendix F): the >30-point inflation
  causes premature termination; fixing it is left to future work.
- **Mixing weak and strong LMs is left open** (Sec. 6.4): they gesture at work combining
  stronger/weaker LMs in mathematical reasoning and defer the question.
- Implicit, acknowledged in passing rather than as limitations: single-run results due to cost;
  `d_max` is a hand-set budget rather than something learned or inferred.

## Appreciation

Keeping mechanism apart from magnitude.

**What transfers as mechanism (argument-level, independent of these numbers):**

1. **Failure as the decomposition trigger.** The strongest idea in the paper, and it is
   cleanly isolated: decompose *only after* an execution attempt fails, at whatever granularity
   the attempt failed. This makes the decomposition tree a property of the *executor–task pair*
   rather than of the task alone. It is a genuinely different answer to "what decides whether
   to split" than either "the task type" or "an upfront plan", and the Sec. 6.2 experiment
   (same task, three executor strengths, three different amounts of splitting, all improved) is
   the right experiment to support it.
2. **Short plans are affordable *because* recursion exists.** The argument that upfront
   fine-grained plans are epistemically unsound in unexplored environments — they encode
   assumptions the planner cannot yet have — and that 3–5 abstract steps plus the option to
   split again dominates, is an argument, not a measurement. It transfers.
3. **Attempt-first is a cost policy, not just an accuracy policy.** Since no planner call is
   spent on anything the executor can already do, splitting cost is incurred only where it
   buys something. This directly addresses the Subject's "splitting carries a cost — is it
   offset?" question, and the answer offered is structural: make the cost conditional.
4. **Plan-and-execute can be worse than no decomposition.** ALFWorld 43.3 = 43.3 and WebShop
   17.0 < 32.0 support a real qualitative claim: a fixed plan does not merely fail to help,
   it can convert a recoverable trajectory into an unrecoverable one by committing to a step
   the executor cannot perform. This is a mechanism claim about brittleness, and it is the
   most reusable negative result in the paper.
5. **Depth used should be an outcome, not an input.** Table 3's `k_max` (1.9 → 2.8 tracking
   recipe depth 2 → 3) makes the case that a system should have a depth *budget* and a
   *realized* depth, and that the gap between them is diagnostic. Also mechanism.
6. **The recombination step is real work.** And/Or logic plus the controller's propagated
   state (last successful action, current page, inventory) is where sub-task results become
   a task result. The paper treats this as plumbing; it is arguably a finding that pure
   independent-subtask decomposition would not have sufficed.

**What is magnitude — valid only inside this setup:**

- Every absolute number (71.6, 44.0, 52.0) and every delta (28.3 / 27 / 33 / 14.1 / 9 / 20).
  These are GPT-3.5-era, single-run, on three text environments with hand-written
  atomic-skill prompts. **Single run, no variance, no significance testing** — the analysis-level
  gaps (e.g. Try-Again 47.8 vs ReAct 43.3; the `d_max` 2→3 dev-split increments) are not
  established as more than noise by anything reported.
- `d_max` = 3 and 4, and "3–5 steps": tuned artifacts, not transferable constants. TextCraft's
  `d_max`=4 was chosen *because* recipes go 4 deep — the budget was set from known ground truth,
  which is exactly the knowledge a real deployment does not have.
- The Reflexion comparison is a comparison of two *particular implementations* at a matched
  call budget on these tasks, not a general ordering of failure-repair strategies.
- WebShop is the weakest leg: 100 instructions, self-evaluation inflated >30 points, ADaPT
  behind both Reflexion and LATS on the score metric, and the primary metric chosen — with
  a reasoned argument — to be the one it wins on. The LATS number is quoted, not reproduced.
- TextCraft is the authors' own benchmark, introduced in the same paper that wins on it, and
  built to be compositional by construction (a recipe tree *is* a decomposition tree). It is a
  fair and useful instrument — its ground-truth depth is what makes Sec. 6.3 possible — but
  a +33 on a benchmark designed by the proponents of decomposition to exhibit decomposition is
  a demonstration of the mechanism, not an independent test of it.
- `pick2`'s 4× gain is the most striking cell in the tables and rests on 17 instances.

**On the honesty of the paper:** high. Appendix F reports the failure of its own core signal
rather than hiding it. Appendix D argues its metric choice openly against its own score result.
Appendix C tests the method against a *stronger* baseline executor and reports where the
baseline closes. Sec. 6.5 pre-empts the "you just spent more calls" objection with a
measurement instead of an assertion. The single-run caveat is stated rather than buried.

## How it could serve a harness-design effort / limitations / concerns

Stemming the discussion rather than resolving it.

**What a harness could take.** The controller here is ~10 lines and deterministic; the
intelligence lives entirely in two prompted modules and one boolean. That is a cheap thing to
build and a cheap thing to instrument. The design point worth stealing is the *ordering*: try,
then split — never split speculatively. A harness that follows it gets a natural cost profile
(zero decomposition overhead on tasks the model handles directly) and a natural difficulty
signal (the depth actually consumed). `k_max` versus `d_max` is a ready-made runtime telemetry
pair: it says both how hard the task turned out to be and how close the run came to the
ceiling. The planner/executor model split (Sec. 6.4) suggests routing by role — an expensive
planner invoked rarely on failure, a cheap executor doing the volume — which is a shape a
harness can implement independently of anything else in the paper.

**Where it should worry a harness designer.**

- *The trigger is a self-report.* The entire recursion is gated on the executor saying "task
  failed", and Appendix F shows that signal degrading badly (>30 points) exactly where success
  is graded rather than binary. In an environment without a crisp objective state — most
  interesting ones — this method's control flow is being steered by an unreliable narrator, and
  the failure mode is *silent*: it terminates believing it succeeded. Whether a harness can
  substitute a verifier, a test, or an environment check for this boolean seems to me the
  single question that decides if the mechanism is deployable outside these three sandboxes.
  The paper says as much and does not answer it.
- *Failure detection ≠ failure attribution.* ADaPT re-plans the sub-task that reported failure.
  It has no way to conclude the failure was caused by an earlier sibling's bad output, or that
  the plan itself was wrong rather than the step being too hard. Its only repair move is
  "split this again", so a mis-specified plan gets deeper, not corrected.
- *Termination is a fixed integer.* `d_max` is the only guaranteed stop, and it was set here
  from known dataset structure. A harness needs a stopping rule under genuine uncertainty —
  budget-based, confidence-based, or diminishing-returns — and the paper offers none.
  Relatedly, cost here is bounded but not *governed*: recursion under Or-branching can fan out,
  and only average call counts are reported, never a worst case or a variance.
- *The atomic-skill layer is hand-built and does a lot of work.* Each environment gets a
  hand-authored list of atomic skills demonstrated in the executor prompt, plus hand-written
  planner demonstrations, plus a hand-chosen propagated-state channel per environment. The
  claim "the LLM decomposes autonomously without predefined plan libraries" is true at the plan
  level and less true one layer down, where a human decided what counts as atomic. A harness
  inherits that authoring burden per domain, and the boundary between "atomic skill" and
  "sub-task to split" is precisely the thing that determines how deep the recursion goes.
- *Scope.* Everything here is interactive, environment-grounded decision-making with a reward
  at the end. The authors are explicit that transferring to open-ended or generative tasks
  needs a success signal that does not currently exist. Nothing about how splitting/recombining
  bears on tasks whose output is *text to be judged* rather than a *state to be reached* is
  tested.
- *Vintage.* GPT-3.5 executors fail often, which is what gives the mechanism room to help.
  The paper's own GPT-4 result (still +37 on TextCraft) argues the effect survives a stronger
  executor, but the size of the gap between "what the model can do in one attempt" and "what
  the task requires" is the quantity this whole method converts into value, and that gap is a
  moving target.

**The open thread I would carry forward:** the paper's central claim — that decomposition
should be triggered by observed failure — is separable from its central weakness — that the
observation is the model's own opinion. Everything upstream of the boolean is portable; the
boolean is not. What replaces it in a setting with no environment reward is left open.

## Five citations worth chasing next

1. **Khot et al. (2023), "Decomposed Prompting: A Modular Approach for Solving Complex Tasks"** —
   the direct predecessor ADaPT says it extends; the non-adaptive recursive/hierarchical
   decomposition baseline against which "as-needed" is defined.
2. **Shinn et al. (2023), "Reflexion: Language Agents with Verbal Reinforcement Learning"** —
   the adaptive-but-undecomposed comparison point, and the source of the binary success-classifier
   idea ADaPT reuses; the whole-trajectory vs. failed-sub-task contrast is the paper's main argument.
3. **Dziri et al. (2023), "Faith and Fate: Limits of Transformers on Compositionality"** — the
   cited justification for *why* decomposition is needed at all (compositional limits of the
   underlying model), i.e. the premise the method is built on.
4. **Huang et al. (2023a), "Large Language Models Cannot Self-Correct Reasoning Yet"** (with
   Stechly et al. 2023 alongside) — the work the authors themselves name as the threat to their
   control signal; essential for judging how far the mechanism travels.
5. **Zhou et al. (2023), "Language Agent Tree Search Unifies Reasoning, Acting and Planning"** —
   the search-based alternative to recursive decomposition, quoted but not re-run here, and the
   method that beats ADaPT on WebShop's soft score while losing on success rate.
