"""Thin non-streaming Ollama client for the M4 processor runtime.

Working default per M0 findings-log entry 1: qwen2.5-coder 7B Q4_K_M, num_ctx
<= 16384, fully GPU-resident on the reference host. Stdlib only (urllib).
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any

DEFAULT_MODEL = "qwen2.5-coder:7b-instruct-q4_K_M"
DEFAULT_BASE_URL = "http://localhost:11434"
DEFAULT_NUM_CTX = 16384


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
        d = self.raw.get("eval_duration", 0) / 1e9
        return (self.eval_count / d) if d else 0.0


def generate(prompt: str, *, model: str = DEFAULT_MODEL, base_url: str = DEFAULT_BASE_URL,
             num_ctx: int = DEFAULT_NUM_CTX, temperature: float = 0.2,
             num_predict: int = 1536, timeout_s: float = 600.0,
             system: str | None = None) -> Generation:
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


def health(base_url: str = DEFAULT_BASE_URL, timeout_s: float = 5.0) -> bool:
    try:
        with urllib.request.urlopen(f"{base_url}/api/tags", timeout=timeout_s) as resp:
            return resp.status == 200
    except urllib.error.URLError:
        return False
