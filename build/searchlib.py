"""Shared code for build_index.py, bin/search and bin/cite-check.

Standard library only at import time. numpy and tokenizers are imported only
when dense search is used, so BM25 search works without them.
"""
from __future__ import annotations

import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "refs"
COURSE = ROOT / "course"
INDEX = ROOT / ".index"
DB = INDEX / "search.sqlite"
VECTORS = INDEX / "vectors.npy"
MODEL_DIR = INDEX / "model"
MODEL_NAME = "minishlab/potion-retrieval-32M"   # static embeddings, MIT licence, CPU only
TARGET_CHARS = 1200                             # about 300 tokens
RRF_K = 60
COURSE_BOOST = 1.1

ADDRESS = re.compile(r"(?<![\w/.-])((?:[\w.-]+/)+[\w.-]+):L(\d+)(?:-L?(\d+))?")


# ---------------------------------------------------------------- addresses

def resolve(address_path: str) -> Path | None:
    """File for the path part of an address. Reference addresses are relative
    to refs/. Course addresses start with course/."""
    p = address_path[:-3] if address_path.endswith(".md") else address_path
    for base in (ROOT, REFS):
        cand = base / (p + ".md")
        if cand.is_file() and (base == REFS or p.startswith("course/")):
            return cand
    return None


def address_of(path: Path) -> str:
    rel = path.relative_to(REFS) if REFS in path.parents else path.relative_to(ROOT)
    return rel.with_suffix("").as_posix()


# ---------------------------------------------------------------- chunking

def corpus_files() -> list[tuple[str, Path]]:
    """(source id, file) for everything that gets indexed."""
    out: list[tuple[str, Path]] = []
    if COURSE.is_dir():
        out.append(("course", COURSE / "syllabus.md"))
        for sub in ("lectures", "exercises", "exercises/solutions"):
            out += [("course", p) for p in sorted((COURSE / sub).glob("*.md"))]
    if REFS.is_dir():
        for src in sorted(p for p in REFS.iterdir() if p.is_dir()):
            out += [(src.name, p) for p in sorted(src.glob("*/*.md"))]
            out += [(src.name, p) for p in sorted(src.glob("*/tables/*.md"))]
    return [(s, p) for s, p in out if p.is_file()]


def chunk_file(source: str, path: Path) -> list[dict]:
    """Chunks of about TARGET_CHARS that never cross the file. Cuts fall on
    blank lines or headings, outside code blocks where possible."""
    lines = path.read_text(encoding="utf-8").split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if source == "course":
        base = "Course > " + (lines[0].lstrip("# ").strip() if lines else path.stem)
        url, first = "", 1
    else:
        base = lines[0].lstrip("# ").strip()
        url, first = (lines[1].strip() if len(lines) > 1 else ""), 4
    chunks: list[dict] = []
    cur: list[tuple[int, str]] = []
    size = 0
    fence = False
    sub = ""
    cur_sub = ""

    def flush() -> None:
        nonlocal cur, size, cur_sub
        body = [(n, t) for n, t in cur if t.strip()]
        if body:
            heading = base + (f" > {cur_sub}" if cur_sub and cur_sub not in base else "")
            chunks.append(dict(source=source, path=address_of(path), start=body[0][0], end=body[-1][0],
                               heading=heading, url=url, text="\n".join(t for _, t in cur).strip()))
        cur, size = [], 0
        cur_sub = sub

    for n, text in enumerate(lines[first:], first + 1):
        is_fence = re.match(r"^\s*(`{3,}|~{3,})", text) is not None
        is_head = not fence and re.match(r"^#{1,6}\s", text) is not None
        if is_head:
            if size > TARGET_CHARS // 3:
                flush()
            sub = text.lstrip("# ").strip()
            if not cur:
                cur_sub = sub
        elif not fence and not text.strip() and size >= TARGET_CHARS:
            flush()
        elif size >= TARGET_CHARS * 2.5:           # a very long code block or list
            flush()
        cur.append((n, text))
        size += len(text) + 1
        if is_fence:
            fence = not fence
    flush()
    return chunks


# ---------------------------------------------------------------- lexical

STOP = set("a an and are as at be but by can do does for from how i if in into is it my of on or so "
           "that the their then there these this to up was what when where which who why will with "
           "you your me we want use using get make way r".split())


def fts_query(query: str) -> str:
    """An FTS5 query: every word or identifier as an OR term. Identifiers such
    as pivot_longer or read.csv become phrases, so their parts must be adjacent."""
    terms = re.findall(r"[A-Za-z0-9_.]+(?:::[A-Za-z0-9_.]+)?|%[^%\s]+%|\|>|<-|\[\[|\$", query)
    words = []
    for t in terms:
        t = t.strip("._")
        if not t or (t.lower() in STOP and len(terms) > 1):
            continue
        words.append('"' + t.replace('"', "") + '"')
    return " OR ".join(dict.fromkeys(words))


