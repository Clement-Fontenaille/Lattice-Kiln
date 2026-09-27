"""Self-test for waiver families and waiver ids (A15). No store, no model.

    python evalkit/test_waivers.py

Checks, each against the code in setup_key.py:
  1. a two-member family behaves exactly as the old pair rule, on every
     pairing drawn from a pool of values;
  2. a three-member family admits all three pairings, and nothing outside it;
  3. a one-member or empty family admits nothing;
  4. a family for arm_sha does not admit a cell differing in any OTHER field
     (compatible() still requires those to match), and a family for one field
     does not waive another field;
  5. load_waivers(): with no ids, exactly the id-less entries, in file order --
     what every caller loaded before ids existed; a named id adds its entries;
     an unknown id raises.
"""
from __future__ import annotations

import itertools
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from setup_key import Cell, _waived, compatible, load_waivers  # noqa: E402


def _old_waived(field_name, x, y, waivers) -> bool:
    """The rule before A15, verbatim."""
    for w in (waivers or []):
        if w.get("field") != field_name:
            continue
        if {x, y} == set(w.get("equivalent", [])):
            return True
    return False


def _cell(**kw) -> Cell:
    base = dict(fixture_sha="f0", task="t", arm="judge_caveat", arm_sha="A",
                prompt_sha="P", backend="ollama", model="m", judge_format="decision_first",
                params='{"protocol": "tools"}')
    base.update(kw)
    return Cell(**base)


FAILS: list[str] = []


def check(cond: bool, what: str) -> None:
    print(f"  {'ok  ' if cond else 'FAIL'} {what}")
    if not cond:
        FAILS.append(what)


def main() -> int:
    pool = ["A", "B", "C", "D"]

    print("1. two-member family == the old pair rule")
    w2 = [{"field": "arm_sha", "equivalent": ["A", "B"]}]
    same = all(_waived("arm_sha", x, y, w2) == _old_waived("arm_sha", x, y, w2)
               for x, y in itertools.product(pool, pool) if x != y)
    check(same, "every distinct pairing from A..D agrees with the old rule")
    check(_waived("arm_sha", "A", "B", w2) and _waived("arm_sha", "B", "A", w2),
          "A~B both ways")
    check(not _waived("arm_sha", "A", "C", w2), "A~C refused")
    check(not _waived("arm_sha", "A", "A", w2) and not _old_waived("arm_sha", "A", "A", w2),
          "x==y is not a waiver, old or new")

    print("2. three-member family admits all three pairings")
    w3 = [{"field": "arm_sha", "equivalent": ["A", "B", "C"]}]
    check(all(_waived("arm_sha", x, y, w3) for x, y in itertools.permutations("ABC", 2)),
          "A~B, A~C, B~C in both directions")
    check(not any(_waived("arm_sha", x, "D", w3) for x in "ABC"), "nothing admits D")
    check(not _old_waived("arm_sha", "A", "C", w3),
          "(the old rule refused these -- the reason for families)")

    print("3. degenerate families admit nothing")
    for fam in ([], ["A"], ["A", "A"]):
        w = [{"field": "arm_sha", "equivalent": fam}]
        check(not any(_waived("arm_sha", x, y, w) for x, y in itertools.product(pool, pool)),
              f"equivalent={fam}")
    check(not _waived("arm_sha", "A", "B", [{"field": "arm_sha"}]), "no equivalent key")

    print("4. an arm_sha family cannot admit a difference in any other field")
    a = _cell(arm_sha="A")
    check(compatible(a, _cell(arm_sha="B"), w3)[0], "arm_sha A vs B, all else equal: admitted")
    others = {"fixture_sha": "f1", "task": "u", "arm": "judge_bypass", "prompt_sha": "Q",
              "backend": "llamacpp", "model": "other", "judge_format": "reason_first",
              "params": '{"protocol": "markers"}'}
    for field, val in others.items():
        ok, why = compatible(a, _cell(arm_sha="B", **{field: val}), w3)
        check(not ok and why.startswith(field), f"arm_sha waived but {field} differs: refused ({why[:40]})")
    wp = [{"field": "prompt_sha", "equivalent": ["A", "B", "C"]}]
    check(not compatible(a, _cell(arm_sha="B"), wp)[0], "a prompt_sha family does not waive arm_sha")

    print("5. load_waivers: default unchanged, ids opt-in, unknown ids refused")
    entries = [{"field": "arm_sha", "equivalent": ["A", "B"], "arm": "x"},
               {"id": "fam-1", "field": "arm_sha", "equivalent": ["C", "D"], "arm": "y"},
               {"field": "prompt_sha", "equivalent": ["P", "Q"], "arm": "z"},
               {"id": "fam-2", "field": "arm_sha", "equivalent": ["E", "F"], "arm": "w"}]
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "waivers.json"
        p.write_text(json.dumps({"waivers": entries}), encoding="utf-8")
        check(load_waivers(path=p) == [entries[0], entries[2]],
              "no ids -> exactly the id-less entries, in file order")
        check(load_waivers([], path=p) == [entries[0], entries[2]], "empty id list -> same")
        check(load_waivers(["fam-1"], path=p) == [entries[0], entries[2], entries[1]],
              "named id -> id-less entries plus that family")
        try:
            load_waivers(["fam-9"], path=p)
            check(False, "unknown id raises")
        except ValueError:
            check(True, "unknown id raises")
    real = json.loads((HERE / "waivers.json").read_text(encoding="utf-8"))["waivers"]
    check(load_waivers() == [w for w in real if not w.get("id")],
          "the repo's waivers.json: default load is its id-less entries")

    print(f"\n{'PASS' if not FAILS else 'FAIL'}: {len(FAILS)} failure(s)")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
