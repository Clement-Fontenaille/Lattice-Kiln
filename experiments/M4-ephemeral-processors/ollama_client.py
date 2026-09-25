"""Thin non-streaming Ollama client for the M4 processor runtime.

Working default per M0 findings-log entry 1: qwen2.5-coder 7B Q4_K_M, fully
GPU-resident on the reference host. Stdlib only (urllib).

DEFAULT_NUM_CTX cut from 16384 to 8192 on 2026-09-15, mid the M6 overnight
queue (queue.json), to free VRAM for a second worker -- observed usage on the
implementer role was ~900-950 tokens/call, nowhere near either bound. This
changes a variable partway through a table `queue.json` itself calls out as
meant to be comparable on one suite version; jobs already run (baseline,
test_synth, judge_anchored, m7f, judge_fullctx) used 16384, everything after
uses 8192. Flagged, not hidden -- see M6's queue notes/findings before reading
across that boundary. Not yet observed to truncate anything, but the
full-context judge arms are the ones most likely to feel it first.
"""
from __future__ import annotations

import gzip
import hashlib
import socket
import json
import os
import re
from pathlib import Path
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any

DEFAULT_MODEL = os.environ.get("LATTICE_EVAL_MODEL", "qwen2.5-coder:7b-instruct-q4_K_M")
# LATTICE_NUM_CTX: the context ceiling, settable because it now binds.
#
# It was hardcoded while it was slack -- observed usage sat around 900-950
# tokens per call and nothing was ever seen to truncate. The tool protocol
# changed that on both ends: the definitions cost ~600 prompt tokens before a
# word is generated, and a reasoning model needs thousands of OUTPUT tokens
# inside the same window. Measured 2026-09-23: judge_anchored on the 9B wanted
# min_predict 8192 against num_ctx 8192, leaving nothing for the prompt, and
# the server answered HTTP 500.
#
# It is recorded in _eval_meta, so raising it moves the cell and rows taken at
# two ceilings never pool silently.
DEFAULT_NUM_CTX = int(os.environ.get("LATTICE_NUM_CTX", "8192"))

# LATTICE_BACKEND: "ollama" (default) or "llamacpp". Added 2026-09-15 for the
# Nemotron 2x16k llama-server setup -- a llama-server instance shares one
# model load across N parallel slots (confirmed in M0 findings entry 1's
# addendum: 2 concurrent 16384-ctx streams cost the same VRAM as one 32768
# stream), which Ollama's per-process model loading cannot do. Every caller
# of generate()/health() is unchanged; only this module routes differently.
BACKEND = os.environ.get("LATTICE_BACKEND", "ollama")
DEFAULT_BASE_URL = os.environ.get(
    "LATTICE_BASE_URL",
    "http://localhost:8090" if BACKEND == "llamacpp" else "http://localhost:11434")

# LATTICE_THINK: unset sends no `think` key at all, which is the behaviour every
# run before 2026-09-19 had. "0" sends think=false, "1" sends think=true.
#
# It exists because a reasoning model silently produced nothing for thirteen
# arms. Ollama returns reasoning in a separate `thinking` field and leaves
# `response` empty until the model exits the thinking block; the audit and judge
# calls cap generation at 200 and 220 tokens, and Nemotron Nano 9B v2 needs
# 609-2635 (median 1166, one prompt, ten reps) to get out of it. Every one of
# those calls returned "". `/think` and `/no_think` control tokens do not work
# through this path; this parameter does. See 50-findings/12, addendum 2.
_THINK_ENV = os.environ.get("LATTICE_THINK")
THINK = None if _THINK_ENV is None else _THINK_ENV not in ("0", "false", "False", "")

# LATTICE_MIN_PREDICT: a floor under every caller's num_predict. The arms
# hardcode 200 and 220, which is below what some models need for the ANSWER
# alone -- with reasoning off, Nemotron's audit answer costs a median 212 tokens
# and 5 of 8 runs truncate mid-object at 200. A floor raises them without
# editing eight workflow files, and is a no-op for a model that stops earlier.
MIN_PREDICT = int(os.environ.get("LATTICE_MIN_PREDICT", "0"))

# LATTICE_NUDGE: text appended to EVERY prompt this client sends.
#
# It lives here, not in prompt_for, because "the whole pipeline" means every
# model call in an arm -- the implementer, the pre-work audit, and the judge --
# and the M7 judge stages call generate() directly rather than going through
# the role library. Appending at the transport is the only point that catches
# all three.
#
# It is model-visible text, so it is part of the ADAPTER and lands in
# adapter_fingerprint(); a run with a nudge can never pool with one without.
# That is the whole reason the adapter got its own hash: a wording change that
# reaches the model and moves no key is the defect 50-findings/15 closes on.
#
# Empty by default. Nothing that has already run is affected.
NUDGE = os.environ.get("LATTICE_NUDGE", "")


