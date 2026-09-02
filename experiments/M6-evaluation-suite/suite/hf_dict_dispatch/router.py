"""route() dispatches a command string to an action. The task: replace the
if/elif/else chain with a dict dispatch, same behaviour."""


def route(cmd, ctx):
    if cmd == "add":
        ctx["items"].append(ctx["arg"])
        return f"added {ctx['arg']}"
    elif cmd == "remove":
        if ctx["arg"] in ctx["items"]:
            ctx["items"].remove(ctx["arg"])
        return f"removed {ctx['arg']}"
    elif cmd == "audit":
        ctx["audit_count"] += 1          # side effect
        return f"audit #{ctx['audit_count']}"
    elif cmd == "count":
        return str(len(ctx["items"]))
    else:
        return f"unknown command: {cmd}"   # fall-through default
