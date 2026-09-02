"""count_nodes() is recursive and blows the recursion limit on deep trees.
The task: make it iterative, same results."""


def count_nodes(node):
    """Total number of nodes in a tree of dicts with optional 'children'."""
    if node is None:
        return 0
    total = 1
    for child in node.get("children", []):
        total += count_nodes(child)
    return total
