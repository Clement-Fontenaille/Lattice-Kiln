"""Import bridge to the M2 recorder and the M3 enforcement floor.

M4 reuses those modules rather than reimplementing them (PROGRESS/M4 note). If
either needs a change to be usable from a real run, that change is a finding for
its own milestone, not a fork here.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
for _p in (_ROOT / "M2-observability-foundation", _ROOT / "M3-invariant-floor"):
    s = str(_p)
    if s not in sys.path:
        sys.path.insert(0, s)

from event_model import RunRecorder  # noqa: E402,F401
from reconstruct import Run  # noqa: E402,F401
from capabilities import CapabilitySet, default_capability_sets  # noqa: E402,F401
from enforce import submit_effect  # noqa: E402,F401
from gate import Gate  # noqa: E402,F401
