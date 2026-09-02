"""dispatch() reaches exporters by name - the only reference to _legacy_export
is the string "legacy" plus the @register decorator."""
import plugins


def dispatch(name, data):
    return plugins.REGISTRY[name](data)
