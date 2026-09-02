"""load() crashes when a value is not an integer string. The task: don't crash on
that - but a genuinely broken input (e.g. raw is not a mapping) must still
surface, not be silently swallowed."""


def load(raw):
    return {k: int(v) for k, v in raw.items()}
