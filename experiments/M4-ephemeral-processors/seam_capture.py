"""Request and parse equivalence for the transport seam, with no server (A1a).

    python seam_capture.py                  # compare every case to its golden
    python seam_capture.py --write          # (re)write the goldens -- see below
    python seam_capture.py --cassette DIR   # add cases from recorded transcripts
    python seam_capture.py --only chat_tools
    python seam_capture.py --client-dir <other checkout>/experiments/M4-ephemeral-processors

THE RISK A1 CARRIES is not that generation changes. It is that the outgoing
REQUEST changes: a different body is a different prompt, and a different
prompt is two populations pooled under one key. That is testable without a
model, so it is tested here, byte for byte.

HOW. `urllib.request.urlopen` is replaced at the last moment before bytes
leave the process. The replacement records exactly what WOULD have been sent
-- URL, method, headers, timeout, and the body as raw bytes -- and answers with
a fixed payload, so the response side runs through the real parse path too.
Every case runs in its own interpreter, because THINK, NUDGE, TEMPERATURE,
TOP_P, MIN_PREDICT and BACKEND are read from the environment at import.

GOLDENS live in seam_golden/<case>/:

    request.meta.json   url, method, headers, timeout (sorted JSON)
    request.body        the body, verbatim bytes
    result.json         what the caller got back: the Generation's fields and
                        the meter's movement, or the exception raised

The comparison is BYTE-IDENTICAL, not equivalent. If a refactor changes key
order, the fix is in the serialization, never a re-baselined golden. `--write`
exists to create the goldens once, from the code BEFORE a change; running it
after a change to make a failing comparison pass defeats the file.

WHAT THE RESPONSE FIXTURES ARE. Two kinds, kept apart:
  * server behaviour stated, not model output invented -- an HTTP 500 with a
    body, a refused connection, a reply that is not JSON, a reply missing its
    field. These test the error mapping a transport change could break.
  * real generations only. The one in this clone is
    evalkit_store/probe_prompts/runaway_thinking.txt, the thinking of a genuine
    truncation. Malformed tool calls, bare-args conclusions, XML near-misses
    and repaired JSON must come from recorded transcripts via --cassette:
    nobody invents those correctly, and they are the cases that matter.
"""
from __future__ import annotations

import argparse
import base64
import difflib
import gzip
import io
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GOLDEN = HERE / "seam_golden"
RUNAWAY = ROOT / "evalkit_store" / "probe_prompts" / "runaway_thinking.txt"
FIXTURES = ROOT / "evalkit_store" / "parse_fixtures" / "ollama_responses.json"
RECOVERY_FNS = ("_calls_from_text", "_calls_from_xml", "_calls_from_bare_args",
                "_repair_json")

# Model-shaped text for the REQUEST side only: what we send, not what a model
# said. Quotes, backslashes, newlines, tabs and non-ASCII, because those are
# where two serializers disagree.
PROMPT = ('Fix client.py so every subtest passes.\n\n----- client.py -----\n'
          'def call(self, fn):\n\t"""Invoke fn() once."""\n    return fn()  # é ✓\n'
          'path = "C:\\\\tmp\\\\x"\n')
SYSTEM = "You are an implementer. Reply with tool calls only."

OK_GENERATE = {"model": "m", "response": "ok", "done": True, "done_reason": "stop",
               "prompt_eval_count": 11, "eval_count": 2, "eval_duration": 2000000,
               "prompt_eval_duration": 1000000, "total_duration": 5000000,
               "load_duration": 0}
OK_CHAT = {"model": "m", "message": {"role": "assistant", "content": "ok"},
           "done": True, "done_reason": "stop", "prompt_eval_count": 11,
           "eval_count": 2, "eval_duration": 2000000,
           "prompt_eval_duration": 1000000, "total_duration": 5000000,
           "load_duration": 0}
OK_LLAMACPP = {"content": "ok", "model": "m", "stopped_limit": False,
               "timings": {"prompt_n": 11, "predicted_n": 2, "prompt_ms": 1.0,
                           "predicted_ms": 2.0}}


