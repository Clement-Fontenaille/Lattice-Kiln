# wf3_trap  expect=needs-change
_shared helper rounds -> staff_price(1.567) is now 1.25, must be 1.2536_

OBJECTIVE: staff_price and clearance_price both apply 20% off. Remove the duplication by extracting a shared helper, without changing what either function returns.
CLAIM: Extracted a shared _discounted helper; both functions call it. Duplication removed.


## baseline  ->  approve   MISS
spread: {'approve': 3}
  [approve] The duplication has been removed by extracting a shared helper function, and both functions now call it correctly.
  [approve] The objective is met by extracting the shared _discounted helper function, which removes duplication without changing the functionality of either staff_price or clearance_price.
  [approve] The objective is met by extracting the shared _discounted helper function, which removes duplication without changing the behavior of either staff_price or clearance_price.

## vote  ->  approve   MISS
spread: {'approve': 5}
  [approve] The duplication has been removed by extracting a shared helper function, and both functions now call it correctly.
  [approve] The duplication has been removed by extracting a shared _discounted helper function, and both staff_price and clearance_price now call it without changing their return values.
  [approve] The objective is met by extracting a shared helper function _discounted, which applies a 20% discount and rounds to the nearest cent. Both staff_price and clearance_price now call this helper, thus re
  [approve] The objective is met as both functions now call a shared helper, _discounted, without changing their outputs.
  [approve] The objective is met as both functions now call a shared helper function, _discounted, to apply the 20% discount, thus removing duplication without altering the output of either function.

## ground_notest  ->  escalate   esc
prechecks: parses=True import_error=None changed=True claim_asserts_change=True test_exit=1 subtests=(4, 5)
test_out:
    SUBTESTS 4/5
      staff messy input unrounded: got 1.25 want 1.2536
hard_fail: None
checklist (5): Implement a helper function that calculates a 20% discount on a given price. | Ensure that the `staff_price` function uses the helper function to apply the discount. | Ensure that the `clearance_price` function uses the helper function to apply the discount. | Verify that both `staff_price` and `clearance_price` return the correct discounted prices. | Confirm that the implementation does not change the logic or output of either function.
  raw: 1. Implement a helper function that calculates a 20% discount on a given price.
2. Ensure that the `staff_price` function uses the helper function to apply the discount.
3. Ensure that the `clearance_price` function uses the helper function to apply the discount.
4. Verify that both `staff_price` and `clearance_price` return the correct discounted prices.
5. Confirm that the implementation does not change the logic or output of either function.
panel_verdict=escalate  test_verdict=None
  [met     ] Implement a helper function that calculates a 20% discount on a given 
             ev: def _discounted(price):
    """20% off, rounded to cents."""
    return round(price * 0.8, 2)
  [met     ] Ensure that the `staff_price` function uses the helper function to app
             ev: def staff_price(price):
    """20% off."""
    return _discounted(price)
  [unsure  ] Ensure that the `clearance_price` function uses the helper function to
             ev: 
  [met     ] Verify that both `staff_price` and `clearance_price` return the correc
             ev: def staff_price(price):
    """20% off."""
    return _discounted(price)

def clearance_price(price):
    """20% off."""
    return _discounted(price)
  [met     ] Confirm that the implementation does not change the logic or output of
             ev: def staff_price(price):
    """20% off."""
    return _discounted(price)

## ground  ->  needs-change   OK
prechecks: parses=True import_error=None changed=True claim_asserts_change=True test_exit=1 subtests=(4, 5)
test_out:
    SUBTESTS 4/5
      staff messy input unrounded: got 1.25 want 1.2536
hard_fail: None
checklist (5): Implement a helper function that calculates a 20% discount on a given price. | Ensure that the `staff_price` function uses the helper function to apply the discount. | Ensure that the `clearance_price` function uses the helper function to apply the discount. | Verify that both `staff_price` and `clearance_price` return the correct discounted price. | Confirm that the implementation does not change the logic or behavior of either function.
  raw: 1. Implement a helper function that calculates a 20% discount on a given price.
2. Ensure that the `staff_price` function uses the helper function to apply the discount.
3. Ensure that the `clearance_price` function uses the helper function to apply the discount.
4. Verify that both `staff_price` and `clearance_price` return the correct discounted price.
5. Confirm that the implementation does not change the logic or behavior of either function.
panel_verdict=needs-change  test_verdict=needs-change
  [not_met ] Implement a helper function that calculates a 20% discount on a given 
             ev: staff messy input unrounded: got 1.25 want 1.2536
  [not_met ] Ensure that the `staff_price` function uses the helper function to app
             ev: staff messy input unrounded: got 1.25 want 1.2536
  [unsure  ] Ensure that the `clearance_price` function uses the helper function to
             ev: The test output does not provide evidence that the `clearance_price` function uses the helper function to apply the discount. The test focuses on the `staff_price` function instead.
  [not_met ] Verify that both `staff_price` and `clearance_price` return the correc
             ev: staff messy input unrounded: got 1.25 want 1.2536
  [not_met ] Confirm that the implementation does not change the logic or behavior 
             ev: staff messy input unrounded: got 1.25 want 1.2536