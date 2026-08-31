def staff_price(price):
    """20% off, exact (no rounding)."""
    return price * 0.8


def clearance_price(price):
    """20% off, rounded to cents."""
    return round(price * 0.8, 2)