def _history():
    """A tool loop mid-flight: user turn, assistant call, tool result."""
    return [
        {"role": "user", "content": PROMPT},
        {"role": "assistant", "content": "",
         "tool_calls": [{"function": {"name": "write_file", "arguments": {
             "path": "client.py", "content": 'def call(self, fn):\n    return fn()\n'}}}]},
        {"role": "tool", "tool_name": "write_file",
         "content": json.dumps({"status": "accepted", "path": "client.py",
                                "bytes": 36, "lines": 3,
                                "files_so_far": ["client.py"]})},
    ]


# name -> (env, call, reply). `call` is evaluated in the child against the
# module `oc` and roles.TOOLS; `reply` is what the fake server answers:
#   a dict (JSON body) | ("http", code, body) | ("url",) | ("raw", bytes)
CASES: dict[str, tuple[dict, str, object]] = {
    # ---- the four shapes that matter
    "generate_plain":      ({}, "oc.generate(PROMPT)", OK_GENERATE),
    "chat_tools":          ({}, "oc.chat([{'role': 'user', 'content': PROMPT}], tools=TOOLS)",
                            OK_CHAT),
    "chat_tool_result":    ({}, "oc.chat(_history(), tools=TOOLS)", OK_CHAT),
    "generate_options_t0": ({}, "oc.generate(PROMPT, temperature=0.0, num_ctx=16384, "
                                "num_predict=64)", OK_GENERATE),
    "chat_options_t0":     ({}, "oc.chat(_history(), tools=TOOLS, temperature=0.0, "
                                "num_ctx=16384, num_predict=64)", OK_CHAT),
    # ---- every optional key, since optional keys are where order slips
    "generate_system_think": ({"LATTICE_THINK": "1"},
                              "oc.generate(PROMPT, system=SYSTEM)", OK_GENERATE),
    "generate_think_off":    ({"LATTICE_THINK": "0"}, "oc.generate(PROMPT)", OK_GENERATE),
    "generate_env_sampling": ({"LATTICE_TEMPERATURE": "0.6", "LATTICE_TOP_P": "0.95",
                               "LATTICE_MIN_PREDICT": "2048", "LATTICE_NUDGE": "Be brief."},
                              "oc.generate(PROMPT, num_predict=100)", OK_GENERATE),
    "chat_env_all":          ({"LATTICE_THINK": "0", "LATTICE_TEMPERATURE": "0.6",
                               "LATTICE_TOP_P": "0.95", "LATTICE_MIN_PREDICT": "2048",
                               "LATTICE_NUDGE": "Be brief.", "LATTICE_NUM_CTX": "16384"},
                              "oc.chat(_history(), tools=TOOLS)", OK_CHAT),
    "generate_with_tools":   ({}, "oc.generate(PROMPT, tools=TOOLS, system=SYSTEM)", OK_CHAT),
    "base_url_override":     ({"LATTICE_BASE_URL": "http://10.0.0.5:11434"},
                              "oc.generate(PROMPT)", OK_GENERATE),
    "timeout_passed":        ({}, "oc.chat([{'role': 'user', 'content': PROMPT}], "
                                  "timeout_s=42.0)", OK_CHAT),
    # ---- llama.cpp's raw /completion
    "llamacpp_generate":     ({"LATTICE_BACKEND": "llamacpp", "LATTICE_TOP_P": "0.9"},
                              "oc.generate(PROMPT, system=SYSTEM, num_predict=77)",
                              OK_LLAMACPP),
    "llamacpp_generate_env_temp": ({"LATTICE_BACKEND": "llamacpp",
                                    "LATTICE_TEMPERATURE": "0.0",
                                    "LATTICE_MIN_PREDICT": "4096"},
                                   "oc.generate(PROMPT)", OK_LLAMACPP),
    "llamacpp_generate_tools": ({"LATTICE_BACKEND": "llamacpp"},
                                "oc.generate(PROMPT, tools=TOOLS)", OK_LLAMACPP),
    "llamacpp_chat":         ({"LATTICE_BACKEND": "llamacpp"},
                              "oc.chat([{'role': 'user', 'content': PROMPT}], tools=TOOLS)",
                              OK_CHAT),
    # ---- server behaviour: the error mapping a transport change can break
    "generate_http_500":   ({}, "oc.generate(PROMPT)",
                            ("http", 500, b'{"error":"model requires more system memory"}')),
    "chat_http_400":       ({}, "oc.chat(_history(), tools=TOOLS)",
                            ("http", 400, b'{"error":"invalid message"}')),
    "generate_refused":    ({}, "oc.generate(PROMPT)", ("url",)),
    "chat_refused":        ({}, "oc.chat(_history(), tools=TOOLS)", ("url",)),
    "generate_not_json":   ({}, "oc.generate(PROMPT)", ("raw", b"<html>502</html>")),
    "chat_not_json":       ({}, "oc.chat(_history())", ("raw", b"<html>502</html>")),
    "generate_no_response": ({}, "oc.generate(PROMPT)", {"model": "m", "done": True}),
    "chat_no_message":     ({}, "oc.chat(_history())", {"model": "m", "done": True}),
    "llamacpp_error_field": ({"LATTICE_BACKEND": "llamacpp"}, "oc.generate(PROMPT)",
                             {"error": {"code": 500, "message": "slot unavailable"}}),
    "llamacpp_http_503":   ({"LATTICE_BACKEND": "llamacpp"}, "oc.generate(PROMPT)",
                            ("http", 503, b"Loading model")),
    "llamacpp_not_json":   ({"LATTICE_BACKEND": "llamacpp"}, "oc.generate(PROMPT)",
                            ("raw", b"not json")),
}


