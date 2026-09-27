"""Does Ollama actually do its half of the tool protocol, per model?

Two halves, and they fail separately:

  RENDER  serialise the tool definitions into the prompt in the model's own
          tuned dialect. Measured as the prompt-token cost of adding `tools`
          to an otherwise identical request. Zero means nothing was injected
          and the model was never told the tools exist.

  PARSE   lift the emitted call back out of the text into `message.tool_calls`.
          Measured by whether the call arrives structured, or has to be
          recovered from `content` by the client.

A model can pass one and fail the other, and the failure modes look nothing
alike from the outside -- which is why they are separated here.

WHOSE FAULT A MISSING PARSE IS DEPENDS ON THE TEMPLATE, and reading it is not
optional. qwen2.5-coder returns its call as plain `content`, which looks like an
Ollama parser gap and is not: its template explicitly instructs
`<tool_call>{...}</tool_call>` with "NO other text", and the model emits bare
JSON without the wrapper. Ollama rendered the contract correctly; the model did
not honour it. Measured 9/9 bare, with and without this harness's own protocol
text, so the prompt is not the cause either.

That is why `wrapper_demanded` is reported below. Without it a compliance
failure reads as an infrastructure failure, which is the same mistake in the
opposite direction as the one 50-findings/15 is about.

Also reports the turn structure, because the tool protocol is multi-turn where
the marker protocol was not: a model emits one call, stops, and waits for a
tool result before emitting the next.

    python probe_tool_channel.py [model ...]
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "M4-ephemeral-processors"))

from ollama_client import _calls_from_text  # noqa: E402
from roles import PROTOCOL_TOOLS, TOOLS     # noqa: E402
from probe_record import persist            # noqa: E402

BASE = "http://localhost:11434"
DEFAULT_MODELS = ["nemotron3-nano-4b:latest",
                  "nemotron-gpu:latest",
                  "qwen2.5-coder:7b-instruct-q4_K_M"]

OBJECTIVE = ("Create a file utils/greet.py holding a function greet(name) that "
             "returns the string 'Hello, <name>!'. Include a module docstring.")
PROMPT = f"You are an implementer.\n\n# OBJECTIVE\n{OBJECTIVE}\n\n{PROTOCOL_TOOLS}"


def _post(path: str, body: dict, timeout: float = 300.0) -> dict:
    req = urllib.request.Request(
        f"{BASE}{path}", data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def declared(model: str) -> dict:
    """What Ollama says it can do, before anything is generated."""
    try:
        d = _post("/api/show", {"model": model}, timeout=30)
    except Exception as e:                                     # noqa: BLE001
        return {"error": repr(e)[:80]}
    tmpl = d.get("template") or ""
    return {"capabilities": d.get("capabilities") or [],
            "tools_in_template": ".Tools" in tmpl,
            # The wrapper the template tells the model to emit. If one is
            # demanded and the call still arrives as bare text, the model broke
            # the contract -- Ollama did its half.
            "wrapper_demanded": "<tool_call>" in tmpl,
            "family": (d.get("details") or {}).get("family", "?")}


def render_cost(model: str) -> tuple[int, int]:
    """Prompt tokens without tools, and with. The difference IS the injection."""
    msgs = [{"role": "user", "content": "hi"}]
    opts = {"temperature": 0, "num_predict": 1, "num_ctx": 8192}
    a = _post("/api/chat", {"model": model, "messages": msgs,
                            "stream": False, "options": opts})
    b = _post("/api/chat", {"model": model, "messages": msgs, "tools": TOOLS,
                            "stream": False, "options": opts})
    return a.get("prompt_eval_count", 0), b.get("prompt_eval_count", 0)


def loop(model: str, max_turns: int = 6) -> dict:
    """Drive the real protocol and report how each call arrived."""
    msgs = [{"role": "user", "content": PROMPT}]
    turns, native, recovered, files, ctrl = [], 0, 0, {}, None
    per_turn = []                 # raw, per request: persisted, not summarised
    for _ in range(max_turns):
        p = _post("/api/chat", {"model": model, "messages": msgs,
                                "tools": TOOLS, "stream": False,
                                "options": {"temperature": 0.2, "num_ctx": 8192,
                                            "num_predict": 1024}})
        msg = p.get("message") or {}
        raw = msg.get("tool_calls") or []
        text = msg.get("content") or ""
        if raw:
            calls = [{"name": c["function"]["name"],
                      "arguments": c["function"].get("arguments") or {}}
                     for c in raw]
            native += len(calls)
            how = "native"
        else:
            calls = _calls_from_text(text)
            recovered += len(calls)
            how = "recovered" if calls else "none"
        turns.append(how)
        per_turn.append({"how": how, "n_calls": len(calls),
                         "prompt_eval_count": p.get("prompt_eval_count"),
                         "eval_count": p.get("eval_count"),
                         "done_reason": p.get("done_reason"),
                         "content": text, "tool_calls": raw})
        if not calls:
            break
        msgs.append({"role": "assistant", "content": text, "tool_calls": raw})
        for c in calls:
            if c["name"] == "write_file":
                files[str(c["arguments"].get("path", ""))] = \
                    str(c["arguments"].get("content", ""))
            elif c["name"] == "conclude":
                ctrl = c["arguments"]
            msgs.append({"role": "tool", "tool_name": c["name"],
                         "content": "recorded"})
        if ctrl is not None:
            break
    return {"turns": turns, "native": native, "recovered": recovered,
            "files": files, "control": ctrl, "per_turn": per_turn}


def _verdict(dec: dict, cost: tuple[int, int], r: dict) -> str:
    if not r["files"]:
        return "BROKEN - no file came back"
    if r["control"] is None:
        return "PARTIAL - file written, conclude never arrived"
    body = next(iter(r["files"].values()))
    if body.count("\n") < 2:
        return "DEGENERATE - file content has no line structure"
    if r["recovered"] and not r["native"]:
        if dec.get("wrapper_demanded"):
            return ("WORK OK, PROTOCOL BROKEN BY MODEL - template demands "
                    "<tool_call> wrapper, model emitted bare JSON; recovered")
        return ("WORK OK, OLLAMA PARSER DID NOT FIRE - template demands no "
                "wrapper, so the gap is server-side; recovered")
    if r["recovered"]:
        return "OK - but some calls needed recovery"
    return "OK - native end to end"


def main(models: list[str]) -> None:
    records = []
    try:
        _main(models, records)
    finally:
        persist("tool_channel", {"models": models, "prompt": PROMPT,
                                 "loop_options": {"temperature": 0.2,
                                                  "num_ctx": 8192,
                                                  "num_predict": 1024}},
                records)


def _main(models: list[str], records: list) -> None:
    for m in models:
        rec = {"model": m}
        records.append(rec)
        print("=" * 70)
        print(m)
        dec = declared(m)
        rec["declared"] = dec
        if "error" in dec:
            print("  /api/show failed:", dec["error"])
            continue
        print(f"  declared : capabilities={dec['capabilities']} "
              f"family={dec['family']} .Tools_in_template={dec['tools_in_template']} "
              f"wrapper_demanded={dec['wrapper_demanded']}")
        try:
            a, b = render_cost(m)
        except Exception as e:                                 # noqa: BLE001
            print("  render   : FAILED", repr(e)[:80])
            a = b = 0
        rec["render_prompt_tokens"] = [a, b]
        print(f"  render   : prompt tokens {a} -> {b} with tools "
              f"(+{b - a}){'  <-- NOTHING INJECTED' if b <= a else ''}")
        try:
            r = loop(m)
        except Exception as e:                                 # noqa: BLE001
            print("  loop     : FAILED", repr(e)[:120])
            rec["loop_error"] = repr(e)
            continue
        rec["loop"] = r
        print(f"  parse    : {' '.join(r['turns'])}  "
              f"(native={r['native']} recovered={r['recovered']})")
        for p, c in r["files"].items():
            print(f"  file     : {p!r} {len(c)}ch {c.count(chr(10))} newlines")
            for line in c.splitlines()[:4]:
                print("             |", line)
        print(f"  conclude : {r['control']}")
        rec["verdict"] = _verdict(dec, (a, b), r)
        print(f"  VERDICT  : {rec['verdict']}")


if __name__ == "__main__":
    main(sys.argv[1:] or DEFAULT_MODELS)
