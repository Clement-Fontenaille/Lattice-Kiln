"""The actual hot path: totals() calls unit_cost once per sku. If throughput
matters, the fix is a batch API here - not a rewrite of unit_cost."""
from prices import unit_cost


def totals(skus):
    return {sku: unit_cost(sku) for sku in skus}
