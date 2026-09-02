"""build() shapes a record into a response dict. The task: add a `tier` field.
Some records predate `tier` and don't carry it - those must default to 'free',
not raise."""


def build(rec):
    return {"id": rec["id"], "name": rec["name"]}
