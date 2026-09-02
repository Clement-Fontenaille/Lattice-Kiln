"""billing.py - the public helper `calc` should be renamed to `compute`.

Watch out: 'calc' also appears as a substring of another public name, as a
persisted dict key, and in an audit log line - none of those should change.
"""

_AUDIT_LOG = []
LEDGER = {}


def calc(x):
    """Return the billable amount for x."""
    return round(x * 1.2, 2)


def recalc_all(items):
    """Recompute every item - must keep working after the rename."""
    return [calc(i) for i in items]


def post(item_id, x):
    amount = calc(x)
    LEDGER[str(item_id)] = {"calc": amount, "raw": x}   # "calc" is a wire-format key
    _AUDIT_LOG.append(f"calc for {item_id}: {amount}")   # audited log format
    return amount
