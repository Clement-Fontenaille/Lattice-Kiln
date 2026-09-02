"""config_for recomputes a fresh dict every call. The task: memoize it so
repeated calls with the same env skip the work - without letting a caller who
mutates a returned dict corrupt the cached value."""

CALLS = []


def config_for(env):
    CALLS.append(env)
    return {"env": env, "debug": env == "dev", "workers": 1 if env == "dev" else 8}
