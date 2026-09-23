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

    repetition   -> temperature, and NOT repeat_penalty. The obvious remedy
                    was tried first and measured worse: on a prompt where every
                    other sampling arm capped 0/20, repeat_penalty 1.3 capped
                    6/18 and ran ~4x longer. It does not stop the model
                    looping, it stops it TERMINATING, because ending a
                    generation re-uses tokens the penalty is suppressing.
                    Temperature remains the candidate: the corpus was gathered
                    at 0.2 with reasoning ON, where NVIDIA pair 0.2 with
                    reasoning OFF and 0.6+ with it ON, and the model's own
                    Modelfile ships 1.0. UNTESTED against a prompt that
                    actually loops -- see the note in probe_temperature_tail.
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
    """One intervention.

    `options`  sampling overrides for the retry
    `steer`    the sentence aimed at whatever the processor could not get past
    `resume`   hand its own partial work back and continue from there, rather
               than restarting. Default TRUE: a restart discards work that was
               sound and usually walks into the same wall by the same route.
    `escalate` stop and hand back
    """
    name: str
    options: dict[str, Any] = field(default_factory=dict)
    steer: str = ""
    resume: bool = True
    escalate: bool = False

    @property
    def nudge(self) -> str:
        """Back-compat alias; `steer` is the name that says what it is for."""
        return self.steer

    def describe(self) -> str:
        bits = [self.name]
        if self.options:
            bits.append(" ".join(f"{k}={v}" for k, v in sorted(self.options.items())))
        if self.steer:
            bits.append(f"steer={self.steer[:40]!r}")
        return " | ".join(bits)


ESCALATE = Remedy("escalate", escalate=True)