def _nudged(prompt: str) -> str:
    return f"{prompt}\n\n{NUDGE}" if NUDGE else prompt


def _transcript_failure(prompt: str, payload: dict, num_predict: int) -> "Generation":
    """Record a call that is about to raise.

    Truncation is the failure this project keeps mistaking for a capability
    result -- an empty answer from a reasoning model that spent its whole
    budget thinking. The guards below catch it loudly, but they used to raise
    before the transcript sink ran, so the only call worth reading afterwards
    was the only one not written down.

    Built as a Generation so the record has the same shape as every other,
    with `done_reason` and the thinking length carrying the diagnosis.
    """
    g = Generation(
        text="",
        model=payload.get("model", ""),
        prompt_eval_count=payload.get("prompt_eval_count", 0),
        eval_count=payload.get("eval_count", 0),
        total_duration_s=payload.get("total_duration", 0) / 1e9,
        load_duration_s=payload.get("load_duration", 0) / 1e9,
        raw=payload)
    try:
        _transcript(prompt, g)
    except Exception:  # noqa: BLE001
        pass  # a failed record must never mask the error it was recording
    return g

# LATTICE_TEMPERATURE / LATTICE_TOP_P: override what the arms hardcode.
#
# Every call site passes temperature=0.2 and none passes top_p, so the sampling
# regime was fixed at a value nobody chose for any particular model and could
# not be varied without editing eight workflow files.
#
# It is not a free parameter. NVIDIA's guidance for Nemotron Nano is
# temperature 0.6 with top_p 0.95 when reasoning is ON, and temperature 0 with
# greedy decoding when it is OFF. Measured here on one implementer prompt,
# reasoning off, five samples each: temperature 0.0 degenerated 5 times out of
# 5, 0.2 four times, 0.6 twice -- degenerate meaning newlines collapsed to
# spaces and the generation running to its cap. That is the opposite direction
# from the published recommendation and rests on one prompt, so it is a reason
# to make the parameter settable rather than a reason to trust a value.
#
# Unset leaves each call site's own argument untouched, so nothing already
# recorded changes meaning.
_TEMP_ENV = os.environ.get("LATTICE_TEMPERATURE")
TEMPERATURE = None if _TEMP_ENV is None else float(_TEMP_ENV)
_TOPP_ENV = os.environ.get("LATTICE_TOP_P")
TOP_P = None if _TOPP_ENV is None else float(_TOPP_ENV)


class OllamaError(RuntimeError):
    pass


class Truncated(OllamaError):
    """A generation that hit the cap without producing an answer.

    A SUBCLASS on purpose, and the reason matters. This condition used to be
    returned silently: thirteen arms recorded `parsed: False, error: None` for
    it and it was read as a model that judges badly -- 90 of judge_bypass's 102
    rows were this, scored as results. Raising was the fix, and "never silent
    again" is not up for renegotiation.

    But raising a bare OllamaError also makes the condition UNRECOVERABLE. It
    crosses the module boundary, `_run_tools` does not catch it, and it lands in
    run_task as `run_ok: false` -- so the processor never gets to diagnose the
    one failure recovery exists for, and the 25,141 characters of thinking that
    say WHY exist only in the transcript on disk, not in anything the caller
    holds.

    Subclassing gives both. Every existing `except OllamaError` still catches
    it, unchanged, so nothing can silently succeed. And a caller that wants to
    recover catches `Truncated` and gets the whole generation to diagnose from.

    `gen` carries the full payload: the thinking text, done_reason, the token
    counts. That is what recovery.diagnose() reads.
    """

    def __init__(self, message: str, gen: "Generation", num_predict: int):
        super().__init__(message)
        self.gen = gen
        self.num_predict = num_predict


@dataclass
class Generation:
    text: str
    model: str
    prompt_eval_count: int
    eval_count: int
    total_duration_s: float
    load_duration_s: float
    raw: dict[str, Any] = field(repr=False, default_factory=dict)
    # Populated only on the /api/chat path. Ollama's PARSER lifts these OUT of
    # the response text, so `text` is what is left over once they are removed --
    # usually empty. Each entry is {"name": str, "arguments": dict}.
    tool_calls: list[dict[str, Any]] = field(repr=False, default_factory=list)

    @property
    def tokens_per_s(self) -> float:
        # Ollama: eval_duration is nanoseconds. llama-server: timings.predicted_ms
        # is milliseconds. Different units, same meaning (generation-phase time).
        if "timings" in self.raw:
            d = self.raw.get("timings", {}).get("predicted_ms", 0) / 1000
        else:
            d = self.raw.get("eval_duration", 0) / 1e9
        return (self.eval_count / d) if d else 0.0


