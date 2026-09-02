# to_json wraps json.dumps and chokes on our value types.
import json


def to_json(obj):
    return json.dumps(obj)
