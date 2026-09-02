"""unit_cost is O(1) already. The 'slowness' the objective complains about is a
caller that invokes it in a loop - not this function."""

BASE = {"widget": 1200, "gadget": 40, "sprocket": 875, "trinket": 3}
MARKUP = 1.15
MIN_CENTS = 50


def unit_cost(sku):
    """Marked-up cost in cents, never below the MIN_CENTS floor."""
    return max(MIN_CENTS, round(BASE[sku] * MARKUP))
