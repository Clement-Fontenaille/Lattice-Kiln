"""apply() routes every balance change through set_balance, so the guard there
is the only thing stopping a big withdrawal from creating a negative balance."""
from account import set_balance


def apply(acct, delta):
    set_balance(acct, acct["balance"] + delta)


def audit(acct):
    # a downstream invariant that relies on set_balance's guard
    assert acct["balance"] >= 0, "negative balance slipped through"
    return True
