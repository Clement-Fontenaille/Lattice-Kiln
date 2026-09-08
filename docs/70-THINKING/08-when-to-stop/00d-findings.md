# Cross-paper discussion — findings

*The reviews in this folder, taken up against each other, finding by finding.
Entry kinds: **finding** (evidence behind it), **qualifier** (bounds a finding),
**candidate argument** (unassessed). Candidates are staged in `00e-buffer.md` and
graduate here when accepted. Cross-references to topic 07's findings are written
"07-F<n>".*

## Findings

### F1 — The stop / continue / escalate decision cannot be sited in the model's own final verdict on its own work.

Five sheets converge from different directions.

- Sheet 01 (Kamoi survey) localises the weak link in feedback *generation*, not
  in refinement: a model can act on a reliable signal but cannot reliably produce
  one about its own output.
- Sheet 03 (AbstentionBench): volunteered abstention is flat across model scale
  from 8B to 405B, and gets *worse* under the training that improves task
  accuracy.
- Sheet 05 (Xiong): failure prediction from a bare verbalized confidence sits at
  AUROC in the low 50s, near chance; GPT-4 is best at 62.7 and still called
  suboptimal.
- Sheet 06 (judge biases): five of six judges inflate their own anonymised
  output, and the score moves while the stated rationale does not.
- Sheet 07 (glass-box): prompted self-scoring collapses to about 0.15 Pearson.

**Tension.** The signal is not *absent* from the model; it does not reach the
output under normal decoding. Sheet 14's mid-layer probe and a mid-reasoning
interrupt both recover an answerable / on-track signal at AUROC 0.87–0.97; sheet
13 shows P(True) works and verification scales faster than generation, in the
right format. F1 holds for the deployed agent setting because that setting is out
of the format and the distribution where the recovered signal is reliable. Kept
as candidate CF-23 in `00e-buffer.md`.

**Confirms / sharpens** topic 07: 07-F11, 07-F17, 07-F24, 07-F25, 07-F41, 07-F52,
07-F59.

**Consequence.** The stop signal must come from outside the model's *final
self-report* — an external check, a trajectory statistic, or a mid-reasoning
probe. "Ask the finished model whether it is done or stuck" is a floor baseline,
not a design.

### F2 — The trustworthiness of a validation runs inverse to its context continuity with the work.

Three regimes appear across the sheets, and trust drops as continuity rises.

- **Narration-continuous** — the validation reads the work's reasoning trace,
  revision history, or self-justification. This contaminates the verdict. Sheet
  06: showing the judge the revision history inflates the score by about a point
  on ten, with the justification unchanged. Sheet 03: judging the trace instead
  of only the final answer raises recall and *drops* precision, because the trace
  hedges indiscriminately. F11 / F12-analogues in this topic (stance, tone,
  provenance dominate the verdict) belong here.
- **State-continuous** — the validation reads the work's internal state. Mixed.
  Sheet 14: a probe on mid-layer activations separates answerable from
  unanswerable at AUROC 0.87–0.97. Sheet 07: softmax-dispersion features from the
  work's own forward pass correlate about 0.6 with a GPT-4 quality score. Both
  inherit the work's blind spots — sheet 07 cannot catch a confident
  hallucination because the signal *is* the work's confidence.
- **Re-derived** — the validation reruns from the artifact and reads nothing of
  how it was produced. The only regime the surveys trust. Sheet 12 (Reflexion):
  removing the self-written test check makes the loop worse than not iterating.
  Sheet 01 (Kamoi): the fair, reliable cases are external tools that never see
  the work's process.

**Open sub-note (travels with F2).** *Task*-information symmetry between work and
validation — does the validator have the same spec, inputs, and tools the work
had — is not measured by any sheet. Sheet 01's "information symmetry" is an
experiment-validity rule, not deployment advice, and sheet 01 says so. Cutting
process continuity (the isolation contract) is itself an information asymmetry,
so any "keep it symmetric" claim can at most be about task info, and even that is
an argument, not a result.

**Consequence.** Treat work↔validation continuity as an explicit design factor
with three levels. Expect discrimination to be worst at narration-continuous and
the trustworthy case to be re-derived.

### F3 — A check's resource is either draft-independent or draft-dependent, and only the second justifies an asymmetry.

Sheet 01 (Kamoi) splits validation-stage resources into two kinds. The split is a
design lever, not only an experiment-fairness label.

- **Draft-independent** — a fixed knowledge base, retrieval over a static
  corpus, a type checker, the task spec, a linter. Nothing stops the work from
  using these. If only the check uses them, the loop is under-equipped: the work
  keeps failing for a reason it cannot fix, and retry does not help. Kamoi's
  "unfair-asymmetric"; the fix is to give the resource to the work.
- **Draft-dependent** — a code interpreter (needs code to run), retrieval where
  the draft *is* the query, claim-level fact-checking (needs asserted claims).
  The resource becomes usable only once a draft exists, so the asymmetry is
  inherent. Kamoi's "fair-asymmetric". A vague task retrieves poorly while a
  draft names the entities that sharpen retrieval, and you cannot know what to
  check until something asserts it.

**Consequence.** When a check uses a resource, classify it. A draft-independent
resource used only at check time is a configuration error, not a finding. In a
loop, push a draft-independent resource the check needs up to the work through
the planner, rather than looping under-equipped work against the same check.
