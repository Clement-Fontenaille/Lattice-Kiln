# wf1_crossfile rep1 -> needs-change
_baseline (2, 5) -> final (5, 5), 22 calls, 105.8s_

signals: {"premise_unsound": false, "l1_provided_fail": false, "regression": false, "l2_violated": true, "synth_trusted_fail": false, "l2_needs_human": false, "blowout": false, "refactor_unverified": false}
load-bearing: ['l2_violated']
open_items: []

OBJECTIVE: orders.total() returns the wrong amount when an order line's qty is greater than 1. Fix the code so every subtest in test_task.py passes. Note that one subtest calls pricing.line_price directly.

## ledger

- **S0-premise** (3c 9.6s): sound=True type=bugfix votes=[True, True, True] reason=''
- **S1-testspec** (1c 7.2s): 13 items 8B/5S
- **S2-implspec** (2c 8.7s): 6/6 steps, overlap=0.41 disagree=False
- **S3-alignment** (1c 2.9s): advisory: unverified=0 unplanned=0
- **S4-synth** (3c 29.5s): 2/3 valid; checks/suite=7,1,0
- **S5-coding** (2c 10.5s): incumbent comb=2 | impl_a comb=5(sub5) impl_b comb=5(sub5) agree=True -> winner a sub(5, 5) docNone todoNone diff_lines=7 blowout=False
- **S6b-l2** (10c 36.9s): pass,fail,fail,fail,fail b_consistent=True

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
{"sound": true, "task_type": "bugfix", "reason": "The code currently produces the wrong result due to a bug in pricing.line_price.", "correct_action": "Fix the bug in pricing.line_price to include item['qty'] in the calculation."}
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
{"sound": true, "task_type": "bugfix", "reason": "The code currently ignores the quantity of items when calculating the line price.", "correct_action": "Modify the line_price function to multiply the unit price by the quantity."}
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
{"sound": true, "task_type": "bugfix", "reason": "The code currently calculates the total price incorrectly by ignoring the quantity of each item.", "correct_action": "Fix the line_price function to multiply the unit price by the quantity."}
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
orders.total() returns the wrong amount when an order line's qty is 
```
->
```
1. [BEHAVIOURAL] orders.total() should correctly calculate the total amount for an order with multiple lines, including lines where the quantity is greater than 1.
2. [BEHAVIOURAL] orders.total() should return the correct total amount when a line's quantity is 1.
3. [BEHAVIOURAL] orders.total() should handle cases where an order line's quantity is zero.
4. [BEHAVIOURAL] orders.total() should correctly calculate the total amount when an order line's quantity is negative.
5. [BEHAVIOURAL] orders.total() should handle cases where an order line's quantity is a non-integer value.
6. [BEHAVIOURAL] orders.total() should correctly calculate the total amount when an order line's quantity is a floating-point number.
7. [BEHAVIOURAL] orders.total() should handle cases where an order line's quantity is a large number.
8. [BEHAVIOURAL] orders.total() should correctly calculate the total amount when an order line's quantity is a very small number.
9. [STRUCTURAL] The code should not contain any duplication.
10. [STRUCTURAL] The code should have helper functions or methods extracted where appropriate.
11. [STRUCTURAL] The code should have a docstring present for each function or method.
12. [STRUCTURAL] The code should not have any unnecessary comments.
13. [STRUCTURAL] The code should have consistent and meaningful naming conventions.
```

### S2-implspec-t0.2
```
You are a planner. The work has NOT happened yet.

From the objective alone, say WHAT to change and in WHICH file - 3 to 6 short
imperative steps. Name functions and files. Do not write code. Do not use past
tense. Put the steps as a numbered list, nothing else.


OBJECTIVE:
orders.total() returns the wrong amount when an order line's qty is greater than 1. Fix the code so every subtest in test_task.py passes. Note that one subtest calls pricing.line_price directly.
```
->
```
1. Review the `orders.py` file to identify the `total()` function.
2. Locate the `pricing.py` file and find the `line_price()` function.
3. Modify the `total()` function in `orders.py` to correctly calculate the total amount by iterating through each order line and using the `line_price()` function.
4. Update the `line_price()` function in `pricing.py` to ensure it correctly calculates the price for each line based on the quantity.
5. Run the `test_task.py` file to verify that all subtests pass.
6. If any subtests fail, revisit the `total()` and `line_price()` functions for further adjustments.
```

### S2-implspec-t0.55
```
You are a planner. The work has NOT happened yet.

