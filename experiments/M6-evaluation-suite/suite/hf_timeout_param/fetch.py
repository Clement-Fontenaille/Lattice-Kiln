"""fetch(url) has no timeout. The task: add fetch(url, timeout=None).
Semantics to get right: None (default) = no timeout, existing callers
unaffected; 0 = a zero budget that times out immediately (NOT 'falsy so
ignore'). URLs in _SLOW exceed any positive-or-zero budget."""

_RESPONSES = {"a.example": "ok-a", "b.example": "ok-b", "slow.example": "ok-slow"}
_SLOW = {"slow.example"}


def fetch(url):
    return _RESPONSES.get(url, "404")
