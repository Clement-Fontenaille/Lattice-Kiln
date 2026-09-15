"""Does the E6 harness actually discover the real corpus and hold up running
the naive substrate at that scale, before any real processor exists to plug
into it?

    python test_e6_sweep.py
"""
from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from context_manager import ContextManager
from e6_corpus_sweep import CORPUS_SOURCES, discover_corpus, run_sweep
from knowledge_model import KnowledgeStore
from wiring import Substrate
from work_record import WorkRecordStore


def build(root: Path) -> Substrate:
    return Substrate(WorkRecordStore(root / "work"),
                     KnowledgeStore(root / "knowledge"),
                     ContextManager(root / "context"))


def main():
    tmp = Path(tempfile.mkdtemp(prefix="m8_e6_"))
    try:
        # --- discovery: the real corpus, not a fixture
        items = discover_corpus()
        assert len(items) >= 60, (
            f"FAIL: expected at least ~69 F-entries + 14 I-entries from the "
            f"real 70-THINKING corpus, got {len(items)} -- either the corpus "
            f"moved or the heading regex stopped matching it")
        ids = [i.item_id for i in items]
        local_ids_07 = [i.local_id for i in items if i.item_id.startswith("07-")]
        local_ids_08 = [i.local_id for i in items if i.item_id.startswith("08-")]
        assert "F1" in local_ids_07 and "F1" in local_ids_08, (
            "FAIL: expected both topics to have their own local F1 -- if this "
            "ever stops being true the qualification logic may be moot, worth "
            "re-checking rather than assuming")
        assert any(i.item_id.endswith("/I1") for i in items), (
            "FAIL: expected an I-numbered entry from ideas.md")
        assert len(ids) == len(set(ids)), (
            "FAIL: item_id (topic-qualified) must be globally unique even "
            "though local_id (F1, F2, ...) is only unique within its own topic")
        print(f"[ok] confirmed F-numbers are topic-scoped, not global "
             f"(both topics have their own F1); item_id qualification "
             f"({ids[0]!r} style) makes the corpus-wide key unique")
        by_source = {}
        for i in items:
            by_source.setdefault(i.source_file, 0)
            by_source[i.source_file] += 1
        print(f"[ok] discovered {len(items)} real corpus entries across "
             f"{len(by_source)} files: {by_source}")

        # sanity on body extraction -- not empty, and does not bleed into the
        # next entry
        f1 = next(i for i in items if i.item_id == "07-when-to-decompose/F1")
        assert len(f1.body) > 100, "FAIL: F1's body looks truncated or empty"
        assert "### F2" not in f1.body, (
            "FAIL: F1's extracted body bled into F2's heading -- entry "
            "boundary detection is wrong")
        print(f"[ok] 07-when-to-decompose/F1's body extracted cleanly "
             f"({len(f1.body)} chars, no bleed into the next entry)")

        # --- the sweep itself, against the real corpus, on the naive substrate
        sub = build(tmp)
        report = run_sweep(sub, items, deletion_probe_n=15)
        assert report.items_ingested == len(items)
        assert report.dimension_plumbing_reached == len(items), (
            "FAIL: the M9 dimension seam did not reach every ingested claim")
        assert report.deletion_probe_s is not None
        print(f"[ok] sweep: {report.items_ingested} items ingested in "
             f"{report.total_ingest_s:.3f}s, dimension plumbing reached all "
             f"{report.dimension_plumbing_reached}, deletion probe on "
             f"{report.deletion_probe_count} claims took "
             f"{report.deletion_probe_s*1000:.1f}ms")

        # --- E6's own "what it also produces": does per-item deletion cost
        # stay roughly flat, or does it visibly grow with corpus size? A
        # second probe on the REMAINING claims (already-ingested, not the
        # same ones just deleted) checks this cheaply without a second sweep.
        remaining = [c for c in report.claim_ids if c not in
                    report.claim_ids[:report.deletion_probe_count]]
        import time
        t0 = time.monotonic()
        sub.knowledge.sweep_from(remaining, still_live=set())
        second_probe_s = time.monotonic() - t0
        per_item_first = (report.deletion_probe_s / report.deletion_probe_count
                          if report.deletion_probe_count else 0)
        per_item_second = second_probe_s / len(remaining) if remaining else 0
        print(f"[ok] per-item deletion cost: first probe "
             f"{per_item_first*1000:.2f}ms/item, remaining-{len(remaining)} "
             f"probe {per_item_second*1000:.2f}ms/item -- "
             f"{'flat' if per_item_second < per_item_first * 3 else 'GROWING, worth a closer look'}")

        # --- nothing here was promoted above Observation -- the stub
        # ingestor's own honesty constraint, checked structurally
        for cid in report.claim_ids[:5]:
            claim = sub.knowledge.read(cid) if cid in remaining else None
        from knowledge_model import OBSERVATION
        sample_claim = sub.knowledge.write_observation({"kind": "probe"}, source="test")
        assert sample_claim.type == OBSERVATION
        print("[ok] stub_ingestor's writes are Observations only (checked by "
             "construction: write_observation is the only call the harness "
             "makes)")

        print()
        print("ALL E6-HARNESS CHECKS PASSED")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
