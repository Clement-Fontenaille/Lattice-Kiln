"""Transport to an inference server, normalised to one shape.

WHY THIS EXISTS. Until now the client carried `if BACKEND == "llamacpp"` at
three call sites, which was tolerable for two backends and is not for four. The
H100 sweep will not have Ollama at all, and the stack there is some mix of
vLLM, litellm and llama.cpp.

THE SEAM IS OPENAI /v1/chat/completions. vLLM serves it, llama.cpp serves it
under `--jinja`, litellm *is* it, and Ollama offers it too. Ollama's native
/api/chat is the exception rather than the default, which is the opposite of
how this module used to be organised.

WHAT IS AND IS NOT BACKEND BUSINESS. This module does transport and nothing
else: build a request, read a response, normalise it. The repair and recovery
layers (`_calls_from_text`, `_calls_from_xml`, `_repair_json`) stay in the
client, because 2026-09-23 established they are properties of the MODEL, not
the server -- qwen2.5-coder emits bare unwrapped JSON whoever is serving it,
and Nemotron Nano 9B improvises XML for the same reason anywhere.

WHAT CHANGES ON THE OTHER BACKENDS, AND IT IS NOT SMALL. Ollama renders the
prompt with a RENDERER chosen from the model's architecture, which cannot be
displaced -- two Modelfile routes were tried and both rendered byte-identically
(42 -> 619 prompt tokens either way). That single fact is why three separate
things were unreachable here:

    NVIDIA's <AVAILABLE_TOOLS>/<TOOLCALL> format   the 9B's own dialect
    /think and /no_think                           its documented reasoning
                                                   control
    qwen's <tool_call> wrapper                     needs a matching parser

vLLM and llama.cpp both take a chat template as an argument, and vLLM takes a
named tool parser (`hermes`, `nemotron_json`). So on those backends the output
protocol goes back to being OUR variable, which is what 50-findings/15 wanted
and could not have. Findings recorded here as "ruled out" are ruled out ON
OLLAMA and should be re-tested rather than inherited.

It also means the prompt becomes RECORDABLE. Ollama composes several hundred
tokens of tool-definition text we never see; where we supply the template, the
whole rendered prompt is ours to hash. `template_ref` carries that so the key
can grow into it without another migration.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any


class BackendError(RuntimeError):
    """A transport failure. `kind` says which, so a caller can word it its own way:

        http   the server answered with an error status; `code`, `detail`
        url    no answer at all (refused, unreachable, timed out)
        json   an answer that was not JSON
        None   anything else raised here (a reply missing its field, ...)

    The original exception is the __cause__, as it always was.
    """

    def __init__(self, message: str, *, kind: str | None = None,
                 code: int | None = None, detail: str | None = None):
        super().__init__(message)
        self.kind, self.code, self.detail = kind, code, detail


@dataclass
class Reply:
    """One completion, in the same shape whatever produced it.

    `tool_calls` is the SERVER's structured extraction only -- [] means the
    server parsed none, never that the model emitted none. The client's
    recovery layer decides that, and needs the distinction to count
    `tool_native` against `tool_recovered`.
    """
    text: str
    thinking: str = ""
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    prompt_tokens: int = 0
    eval_tokens: int = 0
    total_s: float = 0.0
    load_s: float = 0.0
    gen_s: float = 0.0
    prompt_s: float = 0.0
    done_reason: str | None = None
    raw: dict[str, Any] = field(repr=False, default_factory=dict)


def _post(url: str, body: dict, timeout_s: float) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        # Read the body. Every server puts the actual reason in it, and a bare
        # "HTTP 500" says nothing about whether the fault is the prompt, the
        # options or the message list.
        try:
            detail = e.read().decode("utf-8", "replace")[:500]
        except Exception:  # noqa: BLE001
            detail = "(body unreadable)"
        raise BackendError(f"{url} -> HTTP {e.code}: {detail}", kind="http",
                           code=e.code, detail=detail) from e
    except urllib.error.URLError as e:
        raise BackendError(f"{url} -> {e}", kind="url") from e
    except json.JSONDecodeError as e:
        raise BackendError(f"{url} -> malformed JSON: {e}", kind="json") from e


def _norm_calls(raw: list | None) -> list[dict[str, Any]]:
    """OpenAI-shaped tool calls -> {"name", "arguments"} with arguments decoded.

    `arguments` is a JSON STRING in the OpenAI wire format and an object in
    Ollama's. Both appear; decode one level so callers never have to care.
    """
    out = []
    for c in raw or []:
        fn = (c or {}).get("function") or {}
        args = fn.get("arguments")
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except json.JSONDecodeError:
                args = {"_raw": args}
        out.append({"name": fn.get("name", ""),
                    "arguments": args if isinstance(args, dict) else {}})
    return out


# --------------------------------------------------------------- ollama
class Ollama:
    """Native /api/chat and /api/generate.

    Kept because it is what runs locally, and because /api/generate is the only
    endpoint here that takes a pre-rendered string without a chat template
    wrapped round it.
    """
    name = "ollama"
    supports_tools = True
    supports_raw_prompt = True
    default_base_url = "http://localhost:11434"
    # Ollama chooses the chat template itself, from the model's architecture,
    # and will not let it be replaced. Recorded as a fact about the key: the
    # prompt cannot be reconstructed from anything we hold.
    template_ref = "server-chosen:opaque"

    # The *_raw methods are the seam ollama_client uses: build the request, send
    # it, return the reply as the server gave it. Validation and parsing stay
    # with the caller, which is where the model-specific recovery lives. Key
    # ORDER in these bodies is part of the contract -- it is what the bytes on
    # the wire are, and seam_capture.py holds them byte for byte.
    def chat_raw(self, messages, *, base_url, model, tools=None, options=None,
                 think=None, timeout_s=600.0) -> dict:
        body = {"model": model, "messages": messages, "stream": False,
                "options": options or {}}
        if tools:
            body["tools"] = tools
        if think is not None:
            body["think"] = think
        return _post(f"{base_url}/api/chat", body, timeout_s)

    def complete_raw(self, prompt, *, base_url, model, options=None, system=None,
                     think=None, timeout_s=600.0) -> dict:
        body = {"model": model, "prompt": prompt, "stream": False,
                "options": options or {}}
        # think BEFORE system: the order ollama_client always sent. This method
        # first had them swapped (as the old complete() did), and seam_capture's
        # generate_system_think golden caught it byte for byte.
        if think is not None:
            body["think"] = think
        if system:
            body["system"] = system
        return _post(f"{base_url}/api/generate", body, timeout_s)

    def chat(self, messages, *, base_url, model, tools=None, options=None,
             think=None, timeout_s=600.0) -> Reply:
        p = self.chat_raw(messages, base_url=base_url, model=model, tools=tools,
                          options=options, think=think, timeout_s=timeout_s)
        msg = p.get("message")
        if not isinstance(msg, dict):
            raise BackendError(f"no 'message' in reply: {p!r}")
        return self._reply(p, msg.get("content") or "",
                           msg.get("thinking") or "",
                           _norm_calls(msg.get("tool_calls")))

    def complete(self, prompt, *, base_url, model, options=None, system=None,
                 think=None, timeout_s=600.0) -> Reply:
        p = self.complete_raw(prompt, base_url=base_url, model=model,
                              options=options, system=system, think=think,
                              timeout_s=timeout_s)
        if "response" not in p:
            raise BackendError(f"no 'response' in reply: {p!r}")
        return self._reply(p, p["response"], p.get("thinking") or "", [])

    @staticmethod
    def _reply(p: dict, text: str, thinking: str, calls: list) -> Reply:
        return Reply(
            text=text, thinking=thinking, tool_calls=calls,
            prompt_tokens=p.get("prompt_eval_count", 0),
            eval_tokens=p.get("eval_count", 0),
            total_s=p.get("total_duration", 0) / 1e9,
            load_s=p.get("load_duration", 0) / 1e9,
            gen_s=p.get("eval_duration", 0) / 1e9,          # nanoseconds
            prompt_s=p.get("prompt_eval_duration", 0) / 1e9,
            done_reason=p.get("done_reason"), raw=p)

    def health(self, base_url, timeout_s=5.0) -> bool:
        try:
            urllib.request.urlopen(f"{base_url}/api/tags", timeout=timeout_s)
            return True
        except Exception:  # noqa: BLE001
            return False


# --------------------------------------------------------------- openai
class OpenAICompatible:
    """/v1/chat/completions: vLLM, litellm, llama.cpp --jinja, and others.

    The target for the H100 sweep. Three things it can do that Ollama cannot,
    all of which today's findings ran aground on:

      - the chat template is supplied at server start, so the model's OWN
        documented format is reachable;
      - the tool parser is named (`--tool-call-parser hermes`,
        `nemotron_json`), rather than inferred from the architecture;
      - the rendered prompt is therefore something we author and can hash.

    Reasoning text arrives as `reasoning_content` on vLLM (with a reasoning
    parser configured) and llama.cpp; both spellings are read, because a
    reasoning model whose thinking lands in `content` instead is the failure
    that cost this project a day when it looked like a model that judged badly.
    """
    name = "openai"
    supports_tools = True
    supports_raw_prompt = False
    default_base_url = "http://localhost:8000/v1"
    template_ref = "client-supplied"

    def chat(self, messages, *, base_url, model, tools=None, options=None,
             think=None, timeout_s=600.0) -> Reply:
        o = dict(options or {})
        body: dict[str, Any] = {"model": model, "messages": messages,
                                "stream": False}
        # Option names differ from Ollama's; translate rather than leak either
        # vocabulary into the callers.
        if "temperature" in o:
            body["temperature"] = o["temperature"]
        if "top_p" in o:
            body["top_p"] = o["top_p"]
        if o.get("num_predict"):
            body["max_tokens"] = o["num_predict"]
        if tools:
            body["tools"] = tools
            body["tool_choice"] = "auto"
        # There is no portable `think` flag. vLLM and llama.cpp take reasoning
        # settings at SERVER START, not per request, so a caller asking for it
        # here is asking for something this transport cannot deliver -- say so
        # rather than silently ignoring it.
        if think is not None:
            body["chat_template_kwargs"] = {"enable_thinking": bool(think)}
        t0 = time.monotonic()
        p = _post(f"{base_url}/chat/completions", body, timeout_s)
        wall = time.monotonic() - t0
        choices = p.get("choices") or []
        if not choices:
            raise BackendError(f"no choices in reply: {p!r}")
        msg = choices[0].get("message") or {}
        usage = p.get("usage") or {}
        return Reply(
            text=msg.get("content") or "",
            thinking=(msg.get("reasoning_content")
                      or msg.get("reasoning") or ""),
            tool_calls=_norm_calls(msg.get("tool_calls")),
            prompt_tokens=usage.get("prompt_tokens", 0),
            eval_tokens=usage.get("completion_tokens", 0),
            total_s=wall,
            # Neither server reports a decode/prefill split in this shape, so
            # gen_s is left at 0 rather than filled with the wall clock. A
            # throughput figure built from a wall clock that includes queueing
            # is not the same measurement as one built from decode time, and
            # silently substituting one for the other is how a 3.4x placement
            # difference once read as hardware.
            done_reason=choices[0].get("finish_reason"), raw=p)

    def health(self, base_url, timeout_s=5.0) -> bool:
        try:
            urllib.request.urlopen(f"{base_url}/models", timeout=timeout_s)
            return True
        except Exception:  # noqa: BLE001
            return False


# --------------------------------------------------------------- llama.cpp
class LlamaCppRaw:
    """llama-server's native /completion: a pre-rendered string, no template.

    Retained, not deprecated. It is the ONLY transport here that sends exactly
    the bytes given, which makes it the instrument for any question about what
    a template or renderer is doing -- the `raw: true` probes that established
    which Nemotron tokens are live needed precisely this.

    It has no tool channel. That is a fact about the endpoint, not a gap to be
    papered over: asking it for tools raises, so a caller cannot quietly get a
    tool-less run and score it against tool-enabled ones.
    """
    name = "llamacpp"
    supports_tools = False
    supports_raw_prompt = True
    default_base_url = "http://localhost:8090"
    template_ref = "none:caller-rendered"

    def chat(self, messages, **kw):
        raise BackendError(
            "llamacpp /completion has no chat or tool channel. Use the openai "
            "backend against llama-server --jinja, which does.")

    def complete_raw(self, prompt, *, base_url, model=None, options=None,
                     system=None, think=None, timeout_s=600.0) -> dict:
        o = dict(options or {})
        body = {"prompt": (f"{system}\n\n{prompt}" if system else prompt),
                "n_predict": o.get("num_predict", 1536),
                "temperature": o.get("temperature", 0.2)}
        if "top_p" in o:
            body["top_p"] = o["top_p"]
        return _post(f"{base_url}/completion", body, timeout_s)

    def complete(self, prompt, *, base_url, model=None, options=None,
                 system=None, think=None, timeout_s=600.0) -> Reply:
        p = self.complete_raw(prompt, base_url=base_url, model=model,
                              options=options, system=system, think=think,
                              timeout_s=timeout_s)
        t = p.get("timings") or {}
        return Reply(
            text=p.get("content") or "",
            prompt_tokens=t.get("prompt_n", 0),
            eval_tokens=t.get("predicted_n", 0),
            gen_s=t.get("predicted_ms", 0) / 1000,          # milliseconds
            prompt_s=t.get("prompt_ms", 0) / 1000,
            done_reason=("length" if p.get("stopped_limit") else "stop"),
            raw=p)

    def health(self, base_url, timeout_s=5.0) -> bool:
        try:
            urllib.request.urlopen(f"{base_url}/health", timeout=timeout_s)
            return True
        except Exception:  # noqa: BLE001
            return False


REGISTRY = {b.name: b for b in (Ollama(), OpenAICompatible(), LlamaCppRaw())}
ALIASES = {"vllm": "openai", "litellm": "openai", "llamacpp-jinja": "openai",
           "llama.cpp": "llamacpp", "llama_cpp": "llamacpp"}


def get(name: str | None = None):
    """Backend by name. Aliases resolve, so a config may say what it means."""
    n = (name or os.environ.get("LATTICE_BACKEND") or "ollama").strip().lower()
    n = ALIASES.get(n, n)
    if n not in REGISTRY:
        raise BackendError(
            f"unknown backend {n!r}; have {sorted(REGISTRY)} "
            f"and aliases {sorted(ALIASES)}")
    return REGISTRY[n]
