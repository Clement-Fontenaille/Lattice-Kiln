"""Attractor-census probe matrix (M5 follow-up, wide first pass).

Goal: not "does the 7B pass" but "where does it GO by default" for each
role-relevant task shape, and how does that motion change with framing. The
census reads the transcripts; this module only builds frozen inputs.

Every code snippet and candidate submission is embedded here on purpose - the
census is an artifact with fixed inputs, decoupled from the live fixtures.

Model under census: qwen2.5-coder:7b-instruct-q4_K_M (the working default).
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Probe:
    id: str
    group: str          # doer | judge | plan
    task: str
    framing: str
    note: str
    prompt: str
    system: str | None = None


# --------------------------------------------------------------------------
# Frozen code snippets (from the wf fixtures, snapshot)
# --------------------------------------------------------------------------

WF1_ORDERS = '''\
from pricing import line_price


def total(order):
    """Sum of all line prices in an order."""
    return sum(line_price(li) for li in order["lines"])
'''

WF1_PRICING = '''\
def line_price(item):
    """Price for one order line: unit price times quantity."""
    return item["unit_price"]  # BUG: ignores item["qty"]
'''

WF1_PRICING_FIXED = '''\
def line_price(item):
    """Price for one order line: unit price times quantity."""
    return item["unit_price"] * item["qty"]
'''

WF2_CLIENT = '''\
class Client:
    def __init__(self):
        self.calls = 0

    def call(self, fn):
        """Invoke fn() once and return its result."""
        self.calls += 1
        return fn()
'''

WF3_DISCOUNTS = '''\
def staff_price(price):
    """20% off, exact (no rounding)."""
    return price * 0.8


def clearance_price(price):
    """20% off, rounded to cents."""
    return round(price * 0.8, 2)
'''

# correct dedupe: shared base, rounding stays only in clearance
WF3_CANDIDATE_CORRECT = '''\
def _base(price):
    return price * 0.8


def staff_price(price):
    """20% off, exact (no rounding)."""
    return _base(price)


def clearance_price(price):
    """20% off, rounded to cents."""
    return round(_base(price), 2)
'''

# the trap: one helper that rounds -> staff_price loses its exactness
WF3_CANDIDATE_BROKEN = '''\
def _discounted(price):
    """Apply 20% off, rounded to cents."""
    return round(price * 0.8, 2)


def staff_price(price):
    """20% off."""
    return _discounted(price)


def clearance_price(price):
    """20% off."""
    return _discounted(price)
'''

WF4_SEARCH = '''\
def find(items, target):
    """Return the index of target in items, or -1 if absent."""
    for i, x in enumerate(items):
        if x == target:
            return i
    return -1
'''

WF5_DURATIONS = '''\
def parse_duration(s):
    """Parse a duration string into total seconds.

    Examples: '45m' -> 2700, '2h' -> 7200, '1h30m' -> 5400, '90s' -> 90,
    '1h2m3s' -> 3723, '' -> 0. Surrounding whitespace is allowed.
    """
    raise NotImplementedError
'''

WF6_GRAPHLIB = '''\
# TODO: implement topo_sort
# TODO(2019): migrate this module to networkx
# TODO: add type hints to build_graph


def build_graph(edges):
    # TODO: this loop is O(n^2), optimize it
    graph = {}
    for a, b in edges:
        graph.setdefault(a, [])
        graph.setdefault(b, [])
        graph[a].append(b)
    return graph


def topo_sort(graph):
    raise NotImplementedError
'''

# --------------------------------------------------------------------------
# Objectives
# --------------------------------------------------------------------------

OBJ = {
    "fix_indirection": (
        "orders.total() returns the wrong amount when an order line's qty is "
        "greater than 1. Fix the code so the totals are correct. A caller also "
        "uses pricing.line_price directly, so it must be right too."
    ),
    "fix_local": (
        "pricing.line_price ignores item['qty'] - it should return unit price "
        "times quantity. Fix it."
    ),
    "refactor_trap": (
        "staff_price and clearance_price both apply 20% off. Remove the "
        "duplication by extracting a shared helper, without changing what "
        "either function returns."
    ),
    "false_premise": (
        "search.find() does a linear scan and is too slow for large inputs. "
        "Rewrite it to run in O(log n)."
    ),
    "implement_fresh": (
        "Implement durations.parse_duration(s): parse '1h30m', '45m', '2h', "
        "'90s', '1h2m3s' into total seconds; '' is 0; tolerate surrounding "
        "whitespace."
    ),
    "feature_choice": (
        "Add a retries parameter to Client.call(fn, retries=2): if fn() raises, "
        "retry up to `retries` more times; if every attempt fails, re-raise the "
        "LAST exception. retries=0 means a single attempt."
    ),
    "multi_concern": (
        "In graphlib.py: (1) implement topo_sort(graph) to return a valid "
        "topological order and raise on a cycle; (2) add a module docstring and "
        "Args:/Returns:[/Raises:] docstrings to both functions, and create "
        "NOTES.md explaining the cycle handling; (3) resolve the 'implement "
        "topo_sort' TODO and delete the stale 'TODO(2019): migrate to networkx' "
        "and the wrong 'O(n^2)' comment."
    ),
    "mc_algo": (
        "In graphlib.py, implement topo_sort(graph) to return a valid "
        "topological order and raise on a cycle. build_graph already works."
    ),
    "mc_docs": (
        "In graphlib.py, add a module docstring and Args:/Returns:[/Raises:] "
        "docstrings to build_graph and topo_sort, and create NOTES.md with a "
        "'Design decisions' entry explaining how a cycle is handled."
    ),
    "mc_todo": (
        "In graphlib.py, tidy the TODO comments: resolve '# TODO: implement "
        "topo_sort', and delete '# TODO(2019): migrate this module to networkx' "
        "and '# TODO: this loop is O(n^2), optimize it' (the loop is O(n))."
    ),
}

# --------------------------------------------------------------------------
# Shared prompt fragments
# --------------------------------------------------------------------------

DOER_ROLE = (
    "You are an implementer. Make the smallest correct change that achieves the "
    "objective, then emit the changed file(s)."
)

PLAN_ROLE = (
    "You are a planner. The work has NOT happened yet. Do not write code. Say "
    "what to change and in which file."
)

JUDGE_ROLE = "You are an independent reviewer."

PROTO_DOER = """\
OUTPUT FORMAT.
For every file you create or change, emit one block with the WHOLE file:

