def line_price(item):
    """Price for one order line: unit price times quantity."""
    return item["unit_price"]  # BUG: ignores item["qty"]
