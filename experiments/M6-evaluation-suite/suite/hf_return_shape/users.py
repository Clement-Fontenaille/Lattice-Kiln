"""get_user returns a (name, age) tuple. Callers use index access:
    u = get_user(uid); label = f"{u[0]} ({u[1]})"
The task: also expose an `email`, without breaking those callers."""

_DB = {
    1: {"name": "Ada", "age": 36, "email": "ada@example.com"},
    2: {"name": "Bo", "age": 29, "email": "bo@example.com"},
}


def get_user(uid):
    r = _DB[uid]
    return (r["name"], r["age"])
