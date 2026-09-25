"""M4 role library - a tiny fixed set (PROGRESS/M4).

Free-text role instructions per docs/10-technical/06-processor-contract.md. The
library is fixed for M4; a governed role library is system-level feedback's
concern from Milestone 10.

Output format: zero or more FILE blocks, then exactly one CONTROL block last.
File bodies are raw text (never JSON), so triple-quotes and newlines are fine.
"""
from __future__ import annotations

import os

PROTOCOL = """\
OUTPUT FORMAT - follow it exactly.

For every file you create or change, emit one block (give the WHOLE file, never a diff):

<<<FILE path=relative/name.py>>>
...the full new file content...
<<<ENDFILE>>>

Then, as the very last thing in your reply, emit exactly one control block:

<<<CONTROL>>>
{"terminal_state": "answered" | "blocked" | "declined",
 "summary": "one or two sentences on what you concluded or did",
 "verdict": "approve" | "needs-change",
 "run": ["python test_task.py"],
 "context_requests": []}
<<<ENDCONTROL>>>

Rules:
- The CONTROL block must be valid JSON. Keep it short - no file contents inside it.
- "run" and "context_requests" may be empty lists. "run" is optional.
- "verdict" is only for the reviewer role; other roles may omit it.
- terminal_state = "declined" if the right answer is NOT to do the task (false
  premise, wrong problem, already satisfied, needs investigation first) - explain
  in "summary" and emit no FILE blocks.
- You cannot execute anything yourself; the runtime runs permitted commands.
"""

# --------------------------------------------------------------- tools mode
#
# The same contract as PROTOCOL above, expressed as tool definitions instead of
# bespoke markers. Findings 15 measured the marker form degenerating on
# nemotron3-nano-4b -- newlines collapsing to spaces inside a FILE block -- and
# established that "<<<" carries no trained state change in that model's
# vocabulary, while its tuned tool channel emitted the same content with
# newlines correctly escaped.
#
# Two tools cover everything the markers did:
#   write_file(path, content)  <- one FILE block
#   conclude(...)              <- the single CONTROL block
#
# Shapes follow the OpenAI function-calling convention, which is what Ollama's
# per-model RENDERER takes as input and re-serialises into whatever dialect the
# model was actually tuned on.
TOOLS = [
    {"type": "function", "function": {
        "name": "write_file",
        "description": ("Create or replace one file. Give the WHOLE file "
                        "content, never a diff. Call once per file changed."),
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string",
                     "description": "Path relative to the repository root."},
            "content": {"type": "string",
                        "description": "The complete new file content."},
        }, "required": ["path", "content"]}}},
    {"type": "function", "function": {
        "name": "conclude",
        "description": ("Record the outcome and end the exchange. Call this "
                        "once the task is finished, or once you have "
                        "decided not to do it."),
        "parameters": {"type": "object", "properties": {
            "terminal_state": {"type": "string",
                               "enum": ["answered", "blocked", "declined"]},
            "summary": {"type": "string",
                        "description": "One or two sentences on what you "
                                       "concluded or did."},
            "verdict": {"type": "string", "enum": ["approve", "needs-change"],
                        "description": "Reviewer role only; omit otherwise."},
            "run": {"type": "array", "items": {"type": "string"},
                    "description": "Commands for the runtime to execute."},
            "context_requests": {"type": "array", "items": {"type": "string"}},
        }, "required": ["terminal_state", "summary"]}}},
]