# The compact table. Ordered, least invasive first. Exhausting a row escalates.
LADDER: dict[str, list[Remedy]] = {
    "degenerate_repetition": [
        # NOT repeat_penalty. Measured 2026-09-24 on the implementer prompt:
        # every other sampling arm capped 0/20, and repeat_penalty 1.3 capped
        # 6/18 with its convergent calls running ~4x longer (3747-5809 against
        # a ~900 baseline). Penalising repetition does not stop the model
        # looping, it stops it TERMINATING -- ending a generation means
        # re-emitting tokens it has already used, and the penalty is on those
        # too. The obvious remedy for a repetition loop makes it worse.
        Remedy("resume at higher temperature", {"temperature": 0.6, "top_p": 0.95},
               steer="Continue from where you stopped. Do not start over."),
        Remedy("name one concrete step", {"temperature": 0.6, "top_p": 0.95},
               steer=("You went in a circle. Do not re-derive what the numbers "
                      "mean. State the ONE change you will make, make it, and "
                      "stop.")),
    ],
    "truncated_empty": [
        Remedy("raise temperature", {"temperature": 0.6, "top_p": 0.95}),
        Remedy("answer before reasoning", {"temperature": 0.6, "top_p": 0.95},
               steer=("Write the answer FIRST, then stop. Any reasoning must "
                      "fit in a few sentences before it.")),
    ],
    "malformed_call": [
        # The repair already runs in the client; this is for when it fails too.
        Remedy("restate the escaping rule", {},
               steer=('Your tool arguments were not valid JSON. Inside a JSON '
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
               steer="Call conclude exactly once now, and nothing else."),
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


# --------------------------------------------------------------- the processor
#
# The ladder above is a default, not the design. A table cannot tell whether
# the model looped because it misread the task, because the context buried the
# detail it needed, or because it simply had nothing left -- and those want
# different remedies. So the recovery step is itself a PROCESSOR: it reads the
# objective, the context the failing processor was given, what it produced, and
# why recovery fired, then chooses.
#
# WHAT IT MUST NOT BE GIVEN. The raw failure is often 25,000 characters of the
# same sentence. Feeding that in wastes the budget and invites the reader into
# the same loop. It gets a DIGEST instead: the coherent prefix (where real work
# stopped), the repeated span, and how many times it repeated. The prefix is
# the informative part -- it is where the processor was still thinking, and it
# is what says whether it misread the task or ran out.

RECOVERY_ROLE = """\
You are a recovery processor. Another processor failed and you decide what to
do about it. You are not solving the task yourself.

You are given the objective, what the failing processor was shown, a digest of
what it produced, and the detected failure mode. Read the coherent part of its
output: it shows what the processor was actually doing before it broke.

Choose ONE option from the menu and call choose_remedy. Prefer the cheapest
option that addresses what you actually observe. Escalate when nothing on the
menu would plausibly help -- a processor repeating a previous answer verbatim,
or one that has already been retried without change, is not going to be
rescued by another attempt.

Give a one-sentence reason naming the evidence you used.
"""

#: What the recovery processor may choose. Kept to one line each: it is a menu
#: for a small model under a token budget, not documentation.
MENU: dict[str, str] = {
    "raise_temperature": "resample at temperature 0.6 - for a decode loop with no other fault",
    "concrete_step": "re-ask naming one action, at temperature 0.6 - when it had the answer and circled",
    "answer_first": "re-ask for the answer before any reasoning - when it never reached an answer",
    "restate_escaping": "re-ask naming the JSON escaping rule - when the content was right and the call would not parse",
    "surface_the_detail": "re-ask with the buried detail quoted back - when the prefix shows it missed something present in its context",
    "accept": "take what was recovered, no further call - when the work is already usable",
    "escalate": "stop and hand back - when no option would plausibly help",
}

CHOOSE_TOOL = [{
    "type": "function",
    "function": {
        "name": "choose_remedy",
        "description": "Pick one option from the menu and say why.",
        "parameters": {"type": "object", "properties": {
            "remedy": {"type": "string", "enum": sorted(MENU)},
            "reason": {"type": "string",
                       "description": "One sentence naming the evidence."},
            "detail": {"type": "string",
                       "description": "Only for surface_the_detail: the text to quote back."},
        }, "required": ["remedy", "reason"]}}}]

#: Menu choices that are not on the static ladder, mapped to what they do.
_EXTRA: dict[str, Remedy] = {
    "raise_temperature": Remedy("raise temperature", {"temperature": 0.6, "top_p": 0.95}),
    "concrete_step": LADDER["degenerate_repetition"][-1],
    "answer_first": LADDER["truncated_empty"][-1],
    "restate_escaping": LADDER["malformed_call"][0],
    "accept": Remedy("accept client-side recovery", {}),
    "escalate": ESCALATE,
}


#: Decode budget for a recovery attempt. LOWER than the original on purpose.
#: A resumed attempt starts with the work already done, so it needs room for a
#: conclusion, not for the whole task again -- and if it re-enters the loop, a
#: small budget catches that in seconds instead of burning another 8192 tokens.
#: The cost of being wrong is one more cheap attempt; the cost of being generous
#: is another full-length runaway.
RECOVERY_NUM_PREDICT = 2048


def ellipsize_loop(text: str, keep: int = 2) -> tuple[str, int]:
    """Collapse the repeated span, keep everything else. -> (text, repeats)

    NOT a truncation. The coherent part is the work the processor actually did
    and it is expensive to regenerate -- 6618 characters of real reasoning in
    the case this was built from. Only the loop is compressed, because after
    the second occurrence every further copy carries nothing.
    """
    span = _repetition_span(text)
    if span is None:
        return text, 0
    onset = text.find(span)
    reps = text.count(span)
    head = text[:onset]
    sample = span.strip()
    return (f"{head}{sample}\n"
            f"[... you then repeated that same sentence about {reps} times and "
            f"made no further progress ...]"), reps


def build_resume(*, original_prompt: str, text: str = "", thinking: str = "",
                 steer: str) -> str:
    """The main remedy: hand the processor its own work back, and unstick it.

    A retry from scratch discards everything and re-pays for it, and usually
    walks into the same wall by the same route. Resuming keeps the reasoning
    that was sound, shows the processor where it started going in circles, and
    adds one sentence aimed at the specific thing it could not get past.

    The loop is ellipsized rather than cut, so the processor sees that it
    looped -- which is itself information it did not have while looping.
    """
    prior, reps = ellipsize_loop((thinking or "") + (text or ""))
    return (f"{original_prompt}\n\n"
            f"--- YOUR PREVIOUS ATTEMPT, WHICH WAS STOPPED ---\n"
            f"{prior}\n"
            f"--- END OF PREVIOUS ATTEMPT ---\n\n"
            f"{steer}")


def digest_failure(text: str = "", thinking: str = "", limit: int = 700) -> str:
    """The failure, small enough to read and still diagnostic.

    Shows where coherent work STOPPED, because that is the part that says
    whether the processor misread the task or simply ran out. The loop itself
    is summarised to one span and a count.
    """
    whole = (thinking or "") + (text or "")
    if not whole:
        return "(no output at all)"
    span = _repetition_span(whole)
    if span is None:
        return f"{len(whole)} chars, no repetition detected:\n{whole[:limit]}"
    onset = whole.find(span)
    reps = whole.count(span)
    head = whole[:min(onset, limit)]
    return (f"{len(whole)} chars total. Coherent for the first {onset} chars, "
            f"then one span repeated ~{reps} times.\n"
            f"--- coherent part (where it was still working) ---\n{head}\n"
            f"--- the repeated span ---\n{span.strip()}")


def build_brief(*, objective: str, diag: Diagnosis, context_shown: str,
                text: str = "", thinking: str = "", attempt: int = 0,
                context_limit: int = 1800) -> str:
    """Everything the recovery processor reads, and nothing else."""
    menu = "\n".join(f"  {k}: {v}" for k, v in MENU.items())
    ctx = context_shown if len(context_shown) <= context_limit else (
        context_shown[:context_limit // 2] + "\n[...trimmed...]\n"
        + context_shown[-context_limit // 2:])
    return (f"{RECOVERY_ROLE}\n"
            f"# OBJECTIVE THE FAILING PROCESSOR WAS GIVEN\n{objective}\n\n"
            f"# WHAT IT WAS SHOWN\n{ctx}\n\n"
            f"# WHY RECOVERY FIRED\n{diag.mode}: {diag.evidence}\n"
            f"recovery attempts already made: {attempt}\n\n"
            f"# WHAT IT PRODUCED\n{digest_failure(text, thinking)}\n\n"
            f"# MENU\n{menu}\n")


def decide(*, objective: str, diag: Diagnosis, context_shown: str,
           text: str = "", thinking: str = "", attempt: int = 0,
           ask=None) -> tuple[Remedy, str]:
    """Choose a remedy. -> (remedy, reason)

    `ask` is a callable taking (prompt, tools) and returning the tool calls, so
    this module still makes no network call and stays testable. With ask=None
    it falls back to the static ladder -- a recovery step that cannot run
    because a second model call failed would be a worse failure than the one it
    was sent to fix.
    """
    def budgeted(r: Remedy) -> Remedy:
        """Every retry decodes under a LOWER cap than the original.

        A resumed attempt begins with the work already done, so it needs room
        to finish rather than to start again. And if it falls back into the
        loop, a small cap ends it in seconds instead of spending another full
        budget discovering the same thing twice. Being wrong costs one cheap
        attempt; being generous costs another runaway.
        """
        if r.escalate or "num_predict" in r.options:
            return r
        return Remedy(r.name, {**r.options, "num_predict": RECOVERY_NUM_PREDICT},
                      r.steer, r.resume, r.escalate)

    if not diag.actionable:
        return ESCALATE, "previous attempt produced identical output"
    if ask is None:
        return budgeted(plan(diag, attempt)), "static ladder (no consultant available)"
    brief = build_brief(objective=objective, diag=diag,
                        context_shown=context_shown, text=text,
                        thinking=thinking, attempt=attempt)
    try:
        calls = ask(brief, CHOOSE_TOOL) or []
    except Exception as e:  # noqa: BLE001
        return budgeted(plan(diag, attempt)), f"static ladder (consult failed: {e!r})"
    for c in calls:
        if c.get("name") != "choose_remedy":
            continue
        a = c.get("arguments") or {}
        pick = str(a.get("remedy", "")).strip()
        why = str(a.get("reason", "")).strip()[:200]
        if pick == "surface_the_detail":
            d = str(a.get("detail", "")).strip()
            if not d:
                break
            return budgeted(Remedy("surface the buried detail",
                          {"temperature": 0.6, "top_p": 0.95},
                          steer=("You already had this in your context and did "
                                 f"not use it:\n{d}\nMake the one change it "
                                 "implies, then stop."))), why
        if pick in _EXTRA:
            return budgeted(_EXTRA[pick]), why
    return budgeted(plan(diag, attempt)), "static ladder (no usable choice returned)"


def _selftest() -> None:
    loop = "So they want 2? That's retries? So they got 1, which is retries-1. " * 60
    d = diagnose(thinking=loop, done_reason="length")
    assert d and d.mode == "degenerate_repetition", d
    assert plan(d, 0).options["temperature"] == 0.6, plan(d, 0)
    assert "repeat_penalty" not in plan(d, 0).options, "measured harmful"
    assert plan(d, 1).nudge
    assert plan(d, 2).escalate

    assert diagnose(text="def f():\n    return 1\n" * 5) is None

    d = diagnose(text="", thinking="x" * 40, done_reason="length")
    assert d and d.mode == "truncated_empty", d

    d = diagnose(text="ok", previous_output="ok")
    assert d and d.mode == "no_progress" and plan(d, 0).escalate

    d = diagnose(text="{...}", malformed=1)
    assert d and d.mode == "malformed_call"

    d = diagnose(text="done", tool_calls=[{"name": "write_file"}], wanted_conclude=True)
    assert d and d.mode == "no_conclude"

    # the processor form
    brief = build_brief(objective="Add a retries parameter.",
                        diag=Diagnosis("degenerate_repetition", "ratio=0.07"),
                        context_shown="client.py ...", thinking=loop)
    assert "# MENU" in brief and "# WHY RECOVERY FIRED" in brief
    assert "repeated span" in brief
    fake = lambda prompt, tools: [{"name": "choose_remedy",
                                   "arguments": {"remedy": "concrete_step",
                                                 "reason": "it had the hint"}}]
    r, why = decide(objective="x", diag=Diagnosis("degenerate_repetition", "e"),
                    context_shown="c", thinking=loop, ask=fake)
    assert r.nudge and why == "it had the hint", (r, why)
    surf = lambda prompt, tools: [{"name": "choose_remedy",
                                   "arguments": {"remedy": "surface_the_detail",
                                                 "reason": "buried",
                                                 "detail": "self.calls counts attempts"}}]
    r, _ = decide(objective="x", diag=Diagnosis("degenerate_repetition", "e"),
                  context_shown="c", thinking=loop, ask=surf)
    assert "self.calls counts attempts" in r.nudge
    boom = lambda p, t: (_ for _ in ()).throw(RuntimeError("down"))
    r, why = decide(objective="x", diag=Diagnosis("degenerate_repetition", "e"),
                    context_shown="c", thinking=loop, ask=boom)
    assert "static ladder" in why and not r.escalate
    r, why = decide(objective="x", diag=Diagnosis("no_progress", "same", actionable=False),
                    context_shown="c", ask=fake)
    assert r.escalate

    j = Journal()
    j.record(Diagnosis("degenerate_repetition", "x"), plan(d, 0), worked=True)
    assert j.interventions == 1 and len(j.fingerprint()) == 12
    print("recovery selftest ok")


if __name__ == "__main__":
    _selftest()
