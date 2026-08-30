"""M3 self-test: synthetic effects through the invariant floor.

No real effects flow yet (that is M4). This drives hand-built proposed effects
through capabilities.py / gate.py / enforce.py and asserts:

  - every layer (representability, capability, gate, sequence-stub) stops what it
    should and passes what it should;
  - every hard constraint H1..H7 and every resource ceiling R1..R3 refuses at
    least once (coverage);
  - the gate is deterministic and role-independent;
  - the sequence check is a wired-in stub that is actually called;
  - revocation is immediate and takes no proposal.

    python experiments/M3-invariant-floor/selftest.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from capabilities import default_capability_sets  # noqa: E402
from enforce import submit_effect  # noqa: E402
from gate import Gate  # noqa: E402

WS = "/ws/repo"
_fails: list[str] = []
_clauses_seen: set[str] = set()


def want(cond: bool, msg: str) -> None:
    print(("  ok  " if cond else "  FAIL") + " " + msg)
    if not cond:
        _fails.append(msg)


def eff(t: int, **env):
    e = {"effect_type": t, "envelope": env}
    if "initiated_by" in env:
        e["initiated_by"] = env["initiated_by"]
    return e


def note_refuse(v_or_d) -> str:
    c = getattr(v_or_d, "clause", None)
    if c:
        _clauses_seen.add(c)
    return c or ""


def main() -> None:
    caps = default_capability_sets()
    impl = caps["implementer"]
    reviewer = caps["reviewer"]
    fetcher = caps["fetcher"]
    gate = Gate()

    # -- 1. clean path: implementer edits inside its workspace -> proceed ----
    e_ok = eff(1, workspace_root=WS, target_path=f"{WS}/client/ratelimiter.py", op="modify")
    v = submit_effect(e_ok, impl, gate=gate)
    want(v.proceed, f"in-workspace edit proceeds through all layers (got {v.stopped_by}/{v.reason})")

    # -- 2. representability stops an out-of-workspace write ----------------
    e_esc = eff(1, workspace_root=WS, target_path="/etc/hosts", op="modify")
    v = submit_effect(e_esc, impl, gate=gate)
    want(v.stopped_by == "representability", f"out-of-workspace write stopped at representability (got {v.stopped_by})")
    #    ... and the gate re-checks the boundary anyway (defense in depth = H1)
    d = gate.check(e_esc)
    want(d.refused and d.clause == "H1", f"gate independently refuses the same effect via H1 (got {d.clause})")
    note_refuse(d)

    # -- 3. capability stops network access the implementer was not granted -
    e_net = eff(3, host="pypi.org")
    v = submit_effect(e_net, impl, gate=gate)
    want(v.stopped_by == "capability", f"implementer network access stopped at capability (got {v.stopped_by})")

    # -- 4. a role granted registry egress reaches an allowlisted host ------
    e_reg = eff(3, host="pypi.org", destination_class="registry")
    v = submit_effect(e_reg, fetcher, gate=gate)
    want(v.proceed, f"fetcher -> allowlisted registry proceeds (got {v.stopped_by}/{v.reason})")

    # -- 5. gate (H2) stops a non-allowlisted host that passed capability ---
    e_evil = eff(3, host="evil.example.com", destination_class="registry")
    v = submit_effect(e_evil, fetcher, gate=gate)
    want(v.stopped_by == "gate" and v.clause == "H2", f"non-allowlisted host refused by gate H2 (got {v.stopped_by}/{v.clause})")
    note_refuse(v)

    # -- 6. H3: no in-place trusted-config edit, no automated promotion -----
    d = gate.check(eff(7, config_target="trusted"))
    want(d.refused and d.clause == "H3", f"type-7 targeting trusted config refused H3 (got {d.clause})")
    note_refuse(d)
    want(gate.check(eff(7, config_target="candidate")).passed, "type-7 producing a candidate passes the gate")
    d = gate.check(eff(8))
    want(d.refused and d.clause == "H3", f"promotion (type 8) refused H3 (got {d.clause})")
    note_refuse(d)

    # -- 7. H4: cognition-initiated capability change is refused -----------
    d = gate.check(eff(9, initiated_by="cognition"))
    want(d.refused and d.clause == "H4", f"cognition-initiated type-9 refused H4 (got {d.clause})")
    note_refuse(d)
    want(gate.check(eff(9, initiated_by="runtime")).passed, "runtime-initiated revocation passes the gate")

    # -- 8. H5: no self-modification of the floor (independent of H1) ------
    prot = "experiments/M3-invariant-floor/invariants.json"
    d = gate.check(eff(1, workspace_root="experiments/M3-invariant-floor", target_path=prot, op="modify"))
    want(d.refused and d.clause == "H5",
         f"editing invariants.json refused H5 even when inside a workspace (got {d.clause})")
    note_refuse(d)

    # -- 9. H6: no deletion of observability records ----------------------
    d = gate.check(eff(4, target_path="project/runs/run_abc123/events.jsonl", op="delete"))
    want(d.refused and d.clause == "H6", f"deleting a run's events.jsonl refused H6 (got {d.clause})")
    note_refuse(d)

    # -- 10. H7: host-destructive process execution ---------------------
    for cmd in ("rm -rf /", "sudo apt-get remove python3", "mkfs.ext4 /dev/sda1", "shutdown -h now"):
        d = gate.check(eff(2, command=cmd))
        want(d.refused and d.clause == "H7", f"destructive command refused H7: {cmd!r} (got {d.clause})")
        note_refuse(d)
    want(gate.check(eff(2, command="pytest -q")).passed, "a benign test command passes the gate")
    v = submit_effect(eff(2, command="pytest -q tests/"), impl, gate=gate)
    want(v.proceed, f"implementer running an allowlisted test command proceeds (got {v.stopped_by}/{v.reason})")

    # -- 11. resource ceilings R1 / R2 / R3 -----------------------------
    d = gate.check(eff(6, over_resident_envelope=True))
    want(d.refused and d.clause == "R1", f"over-VRAM invocation refused R1 (got {d.clause})")
    note_refuse(d)
    d = gate.check(eff(6, concurrent_invocations=2))
    want(d.refused and d.clause == "R2", f"second concurrent invocation refused R2 (got {d.clause})")
    note_refuse(d)
    want(gate.check(eff(6, concurrent_invocations=1)).passed, "a single invocation passes R2")
    d = gate.check_run_bounds(effects_realized=200, minutes_elapsed=0.0)
    want(d.refused and d.clause == "R3", f"run hitting the effect ceiling refused R3 (got {d.clause})")
    note_refuse(d)
    want(gate.check_run_bounds(3, 1.0).passed, "a young run within bounds passes R3")

    # -- 12. malformed input fails closed (never a pass) ---------------
    want(gate.check({}).refused, "gate refuses an effect with no effect_type")
    want(gate.check({"effect_type": 99}).refused, "gate refuses an effect_type outside 1..9")
    #    authorize() raises CapabilityError on a bad type; submit_effect catches
    #    it and returns a stopped verdict rather than letting it escape.
    v = submit_effect({"effect_type": 42, "envelope": {}}, impl, gate=gate)
    want(v.stopped_by == "capability" and not v.proceed, "a bad effect_type is stopped, not run")

    # -- 13. unreadable invariant list -> refuse everything ------------
    broken = Gate(HERE / "does-not-exist.json")
    want(broken.check(e_ok).refused, "a gate with no loadable invariant list refuses all effects")

    # -- 14. determinism + role-independence --------------------------
    decs = {(gate.check(e_evil).outcome, gate.check(e_evil).clause) for _ in range(200)}
    want(decs == {("refuse", "H2")}, f"gate.check is deterministic over 200 calls (got {decs})")
    r_impl = gate.check(e_evil, actor=impl)
    r_rev = gate.check(e_evil, actor=reviewer)
    r_none = gate.check(e_evil, actor=None)
    want((r_impl.outcome, r_impl.clause) == (r_rev.outcome, r_rev.clause) == (r_none.outcome, r_none.clause),
         "gate decision does not depend on the proposing actor's role")

    # -- 15. the sequence check is a stub, and it is actually called ---
    s = gate.check_sequence([], e_ok)
    want(s.passed and "stub" in s.reason.lower(), "check_sequence is a wired-in stub that passes in v0")
    called = {"n": 0}
    real = gate.check_sequence
    gate.check_sequence = lambda h, p: (called.__setitem__("n", called["n"] + 1) or real(h, p))  # type: ignore
    submit_effect(e_ok, impl, gate=gate)
    gate.check_sequence = real  # type: ignore
    want(called["n"] == 1, "the enforcement pipeline calls check_sequence on a proceeding effect")

    # -- 16. revocation is immediate and takes no proposal ------------
    ret = impl.revoke()
    want(ret is None and impl.grants == {} and impl.revoked,
         "revoke() clears grants immediately, returns nothing, takes no proposal")
    v = submit_effect(e_ok, impl, gate=gate)
    want(v.stopped_by == "capability", f"a revoked actor can request nothing (got {v.stopped_by})")

    # -- 17. coverage: every clause refused at least once ------------
    expected = {"H1", "H2", "H3", "H4", "H5", "H6", "H7", "R1", "R2", "R3"}
    want(expected <= _clauses_seen, f"every H/R clause exercised (missing: {sorted(expected - _clauses_seen)})")

    print()
    if _fails:
        print(f"SELFTEST FAILED ({len(_fails)} assertion(s))")
        raise SystemExit(1)
    print("SELFTEST PASSED")


if __name__ == "__main__":
    main()