def _runaway_cases():
    """The one real generation this clone holds: a truncation's thinking.

    The envelope is Ollama's documented reply shape; the thinking inside it is
    what the model actually produced.
    """
    if not RUNAWAY.is_file():
        return {}
    think = RUNAWAY.read_text(encoding="utf-8")
    trunc_chat = {"model": "nemotron3-nano-4b:latest",
                  "message": {"role": "assistant", "content": "", "thinking": think},
                  "done": True, "done_reason": "length", "prompt_eval_count": 1170,
                  "eval_count": 8192, "eval_duration": 1, "total_duration": 1}
    trunc_gen = {"model": "nemotron3-nano-4b:latest", "response": "", "thinking": think,
                 "done": True, "done_reason": "length", "prompt_eval_count": 1170,
                 "eval_count": 8192, "eval_duration": 1, "total_duration": 1}
    return {
        "real_runaway_chat_truncated": ({}, "oc.chat(_history(), tools=TOOLS)", trunc_chat),
        "real_runaway_generate_truncated": ({}, "oc.generate(PROMPT)", trunc_gen),
    }


def _fixture_cases() -> dict:
    """evalkit_store/parse_fixtures: 19 real /api/chat replies from the store's
    transcripts, each replayed through chat() with the tools that were offered.

    Bodies are reassembled from recorded fields, not wire bytes (see that
    directory's README), so these test the PARSE path only. They carry no
    total_duration, so the client falls back to its wall clock for
    total_duration_s; that one field is dropped from these results and nothing
    else. Each result also counts, per recovery function, how many calls it got
    and how many returned something -- so the goldens show which fixture drove
    which path, and a refactor that bypassed one would show.
    """
    if not FIXTURES.is_file():
        return {}
    out = {}
    for c in json.loads(FIXTURES.read_text(encoding="utf-8")):
        out[f"fixture_{c['case']}_{c['id']}"] = (
            {"SEAM_FIXTURE": "1"},
            "oc.chat([{'role': 'user', 'content': FIXTURE_PROMPT}], tools=TOOLS)",
            {"__fixture_prompt__": c["request_prompt"], **c["response_body"]})
    return out


