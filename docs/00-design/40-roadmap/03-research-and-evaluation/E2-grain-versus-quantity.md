# E2 — Does grain matter independently of quantity?

**Status:** **forecast move run 2026-09-17 — prediction failed, result not
interpretable as evidence about grain.** The token-matched design remains not run.
**Gates:** E3's motivation.
**Protocol:** [`experiments/E2-grain-versus-quantity/PROTOCOL.md`](../../../../experiments/E2-grain-versus-quantity/PROTOCOL.md)
— covers the forecast move below. The token-matched design is not buildable yet;
the folder's README says why.

## The question

The discriminator for the decomposition account
(`00-design/22-arch-cognition/08-decomposition.md`). That account holds that what
varies with an assembly's capability is the **coarsest grain it can integrate
correctly**, not how much it can hold.

## What would falsify it

Two arms, **token-matched and sufficiency-matched**, varying only the level of
abstraction at which the same information is supplied. If the coarse arm and the fine
arm come out equal, grain does not matter independently of quantity.

Token-matching and sufficiency-matching are both required. Matching only tokens lets
the fine arm carry more information; matching only sufficiency lets it carry more
tokens.

## What a null means

**The decomposition account collapses into *relevant context beats maximal context*
and should be retired to that sentence.** This is the cleanest retirement condition in
the folder, and it is why this experiment ranks high despite nothing depending on it:
it can remove a standing account rather than refine one.

E3 then loses its motivation, though a ladder may survive as a difficulty scale
without the account behind it.

## A cheaper move first — forecast against an unseen model, not fit

The token-matched/sufficiency-matched design above is not yet buildable cleanly:
size can only be matched by padding the shorter arm with filler validated inert
by a calibration run; content can only be matched as *entailed sufficiency*, not
literal equivalence, since coarsening is lossy by construction; format is only
held fixed by generating both arms from one canonical state through matched
templates, not by hand-writing a raw document and a summary of it (operator's
working notes, 2026-09-15). None of that apparatus exists yet.

`02-capability-as-granularity.md`'s "forecast, don't fit" move is cheaper and
runs on data already being produced:

1. **Pre-register a granularity ranking of the 30 M6 suite tasks, in writing,
   timestamped, before reading any per-task Nemotron result.** One proxy (or a
   stated combination) from the candidates already listed there: distinct
   entities to relate, hops of indirection, context-type heterogeneity,
   counterfactual depth. Authored from task **structure**, not from memory of
   which tasks qwen passed — true blindness to qwen's pattern is already gone
   (this project has studied it for weeks), so the ranking must not be
   reverse-engineered from a half-remembered result.
2. **Nemotron is already running the same 30-task suite**, on a genuinely
   different architecture (hybrid Mamba-2) with no prior exposure in this
   project's analysis — a real held-out subject, unlike qwen.
3. **Prediction:** wherever Nemotron and qwen diverge (newly passed / newly
   failed, task by task) should **not** be scattered randomly across the
   pre-registered ranking. The grain account predicts divergence clustering at
   the high-granularity-demand end. Even scattering falsifies — cleanly, not
   ambiguously — that whatever separates these two models on this suite tracks
   the proxy at all.

**Cost:** zero marginal apparatus. The Nemotron sweep already running (M6, N=1,
llama-server backend) turns from a throughput comparison into hypothesis
evidence for free, provided the ranking is committed before its per-task results
are read. It is also a **different, and additional**, confound to E4's
size-and-tuning design: Nemotron is architecturally different from qwen (hybrid
Mamba-2 vs. transformer), not just differently sized or tuned, so a positive
result here says the grain proxy tracks something surviving an architecture
change too — a stronger claim than E4 alone can make, but for the same reason
not a substitute for E4's controlled size×tuning design.

**Named limitation, not deferred:** **30 tasks is thin for this.** A forecast
test over 30 points has little power to distinguish "clusters at the
high-demand end" from "mildly correlated by chance" — this reads as
**directional, not decisive**, on the current suite. The real-powered version
needs the larger, purpose-generated item set `02-capability-as-granularity.md`
already scopes under "item generation changes what is hard" (over-generate,
pilot, keep on measured discrimination) — this move is worth running now, on
what exists, as a cheap first look, not as a substitute for that larger set or
for the token-matched design above once it is buildable.

### Result, 2026-09-17

Pre-registration committed at `2820d0c` before any Nemotron result was read;
proxy **P1** (distinct named entities to read or modify), bands by count value:
high ≥ 4 (14 tasks), mid = 3 (6), low = 2 (14). Analysis:
[`experiments/E2-grain-versus-quantity/results/divergence.md`](../../../../experiments/E2-grain-versus-quantity/results/divergence.md).

**The sweep had not finished.** Of 15 arms, Nemotron completed two —
`baseline` and `test_synth` — and died with `judge_anchored` started but never
returned. `baseline` makes no model call, so **one arm is usable**. It did serve
as a harness sanity check: 34 baseline tasks, **zero mismatches** between the
Ollama and llama-server backends, which is worth having independently.

#### The prediction failed, in the falsifier's stronger form

| band | tasks | divergent | rate |
|---|---|---|---|
| **high** | 14 | 4 | **28.6%** |
| mid | 6 | 4 | 66.7% |
| **low** | 14 | 9 | **64.3%** |

Divergence did not cluster at the high-granularity end. It clustered at the
**low** end — which the pre-registration named as *"actively against the
account"*, not merely as the even-distribution null.

#### But the test is partly blind, and the blindness is concentrated in the high band

Two classes of task cannot diverge on `objective_pass` whatever the models do:
false-premise tasks (doing nothing is the answer) and the three no-witness tasks
E0's untouched-source test identified **the same day** (`wf3_refactor`,
`hf_extract_fn`, `hf_dict_dispatch`).

**Six of the fourteen high-band tasks are in one of those classes** — against two
of fourteen in the low band. Excluding them:

| band | sighted tasks | divergent | rate |
|---|---|---|---|
| high | 8 | 4 | 50.0% |
| mid | 5 | 4 | 80.0% |
| low | 12 | 9 | 75.0% |

The prediction still fails. The gap narrows a great deal.

#### What this actually measured

Nemotron passes **10/34** against qwen's **25/34** on this arm, and **16 of 17
divergences are qwen-passes-where-Nemotron-fails**. That is dominated by one
model being weaker on this arm, not by a grain-structured difference in where
they fail.

**Verdict: this says little about grain and a good deal about instrument
readiness.** `00-questions.md` orders E0 before E2, and this run is a concrete
demonstration of why — nearly half the high band is composed of items whose
gating metric cannot see whether the work was done, so the band with the
strongest prediction attached to it is the band least able to test it.

#### Two things learned about the proxy itself

1. **P1 partly tracks trap type rather than grain.** False-premise tasks name
   many entities — the thing that is not broken, plus its callers — so they
   score high on entity count while being trivially passable by doing nothing.
   Three of them landed in the high band. Any next proxy should be checked
   against `trap` and `expect.decline_correct` before being used.
2. **The forecast move is not re-runnable on this pre-registration.** The
   ranking has now been compared against results; re-running it on the remaining
   arms when the sweep completes would no longer be blind. Those arms can be
   reported as **exploratory** — the pre-registered forecast has been spent.

#### What would make this worth re-running

A fresh pre-registration, after E0's defect-1 repair decision is made and the
no-witness tasks are fixed, against a completed sweep. In that order — the
instrument first, then the forecast.