From the objective alone, say WHAT to change and in WHICH file - 3 to 6 short
imperative steps. Name functions and files. Do not write code. Do not use past
tense. Put the steps as a numbered list, nothing else.


OBJECTIVE:
orders.total() returns the wrong amount when an order line's qty is greater than 1. Fix the code so every subtest in test_task.py passes. Note that one subtest calls pricing.line_price directly.
```
->
```
1. Review the `orders.total()` function in the `orders.py` file.
2. Identify where the `qty` of each order line is being used to calculate the total.
3. Modify the `orders.total()` function to correctly handle `qty` values greater than 1.
4. Update the `pricing.line_price()` function in the `pricing.py` file if it is directly called by a subtest.
5. Ensure that the updated functions are tested with the existing subtests in `test_task.py`.
6. Run `test_task.py` to confirm that all subtests pass.
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
[BEHAVIOURAL] orders.total() should correctly calculate the total amount for an order with multiple lines, including lines where the quantity is gr
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

1. orders.total() should correctly calculate the total amount for an order with multiple lines, including lines where the quantity is greater than 1.
2. orders.total() should
```
->
```
```python
import sys

def check_order_total():
    # Mock order lines for testing
    order_lines = [
        {'price': 10, 'quantity': 3},
        {'price': 5, 'quantity': 1},
        {'price': 0, 'quantity': 0},
        {'price': 20, 'quantity': -2},
        {'price': 100, 'quantity': 1.5},
        {'price': 0.01, 'quantity': 1000000},
        {'price': 1000000, 'quantity': 0.000001}
    ]
    
    # Expected results
    expected_results = [
        30,  # 10 * 3
        5,   # 5 * 1
        0,   # 0 * 0
        -40, # 20 * -2
        150, # 100 * 1.5
        1000000, # 0.01 * 1000000
        1000  # 1000000 * 0.000001
    ]
    
    # Import the orders module
    try:
        import orders
    except ImportError:
        print("CHECK orders_import FAIL: orders module not found")
        sys.exit(1)
    
    # Check each requirement
    passed = 0
    total = len(order_lines)
    
    for i, order_line in enumerate(order_lines):
        try:
            total_amount = orders.total(order_line['price'], order_line['quantity'])
            if total_amount == expected_results[i]:
                print(f"CHECK requirement_{i+1} PASS")
                passed += 1
            else:
                print(f"CHECK requirement_{i+1} FAIL: Expected {expected_results[i]}, got {total_amount}")
        except Exception as e:
            print(f"CHECK requirement_{i+1} FAIL: Exception {e}")
    
    # Print final result
    print(f"DONE {passed}/{total}")
    sys.exit(0 if passed == total 
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

1. orders.total() should correctly calculate the total amount for an order with multiple lines, including lines where the quantity is greater than 1.
2. orders.total() should
```
->
```
```python
import sys

class OrderLine:
    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity

class Order:
    def __init__(self):
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)

    def total(self):
        return sum(line.price * line.quantity for line in self.lines)

def test_orders_total():
    order = Order()
    order.add_line(OrderLine(10, 2))
    order.add_line(OrderLine(5, 1))
    order.add_line(OrderLine(1, 0))
    order.add_line(OrderLine(1, -1))
    order.add_line(OrderLine(1, 1.5))
    order.add_line(OrderLine(1, 1000000))
    order.add_line(OrderLine(1, 1e-10))

    expected = (10 * 2) + (5 * 1) + (1 * 0) + (1 * -1) + (1 * 1.5) + (1 * 1000000) + (1 * 1e-10)
    result = order.total()

    if result == expected:
        print("CHECK total PASS")
    else:
        print(f"CHECK total FAIL: Expected {expected}, got {result}")

    print(f"DONE {1}/{1}")
    sys.exit(0 if result == expected else 1)

if __name__ == "__main__":
    test_orders_total()
```
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

1. orders.total() should correctly calculate the total amount for an order with multiple lines, including lines where the quantity is greater than 1.
2. orders.total() should
```
->
```
```python
import sys

class OrderLine:
    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity

class Order:
    def __init__(self):
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)

    def total(self):
        return sum(line.price * line.quantity for line in self.lines)

