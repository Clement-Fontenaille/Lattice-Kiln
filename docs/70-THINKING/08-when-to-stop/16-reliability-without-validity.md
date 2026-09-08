# Reliability without Validity: A Systematic, Large-Scale Evaluation of LLM-as-a-Judge Models Across Agreement, Consistency, and Bias

## Density

**Density: HIGH.** Almost every section carries a number that is doing work, and the

paper repeats itself only in the disciplined way a measurement report has to (abstract,
results, discussion, conclusion state the same four findings); the bearing on the Subject
is indirect but structural, because the paper is about how you would ever know that a
model-as-judge verdict — including a verdict on an agent's own work — means anything.

## Name, keywords, year, venue

**Name.** Justin D. Norman, Michael U. Rivera, D. Alex Hughes. "Reliability without
Validity: A Systematic, Large-Scale Evaluation of LLM-as-a-Judge Models Across Agreement,
Consistency, and Bias." arXiv:2606.19544v1 [cs.CL], submitted 17 June 2026. Licence CC BY 4.0.

**Venue.** Preprint on arXiv; not peer-reviewed. The manuscript is written to a conference
template — it carries a Limitations section and a "Responsibility Checklist Notes" appendix,
and it anonymises the name of its own evaluation framework, which are the marks of an
ACL-style submission under review.

**Keywords (mine).** LLM-as-a-judge; chance-corrected agreement; Cohen's kappa; kappa
deflation; test-retest reliability; position bias; verbosity bias; construct validity;
benchmark discriminability; rank instability; validation protocol; meta-evaluation.

## Approach

The authors argue that the field validates its automatic judges with the wrong statistic.
The standard headline number is exact-match agreement, meaning the share of items on which
the judge's verdict equals the human label. That statistic does not subtract the agreement
you would get by guessing, so it rewards chance as though it were discrimination, and how
much it rewards depends on the label distribution of the benchmark rather than on the judge.

Their response is measurement rather than method: they run the largest single systematic
audit of LLM judges reported to date and report chance-corrected numbers next to the raw
ones. The design is a full crossing of judges by benchmarks by protocols. Twenty-one
judges from nine providers are each run over three benchmarks under three protocols —
agreement (one verdict per item, compared to the human label), consistency (three to five
independent re-runs per item with caching off, in both AB and BA orderings), and a bias
audit (paired AB+BA orderings plus response-length analysis). That produced 118 runs and
roughly 541,000 individual judgments over a five-week window in March and April 2026.

Two pieces of vocabulary are introduced as the paper's conceptual contribution. *Kappa
deflation* is defined as the arithmetic gap between exact match and Cohen's kappa for a
given judge-benchmark pair, and the *consistency-bias paradox* names the case where a judge
repeats itself almost perfectly across runs while being severely position-biased. The
authors are careful that neither is mathematically novel: deflation is a direct consequence
of Cohen's 1960 correction, and they claim only that nobody has measured it at this scale
across current judges. The findings are distilled into a five-step Minimum Viable
Validation Protocol.

## Models targeted

Twenty-one general-purpose models are used as judges, from nine providers, sorted by the
authors into three tiers. Tier 1 is widely deployed production judges: GPT-4o, GPT-4o-mini,
GPT-4.1, Gemini 2.5 Pro, Gemini 2.5 Flash, Claude Haiku 4.5, Llama 3.3 70B, Qwen 3 8B.
Tier 2 is the cost-conscious band: Mixtral 8x22B, GPT-4.1-mini, Claude Sonnet 4. Tier 3 is
the April 2026 frontier plus open-weight systems: GPT-5.4, GPT-5.4-mini, Claude Opus 4.6,
Claude Sonnet 4.6, Gemini 3.1 Pro, GPT-oss 120B, Minimax M2.7, DeepSeek V3.2, Kimi K2.5,
GLM-5. Parameter counts span 8B to over 100B. Open-weight models were served through the
Fireworks endpoint; the rest through provider APIs.