# LATTICE_PROTOCOL_VARIANT selects the OUTPUT FORMAT text: v1 is the wording
# every tool-protocol row before 2026-09-25 used, v2 the rework. Both are kept
# because a probe on a synthetic task could not reproduce the failure the rework
# was aimed at -- 4 prose conclusions in 100 runs against the suite's 29% -- so
# the comparison has to happen at suite scale. The text feeds
# adapter_fingerprint(), so the two variants key to different cells and cannot
# pool.
PROTOCOL_TOOLS_V1 = """\
OUTPUT FORMAT - use the provided tools, not prose.

For every file you create or change, call write_file with the path and the
WHOLE new file content (never a diff).

Then call conclude exactly once, as the last thing you do.

Rules:
- conclude is required on every turn, including when you write no files.
- "verdict" is only for the reviewer role; other roles may omit it.
- terminal_state = "declined" if the right answer is NOT to do the task (false
  premise, wrong problem, already satisfied, needs investigation first) -
  explain in "summary" and call write_file zero times.
- You cannot execute anything yourself; the runtime runs permitted commands.
"""

PROTOCOL_TOOLS_V2 = """\
OUTPUT FORMAT

Do the work by calling the tools. Do not describe changes in prose.

write_file takes the path and the WHOLE new file content, never a diff.

Calling conclude ends the exchange. Call it when the task is finished or when
you have decided not to do it -- not before. You may take as many turns as you
need first.

Rules:
- "verdict" is only for the reviewer role; other roles may omit it.
- terminal_state = "declined" if the right answer is NOT to do the task (false
  premise, wrong problem, already satisfied, needs investigation first) -
  explain in "summary" and call write_file zero times.
- You cannot execute anything yourself; the runtime runs permitted commands.
"""

PROTOCOL_VARIANT = os.environ.get("LATTICE_PROTOCOL_VARIANT", "v2")
PROTOCOL_TOOLS = (PROTOCOL_TOOLS_V1 if PROTOCOL_VARIANT == "v1"
                  else PROTOCOL_TOOLS_V2)


IMPLEMENTER = """\
You are an implementer. You are given an objective and some repository context.
Make the smallest correct change that achieves the objective. Prefer editing
existing files over adding new ones. If the objective looks wrong or rests on a
false assumption, decline and explain rather than implementing it.
"""

PLANNER = """\
You are a planner. You are given an objective and some repository context. Do NOT
write code and emit NO FILE blocks. Produce a short numbered plan (3-6 steps) an
implementer can follow, and name any file you expect needs changing. Put the whole
plan in the CONTROL block's "summary". Use terminal_state "answered", or
"declined" if the task should not be done.
"""

REVIEWER = """\
You are an independent reviewer. You are given the objective, the implementer's
stated conclusion, and the files the implementer wrote. You did NOT see the
implementer's reasoning. Judge only whether the objective is met and the change
is sound. Emit NO FILE blocks. Set the CONTROL block's "verdict" to "approve" or
"needs-change", put one or two sentences of reasoning in "summary", and use
terminal_state "answered".
"""

ROLE_INSTRUCTIONS = {
    "implementer": IMPLEMENTER,
    "planner": PLANNER,
    "reviewer": REVIEWER,
}

# role -> capability grants (plain data; processor.py builds the CapabilitySet).
# Keyed to the nine effect types (docs/10-technical/03). Absent type => refused.
ROLE_GRANTS: dict[str, dict[int, dict]] = {
    "implementer": {
        1: {"path_within": "<workspace_root>"},
        2: {"command_allowlist": ["python", "pytest", "ruff", "make", "node", "npm"]},
        4: {},
    },
    "planner": {4: {}},           # may record a plan/proposal; no code, no commands
    "reviewer": {4: {}},          # may record an assessment; no code, no commands
}


def prompt_for(role: str, rendered_context: str, objective: str,
               extra: str | None = None, protocol: str | None = None) -> str:
    """`protocol` overrides the OUTPUT FORMAT section; defaults to markers."""
    parts = [ROLE_INSTRUCTIONS[role].strip(), "", "# CONTEXT", rendered_context, ""]
    if extra:
        parts += ["# ADDITIONAL INPUT", extra, ""]
    parts += ["# OBJECTIVE", objective, "",
              PROTOCOL if protocol is None else protocol]
    return "\n".join(parts)
