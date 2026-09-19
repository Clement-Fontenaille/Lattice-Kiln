"""Two orderings for the judge's per-condition output, selected by env.

`LATTICE_JUDGE_FORMAT`:
    "decision_first"  (default) -- each `checked` entry opens with the verdict
                      token and justifies it afterwards: "yes - <reason>".
                      This is what every run before 2026-09-19 used.
    "reason_first"    -- each entry states the observation and ends with the
                      token: "<what you observe> -> yes".

Why this is a variable and not a fix. In the decision-first format the judge
commits to a verdict before writing the reason for it, and on
`judge_anchored`, `judge_bypass` and `judge_caveat` it rejected 21-31% of
candidates whose deterministic check had already passed. Those three arms are
also the only ones carrying a worked example in their JUDGE prompt, and that
example's first entry reads:

    "no - range(retries) with retries=0 skips the loop, then fn() runs once,
     so that one is satisfied"

The code it describes does satisfy the condition. The label says no and the
prose says yes. Measured across the three arms, that label/prose contradiction
appears in only 0.6-1.0% of condition assessments, so it does not by itself
explain the rejection rate -- it is a candidate cause to test, not a
demonstrated one.

The transformations below are exact string replacements and raise if the text
they expect is absent. A prompt variant that silently failed to apply would
produce a clean-looking null result, which is the failure mode this project
spent 2026-09-17 to 2026-09-19 recovering from.
"""
from __future__ import annotations

import os

DECISION_FIRST = "decision_first"
REASON_FIRST = "reason_first"
VALID = (DECISION_FIRST, REASON_FIRST)

_CONTRACT_OLD = '''  "checked": one line per condition, in order, each "yes" or "no"'''

_CONTRACT_NEW = '''  "checked": one line per condition, in order. Say what the code actually does
  for that condition FIRST, then the verdict token LAST:
      "<what you observe in the diff> -> yes"
      "<what you observe in the diff> -> no"
  Write the observation before you decide it. Do not open with the token.'''

_EXAMPLE_OLD = '''{"checked": ["no - range(retries) with retries=0 skips the loop, then fn() runs once,
so that one is satisfied", "no - the final fn() raises its own exception, which is not
kept from earlier attempts"], "verdict": "not_met", "instruction": "Re-raise the
exception from the last attempt when every attempt has failed."}'''

_EXAMPLE_NEW = '''{"checked": ["range(retries) with retries=0 skips the loop, then fn() runs once
-> yes", "the final fn() raises its own exception, which is not kept from earlier
attempts -> no"], "verdict": "not_met", "instruction": "Re-raise the
exception from the last attempt when every attempt has failed."}'''


def current() -> str:
    fmt = os.environ.get("LATTICE_JUDGE_FORMAT", DECISION_FIRST)
    if fmt not in VALID:
        raise ValueError(f"LATTICE_JUDGE_FORMAT must be one of {VALID}, got {fmt!r}")
    return fmt


def apply(judge_prompt: str) -> str:
    """Return the prompt in the format named by the environment.

    Raises if a replacement target is missing, rather than returning the prompt
    unchanged. An unapplied variant is indistinguishable from a null result.
    """
    fmt = current()
    if fmt == DECISION_FIRST:
        return judge_prompt

    out = judge_prompt
    if _CONTRACT_OLD not in out:
        raise RuntimeError(
            "judge_format: the `checked` contract line was not found; the JUDGE "
            "prompt has changed and this module needs updating before the "
            "reason_first variant can be trusted.")
    out = out.replace(_CONTRACT_OLD, _CONTRACT_NEW, 1)

    # The worked example exists in three of the seven arms. Correct it where it
    # is present; its absence is not an error.
    if _EXAMPLE_OLD in out:
        out = out.replace(_EXAMPLE_OLD, _EXAMPLE_NEW, 1)
    return out
