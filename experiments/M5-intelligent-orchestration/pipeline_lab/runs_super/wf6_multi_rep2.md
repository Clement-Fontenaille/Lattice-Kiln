# wf6_multi rep2 -> resolved
_baseline (2, 6) -> final (6, 6), 29 calls, 222.6s_

signals: {"premise_unsound": false, "l1_provided_fail": false, "regression": false, "l2_violated": false, "synth_trusted_fail": false, "l2_needs_human": false, "blowout": false, "refactor_unverified": false}
load-bearing: []
open_items: []

OBJECTIVE: In graphlib.py: (1) implement topo_sort(graph) to return a valid topological order and raise on a cycle (build_graph already works); (2) add proper docstrings - a module docstring, Args:/Returns: on build_graph, and Args:/Returns:/Raises: on topo_sort - and create NOTES.md with a 'Design decisions' entry explaining the cycle handling; (3) tidy the TODO comments: resolve the 'implement topo_sort' one, and delete the stale 'TODO(2019): migrate to networkx' and the wrong 'O(n^2)' comment (the loop is O(n)). Make test_task.py's SUBTESTS pass and raise DOCSCORE and TODOSCORE.

## ledger

- **S0-premise** (3c 8.8s): sound=True type=feature votes=[True, True, True] reason=''
- **S1-testspec** (1c 8.5s): 15 items 6B/9S
- **S2-implspec** (2c 10.5s): 10/7 steps, overlap=0.90 disagree=False
- **S3-alignment** (1c 3.1s): advisory: unverified=0 unplanned=0
- **S4-synth** (3c 42.0s): 1/3 valid; checks/suite=3,0,0
- **S5-coding** (12c 122.7s): incumbent comb=3 | impl_a comb=13(sub6) impl_b comb=12(sub6) agree=False -> winner a sub(6, 6) doc(4, 4) todo(3, 3) diff_lines=59 blowout=False
- **S6b-l2** (7c 26.6s): pass,pass,pass,pass,pass b_consistent=True

## transcripts


### S0-premise
```
You are a senior engineer auditing whether a task is SOUND to attempt, before
anyone writes code. You have the objective and the current code.

SOUND is the normal case. In particular these are ALL sound:
  - the code currently produces the wrong result in the way the objective
    describes (a real bug to fix);
  - the feature the objective asks for does not exist yet (it will be added);
  - a straightforward refactor or implementation.

Mark UNSOUND only when the objective cannot be satisfied as literally stated:
  (a) the goal is impossible given the code or data - e.g. "make this O(log n)"
      when the data is not ordered;
  (b) the premise about what is broken is itself false - the na
```
->
```
```json
{"sound": true, "task_type": "feature", "reason": "The objective is to implement a topological sort and add documentation, which is a valid feature request.", "correct_action": ""}
```
```

### S0-premise
```
You are a senior engineer auditing whether a task is SOUND to attempt, before
anyone writes code. You have the objective and the current code.

SOUND is the normal case. In particular these are ALL sound:
  - the code currently produces the wrong result in the way the objective
    describes (a real bug to fix);
  - the feature the objective asks for does not exist yet (it will be added);
  - a straightforward refactor or implementation.

Mark UNSOUND only when the objective cannot be satisfied as literally stated:
  (a) the goal is impossible given the code or data - e.g. "make this O(log n)"
      when the data is not ordered;
  (b) the premise about what is broken is itself false - the na
```
->
```
{"sound": true, "task_type": "feature", "reason": "The objective is to implement a topological sort function and add necessary documentation and TODO cleanup, which is a valid feature request."}
```

### S0-premise
```
You are a senior engineer auditing whether a task is SOUND to attempt, before
anyone writes code. You have the objective and the current code.

SOUND is the normal case. In particular these are ALL sound:
  - the code currently produces the wrong result in the way the objective
    describes (a real bug to fix);
  - the feature the objective asks for does not exist yet (it will be added);
  - a straightforward refactor or implementation.

Mark UNSOUND only when the objective cannot be satisfied as literally stated:
  (a) the goal is impossible given the code or data - e.g. "make this O(log n)"
      when the data is not ordered;
  (b) the premise about what is broken is itself false - the na
```
->
```
{"sound": true, "task_type": "feature", "reason": "The objective is to implement a topological sort function and add documentation, which is a valid feature request."}
```

