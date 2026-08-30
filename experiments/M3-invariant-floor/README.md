# M3 — Invariant Floor (reduced MVP form)

Milestone 3, crossed in the reduced form the execution cadence defines for the
MVP: effect vocabulary (already specified), capability/authority model,
hardcoded deny-list gate, a small provisional human-authored invariant list, and
a human supervising every run. Sequence-check hardening, gate-alter, and the
whole of Milestone 9 — which now also carries the literature-grounding pass — are
deferred and still owed before Milestone 3 counts as complete in its full form.

**Evidence question:** do the enumerated effect types carve cleanly when real
effects flow through the gate, or does the boundary between types blur under use?

Contracts:
- `docs/10-technical/03-capability-authority-model.md`
- `docs/10-technical/04-enforcement-gate.md`
- `docs/10-technical/05-provisional-invariant-list.md` (normative; this dir's
  `invariants.json` is its machine transcription)
- effect types: `docs/10-technical/01-effect-vocabulary.md`

Decomposition + task state: `docs/PROGRESS/M3-invariant-floor.md`.

## What's here now (pre-M4)

Nothing real proposes effects yet — that starts at M4. This directory makes the
floor concrete and testable in isolation so the interface the M4 processor
runtime binds to already exists and is exercised.

| File | Role |
|---|---|
| `invariants.json` | Machine form of the provisional invariant list (schema `m3-invariants/0`): goals, resource ceilings R1–R3, hard constraints H1–H7, allowlists, denylists. |
| `capabilities.py` | Static-grant capability model. `default_capability_sets()` is the human-operator seed; `authorize(actor, effect)` fails closed; `CapabilitySet.revoke()` is immediate and takes no proposal. |
| `gate.py` | The deny-list gate. `Gate.check(effect)` — deterministic, refuse-only, role-independent, fails closed. `check_sequence(...)` — wired-in stub (always passes in v0). `check_run_bounds(...)` — R3. |
| `enforce.py` | The `representability → capability → gate → sequence` pipeline. `submit_effect(effect, actor)` returns a `Verdict`; the first layer to stop the effect is named. |
| `selftest.py` | Drives synthetic effects through all layers; asserts every H/R clause refuses at least once, the gate is deterministic and role-independent, the sequence stub is actually called, and revocation needs no proposal. |

Run the self-test (Windows or WSL):

```
python experiments/M3-invariant-floor/selftest.py
```

Passes on Windows Python and WSL python3.

## Deferred to M4 and beyond

- Wiring the gate into a real processor runtime and letting real effects flow
  (M4) — this is what answers the evidence question and produces the findings-log
  entry.
- Sequence-check hardening (`check_sequence` body), gate-alter, accumulation-stop,
  and the literature-grounding pass against corrigibility / scalable oversight /
  specification gaming / interruptibility work — all Milestone 9.
- Concrete values for the resource ceilings (`N`, `T`, the R1 VRAM math) and the
  list-integrity mechanism — open contracts in the spec docs.
