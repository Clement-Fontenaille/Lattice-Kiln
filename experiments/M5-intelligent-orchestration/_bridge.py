"""Import bridge to the M2 recorder, the M3 floor, and the M4 processor runtime.

M5 reuses all three rather than reimplementing them.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
for _p in (_ROOT / "M2-observability-foundation",
           _ROOT / "M3-invariant-floor",
           _ROOT / "M4-ephemeral-processors"):
    s = str(_p)
    if s not in sys.path:
        sys.path.insert(0, s)

from event_model import RunRecorder  # noqa: E402,F401
from reconstruct import Run  # noqa: E402,F401
from capabilities import CapabilitySet  # noqa: E402,F401
from enforce import submit_effect  # noqa: E402,F401
from gate import Gate  # noqa: E402,F401
from processor import run_processor, _extract  # noqa: E402,F401
from ollama_client import DEFAULT_MODEL, generate, health  # noqa: E402,F401
from context_assembly import assemble  # noqa: E402,F401
