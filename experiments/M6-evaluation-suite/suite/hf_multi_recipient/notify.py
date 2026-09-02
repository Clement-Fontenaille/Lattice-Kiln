"""notify() takes a single recipient string. The task: also accept a list of
recipients - without breaking the existing single-string callers."""

SENT = []          # one (recipient, msg) tuple per delivery


def notify(to, msg):
    SENT.append((to, msg))
    return f"sent to {to}"
