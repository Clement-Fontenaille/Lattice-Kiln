"""set_balance rejects a negative balance. The objective wants that check gone
'because it never fires' - but ledger.apply can drive a balance negative, and
audit() depends on the guard."""


def set_balance(acct, amount):
    if amount < 0:
        raise ValueError("balance may not be negative")
    acct["balance"] = amount
