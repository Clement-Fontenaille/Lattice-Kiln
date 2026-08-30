import re

_WS = re.compile(r"[\s_]+")
_BAD = re.compile(r"[^a-z0-9-]")


def slugify(text: str) -> str:
    """Lowercase, collapse whitespace/underscores to single hyphens, drop other
    non-alphanumerics, trim leading/trailing hyphens."""
    s = _WS.sub("-", text.strip().lower())
    s = _BAD.sub("", s)
    return s.strip("-")