One configuration choice matters more than the tier labels. Every judge that can emit a
built-in reasoning trace had that channel suppressed, using per-provider mechanisms that
Appendix D lists model by model — `thinking_budget=0` or `128` for Gemini,
`reasoning_effort=none` for GPT-5.4 and DeepSeek V3.2, `thinking={type:disabled}` for
Kimi K2.5 and GLM-5, a `/no_think` suffix for Qwen 3 8B, opt-in-only extended thinking left
off for the Anthropic models. The stated reasons are cross-judge comparability and
preventing the verdict token from being truncated when reasoning eats the output budget.
All judges ran at temperature 0. The authors state plainly that they do not claim their
results characterise the thinking-on configuration.

## Benchmarks and datasets

Three existing judge-evaluation benchmarks, ordered by the authors as increasing in
difficulty and differing deliberately in what they label.

- **MT-Bench** (Zheng et al., 2023): 2,391 pairwise comparisons with expert human
  judgments, a balanced A/B/Tie ternary label set, measuring preference alignment. This is
  the most widely used judge benchmark and the one where deflation is largest.
- **JudgeBench** (Tan et al., 2025): 350 items across mathematics, coding, creative
  writing, and analysis, labelled for objective correctness rather than aesthetic preference.
- **RewardBench** (Lambert et al., 2025): 2,981 chosen-versus-rejected pairs, binary labels.

RewardBench required a loader fix that is worth recording. The benchmark's standard
generative loader puts every chosen response in position A, so the human label is
identically "A" on every item, the chance term collapses, and Cohen's kappa degenerates to
exactly 0.000 for every judge regardless of how good it is. The authors instead applied
per-item position randomisation with seed 42, matching the contract of the benchmark's own
`run_generative.py`. This is a small piece of the paper that carries a general lesson: a
degenerate label marginal can make a chance-corrected metric report nothing, which is a
failure of the harness and not of the judge.

No new human annotation was collected; the human labels are inherited from the three source
benchmarks. All three are English and text-only.

## Author incentive

All three authors are at the UC Berkeley School of Information and give Berkeley email
addresses. The paper introduces no judge model, no training data, and no deployable system,
so there is no product being sold by the result. What is being staked is methodological
authority: they name two phenomena (kappa deflation, the consistency-bias paradox), propose
a protocol under a memorable acronym (MVVP), and promise to release both the
541,000-judgment dataset and their evaluation library as a community resource and a "frozen
baseline against which future judges can be evaluated under an identical protocol." That is
a bid to own the meta-evaluation standard, which is a real incentive even though it is
academic rather than commercial. No funding source is disclosed in the text I retrieved.
Appendix G states that AI assistance was used for copy-editing, table and reference
formatting, LaTeX debugging, and BibTeX hygiene only, and not for research claims,
experiment code, design, hypothesis formulation, data collection, or analysis.

The most conflict-shaped pattern in the results — the Anthropic family posting the best
joint kappa-and-bias figures — appears without any affiliation that would explain it.

## Measurement methodology

**Dependent variables.** Fourteen metrics are implemented, of which these carry the paper.
Cohen's kappa, `(p_o - p_e) / (1 - p_e)`, is the primary agreement measure, compared against
the human label set on all three benchmarks; Krippendorff's alpha is used where more than
two raters or multi-run settings are in play (the two coincide in the two-rater nominal
case). Tie-excluded exact match is the raw comparison figure, following Zheng et al.
Kappa deflation is their derived quantity, `EM - kappa`, in percentage points. Test-retest
reliability is the agreement of a judge with itself across independent re-evaluations of
the same items; self-consistency is the share of items where the majority verdict across N
runs agrees with each individual run. Position flip rate is the fraction of items whose
verdict changes when the response order is swapped. Position bias is the aggregate
`|P(A wins) - 0.5|` over paired AB+BA evaluations. Verbosity bias is the Pearson correlation
between the response-length differential and the verdict, following Dubois et al.

