from pricing import line_price


def total(order):
    """Sum of all line prices in an order."""
    return sum(line_price(li) for li in order["lines"])
