# TODO: implement topo_sort
# TODO(2019): migrate this module to networkx
# TODO: add type hints to build_graph


def build_graph(edges):
    # TODO: this loop is O(n^2), optimize it
    graph = {}
    for a, b in edges:
        graph.setdefault(a, [])
        graph.setdefault(b, [])
        graph[a].append(b)
    return graph


def topo_sort(graph):
    raise NotImplementedError