**What is controlled.** Temperature is pinned at 0 for every judge and every run. Reasoning
traces are suppressed across the board so that judges are compared under a common
no-reasoning condition. A single pairwise comparison template is used throughout, and each
metric has one fixed operationalisation. Response caching is disabled specifically for the
consistency protocol, so that replicate runs sample genuinely independent generations rather
than a memoised response; caching stays on for agreement and bias-audit, where it does not
threaten the measurement. Position-swap debiasing (AB+BA pairing) is applied in both the
consistency and bias-audit protocols. Everything ran through one bespoke evaluation library,
promised as an open-source release.

**N.** 118 runs and approximately 541,000 judgments, decomposing as 63 agreement runs
(21 judges over each of three benchmarks), 21 bias-audit runs (all on MT-Bench), and 34
consistency runs (17 judges over two benchmarks). The campaign ran in seven phases; Phases 4
and 5 used 5 replicates per item, Phase 7 used 3. Run counts are stated to be verified
against a `.eval_state.json` production ledger. The consistency cohort reported in the
paradox figure is the 16 judges evaluated under both the consistency and bias-audit
protocols, which is why that figure covers 16 and not 21.

**How significance is treated: essentially, it is not.** This is the single most important
thing to know before reading the tables. Appendix H states the position outright — for each
judge-benchmark cell the paper reports one value per metric rather than a mean with a
confidence interval, on the grounds that agreement-protocol values are population statistics
computed over the entire benchmark rather than sample estimates, and bias-audit values are
point estimates over paired AB+BA evaluations. Consistency values summarise 3 to 5 replicates
and are themselves described as point estimates of within-judge stability. Cohort-level rows
are unweighted means across judges. There are no p-values, no error bars, and no
variance-component decomposition anywhere in the paper; the authors name that decomposition
as future work. The evidential weight therefore rests on effect sizes being large and on
patterns holding across all 21 judges, not on statistical inference.

**A priori hypotheses.** Seven hypotheses (H1-H7) were recorded on 2026-04-14, before the
Phase 6 frontier-model data collection began, based on patterns seen in Phases 1-5.
Appendix C is unusually candid about the standing of this: the predictions were recorded
internally, were not deposited with any external registry, and the authors explicitly
decline to claim the status of formal pre-registration. They report every outcome unmodified,
including the one that failed. Three were fully confirmed (H1, H3, H7), one confirmed for
its stated subset (H6, 7 of 16 judges), two partially confirmed (H2, H4), and one refuted
(H5, where RewardBench was predicted to stay degenerate and did not). They offer that mixture
as a calibration signal, arguing that a post-hoc prediction set would have been confirmed at
a higher rate. The argument is reasonable and is rarely made this explicitly.

## Key findings

### 1. Kappa deflation is universal, and its size is set by the benchmark, not the judge

Every one of the 21 judges shows a large gap between exact match and Cohen's kappa on
MT-Bench. The range is 33.8 to 41.3 percentage points, with a cohort mean of 38.6 pp. All
ten frontier-generation judges sit at 30 pp or above, which confirms H1. The best judge on
chance-corrected agreement, Gemini 3.1 Pro, still shows a 33.8 pp gap: exact match 0.849
against kappa 0.511. The authors compress the practical consequence into one sentence that
is the most quotable line in the paper — a judge advertised as "85% agreement" on MT-Bench
has a kappa of about 0.48, which is moderate agreement, not the near-perfect performance the
percentage implies.

The deflation tracks the label distribution exactly as Cohen's correction predicts. MT-Bench,
with a balanced A/B/Tie ternary set and therefore a chance baseline near one third, gives a
mean deflation of 38.6 pp. JudgeBench's pairwise correctness labels give 23.7 pp (range 8.1
to 38.5). RewardBench's binary chosen-versus-rejected labels give 10.2 pp (range 5.9 to 21.3).
The authors' own reading is emphatic on this point: the gap "is not a model-quality artifact;
it is how an uncorrected metric interacts with the label marginals of the benchmark." The
amount by which a judge's headline number overstates it depends on which dataset you validated
on. Their recommendation is that kappa or Krippendorff's alpha should be reported alongside
any exact-match figure and should be the headline reliability number.

