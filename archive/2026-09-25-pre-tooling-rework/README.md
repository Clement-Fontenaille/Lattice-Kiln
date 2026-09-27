# Archive — corpus from before the tool-calling rework

Moved 2026-09-27. Nothing here is deleted; every tracked file is recoverable
with `git log --follow` or by moving it back.

## The boundary

The output contract changed twice in late September 2026: the bespoke
`<<<FILE>>>` marker protocol gave way to the model's native tool-calling
channel (`protocol: markers` -> `protocol: tools`), and that protocol was then
revised (v1 -> v2). The change is keyed — `params.protocol` and
`params.adapter` on every store row — so the two corpora never pool silently.

The live corpus is the full matrix: on the 4B every arm holds exactly 34 rows
at adapter `63b5b222daf4`. Everything in this directory predates that sweep.

## What is here

| path | what | last written |
|---|---|---|
| `M6-results/results` | the default results dir, 36 files | 2026-09-24 |
| `M6-results/results_nemotron` | first 9B sweep | 2026-09-18 |
| `M6-results/results_nemotron_nothink` | 9B, reasoning off | 2026-09-19 |
| `M6-results/results_nemo3_fair` | 4B fair-run comparison | 2026-09-24 |
| `M7-stage-logs/*.jsonl` | stage records for arms retired before the matrix | 2026-09-19 |
| `M7-runs/runs_*` | the matching run/event directories | 2026-09-19 |
| `pools/evalkit_pool.archived-*` | two already-archived work pools, untracked | 2026-09-20, -22 |

The M7 arms archived here — `judge_staged`, `m7b`, `m7c`, `m7e`, `m7f`,
`test_synth_retry` — are the ones `queue_full_matrix.py` deliberately excludes:
"barely exercised … sweeping them would spend the night on cells nothing reads".
They will not be re-run, so their logs will not grow.

## What was deliberately NOT archived, and why

**The matrix was running while this was done** — `queue_full_matrix.py` plus
`run_suite.py --arm judge_anchored --store-resume`, writing every few minutes.
Untouched, in consequence:

- `evalkit_store/` — live, and the source of truth for every current reading
- `experiments/M6-evaluation-suite/results_matrix_*` — the live sweep's output
- `experiments/M6-evaluation-suite/matrix_logs/` — live
- `evalkit_pool/` — `evalkit.pool.DEFAULT_POOL` still points at it
- `stage_influence_{judge_anchored,judge_caveat,judge_bypass,judge_fullctx,test_synth}.jsonl`
  and `stage_influence.jsonl`, with their `runs_*` directories

**The last group is the dirty one and is still dirty.** Those files are
append-only piles spanning both protocols and up to three models, with up to 13
records per `(task, rep)` key — see `50-findings/17`. They cannot be archived
wholesale because the matrix-tagged records inside them are the only clean judge
data there is. Splitting them by `results_subdir` is the right operation and
should happen **after the matrix finishes**, not during.

`results_proto_v1/` and `results_proto_v2/` also stay. They are not stale
leftovers — they are the deliberate v1/v2 comparison that Queue B item B8 reads.

## Consequence: readers that pointed at `results/`

About twenty analysis scripts resolve a path ending `"results"`, among them
`M6/collect.py`, `M6/plots.py`, `M7/compare_arms.py`, `M7/score_correlation.py`,
`M7/score_self_report.py`, `E0/item_analysis.py` and `E7/flip_table.py`. They
will now find nothing there.

That is mostly correct rather than broken: they are readers of the pre-rework
corpus, which moved with them into `M6-results/results`. Point them here, or at
`results_matrix_*`, depending on which corpus the question is about — and say
which, because `50-findings/17` exists precisely because that went unsaid.

`run_suite.py` recreates `results/` on any run that does not set
`LATTICE_RESULTS_SUBDIR`. A new directory of that name is new data, not a
restoration of this one.
