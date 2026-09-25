# Buffer — Small-Model Lift

*A staging area. Nothing here is locked. Grow it and consume it at any pace.*

- **Candidate findings** graduate to `00d-findings.md` with an F-number when
  accepted. Rejected ones are struck through and kept, so they are not
  re-proposed.
- **Proposed ideas** graduate to the global `../ideas.md` with an I-number when
  accepted.
- **Reading queue** is what I propose to read next, in my suggested order.

**Sweep tag.** `[SWEEP]` changes what an upcoming sweep should measure or build.
`[background]` is reference for later.

---

## Source dropped 2026-09-25

**Paulius Iusztin, LinkedIn, "dissecting how Claude Code works".** Not a paper,
not peer reviewed, no measurements — a practitioner's architecture teardown.
Treat as a **structural claim to test against our own build**, not as evidence.
Points at an open-sourced companion agent ("Decode") on GitHub, unread.

Its six layers, as stated:

| layer | described as |
|---|---|
| Surface | CLI / SDK / IDE, streaming, approvals, real-time steering |
| State | conversation history, project instructions, session events |
| Core | the agent loop: Reason → Act → Observe → Repeat |
| Safety | whether a command runs, needs permission, or is blocked |
| Backend | tool implementations, context management, memory, skills, remote execution, MCP |
| Evals harness | benchmarking, regression testing, observability |

Headline claim: **the model is "just one box inside a much larger system"**, and
most production engineering is in the surrounding harness.

---

## Candidate leads

### C1 — The six-layer split against ours [background]

Our architecture is not organised this way, and the differences are the
interesting part rather than the overlap.

- **Safety** maps cleanly onto M3's gate: every proposed effect routed, only
  what the floor passes realised. We have it, and ours refuses rather than asks,
  because there is no interactive operator inside a sweep.
- **Evals harness** is M6 and this whole folder. Theirs is listed as a layer;
  ours is the point of the project.
- **Surface** we effectively do not have, and it is worth naming as an absence:
  "real-time steering" and "approvals" presuppose a human in the loop, which a
  batch sweep has by construction removed. Anything their harness achieves
  through mid-flight human correction, ours has to achieve some other way or
  not at all.
- **State** is the one we are thinnest on. We have per-rep workspaces and a
  transcript sink; we do not have session events feeding back into context.

**Why it matters to this topic:** if most of the lift is harness rather than
model, then the layers a harness is *missing* bound the lift available. Ours is
missing Surface entirely and thin on State.

### C2 — "Reason → Act → Observe → Repeat" is what we just measured [SWEEP]

The Core loop as stated is exactly the tool loop built on 2026-09-23/24, and
today's results say the **Observe** step is where the engineering sits, not the
loop shape:

- returning the bare word `recorded` as the observation produced 4,466
  characters of circular reasoning and no answer; a structured result naming
  what happened fixed it (`processor._tool_result`).
- the `conclude` call — the loop's own terminator — failed to parse on 11 of 34
  runs, discarding completed work, and the fix was reading Ollama's renderer
  source rather than any change to the loop.

So a teardown that names the loop and stops there has named the cheap part. The
candidate finding is that **loop shape is not where small-model lift comes from;
the fidelity of the observation step is**.

### C3 — Evals as a *layer* versus evals as the instrument [background]

They list an evals harness beside the others, with named observability tools.
Ours is not a layer — it is what the rest exists to feed. Worth holding as a
contrast when this topic asks what a harness is *for*: if evals are a layer, the
harness is a product; if evals are the instrument, the harness is an experiment.
This project is the second, and the distinction may explain why we keep finding
defects a product-shaped harness would absorb silently (the 11 lost runs would
have been invisible without the transcript sink).

### C4 — "Most of the engineering is in the harness" is testable here, and partly tested [SWEEP]

We have a same-day, same-model, same-sampling pair: `monolith` (one shot) at
16/34 against `judge_anchored` at 24/34, with regressions 8→0 and crashes 6→0.
That is harness structure moving outcome on a fixed model, which is the claim in
its strong form.

But it is **not yet clean**: the monolith side lost completed work on 11 rows to
a parse defect when that gap was first measured, and the arms differ in more than
"judged" — `judge_anchored` also retries against a failing check. The lead is to
use this comparison as the topic's quantitative anchor once the matrix sweep
lands, not to quote the gap as it stands.

### C5 — The absent layer: nothing owns the model-facing contract [SWEEP]

None of the six layers is the **adapter** — the thing that decides what format
the model is asked to emit and how its output is read back. In our build that
turned out to be where several days of failures lived (50-findings/15, /16), and
it needed its own key (`adapter_fingerprint`) once it was recognised as a
variable rather than plumbing.

Their taxonomy folds it into Backend alongside memory and MCP. Candidate
finding: **a harness taxonomy that does not name the model-facing contract as
its own layer will mistake adapter defects for model limits.** That is exactly
the error this project made repeatedly before the layer was named.

---

## Reading queue

1. **The "Decode" repo** the post links. A named, open, small agent harness is
   directly comparable to ours, and reading code beats reading a teardown of
   code. Specifically: what it puts in its Observe step, and whether anything
   owns the model-facing format.
2. Anything on **agent loop observation fidelity** — the C2 lead is ours alone at
   present and wants external company or contradiction.
3. Deprioritised: the observability tools named (Opik, Kitaru). Product-shaped
   evals, likely C3's contrast rather than method.

---

## Not a finding, flagged

The post is a LinkedIn teardown with no measurements and no method section. It
is useful as a **taxonomy to argue with** and as a pointer to a repo. Nothing in
it should graduate to `00d-findings.md` on its own authority; C1–C5 are claims
about *our* build prompted by it, and each is either already measured here or
names what would measure it.
