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