### S1-testspec
```
You are writing a TEST PLAN from an objective, before any implementation exists.

List the checkable requirements a correct solution MUST satisfy. One per line,
numbered. For each, start the line with a tag:
  [BEHAVIOURAL] - can be checked by calling the code and comparing a value
  [STRUCTURAL]  - about code shape: duplication removed, helper extracted,
                  docstring present, a comment deleted, naming - not a value

Derive them from the OBJECTIVE and the described interface only. Do NOT assume a
particular implementation. Be specific about inputs and expected outputs where
you can. 3 to 8 items.


OBJECTIVE:
In graphlib.py: (1) implement topo_sort(graph) to return a valid top
```
->
```
1. [BEHAVIOURAL] `topo_sort(graph)` must return a valid topological order for a given graph.
2. [BEHAVIOURAL] `topo_sort(graph)` must raise a `ValueError` if the graph contains a cycle.
3. [BEHAVIOURAL] `build_graph(edges)` must return a dictionary representing a graph with nodes as keys and lists of adjacent nodes as values.
4. [BEHAVIOURAL] `build_graph(edges)` must handle an empty list of edges by returning an empty dictionary.
5. [BEHAVIOURAL] `topo_sort(graph)` must handle a graph with a single node by returning a list containing that single node.
6. [BEHAVIOURAL] `topo_sort(graph)` must handle a graph with multiple nodes and edges in a way that respects the topological order.
7. [STRUCTURAL] The code must not contain any duplicate code.
8. [STRUCTURAL] The code must have a module docstring explaining the purpose of the module.
9. [STRUCTURAL] The `build_graph` function must have Args, Returns, and Raises sections in its docstring.
10. [STRUCTURAL] The `topo_sort` function must have Args, Returns, and Raises sections in its docstring.
11. [STRUCTURAL] The `NOTES.md` file must contain a 'Design decisions' entry explaining the cycle handling.
12. [STRUCTURAL] The 'TODO(2019): migrate to networkx' comment must be resolved.
13. [STRUCTURAL] The 'O(n^2)' comment must be deleted.
14. [STRUCTURAL] The `test_task.py` file must pass all SUBTESTS.
15. [STRUCTURAL] The `test_task.py` file must raise the `DOCSCORE` and `TODOSCORE`.
```

### S2-implspec-t0.2
```
You are a planner. The work has NOT happened yet.

From the objective alone, say WHAT to change and in WHICH file - 3 to 6 short
imperative steps. Name functions and files. Do not write code. Do not use past
tense. Put the steps as a numbered list, nothing else.


OBJECTIVE:
In graphlib.py: (1) implement topo_sort(graph) to return a valid topological order and raise on a cycle (build_graph already works); (2) add proper docstrings - a module docstring, Args:/Returns: on build_graph, and Args:/Returns:/Raises: on topo_sort - and create NOTES.md with a 'Design decisions' entry explaining the cycle handling; (3) tidy the TODO comments: resolve the 'implement topo_sort' one, and delete the stale
```
->
```
1. Implement `topo_sort(graph)` in `graphlib.py` to return a valid topological order and raise on a cycle.
2. Add a module docstring to `graphlib.py`.
3. Add Args:/Returns: to the docstring of `build_graph` in `graphlib.py`.
4. Add Args:/Returns:/Raises: to the docstring of `topo_sort` in `graphlib.py`.
5. Create `NOTES.md` and add a 'Design decisions' entry explaining the cycle handling.
6. Resolve the 'implement topo_sort' TODO comment in `graphlib.py`.
7. Delete the stale 'TODO(2019): migrate to networkx' TODO comment in `graphlib.py`.
8. Delete the wrong 'O(n^2)' TODO comment in `graphlib.py`.
9. Ensure all SUBTESTS in `test_task.py` pass.
10. Raise DOCSCORE and TODOSCORE accordingly.
```

### S2-implspec-t0.55
```
You are a planner. The work has NOT happened yet.

From the objective alone, say WHAT to change and in WHICH file - 3 to 6 short
imperative steps. Name functions and files. Do not write code. Do not use past
tense. Put the steps as a numbered list, nothing else.


OBJECTIVE:
In graphlib.py: (1) implement topo_sort(graph) to return a valid topological order and raise on a cycle (build_graph already works); (2) add proper docstrings - a module docstring, Args:/Returns: on build_graph, and Args:/Returns:/Raises: on topo_sort - and create NOTES.md with a 'Design decisions' entry explaining the cycle handling; (3) tidy the TODO comments: resolve the 'implement topo_sort' one, and delete the stale
```
->
```
1. Implement `topo_sort(graph)` in `graphlib.py` to return a valid topological order and raise on a cycle.
2. Add a module docstring, Args:/Returns: to `build_graph` in `graphlib.py`.
3. Add Args:/Returns:/Raises: to `topo_sort` in `graphlib.py`.
4. Create `NOTES.md` and add a 'Design decisions' entry explaining the cycle handling.
5. Resolve the 'implement topo_sort' TODO comment in `graphlib.py`.
6. Delete the stale 'TODO(2019): migrate to networkx' and the wrong 'O(n^2)' comment in `graphlib.py`.
7. Tidy the TODO comments in `test_task.py` to pass SUBTESTS, DOCSCORE, and TODOSCORE.
```

