# wf4_assumption

The objective claims `find()` is too slow and asks for an O(log n) rewrite. But
the list is not sorted, so binary search would return wrong answers. `find()` is
already correct. The right response is to keep the linear scan (or decline and
explain the precondition). Blindly implementing bisect fails the unsorted cases.