# ---------------------------------------------------------------- the meter
#
# Every generation's token counts, accumulated per process. Rows carried
# `wall_s` and nothing about what was generated inside it, so a slow rep and a
# long rep were the same number and neither could be compared across hosts,
# models or degrees of concurrency. Two separate quantities, and keeping them
# apart is the whole point:
#
#   gen_s   generation-phase seconds the BACKEND reports -- decode time only
#   wall_s  the rep's own clock -- decode plus prompt, plus scoring, plus
#           fixture setup, plus every gap
#
# tokens/gen_s is what the card does while it is decoding, and two workers
# sharing one GPU push it DOWN. tokens/wall_s is throughput, and two workers
# push it UP exactly insofar as one's gaps cover the other's decoding. Reporting
# one as the other is how a real speedup gets mistaken for a regression.
#   prompt_s  prompt-evaluation seconds the backend reports -- reading the
#             input before a single token comes out. Separate from gen_s
#             because they scale with different things and can differ by an
#             order of magnitude between models at the SAME prompt size:
#             nemotron showed 19 s per call outside decode against qwen's 3 s
#             on 1,170-token prompts, and without this field there was no way
#             to tell prompt evaluation from queueing.
# tool_turns / tool_native / tool_recovered exist because Ollama's PARSER is
# not uniformly reliable and its failure is indistinguishable from the model
# refusing to call a tool. qwen2.5-coder emits a well-formed call and Ollama
# hands it back as plain content with tool_calls empty; the call is recovered
# from the text here. Without a per-row count, a cross-model comparison over
# this protocol would silently score an Ollama template gap as a model
# property -- the exact confusion 50-findings/15 is about.
_TOOL_KEYS = {"tool_turns": 0, "tool_native": 0, "tool_recovered": 0,
              "tool_malformed": 0, "tool_repaired": 0}
_METER = {"calls": 0, "gen_tok": 0, "prompt_tok": 0, "gen_s": 0.0,
          "prompt_s": 0.0, **_TOOL_KEYS}


def meter_reset() -> None:
    _METER.update(calls=0, gen_tok=0, prompt_tok=0, gen_s=0.0, prompt_s=0.0,
                  **_TOOL_KEYS)


def meter_read() -> dict:
    return dict(_METER)


def _transcript_dir() -> Path | None:
    """Where raw generations go. ON by default, and that default is the point.

    Nothing in this project stored what a model actually said. Stage records
    keep parsed fields only, store rows keep scores and timings, and the M2
    event log records effects by reference -- so a generation was discarded the
    moment it was parsed, and when parsing FAILED all of those came back empty
    and nothing survived at all.

    That breaks the store's whole premise. A result gathered for one experiment
    is supposed to be reusable by another, but a row can only answer questions
    whose answers were parsed out when it was written. Every NEW question about
    an old run then needs a re-run, which is the cost the store exists to avoid.
    This session hit it directly: nemotron's judge produced no JSON in 18% of
    calls under one format and 2% under another, 1,513 reps were on disk, and
    the cause was not recoverable from any of them.

    The trade is not close, and gzip makes it absurd. Filing by cell groups
    same-task, same-arm generations into one file, so the ~2.3 KB judge prompt
    repeats identically down the whole stream: measured at 51x on a realistic
    cell, which puts a sweep of E8's shape at 68 MiB raw and about 1 MiB on
    disk, against thirty to forty hours of GPU. Keeping them is the default.

    (That ratio assumes the prompt template dominates, which it does here --
    only the diff varies between reps of a task. A workload with genuinely
    distinct prompts per call would compress far less.)

        LATTICE_TRANSCRIPT=<dir>   write somewhere else
        LATTICE_TRANSCRIPT=0       off, for a throwaway run

    ONE FILE PER REP, never shared: `<cell>/<rep>.jsonl.gz`. The first version
    appended every rep of a cell into one archive, so a worker killed mid-write
    truncated a file holding OTHER reps' records -- and this project kills
    workers routinely, since the pool's lease exists for exactly that. A reader
    that tolerates the damage is the wrong fix; not sharing the file is the
    right one. A dead attempt now damages only its own rep, which the pool
    releases and re-runs anyway, and the retry truncates the file rather than
    appending to the corpse.

    Compaction into a single per-cell archive is a separate offline step
    (`transcripts.py --compact`), run when nothing is writing. That is also
    where the compression lands: 51x measured, because a cell's reps share the
    same prompt template.
    """
    v = os.environ.get("LATTICE_TRANSCRIPT")
    if v in ("0", "off", "false", "no"):
        return None
    if v:
        return Path(v)
    return Path(__file__).resolve().parents[2] / "evalkit_store" / "transcripts"


_TSINK = None
_TSINK_KEY = None


