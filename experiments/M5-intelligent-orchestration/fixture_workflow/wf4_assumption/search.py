def find(items, target):
    """Return the index of target in items, or -1 if absent."""
    for i, x in enumerate(items):
        if x == target:
            return i
    return -1
