"""Role prompts for the super-pipeline (pipeline_lab).

Design constraints from the M5 follow-up findings:
  - a 7B verdict is systematically approve-biased -> verification bottoms out in
    execution or deterministic rules, never a bare model verdict;
  - the model reverse-engineers criteria from whatever concrete artifact is in
    context -> test synthesis runs with NO candidate code visible;
  - the planner/analyst stance is the only one that catches a false premise ->
    the premise audit uses it and holds decline authority;
  - context diversity (different anchors), not prompt perturbation, is what may
    decorrelate the bias -> the two structural verifiers get disjoint context.

Every prompt asks for a small, rigid output the driver parses deterministically.
"""
from __future__ import annotations

PREMISE_AUDIT = """\
You are a senior engineer auditing whether a task is SOUND to attempt, before
anyone writes code. You have the objective and the current code.

SOUND is the normal case. In particular these are ALL sound:
  - the code currently produces the wrong result in the way the objective
    describes (a real bug to fix);
  - the feature the objective asks for does not exist yet (it will be added);
  - a straightforward refactor or implementation.

Mark UNSOUND only when the objective cannot be satisfied as literally stated:
  (a) the goal is impossible given the code or data - e.g. "make this O(log n)"
      when the data is not ordered;
  (b) the premise about what is broken is itself false - the named bug does not
      exist and the code is already correct;
  (c) the objective is self-contradictory.

"the current code is wrong" is NOT a reason for UNSOUND - that is what a bugfix
task is for.

Also classify the task_type: "bugfix" | "feature" | "refactor" | "perf" | "mixed".

Answer with ONE JSON object, one line, terse (correct_action <= 25 words):
{"sound": true | false, "task_type": "...", "reason": "<one sentence>", "correct_action": "<if unsound only>"}
"""

VIOLATION_INPUT = """\
You said this obligation is VIOLATED by the change. Give the single concrete
input that demonstrates it: write a <= 12-line standalone Python snippet that
imports the code in the working directory, exercises it, and prints
  PROBE PASS   if the obligation actually HOLDS (you were wrong)
  PROBE FAIL: <detail>   if it is genuinely violated
Exit 0 / 1 to match. Output only the snippet, no fences.

OBLIGATION:
"""

TEST_SPEC = """\
You are writing a TEST PLAN from an objective, before any implementation exists.

List the checkable requirements a correct solution MUST satisfy. One per line,
numbered. For each, start the line with a tag:
  [BEHAVIOURAL] - can be checked by calling the code and comparing a value
  [STRUCTURAL]  - about code shape: duplication removed, helper extracted,
                  docstring present, a comment deleted, naming - not a value

Derive them from the OBJECTIVE and the described interface only. Do NOT assume a
particular implementation. Be specific about inputs and expected outputs where
you can. 3 to 8 items.
"""

IMPL_SPEC = """\
You are a planner. The work has NOT happened yet.

From the objective alone, say WHAT to change and in WHICH file - 3 to 6 short
imperative steps. Name functions and files. Do not write code. Do not use past
tense. Put the steps as a numbered list, nothing else.
"""

ALIGNMENT = """\
Here are two INDEPENDENT specifications of the same task: a TEST spec (what will
be checked) and an IMPL spec (what will be done). You do NOT have the code.

Report, as JSON on one line:
{"unverified": ["<impl step with no matching test item>", ...],
 "unplanned": ["<test item with no matching impl step>", ...],
 "contradictions": ["<where the two disagree>", ...],
 "underspecified": true | false}

"underspecified" is true if "unverified" or "unplanned" is non-empty - i.e. the
task cannot be fully checked by the test plan as written.
"""

TEST_IMPL = """\
Write ONE standalone Python test script (stdlib only) that checks the
requirements below against code you have NOT seen.

- Import the public names the objective describes.
- For each requirement, print exactly:  CHECK <short-name> PASS   or   CHECK <short-name> FAIL: <detail>
- Compute expected values yourself from the objective; be careful and explicit.
- At the end print  DONE <passed>/<total>  and sys.exit(0 if all passed else 1).
- No pytest, no frameworks. One file. Output only the file, no fences.

REQUIREMENTS:
"""

PROBE_SYNTH = """\
Write a SHORT standalone Python snippet (stdlib only, <= 15 lines) that checks
this ONE obligation against the code in the working directory by importing it and
calling it. Print exactly  PROBE PASS  or  PROBE FAIL: <detail>  and exit
0/1 accordingly. Output only the snippet, no fences.

OBLIGATION:
"""

STRUCT_VERIFY_A = """\
You are checking ONE obligation against a code change, by reading the diff only.

Answer with one JSON object on one line:
{{"result": "SATISFIED" | "VIOLATED" | "NEEDS-EXECUTION" | "NEEDS-HUMAN",
 "evidence": "<a verbatim line from the diff, or why you cannot tell>"}}

Use NEEDS-EXECUTION if it can only be confirmed by running the code. Use
NEEDS-HUMAN if it is a judgement call (taste, clarity) with no mechanical check.

OBLIGATION:
{obligation}

DIFF:
{diff}
"""

STRUCT_VERIFY_B = """\
You are given the ORIGINAL file(s) and an objective. The change has NOT been made
yet. Describe the MINIMAL change required as a list of concrete edits, one per
line, each as:  <file>::<function-or-region> :: <what must change>

Name only things that genuinely must change. Do not speculate about style.

OBJECTIVE:
{objective}

ORIGINAL:
{original}
"""


def numbered_list(text: str) -> list[str]:
    import re
    out = []
    for ln in (text or "").splitlines():
        m = re.match(r"\s*(?:\d+[.)]|[-*])\s+(.*)", ln)
        if m and len(m.group(1).strip()) > 4:
            out.append(m.group(1).strip())
    return out
