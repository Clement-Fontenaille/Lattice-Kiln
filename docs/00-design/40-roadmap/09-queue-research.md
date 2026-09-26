# Queue B — result unpacking and research steps

**What belongs here:** work whose output is a judgement about what a number
means. Not outsourceable, because the failure mode is a plausible-looking
conclusion rather than a failing test.

**What does not belong here:** anything with a mechanical acceptance test. That
is [Queue A](08-queue-dev-outsourceable.md).

**Standing discipline**, earned the hard way over 2026-09-23/26:

- A number earns its ground before it is interpreted. Read the artifact, not the
  summary.
- Print the series when the group is small; five numbers plus the censoring
  count above that. Shape — gaps, bimodality — is invisible in quantiles.
- A probe that does not reproduce the phenomenon licenses nothing, in either
  direction. Include the arm that is known to fail.
- Susceptibility can be a **task×model interaction**. An entry built on one
  model will read an interaction as a difficulty.

---

## B1 — Read the matrix *(first, when it lands)*

3 models × 11 arms, n=1, v2 protocol, temp 0.6/0.95. A survey: it finds where
differences are, it does not establish them.

**Questions, in order:**

1. Does the arm ladder hold on the 9B and on qwen, or is 6/34 → 27/34 a 4B
   story? The lift is the project's central claim and it has one model behind it.
2. Which tasks **flip** between arms, per model (needs A7). A flip names a
   condition; a rate names nothing.
3. Do the crash and regression columns stay concentrated in the unverified arms?
   On the 4B only `monolith` and `monolith_recovery` crashed at all — every
   arm with a verification step sat at zero.
4. Where do `tool_recovered` and `tool_repaired` fire, per model? qwen needs
   repair structurally (unescaped quotes in file content); the 4B should not.

**Output:** a short written reading, and a shortlist of comparisons worth n≥3.

## B2 — E0, with a second question it did not have

Already P2 and promoted: does the suite discriminate *designs* or merely
*tasks*? M7 and `dloop` both scored 24/30 with four tasks flipping between them.

`50-findings/16` adds a second: **does it discriminate capability from decode
pathology?** Degeneracy is a task×model interaction — `hf_retry_backoff`
collapses 0/11 for qwen and 33/40 for the 4B, while `hf_rename` and
`hf_extract_fn` never collapse for either. A per-task difference between two
models is partly a difference in which items trigger each one's sampler.

**Possibly answerable from data already on disk**, including the matrix. Try
that before scheduling runs.

## B3 — Settle the sampling per model

`temperature 0.6 / top_p 0.95` is the documented tool-calling setting for both
Nemotrons and was applied to qwen for comparability, not because qwen documents
it. On the 4B's retry prompt: 0.2 capped 9/20, 0.6 capped 2/20, 1.0 capped 0/20
— but 0.6 was cheapest at every quartile (median 1652 against 1690 and 2118).

**Open:** whether 0.6's 2/20 residue is better absorbed by recovery than bought
out with ~22% more decode everywhere. And what qwen's own documentation says,
which nobody has read.

## B4 — Does recovery earn its place?

`monolith_recovery` 18/34 against `monolith` 14/34 on the 4B, crashes 8→7,
regressions 11→9. n=1, and the arms share a cell-level confound worth checking
before anything is claimed.

**The floor it has to beat is the naive retry**, which is now general: every arm
gets one more draw on a collapse, recorded with `worked: true/false`. If simply
asking again works, a diagnosis and a steering sentence buy nothing. That
comparison is available from the journal in rows already collected — no paired
sweep needed.

**Also open:** the one standalone test said resume wrote 2/10 against a plain
restart's 6/10, on a probe whose 2048 cap bound half the calls and whose
`conclude` criterion was unreachable in a single call. Flawed, and pointing
against the main remedy.

## B5 — The `hf_json_serialize` case

The only task in the 4B sweep where the judge arm **lost** ground: `monolith`
5/5, `judge_anchored` 2/5. A judge rejecting correct work is the failure mode
`50-findings/14` is about, and here there is a concrete instance with a
transcript rather than a rate.

**Read it.** One case, read properly, is worth more than another rate.

## B6 — Audit S1–S8 against criterion 5

`E5-skill-scales.md` gained a fifth convergence criterion on 2026-09-25: every
candidate names something it blocked, or is marked as not yet observed to block
anything.

**The omission that prompted it:** none of S1–S8 is **termination**, though it
is the prerequisite to all of them and is exactly what failed. Nor is escaping
inside a structured envelope, nor tolerating an unfamiliar delimiter, nor
noticing your own repetition — all watched failing, all carrying detectors and
fixtures (`E4` appendix).

**Expect:** S2 and S3 have grounding; S4–S7 may have none yet. Marked, not
removed — the sheet's own working rule keeps awkward demands written down.

## B7 — Who owns the model-facing contract?

The adapter layer produced most of this week's failures, was given its own
fingerprint and its own recovery, and **no milestone owns it**. On vLLM we
choose the chat template rather than inherit one, which is a design decision
with consequences and no home.

**Decide:** a new milestone, or a package inside an existing one. Note that the
Claude Code teardown in `70-THINKING/15` has the same gap — its six layers fold
the contract into "Backend" beside memory and MCP. A taxonomy that does not name
it will mistake adapter defects for model limits, which is the error this
project made repeatedly.

## B8 — Keep v2 or revert?

The protocol rework produced **16/34 both ways** at suite scale, with
`lost-conclude` 2→0 and `recovered` 5→2 — movements too small to attribute at
n=1 per task. The textual contradiction it fixed ("conclude is required on every
turn" against the template's "answer the question like normal") is real and
appears inconsequential.

The real fix was reading Ollama's source, not rewriting the prompt. **v2 earns
no claim.** Keeping it on clarity grounds is defensible; saying it helped is not.

---

## Dependencies between the queues

| B item | needs from A |
|---|---|
| B1 | A5 (partial tails), A6 (matrix reader), A7 (flip table) |
| B2 | A7 |
| B4 | A8 (counters in the report) |
| everything off this machine | A1, A2, A3 |

A1–A3 are the hard blocker: the H100 has no Ollama, and `backends.py` is
imported by nothing.
