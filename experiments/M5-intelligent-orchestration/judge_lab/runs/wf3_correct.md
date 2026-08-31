# wf3_correct  expect=approve
_correct dedupe; rounding kept only in clearance_

OBJECTIVE: staff_price and clearance_price both apply 20% off. Remove the duplication by extracting a shared helper, without changing what either function returns.
CLAIM: Extracted a shared _base helper; both functions call it; clearance still rounds.


## baseline  ->  approve   OK
spread: {'approve': 3}
  [approve] The objective is met by extracting a shared helper function that applies the 20% discount. Both functions call this helper, and the rounding behavior for clearance_price remains unchanged.
  [approve] The objective is met by extracting a shared helper function that applies the 20% discount. Both functions call this helper, and the clearance_price function still rounds to cents as required.
  [approve] The objective is met as both functions now call a shared helper and the rounding behavior for clearance_price remains unchanged.

## vote  ->  approve   OK
spread: {'approve': 5}
  [approve] The objective is met by extracting the common logic into a shared helper function without changing the behavior of the original functions.
  [approve] The objective is met as both functions now call a shared _base helper, and clearance_price still rounds to cents.
  [approve] The objective is met as both functions now call the shared _base helper, and the rounding in clearance_price remains unchanged.
  [approve] The objective is met by extracting a shared helper function that applies the 20% discount. Both functions now call this helper, and the clearance_price function still rounds to the nearest cent.
  [approve] Both functions now call the shared _base helper and the clearance_price function rounds the result as required.

## ground_notest  ->  escalate   esc
prechecks: parses=True import_error=None changed=True claim_asserts_change=True test_exit=0 subtests=(5, 5)
test_out:
    SUBTESTS 5/5
hard_fail: None
checklist (5): Implement a helper function that calculates a 20% discount on a given price. | Ensure that the `staff_price` function uses the helper function to apply the discount. | Ensure that the `clearance_price` function uses the helper function to apply the discount. | Verify that both `staff_price` and `clearance_price` return the correct discounted prices. | Confirm that the implementation does not change the logic or output of either function.
  raw: 1. Implement a helper function that calculates a 20% discount on a given price.
2. Ensure that the `staff_price` function uses the helper function to apply the discount.
3. Ensure that the `clearance_price` function uses the helper function to apply the discount.
4. Verify that both `staff_price` and `clearance_price` return the correct discounted prices.
5. Confirm that the implementation does not change the logic or output of either function.
panel_verdict=escalate  test_verdict=None
  [unsure  ] Implement a helper function that calculates a 20% discount on a given 
             ev: The submission does not implement a helper function that calculates a 20% discount on a given price. The function `staff_price` and `clearance_price` both use `_base(price)`, which applies an 80% disc
  [unsure  ] Ensure that the `staff_price` function uses the helper function to app
             ev: 
  [unsure  ] Ensure that the `clearance_price` function uses the helper function to
             ev: The `clearance_price` function does not use the helper function to apply the discount.
  [unsure  ] Verify that both `staff_price` and `clearance_price` return the correc
             ev: The submission does not provide any test output or evidence to verify the correctness of the `staff_price` and `clearance_price` functions.
  [unsure  ] Confirm that the implementation does not change the logic or output of
             ev: The submission does not provide any automated test output to verify the correctness of the implementation.

## ground  ->  escalate   esc
prechecks: parses=True import_error=None changed=True claim_asserts_change=True test_exit=0 subtests=(5, 5)
test_out:
    SUBTESTS 5/5
hard_fail: None
checklist (5): Implement a helper function that applies a 20% discount to a given price. | Ensure that the `staff_price` function uses the helper function to calculate the discounted price. | Ensure that the `clearance_price` function uses the helper function to calculate the discounted price. | Verify that both `staff_price` and `clearance_price` return the correct discounted prices. | Confirm that the implementation does not change the logic or behavior of the original functions.
  raw: 1. Implement a helper function that applies a 20% discount to a given price.
2. Ensure that the `staff_price` function uses the helper function to calculate the discounted price.
3. Ensure that the `clearance_price` function uses the helper function to calculate the discounted price.
4. Verify that both `staff_price` and `clearance_price` return the correct discounted prices.
5. Confirm that the implementation does not change the logic or behavior of the original functions.
panel_verdict=escalate  test_verdict=approve
  [unsure  ] Implement a helper function that applies a 20% discount to a given pri
             ev: 
  [unsure  ] Ensure that the `staff_price` function uses the helper function to cal
             ev: 
  [unsure  ] Ensure that the `clearance_price` function uses the helper function to
             ev: 
  [met     ] Verify that both `staff_price` and `clearance_price` return the correc
             ev: The `staff_price` and `clearance_price` functions correctly apply a 20% discount and return the expected results.
  [met     ] Confirm that the implementation does not change the logic or behavior 
             ev: The implementation of staff_price and clearance_price functions does not change the logic or behavior of the original functions as they both apply a 20% discount to the input price.