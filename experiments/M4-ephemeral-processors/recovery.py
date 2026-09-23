"""A failure is a signal. Diagnose it, choose a remedy, and RECORD the help.

WHY THIS EXISTS. A model that collapses into repetition is telling the system
something: it has nothing further to add from where it is standing. Counting
that as a zero throws the signal away. The system can often supply what the
model could not find for itself -- a detail lost in noise, a different sampling
regime, a concrete next step -- and that is the whole claim of this project:
the assembled system reaches higher than the bare model.

THE DISCIPLINE THAT MAKES IT HONEST. Recovery is a MEASUREMENT, not a cover-up.
Every attempt is counted and reported beside the score, so a result reads "this
model passed, with two interventions" rather than "this model passed". A
processor that quietly retries until something works is not raising a ceiling,
it is hiding one. Two rules follow, and neither is optional:

    1. Every remedy is recorded -- which mode, which remedy, whether it worked.
    2. Any remedy that changes model-visible text or sampling MOVES THE ADAPTER
       KEY, so recovered rows never pool with clean ones.

WHAT THE FAILURE MODES ARE. Read off 637 stored outputs and a day of reading
transcripts rather than imagined:

    degenerate_repetition  the model emits the same span until the cap. Two
                           shadows, one shape: qwen echoes the PROMPT (median
                           coherent prefix 0 chars -- it never starts), the 4B
                           repeats ITS OWN last sentence (median 640 chars
                           under markers, 3460 under tools). 50-findings/16.
    truncated_empty        done_reason=length with no content and no tool call.
                           Almost always the above, seen from outside.
    malformed_call         a call-shaped span that will not parse. qwen escapes
                           newlines and not quotes, so a docstring breaks its
                           own tool call. Documented upstream as a family trait.
    unparsed_call          a well-formed call the server did not extract --
                           qwen emits bare JSON where its template demands
                           <tool_call>. The MODEL complied with the contract it
                           was tuned on; the template asked for another.
    no_conclude            the tool loop ended without the closing call.
    no_progress            two attempts produced byte-identical work. Retrying
                           the same way cannot help and must not be counted as
                           an attempt remaining.

WHERE THE REMEDIES COME FROM. Each is the cheapest intervention that addresses
the mechanism, ordered so the least invasive runs first:

    repetition   -> repeat_penalty, THEN temperature. Both cure a loop, and
                    they distinguish the cause: if the penalty alone fixes it,
                    loops were merely unpenalised; if only temperature does,
                    the 0.2 setting is the fault. The corpus was gathered at
                    temperature 0.2 with reasoning ON, where NVIDIA pair 0.2
                    with reasoning OFF and 0.6+ with it ON, and the model's own
                    Modelfile ships 1.0.
    repetition   -> then a CONCRETE-STEP re-ask. Measured on wf2_retry: the
                    model looped on "so they want 2? that's retries?" while the
                    prompt already contained the test source AND the hint
                    "Make self.calls reflect the number of attempts". It had
                    the answer and could not land on it, so the remedy names
                    one action rather than adding information.
    malformed    -> repair client-side first; only then ask again, naming the
                    escaping rule, because the model's content is usually
                    correct and only its JSON is not.
    no_progress  -> ESCALATE. Never retry. Identical output twice means the
                    model is where it is going to stay.

This module decides only. It does not call a server, so it is testable without
one, and the executor stays in the processor where the gate already lives.
"""
from __future__ import annotations

import json
import re
import zlib
from dataclasses import dataclass, field
from typing import Any

# Compression ratio below which text is degenerate. The distribution over 637
# stored long outputs is bimodal -- p25 0.070, p75 0.352 -- so this sits in a
# gap rather than on a slope, and samples either side were read by eye.
DEGENERATE_RATIO = 0.12
MIN_CHARS_TO_JUDGE = 1500


@dataclass(frozen=True)
class Diagnosis:
    mode: str
    evidence: str
    #: False when the same thing has already been tried and changed nothing.
    actionable: bool = True


