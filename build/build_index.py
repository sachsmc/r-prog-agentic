# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy>=1.26", "model2vec>=0.6"]
# ///
"""Build the search index in .index/ from course/ and refs/.

Writes search.sqlite (chunks and an FTS5 table for BM25) and vectors.npy
(one normalised embedding per chunk). With --no-dense only the BM25 part is
built, and `search` then runs in BM25 mode.

Run:  uv run build/build_index.py [--no-dense]        (or: make index)
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import searchlib as sl  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--no-dense", action="store_true", help="skip the embedding model and vectors")
    args = ap.parse_args()
    t0 = time.time()

    files = sl.corpus_files()
    if not files:
        sys.exit("error: nothing to index. course/ is missing.")
    chunks: list[dict] = []
    for source, path in files:
        chunks += sl.chunk_file(source, path)
    by_source: dict[str, int] = {}
    for c in chunks:
        by_source[c["source"]] = by_source.get(c["source"], 0) + 1

    sl.INDEX.mkdir(exist_ok=True)
    for old in (sl.DB, sl.VECTORS):
        old.unlink(missing_ok=True)
    con = sqlite3.connect(sl.DB)
    con.executescript("""
        CREATE TABLE chunks (id INTEGER PRIMARY KEY, source TEXT, path TEXT, start INTEGER,
                             end INTEGER, heading TEXT, url TEXT, text TEXT);
        CREATE INDEX chunks_source ON chunks (source);
        CREATE VIRTUAL TABLE fts USING fts5 (heading, text, tokenize = "porter unicode61");
    """)
    for i, c in enumerate(chunks, 1):
        con.execute("INSERT INTO chunks VALUES (?,?,?,?,?,?,?,?)",
                    (i, c["source"], c["path"], c["start"], c["end"], c["heading"], c["url"], c["text"]))
        con.execute("INSERT INTO fts (rowid, heading, text) VALUES (?,?,?)", (i, c["heading"], c["text"]))
    con.commit()
    con.close()
    print(f"[index] {len(chunks)} chunks from {len(files)} files: "
          + ", ".join(f"{k} {v}" for k, v in sorted(by_source.items())), flush=True)
    if "course" in by_source and len(by_source) == 1:
        print("[index] refs/ is not built, so only the course material is indexed. Run `make refs` to add the books.")

    if args.no_dense:
        print(f"[index] BM25 only (--no-dense). Done in {time.time() - t0:.1f}s")
        return 0
    try:
        import json
        import shutil

        import numpy as np
        from model2vec import StaticModel
        model = StaticModel.from_pretrained(sl.MODEL_NAME)
        if model.weights is not None or model.token_mapping is not None:
            raise RuntimeError("this model needs token weights, which the query encoder does not support")
        vecs = model.encode([c["heading"] + "\n" + c["text"] for c in chunks]).astype("float32")
        vecs /= np.maximum(np.linalg.norm(vecs, axis=1, keepdims=True), 1e-9)
        np.save(sl.VECTORS, vecs)
        # Files for the light query encoder in searchlib.py.
        shutil.rmtree(sl.MODEL_DIR, ignore_errors=True)
        sl.MODEL_DIR.mkdir(parents=True)
        model.tokenizer.save(str(sl.MODEL_DIR / "tokenizer.json"))
        np.save(sl.MODEL_DIR / "embeddings.npy", np.asarray(model.embedding, dtype="float16"))
        (sl.MODEL_DIR / "encoder.json").write_text(
            json.dumps({"model": sl.MODEL_NAME, "unk_id": model.unk_token_id}), encoding="utf-8")
        probe = "how do I reshape data from wide to long"
        a = model.encode([probe])[0]
        b = sl.QueryEncoder().encode(probe)
        cos = float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))
        if cos < 0.999:
            raise RuntimeError(f"query encoder does not match the model (cosine {cos:.4f})")
        print(f"[index] embeddings: {vecs.shape[0]} x {vecs.shape[1]} with {sl.MODEL_NAME}")
    except Exception as e:  # noqa: BLE001
        sl.VECTORS.unlink(missing_ok=True)
        print(f"[index] could not build embeddings ({type(e).__name__}: {e}).")
        print("[index] search will use BM25 only. Run `make index` again when you are online.")
    print(f"[index] done in {time.time() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
