"""Naive context assembly - v0 implementation of docs/10-technical/07.

Deliberately poor: no embeddings, no summaries, no history, no model calls.
Deterministic. Emits a full selection trace. Milestone 7 measures against this
and is expected to REPLACE it, not extend it.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ~4 chars/token is close enough for a budget guard on this model family.
CHARS_PER_TOKEN = 4
DEFAULT_TOKEN_BUDGET = 8000
README_CHAR_CAP = 2000
TREE_DEPTH = 3
CONTENT_SCAN_CAP = 60  # files whose contents we substring-scan in step 3

_STOPWORDS = {
    "the", "a", "an", "and", "or", "to", "of", "in", "on", "for", "with", "is",
    "are", "be", "that", "this", "it", "as", "at", "by", "from", "add", "make",
    "should", "must", "when", "if", "so", "into", "use", "using", "given",
}
_SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", ".pytest_cache"}


@dataclass
class BundleEntry:
    source_ref: str
    text: str
    included_fully: bool

    @property
    def chars(self) -> int:
        return len(self.text)


@dataclass
class ContextBundle:
    objective: str
    entries: list[BundleEntry] = field(default_factory=list)
    trace: dict[str, Any] = field(default_factory=dict)

    @property
    def token_estimate(self) -> int:
        return sum(e.chars for e in self.entries) // CHARS_PER_TOKEN

    def render(self) -> str:
        parts = []
        for e in self.entries:
            tag = "" if e.included_fully else "  [truncated]"
            parts.append(f"----- {e.source_ref}{tag} -----\n{e.text}")
        return "\n\n".join(parts)


def _terms(objective: str) -> list[str]:
    raw = re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", objective.lower())
    seen, out = set(), []
    for t in raw:
        if t not in _STOPWORDS and t not in seen:
            seen.add(t)
            out.append(t)
    return out


def _tree(root: Path, depth: int) -> list[tuple[str, int]]:
    out = []
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if any(part in _SKIP_DIRS for part in rel.parts):
            continue
        if len(rel.parts) > depth:
            continue
        if p.is_file():
            out.append((rel.as_posix(), p.stat().st_size))
    return out


def assemble(objective: str, repo_root: str | Path, *,
             path_hints: list[str] | None = None,
             token_budget: int = DEFAULT_TOKEN_BUDGET,
             prior_conclusion: str | None = None) -> ContextBundle:
    root = Path(repo_root).resolve()
    budget_chars = token_budget * CHARS_PER_TOKEN
    b = ContextBundle(objective=objective)
    used = 0
    trace: dict[str, Any] = {"terms": [], "hints": list(path_hints or []),
                             "matched": [], "dropped_for_budget": [], "truncated": None,
                             "token_budget": token_budget}

    def add(ref: str, text: str) -> bool:
        nonlocal used
        room = budget_chars - used
        if room <= 0:
            trace["dropped_for_budget"].append(ref)
            return False
        if len(text) <= room:
            b.entries.append(BundleEntry(ref, text, True))
            used += len(text)
            return True
        b.entries.append(BundleEntry(ref, text[:room], False))
        used += room
        trace["truncated"] = ref
        return False

    # step 1 - always include
    add("OBJECTIVE", objective)
    readme = next((p for p in root.iterdir() if p.name.lower().startswith("readme")), None)
    if readme and readme.is_file():
        add(f"{readme.name} (capped)", readme.read_text(encoding="utf-8", errors="replace")[:README_CHAR_CAP])
    tree = _tree(root, TREE_DEPTH)
    add("FILE TREE", "\n".join(f"{path}  ({size}B)" for path, size in tree))

    if prior_conclusion is not None:
        add("PRIOR PROCESSOR CONCLUSION (review mode)", prior_conclusion)

    # step 2 / 3 - hint files, else naive substring match
    candidates: list[tuple[int, str]] = []
    if path_hints:
        for i, h in enumerate(path_hints):
            candidates.append((-(10_000 - i), h))  # preserve caller order, high priority
    else:
        terms = _terms(objective)
        trace["terms"] = terms
        files = [p for p, _ in tree]
        scanned = 0
        for rel in files:
            fp = root / rel
            score = sum(rel.lower().count(t) for t in terms)
            if scanned < CONTENT_SCAN_CAP and fp.is_file() and fp.stat().st_size < 200_000:
                try:
                    body = fp.read_text(encoding="utf-8", errors="replace").lower()
                    score += sum(body.count(t) for t in terms)
                except OSError:
                    pass
                scanned += 1
            if score > 0:
                candidates.append((-score, rel))

    for negscore, rel in sorted(candidates, key=lambda c: (c[0], c[1])):
        fp = root / rel
        if not fp.is_file():
            trace["matched"].append({"path": rel, "score": -negscore, "state": "missing"})
            continue
        text = fp.read_text(encoding="utf-8", errors="replace")
        ok = add(f"FILE {rel}", text)
        trace["matched"].append({"path": rel, "score": -negscore,
                                 "state": "included" if ok else ("truncated" if trace["truncated"] == f"FILE {rel}" else "dropped")})

    b.trace = trace
    return b
