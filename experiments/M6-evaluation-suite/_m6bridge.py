"""Path wiring for the M6 evaluation suite runner.

Reuses the M2 recorder, the M4 processor runtime, and (optionally) the
loop_lab / pipeline_lab arms.
"""
from __future__ import annotations

import sys
from pathlib import Path

_EXP = Path(__file__).resolve().parent.parent
# order matters: M4 last so its own `_bridge.py` (which wires M2/M3 for
# `processor`) is the one resolved, not M5's same-named module.
for _p in (_EXP / "M2-observability-foundation",
           _EXP / "M3-invariant-floor",
           _EXP / "M4-ephemeral-processors"):
    s = str(_p)
    if s not in sys.path:
        sys.path.insert(0, s)

from event_model import RunRecorder  # noqa: E402,F401
from capabilities import CapabilitySet  # noqa: E402,F401
from gate import Gate  # noqa: E402,F401
from ollama_client import DEFAULT_MODEL, generate, health  # noqa: E402,F401
from context_assembly import assemble  # noqa: E402,F401
from processor import run_processor  # noqa: E402,F401
