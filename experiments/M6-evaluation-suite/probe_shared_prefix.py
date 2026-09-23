"""A/B prompts that share a long prefix, for testing prefix-cache bleed.

WHY THE FIRST DESIGN WAS TOO WEAK. probe_slot_bleed's original A and B shared
no prefix at all -- one began "Write a Python function...", the other "Explain
what this function does...". Prefix KV caching only engages on a COMMON prefix,
so the mechanism most likely to leak was the one the test could not reach. It
measured slot contention between unrelated prompts, which is worth knowing and
is not the sharp case.

THE HARNESS HAS THE OPPOSITE SHAPE, and that is what makes this matter. Every
rep of a cell sends a multi-thousand-token prompt that is identical except for
the task tail, arms share their whole boilerplate preamble, and those requests
hit concurrent slots repeatedly. A long common prefix, cached and re-served, is
the normal case there -- not the exception.

THE CONSTRUCTION. One realistic script, in three parts:

    HEAD    imports, constants, dataclass, helpers          <- SHARED, long
    MIDDLE  the slugify implementation, or nothing          <- the divergence
    TAIL    code that calls slugify, main()                 <- shared text

    A = HEAD + TAIL + "slugify is missing, write it"
    B = HEAD + MIDDLE(with markers) + TAIL + "explain slugify"

So both prompts open with the same several hundred tokens, then diverge in the
middle rather than at the end. If a slot ever serves a cached prefix with the
wrong continuation's state attached, B's planted identifiers can surface in an
answer to A -- and those identifiers are ones no model writes unprompted.
"""
from __future__ import annotations

MARKER_ID = "_zarquon_pattern"
MARKER_NOTE = "PLUGH-SENTINEL-7731"

HEAD = '''"""Static site builder: turn markdown posts into a dated archive."""
import re
import json
import datetime as dt
from dataclasses import dataclass, field
from pathlib import Path

CONTENT_DIR = Path("content")
OUTPUT_DIR = Path("public")
INDEX_NAME = "index.json"
MAX_SUMMARY_CHARS = 280
DATE_FMT = "%Y-%m-%d"
DRAFT_PREFIX = "_"


@dataclass
class Post:
    title: str
    body: str
    published: dt.date
    tags: list[str] = field(default_factory=list)
    draft: bool = False

    @property
    def year(self) -> int:
        return self.published.year


def read_front_matter(text):
    """Split a leading --- delimited YAML-ish block from the body."""
    if not text.startswith("---"):
        return {}, text
    _, raw, body = text.split("---", 2)
    meta = {}
    for line in raw.strip().splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip()
    return meta, body.strip()


def parse_date(value):
    """Accept an ISO date or fall back to today."""
    try:
        return dt.datetime.strptime(value, DATE_FMT).date()
    except (TypeError, ValueError):
        return dt.date.today()


def summarise(body, limit=MAX_SUMMARY_CHARS):
    """First paragraph, trimmed on a word boundary."""
    para = body.split("\\n\\n", 1)[0].replace("\\n", " ").strip()
    if len(para) <= limit:
        return para
    cut = para[:limit].rsplit(" ", 1)[0]
    return cut + "..."


def load_post(path):
    meta, body = read_front_matter(path.read_text(encoding="utf-8"))
    return Post(
        title=meta.get("title", path.stem.replace("-", " ").title()),
        body=body,
        published=parse_date(meta.get("date")),
        tags=[t for t in meta.get("tags", "").split(",") if t.strip()],
        draft=path.name.startswith(DRAFT_PREFIX),
    )
'''

MIDDLE = f'''

def slugify(title):
    # {MARKER_NOTE}
    return {MARKER_ID}.sub("-", title.lower()).strip("-")
'''

# The compiled pattern sits in HEAD's namespace only when MIDDLE is present, so
# B is self-consistent and A is genuinely missing one function.
MIDDLE_DECL = f'\n{MARKER_ID} = re.compile(r"[^a-z0-9]+")\n'

TAIL = '''

def output_path(post):
    """public/<year>/<slug>.html"""
    return OUTPUT_DIR / str(post.year) / (slugify(post.title) + ".html")


def build_index(posts):
    return [
        {
            "title": p.title,
            "slug": slugify(p.title),
            "date": p.published.strftime(DATE_FMT),
            "tags": p.tags,
            "summary": summarise(p.body),
        }
        for p in posts
        if not p.draft
    ]


def main():
    posts = [load_post(p) for p in sorted(CONTENT_DIR.glob("*.md"))]
    posts.sort(key=lambda p: p.published, reverse=True)
    for post in posts:
        if post.draft:
            continue
        dest = output_path(post)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(post.body, encoding="utf-8")
    index = OUTPUT_DIR / INDEX_NAME
    index.write_text(json.dumps(build_index(posts), indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
'''

A = (
    HEAD + TAIL
    + "\n\nThe function `slugify(title)` is used above but is missing from this "
      "script. It must lowercase the title, replace any run of non-alphanumeric "
      "characters with a single hyphen, and strip leading and trailing hyphens. "
      "Write only that one function. Return only the code."
)

B_RELATED = (
    HEAD + MIDDLE_DECL + MIDDLE + TAIL
    + "\n\nExplain what the `slugify` function in this script does, line by "
      "line, naming the identifiers it uses."
)


def shared_prefix_chars() -> int:
    """How much text the two prompts have in common from the start."""
    n = 0
    for x, y in zip(A, B_RELATED):
        if x != y:
            break
        n += 1
    return n


if __name__ == "__main__":
    print(f"A            {len(A):>6} chars")
    print(f"B_RELATED    {len(B_RELATED):>6} chars")
    print(f"shared prefix{shared_prefix_chars():>6} chars "
          f"({100 * shared_prefix_chars() / len(A):.0f}% of A)")
    print(f"markers: {MARKER_ID!r}, {MARKER_NOTE!r}")