def test_orders_total():
    order = Order()

    # Requirement 1: Correctly calculate the total amount for an order with multiple lines
    order.add_line(OrderLine(10, 2))
    order.add_line(OrderLine(5, 3))
    assert order.total() == 20 + 15, "Requirement 1 failed"

    # Requirement 2: Return the correct total amount when a line's quantity is 1
    order = Order()
    order.add_line(OrderLine(10, 1))
    assert order.total() == 10, "Requirement 2 failed"

    # Requirement 3: Handle cases where an order line's quantity is zero
    order = Order()
    order.add_line(OrderLine(10, 0))
    assert order.total() == 0, "Requirement 3 failed"

    # Requirement 4: Correctly calculate the total amount when an order line's quantity is negative
    order = Order()
    order.add_line(OrderLine(10, -2))
    assert order.total() == -20, "Requirement 4 failed"

    # Requirement 5: Handle cases where an order line's quantity is a non-integer value
    order = Order()
    order.add_line(OrderLine(10, 2.5))
    assert order.total() == 25, "Requirement 5 failed"

    # Requirement 6: Correctly calculate the total amount when an order li
```

### S5-impl-a-seg0r0
```
orders.total() returns the wrong amount when an order line's qty is greater than 1. Fix the code so every subtest in test_task.py passes. Note that one subtest calls pricing.line_price directly.

Plan (follow it):
1. Review the `orders.py` file to identify the `total()` function.
2. Locate the `pricing.py` file and find the `line_price()` function.
3. Modify the `total()` function in `orders.py` to correctly calculate the total amount by iterating through each order line and using the `line_price()` function.
4. Update the `line_price()` function in `pricing.py` to ensure it correctly calculates the price for each line based on the quantity.
5. Run the `test_task.py` file to verify that all 
```
->
```
<<<FILE path=pricing.py>>>
def line_price(item):
    """Price for one order line: unit price times quantity."""
    return item["unit_price"] * item["qty"]  # Corrected to multiply unit_price by qty
<<<ENDFILE>>>
```

### S5-impl-b-seg0r0
```
orders.total() returns the wrong amount when an order line's qty is greater than 1. Fix the code so every subtest in test_task.py passes. Note that one subtest calls pricing.line_price directly.

Plan (follow it):
1. Review the `orders.py` file to identify the `total()` function.
2. Locate the `pricing.py` file and find the `line_price()` function.
3. Modify the `total()` function in `orders.py` to correctly calculate the total amount by iterating through each order line and using the `line_price()` function.
4. Update the `line_price()` function in `pricing.py` to ensure it correctly calculates the price for each line based on the quantity.
5. Run the `test_task.py` file to verify that all 
```
->
```
<<<FILE path=pricing.py>>>
def line_price(item):
    """Price for one order line: unit price times quantity."""
    return item["unit_price"] * item["qty"]  # Correctly multiply unit price by quantity
<<<ENDFILE>>>
```

### S6b-verifierB
```
You are given the ORIGINAL file(s) and an objective. The change has NOT been made
yet. Describe the MINIMAL change required as a list of concrete edits, one per
line, each as:  <file>::<function-or-region> :: <what must change>

Name only things that genuinely must change. Do not speculate about style.

OBJECTIVE:
orders.total() returns the wrong amount when an order line's qty is greater than 1. Fix the code so every subtest in test_task.py passes. Note that one subtest calls pricing.line_price directly.

ORIGINAL:
--- orders.py ---
from pricing import line_price


def total(order):
    """Sum of all line prices in an order."""
    return sum(line_price(li) for li in order["lines"])

--- pr
```
->
```
--- pricing.py ---
def line_price(item):
    """Price for one order line: unit price times quantity."""
    return item["unit_price"] * item["qty"]
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
The code should not contain any duplication.

DIFF:
--- a/pricing.py
+++ b/pricing.py
@@ -1,3 +1,3 @@
 def line_price(item):
     """Price for one order line: unit price times quantity."""
-    return item["unit_price"]  # BUG: ignores item["qty"]
+    return item
```
->
```
{"result": "SATISFIED", "evidence": "The code now correctly multiplies the unit price by the quantity, removing any duplication."}
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
The code should have helper functions or methods extracted where appropriate.

DIFF:
--- a/pricing.py
+++ b/pricing.py
@@ -1,3 +1,3 @@
 def line_price(item):
     """Price for one order line: unit price times quantity."""
-    return item["unit_price"]  # BUG: ign
```
->
```
{"result": "NEEDS-EXECUTION", "evidence": "The diff only shows a correction in the calculation of line_price, but it does not provide evidence that helper functions or methods have been extracted where appropriate."}
```

### S6b-probe
```
Write a SHORT standalone Python snippet (stdlib only, <= 15 lines) that checks
this ONE obligation against the code in the working directory by importing it and
calling it. Print exactly  PROBE PASS  or  PROBE FAIL: <detail>  and exit
0/1 accordingly. Output only the snippet, no fences.

OBLIGATION:

