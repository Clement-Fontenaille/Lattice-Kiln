"""describe() calls rect_area for every shape, including triangles. tri_area
already exists and is correct - describe just never dispatches to it."""
from shapes import rect_area


def tri_area(s):
    return s["w"] * s["h"] / 2


def describe(s):
    return f"{s['kind']} area {rect_area(s)}"
