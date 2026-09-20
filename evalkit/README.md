# evalkit — results that outlive the experiment that produced them

Tests live here, not inside an experiment. An experiment **declares the cells it
needs**; the planner answers `needed − have = run`, and existing results are
reused by design rather than by somebody remembering they exist.

## The problem it replaces

Until 2026-09-19 a result was identified by **which directory it sat in**.
`results/` meant qwen. `results_nemotron_nothink/` meant Nemotron with reasoning
off. Nothing else recorded the model, the reasoning setting, the fixture version
or the arm version — so "can I reuse this?" was answered by reading directory
names, diffing arm files against git history, and remembering which sweep was
which.

That failed, concretely and recently. E8's first seeder green-lit stale qwen
rows because it checked the two repaired tasks were *present* in a tree — they
were, in their stale form — and the directory name said nothing about the
fixture version.

## The unit

A **Cell** is everything that can change an outcome except the draw itself. Reps
are draws from a cell, so `rep` is not part of cell identity.

| field | why it is in the key |
|---|---|
| `fixture_sha` | this task's fixture files, hashed. **Per task, not per suite** — the 0.4.1 bump changed 2 fixtures of 34, and keying on a suite version refused the other 32 for no reason |
| `task` | |
| `arm` | |
| `arm_sha` | the arm's source. Strict: the rotated-argument bug of 2026-09-17 changed logic without touching prompts |
| `prompt_sha` | the prompts that arm will actually send, after the judge-format transform. Separate from `arm_sha` so a change moving one and not the other is visible |
| `backend`, `model`, `params` | `think`, `min_predict`, `num_ctx` |
| `judge_format` | `decision_first` \| `reason_first` |

## A cell is a fact; a declaration is a query

A cell never carries a wildcard. `params` holds what actually ran, so a default
expands to its concrete value rather than standing for "whatever was usual that
week". That is strict on purpose: `num_ctx` was 16384 for the arms queued before
the 2026-09-15 cut and 8192 after, and a cell says which.

Vagueness belongs to the experiment, not the key. A declaration may give a param
the value **`"any"`**, which means two different things on the two sides:

| | |
|---|---|
| **running** | use the ambient default, and record the concrete result |
| **matching** | accept a stored row whatever value it has there |

E8 varies the judge's output order, not the context ceiling, so it declares
`"num_ctx": "any"` and reuses rows from either side of that cut. The effect is
measurable rather than rhetorical:

| E8 declaration | `judge_anchored`/qwen/`decision_first` | total reuse |
|---|---|---|
| silent — default expands to 8192 | 0 of 170 | 15% |
| `"num_ctx": "any"` | 170 of 170 | 23% |

Omission is **not** `any`. A param the declaration leaves out still expands to
the default and must match it exactly; only `any` waives the comparison. And
`any` is per key — one wildcard does not wave through the rest of the dict.

`model_digest` is recorded but **not** in the key: legacy rows have none, and
requiring one would refuse everything recorded before today. The rule is
*known-different blocks, unknown abstains*.

## Provenance, and why it is two words

Every entry carries one:

- **`recorded`** — the harness wrote the setup at run time.
- **`declared`** — the setup was supplied afterwards from
  `migration_manifest.json`, because the row predates the harness recording it.

Nothing treats those as equal. `plan.py --require-recorded` refuses declared
rows outright.

## Waivers

A hash difference refuses reuse. That is the default and the safe direction. To
admit rows across a difference you write a **waiver**: one field, the two values,
a date, and the evidence.

`waivers.json` currently holds three, one per judge arm, for the `arm_sha` moved
by 654ac97 — which added an import and one line, and under `decision_first`
leaves the prompt unchanged. Each carries the diffstat that shows it. Rows under
`reason_first` are not admitted by them, because `prompt_sha` differs there and
still blocks.

A waiver is an artifact. `store.have()` applies one; it decides nothing.

## Using it

```bash
python migrate.py --dry-run          # legacy trees -> store, report only
python migrate.py                    # 1210 cells, 2581 rows

python plan.py <declaration.json>              # needed - have = run
python plan.py <declaration.json> --explain    # and why cells do not match
python plan.py <declaration.json> --no-waivers # hashes alone

python run_plan.py <declaration.json> --dry-run   # the commands it would issue
python run_plan.py <declaration.json>             # run the deficit, nothing else
```

`run_plan.py` closes the loop: it groups the deficit by (arm, model, format) --
the unit `run_suite` takes -- and passes only the tasks still short, so a group
that is nine-tenths complete costs a tenth of a run. On E8 it issues **11** runs
rather than 12, because `qwen/decision_first/judge_anchored` is already
satisfied.

`run_suite --store-resume` is what makes that safe at rep granularity. Plain
`--resume` sees only the results directory it is writing to, so a rep another
experiment already paid for would be run again; `--store-resume` counts what the
store holds for this exact setup, wherever it was produced. Demonstrated:

```
store already holds 3 rep(s) across 1 task(s) for this setup
[4/5] wf1_crossfile rep4 (judge_bypass) ...
[5/5] wf1_crossfile rep5 (judge_bypass) ...
```

Three `declared` reps and two `recorded` ones now sit in one cell, and the plan
drops that task from the deficit. Rep numbers are per-series labels, not
identities -- N reps held anywhere satisfy the first N of a target.

A declaration names arms, models, judge formats, a task set and a target rep
count — see `experiments/E8-judge-verdict-order/declaration.json`. The planner
resolves it against the **current** environment, so an edited arm produces
different cells and prior rows correctly stop matching.

## Layout, and the air-gapped case

```
evalkit_store/
  index.jsonl            one line per (cell, rep): cell fields inline, plus
                         provenance and where the row lives
  rows/<cell_id>.jsonl   the rows
```

Append-only. Two stores merge by concatenating both files and de-duplicating on
`(cell_id, rep, row_sha)` — which is what a run on a disconnected machine needs,
and why the index carries the cell fields inline instead of pointing at a table
that would have to travel with it.

## Two bugs this found in itself, worth knowing about

Both produced *wrong hashes for identical content*, and both were caught because
`--explain` names the differing fields rather than just saying "no match".

1. **`sorted()` on `Path` is case-insensitive on Windows.** The working-tree
   hasher ordered `orders.py` before `README.md`; the git-side hasher sorted raw
   names and put `README.md` first. Same files, different hash, on one platform.
2. **`subprocess(text=True)` decodes with the locale encoding**, cp1252 here, not
   UTF-8. One README with a multi-byte character was enough to mojibake the
   git-side read and disagree with the same bytes off disk.

Both are now sorted on the same canonical key and decoded explicitly as UTF-8,
with a regression check: every unchanged fixture hashes identically from the
working tree and from `git show`, and exactly the two repaired fixtures differ.