Selected rows from their Table 2, MT-Bench first, as EM / kappa / deflation-pp:
Gemini 3.1 Pro 0.849 / 0.511 / 33.8; Claude Opus 4.6 0.848 / 0.489 / 35.9; DeepSeek V3.2
0.845 / 0.486 / 35.9; Claude Sonnet 4.6 0.851 / 0.484 / 36.7; GPT-5.4 0.836 / 0.457 / 38.0;
GPT-4o 0.832 / 0.451 / 38.1; Qwen 3 8B 0.810 / 0.406 / 40.4; GPT-4o-mini 0.809 / 0.396 / 41.3;
GPT-5.4-mini 0.788 / 0.376 / 41.2. On JudgeBench the same cohort spreads far wider: Claude
Opus 4.6 reaches kappa 0.875 and Gemini 3.1 Pro 0.841, while Mixtral 8x22B sits at 0.271 and
Llama 3.3 70B at 0.283.

### 2. Judge rankings do not transfer across benchmarks

Eleven of the 21 judges shift by four or more rank positions between benchmarks. Only Claude
Opus 4.6 and Gemini 3.1 Pro hold a top-three place on all three. The largest single shift is
Llama 3.3 70B, which moves 15 positions, from rank 5 on MT-Bench to rank 20 on JudgeBench.
(The abstract and conclusion both say "up to 14 positions" while the results section reports
the Llama shift as 15; the discrepancy is unexplained and is one of a few small internal
inconsistencies.) Other named cases run in both directions: Minimax M2.7 goes from MT rank 17
to JudgeBench rank 5, DeepSeek V3.2 from 3 to 13, GPT-4o from 8 to 18, GPT-oss 120B from
MT 12 to RewardBench 3, Claude Haiku 4.5 from MT 15 to RewardBench 6.

The authors give two coupled causes. The first is discriminability. MT-Bench compresses all
21 judges into a 13.5 pp kappa band, from 0.376 to 0.511, with an average gap of 0.6 pp
between adjacent ranks, so tiny differences produce large rank swings. JudgeBench spreads
the same judges over 60.4 pp, a factor of 4.5 wider, in tiers of 3 to 9 pp. RewardBench falls
in between at 28.1 pp, with the top seven judges inside a 2.7 pp band. The second cause is
construct: the three benchmarks measure preference alignment, objective correctness, and
chosen-versus-rejected discrimination respectively, and a judge strong on one construct can
collapse on another. Their recommendation is to validate on at least two benchmarks chosen
to span the preference-versus-correctness axis.

The compression has a second consequence they draw out in the family analysis. Generational
improvement inside OpenAI's line is clearly visible on JudgeBench — kappa rises 0.309
(GPT-4o) to 0.487 (GPT-4.1) to 0.606 (GPT-5.4) — and nearly invisible on MT-Bench, where the
same three models score 0.451, 0.451, and 0.457. The same holds within Anthropic's line:
Opus 4.6 leads Sonnet 4.6 by 9.3 pp on JudgeBench and by 0.6 pp on MT-Bench. A saturated
benchmark cannot see the differences you care about.

### 3. The consistency-bias paradox

This is the finding that bears most directly on the Subject. Position bias across the cohort
spans nearly two orders of magnitude, from Gemini 2.5 Pro at 0.002 to Qwen 3 8B at 0.192.
Frontier and reasoning models are systematically lower and small cost-optimised models
systematically higher, but within-family heterogeneity is enormous: Gemini 2.5 Pro (0.002)
and Gemini 2.5 Flash (0.125) differ by a factor of 70. H2 predicted that all three
thinking-architecture judges would fall below 0.05 and only Gemini 3.1 Pro (0.038) did;
GPT-5.4 came in at 0.083 and DeepSeek V3.2 at 0.094. Thinking architecture reduces position
bias relative to cheap models but does not eliminate it.

H7 predicted that at least one judge would combine test-retest above 0.95 with position bias
above 0.10, and two did. Qwen 3 8B records test-retest 0.992 — the highest reproducibility in
the entire cohort — with position bias 0.192 and a JudgeBench kappa of 0.289, the third
lowest. Gemini 2.5 Flash shows the same shape more mildly at 0.988 and 0.125. Both are
production-deployed judges.

