"""rect_area is correct for rectangles. The bug report blames it for triangles,
but it is describe() (in report.py) that calls rect_area for every shape."""


def rect_area(s):
    return s["w"] * s["h"]
