"""A record-processing pipeline. process() is one long function; the task is to
split it into helpers without changing behaviour."""


def process(records):
    # 1. validate
    if not records:
        return {"ok": [], "skipped": [], "total": 0}

    ok = []
    skipped = []
    for rec in records:
        # 2. transform - a missing "amount" key is a data problem, not a crash:
        #    log it and skip the record.
        try:
            amount = rec["amount"]
            name = rec.get("name", "?")
            scaled = amount * 2 if rec.get("double") else amount
            ok.append({"name": name, "value": scaled})
        except KeyError as e:
            skipped.append(f"{rec!r}: missing {e}")
            continue

    # 3. aggregate
    total = sum(item["value"] for item in ok)
    return {"ok": ok, "skipped": skipped, "total": total}
