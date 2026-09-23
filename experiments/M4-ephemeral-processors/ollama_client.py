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
DEFAULT_NUM_CTX = 8192

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
_METER = {"calls": 0, "gen_tok": 0, "prompt_tok": 0, "gen_s": 0.0, "prompt_s": 0.0}


def meter_reset() -> None:
    _METER.update(calls=0, gen_tok=0, prompt_tok=0, gen_s=0.0, prompt_s=0.0)


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
            "thinking": g.raw.get("thinking") or "",
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
        raise OllamaError(
            f"empty response, truncated at num_predict={num_predict} "
            f"(done_reason=length, {len(payload.get('thinking') or '')} chars of "
            f"thinking, eval_count={payload.get('eval_count')}). The model did not "
            f"reach an answer. Raise num_predict, or set LATTICE_THINK=0.")
    return _meter(Generation(
        text=payload["response"],
        model=payload.get("model", model),
        prompt_eval_count=payload.get("prompt_eval_count", 0),
        eval_count=payload.get("eval_count", 0),
        total_duration_s=payload.get("total_duration", 0) / 1e9 or (time.monotonic() - t0),
        load_duration_s=payload.get("load_duration", 0) / 1e9,
        raw=payload,
    ), prompt)


_TEXT_CALL = re.compile(
    r'\{\s*"name"\s*:\s*"(?P<name>[A-Za-z_][A-Za-z0-9_]*)"\s*,'
    r'\s*"(?:arguments|parameters)"\s*:\s*(?P<args>\{)', re.S)


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
                    try:
                        args = json.loads(text[i:j + 1])
                    except json.JSONDecodeError:
                        break
                    if isinstance(args, dict):
                        out.append({"name": m.group("name"), "arguments": args})
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
    if not calls and text:
        calls = _calls_from_text(text)
    # Same failure as on /api/generate: a reasoning model that spends the whole
    # budget thinking and reaches no answer. With tools it is worse, because an
    # empty content field is ALSO the normal shape of a pure tool-call reply --
    # so silence only counts as truncation when no call came back either.
    if not text and not calls and payload.get("done_reason") == "length":
        raise OllamaError(
            f"empty response and no tool calls, truncated at "
            f"num_predict={num_predict} (done_reason=length, "
            f"{len(msg.get('thinking') or '')} chars of thinking, "
            f"eval_count={payload.get('eval_count')}). Raise num_predict, "
            f"or set LATTICE_THINK=0.")
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
