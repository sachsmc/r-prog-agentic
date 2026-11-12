"""Retrieval evaluation: recall at 5 for bm25, dense and hybrid search.

Needs refs/ and the index (make refs, make index). Skipped when they are missing.
Run with -s to see the numbers:  uv run --with pytest --with pyyaml --with numpy --with tokenizers pytest -q -s eval
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
import searchlib as sl  # noqa: E402

GOLDEN = yaml.safe_load((ROOT / "eval" / "golden.yml").read_text(encoding="utf-8"))
# CI builds only some of the reference sources (REFS_SUBSET=1). Questions whose
# answers are all in sources that were not built are then left out.
SUBSET = bool(os.environ.get("REFS_SUBSET"))


def questions() -> list[dict]:
    if not SUBSET:
        return GOLDEN
    con = sl.connect()
    paths = [r[0] for r in con.execute("SELECT DISTINCT path FROM chunks")]
    return [g for g in GOLDEN if any(p.startswith(a) for p in paths for a in g["a"])]


def test_golden_set_shape():
    kinds = [g["kind"] for g in GOLDEN]
    assert len(GOLDEN) >= 40
    assert kinds.count("mismatch") >= 10
    assert kinds.count("exact") >= 10
    assert all(g["a"] for g in GOLDEN)


def full_corpus() -> bool:
    return sl.DB.exists() and (sl.REFS / "adv-r").is_dir()


def hit(g: dict, mode: str, k: int = 5) -> bool:
    hits, used = sl.search(g["q"], k=k, mode=mode)
    assert used == mode, f"{mode} search is not available"
    return any(h["path"].startswith(a) for h in hits for a in g["a"])


def recall(mode: str, kind: str | None = None) -> float:
    items = [g for g in questions() if kind is None or g["kind"] == kind]
    return sum(hit(g, mode) for g in items) / len(items)


@pytest.mark.skipif(not full_corpus() or SUBSET, reason="needs every reference source and the index")
def test_golden_answers_exist():
    """Every answer prefix points at something that is in the index."""
    con = sl.connect()
    paths = [r[0] for r in con.execute("SELECT DISTINCT path FROM chunks")]
    missing = [a for g in GOLDEN for a in g["a"] if not any(p.startswith(a) for p in paths)]
    assert not missing, f"answer prefixes that match nothing: {missing}"


@pytest.mark.skipif(not full_corpus(), reason="refs/ or the index is not built")
def test_recall_at_5():
    if not sl.VECTORS.exists() or sl.load_encoder() is None:
        r = recall("bm25")
        print(f"\nrecall@5 bm25 {r:.2f} (dense index not built)")
        assert r >= 0.7
        return
    table = {m: {k or "all": recall(m, k) for k in (None, "mismatch", "exact", "general")}
             for m in ("bm25", "dense", "hybrid")}
    print("\nrecall@5        all  mismatch  exact  general")
    for m, row in table.items():
        print(f"  {m:<8} {row['all']:>8.2f} {row['mismatch']:>9.2f} {row['exact']:>6.2f} {row['general']:>8.2f}")
    best_single = max(table["bm25"]["all"], table["dense"]["all"])
    assert table["hybrid"]["all"] >= best_single, "hybrid is worse than the better single mode"
    assert table["hybrid"]["all"] >= 0.8
