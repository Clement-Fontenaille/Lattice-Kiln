"""withdraw() does no validation. The task: add it - but do not over-reject:
withdrawing the exact balance is legal, and a zero withdrawal is a no-op, not an
error."""


def withdraw(acct, amt):
    acct["balance"] -= amt
    return acct["balance"]
