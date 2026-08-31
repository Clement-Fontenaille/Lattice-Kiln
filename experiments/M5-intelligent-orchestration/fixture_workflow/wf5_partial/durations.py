def parse_duration(s):
    """Parse a duration string into total seconds.

    Examples: '45m' -> 2700, '2h' -> 7200, '1h30m' -> 5400, '90s' -> 90,
    '1h2m3s' -> 3723, '' -> 0. Surrounding whitespace is allowed.
    """
    raise NotImplementedError