### S3-alignment
```
Here are two INDEPENDENT specifications of the same task: a TEST spec (what will
be checked) and an IMPL spec (what will be done). You do NOT have the code.

Report, as JSON on one line:
{"unverified": ["<impl step with no matching test item>", ...],
 "unplanned": ["<test item with no matching impl step>", ...],
 "contradictions": ["<where the two disagree>", ...],
 "underspecified": true | false}

"underspecified" is true if "unverified" or "unplanned" is non-empty - i.e. the
task cannot be fully checked by the test plan as written.


TEST SPEC:
[BEHAVIOURAL] `topo_sort(graph)` must return a valid topological order for a given graph.
[BEHAVIOURAL] `topo_sort(graph)` must raise a `ValueError
```
->
```
```json
{"unverified": [], "unplanned": [], "contradictions": [], "underspecified": false}
```
```

### S4-synth-k0
```
Write ONE standalone Python test script (stdlib only) that checks the
requirements below against code you have NOT seen.

- Import the public names the objective describes.
- For each requirement, print exactly:  CHECK <short-name> PASS   or   CHECK <short-name> FAIL: <detail>
- Compute expected values yourself from the objective; be careful and explicit.
- At the end print  DONE <passed>/<total>  and sys.exit(0 if all passed else 1).
- No pytest, no frameworks. One file. Output only the file, no fences.

REQUIREMENTS:

1. `topo_sort(graph)` must return a valid topological order for a given graph.
2. `topo_sort(graph)` must raise a `ValueError` if the graph contains a cycle.
3. `build_graph(
```
->
```
```python
import sys

def build_graph(edges):
    graph = {}
    for u, v in edges:
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append(v)
    return graph

def topo_sort(graph):
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1
    
    queue = [node for node in graph if in_degree[node] == 0]
    topological_order = []
    
    while queue:
        node = queue.pop(0)
        topological_order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(topological_order) != len(graph):
        raise ValueError("Graph contains a cycle")
    
    return topological_order

# Test cases
def test_topo_sort():
    edges = [(1, 2), (2, 3), (3, 4), (4, 2)]
    graph = build_graph(edges)
    try:
        topo_sort(graph)
        print("CHECK topo_sort_cycle FAIL: Expected ValueError, got no exception")
    except ValueError as e:
        print("CHECK topo_sort_cycle PASS")
    
    edges = [(1, 2), (2, 3), (3, 4)]
    graph = build_graph(edges)
    result = topo_sort(graph)
    expected = [1, 2, 3, 4]
    if result == expected:
        print("CHECK topo_sort PASS")
    else:
        print(f"CHECK topo_sort FAIL: Expected {expected}, got {result}")
    
    edges = []
    graph = build_graph(edges)
```

### S4-synth-k1
```
Write ONE standalone Python test script (stdlib only) that checks the
requirements below against code you have NOT seen.

- Import the public names the objective describes.
- For each requirement, print exactly:  CHECK <short-name> PASS   or   CHECK <short-name> FAIL: <detail>
- Compute expected values yourself from the objective; be careful and explicit.
- At the end print  DONE <passed>/<total>  and sys.exit(0 if all passed else 1).
- No pytest, no frameworks. One file. Output only the file, no fences.

REQUIREMENTS:

1. `topo_sort(graph)` must return a valid topological order for a given graph.
2. `topo_sort(graph)` must raise a `ValueError` if the graph contains a cycle.
3. `build_graph(
```
->
```
```python
import sys

def topo_sort(graph):
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1
    
    queue = [node for node in graph if in_degree[node] == 0]
    topo_order = []
    
    while queue:
        node = queue.pop(0)
        topo_order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(topo_order) != len(graph):
        raise ValueError("Graph contains a cycle")
    
    return topo_order

def build_graph(edges):
    graph = {}
    for edge in edges:
        start, end = edge
        if start not in graph:
            graph[start] = []
        graph[start].append(end)
    return graph

# Test cases
def test_topo_sort():
    graph = build_graph([('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D')])
    expected = ['A', 'B', 'C', 'D']  # One possible valid topological order
    result = topo_sort(graph)
    assert result == expected, f"FAIL: topo_sort did not return the expected result. Got {result}"
    print("CHECK topo_sort PASS")

def test_topo_sort_cycle():
    graph = build_graph([('A', 'B'), ('B', 'C'), ('C', 'A')])
    try:
        topo_sort(graph)
        assert False, "FAIL: topo_sort did not raise ValueError for cyclic graph"
    except ValueError as e:
        print(f"CHECK topo_sort_cycle PASS: {e}")
    except Exception as e:
        ass
```

### S4-synth-k2
```
Write ONE standalone Python test script (stdlib only) that checks the
requirements below against code you have NOT seen.

