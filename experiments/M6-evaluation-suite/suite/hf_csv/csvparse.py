"""parse() naively splits on commas and newlines. The task: parse CSV properly -
quoted fields may contain commas and newlines; tolerate a leading BOM, CRLF line
endings, and a trailing blank line."""


def parse(text):
    return [line.split(",") for line in text.splitlines()]
