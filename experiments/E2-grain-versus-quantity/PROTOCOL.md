# E2 Protocol — experiment A, the forecast test

Paths are relative to the repository root. **Read this whole document before
doing anything**, because Step 0 is a prohibition and the rest is worthless if
it is broken.

---

## Step 0 — The contamination rule (read first, obey throughout)

> **Until Step 4 says so, do not open, print, grep, plot, or summarise anything
> under `experiments/M6-evaluation-suite/results_nemotron_llamacpp/`.**

Not the JSON, not the `.md`, not the queue logs' per-task lines. Checking
*whether the sweep has finished* is allowed (file counts, timestamps, whether the
process is alive). Reading *what it scored on which task* is not.

**Why this is not pedantry.** The whole value of this move is that the ranking
was written by someone who could not have known the answer. A ranking authored
after a glance — even an accidental one, even one you believe you ignored — is a
post-hoc fit wearing a forecast's clothes, and nothing in the result can
distinguish the two afterwards. There is no repair. The move is simply gone.

**If contamination happens anyway:** record it honestly in the pre-registration
file (`contaminated: true`, what was seen, when), run the analysis anyway if you
like, and **report it as exploratory, never as a forecast**. An honest weak
result beats a dishonest strong one.

**On qwen.** Blindness to qwen is already gone — this project has studied its
per-task pattern for weeks. That is acknowledged, not fixed. It constrains
*how* the ranking is authored: from **task structure only** (Step 2), never
from memory of which tasks qwen passed.

---

## Step 1 — Choose one proxy and write down which (10 minutes)

`02-capability-as-granularity.md` lists four candidate granularity proxies. Pick
**one** — or a stated, weighted combination — and commit to it before ranking
anything.

**Recommended default: P1, distinct entities that must be related.** It is the
most mechanically countable of the four, which matters more here than being the
most theoretically apt, because a proxy two people would rank differently cannot
support a forecast.

Operational counting rules, so the count is reproducible:

| proxy | count exactly this |
|---|---|
| **P1 — distinct entities** | number of distinct named code entities (files, functions, classes, symbols) that must be **read or modified** to satisfy the objective. Count an entity once regardless of how many times it appears. Count the test file only if the objective requires touching it |
| **P2 — hops of indirection** | longest chain of "to know X you must first look at Y" required to locate the change. Direct = 1 |
| **P3 — context-type heterogeneity** | how many *kinds* of context must be held at once, from: source, test, objective/intent, error output, history/prior decision. Range 1–5 |
| **P4 — counterfactual depth** | 1 if answering requires holding "what would be true otherwise" (false-premise detection, judging); 0 if not |

Write the choice into the pre-registration file's `proxy` field. **Do not change
it later.** If, while ranking, the proxy turns out to be unworkable, abort and
start a fresh pre-registration with the new proxy and a note saying the first was
abandoned before any result was read — do not silently switch.

---

## Step 2 — Rank the 34 tasks from structure alone (1–2 hours)

**Input, and the only input:**

- `experiments/M6-evaluation-suite/tasks.json` — 34 entries, each with `id`,
  `dir`, `objective`, `shape`, `trap`, `stresses`, `worker_view`.
- The task fixtures themselves: `experiments/M6-evaluation-suite/suite/<id>/`.

**Forbidden inputs:** any file under `results/` or `results_nemotron_llamacpp/`;
any `FINDINGS.md`; any arm comparison table; your own memory of which tasks qwen
found hard. If you catch yourself thinking *"this one was hard for qwen"*, that
thought is not evidence about granularity — set it aside and count the entities.

**Procedure, per task:**

1. Read the `objective` string and the fixture directory.
2. Apply the chosen proxy's counting rule. Write the raw count.
3. Write one sentence of justification naming what you counted. This exists so a
   second person can check the count, and so *you* can be caught out if the
   ranking drifts toward a remembered result.

Then sort by the count, descending. **Ties are allowed and expected** — do not
invent a tiebreak to produce a total order. A tie means the proxy does not
distinguish those tasks, which is information.

---

## Step 3 — Commit the pre-registration, then stop

Write `preregistration/ranking-<YYYY-MM-DD>.json`:

