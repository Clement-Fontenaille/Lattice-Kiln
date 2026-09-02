# wf6_multi

Three concerns in one task:

1. **Algorithmics** — implement `topo_sort(graph)` (Kahn's algorithm or DFS),
   raising on a cycle. `build_graph` already works.
2. **Documentation** — module docstring; `Args:`/`Returns:` on `build_graph`;
   `Args:`/`Returns:`/`Raises:` on `topo_sort`; a `NOTES.md` "Design decisions"
   entry explaining the cycle-handling choice.
3. **TODO gardening** — resolve `# TODO: implement topo_sort`; delete the
   stale `# TODO(2019): migrate ... to networkx` and the wrong
   `# TODO: this loop is O(n^2)` (it is O(n)).

Scored separately: `SUBTESTS` (gates pass), `DOCSCORE`, `TODOSCORE` (quality
signals). Probes whether an arm drops the secondary concerns while carrying the
algorithm work.

**Discriminator:** `DOCSCORE` and `TODOSCORE` staying at 0 while `SUBTESTS` rises — an arm that drops the secondary concerns under load.