def _transcript(prompt: str, g: "Generation") -> None:
    global _TSINK, _TSINK_KEY
    d = _transcript_dir()
    if d is None:
        return
    try:
        cell = os.environ.get("LATTICE_CELL") or "uncelled"
        rep = os.environ.get("LATTICE_REP") or os.environ.get("M6_REP") or "0"
        key = (cell, rep)
        if _TSINK_KEY != key:
            if _TSINK is not None:
                _TSINK.close()
            (d / cell).mkdir(parents=True, exist_ok=True)
            # "wt", not "at": a retry of this rep overwrites whatever a killed
            # attempt left behind, rather than appending to a partial member.
            _TSINK = gzip.open(d / cell / f"{rep}.jsonl.gz", "wt",
                               encoding="utf-8", compresslevel=6)
            _TSINK_KEY = key
        _TSINK.write(json.dumps({
            "t": time.time(),
            "cell": cell,
            "rep": rep,
            "task": os.environ.get("M6_TASK"),
            "runner": f"{socket.gethostname()}-{os.getpid()}",
            "model": g.model,
            "judge_format": os.environ.get("LATTICE_JUDGE_FORMAT"),
            "prompt_sha": hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16],
            "prompt": prompt,
            "prompt_tok": g.prompt_eval_count,
            "eval_count": g.eval_count,
            "done_reason": g.raw.get("done_reason"),
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "text": g.text,
            # On /api/chat the answer is NOT in `text`. Ollama's parser lifts
            # the calls out into a structured field and leaves content empty,
            # and `thinking` moves inside `message`. Recording only `text`
            # there stored nothing at all: measured 2026-09-23, a 4B rep
            # generated 1234 tokens and the transcript captured zero characters
            # of them. That is precisely the loss this sink exists to prevent,
            # reintroduced by the change of endpoint.
            "thinking": (g.raw.get("thinking")
                         or (g.raw.get("message") or {}).get("thinking") or ""),
            "tool_calls": g.tool_calls,
        }) + "\n")
        _TSINK.flush()
    except Exception:  # noqa: BLE001
        pass          # observability must never break the run it observes


def transcript_close() -> None:
    """Finish the current rep's file. Called when a rep's row is committed."""
    global _TSINK, _TSINK_KEY
    if _TSINK is not None:
        try:
            _TSINK.close()
        except Exception:  # noqa: BLE001
            pass
    _TSINK, _TSINK_KEY = None, None


def _meter(g: "Generation", prompt: str = "") -> "Generation":
    if "timings" in g.raw:                       # llama-server: milliseconds
        t = g.raw.get("timings", {})
        d, pd = t.get("predicted_ms", 0) / 1000, t.get("prompt_ms", 0) / 1000
    else:                                        # Ollama: nanoseconds
        d = g.raw.get("eval_duration", 0) / 1e9
        pd = g.raw.get("prompt_eval_duration", 0) / 1e9
    _METER["calls"] += 1
    _METER["gen_tok"] += g.eval_count
    _METER["prompt_tok"] += g.prompt_eval_count
    _METER["gen_s"] += d
    _METER["prompt_s"] += pd
    _transcript(prompt, g)
    return g


def generate(prompt: str, *, model: str = DEFAULT_MODEL, base_url: str = DEFAULT_BASE_URL,
             num_ctx: int = DEFAULT_NUM_CTX, temperature: float = 0.2,
             num_predict: int = 1536, timeout_s: float = 600.0,
             system: str | None = None,
             tools: list[dict[str, Any]] | None = None) -> Generation:
    """`tools` switches to /api/chat, the only endpoint that accepts them.

    /api/generate has no tools parameter -- it is the raw completion endpoint.
    On the chat path Ollama's RENDERER serialises the definitions into the
    prompt in the model's own tuned dialect, and its PARSER extracts any calls
    back out into a structured field. Neither runs on /api/generate.
    """
    prompt = _nudged(prompt)
    if tools:
        if BACKEND == "llamacpp":
            raise OllamaError("tools= requires the ollama backend (/api/chat); "
                              "llama-server's /completion has no tool channel")
        msgs = ([{"role": "system", "content": system}] if system else [])
        msgs.append({"role": "user", "content": prompt})
        return chat(msgs, base_url=base_url, model=model, num_ctx=num_ctx,
                    temperature=temperature, num_predict=num_predict,
                    timeout_s=timeout_s, tools=tools)
    if BACKEND == "llamacpp":
        return _generate_llamacpp(prompt, base_url=base_url, model=model,
                                  temperature=temperature, num_predict=num_predict,
                                  timeout_s=timeout_s, system=system)
    num_predict = max(num_predict, MIN_PREDICT)
    if TEMPERATURE is not None:
        temperature = TEMPERATURE
    opts = {"temperature": temperature, "num_ctx": num_ctx,
            "num_predict": num_predict}
    if TOP_P is not None:
        opts["top_p"] = TOP_P
    body = {"model": model, "prompt": prompt, "stream": False, "options": opts}
    if THINK is not None:
        body["think"] = THINK
    if system:
        body["system"] = system
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(f"{base_url}/api/generate", data=data,
                                 headers={"Content-Type": "application/json"})
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        # Read the body. Ollama puts the actual reason in it, and without this
        # every server-side refusal arrived as a bare "HTTP Error 500", which
        # says nothing about whether the fault is the prompt, the options or
        # the message list.
        try:
            detail = e.read().decode("utf-8", "replace")[:500]
        except Exception:  # noqa: BLE001
            detail = "(body unreadable)"
        raise OllamaError(f"request to {base_url} failed: HTTP {e.code}: {detail}") from e
    except urllib.error.URLError as e:
        raise OllamaError(f"request to {base_url} failed: {e}") from e
    except json.JSONDecodeError as e:
        raise OllamaError(f"bad JSON from Ollama: {e}") from e
    if "response" not in payload:
        raise OllamaError(f"no 'response' field in Ollama reply: {payload!r}")
    # The key is present and empty. This is what thirteen arms recorded as
    # `parsed: False, error: None` and what was read as a model that judges
    # badly: a reasoning model spent the whole budget in its `thinking` channel
    # and never reached an answer. It must never be silent again -- an empty
    # response with done_reason "length" is truncation before any output.
    if not payload["response"] and payload.get("done_reason") == "length":
        # Transcribe BEFORE raising. The guard used to raise straight out of
        # here, so the one call that failed was the one call never recorded --
        # the most diagnostic event in a run, discarded on the way past. A
        # truncation is a result about the model, not an absence of one.
        _g = _transcript_failure(prompt, payload, num_predict)
        raise Truncated(
            f"empty response, truncated at num_predict={num_predict} "
            f"(done_reason=length, {len(payload.get('thinking') or '')} chars of "
            f"thinking, eval_count={payload.get('eval_count')}). The model did not "
            f"reach an answer. Raise num_predict, or set LATTICE_THINK=0.",
            _g, num_predict)
    return _meter(Generation(
        text=payload["response"],
        model=payload.get("model", model),
        prompt_eval_count=payload.get("prompt_eval_count", 0),
        eval_count=payload.get("eval_count", 0),
        total_duration_s=payload.get("total_duration", 0) / 1e9 or (time.monotonic() - t0),
        load_duration_s=payload.get("load_duration", 0) / 1e9,
        raw=payload,
    ), prompt)


