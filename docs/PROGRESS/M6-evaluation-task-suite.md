# M6 — Evaluation Task Suite

**Milestone:** `40-roadmap/01-milestones.md` → Milestone 6 (inserted by sequence
rework 2, `40-roadmap/07-sequence-rework-02.md`)
**Evidence question:** does a trap-structured task suite separate pipeline
variants that a toy fixture cannot, and does it surface failure modes the MVP
fixture missed?
**State:** IN EXECUTION (from 2026-09-02).

## Why this milestone exists

Every MVP-slice finding (entries 5–7) is qualified by "N ≤ 3, 4–6 synthetic
tasks, read the transcript not the score". M7 and every adaptive loop after it
decide things by running against tasks. The ruler has to exist and be good first.

## Deliverables

- **Spec** — `10-technical/10-evaluation-task-suite.md` (DONE). Normative:
  taxonomy (request shape × trap), task schema (`eval-suite-tasks/0`), scoring
  model (gating `SUBTESTS` + non-gating structural scores + `check_crashed`),
  determinism / anti-gaming rules.
- **Suite** — a versioned directory: wf1–wf6 folded in + ~28 intended tasks by
  trap class, each with a stdlib check, a documented discriminator subtest, a
  pre-existing passing test, and `stresses` tags.
- **Runner** — `run_suite.py`: arm-agnostic; reports per-task partial credit,
  terminal-vs-expected, `stresses` slices, decline accuracy, regression count,
  cost ledger vs a monolith baseline; reuses the M2 recorder.
- **Suite-lint** — every non-`decline` task has a documented discriminator; every
  task's check is stdlib-only and < 1 s.
- **Findings entry** — run the existing arms (monolith / d_loop / super-pipeline)
  against the full suite and report whether it separates them where N=3 on the
  toy fixture could not.

## Task breakdown

| # | task | state | notes |
|---|---|---|---|
| 1 | Spec `10-technical/10-evaluation-task-suite.md` | DONE | taxonomy + schema + scoring normative |
| 2 | Fold wf1–wf6 into the suite dir, re-tagged | TODO | |
| 3 | Behaviour-preserving tasks (`hf_extract_fn`, `hf_dict_dispatch`, `hf_rename`, `hf_rec_to_iter`) | TODO | load L2-structural — the weakest stage |
| 4 | Push-back tasks (`hf_suppress`, `hf_already_optimal`, `hf_dead_code`, `hf_remove_validation`, `hf_cache_nondeterministic`) | TODO | load premise-audit beyond wf4 |
| 5 | Backward-compat tasks (`hf_multi_recipient`, `hf_return_shape`, `hf_deprecate`, `hf_json_field`) | TODO | load regression-guard |
| 6 | Edge-coverage tasks (`hf_timeout_param`, `hf_cache_decorator`, `hf_csv`, `hf_path_sanitize`, `hf_merge_config`) | TODO | partial-credit / K-way synth |
| 7 | Misdirection tasks (`hf_pagination`, `hf_misfiled_bug`) | TODO | cross-file |
| 8 | Silent-failure / robustness (`hf_validate_withdraw`, `hf_retry_backoff`) | TODO | |
| 9 | Multi-concern (`hf_json_serialize`, `hf_api_v1_to_v2`) | TODO | concern-split / combined-score |
| 10 | Concurrency (`hf_counter_race`) | TODO | threading, deterministic-ish |
| 11 | `run_suite.py` + suite-lint | TODO | |
| 12 | Baseline run (monolith / d_loop / super-pipeline) + M6 findings entry | TODO | the evidence question |

## Notes

- The suite is the anchor later milestones measure drift against; it is fixed and
  offline by design. Context-quality metrics (M9), meta-evaluation (M14), and
  cross-generation benchmarking (M15) share the fixtures, not the metric.
- If ~34 tasks do not separate arms at N=3–5, growing the catalogue is itself an
  M6 outcome, not a failure.
