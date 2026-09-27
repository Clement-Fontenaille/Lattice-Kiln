# Parse fixtures — real responses for the A1 seam refactor

Nineteen responses taken from `evalkit_store/transcripts/`, chosen to cover
every branch of the client's parse path. They exist so **A1a** — verifying that
routing transport through `backends.py` leaves parsing unchanged — can be done
without a running model.

| case | n | what it exercises |
|---|---|---|
| `native_tool_calls` | 3 | Ollama parsed the call itself; the happy path |
| `json_in_text` | 3 | bare JSON in the content -> `_calls_from_text` |
| `xml_in_text` | 2 | `<tool_call>` / `<function=` -> `_calls_from_xml` |
| `truncated` | 3 | `done_reason: "length"` -> the `Truncated` guard |
| `empty_text` | 3 | no content and no calls -> the empty-response retry |
| `has_thinking` | 2 | a populated `thinking` field alongside content |
| `plain_text` | 3 | prose with no call in it at all |

Each case carries `provenance` (cell, rep, task, model, prompt_sha) so any one
of them can be traced back to the run that produced it.

## The one thing to be careful about

`response_body` is **reassembled from recorded fields, not captured wire
bytes.** The transcript stores `text`, `thinking`, `tool_calls`, `done_reason`
and the token counts; the body here is those fields put back into the shape
Ollama returns them in.

That is faithful enough for its purpose — feeding the same body through the old
and the new code must yield identical results, and it will — but it does **not**
exercise the HTTP layer itself. Streaming, chunk boundaries and header handling
are untested by these fixtures. Those belong to A1b, which needs a live server.

Do not treat a pass here as a pass on A1.

## Why real responses rather than written ones

The `xml_in_text` cases occur twice in 4762 records, and the malformed shapes
are malformed in specific ways — qwen emitting bare JSON where its template
demands `<tool_call>`, quotes unescaped inside file content. A hand-written
fixture reproduces what its author expects a failure to look like, which is the
one thing that has never been the problem here.