@dataclass(frozen=True)
class Remedy:
    """One intervention. `options` are sampling overrides; `nudge` is appended
    to the prompt; `escalate` means stop and hand back."""
    name: str
    options: dict[str, Any] = field(default_factory=dict)
    nudge: str = ""
    escalate: bool = False

    def describe(self) -> str:
        bits = [self.name]
        if self.options:
            bits.append(" ".join(f"{k}={v}" for k, v in sorted(self.options.items())))
        if self.nudge:
            bits.append(f"nudge={self.nudge[:40]!r}")
        return " | ".join(bits)


ESCALATE = Remedy("escalate", escalate=True)

# The compact table. Ordered, least invasive first. Exhausting a row escalates.
LADDER: dict[str, list[Remedy]] = {
    "degenerate_repetition": [
        Remedy("penalise repetition", {"repeat_penalty": 1.3}),
        Remedy("raise temperature", {"temperature": 0.6, "top_p": 0.95}),
        Remedy("name one concrete step", {"temperature": 0.6, "top_p": 0.95},
               nudge=("You went in a circle. Do not re-derive what the numbers "
                      "mean. State the ONE change you will make, make it, and "
                      "stop.")),
    ],
    "truncated_empty": [
        Remedy("penalise repetition", {"repeat_penalty": 1.3}),
        Remedy("raise temperature", {"temperature": 0.6, "top_p": 0.95}),
        Remedy("answer before reasoning", {"temperature": 0.6, "top_p": 0.95},
               nudge=("Write the answer FIRST, then stop. Any reasoning must "
                      "fit in a few sentences before it.")),
    ],
    "malformed_call": [
        # The repair already runs in the client; this is for when it fails too.
        Remedy("restate the escaping rule", {},
               nudge=('Your tool arguments were not valid JSON. Inside a JSON '
                      'string every " must be escaped as \\" and every newline '
                      'as \\n. Send the call again.')),
        Remedy("raise temperature", {"temperature": 0.6, "top_p": 0.95}),
    ],
    "unparsed_call": [
        # Recovered client-side already; nothing to ask the model for.
        Remedy("accept client-side recovery", {}),
    ],
    "no_conclude": [
        Remedy("ask for the closing call", {},
               nudge="Call conclude exactly once now, and nothing else."),
    ],
    "no_progress": [ESCALATE],
}


def _repetition_span(text: str, win: int = 80) -> str | None:
    """The first window that has already appeared earlier, if any."""
    seen: dict[str, int] = {}
    for i in range(0, max(0, len(text) - win), 20):
        w = text[i:i + win]
        if w in seen:
            return w
        seen[w] = i
    return None


def is_degenerate(text: str) -> tuple[bool, str]:
    """Compression ratio, with the repeated span quoted as evidence.

    Ratio rather than an n-gram count because it catches BOTH shadows with one
    threshold: a prompt echo and a self-repeat have different content and the
    same shape. That the detector found both was the clue that they are one
    mechanism.
    """
    if len(text) < MIN_CHARS_TO_JUDGE:
        return False, ""
    ratio = len(zlib.compress(text.encode("utf-8"), 6)) / len(text)
    if ratio >= DEGENERATE_RATIO:
        return False, ""
    span = _repetition_span(text) or text[-80:]
    return True, f"ratio={ratio:.3f} repeats={span.strip()[:70]!r}"