SP, TAB, NL = '\\s', '\\t', '\\n'
"""Regex escape sequences as literals, so building a pattern by
concatenation does not need a backslash inside an f-string."""

_TEXT_CALL = re.compile(
    r'\{\s*"name"\s*:\s*"(?P<name>[A-Za-z_][A-Za-z0-9_]*)"\s*,'
    r'\s*"(?:arguments|parameters)"\s*:\s*(?P<args>\{)', re.S)


_CLOSERS = set(",:}]")


def _repair_json(raw: str) -> str:
    """Re-escape what a model left unescaped inside a JSON string.

    Why this exists rather than rejecting the payload. qwen2.5-coder escapes
    newlines correctly and does NOT escape quotes, so any Python file
    containing a docstring breaks its own tool call:

        "content": "def call(self):\\n        \"\"\"Invoke fn() ...
                                    ^^^^^^ raw quotes, invalid JSON

    Measured here 2026-09-23, and documented upstream as a Qwen family trait
    rather than a local fault -- cline#10843 reports the same model on Ollama
    looping on raw JSON, and llama.cpp#19382 and the Qwen3-Coder-Next thread
    both report invalid tool JSON specifically when writing a file. Qwen's own
    function-calling guide says the protocol is "not guaranteed" to be followed
    and tells integrators to parse it themselves with "countermeasures or
    rectifications in place". A published vLLM tool parser exists for this
    model for the same reason. Repair is the normal integration layer here, not
    a crutch invented for this harness.

    The rule: inside a string, a quote CLOSES it only if the next non-space
    character is one of , : } ] or the end of input. Otherwise it is content
    and gets escaped. Raw control characters, also illegal in JSON strings, are
    escaped the same way.

    THIS CAN BE WRONG. Content that legitimately holds `"}` or `",` -- say
    `print("}")` -- terminates the string early and the repair produces the
    wrong file rather than no file. That is a worse failure than rejection
    because it is silent, so every repair is counted in `tool_repaired` and the
    result is only accepted if it parses. A rate that stops being small is the
    signal to stop trusting this.
    """
    out, i, n, instr = [], 0, len(raw), False
    while i < n:
        ch = raw[i]
        if not instr:
            out.append(ch)
            if ch == '"':
                instr = True
            i += 1
            continue
        if ch == chr(92) and i + 1 < n:          # keep valid escapes intact
            out.append(raw[i:i + 2])
            i += 2
            continue
        if ch == '"':
            j = i + 1
            while j < n and raw[j] in " \t\r\n":
                j += 1
            if j >= n or raw[j] in _CLOSERS:
                out.append(ch)                   # a real terminator
                instr = False
            else:
                out.append(chr(92) + '"')        # content, escape it
            i += 1
            continue
        if ch in "\n\r\t":
            out.append({"\n": chr(92) + "n", "\r": chr(92) + "r",
                        "\t": chr(92) + "t"}[ch])
            i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def _loads_or_repair(raw: str) -> dict | None:
    """json.loads, then one repair attempt. None if both fail."""
    try:
        v = json.loads(raw)
        return v if isinstance(v, dict) else None
    except json.JSONDecodeError:
        pass
    try:
        v = json.loads(_repair_json(raw))
    except json.JSONDecodeError:
        _METER["tool_malformed"] += 1
        return None
    if not isinstance(v, dict):
        _METER["tool_malformed"] += 1
        return None
    _METER["tool_repaired"] += 1
    return v