The authors' explanation is the important part, and it is a conceptual point rather than an
empirical one. Test-retest measures the stability of the output, not the correctness of the
decision process, and the two are mathematically orthogonal. A judge that deterministically
prefers whatever sits in position A will score a perfect test-retest while exhibiting the
maximum possible position bias. Reproducibility is therefore not evidence of validity, and
can be produced by exactly the mechanism that destroys validity. Because reporting test-retest
alone remains common practice, they argue that current reporting "misleads precisely in the
cases that matter most for deployment: highly reproducible judges."

### 4. Consistency degrades on harder items

Seven of the 16 consistency-cohort judges show a position flip-rate increase of at least 1.5x
moving from MT-Bench to JudgeBench, confirming H6 for that subset. The sharpest degradations
are Llama 3.3 70B (3.3x, 0.077 to 0.253), GPT-4o-mini (3.0x, 0.127 to 0.380), and GLM-5
(2.4x, 0.096 to 0.227). Cohort median flip rate rises from 0.09 to 0.17. Mean test-retest
falls from 0.943 to 0.911. Two frontier judges move the other way — Claude Opus 4.6 and
Gemini 3.1 Pro both improve by a factor of 0.58 — which the authors read as some
current-generation systems handling harder items with greater positional stability than
easier ones. Per-judge variation is wide: Gemini 2.5 Flash drops 7.3 pp in test-retest
(0.988 to 0.915) while Gemini 3.1 Pro is flat (0.977 to 0.978).

The general shape is that a judge's stability is not a fixed property of the judge. It is a
property of the judge on a given difficulty of item, and it decays where the items get hard —
which is where you most need it.

### 5. Verbosity bias is small under this rubric

All 21 judges register verbosity bias below 0.011 on MT-Bench, the largest being GPT-4o-mini
at 0.010, with 17 of 21 below 0.005 and the smallest values clustered near 0.001. The authors
note the contrast with the 20-40% variance contributions reported in 2023-era style-and-length
studies, and suggest verbosity sensitivity has fallen substantially over two model generations.

They then caveat their own finding harder than most papers would. The measurement uses a
single pairwise rubric and one fixed length-differential operationalisation (the Pearson
correlation between length difference and verdict, following Dubois et al.), and they
explicitly do not claim verbosity bias is eliminated under arbitrary rubric or task variation.
The Limitations section repeats this and adds the mechanism that would explain a discrepancy
with prior work: rubric design choices, including reference grounding and reasoning
instructions, are known to interact with bias profiles in ways a single-template design
cannot isolate. So the honest reading of finding 5 is narrow — under one pairwise rubric with
an explicit comparison in front of the judge, length stops predicting the verdict. It says
little about single-response absolute scoring, where a judge has no comparison and length may
serve as a proxy for effort.

### 6. RewardBench is not degenerate once the loader is fixed

H5 predicted kappa at or below 0.05 on RewardBench, because the standard loader places every
correct label in position A. Under per-item position randomisation all evaluated judges
produce kappa in [0.616, 0.898], comfortably in the substantial-to-near-perfect bands, with
Gemini 3.1 Pro at 0.898, GPT-oss 120B 0.880, Claude Opus 4.6 0.879, GPT-5.4 0.879, and Claude
Haiku 4.5 0.873. The hypothesis is recorded as refuted. This is the paper's one clean
self-refutation and it doubles as evidence for its own thesis in a different direction: the
degeneracy was an artefact of how the evaluation was set up, and fixing the harness changed
the conclusion completely.

### 7. The Minimum Viable Validation Protocol

The five requirements they distil, to be satisfied before a judge is trusted:

1. **Chance-correct.** Report Cohen's kappa or Krippendorff's alpha alongside any exact-match
   figure, and treat the chance-corrected number as the headline.
2. **Swap positions.** Measure position bias with paired AB+BA evaluations and report
   `|P(A wins) - 0.5|`.
