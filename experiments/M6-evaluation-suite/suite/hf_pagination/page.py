"""page() is meant to take 1-indexed page numbers (page 1 = the first `size`
items). It currently computes start = num * size, so page 1 skips the first
page's worth of items and every page is off by one."""


def page(items, num, size):
    start = num * size
    return items[start:start + size]