def _cassette_cases(path: Path) -> dict:
    """Cases from recorded transcripts: every record replayed as a chat reply.

    A transcript record holds the text, thinking, done_reason and token counts
    the model produced, and `tool_calls` AFTER recovery. The native calls are
    the ones recovery cannot re-derive from the text, so the reply is rebuilt
    with those in message.tool_calls and the text as content -- which puts the
    recovered ones back through _calls_from_text / _calls_from_xml /
    _calls_from_bare_args / _repair_json on replay.
    """
    sys.path.insert(0, str(HERE))
    import ollama_client as oc            # only for the recovery functions
    from roles import TOOLS
    names = [t["function"]["name"] for t in TOOLS]
    files = sorted(path.rglob("*.jsonl.gz")) if path.is_dir() else [path]
    out = {}
    for f in files:
        with gzip.open(f, "rt", encoding="utf-8") as fh:
            for i, line in enumerate(fh):
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    break                      # partial tail: stop, as A5 does
                if not r.get("tool_calls") and not r.get("text"):
                    if r.get("done_reason") != "length":
                        continue
                text = r.get("text") or ""
                rederived = (oc._calls_from_text(text) + oc._calls_from_xml(text, names)
                             + oc._calls_from_bare_args(text, TOOLS)) if text else []
                rkeys = {json.dumps(c, sort_keys=True) for c in rederived}
                native = [c for c in (r.get("tool_calls") or [])
                          if json.dumps(c, sort_keys=True) not in rkeys]
                reply = {"model": r.get("model", ""),
                         "message": {"role": "assistant", "content": text,
                                     "thinking": r.get("thinking") or "",
                                     "tool_calls": [{"function": c} for c in native]},
                         "done": True, "done_reason": r.get("done_reason"),
                         "prompt_eval_count": r.get("prompt_tok") or 0,
                         "eval_count": r.get("eval_count") or 0,
                         # Not recorded in transcripts. Fixed, so the client
                         # does not fall back to a wall clock and make the
                         # result nondeterministic; no parse path reads it.
                         "eval_duration": 1, "total_duration": 1}
                name = f"cassette_{f.parent.name}_{f.stem.split('.')[0]}_{i}"
                out[name] = ({}, "oc.chat(_history(), tools=TOOLS)", reply)
    return out


# --------------------------------------------------------------- the child

def _child(case_json: str) -> None:
    env, call, reply = json.loads(case_json)
    import urllib.error
    import urllib.request
    sent = []

    class _Resp(io.BytesIO):
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def fake_urlopen(req, timeout=None, **kw):
        sent.append({"url": req.full_url, "method": req.get_method(),
                     "headers": sorted(req.header_items()), "timeout": timeout,
                     "extra_kwargs": sorted(kw),
                     "body_b64": base64.b64encode(req.data or b"").decode()})
        if isinstance(reply, list) and reply[0] == "http":
            raise urllib.error.HTTPError(req.full_url, reply[1], "err", {},
                                         io.BytesIO(reply[2].encode("latin-1")))
        if isinstance(reply, list) and reply[0] == "url":
            raise urllib.error.URLError(ConnectionRefusedError(111, "Connection refused"))
        if isinstance(reply, list) and reply[0] == "raw":
            return _Resp(reply[1].encode("latin-1"))
        return _Resp(json.dumps(reply).encode("utf-8"))

    fixture = os.environ.get("SEAM_FIXTURE") == "1"
    fixture_prompt = None
    if fixture:
        reply = dict(reply)
        fixture_prompt = reply.pop("__fixture_prompt__")

    urllib.request.urlopen = fake_urlopen
    # SEAM_CLIENT_DIR loads ollama_client (and roles) from another checkout, so
    # goldens can be written by the code BEFORE a change and compared AFTER.
    sys.path.insert(0, str(HERE))
    sys.path.insert(0, os.environ.get("SEAM_CLIENT_DIR") or str(HERE))
    import ollama_client as oc
    from roles import TOOLS
    hits = {}
    if fixture:
        for fn in RECOVERY_FNS:
            orig = getattr(oc, fn)
            hits[fn] = [0, 0]

            def wrapped(*a, _orig=orig, _fn=fn, **k):
                r = _orig(*a, **k)
                hits[_fn][0] += 1
                hits[_fn][1] += bool(r)
                return r
            setattr(oc, fn, wrapped)
    ns = {"oc": oc, "TOOLS": TOOLS, "PROMPT": PROMPT, "SYSTEM": SYSTEM,
          "_history": _history, "FIXTURE_PROMPT": fixture_prompt}
    oc.meter_reset()
    try:
        g = eval(call, ns)                                   # noqa: S307
        result = {"returned": {
            "text": g.text, "model": g.model,
            "prompt_eval_count": g.prompt_eval_count, "eval_count": g.eval_count,
            "total_duration_s": g.total_duration_s, "load_duration_s": g.load_duration_s,
            "tool_calls": g.tool_calls, "tokens_per_s": g.tokens_per_s,
            "raw": g.raw}}
        if fixture:
            result["returned"].pop("total_duration_s")      # wall-clock fallback
    except Exception as e:  # noqa: BLE001
        result = {"raised": {"type": type(e).__name__,
                             "mro": [c.__name__ for c in type(e).__mro__[:4]],
                             "message": str(e),
                             "cause": type(e.__cause__).__name__ if e.__cause__ else None,
                             "has_gen": hasattr(e, "gen"),
                             "num_predict": getattr(e, "num_predict", None)}}
    result["meter"] = oc.meter_read()
    if fixture:
        result["recovery_calls_and_hits"] = hits
    print("@@CAPTURE@@" + json.dumps({"sent": sent, "result": result}))