3. **Replicate.** Measure test-retest over at least 3 independent runs at temperature 0 with
   response caching disabled.
4. **Cross-validate.** Evaluate on at least 2 benchmarks spanning preference-style and
   correctness-style label distributions.
5. **Audit the paradox.** When test-retest exceeds 0.95, verify that position bias is below
   0.10 before claiming reliability. High stability with high bias is a failure mode, not a
   strength.

Step 5 is the one the rest of the paper exists to justify, and it inverts the ordinary reading
of a stability number. The authors flag in Appendix H that partial adoption is itself a risk:
reporting kappa alone, without the paired swap and replication checks, "can produce a false
sense of having addressed judge reliability."

## Open questions the paper itself raises

From the conclusion and the Limitations section, in the authors' own framing.

- **Calibration is entirely absent, and they say why.** Expected Calibration Error and Brier
  score need token-level logprobs, which most providers in their cohort do not expose. They
  defer calibration to future work and name it as the natural extension of the protocol once
  logprob coverage broadens. For the Subject this is the most consequential gap in the paper:
  a judge's confidence, not just its verdict, is what a stopping rule would want to consume.
- **Variance-component decomposition.** They want a formal treatment of runs, items, and
  position orderings as random effects, which would convert their empirical patterns into
  structured reliability coefficients and give a principled basis for choosing sample sizes
  and replicate counts. This is what would replace the current absence of inferential statistics.
- **Rubric sensitivity.** All results come from one pairwise template. They flag that
  reference grounding and reasoning instructions are known to interact with bias profiles,
  and that a single-template design cannot isolate those interactions. The verbosity result
  is the finding most exposed to this.
- **Thinking-on configurations.** Reasoning channels were suppressed for comparability.
  They explicitly do not claim to characterise judges with reasoning enabled, which leaves
  open whether the position-bias and consistency profiles change when the judge is allowed
  to deliberate.
- **Temporal stability.** All runs sit inside a five-week window. Hosted endpoints drift
  across provider-side updates, sometimes silently and without versioning, and they call for
  a dedicated longitudinal study. The numbers should be read as a snapshot.
- **Multilingual and multimodal judging.** Not characterised, and they warn against
  extrapolating.
- **Cost figures.** List prices only, ignoring volume tiers, batch discounts, and negotiated
  enterprise pricing; to be read as approximate upper bounds.

## Appreciation

### Mechanism

The mechanism is the durable part of this paper and it is almost entirely arithmetic, which
is a strength rather than a weakness. Three distinct mechanisms are established.

The first is that an uncorrected agreement rate absorbs the chance baseline of whatever label
distribution it was computed over. Since the chance baseline is a property of the benchmark,
the amount by which exact match flatters a judge is set by the dataset rather than by the
judge, and so raw agreement rates are not comparable across benchmarks at all. This follows
from Cohen (1960) and needs no new theory; the paper's contribution is showing that it bites
hard on every current judge and giving the gap a name.

The second is the orthogonality argument behind the consistency-bias paradox. Test-retest
reliability measures whether an evaluator repeats itself; validity measures whether it is
right. A deterministic bias maximises the first while destroying the second, so the two are
independent quantities and a high value on the first is not evidence about the second. This
is standard psychometrics, correctly imported. Its force here is that the LLM evaluation
literature has been reporting reproducibility as though it were a quality signal.

The third is the discriminability argument: on a compressed benchmark, ranking is dominated
by noise, because the adjacent-rank gap (0.6 pp on MT-Bench) is far smaller than the
between-benchmark disagreement. That makes leaderboard position on a saturated benchmark
close to uninformative, and it explains the rank instability without needing any claim about
the models themselves.

I would add that the RewardBench loader episode is a fourth mechanism, stated only in passing:
a chance-corrected metric can be silently zeroed by a degenerate label marginal in the
harness. That is a failure mode of the measurement apparatus that will recur wherever someone
builds an evaluation pipeline with a fixed answer position.

### Magnitude