def diagnose(*, text: str = "", thinking: str = "", tool_calls: list | None = None,
             done_reason: str | None = None, error: str = "",
             wanted_conclude: bool = False, malformed: int = 0,
             recovered: int = 0, previous_output: str | None = None) -> Diagnosis | None:
    """Name the failure, or None if the turn was fine.

    Ordered so the most specific wins. `no_progress` is checked FIRST because
    it overrides everything: a model repeating its previous answer verbatim is
    not going to be helped by a different temperature.
    """
    whole = (thinking or "") + (text or "")
    calls = tool_calls or []

    if previous_output is not None and whole and whole == previous_output:
        return Diagnosis("no_progress", "byte-identical to the previous attempt",
                         actionable=False)

    bad, why = is_degenerate(whole)
    if bad:
        return Diagnosis("degenerate_repetition", why)

    if done_reason == "length" and not text and not calls:
        return Diagnosis("truncated_empty",
                         f"done_reason=length, {len(thinking)} chars of thinking, "
                         f"no content and no tool call")
    if "truncated" in error or "empty response" in error:
        return Diagnosis("truncated_empty", error[:120])

    if malformed:
        return Diagnosis("malformed_call", f"{malformed} call-shaped span(s) would not parse")
    if recovered and not calls:
        return Diagnosis("unparsed_call", f"{recovered} call(s) recovered from text")
    if wanted_conclude and not any(c.get("name") == "conclude" for c in calls):
        return Diagnosis("no_conclude", f"loop ended with {len(calls)} call(s), no conclude")
    return None


def plan(diag: Diagnosis, attempt: int) -> Remedy:
    """The remedy for this diagnosis at this attempt. Exhausted rungs escalate.

    `attempt` is 0 for the first recovery, 1 for the second, and so on -- not
    the number of model calls, which a tool loop inflates.
    """
    if not diag.actionable:
        return ESCALATE
    rungs = LADDER.get(diag.mode)
    if not rungs or attempt >= len(rungs):
        return ESCALATE
    return rungs[attempt]


@dataclass
class Journal:
    """What help was given. Reported beside the score, never folded into it."""
    entries: list[dict[str, Any]] = field(default_factory=list)

    def record(self, diag: Diagnosis, remedy: Remedy, worked: bool | None = None) -> None:
        self.entries.append({"mode": diag.mode, "evidence": diag.evidence,
                             "remedy": remedy.name, "options": remedy.options,
                             "nudged": bool(remedy.nudge),
                             "escalated": remedy.escalate, "worked": worked})

    @property
    def interventions(self) -> int:
        return sum(1 for e in self.entries if not e["escalated"])

    def summary(self) -> dict[str, Any]:
        return {"interventions": self.interventions,
                "modes": sorted({e["mode"] for e in self.entries}),
                "escalated": any(e["escalated"] for e in self.entries),
                "detail": self.entries}

    def fingerprint(self) -> str:
        """Hash of the help given, for the adapter key.

        A recovered run saw different prompts and different sampling from a
        clean one. If that does not move the key, recovered and unrecovered
        rows pool silently -- the defect 50-findings/15 closes on, which this
        module would otherwise reintroduce at a new layer.
        """
        import hashlib
        payload = json.dumps([{k: e[k] for k in ("mode", "remedy", "options", "nudged")}
                              for e in self.entries], sort_keys=True)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]


def _selftest() -> None:
    loop = "So they want 2? That's retries? So they got 1, which is retries-1. " * 60
    d = diagnose(thinking=loop, done_reason="length")
    assert d and d.mode == "degenerate_repetition", d
    assert plan(d, 0).options == {"repeat_penalty": 1.3}
    assert plan(d, 1).options["temperature"] == 0.6
    assert plan(d, 2).nudge
    assert plan(d, 3).escalate

    assert diagnose(text="def f():\n    return 1\n" * 5) is None

    d = diagnose(text="", thinking="x" * 40, done_reason="length")
    assert d and d.mode == "truncated_empty", d

    d = diagnose(text="ok", previous_output="ok")
    assert d and d.mode == "no_progress" and plan(d, 0).escalate

    d = diagnose(text="{...}", malformed=1)
    assert d and d.mode == "malformed_call"

    d = diagnose(text="done", tool_calls=[{"name": "write_file"}], wanted_conclude=True)
    assert d and d.mode == "no_conclude"

    j = Journal()
    j.record(Diagnosis("degenerate_repetition", "x"), plan(d, 0), worked=True)
    assert j.interventions == 1 and len(j.fingerprint()) == 12
    print("recovery selftest ok")


if __name__ == "__main__":
    _selftest()
