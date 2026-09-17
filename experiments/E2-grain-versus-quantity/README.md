# E2 — Does grain matter independently of quantity?

**Sheet:** [`docs/00-design/40-roadmap/03-research-and-evaluation/E2-grain-versus-quantity.md`](../../docs/00-design/40-roadmap/03-research-and-evaluation/E2-grain-versus-quantity.md)
**Status:** not run.
**Gates:** E3's motivation. A null here retires the decomposition account.

## Two experiments live under this sheet, and only one is buildable today

### A — the forecast test (buildable now, protocol written)

Pre-register a granularity ranking of the 34 M6 suite tasks, then check whether
qwen↔Nemotron divergence clusters where the ranking predicts. Costs nothing: the
Nemotron sweep is already running for other reasons.

**This has a deadline.** The pre-registration is only honest while nobody has
read Nemotron's per-task results. Every day it sits undone, the chance someone
glances at `results_nemotron_llamacpp/` rises, and the move is then unavailable —
permanently, since you cannot un-see a result.

### B — the token-matched/sufficiency-matched arms (not buildable yet)

The sheet's primary design. Blocked on apparatus that does not exist, for three
reasons established 2026-09-15:

| invariant | why it is not free |
|---|---|
| **size** | a coarse rendering is naturally shorter; matching tokens means padding the coarse arm with filler, and filler is itself a dilution confound unless first validated inert by a calibration run |
| **content** | coarsening is lossy *by construction*, so literal content-matching is impossible. The achievable invariant is **entailed sufficiency**: both arms entail the same set of propositions needed to answer the check |
| **format** | a hand-written raw document and a hand-written summary differ in genre, not just grain. Format is only held fixed by rendering both arms from **one canonical state through matched templates** |

Until those exist, B is not runnable and no amount of care in writing the two
arms substitutes for them.

## Layout

```
E2-grain-versus-quantity/
  README.md          this file
  PROTOCOL.md        experiment A, step by step
  preregistration/   the ranking, committed BEFORE any Nemotron result is read
  results/           committed output
```
