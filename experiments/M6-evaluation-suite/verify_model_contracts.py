"""Render the official chat templates ourselves and check we match the official path (A3).

    python verify_model_contracts.py

The sibling of reconstruct_ollama_prompt.py, one layer over. That script
reconstructed Ollama's Go renderer for the 4B and matched it against the live
prompt by token count. On vLLM and llama.cpp the template is OURS to supply, so
the question moves: given the official template, verbatim from
evalkit_store/model_contracts/, does the prompt we render equal the prompt the
model's own tooling renders?

Two renderings per model per message shape:

    ours      a plain jinja2 environment configured here, independently --
              the renderer this project would use to record and hash the
              prompt it supplies (backends.template_ref = "client-supplied")
    official  transformers.utils.chat_template_utils.render_jinja_template, the
              code path apply_chat_template uses, with the special tokens from
              the model's own tokenizer_config.json

and, for the 4B only, a third: reconstruct_ollama_prompt.render(), the Python
transcription of Ollama's renderer, against the official template -- the
"byte-identical transcription of NVIDIA's own template" claim, checked.

MATCH CRITERION. Byte-identical rendered text. That implies equal token counts
under any tokenizer, which is stronger than the done-when asks. Token counts
are printed only where the model's tokenizer.json is present in its contract
directory; it is not part of the fetched contract, and huggingface.co is not
reachable from every environment. A count that was not computed is never
printed as if it were.

The four shapes are reconstruct_ollama_prompt's CASES, with roles.TOOLS.
Template variables are left at their defaults (enable_thinking etc. unset), and
add_generation_prompt is True, as a serving stack would render a request.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import jinja2
from jinja2.sandbox import ImmutableSandboxedEnvironment

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONTRACTS = ROOT / "evalkit_store" / "model_contracts"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "M4-ephemeral-processors"))
from reconstruct_ollama_prompt import CASES, render as ollama_render  # noqa: E402

MODELS = ["nemotron3-nano-4b", "nemotron-nano-9b-v2", "qwen2.5-coder-7b-instruct"]
SPECIAL = ("bos_token", "eos_token", "unk_token", "pad_token")


# --------------------------------------------------------------- ours

def _tojson(x, indent=None, separators=None, sort_keys=False, ensure_ascii=False):
    # Templates expect JSON as Python's json writes it, not jinja2's built-in
    # tojson, which HTML-escapes < > & ' -- wrong for a prompt.
    return json.dumps(x, ensure_ascii=ensure_ascii, indent=indent,
                      separators=separators, sort_keys=sort_keys)


def _raise(msg):
    raise jinja2.exceptions.TemplateError(msg)


def render_ours(template: str, messages, tools, special: dict) -> str:
    env = ImmutableSandboxedEnvironment(trim_blocks=True, lstrip_blocks=True,
                                        extensions=["jinja2.ext.loopcontrols"])
    env.filters["tojson"] = _tojson
    env.globals["raise_exception"] = _raise
    env.globals["strftime_now"] = lambda fmt: datetime.now().strftime(fmt)
    return env.from_string(template).render(
        messages=messages, tools=tools, add_generation_prompt=True, **special)


# --------------------------------------------------------------- official

def render_official(template: str, messages, tools, special: dict) -> str:
    from transformers.utils.chat_template_utils import render_jinja_template
    out = render_jinja_template(conversations=[messages], tools=tools,
                                chat_template=template,
                                add_generation_prompt=True, **special)
    # Returns (rendered, generation_indices) in current transformers.
    rendered = out[0] if isinstance(out, tuple) else out
    return rendered[0] if isinstance(rendered, list) else rendered


# --------------------------------------------------------------- shared

def _special(model: str) -> dict:
    tc = json.loads((CONTRACTS / model / "tokenizer_config.json").read_text(encoding="utf-8"))
    out = {}
    for k in SPECIAL:
        v = tc.get(k)
        out[k] = v.get("content") if isinstance(v, dict) else v
    return out


def _counter(model: str):
    p = CONTRACTS / model / "tokenizer.json"
    if not p.is_file():
        return None
    from tokenizers import Tokenizer
    tok = Tokenizer.from_file(str(p))
    return lambda s: len(tok.encode(s, add_special_tokens=False).ids)


def _first_diff(a: str, b: str) -> str:
    i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
    return f"first difference at char {i}: {a[max(0, i-30):i+30]!r} vs {b[max(0, i-30):i+30]!r}"


def main() -> int:
    ok = True
    for model in MODELS:
        tmpl = (CONTRACTS / model / "chat_template.jinja").read_text(encoding="utf-8")
        prov = json.loads((CONTRACTS / model / "provenance.json").read_text(encoding="utf-8"))
        special, count = _special(model), _counter(model)
        print(f"{model}  ({prov['hf_repo']} @ {prov['hf_revision'][:8]})")
        for label, msgs, tools in CASES:
            ours = render_ours(tmpl, msgs, tools, special)
            off = render_official(tmpl, msgs, tools, special)
            same = ours == off
            ok &= same
            toks = (f" | tokens ours {count(ours)} official {count(off)}" if count
                    else " | tokens: not computed (no tokenizer.json)")
            print(f"  {label:24} ours {len(ours):>5} ch | official {len(off):>5} ch | "
                  f"{'BYTE-IDENTICAL' if same else 'DIFFER'}{toks}")
            if not same:
                print("      " + _first_diff(ours, off))
        if model == "nemotron3-nano-4b":
            print("  -- Ollama's renderer (reconstruct_ollama_prompt.render) vs the "
                  "official template, recorded, not part of the pass:")
            for label, msgs, tools in CASES:
                oll = ollama_render(msgs, tools)
                off = render_official(tmpl, msgs, tools, special)
                print(f"  {label:24} ollama {len(oll):>5} ch | official {len(off):>5} ch | "
                      + ("BYTE-IDENTICAL" if oll == off else "DIFFER  " + _first_diff(oll, off)))
        print()
    print("OUR RENDERING MATCHES THE OFFICIAL ONE on every model and shape"
          if ok else "MISMATCH -- the differing case shows where")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