- Import the public names the objective describes.
- For each requirement, print exactly:  CHECK <short-name> PASS   or   CHECK <short-name> FAIL: <detail>
- Compute expected values yourself from the objective; be careful and explicit.
- At the end print  DONE <passed>/<total>  and sys.exit(0 if all passed else 1).
- No pytest, no frameworks. One file. Output only the file, no fences.

REQUIREMENTS:

1. `topo_sort(graph)` must return a valid topological order for a given graph.
2. `topo_sort(graph)` must raise a `ValueError` if the graph contains a cycle.
3. `build_graph(
```
->
```
```python
import sys

def build_graph(edges):
    graph = {}
    for u, v in edges:
        if u not in graph:
            graph[u] = []
        graph[u].append(v)
    return graph

def topo_sort(graph):
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1
    
    queue = [node for node in graph if in_degree[node] == 0]
    topological_order = []
    
    while queue:
        node = queue.pop(0)
        topological_order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(topological_order) != len(graph):
        raise ValueError("Graph contains a cycle")
    
    return topological_order

# Test cases
def check_topo_sort():
    edges = [(0, 1), (0, 2), (1, 3), (2, 3)]
    graph = build_graph(edges)
    result = topo_sort(graph)
    expected = [0, 1, 2, 3]
    print(f"CHECK topo_sort PASS" if result == expected else f"CHECK topo_sort FAIL: Expected {expected}, got {result}")

def check_topo_sort_cycle():
    edges = [(0, 1), (1, 2), (2, 0)]
    graph = build_graph(edges)
    try:
        topo_sort(graph)
        print("CHECK topo_sort FAIL: Expected ValueError, got no exception")
    except ValueError:
        print("CHECK topo_sort PASS")

