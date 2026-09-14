"""Money rounding for the billing pipeline.

THE SPEC, from the billing agreement: amounts are rounded HALF UP.
A half-cent always rounds away from zero, so 2.5 -> 3 and 3.5 -> 4.

This is deliberate and is not banker's rounding. Python's built-in round()
rounds half to EVEN, which would give 2.5 -> 2, and that is why this module
does not use it.
"""
from decimal import ROUND_HALF_UP, Decimal


def round_half_up(x):
    """Round x half up, per the billing spec."""
    return int(Decimal(str(x)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
