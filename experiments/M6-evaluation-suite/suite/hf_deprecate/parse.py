"""new_parse is the current implementation. old_parse is the legacy one, kept
for callers that have not migrated. The task: deprecate old_parse - it should
warn, delegate to new_parse, and thus return the same thing."""


def new_parse(s):
    """Split on commas, strip each field, drop empties."""
    return [p.strip() for p in s.split(",") if p.strip()]


def old_parse(s):
    # legacy: raw split, no strip, keeps empty fields
    return s.split(",")
