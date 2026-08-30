def to_int(s: str) -> int:
    """Parse a decimal string to an int, tolerating leading zeros and surrounding
    whitespace. Raises ValueError on anything that is not a decimal integer."""
    return int(s.strip(), 10)
