# E8 Protocol

Paths are relative to the repository root. No fixture changes. The suite must be
**0.4.1** throughout — the counter-semantics repair of 2026-09-19 — on both
models and both formats.

---

## Step 0 — Preconditions

```bash
python -c "import json;print(json.load(open('experiments/M6-evaluation-suite/tasks.json'))['suite_version'])"
# expect: 0.4.1

cd experiments/M7-static-workflow
for f in decision_first reason_first; do
  LATTICE_JUDGE_FORMAT=$f python -c "
import sys; sys.path.insert(0,'.')
import judge_anchored_workflow as w
print('$f', 'verdict token LAST' in w.JUDGE, 'so that one is satisfied' in w.JUDGE)"
done
# expect: decision_first False True
#         reason_first  True  False
```

If the second block does not print exactly that, stop. `judge_format.apply()`
raises when its replacement target is missing, but a prompt that changed shape
could still satisfy the raise and not the intent.

Ollama must be the sole occupant of the card; `queue_runner` checks this per job.

---

## Step 1 — Run the queue

```bash
cd experiments/M6-evaluation-suite
python queue_runner.py --queue ../E8-judge-verdict-order/queue.json
```

12 jobs, grouped arm → model → format, so a queue that stops early leaves
complete 2×2 cells rather than halves. Resumable: `run_suite --resume` keeps
recorded rows and `rows_for()` counts only `run_ok` ones.

Results land in `experiments/E8-judge-verdict-order/results/<model>_<format>/`.

---

## Step 2 — Check the format was obeyed, before reading any score

The variant can apply and still be ignored. Read the recorded `checked` strings:

```bash
cd experiments/M7-static-workflow
python - <<'EOF'
import json
for arm in ("judge_anchored","judge_bypass","judge_caveat"):
    rows=[json.loads(l) for l in open(f"stage_influence_{arm}.jsonl",
          encoding="utf-8",errors="replace") if l.strip()]
    for r in rows[-34:]:
        jc=r.get("judge_candidates"); jc=jc if isinstance(jc,list) else eval(jc or "[]")
        for v in jc:
            for c in (v.get("checked") or []):
                c=str(c).strip().lower()
                print(arm, "OPENS-WITH-TOKEN" if c[:3] in ("yes","no ","no-") else "ends-with-token")
EOF
```

In `reason_first` the entries must **end** with `-> yes` / `-> no`. If they still
open with the token, the judge disregarded the contract: **that is the result**,
and no score comparison below is meaningful. Record it and stop.

---

## Step 3 — The primary measure

Rejections of check-passing candidates, per arm × model × format: candidates
whose deterministic check was already full and whose verdict is `not_met`.

The `decision_first` figures already exist for Nemotron
(`50-findings/13`): 15/54 (28%), 17/55 (31%), 9/42 (21%) for
`judge_anchored`, `judge_bypass`, `judge_caveat`. Those were taken before the
0.4.1 fixture repair, so **they are not the control** — this experiment
re-measures `decision_first` on the repaired suite.

| | expected if ordering is the cause | expected if it is not |
|---|---|---|
| `reason_first` rejection rate | materially below `decision_first` | unchanged |

Report both models separately. They are not pooled: they differ in size,
architecture, quantisation and lineage at once.

---

## Step 4 — The secondary measure

Earned score over the 28 non-floor tasks, with `baseline` and `monolith` read
from `M6-evaluation-suite/results/` and
`M6-evaluation-suite/results_nemotron_nothink/` as the floor and the no-judge
reference. Neither is re-run: neither has a judge stage, so neither can move
with this variable.

Score is the downstream consequence of the rejection rate, not the measurement.
A format that lowers rejections without raising score is still informative, and
means the rejections were not what was costing the score.

---

## Step 5 — Record

`results/e8.md` and `results/e8.json`, then a findings entry if the result is
noteworthy. State, whatever the outcome:

- that `reason_first` changes **two** things at once — the ordering and the
  corrected example — so a positive result does not attribute to either alone;
- that label/prose contradictions ran at 0.6–1.0% in the `decision_first`
  measurements, which is too low to explain a 21–31% rejection rate, so the
  example is unlikely to be the whole of any effect found;
- N=1, three arms, one suite.

## Done when

Both formats have run on both models for all three arms, Step 2 confirms the
contract was obeyed, and the rejection rates are recorded per cell.