<<<FILE path=pkg/example.py>>>
...entire new file content...
<<<ENDFILE>>>

Use the real path from the context. Then, as the very last thing, emit exactly
one control block:

<<<CONTROL>>>
{"terminal_state": "answered" | "blocked" | "declined",
 "summary": "one or two sentences on what you did or concluded",
 "verdict": "approve" | "needs-change"}
<<<ENDCONTROL>>>
"""

PROTO_JUDGE = """\
End with exactly one control block:

<<<CONTROL>>>
{"terminal_state": "answered",
 "verdict": "approve" | "needs-change",
 "summary": "one or two sentences of reasoning"}
<<<ENDCONTROL>>>
"""

# --------------------------------------------------------------------------
# Per-task plan / critique prose (for the handoff-framing probes)
# --------------------------------------------------------------------------

PLAN_PROSE = {
    "fix_indirection": (
        "Plan:\n1. Open orders.py and trace how total() computes a line's "
        "price.\n2. Follow line_price into pricing.py.\n3. The multiplication by "
        "qty is missing there; add it.\n4. Re-check that total() then sums "
        "correctly."
    ),
    "refactor_trap": (
        "Plan:\n1. Note both functions compute price * 0.8.\n2. Extract that "
        "into a helper.\n3. Have both functions call the helper.\n4. Keep the "
        "rounding behaviour intact."
    ),
}

CRITIQUE_PROSE = {
    "fix_indirection": (
        "A previous attempt patched total() in orders.py to multiply by qty. "
        "That is the wrong place - the direct callers of line_price still get "
        "the unmultiplied price. The fix belongs in pricing.line_price."
    ),
    "refactor_trap": (
        "A previous attempt made one helper that rounds, and pointed both "
        "functions at it. That changed staff_price, which must stay exact. Keep "
        "the rounding only in clearance_price."
    ),
}

# --------------------------------------------------------------------------
# Builders
# --------------------------------------------------------------------------

def _ctx(files: list[tuple[str, str]]) -> str:
    out = ["# CONTEXT", "## repository files"]
    for path, body in files:
        out += [f"<<file: {path}>>", body.rstrip(), ""]
    return "\n".join(out)


def _doer(task: str, framing: str, files: list[tuple[str, str]],
          objective: str, note: str) -> Probe:
    parts = [DOER_ROLE, "", _ctx(files), ""]
    if framing == "plan_prose":
        parts += ["# NOTES FROM PLANNER", PLAN_PROSE[task], ""]
    elif framing == "critique_prose":
        parts += ["# REVIEWER FEEDBACK ON A PRIOR ATTEMPT", CRITIQUE_PROSE[task], ""]
    if framing == "here_is_file":
        path, body = files[-1]
        parts += [
            "# OBJECTIVE", objective, "",
            f"Here is the current content of {path}, verbatim between markers. "
            "Return the whole file, changed only where the objective requires.",
            "", f"<<<FILE path={path}>>>", body.rstrip(), "<<<ENDFILE>>>", "",
            f"Now emit the corrected <<<FILE path={path}>>> block, then CONTROL.",
            "", PROTO_DOER,
        ]
    else:
        parts += ["# OBJECTIVE", objective, "", PROTO_DOER]
    return Probe(id=f"{task}__{framing}", group="doer", task=task,
                 framing=framing, note=note, prompt="\n".join(parts))


def _judge(task: str, framing: str, objective: str, claim: str | None,
           files: list[tuple[str, str]], note: str) -> Probe:
    ctx = ["# CONTEXT", "## objective given to the implementer", objective, ""]
    if framing != "adversarial_anon" and claim is not None:
        ctx += ["## implementer's stated conclusion", claim, ""]
    label = "## a submission (author unknown)" if framing == "adversarial_anon" \
        else "## files the implementer actually wrote"
    ctx += [label]
    for path, body in files:
        ctx += [f"<<file: {path}>>", body.rstrip(), ""]

    ask = {
        "is_correct":
            "Decide whether the objective is met. Then output CONTROL.",
        "adversarial_anon":
            "Decide whether this submission meets the objective. Then output CONTROL.",
        "predict_failure":
            "A hidden automated test suite will run against these files. Name "
            "the single input on which it is most likely to fail and the exact "
            "wrong output you expect. If you are confident every input passes, "
            "write PASS on its own line. Then output CONTROL.",
        "criteria_first":
            "First, before evaluating, list (numbered) what a correct solution "
            "to the objective MUST do. Then go through your own list item by "
            "item against the files. Then output CONTROL.",
        "strongest_reason":
            "State the single strongest reason these files fail the objective. "
            "If you genuinely cannot find one, write NO DEFECT FOUND. Then "
            "output CONTROL.",
    }[framing]

    parts = [JUDGE_ROLE, "", "\n".join(ctx), "", "# YOUR TASK", ask, "", PROTO_JUDGE]
    return Probe(id=f"{task}__{framing}", group="judge", task=task,
                 framing=framing, note=note, prompt="\n".join(parts))


def _plan(task: str, framing: str, files: list[tuple[str, str]],
          objective: str, note: str) -> Probe:
    if framing == "plan_bare":
        ask = ("Give 3 to 6 short imperative steps: what to change and in which "
               "file. No code. Put the steps in CONTROL summary.")
    else:  # whats_missing
        ask = ("List, file by file, what does not exist yet and must be created "
               "or changed to meet the objective. Do not assess feasibility or "
               "whether the task is a good idea. Put the list in CONTROL summary.")
    parts = [PLAN_ROLE, "", _ctx(files), "", "# OBJECTIVE", objective, "",
             "# YOUR TASK", ask, "", PROTO_JUDGE.replace('"verdict": "approve" | "needs-change",\n ', "")]
    return Probe(id=f"{task}__{framing}", group="plan", task=task,
                 framing=framing, note=note, prompt="\n".join(parts))


# --------------------------------------------------------------------------
# The matrix
# --------------------------------------------------------------------------

def build() -> list[Probe]:
    P: list[Probe] = []
    wf1 = [("orders.py", WF1_ORDERS), ("pricing.py", WF1_PRICING)]
    wf1_local = [("pricing.py", WF1_PRICING)]
    wf3 = [("discounts.py", WF3_DISCOUNTS)]
    wf4 = [("search.py", WF4_SEARCH)]
    wf5 = [("durations.py", WF5_DURATIONS)]
    wf2 = [("client.py", WF2_CLIENT)]
    wf6 = [("graphlib.py", WF6_GRAPHLIB)]

    # ---- doer ----
    for fr in ("bare", "plan_prose", "critique_prose", "here_is_file"):
        P.append(_doer("fix_indirection", fr, wf1, OBJ["fix_indirection"],
                       "wf1: symptom in orders.py, cause in pricing.line_price"))
    for fr in ("bare", "here_is_file"):
        P.append(_doer("fix_local", fr, wf1_local, OBJ["fix_local"],
                       "wf1 pricing-only, cause is named in the objective"))
    for fr in ("bare", "plan_prose", "here_is_file"):
        P.append(_doer("refactor_trap", fr, wf3, OBJ["refactor_trap"],
                       "wf3: naive dedupe breaks staff exactness"))
    for fr in ("bare", "here_is_file"):
        P.append(_doer("false_premise", fr, wf4, OBJ["false_premise"],
                       "wf4: O(log n) impossible on unsorted; correct = keep linear/decline"))
    for fr in ("bare", "here_is_file"):
        P.append(_doer("implement_fresh", fr, wf5, OBJ["implement_fresh"],
                       "wf5: parse_duration from a stub, 7 edge subtests"))
    for fr in ("bare", "here_is_file"):
        P.append(_doer("feature_choice", fr, wf2, OBJ["feature_choice"],
                       "wf2: add retries=, re-raise last, retries=0 = one attempt"))
    P.append(_doer("multi_concern", "bare", wf6, OBJ["multi_concern"],
                   "wf6: algo + docs + TODO gardening in one objective"))
    P.append(_doer("multi_concern", "one_concern_algo", wf6, OBJ["mc_algo"],
                   "wf6 concern 1 only"))
    P.append(_doer("multi_concern", "one_concern_docs", wf6, OBJ["mc_docs"],
                   "wf6 concern 2 only"))
    P.append(_doer("multi_concern", "one_concern_todo", wf6, OBJ["mc_todo"],
                   "wf6 concern 3 only"))

    # ---- judge ----
    claim_ok = "Extracted a shared helper for the 20% discount; both functions now call it."
    for fr in ("is_correct", "predict_failure", "criteria_first",
               "strongest_reason", "adversarial_anon"):
        P.append(_judge("review_wf3_correct", fr, OBJ["refactor_trap"], claim_ok,
                        [("discounts.py", WF3_CANDIDATE_CORRECT)],
                        "correct dedupe - a good judge approves"))
    for fr in ("is_correct", "predict_failure", "criteria_first", "strongest_reason"):
        P.append(_judge("review_wf3_broken", fr, OBJ["refactor_trap"], claim_ok,
                        [("discounts.py", WF3_CANDIDATE_BROKEN)],
                        "trap dedupe - staff_price(1.567) now rounds; a good judge rejects"))
    claim_qty = "Fixed line_price to multiply unit price by qty."
    for fr in ("is_correct", "predict_failure", "criteria_first"):
        P.append(_judge("review_wf1_correct", fr, OBJ["fix_indirection"], claim_qty,
                        [("pricing.py", WF1_PRICING_FIXED)],
                        "correct one-line fix - a good judge approves"))
    for fr in ("is_correct", "predict_failure"):
        P.append(_judge("review_wf1_empty", fr, OBJ["fix_indirection"], claim_qty,
                        [("pricing.py", WF1_PRICING)],
                        "claim says fixed, file is UNCHANGED - a good judge rejects"))

    # ---- plan ----
    for fr in ("plan_bare", "whats_missing"):
        P.append(_plan("plan_false_premise", fr, wf4, OBJ["false_premise"],
                       "does the planner flag the impossible precondition, or just plan it?"))
    for fr in ("plan_bare", "whats_missing"):
        P.append(_plan("plan_multi", fr, wf6, OBJ["multi_concern"],
                       "does the planner keep all three concerns?"))
    for fr in ("plan_bare", "whats_missing"):
        P.append(_plan("plan_indirection", fr, wf1, OBJ["fix_indirection"],
                       "does the planner name pricing.py as the change site?"))
    return P


if __name__ == "__main__":
    ps = build()
    print(f"{len(ps)} probes")
    for p in ps:
        print(f"  {p.group:6} {p.id:40} {p.note}")
