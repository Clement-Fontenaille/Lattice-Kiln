"""M8 work package 6 / E6: the corpus sweep harness.

Specification: docs/00-design/40-roadmap/03-research-and-evaluation/E6-corpus-digestion.md
Milestone: 08-persistent-work-and-knowledge.md, package 6 -- "Run here; graded
in M9, since E6 is explicitly not graded on task success."

E6's own design: "Small tests first -- a processor reuses one stored finding
and measurably beats one starting cold -- then the corpus sweep." The small
test already exists (test_small.py, on synthetic content). What was missing
is everything else: discovering the real corpus, a plug-in point for the
ingestion a real processor would do, and the sweep loop itself. All of that
is buildable and testable now, without a model -- what needs a real processor
is only the one function this file explicitly stubs (`ingest`), which is
exactly the seam a real invocation (Nemotron, run against `-hf` on rented
H100 time) plugs into later. Building and load-testing the harness now, on
the real 70-THINKING corpus, is what makes that later run cheap to trust
instead of a first contact with unknown plumbing.

E6 is explicit that this corpus is graded against M9's dimensions, "not task
success alone, since the corpus was not produced to serve any one task." A
stub ingestor cannot supply real Validity/Reliability/Pertinence/Scope
verdicts any more than mandate_check.py's stub can supply a real mandate
verdict -- so this harness proves the GRADING PLUMBING reaches every ingested
claim end-to-end, at real corpus scale, while every actual verdict stays
honestly UNASSESSED until a real processor is wired in.
"""
from __future__ import annotations

import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent /
                      "M9-context-governance-measurement"))
from claim_dimensions import assess_validity, reliability_evidence  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
THINKING = REPO_ROOT / "docs" / "70-THINKING"

# 08d-persistent-work-and-knowledge.md and E6-corpus-digestion.md both name
# this exact scope: "the F-numbered findings across topics 07 and 08, the
# I-numbered ideas register." Buffer files (00e-buffer.md) are deliberately
# excluded -- litreview-buffer-workflow's own convention holds them as
# pre-review candidates, not settled findings, and E6 is explicit it is
# digesting *findings*, not the review queue that has not been batch-reviewed
# yet.
CORPUS_SOURCES = [
    THINKING / "07-when-to-decompose" / "00d-findings.md",
    THINKING / "08-when-to-stop" / "00d-findings.md",
    THINKING / "ideas.md",
]

_ENTRY_RE = re.compile(r"^(#{2,3})\s+([FI]\d+)\s*(?:—|--|-)\s*(.+)$")


@dataclass
class CorpusItem:
    item_id: str          # GLOBALLY qualified, e.g. "07-when-to-decompose/F1"
    local_id: str          # as written in the file, e.g. "F1" -- NOT globally unique
    title: str
    body: str              # full entry text, heading to next same-level heading
    source_file: str        # relative to REPO_ROOT, for provenance


def discover_corpus(sources: Optional[list[Path]] = None) -> list[CorpusItem]:
    """Parse `### F<n> — <title>` / `## I<n> — <title>` entries out of the
    named findings/ideas files. Deliberately regex-based, not a markdown
    parser -- the heading shape is simple and stable, and this harness's job
    is discovery + plumbing, not markdown fidelity.

    A real finding from building this harness, not a bug: `F<n>` is scoped
    PER TOPIC, not global -- 07-when-to-decompose/00d-findings.md and
    08-when-to-stop/00d-findings.md each restart at F1. The corpus's own
    `[[F1]]`-style cross-links are presumably resolved the same way (within
    the citing document's own topic), so `item_id` here is qualified by the
    parent directory name to get a store-wide-unique key, and `local_id` keeps
    the as-written form for anything that needs to match the corpus's own
    link syntax.
    """
    items = []
    for path in (sources or CORPUS_SOURCES):
        if not path.is_file():
            continue
        topic = path.parent.name if path.name != "ideas.md" else "ideas"
        text = path.read_text(encoding="utf-8")
        lines = text.split("\n")
        starts = []
        for i, line in enumerate(lines):
            m = _ENTRY_RE.match(line)
            if m:
                starts.append((i, m.group(1), m.group(2), m.group(3).strip()))
        for idx, (line_no, hashes, local_id, title) in enumerate(starts):
            body_start = line_no + 1
            body_end = starts[idx + 1][0] if idx + 1 < len(starts) else len(lines)
            body = "\n".join(lines[body_start:body_end]).strip()
            items.append(CorpusItem(item_id=f"{topic}/{local_id}", local_id=local_id,
                                    title=title, body=body,
                                    source_file=str(path.relative_to(REPO_ROOT))))
    return items