def _calls_from_text(text: str) -> list[dict[str, Any]]:
    """Tool calls Ollama's PARSER did not lift out of the text.

    Not a nicety. qwen2.5-coder emits a perfectly well-formed
    {"name": ..., "arguments": {...}} and Ollama hands it back as plain
    `content` with `tool_calls` empty -- the model complied and the server-side
    extraction did not fire. Discarding that would score a parser gap as a
    model failure, which is the exact confusion Findings 15 is about.

    Brace-matched rather than regex-captured, because file content routinely
    contains braces.
    """
    out = []
    for m in _TEXT_CALL.finditer(text):
        i, depth, esc, instr = m.start("args"), 0, False, False
        for j in range(i, len(text)):
            ch = text[j]
            if instr:
                if esc:
                    esc = False
                elif ch == chr(92):
                    esc = True
                elif ch == '"':
                    instr = False
                continue
            if ch == '"':
                instr = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    args = _loads_or_repair(text[i:j + 1])
                    if args is None:
                        break
                    out.append({"name": m.group("name"), "arguments": args})
                    break
    return out


def _calls_from_xml(text: str, names: list[str]) -> list[dict[str, Any]]:
    """Recover a tool call written in Ollama's format but missing its wrapper.

    THE FORMAT IS NOT GUESSED. Read out of ollama/model/renderers/nemotron3nano.go
    and ollama/model/parsers/qwen3coder.go -- the nemotron3nano parser delegates
    to Qwen3CoderParser, so an NVIDIA model is told to emit Qwen3-Coder syntax
    and parsed by Qwen3-Coder's parser:

        <tool_call>
        <function=NAME>
        <parameter=KEY>
        value
        </parameter>
        </function>
        </tool_call>

    `toolOpenTag = "<tool_call>"` is REQUIRED. Without it the parser is in
    LookingForToolStart and the whole thing is content. Values have exactly one
    leading and one trailing newline trimmed (strings.TrimPrefix / TrimSuffix),
    which this mirrors -- trimming all whitespace would corrupt any parameter
    whose value is deliberately indented.

    WHAT THIS RECOVERS is the near miss actually observed: nemotron3-nano-4b
    emits the correct inner <function=...> block and omits the <tool_call>
    wrapper, on 11 of 34 monolith runs, always on the final `conclude` after
    having made a natively-parsed write_file call in the same sequence. The
    earlier version of this function matched `<NAME>` and `NAME` + newline + `<parameter=`,
    shapes inferred from reading output rather than from the spec, and so missed
    the one form the model actually produces.
    """
    out: list[dict[str, Any]] = []
    allowed = {n for n in names if n}
    # With or without the wrapper: the wrapper is what the parser requires and
    # its absence is exactly the failure being recovered.
    for m in re.finditer(r"<function=([A-Za-z_][A-Za-z0-9_]*)\s*>(.*?)"
                         r"(?=</function>|<function=|\Z)", text, re.S):
        name = m.group(1)
        if allowed and name not in allowed:
            continue
        args: dict[str, Any] = {}
        for pm in re.finditer(r"<parameter=([A-Za-z_][A-Za-z0-9_]*)\s*>"
                              r"(.*?)(?=</parameter>|<parameter=|</function>|\Z)",
                              m.group(2), re.S):
            raw = pm.group(2)
            if raw.startswith("\n"):
                raw = raw[1:]
            if raw.endswith("\n"):
                raw = raw[:-1]
            args[pm.group(1)] = raw
        if args:
            out.append({"name": name, "arguments": args})
    return out


