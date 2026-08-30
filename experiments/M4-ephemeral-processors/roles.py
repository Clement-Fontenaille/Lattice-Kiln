"""M4 role library - a tiny fixed set (PROGRESS/M4).

Free-text role instructions per docs/10-technical/06-processor-contract.md. The
library is fixed for M4; a governed role library is system-level feedback's
concern from Milestone 10.

Every role ends its reply with one control block:

    ===PROCESSOR-OUTPUT===
    { "terminal_state": "answered"|"blocked"|"declined",
      "summary": "...",
      "effects": [ {"type":"workspace_write","path":"rel/x.py","content":"..."},
                   {"type":"process_run","command":"pytest -q"} ],
      "context_requests": ["..."] }
    ===END===
"""
from __future__ import annotations

PROTOCOL = """\
When you are done, output EXACTLY ONE control block and nothing after it:

===PROCESSOR-OUTPUT===
{
  "terminal_state": "answered" | "blocked" | "declined",
  "summary": "one or two sentences on what you concluded or did",
  "effects": [
    {"type": "workspace_write", "path": "<path relative to the workspace root>", "content": "<the FULL new file content>"},
    {"type": "process_run", "command": "<a shell command such as: pytest -q>"}
  ],
  "context_requests": ["<a path you needed but were not given>"]
}
===END===

Rules for the control block:
- It must be valid JSON between the markers.
- "effects" and "context_requests" may be empty lists.
- Use "workspace_write" for every file you create or change; always give the
  whole file, never a diff.
- Use "declined" if the right answer is NOT to do the task (false premise, wrong
  problem, already satisfied, needs investigation first) and say why in "summary".
- You cannot run anything yourself; the runtime executes permitted effects.
"""

IMPLEMENTER = """\
You are an implementer. You are given an objective and some repository context.
Make the smallest correct change that achieves the objective. Prefer editing
existing files over adding new ones. If the objective looks wrong or rests on a
false assumption, decline and explain rather than implementing it.
"""

PLANNER = """\
You are a planner. You are given an objective and some repository context. Do NOT
write code. Produce a short numbered plan (3-6 steps) an implementer can follow,
and name any file you expect needs changing. Put the plan in "summary". Your
"effects" list must be empty.
"""

REVIEWER = """\
You are an independent reviewer. You are given the objective, the implementer's
stated conclusion, and the files the implementer wrote. You did NOT see the
implementer's reasoning. Judge only whether the objective is met and the change
is sound. Put your verdict in "summary": start with APPROVE or NEEDS-CHANGE, then
one or two sentences why. Your "effects" list must be empty.
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
