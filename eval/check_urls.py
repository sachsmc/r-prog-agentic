# /// script
# requires-python = ">=3.10"
# ///
"""Check that section URLs in refs/ point at the right place in the online books.

For a random sample of section files, fetch the URL on line 2 and check that
the page loads and, when the URL has an anchor, that the page has that id.

Run:  uv run eval/check_urls.py [--n 20] [--seed 1] [--source ID ...]
"""
from __future__ import annotations

import argparse
import random
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "refs"
# PDF sources have one URL for the whole document, so there is nothing to check per section.
SKIP = {"tidy-data", "layered-grammar", "cheatsheets-pdf"}
_cache: dict[str, tuple[int, str]] = {}


def get(url: str) -> tuple[int, str]:
    if url not in _cache:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (url check)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                _cache[url] = (r.status, r.read().decode("utf-8", errors="replace"))
        except urllib.error.HTTPError as e:
            _cache[url] = (e.code, "")
        except Exception as e:  # noqa: BLE001
            _cache[url] = (0, str(e))
    return _cache[url]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--source", nargs="+")
    args = ap.parse_args()
    files = sorted(p for p in REFS.glob("*/*/*.md")
                   if p.parts[-3] not in SKIP and (not args.source or p.parts[-3] in args.source))
    if not files:
        sys.exit("no section files found. Run `make refs` first.")
    random.Random(args.seed).shuffle(files)
    bad = 0
    for p in files[:args.n]:
        url = p.read_text(encoding="utf-8").split("\n")[1].strip()
        page, _, anchor = url.partition("#")
        status, html = get(page)
        ok = status == 200
        why = f"HTTP {status}"
        if ok and anchor:
            a = urllib.parse.unquote(anchor)
            ok = re.search(rf"""(id|name)=["']{re.escape(a)}["']""", html) is not None
            why = "anchor found" if ok else "anchor missing"
        bad += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {p.relative_to(REFS).as_posix()}  {url}  ({why})")
    print(f"{args.n - bad} of {min(args.n, len(files))} URLs are right")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