# The ingestion seam. A real one reads `item.body`, decides what it supports
# well enough to write, and returns claim content -- this is cognition,
# 08-persistent-work-and-knowledge.md's own reason package 6 stayed
# unbuilt ("needs a processor to do the ingesting").
Ingestor = Callable[[CorpusItem], dict]


def stub_ingestor(item: CorpusItem) -> dict:
    """Writes bookkeeping only -- title, item_id, source, a truncated body
    preview -- and does NOT attempt to extract a claim's substance, because
    doing that honestly requires reading and judging the argument, which is
    exactly the reasoning this stub does not have. Mirrors mandate_check.py's
    stub_checker and failure_modes.py's stub discipline: a stub that produced
    a confident-looking extraction would be indistinguishable afterward from
    a real one that actually read the entry.
    """
    return {
        "kind": "corpus_entry_bookkeeping",
        "item_id": item.item_id,
        "title": item.title,
        "source_file": item.source_file,
        "body_preview": item.body[:200],
        "body_length_chars": len(item.body),
    }


@dataclass
class SweepReport:
    items_ingested: int
    total_ingest_s: float
    claim_ids: list
    dimension_plumbing_reached: int   # how many ingested claims got a dimension pass
    deletion_probe_s: Optional[float]
    deletion_probe_count: int


def run_sweep(substrate, items: list[CorpusItem], *,
             ingestor: Optional[Ingestor] = None,
             run_deletion_probe: bool = True,
             deletion_probe_n: int = 10) -> SweepReport:
    """Ingests every item as an Observation (never higher -- see stub_ingestor's
    docstring on why a stub cannot justify a gated type-5 write), then runs
    each resulting claim through M9's claim-dimension seam to prove the
    grading plumbing reaches real corpus-scale content, not just test_small.py's
    two synthetic claims.

    `run_deletion_probe`: E6's own "what it also produces" -- the first corpus
    large enough to ask whether incremental deletion (12-knowledge-model.md,
    `sweep_from`) stays cheap. Probes it on a subset of what was just
    ingested rather than the whole corpus, since the timing question is about
    per-item cost, not this run's total wall clock.
    """
    fn = ingestor or stub_ingestor
    claim_ids = []
    t0 = time.monotonic()
    for item in items:
        content = fn(item)
        claim = substrate.knowledge.write_observation(content, source="e6_sweep")
        claim_ids.append(claim.claim_id)
    total_ingest_s = time.monotonic() - t0

    dimension_reached = 0
    for cid in claim_ids:
        claim = substrate.knowledge.read(cid)
        assess_validity(claim)          # stub -- proves the call succeeds at scale
        reliability_evidence(claim)     # real, mechanical
        dimension_reached += 1

    deletion_probe_s = None
    probe_ids = claim_ids[:deletion_probe_n]
    if run_deletion_probe and probe_ids:
        t1 = time.monotonic()
        substrate.knowledge.sweep_from(probe_ids, still_live=set())
        deletion_probe_s = time.monotonic() - t1

    return SweepReport(items_ingested=len(claim_ids), total_ingest_s=total_ingest_s,
                       claim_ids=claim_ids, dimension_plumbing_reached=dimension_reached,
                       deletion_probe_s=deletion_probe_s,
                       deletion_probe_count=len(probe_ids) if run_deletion_probe else 0)
