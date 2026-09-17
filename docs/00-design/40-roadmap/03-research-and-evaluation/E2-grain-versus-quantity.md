# E2 — Does grain matter independently of quantity?

**Status:** not run. Nobody appears to have run it anywhere.
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