def connect() -> sqlite3.Connection:
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def bm25_ranking(con: sqlite3.Connection, query: str, sources: list[str] | None, limit: int) -> list[int]:
    q = fts_query(query)
    if not q:
        return []
    sql = ("SELECT c.id FROM fts JOIN chunks c ON c.id = fts.rowid WHERE fts MATCH ? "
           + (f"AND c.source IN ({','.join('?' * len(sources))}) " if sources else "")
           + "ORDER BY bm25(fts, 3.0, 1.0) LIMIT ?")
    try:
        rows = con.execute(sql, [q, *(sources or []), limit]).fetchall()
    except sqlite3.OperationalError:
        return []
    return [r[0] for r in rows]


# ---------------------------------------------------------------- dense

class QueryEncoder:
    """Embeds a query the way the model2vec model does: the mean of the token
    vectors, normalised. Needs only numpy and tokenizers, so it loads fast.
    build_index.py writes the files it reads."""

    def __init__(self) -> None:
        import json

        import numpy as np
        from tokenizers import Tokenizer
        self.np = np
        self.tok = Tokenizer.from_file(str(MODEL_DIR / "tokenizer.json"))
        self.tok.no_truncation()
        self.unk = json.loads((MODEL_DIR / "encoder.json").read_text(encoding="utf-8"))["unk_id"]
        self.emb = np.load(MODEL_DIR / "embeddings.npy", mmap_mode="r")

    def encode(self, text: str):
        np = self.np
        ids = [i for i in self.tok.encode(text, add_special_tokens=False).ids if i != self.unk]
        if not ids:
            return np.zeros(self.emb.shape[1], dtype="float32")
        v = np.asarray(self.emb[np.array(sorted(set(ids)))], dtype="float32")
        # weight repeated tokens as the mean over all tokens would
        counts = np.array([ids.count(i) for i in sorted(set(ids))], dtype="float32")
        v = (v * counts[:, None]).sum(axis=0) / counts.sum()
        return v / (np.linalg.norm(v) or 1.0)


def load_encoder():
    """The query encoder, or None if its files or packages are missing."""
    if not all((MODEL_DIR / f).exists() for f in ("tokenizer.json", "encoder.json", "embeddings.npy")):
        return None
    try:
        return QueryEncoder()
    except Exception:  # noqa: BLE001
        return None


def dense_ranking(con: sqlite3.Connection, query: str, sources: list[str] | None, limit: int) -> list[int] | None:
    if not VECTORS.exists():
        return None
    enc = load_encoder()
    if enc is None:
        return None
    import numpy as np
    vecs = np.load(VECTORS, mmap_mode="r")
    q = enc.encode(query)
    scores = np.asarray(vecs @ q, dtype="float32")
    if sources:
        ids = [r[0] for r in con.execute(
            f"SELECT id FROM chunks WHERE source IN ({','.join('?' * len(sources))})", sources)]
        mask = np.full(scores.shape, -np.inf, dtype="float32")
        idx = np.array(ids, dtype="int64") - 1
        mask[idx] = scores[idx]
        scores = mask
    top = np.argsort(-scores)[:limit]
    return [int(i) + 1 for i in top if np.isfinite(scores[i])]


# ---------------------------------------------------------------- fusion

def search(query: str, sources: list[str] | None = None, k: int = 8, mode: str = "hybrid",
           depth: int = 50) -> tuple[list[dict], str]:
    """Top k chunks and the mode that was really used."""
    con = connect()
    bm = bm25_ranking(con, query, sources, depth) if mode in ("hybrid", "bm25") else []
    dn = None
    if mode in ("hybrid", "dense"):
        dn = dense_ranking(con, query, sources, depth)
        if dn is None:
            mode = "bm25"
            if not bm:
                bm = bm25_ranking(con, query, sources, depth)
    dn = dn or []
    bm_rank = {cid: i + 1 for i, cid in enumerate(bm)}
    dn_rank = {cid: i + 1 for i, cid in enumerate(dn)}
    score: dict[int, float] = {}
    for ranks in (bm_rank, dn_rank):
        for cid, r in ranks.items():
            score[cid] = score.get(cid, 0.0) + 1.0 / (RRF_K + r)
    if not score:
        return [], mode
    rows = {r["id"]: dict(r) for r in con.execute(
        f"SELECT * FROM chunks WHERE id IN ({','.join('?' * len(score))})", list(score))}
    for cid in score:
        if rows[cid]["source"] == "course":
            score[cid] *= COURSE_BOOST
    order = sorted(score, key=lambda c: (-score[c], c))[:k]
    hits = []
    for cid in order:
        h = rows[cid]
        h["bm25_rank"] = bm_rank.get(cid)
        h["dense_rank"] = dn_rank.get(cid)
        h["score"] = round(score[cid], 5)
        h["address"] = f"{h['path']}:L{h['start']}-L{h['end']}"
        hits.append(h)
    return hits, mode