def _calls_from_bare_args(text: str, tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Recover a call emitted as its ARGUMENTS OBJECT ALONE, with no envelope.

    The commonest failure in the 2026-09-24 sweep: 9 of 34 monolith runs ended
    by emitting

        {"terminal_state": "answered", "summary": "...", "verdict": "approve",
         "run": [], "context_requests": []}

    every field name correct, every optional field filled, and no indication
    that it is a call at all -- no <tool_call>, no <function=>, no "name".
    Ollama's parser is in LookingForToolStart and treats it as content, so the
    work already written by earlier native write_file calls is discarded.

    IDENTIFIED BY SCHEMA, not by hardcoding a tool name. An object is read as a
    call when it carries every REQUIRED parameter of exactly one offered tool
    and no key outside that tool's properties. That makes it unambiguous by
    construction: two tools with disjoint required sets cannot both match, and
    an object that matches none is left alone. `conclude` qualifies because
    `terminal_state` and `summary` belong to nothing else in the protocol.

    Deliberately NOT a fallback for write_file: its required `content` is
    free-form file text, so a file that happens to contain a JSON object could
    match. Tools whose parameters are open-ended are skipped.
    """
    out: list[dict[str, Any]] = []
    specs = []
    for t in tools or []:
        fn = (t or {}).get("function") or {}
        params = fn.get("parameters") or {}
        props = set((params.get("properties") or {}).keys())
        req = set(params.get("required") or [])
        # Only tools whose required set is fully enumerated and small enough to
        # be distinctive. write_file's `content` is arbitrary text, so a file
        # body could impersonate it; such tools are excluded.
        if req and props and "content" not in req:
            specs.append((fn.get("name", ""), props, req))
    if not specs:
        return out
    for m in re.finditer(r"\{", text):
        i, depth, esc, instr = m.start(), 0, False, False
        for j in range(i, len(text)):
            ch = text[j]
            if instr:
                if esc:
                    esc = False
                elif ch == chr(92):
                    esc = True
                elif ch == '"':
                    instr = False
                continue
            if ch == '"':
                instr = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    obj = _loads_or_repair(text[i:j + 1])
                    if isinstance(obj, dict) and "name" not in obj:
                        keys = set(obj)
                        hit = [n for n, props, req in specs
                               if req <= keys <= props]
                        if len(hit) == 1:
                            out.append({"name": hit[0], "arguments": obj})
                    break
        if out:
            break
    return out


def chat(messages: list[dict[str, Any]], *, model: str = DEFAULT_MODEL,
         base_url: str = DEFAULT_BASE_URL, num_ctx: int = DEFAULT_NUM_CTX,
         temperature: float = 0.2, num_predict: int = 1536,
         timeout_s: float = 600.0,
         tools: list[dict[str, Any]] | None = None) -> Generation:
    """/api/chat over a full message list, so a tool loop can carry history.

    A loop is not optional on this endpoint. Measured 2026-09-23 on
    nemotron3-nano-4b: turn one returns write_file and stops, and conclude only
    arrives on turn two, after a tool result has been appended. Asking for both
    in one shot gets one. That is how the format was tuned -- a call is a turn
    boundary -- and it is the substantive difference from the marker protocol,
    which was single-shot by construction.

    Same options and timing fields as /api/generate, so the meter and the
    transcript need no special case.
    """
    num_predict = max(num_predict, MIN_PREDICT)
    if TEMPERATURE is not None:
        temperature = TEMPERATURE
    opts = {"temperature": temperature, "num_ctx": num_ctx,
            "num_predict": num_predict}
    if TOP_P is not None:
        opts["top_p"] = TOP_P
    # The nudge attaches to the FIRST user turn and only there. chat() is
    # re-entered once per turn of the tool loop with a growing history, so
    # appending per call would stack one copy per turn; and appending to a
    # tool-result turn would make the runtime nag, which is what the "then call
    # conclude" line did before it was removed.
    if NUDGE and messages:
        messages = list(messages)
        for i, m in enumerate(messages):
            if m.get("role") == "user":
                if not (m.get("content") or "").endswith(NUDGE):
                    messages[i] = {**m, "content": _nudged(m.get("content", ""))}
                break
    body = {"model": model, "messages": messages, "stream": False,
            "options": opts}
    if tools:
        body["tools"] = tools
    if THINK is not None:
        body["think"] = THINK
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(f"{base_url}/api/chat", data=data,
                                 headers={"Content-Type": "application/json"})
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        # Read the body. Ollama puts the actual reason in it, and without this
        # every server-side refusal arrived as a bare "HTTP Error 500", which
        # says nothing about whether the fault is the prompt, the options or
        # the message list.
        try:
            detail = e.read().decode("utf-8", "replace")[:500]
        except Exception:  # noqa: BLE001
            detail = "(body unreadable)"
        raise OllamaError(f"request to {base_url} failed: HTTP {e.code}: {detail}") from e
    except urllib.error.URLError as e:
        raise OllamaError(f"request to {base_url} failed: {e}") from e
    except json.JSONDecodeError as e:
        raise OllamaError(f"bad JSON from Ollama: {e}") from e
    msg = payload.get("message")
    if not isinstance(msg, dict):
        raise OllamaError(f"no 'message' field in Ollama reply: {payload!r}")
    calls = []
    for c in msg.get("tool_calls") or []:
        fn = (c or {}).get("function") or {}
        args = fn.get("arguments")
        if isinstance(args, str):          # some renderers hand back a string
            try:
                args = json.loads(args)
            except json.JSONDecodeError:
                args = {"_raw": args}
        calls.append({"name": fn.get("name", ""),
                      "arguments": args if isinstance(args, dict) else {}})
    text = msg.get("content") or ""
    _METER["tool_turns"] += 1
    _METER["tool_native"] += len(calls)
    # Recovery runs even when SOME calls parsed natively. The 9B returns
    # write_file structured and conclude as XML in the same turn, so "any
    # native call" is not evidence the turn was fully understood.
    if text:
        seen = {c["name"] for c in calls}
        names = [((t.get("function") or {}).get("name") or "")
                 for t in (tools or [])]
        extra = [c for c in (_calls_from_text(text)
                             + _calls_from_xml(text, [n for n in names if n])
                             + _calls_from_bare_args(text, tools or []))
                 if c["name"] not in seen]
        if extra:
            _METER["tool_recovered"] += len(extra)
            calls = calls + extra
    # Same failure as on /api/generate: a reasoning model that spends the whole
    # budget thinking and reaches no answer. With tools it is worse, because an
    # empty content field is ALSO the normal shape of a pure tool-call reply --
    # so silence only counts as truncation when no call came back either.
    if not text and not calls and payload.get("done_reason") == "length":
        _g = _transcript_failure(
            messages[-1].get("content", "") if messages else "",
            payload, num_predict)
        raise Truncated(
            f"empty response and no tool calls, truncated at "
            f"num_predict={num_predict} (done_reason=length, "
            f"{len(msg.get('thinking') or '')} chars of thinking, "
            f"eval_count={payload.get('eval_count')}). Raise num_predict, "
            f"or set LATTICE_THINK=0.",
            _g, num_predict)
    return _meter(Generation(
        text=text,
        model=payload.get("model", model),
        prompt_eval_count=payload.get("prompt_eval_count", 0),
        eval_count=payload.get("eval_count", 0),
        total_duration_s=payload.get("total_duration", 0) / 1e9 or (time.monotonic() - t0),
        load_duration_s=payload.get("load_duration", 0) / 1e9,
        raw=payload,
        tool_calls=calls,
    ), messages[-1].get("content", "") if messages else "")


def _generate_llamacpp(prompt: str, *, base_url: str, model: str, temperature: float,
                       num_predict: int, timeout_s: float, system: str | None) -> Generation:
    """llama-server's native /completion endpoint (not the OpenAI-compat one --
    this is the same endpoint and response shape validated manually against
    the 2x16k/2x32k concurrent-slot runs in M0 findings entry 1's addendum).
    `num_ctx` is deliberately not a parameter here: llama-server reserves each
    slot's context size at server STARTUP (`--kv-unified-per-slot`), not per
    request -- passing a per-call ctx would be a silent no-op that misleads a
    caller into thinking it did something.
    """
    full_prompt = f"{system}\n\n{prompt}" if system else prompt
    body = {"prompt": full_prompt, "n_predict": num_predict,
            "temperature": TEMPERATURE if TEMPERATURE is not None else temperature}
    if TOP_P is not None:
        body["top_p"] = TOP_P
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(f"{base_url}/completion", data=data,
                                 headers={"Content-Type": "application/json"})
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        # Read the body. Ollama puts the actual reason in it, and without this
        # every server-side refusal arrived as a bare "HTTP Error 500", which
        # says nothing about whether the fault is the prompt, the options or
        # the message list.
        try:
            detail = e.read().decode("utf-8", "replace")[:500]
        except Exception:  # noqa: BLE001
            detail = "(body unreadable)"
        raise OllamaError(f"request to {base_url} failed: HTTP {e.code}: {detail}") from e
    except urllib.error.URLError as e:
        raise OllamaError(f"request to {base_url} failed: {e}") from e
    except json.JSONDecodeError as e:
        raise OllamaError(f"bad JSON from llama-server: {e}") from e
    if "error" in payload:
        raise OllamaError(f"llama-server error: {payload['error']!r}")
    if "content" not in payload:
        raise OllamaError(f"no 'content' field in llama-server reply: {payload!r}")
    t = payload.get("timings", {})
    return _meter(Generation(
        text=payload["content"],
        model=payload.get("model", model),
        prompt_eval_count=int(t.get("prompt_n", 0)),
        eval_count=int(t.get("predicted_n", 0)),
        total_duration_s=(t.get("prompt_ms", 0) + t.get("predicted_ms", 0)) / 1000
                         or (time.monotonic() - t0),
        load_duration_s=0.0,   # llama-server loads once at startup, not per-request
        raw=payload,
    ), prompt)


def health(base_url: str = DEFAULT_BASE_URL, timeout_s: float = 5.0) -> bool:
    if BACKEND == "llamacpp":
        try:
            with urllib.request.urlopen(f"{base_url}/health", timeout=timeout_s) as resp:
                return resp.status == 200
        except urllib.error.URLError:
            return False
    try:
        with urllib.request.urlopen(f"{base_url}/api/tags", timeout=timeout_s) as resp:
            return resp.status == 200
    except urllib.error.URLError:
        return False
