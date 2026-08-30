"""M4 role library - a tiny fixed set (PROGRESS/M4).

Free-text role instructions per docs/10-technical/06-processor-contract.md. The
library is fixed for M4; a governed role library is system-level feedback's
concern from Milestone 10.

Output format: zero or more FILE blocks, then exactly one CONTROL block last.
File bodies are raw text (never JSON), so triple-quotes and newlines are fine.
"""
from __future__ import annotations

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
               extra: str | None = None) -> str:
    parts = [ROLE_INSTRUCTIONS[role].strip(), "", "# CONTEXT", rendered_context, ""]
    if extra:
        parts += ["# ADDITIONAL INPUT", extra, ""]
    parts += ["# OBJECTIVE", objective, "", PROTOCOL]
    return "\n".join(parts)
