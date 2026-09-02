"""safe_name() currently trusts its input. The task: sanitize a user-supplied
filename before it is joined to a directory. Reject traversal, absolute paths,
null bytes and Windows reserved names (raise ValueError); strip trailing dots and
spaces; leave an ordinary name like 'my.file.txt' untouched."""


def safe_name(name):
    return name
