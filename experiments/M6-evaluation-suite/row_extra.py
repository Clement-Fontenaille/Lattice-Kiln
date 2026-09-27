"""Fields an arm wants on its row, beside the score.

`run_suite.run_task` clears EXTRA before each arm call and copies it onto the
row as `arm_extra` afterwards, only when an arm put something there -- so rows
from arms that never touch it are unchanged. A neutral module because an arm
cannot import run_suite (usually __main__) without importing a second copy.

Beside the score, never folded into it: nothing in run_suite reads these.
"""
from __future__ import annotations

EXTRA: dict = {}