# --------------------------------------------------------------- the parent

CLIENT_DIR: Path | None = None


def _run(name: str, case) -> dict:
    env, call, reply = case
    if isinstance(reply, tuple):
        reply = [reply[0], *[(x.decode("latin-1") if isinstance(x, bytes) else x)
                             for x in reply[1:]]]
    child_env = {k: v for k, v in os.environ.items() if not k.startswith("LATTICE_")}
    child_env.update({"LATTICE_TRANSCRIPT": "0", **env})
    if CLIENT_DIR:
        child_env["SEAM_CLIENT_DIR"] = str(CLIENT_DIR)
    cp = subprocess.run([sys.executable, __file__, "--child",
                         json.dumps([env, call, reply])],
                        env=child_env, capture_output=True, text=True, cwd=HERE)
    line = next((l for l in cp.stdout.splitlines() if l.startswith("@@CAPTURE@@")), None)
    if line is None:
        raise SystemExit(f"{name}: child failed\n{cp.stderr[-3000:]}")
    return json.loads(line[len("@@CAPTURE@@"):])


def _files(cap: dict) -> dict[str, bytes]:
    """The golden files for one capture, as exact bytes."""
    if len(cap["sent"]) > 1:
        raise SystemExit("a case sent more than one request; split it")
    files = {}
    if cap["sent"]:
        s = cap["sent"][0]
        meta = {k: s[k] for k in ("url", "method", "headers", "timeout", "extra_kwargs")}
        files["request.meta.json"] = (json.dumps(meta, indent=1, sort_keys=True)
                                      + "\n").encode()
        files["request.body"] = base64.b64decode(s["body_b64"])
    else:
        files["request.meta.json"] = b'"no request was sent"\n'
    files["result.json"] = (json.dumps(cap["result"], indent=1, sort_keys=True,
                                       ensure_ascii=False) + "\n").encode("utf-8")
    return files


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--cassette", type=Path)
    ap.add_argument("--golden", type=Path, default=GOLDEN)
    ap.add_argument("--child")
    ap.add_argument("--client-dir", type=Path,
                    help="import ollama_client from this directory instead, "
                         "e.g. an M4 dir in a worktree of the pre-change commit")
    a = ap.parse_args(argv)
    global CLIENT_DIR
    CLIENT_DIR = a.client_dir.resolve() if a.client_dir else None
    if a.child:
        _child(a.child)
        return 0
    cases = {**CASES, **_runaway_cases(), **_fixture_cases()}
    if a.cassette:
        cases.update(_cassette_cases(a.cassette))
    if a.only:
        cases = {k: v for k, v in cases.items() if k in a.only}
    bad = 0
    for name, case in cases.items():
        files = _files(_run(name, case))
        d = a.golden / name
        if a.write:
            d.mkdir(parents=True, exist_ok=True)
            for fn, data in files.items():
                (d / fn).write_bytes(data)
            print(f"wrote   {name}")
            continue
        diffs = []
        for fn, data in files.items():
            p = d / fn
            old = p.read_bytes() if p.is_file() else None
            if old != data:
                diffs.append(fn)
                if old is not None:
                    sys.stdout.writelines(difflib.unified_diff(
                        old.decode("utf-8", "replace").splitlines(True),
                        data.decode("utf-8", "replace").splitlines(True),
                        f"golden/{name}/{fn}", f"now/{name}/{fn}"))
                else:
                    print(f"  (no golden {name}/{fn})")
        extra = ({p.name for p in d.iterdir()} - set(files)) if d.is_dir() else set()
        diffs += sorted(extra)
        print(f"{'IDENTICAL' if not diffs else 'DIFFERS  '} {name}"
              + (f"  {diffs}" if diffs else ""))
        bad += bool(diffs)
    if not a.write:
        print(f"\n{len(cases) - bad}/{len(cases)} case(s) byte-identical to golden")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
