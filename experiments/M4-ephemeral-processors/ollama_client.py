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

import json
import os
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

    @property
    def tokens_per_s(self) -> float:
        # Ollama: eval_duration is nanoseconds. llama-server: timings.predicted_ms
        # is milliseconds. Different units, same meaning (generation-phase time).
        if "timings" in self.raw:
            d = self.raw.get("timings", {}).get("predicted_ms", 0) / 1000
        else:
            d = self.raw.get("eval_duration", 0) / 1e9
        return (self.eval_count / d) if d else 0.0


def generate(prompt: str, *, model: str = DEFAULT_MODEL, base_url: str = DEFAULT_BASE_URL,
             num_ctx: int = DEFAULT_NUM_CTX, temperature: float = 0.2,
             num_predict: int = 1536, timeout_s: float = 600.0,
             system: str | None = None) -> Generation:
    if BACKEND == "llamacpp":
        return _generate_llamacpp(prompt, base_url=base_url, model=model,
                                  temperature=temperature, num_predict=num_predict,
                                  timeout_s=timeout_s, system=system)
    body = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature, "num_ctx": num_ctx, "num_predict": num_predict},
    }
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
    return Generation(
        text=payload["response"],
        model=payload.get("model", model),
        prompt_eval_count=payload.get("prompt_eval_count", 0),
        eval_count=payload.get("eval_count", 0),
        total_duration_s=payload.get("total_duration", 0) / 1e9 or (time.monotonic() - t0),
        load_duration_s=payload.get("load_duration", 0) / 1e9,
        raw=payload,
    )


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
    body = {"prompt": full_prompt, "n_predict": num_predict, "temperature": temperature}
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
    return Generation(
        text=payload["content"],
        model=payload.get("model", model),
        prompt_eval_count=int(t.get("prompt_n", 0)),
        eval_count=int(t.get("predicted_n", 0)),
        total_duration_s=(t.get("prompt_ms", 0) + t.get("predicted_ms", 0)) / 1000
                         or (time.monotonic() - t0),
        load_duration_s=0.0,   # llama-server loads once at startup, not per-request
        raw=payload,
    )


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