The magnitudes are large, consistent, and — this is what gives them weight given the absence
of inferential statistics — universal across the cohort. A 33.8 to 41.3 pp deflation with no
exceptions in 21 judges from nine providers spanning three generations is not a result that
needs a confidence interval to be believed. The 4.5x difference in kappa spread between
JudgeBench (60.4 pp) and MT-Bench (13.5 pp) is similarly hard to argue with, and the 15-position
rank shift for Llama 3.3 70B is a concrete demonstration rather than a summary statistic.

The paradox finding is where magnitude and mechanism should be kept apart most carefully. The
mechanism is airtight and general. The magnitude rests on exactly two judges out of 16 crossing
the thresholds their own hypothesis pre-specified, and those thresholds (0.95 and 0.10) are
chosen rather than derived. Qwen 3 8B at test-retest 0.992 with position bias 0.192 is a
genuinely striking instance. But "two of sixteen" is the honest frequency, and the finding is
better read as a demonstration that the failure mode is real and reachable in production
systems than as an estimate of how often it occurs.

The verbosity magnitude is the weakest number in the paper, not because it is wrong but because
its scope is narrow, and the authors say so themselves in two separate places. A Pearson
correlation below 0.011 under one pairwise rubric with a fixed length-differential
operationalisation does not license the general claim that verbosity bias has receded, and
they decline to make that claim.

## How it could serve a harness-design effort

The Subject concerns agent loops deciding whether their work is done, is failing, or exceeds
them. This paper is not about agents and never mentions them, so everything below is transfer
rather than a claim the authors make.

The transfer that matters is this. An agent loop that consults a model to ask "is this
finished?" or "did this attempt work?" is running an LLM judge inside the control path, with
the loop's continuation as the consumer of the verdict. Every failure mode catalogued here
then applies to the loop's own stopping decision, with two aggravating differences: the
judgement is usually self-judgement, and there is usually no human label to validate against
at runtime.

Concrete consequences for a harness:

- **Any "the model agrees with ground truth X% of the time" figure used to justify a
  self-evaluation gate should be discounted, and by an amount set by the label balance of
  whatever you measured on.** A binary done/not-done gate has a chance baseline near 0.5, so
  a judge reporting 85% agreement on a balanced binary gate is at kappa around 0.70; on a
  skewed gate where 90% of attempts genuinely succeed, 85% agreement can be worse than always
  saying "done." The deflation is largest exactly where the decision is most balanced, which
  is where the gate matters most.
- **A stable self-assessment is not a trustworthy one.** This is the single most transferable
  point. If a harness validates its stopping criterion by re-running it and observing that the
  answer is reproducible, the paper shows that reproducibility can be produced by a
  deterministic bias that is orthogonal to correctness. Their step 5 translates directly: if
  your stopping check is highly stable, that is the case in which you must look for a
  systematic bias, not the case in which you may relax.
- **Order and presentation effects are a live confound for self-assessment.** A judge with
  position bias 0.192 is largely responding to where a thing sits rather than what it is. The
  agent-loop analogue is any assessment where the framing, order, or position of the
  candidate outcome could carry the decision — for example asking "did A or B work better"
  where A is always the newest attempt. The paper's countermeasure, paired swapped
  evaluations, is cheap and directly implementable.
- **Judge quality degrades where items get hard.** Flip rates roughly double from MT-Bench to
  JudgeBench at the cohort median, and by 3x for the weaker judges. An agent loop encounters
  hard items precisely when it is in trouble, which is when a self-assessment gate is most
  load-bearing and, by this evidence, least stable. Validating a gate on easy cases predicts
  little about its behaviour on the cases that trigger escalation.
- **Validate on more than one construct.** Preference-style and correctness-style benchmarks
  rank the same judges differently by up to 15 positions. Choosing a self-evaluation model on
  the basis of one internal eval set is choosing on a single construct.
- **Cheap judges are disproportionately biased.** The cost-optimised tier carries the highest
  position bias (Qwen 3 8B 0.192, Gemini 2.5 Flash 0.125), which matters because a
  per-iteration gate inside a loop is exactly the place where a designer is tempted to use the
  cheapest possible model. The within-family gap between Gemini 2.5 Pro (0.002) and Gemini 2.5
  Flash (0.125) shows the tradeoff is not smooth and cannot be assumed from the family name.

