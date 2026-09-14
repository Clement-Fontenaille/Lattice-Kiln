# Open questions that could become experiments

*The register. A question is here because an experiment could settle it, not because
one is planned. A question earns its own sheet when it is circumscribed enough to
state what would falsify it.*

> **Motto:** A question with no falsifier is a position, not an experiment.

## How a question leaves this file

Three ways, and only one of them is running something.

**It gets a sheet.** The question is circumscribed, the arms are nameable, and what a
null result would mean is decidable in advance. That is the bar, and most questions
here do not meet it yet.

**It turns out not to be empirical.** Several questions that looked like they needed
evidence were build decisions an existing contract already covered. Asking *is this
design, implementation, or evidence?* dissolves more of these than running anything
would.

**It is answered by a measurement rather than an experiment.** A measurement has no
arms and no hypothesis — the bootstrap occupancy test
(`10-technical/05-provisional-invariant-list.md`) is one. Those belong in the
specification that requires them, not here.

## With a sheet

| | Question | Sheet |
|---|---|---|
| **E0** | Is the evaluation suite measuring one coherent thing? | [`E0-suite-construct-validation.md`](E0-suite-construct-validation.md) |
| **E1** | Can context pathology be detected from processing? | [`E1-context-pathology-probe.md`](E1-context-pathology-probe.md) |
| **E2** | Does grain matter independently of quantity? | [`E2-grain-versus-quantity.md`](E2-grain-versus-quantity.md) |
| **E3** | Does a graded ladder of relational demand behave monotonically? | [`E3-first-ladder.md`](E3-first-ladder.md) |
| **E4** | How does the suite behave across model size and tuning? | [`E4-capability-sweep.md`](E4-capability-sweep.md) |
| **E5** | How much does the operator account for the outcome? | [`E5-population-spread.md`](E5-population-spread.md) |
| **E6** | Does the system hold and use knowledge it did not derive itself? | [`E6-corpus-digestion.md`](E6-corpus-digestion.md) |
| **E7** | Which scenarios flipped between the M4 and M5 arms? | [`E7-paired-reanalysis.md`](E7-paired-reanalysis.md) |

## Without a sheet yet

Each of these could become one. None is circumscribed enough today, and the note says
what is missing.

**Does an isolated judge actually judge differently?** A scope check assembled off the
prefix of the work it judges is required to be isolated
(`10-technical/14-context-manager.md`), on the argument that it would otherwise
inherit the reasoning it assesses. Nothing has tested that the inheritance changes the
verdict. *Missing: a scope check to run, which is M17.*

**Does recording a derived scope with its derivation change whether it gets
contested?** The whole derive-record-contest requirement rests on the claim that an
uncontested derivation is ratified rather than caught. *Missing: an operator
population, which is the same gap E5 has.*

**Does splitting a processor's output measurably help?** The reasoning/conclusion cut
is argued from four consequences and measured in none. *Missing: the cut to be
implemented; and a design that separates the recall saving from the independence
effect, since both would move together.*

**Is registration order actually the worst ordering?** The degenerate recall policy
orders by registration time and the specification calls that arbitrary
(`10-technical/07-naive-context-assembly.md`). Arbitrary is not the same as bad.
*Missing: at least one alternative ordering to compare it against, which is what a
live set carrying origin invocation now makes expressible.*

**Does the incremental deletion walk stay cheap?** Removal runs per task end rather
than as a periodic sweep (`10-technical/12-knowledge-model.md`), a trade of one large
occasional cost for many small ones. *Missing: a corpus large enough for the question
to have an answer, which E6 produces.*

**Does a 7B follow the framework's conventions well enough to work inside it?**
Several measured failures were compliance failures rather than capability ones — the
implementer that narrates, the planner that blocks on "not built yet". `70-THINKING`
I14 proposes fine-tuning as the answer. *Missing: a way to evaluate it that is not
circular, since training on this project's runs and testing on this project's suite
are close to the same corpus.*

**Does the corpus-as-system-output constraint actually bite?** Comparisons hold within
a lineage and transfer is a separate measurement
(`00-design/23-arch-context-management/02-context-as-experimental-surface.md`).
*Missing: two lineages to compare, which needs generations, which is M13.*

## What would make the whole plan wrong

- **E0 says the suite is incoherent.** Most of this loses its instrument and reorders
  around building one.
- **E2 returns null.** The decomposition account retires to *relevant context beats
  maximal context*, and E3 loses its motivation — though a ladder may survive as a
  difficulty scale without it.
- **A materially stronger model arrives before E0–E2 run.** The comparisons are then
  against a moving target, and the ageing rules applied to external evidence
  (findings entry 9) apply to this project's own results too.
