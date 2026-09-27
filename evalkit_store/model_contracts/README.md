# Model contracts — the chat template and token table per model

Queue item **A3**. On vLLM and llama.cpp the chat template is ours to supply,
where Ollama supplied one for us. These are the official templates, taken from
each model's own repository, not authored here.

| directory | HF repo | revision | template came from |
|---|---|---|---|
| `nemotron3-nano-4b/` | `nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16` | `dfaf35de` | `chat_template.jinja` |
| `nemotron-nano-9b-v2/` | `nvidia/NVIDIA-Nemotron-Nano-9B-v2` | `6533e8de` | `tokenizer_config.json:chat_template` |
| `qwen2.5-coder-7b-instruct/` | `Qwen/Qwen2.5-Coder-7B-Instruct` | `c03e6d35` | `tokenizer_config.json:chat_template` |

Each directory holds `chat_template.jinja`, `tokenizer_config.json`,
`special_tokens.json` and `provenance.json` (repo, revision, source, the Ollama
model it corresponds to, fetch time).

**Use these verbatim.** Ollama's renderer for the 4B turned out to be a
byte-identical transcription of NVIDIA's own template; reading the source first
would have saved a week. The same discipline applies on the next backend.

## Not yet done

A3's done-when also requires that a prompt rendered from these templates matches
the official rendering by token count on four message shapes, in the style of
`experiments/M6-evaluation-suite/reconstruct_ollama_prompt.py`. **That
verification has not been run.** These files are the inputs to it, not the
result of it.

## One thing the fetch settled on the way past

The 9B's own template emits its tool surface as:

    <AVAILABLE_TOOLS>[ ... ]</AVAILABLE_TOOLS>
    <TOOLCALL>[{"name": ..., "arguments": ...}]</TOOLCALL>

Angle-bracketed, and spelled `TOOLCALL`. `50-findings/15` records a probe of
`[AVAILABLE_TOOLS]` and `[TOOL_CALLS]` -- square-bracketed, and spelled
`TOOL_CALLS` -- concluding they were "dead in use". Those are not the same
tokens. Queue item **A10** is the addendum that says so; this is the primary
source for it. Nothing is edited in `50-findings/15` -- it is append-only.