### Limitations and major concerns for that use

- **It is a preprint with no peer review**, and it contains small internal inconsistencies:
  the "14 positions" of the abstract against the 15-position shift in the results, the 33.8-41.2
  pp range in the abstract against 33.8-41.3 pp in the results, and an appendix footnote
  instructing that a RewardBench item count of 2,985 in the body "should be updated" to 2,981.
  These are cosmetic rather than substantive, but they indicate the manuscript had not settled.
- **No inferential statistics at all.** Single point estimates, no confidence intervals, no
  significance tests. The population-statistic justification is defensible for the agreement
  protocol but weaker for the consistency protocol, where 3 to 5 replicates per item are being
  summarised as though they were exact. Per-judge differences of a few pp should not be treated
  as real.
- **The dataset and the library are promised, not released.** Every number here is currently
  unverifiable by a reader.
- **Reasoning was suppressed everywhere.** A harness that uses a reasoning model for its
  self-evaluation gate — which is the natural design — is outside the configuration this paper
  measured, and the authors say so.
- **No calibration, no abstention, no self-evaluation.** The paper measures judges scoring
  other models' outputs against human labels. It does not study a model judging its own work,
  where self-preference bias is a documented and separate phenomenon (they cite Panickssery et
  al. but do not measure it), and it does not study confidence at all. The transfer to the
  Subject is by analogy on the measurement side and should not be overstated.
- **Snapshot in time, hosted endpoints, single rubric.** All three limit generalisation, and
  the temporal one is the most corrosive for a harness: the judge behind your gate can change
  under you without a version bump.

The most useful thing the paper offers a harness effort is not any single number but the MVVP
as a checklist for validating a stopping or self-assessment gate, plus the reframing of
stability from a reassurance into a thing that itself requires auditing.

## Five citations worth chasing next

1. **Guerdan et al. (2025), "Validating LLM-as-a-Judge Under Rating Indeterminacy" (NeurIPS).**
   Cited at three separate points as the source for the claim that raw agreement overstates
   discrimination. Rating indeterminacy — cases where the correct label is genuinely unclear —
   is directly the situation an agent faces when deciding whether partial progress counts as
   done.
2. **Choi et al. (2026), "Diagnosing the Reliability of LLM-as-a-Judge via Item Response
   Theory" (arXiv:2602.00521).** The paper credits it with separating intrinsic consistency
   from human alignment, which is exactly the reliability-versus-validity distinction this
   paper argues for empirically. IRT would also supply the structured reliability coefficients
   the authors name as future work.
3. **Bavaresco et al. (2025), "LLMs Instead of Human Judges? A Large Scale Empirical Study
   Across 20 NLP Evaluation Tasks" (ACL).** Named as the closest prior work in scale, 11 judges
   over 20 tasks, and it reaches a compatible recommendation about validating against
   task-specific annotation before deployment. The natural comparison point for this paper's
   claim to be the largest such study.
4. **Haldar and Hockenmaier (2025), "Rating Roulette: Self-Inconsistency in LLM-as-a-Judge
   Frameworks" (Findings of EMNLP).** Cited for the temperature-sensitivity result that
   same-verdict rates fall from above 95% at temperature 0 to as low as 70% at temperature 1.
   That is the run-to-run instability an agent loop actually lives with, since production loops
   rarely run at temperature 0.
5. **Panickssery et al. (2024)** on self-preference — cited in the introduction among the
   reliability problems but never measured here, and it is the missing piece for the Subject,
   since an agent judging whether its own work is done is the self-preference case rather than
   the third-party judging case this paper studies.

*(Runners-up: Collot et al. (2025) on balanced accuracy via Youden's J as an alternative
chance correction; Stureborg et al. (2024) on inconsistency under prompt and temperature
variation; Zheng et al. (2023) for MT-Bench itself, the source of the position-bias and
flip-rate definitions used throughout.)*
