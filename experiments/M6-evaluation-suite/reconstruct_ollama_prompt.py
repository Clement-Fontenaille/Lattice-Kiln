"""Reconstruct, byte for byte, the prompt Ollama builds for nemotron-3-nano.

WHY. The rendered prompt is not returned by any Ollama endpoint, so what
actually reaches the model was unknown. That is not a black box: the renderer is
Go source in ollama/model/renderers/nemotron3nano.go, reading it is in scope,
and a reconstruction can be VERIFIED rather than believed -- if it tokenises to
the same prompt_eval_count as the live call, the contract is established.

TRANSCRIBED FROM SOURCE, not inferred from behaviour. Every literal below is
copied from Render() and renderTools(). The verification step is what makes this
worth anything: a reconstruction nobody checked is just a second guess.

    python reconstruct_ollama_prompt.py
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "M4-ephemeral-processors"))
from roles import TOOLS  # noqa: E402

BASE = "http://localhost:11434"
MODEL = "nemotron3-nano-4b:latest"

# renderTools(), verbatim from source.
_TOOL_HEAD = "# Tools\n\nYou have access to the following functions:\n\n<tools>"
_TOOL_TAIL = (
    "\n</tools>"
    "\n\nIf you choose to call a function ONLY reply in the following format with NO suffix:\n\n"
    "<tool_call>\n<function=example_function_name>\n<parameter=example_parameter_1>\nvalue_1\n</parameter>\n"
    "<parameter=example_parameter_2>\nThis is the value for the second parameter\nthat can span\nmultiple lines\n"
    "</parameter>\n</function>\n</tool_call>\n\n<IMPORTANT>\nReminder:\n"
    "- Function calls MUST follow the specified format: an inner <function=...></function> block must be nested within <tool_call></tool_call> XML tags\n"
    "- Required parameters MUST be specified\n"
    "- You may provide optional reasoning for your function call in natural language BEFORE the function call, but NOT after\n"
    "- If there is no function call available, answer the question like normal with your current knowledge and do not tell the user about function calls\n</IMPORTANT>")


def _python_json(v) -> str:
    """pythonJSON(): a []string renders as ["a", "b"] -- note the space."""
    if isinstance(v, str):
        return json.dumps(v)
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(_python_json(x) for x in v) + "]"
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return "null"
    if isinstance(v, dict):
        return "{" + ", ".join(f"{json.dumps(k)}: {_python_json(v[k])}"
                               for k in sorted(v)) + "}"
    return json.dumps(v)


def render_tools(tools: list[dict]) -> str:
    sb = [_TOOL_HEAD]
    for t in tools:
        fn = t["function"]
        sb.append("\n<function>\n<name>" + fn["name"] + "</name>")
        if fn.get("description"):
            sb.append("\n<description>" + fn["description"].strip() + "</description>")
        sb.append("\n<parameters>")
        params = fn.get("parameters") or {}
        for pname, pf in (params.get("properties") or {}).items():
            sb.append("\n<parameter>")
            sb.append("\n<name>" + pname + "</name>")
            ptype = pf.get("type")
            if ptype:
                # formatPropertyType: one type prints bare, several as
                # ['a', 'b'] with single quotes.
                sb.append("\n<type>" + (ptype if isinstance(ptype, str) else
                                        "[" + ", ".join(f"'{x}'" for x in ptype) + "]")
                          + "</type>")
            if pf.get("description"):
                sb.append("\n<description>" + pf["description"].strip() + "</description>")
            if pf.get("enum"):
                sb.append("\n<enum>" + _python_json(pf["enum"]) + "</enum>")
            if pf.get("items") is not None:
                sb.append("\n<items>" + _python_json(pf["items"]) + "</items>")
            sb.append("\n</parameter>")
        if params.get("required"):
            sb.append("\n<required>" + _python_json(params["required"]) + "</required>")
        sb.append("\n</parameters>")
        sb.append("\n</function>")
    sb.append(_TOOL_TAIL)
    return "".join(sb)


def render(messages: list[dict], tools: list[dict] | None,
           thinking: bool = True) -> str:
    """Render(), verbatim. Returns the exact string fed to the model."""
    system, loop = "", list(messages)
    if loop and loop[0]["role"] == "system":
        system = loop[0]["content"]
        loop = loop[1:]

    last_user = -1
    for i, m in enumerate(loop):
        if m["role"] == "user":
            last_user = i

    out = ["<|im_start|>system\n"]
    if system:
        out.append(system)
    if tools:
        if system:
            out.append("\n\n")
        out.append(render_tools(tools))
    out.append("<|im_end|>\n")

    for i, m in enumerate(loop):
        role = m["role"]
        if role == "assistant":
            content = m.get("content") or ""
            if m.get("thinking"):
                content = "<think>\n" + m["thinking"] + "\n</think>\n" + content
            elif "<think>" not in content and "</think>" not in content:
                content = "<think></think>" + content
            out.append("<|im_start|>assistant\n")
            if m.get("tool_calls"):
                out.append("<think></think>" if not content.strip()
                           else content.strip() + "\n")
                for tc in m["tool_calls"]:
                    f = tc["function"]
                    out.append("<tool_call>\n<function=" + f["name"] + ">\n")
                    for k, v in (f.get("arguments") or {}).items():
                        sv = (_python_json(v) if isinstance(v, (list, dict))
                              else ("None" if v is None else
                                    "True" if v is True else
                                    "False" if v is False else str(v)))
                        out.append("<parameter=" + k + ">\n" + sv + "\n</parameter>\n")
                    out.append("</function>\n</tool_call>\n")
            else:
                out.append(content.strip())
            out.append("<|im_end|>\n")
        elif role in ("user", "system"):
            out.append("<|im_start|>" + role + "\n")
            # stripThinkToggles then TrimSpace
            c = (m.get("content") or "").replace("</think>", "<_end_think>")
            c = c.replace("/think", "").replace("/no_think", "")
            out.append(c.replace("<_end_think>", "</think>").strip())
            out.append("<|im_end|>\n")
        elif role == "tool":
            prev_tool = i > 0 and loop[i - 1]["role"] == "tool"
            next_tool = i + 1 < len(loop) and loop[i + 1]["role"] == "tool"
            if i > 0 and not prev_tool:
                out.append("<|im_start|>user\n")
            out.append("<tool_response>\n" + (m.get("content") or "") + "\n</tool_response>\n")
            if not next_tool:
                out.append("<|im_end|>\n")
    out.append("<|im_start|>assistant\n<think>\n" if thinking
               else "<|im_start|>assistant\n<think></think>")
    return "".join(out)


def prompt_tokens_live(messages, tools, think=True) -> int:
    body = {"model": MODEL, "messages": messages, "stream": False, "think": think,
            "options": {"temperature": 0, "num_predict": 1, "num_ctx": 16384}}
    if tools:
        body["tools"] = tools
    req = urllib.request.Request(f"{BASE}/api/chat",
                                data=json.dumps(body).encode("utf-8"),
                                headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read().decode("utf-8")).get("prompt_eval_count", 0)


def prompt_tokens_raw(text: str) -> int:
    """Token count for a string sent with raw:true, so no template applies."""
    body = {"model": MODEL, "prompt": text, "raw": True, "stream": False,
            "options": {"temperature": 0, "num_predict": 1, "num_ctx": 16384}}
    req = urllib.request.Request(f"{BASE}/api/generate",
                                data=json.dumps(body).encode("utf-8"),
                                headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read().decode("utf-8")).get("prompt_eval_count", 0)


CASES = [
    ("user only, no tools", [{"role": "user", "content": "hi"}], None),
    ("user only, with tools", [{"role": "user", "content": "hi"}], TOOLS),
    ("system + user + tools",
     [{"role": "system", "content": "You are terse."},
      {"role": "user", "content": "hi"}], TOOLS),
    ("after a tool turn",
     [{"role": "user", "content": "write a.py"},
      {"role": "assistant", "content": "",
       "tool_calls": [{"function": {"name": "write_file",
                                    "arguments": {"path": "a.py", "content": "x = 1"}}}]},
      {"role": "tool", "tool_name": "write_file", "content": '{"status": "accepted"}'}],
     TOOLS),
]

if __name__ == "__main__":
    print(f"{MODEL}\n")
    ok = True
    for label, msgs, tools in CASES:
        mine = render(msgs, tools)
        n_mine = prompt_tokens_raw(mine)
        n_live = prompt_tokens_live(msgs, tools)
        match = n_mine == n_live
        ok &= match
        print(f"  {label:24} reconstructed {n_mine:>5} | live {n_live:>5} | "
              f"{'MATCH' if match else 'DIFFER by ' + str(n_mine - n_live)}")
    print()
    print("EXACT CONTRACT ESTABLISHED" if ok else
          "reconstruction incomplete -- the differing case shows where")
    print()
    print("=== what actually reaches the model (user only, with tools) ===")
    print(render([{"role": "user", "content": "hi"}], TOOLS))
