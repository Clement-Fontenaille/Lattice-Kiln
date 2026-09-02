"""merge() does a shallow {**base, **override}. The task: a proper config merge -
nested dicts merge recursively, a None value in override deletes the key, and
lists replace (not concat)."""


def merge(base, override):
    return {**base, **override}