The code should have helper functions or methods extracted where appropriate.
```
->
```
```python
import os
import inspect

def check_helper_functions():
    for file_name in os.listdir('.'):
        if file_name.endswith('.py'):
            with open(file_name, 'r') as file:
                content = file.read()
                if not any(inspect.isfunction(obj) and obj.__name__.startswith('helper_') for obj in inspect.getmembers(content)):
                    return False
    return True

if check_helper_functions():
    print("PROBE PASS")
    exit(0)
else:
    print("PROBE FAIL: No helper functions found")
    exit(1)
```
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
The code should have a docstring present for each function or method.

DIFF:
--- a/pricing.py
+++ b/pricing.py
@@ -1,3 +1,3 @@
 def line_price(item):
     """Price for one order line: unit price times quantity."""
-    return item["unit_price"]  # BUG: ignores ite
```
->
```
{"result": "NEEDS-EXECUTION", "evidence": "The diff does not include a docstring for the function."}
```

### S6b-probe
```
Write a SHORT standalone Python snippet (stdlib only, <= 15 lines) that checks
this ONE obligation against the code in the working directory by importing it and
calling it. Print exactly  PROBE PASS  or  PROBE FAIL: <detail>  and exit
0/1 accordingly. Output only the snippet, no fences.

OBLIGATION:

The code should have a docstring present for each function or method.
```
->
```
```python
import os
import inspect

def check_docstrings():
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r') as f:
                    code = f.read()
                    for name, obj in inspect.getmembers(inspect.getmodule(inspect.currentframe()), inspect.isfunction):
                        if not obj.__doc__:
                            return False
    return True

if check_docstrings():
    print("PROBE PASS")
    exit(0)
else:
    print("PROBE FAIL: Missing docstrings in some functions")
    exit(1)
```
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
The code should not have any unnecessary comments.

DIFF:
--- a/pricing.py
+++ b/pricing.py
@@ -1,3 +1,3 @@
 def line_price(item):
     """Price for one order line: unit price times quantity."""
-    return item["unit_price"]  # BUG: ignores item["qty"]
+    retur
```
->
```
{"result": "NEEDS-EXECUTION", "evidence": "The diff does not show any unnecessary comments. The code has been modified to correct a bug, but it does not introduce any new unnecessary comments."}
```

### S6b-probe
```
Write a SHORT standalone Python snippet (stdlib only, <= 15 lines) that checks
this ONE obligation against the code in the working directory by importing it and
calling it. Print exactly  PROBE PASS  or  PROBE FAIL: <detail>  and exit
0/1 accordingly. Output only the snippet, no fences.

OBLIGATION:

The code should not have any unnecessary comments.
```
->
```
```python
import os
import re

def check_unnecessary_comments():
    pattern = re.compile(r'#.*')
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    if pattern.search(content):
                        return False
    return True

if check_unnecessary_comments():
    print("PROBE PASS")
    exit(0)
else:
    print("PROBE FAIL: Unnecessary comments found")
    exit(1)
```
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
The code should have consistent and meaningful naming conventions.

DIFF:
--- a/pricing.py
+++ b/pricing.py
@@ -1,3 +1,3 @@
 def line_price(item):
     """Price for one order line: unit price times quantity."""
-    return item["unit_price"]  # BUG: ignores item["
```
->
```
{"result": "NEEDS-EXECUTION", "evidence": "The diff shows a code change that corrects a bug, but it does not provide evidence of consistent and meaningful naming conventions."}
```

### S6b-probe
```
Write a SHORT standalone Python snippet (stdlib only, <= 15 lines) that checks
this ONE obligation against the code in the working directory by importing it and
calling it. Print exactly  PROBE PASS  or  PROBE FAIL: <detail>  and exit
0/1 accordingly. Output only the snippet, no fences.

OBLIGATION:

The code should have consistent and meaningful naming conventions.
```
->
```
```python
import os
import re

def check_naming_convention():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for file in files:
        with open(file, 'r') as f:
            content = f.read()
            if not re.match(r'^[a-z_][a-z0-9_]*$', file):
                return "PROBE FAIL: Inconsistent file naming"
            if not re.match(r'^def [a-z_][a-z0-9_]*\(.*\):$', content):
                return "PROBE FAIL: Inconsistent function naming"
            if not re.match(r'^class [A-Z][a-zA-Z0-9]*\(.*\):$', content):
                return "PROBE FAIL: Inconsistent class naming"
    return "PROBE PASS"

result = check_naming_convention()
print(result)
exit(0 if "PASS" in result else 1)
```
```