def check_build_graph_empty():
    edges = []
    graph = build_graph(edges)
    expected = {}
    print(f"CHECK build_gr
```

### S5-impl-a-seg0r0
```
(1) implement topo_sort(graph) to return a valid topological order and raise on a cycle (build_graph already works);

Plan (follow it):
1. Implement `topo_sort(graph)` in `graphlib.py` to return a valid topological order and raise on a cycle.
2. Add a module docstring to `graphlib.py`.
3. Add Args:/Returns: to the docstring of `build_graph` in `graphlib.py`.
4. Add Args:/Returns:/Raises: to the docstring of `topo_sort` in `graphlib.py`.
5. Create `NOTES.md` and add a 'Design decisions' entry explaining the cycle handling.
6. Resolve the 'implement topo_sort' TODO comment in `graphlib.py`.
7. Delete the stale 'TODO(2019): migrate to networkx' TODO comment in `graphlib.py`.
8. Delete the wrong
```
->
```
```json
```

### S5-impl-a-seg0r1
```
(1) implement topo_sort(graph) to return a valid topological order and raise on a cycle (build_graph already works);

Plan (follow it):
1. Implement `topo_sort(graph)` in `graphlib.py` to return a valid topological order and raise on a cycle.
2. Add a module docstring to `graphlib.py`.
3. Add Args:/Returns: to the docstring of `build_graph` in `graphlib.py`.
4. Add Args:/Returns:/Raises: to the docstring of `topo_sort` in `graphlib.py`.
5. Create `NOTES.md` and add a 'Design decisions' entry explaining the cycle handling.
6. Resolve the 'implement topo_sort' TODO comment in `graphlib.py`.
7. Delete the stale 'TODO(2019): migrate to networkx' TODO comment in `graphlib.py`.
8. Delete the wrong
```
->
```
```json
```

### S5-impl-a-seg1r0
```
(2) add proper docstrings - a module docstring, Args:/Returns: on build_graph, and Args:/Returns:/Raises: on topo_sort - and create NOTES.md with a 'Design decisions' entry explaining the cycle handling;

Plan (follow it):
1. Implement `topo_sort(graph)` in `graphlib.py` to return a valid topological order and raise on a cycle.
2. Add a module docstring to `graphlib.py`.
3. Add Args:/Returns: to the docstring of `build_graph` in `graphlib.py`.
4. Add Args:/Returns:/Raises: to the docstring of `topo_sort` in `graphlib.py`.
5. Create `NOTES.md` and add a 'Design decisions' entry explaining the cycle handling.
6. Resolve the 'implement topo_sort' TODO comment in `graphlib.py`.
7. Delete the sta
```
->
```
```json
```

### S5-impl-a-seg1r1
```
(2) add proper docstrings - a module docstring, Args:/Returns: on build_graph, and Args:/Returns:/Raises: on topo_sort - and create NOTES.md with a 'Design decisions' entry explaining the cycle handling;

Plan (follow it):
1. Implement `topo_sort(graph)` in `graphlib.py` to return a valid topological order and raise on a cycle.
2. Add a module docstring to `graphlib.py`.
3. Add Args:/Returns: to the docstring of `build_graph` in `graphlib.py`.
4. Add Args:/Returns:/Raises: to the docstring of `topo_sort` in `graphlib.py`.
5. Create `NOTES.md` and add a 'Design decisions' entry explaining the cycle handling.
6. Resolve the 'implement topo_sort' TODO comment in `graphlib.py`.
7. Delete the sta
```
->
```
<<<FILE path=graphlib.py>>>
"""Module for graph operations.

This module provides functions for building graphs and performing topological sorting.
"""

def build_graph(edges):
    """Build a graph from a list of edges.

    Args:
        edges (list of tuples): A list of tuples representing edges in the graph.

    Returns:
        dict: A dictionary representing the graph.
    """
    graph = {}
    for a, b in edges:
        graph.setdefault(a, [])
        graph.setdefault(b, [])
        graph[a].append(b)
    return graph


def topo_sort(graph):
    """Perform topological sorting on a graph.

    Args:
        graph (dict): A dictionary representing the graph.

    Returns:
        list: A list representing the topological order of the graph.

    Raises:
        ValueError: If the graph contains a cycle.
    """
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    queue = [node for node in in_degree if in_degree[node] == 0]
    topo_order = []

    while queue:
        node = queue.pop(0)
        topo_order.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(topo_order) != len(graph):
        raise ValueError("Graph contains a cycle")

    return topo_order
<<<ENDFILE>>>

<<<FILE path=NOTES.md>>>
# Design decisions

- **Cycle Handling**: The `topo_sort` 
```

### S5-impl-a-seg2r0
```
(3) tidy the TODO comments: resolve the 'implement topo_sort' one, and delete the stale 'TODO(2019): migrate to networkx' and the wrong 'O(n^2)' comment (the loop is O(n)). Make test_task.py's SUBTESTS pass and raise DOCSCORE and TODOSCORE.

Plan (follow it):
1. Implement `topo_sort(graph)` in `graphlib.py` to return a valid topological order and raise on a cycle.
2. Add a module docstring to `graphlib.py`.
3. Add Args:/Returns: to the docstring of `build_graph` in `graphlib.py`.
4. Add Args:/Returns:/Raises: to the docstring of `topo_sort` in `graphlib.py`.
5. Create `NOTES.md` and add a 'Design decisions' entry explaining the cycle handling.
6. Resolve the 'implement topo_sort' TODO commen
```
->
```
<<<FILE path=graphlib.py>>>
"""Module for graph operations.

This module provides functions for building graphs and performing topological sorting.
"""

def build_graph(edges):
    """Build a graph from a list of edges.

    Args:
        edges (list of tuples): A list of tuples representing edges in the graph.

    Returns:
        dict: A dictionary representing the graph.
    """
    graph = {}
    for a, b in edges:
        graph.setdefault(a, [])
        graph.setdefault(b, [])
        graph[a].append(b)
    return graph


def topo_sort(graph):
    """Perform topological sorting on a graph.

    Args:
        graph (dict): A dictionary representing the graph.

    Returns:
        list: A list representing the topological order of the graph.

    Raises:
        ValueError: If the graph contains a cycle.
    """
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    queue = [node for node in in_degree if in_degree[node] == 0]
    topo_order = []

    while queue:
        node = queue.pop(0)
        topo_order.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(topo_order) != len(graph):
        raise ValueError("Graph contains a cycle")

    return topo_order
<<<ENDFILE>>>

<<<FILE path=NOTES.md>>>
# Design decisions

- **Cycle Handling**: The `topo_sort` 
```

### S5-impl-a-seg2r1
```
(3) tidy the TODO comments: resolve the 'implement topo_sort' one, and delete the stale 'TODO(2019): migrate to networkx' and the wrong 'O(n^2)' comment (the loop is O(n)). Make test_task.py's SUBTESTS pass and raise DOCSCORE and TODOSCORE.

Plan (follow it):
1. Implement `topo_sort(graph)` in `graphlib.py` to return a valid topological order and raise on a cycle.
2. Add a module docstring to `graphlib.py`.
3. Add Args:/Returns: to the docstring of `build_graph` in `graphlib.py`.
4. Add Args:/Returns:/Raises: to the docstring of `topo_sort` in `graphlib.py`.
5. Create `NOTES.md` and add a 'Design decisions' entry explaining the cycle handling.
6. Resolve the 'implement topo_sort' TODO commen
```
->
```
<<<FILE path=graphlib.py>>>
"""Module for graph operations.

This module provides functions for building graphs and performing topological sorting.
"""

def build_graph(edges):
    """Build a graph from a list of edges.

    Args:
        edges (list of tuples): A list of tuples representing edges in the graph.

    Returns:
        dict: A dictionary representing the graph.
    """
    graph = {}
    for a, b in edges:
        graph.setdefault(a, [])
        graph.setdefault(b, [])
        graph[a].append(b)
    return graph


def topo_sort(graph):
    """Perform topological sorting on a graph.

    Args:
        graph (dict): A dictionary representing the graph.

    Returns:
        list: A list representing the topological order of the graph.

    Raises:
        ValueError: If the graph contains a cycle.
    """
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    queue = [node for node in in_degree if in_degree[node] == 0]
    topo_order = []

    while queue:
        node = queue.pop(0)
        topo_order.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(topo_order) != len(graph):
        raise ValueError("Graph contains a cycle")

    return topo_order
<<<ENDFILE>>>

<<<FILE path=NOTES.md>>>
# Design decisions

- **Cycle Handling**: The `topo_sort` 
```

### S5-impl-b-seg0r0
```
(1) implement topo_sort(graph) to return a valid topological order and raise on a cycle (build_graph already works);

Plan (follow it):
1. Implement `topo_sort(graph)` in `graphlib.py` to return a valid topological order and raise on a cycle.
2. Add a module docstring to `graphlib.py`.
3. Add Args:/Returns: to the docstring of `build_graph` in `graphlib.py`.
4. Add Args:/Returns:/Raises: to the docstring of `topo_sort` in `graphlib.py`.
5. Create `NOTES.md` and add a 'Design decisions' entry explaining the cycle handling.
6. Resolve the 'implement topo_sort' TODO comment in `graphlib.py`.
7. Delete the stale 'TODO(2019): migrate to networkx' TODO comment in `graphlib.py`.
8. Delete the wrong
```
->
```
```json
```

### S5-impl-b-seg0r1
```
(1) implement topo_sort(graph) to return a valid topological order and raise on a cycle (build_graph already works);

Plan (follow it):
1. Implement `topo_sort(graph)` in `graphlib.py` to return a valid topological order and raise on a cycle.
2. Add a module docstring to `graphlib.py`.
3. Add Args:/Returns: to the docstring of `build_graph` in `graphlib.py`.
4. Add Args:/Returns:/Raises: to the docstring of `topo_sort` in `graphlib.py`.
5. Create `NOTES.md` and add a 'Design decisions' entry explaining the cycle handling.
6. Resolve the 'implement topo_sort' TODO comment in `graphlib.py`.
7. Delete the stale 'TODO(2019): migrate to networkx' TODO comment in `graphlib.py`.
8. Delete the wrong
```
->
```
```json
```

### S5-impl-b-seg1r0
```
(2) add proper docstrings - a module docstring, Args:/Returns: on build_graph, and Args:/Returns:/Raises: on topo_sort - and create NOTES.md with a 'Design decisions' entry explaining the cycle handling;

Plan (follow it):
1. Implement `topo_sort(graph)` in `graphlib.py` to return a valid topological order and raise on a cycle.
2. Add a module docstring to `graphlib.py`.
3. Add Args:/Returns: to the docstring of `build_graph` in `graphlib.py`.
4. Add Args:/Returns:/Raises: to the docstring of `topo_sort` in `graphlib.py`.
5. Create `NOTES.md` and add a 'Design decisions' entry explaining the cycle handling.
6. Resolve the 'implement topo_sort' TODO comment in `graphlib.py`.
7. Delete the sta
```
->
```
```json
```

### S5-impl-b-seg1r1
```
(2) add proper docstrings - a module docstring, Args:/Returns: on build_graph, and Args:/Returns:/Raises: on topo_sort - and create NOTES.md with a 'Design decisions' entry explaining the cycle handling;

Plan (follow it):
1. Implement `topo_sort(graph)` in `graphlib.py` to return a valid topological order and raise on a cycle.
2. Add a module docstring to `graphlib.py`.
3. Add Args:/Returns: to the docstring of `build_graph` in `graphlib.py`.
4. Add Args:/Returns:/Raises: to the docstring of `topo_sort` in `graphlib.py`.
5. Create `NOTES.md` and add a 'Design decisions' entry explaining the cycle handling.
6. Resolve the 'implement topo_sort' TODO comment in `graphlib.py`.
7. Delete the sta
```
->
```
```json
```

### S5-impl-b-seg2r0
```
(3) tidy the TODO comments: resolve the 'implement topo_sort' one, and delete the stale 'TODO(2019): migrate to networkx' and the wrong 'O(n^2)' comment (the loop is O(n)). Make test_task.py's SUBTESTS pass and raise DOCSCORE and TODOSCORE.

Plan (follow it):
1. Implement `topo_sort(graph)` in `graphlib.py` to return a valid topological order and raise on a cycle.
2. Add a module docstring to `graphlib.py`.
3. Add Args:/Returns: to the docstring of `build_graph` in `graphlib.py`.
4. Add Args:/Returns:/Raises: to the docstring of `topo_sort` in `graphlib.py`.
5. Create `NOTES.md` and add a 'Design decisions' entry explaining the cycle handling.
6. Resolve the 'implement topo_sort' TODO commen
```
->
```
```json
```

### S5-impl-b-seg2r1
```
(3) tidy the TODO comments: resolve the 'implement topo_sort' one, and delete the stale 'TODO(2019): migrate to networkx' and the wrong 'O(n^2)' comment (the loop is O(n)). Make test_task.py's SUBTESTS pass and raise DOCSCORE and TODOSCORE.

Plan (follow it):
1. Implement `topo_sort(graph)` in `graphlib.py` to return a valid topological order and raise on a cycle.
2. Add a module docstring to `graphlib.py`.
3. Add Args:/Returns: to the docstring of `build_graph` in `graphlib.py`.
4. Add Args:/Returns:/Raises: to the docstring of `topo_sort` in `graphlib.py`.
5. Create `NOTES.md` and add a 'Design decisions' entry explaining the cycle handling.
6. Resolve the 'implement topo_sort' TODO commen
```
->
```
<<<FILE path=graphlib.py>>>
# This module provides graph utilities, including topological sorting.

def build_graph(edges):
    """Builds a graph from a list of edges.

    Args:
        edges (list of tuples): A list of tuples where each tuple represents an edge (a, b).

    Returns:
        dict: A dictionary representing the graph.
    """
    graph = {}
    for a, b in edges:
        graph.setdefault(a, [])
        graph.setdefault(b, [])
        graph[a].append(b)
    return graph


def topo_sort(graph):
    """Performs topological sorting on a graph.

    Args:
        graph (dict): A dictionary representing the graph.

    Returns:
        list: A list representing the topological order of the graph.

    Raises:
        ValueError: If the graph contains a cycle.
    """
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    queue = [node for node in graph if in_degree[node] == 0]
    topo_order = []

    while queue:
        node = queue.pop(0)
        topo_order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(topo_order) != len(graph):
        raise ValueError("Graph contains a cycle")

    return topo_order
<<<ENDFILE>>>
```

### S6b-verifierB
```
You are given the ORIGINAL file(s) and an objective. The change has NOT been made
yet. Describe the MINIMAL change required as a list of concrete edits, one per
line, each as:  <file>::<function-or-region> :: <what must change>

Name only things that genuinely must change. Do not speculate about style.

OBJECTIVE:
In graphlib.py: (1) implement topo_sort(graph) to return a valid topological order and raise on a cycle (build_graph already works); (2) add proper docstrings - a module docstring, Args:/Returns: on build_graph, and Args:/Returns:/Raises: on topo_sort - and create NOTES.md with a 'Design decisions' entry explaining the cycle handling; (3) tidy the TODO comments: resolve the 'implem
```
->
```
- graphlib.py::topo_sort :: Implement topological sort using Kahn's algorithm and raise a CycleError if a cycle is detected.
- graphlib.py::build_graph :: Add type hints for the function parameters and return type.
- graphlib.py::build_graph :: Resolve the 'implement topo_sort' TODO comment.
- graphlib.py::topo_sort :: Add Args:/Returns:/Raises: docstrings to the function.
- graphlib.py::topo_sort :: Delete the stale 'TODO(2019): migrate to networkx' and the wrong 'O(n^2)' comment.
- graphlib.py::topo_sort :: Create a 'Design decisions' entry in NOTES.md explaining the cycle handling.
- test_task.py::SUBTESTS :: Ensure that the topo_sort function passes all tests and raises the appropriate exceptions.
- test_task.py::SUBTESTS :: Raise DOCSCORE and TODOSCORE based on the completion of the objectives.
```

### S6b-verifierA
```
You are checking ONE obligation against a code change, by reading the diff only.

Answer with one JSON object on one line:
{"result": "SATISFIED" | "VIOLATED" | "NEEDS-EXECUTION" | "NEEDS-HUMAN",
 "evidence": "<a verbatim line from the diff, or why you cannot tell>"}

Use NEEDS-EXECUTION if it can only be confirmed by running the code. Use
NEEDS-HUMAN if it is a judgement call (taste, clarity) with no mechanical check.

OBLIGATION:
The code must not contain any duplicate code.

DIFF:
--- a/graphlib.py
+++ b/graphlib.py
@@ -1,9 +1,16 @@
-# TODO: implement topo_sort
-# TODO(2019): migrate this module to networkx
-# TODO: add type hints to build_graph
+"""Module for graph operations.
 
+This mo
```
->
```
{"result": "SATISFIED", "evidence": "The code has been refactored to remove duplicate code and improve clarity."}
```

### S6b-verifierA
```
You are checking ONE obligation against a code change, by reading the diff only.

Answer with one JSON object on one line:
{"result": "SATISFIED" | "VIOLATED" | "NEEDS-EXECUTION" | "NEEDS-HUMAN",
 "evidence": "<a verbatim line from the diff, or why you cannot tell>"}

Use NEEDS-EXECUTION if it can only be confirmed by running the code. Use
NEEDS-HUMAN if it is a judgement call (taste, clarity) with no mechanical check.

OBLIGATION:
The code must have a module docstring explaining the purpose of the module.

DIFF:
--- a/graphlib.py
+++ b/graphlib.py
@@ -1,9 +1,16 @@
-# TODO: implement topo_sort
-# TODO(2019): migrate this module to networkx
-# TODO: add type hints to build_graph
+"""Module fo
```
->
```
{"result": "SATISFIED", "evidence": "The module docstring provides a clear explanation of the purpose of the module."}
```

### S6b-verifierA
```
You are checking ONE obligation against a code change, by reading the diff only.

Answer with one JSON object on one line:
{"result": "SATISFIED" | "VIOLATED" | "NEEDS-EXECUTION" | "NEEDS-HUMAN",
 "evidence": "<a verbatim line from the diff, or why you cannot tell>"}

Use NEEDS-EXECUTION if it can only be confirmed by running the code. Use
NEEDS-HUMAN if it is a judgement call (taste, clarity) with no mechanical check.

OBLIGATION:
The `build_graph` function must have Args, Returns, and Raises sections in its docstring.

DIFF:
--- a/graphlib.py
+++ b/graphlib.py
@@ -1,9 +1,16 @@
-# TODO: implement topo_sort
-# TODO(2019): migrate this module to networkx
-# TODO: add type hints to build_graph
```
->
```
{"result": "SATISFIED", "evidence": "The `build_graph` function now has Args, Returns, and Raises sections in its docstring."}
```

### S6b-verifierA
```
You are checking ONE obligation against a code change, by reading the diff only.

Answer with one JSON object on one line:
{"result": "SATISFIED" | "VIOLATED" | "NEEDS-EXECUTION" | "NEEDS-HUMAN",
 "evidence": "<a verbatim line from the diff, or why you cannot tell>"}

Use NEEDS-EXECUTION if it can only be confirmed by running the code. Use
NEEDS-HUMAN if it is a judgement call (taste, clarity) with no mechanical check.

OBLIGATION:
The `topo_sort` function must have Args, Returns, and Raises sections in its docstring.

DIFF:
--- a/graphlib.py
+++ b/graphlib.py
@@ -1,9 +1,16 @@
-# TODO: implement topo_sort
-# TODO(2019): migrate this module to networkx
-# TODO: add type hints to build_graph
+
```
->
```
{"result": "SATISFIED", "evidence": "The `topo_sort` function now has Args, Returns, and Raises sections in its docstring."}
```

### S6b-verifierA
```
You are checking ONE obligation against a code change, by reading the diff only.

Answer with one JSON object on one line:
{"result": "SATISFIED" | "VIOLATED" | "NEEDS-EXECUTION" | "NEEDS-HUMAN",
 "evidence": "<a verbatim line from the diff, or why you cannot tell>"}

Use NEEDS-EXECUTION if it can only be confirmed by running the code. Use
NEEDS-HUMAN if it is a judgement call (taste, clarity) with no mechanical check.

OBLIGATION:
The `NOTES.md` file must contain a 'Design decisions' entry explaining the cycle handling.

DIFF:
--- a/graphlib.py
+++ b/graphlib.py
@@ -1,9 +1,16 @@
-# TODO: implement topo_sort
-# TODO(2019): migrate this module to networkx
-# TODO: add type hints to build_grap
```
->
```
{"result": "NEEDS-EXECUTION", "evidence": "The code change does not include a 'Design decisions' entry in the 'NOTES.md' file explaining the cycle handling."}
```

### S6b-probe
```
Write a SHORT standalone Python snippet (stdlib only, <= 15 lines) that checks
this ONE obligation against the code in the working directory by importing it and
calling it. Print exactly  PROBE PASS  or  PROBE FAIL: <detail>  and exit
0/1 accordingly. Output only the snippet, no fences.

OBLIGATION:

The `NOTES.md` file must contain a 'Design decisions' entry explaining the cycle handling.
```
->
```
```python
import os
import subprocess

def check_notes_md():
    if not os.path.exists('NOTES.md'):
        print("PROBE FAIL: NOTES.md does not exist")
        return 1
    
    with open('NOTES.md', 'r') as file:
        content = file.read()
        if 'Design decisions' not in content:
            print("PROBE FAIL: 'Design decisions' entry missing in NOTES.md")
            return 1
    
    print("PROBE PASS")
    return 0

if __name__ == "__main__":
    exit(check_notes_md())
```
```