"""A tiny plugin registry. _legacy_export has no direct callers, but it is
registered and reached by name from run.dispatch - it is NOT dead."""

REGISTRY = {}


def register(name):
    def deco(fn):
        REGISTRY[name] = fn
        return fn
    return deco


@register("json")
def _json_export(data):
    return {"format": "json", "rows": len(data)}


@register("legacy")
def _legacy_export(data):
    return {"format": "legacy", "rows": len(data), "v": 1}