```json
{
  "schema": "e2-prereg/1",
  "authored": "ISO-8601",
  "author": "name",
  "proxy": "P1",
  "proxy_rule": "verbatim copy of the counting rule used",
  "contaminated": false,
  "attestation": "Authored from tasks.json and suite fixtures only. No Nemotron result read before this timestamp.",
  "ranking": [
    {"task": "wf1_crossfile", "count": 3, "rank": 12,
     "justification": "orders.py, pricing.py, test_task.py must all be read"}
  ],
  "prediction": "qwen<->Nemotron per-task divergence clusters in the top third of this ranking",
  "falsifier": "divergence distributed evenly across ranking thirds"
}
```

**Then `git commit` it, immediately, as its own commit, before reading
anything.** The commit timestamp is the evidence that the ranking predates the
result. A ranking sitting uncommitted in a working tree proves nothing.

Suggested message:

```
E2 pre-registration: granularity ranking of the 34 M6 tasks (proxy P1)

Authored from task structure only. No Nemotron per-task result read
before this commit.
```

---

## Step 4 — Only now, read the results

Preconditions: Step 3 is committed, and the Nemotron sweep is complete. Check
completeness without reading scores:

```bash
ls -1 experiments/M6-evaluation-suite/results_nemotron_llamacpp/*.json | wc -l
tail -3 experiments/M6-evaluation-suite/queue_nemotron_llamacpp_main.log
# expect the DONE line
```

If the sweep is **incomplete**, you may still proceed on the arms that finished —
record which arms those are. A partial sweep weakens power; it does not
invalidate the forecast.

**Build the divergence set.** For each task, compare qwen and Nemotron on the
same arm:

- qwen: `experiments/M6-evaluation-suite/results/<arm>.json`
- Nemotron: `experiments/M6-evaluation-suite/results_nemotron_llamacpp/<arm>.json`

Nemotron ran at **N=1**; qwen ran at N=3 or N=5 depending on arm. **Do not
compare a single Nemotron attempt against a qwen rate.** Collapse qwen to a
single comparable value per `(task, arm)` using a rule fixed here, before
looking:

> qwen counts as **pass** on `(task, arm)` iff it passed a **strict majority** of
> its reps. Cells where qwen is exactly split are labelled `qwen_unstable` and
> **excluded** from the divergence set, with the count of exclusions reported.

A task is `divergent` on an arm iff qwen's collapsed verdict and Nemotron's
single verdict differ.

---

## Step 5 — The test, stated before the data

Split the pre-registered ranking into **thirds** (high / mid / low granularity
demand). Count divergent tasks in each third.

| outcome | reading |
|---|---|
| divergence concentrated in the **high** third | consistent with the grain account. **Not confirmation** — 34 tasks cannot confirm anything; it is a survived prediction |
| divergence **evenly spread** across thirds | the falsifier fired. Whatever separates these two models does not track the proxy |
| divergence concentrated in the **low** third | actively against the account, and more interesting than either of the above. Report it loudly |
| **almost no divergence at all** | the test is uninformative — the two models agree per-task. Report as such; it is a finding about the suite's discrimination, not about grain |

**The power limitation, to be stated in the result, not discovered by a reader:**
34 tasks, split three ways, with N=1 on one side. This distinguishes "strongly
clustered" from "clearly even" and nothing finer. It is **directional, not
decisive**, and it does not substitute for the larger purpose-generated item set
or for experiment B.

**A second confound to state plainly:** Nemotron differs from qwen in
architecture (hybrid Mamba-2 vs. transformer), not only size or tuning. A
survived prediction therefore says the proxy tracks something robust across an
architecture change — a *stronger* claim than E4's size×tuning design makes — but
for exactly that reason this is **not** a substitute for E4's controlled design.

---

## Step 6 — Record it

1. `results/divergence.json` (the divergence set and the thirds counts) and
   `results/divergence.md` (readable).
2. Append a result section to the sheet. State: the proxy, the outcome, the
   power limitation, the architecture confound. **Do not** revise the
   pre-registration file — it is the evidence, and editing it destroys its value.
3. If the falsifier fired, say so in the sheet's status line, in those words.
   A falsifier that fires quietly is a falsifier that was never real.

## Done when

The pre-registration is committed with a timestamp preceding any Nemotron read,
`results/divergence.md` exists, and the sheet carries the outcome including its
stated limitations.
