# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6", "pypdf>=4"]
# ///
"""Fetch the reference sources at their pins and build refs/.

Layout: refs/<source>/<NN-chapter>/<NN-section>.md, one sentence or code line
per line. The line numbers of those files are the citation IDs, so a rebuild
from the same pins gives the same bytes (except build_date in meta.json).

Run:  uv run build/fetch_refs.py [--only ID ...] [--offline]     (or: make refs)
"""
from __future__ import annotations

import argparse
import datetime as dt
import io
import json
import re
import shutil
import sys
import tarfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from parsers import bookdown, pdf, texinfo  # noqa: E402
from parsers.common import Chapter  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "refs"
CACHE = ROOT / ".cache" / "refs-src"
PARSERS = {"bookdown": bookdown.parse, "texinfo": texinfo.parse, "pdf": pdf.parse}
TEXT_EXT = {".rmd", ".qmd", ".md", ".yml", ".yaml", ".texi", ".txt", ".bib"}
MAX_LINES = 400
UA = {"User-Agent": "r-course-refs-builder"}


def log(msg: str) -> None:
    print(msg, flush=True)


class FetchError(Exception):
    pass


def download(url: str, tries: int = 3) -> bytes:
    last = None
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last = e
            time.sleep(2 * (attempt + 1))
    raise FetchError(f"could not download {url}: {last}")


def fetch(src: dict, offline: bool) -> Path:
    """Download the source at its pin into the cache. Returns the folder."""
    dest = CACHE / f"{src['id']}-{src['pin'][:12]}"
    done = dest / ".complete"
    if done.exists():
        return dest
    if offline:
        raise FetchError(f"{src['id']} is not in the cache and --offline was given")
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    repo, pin = src["upstream"], src["pin"]
    if src.get("fetch", "tarball") == "tarball":
        data = download(f"https://github.com/{repo}/archive/{pin}.tar.gz")
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
            for m in tar.getmembers():
                parts = Path(m.name).parts[1:]
                # top-level text files only: that is where book chapters live
                if not m.isfile() or len(parts) != 1 or Path(parts[0]).suffix.lower() not in TEXT_EXT:
                    continue
                (dest / parts[0]).write_bytes(tar.extractfile(m).read())
    else:
        for f in src["files"]:
            url = f"https://raw.githubusercontent.com/{repo}/{pin}/{urllib.parse.quote(f)}"
            out = dest / f
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(download(url))
    done.write_text("ok", encoding="utf-8")
    return dest


# ---------------------------------------------------------------- writing

def split_long(lines: list[str]) -> list[list[str]]:
    """Cut a section into parts of at most about MAX_LINES lines. Cuts go
    before a heading when there is one, otherwise at a blank line outside code."""
    if len(lines) <= MAX_LINES:
        return [lines]
    safe: list[tuple[int, bool]] = []        # (index, is_heading) of possible cut points
    fence = None
    for i, ln in enumerate(lines):
        m = re.match(r"^\s*(`{3,}|~{3,})", ln)
        if m:
            fence = None if fence else m.group(1)
            continue
        if fence is None:
            if re.match(r"^#{3,6}\s", ln):
                safe.append((i, True))
            elif ln == "" and i + 1 < len(lines) and not re.match(r"^#{3,6}\s", lines[i + 1]):
                safe.append((i + 1, False))
    parts: list[list[str]] = []
    start = 0
    while len(lines) - start > MAX_LINES:
        window = [(i, h) for i, h in safe if start + MAX_LINES // 2 <= i <= start + MAX_LINES]
        heads = [i for i, h in window if h]
        if heads:
            cut = heads[-1]
        elif window:
            cut = window[-1][0]
        else:
            later = [i for i, _ in safe if i > start + MAX_LINES]
            if not later:
                break
            cut = later[0]
        parts.append(lines[start:cut])
        start = cut
    parts.append(lines[start:])
    return [[*p] for p in parts if any(x.strip() for x in p)]


TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?\s*$")


def pull_tables(lines: list[str]) -> tuple[list[str], list[list[str]]]:
    """Move pipe tables out of the text. Returns the text with pointer
    placeholders ("\\x00TABLE n") and the tables."""
    out: list[str] = []
    tables: list[list[str]] = []
    fence = None
    i = 0
    while i < len(lines):
        ln = lines[i]
        m = re.match(r"^\s*(`{3,}|~{3,})", ln)
        if m:
            fence = None if fence else m.group(1)
        if fence is None and "|" in ln and i + 1 < len(lines) and TABLE_SEP.match(lines[i + 1]):
            j = i + 2
            while j < len(lines) and "|" in lines[j] and lines[j].strip():
                j += 1
            if j < len(lines) and re.match(r"^\s*(Table:|:)\s", lines[j]):
                j += 1
            tables.append(lines[i:j])
            out.append(f"\x00TABLE {len(tables)}")
            i = j
            continue
        out.append(ln)
        i += 1
    return out, tables


def write_source(src: dict, chapters: list[Chapter]) -> dict:
    out = REFS / src["id"]
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    pin_note = f"source: {src['upstream']}@{src['pin'][:12]}"
    toc = [f"# {src['title']}", "", f"Source id: `{src['id']}`. Online: <{src['url']}>", ""]
    n_sections = n_tables = n_lines = 0
    width = 3 if len(chapters) > 99 else 2
    for ci, ch in enumerate(chapters):
        cdir = f"{ci:0{width}d}-{ch.slug}"
        (out / cdir).mkdir()
        toc.append(f"- {ch.title}: `{src['id']}/{cdir}/`")
        files: list[tuple[str, str, str, list[str]]] = []
        for s in ch.sections:
            body, tables = pull_tables(s.lines)
            parts = split_long(body)
            for pi, part in enumerate(parts):
                slug = s.slug if pi == 0 else f"{s.slug}-part-{pi + 1}"
                title = s.title if pi == 0 else f"{s.title} (part {pi + 1})"
                files.append((slug, title, s, part, tables))
        offset = 0 if files and files[0][0] == "intro" else 1
        for fi, (slug, title, s, part, tables) in enumerate(files):
            name = f"{fi + offset:02d}-{slug}"
            path_title = " > ".join(dict.fromkeys([src["title"], ch.title, title]))
            body: list[str] = []
            for ln in part:
                m = re.match(r"^\x00TABLE (\d+)$", ln)
                if m:
                    k = int(m.group(1))
                    (out / cdir / "tables").mkdir(exist_ok=True)
                    tname = f"{name}-t{k}.md"
                    thead = [f"# {path_title} > table {k}", s.url, f"{pin_note} {s.src}", ""]
                    (out / cdir / "tables" / tname).write_text(
                        "\n".join(thead + tables[k - 1]) + "\n", encoding="utf-8", newline="\n")
                    body.append(f"[table: {src['id']}/{cdir}/tables/{tname}]")
                    n_tables += 1
                else:
                    body.append(ln)
            head = [f"# {path_title}", s.url, f"{pin_note} {s.src}", ""]
            text = "\n".join(head + body).rstrip("\n") + "\n"
            (out / cdir / f"{name}.md").write_text(text, encoding="utf-8", newline="\n")
            toc.append(f"    - {title}: `{src['id']}/{cdir}/{name}.md`")
            n_sections += 1
            n_lines += text.count("\n")
    (out / "toc.md").write_text("\n".join(toc) + "\n", encoding="utf-8", newline="\n")
    meta = {
        "id": src["id"], "title": src["title"], "authors": src.get("authors"),
        "edition": src.get("edition"), "url": src["url"],
        "upstream": f"https://github.com/{src['upstream']}", "pin": src["pin"],
        "licence": src.get("licence"), "licence_url": src.get("licence_url"),
        "redistributable": bool(src.get("redistributable")),
        "build_date": dt.date.today().isoformat(),
        "chapters": len(chapters), "sections": n_sections, "tables": n_tables, "lines": n_lines,
    }
    (out / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n",
                                   encoding="utf-8", newline="\n")
    return meta


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", nargs="+", metavar="ID", help="build only these sources")
    ap.add_argument("--offline", action="store_true", help="use the download cache only")
    args = ap.parse_args()

    sources = yaml.safe_load((ROOT / "sources.yml").read_text(encoding="utf-8"))["references"]
    if args.only:
        unknown = set(args.only) - {s["id"] for s in sources}
        if unknown:
            sys.exit(f"error: unknown source id: {', '.join(sorted(unknown))}")
        sources = [s for s in sources if s["id"] in args.only]

    t0 = time.time()
    failed: list[str] = []
    built = 0
    for src in sources:
        if src.get("status", "ok") != "ok":
            log(f"[refs] {src['id']}: skipped (status: {src.get('status')})")
            continue
        t1 = time.time()
        try:
            folder = fetch(src, args.offline)
            src.setdefault("base_url", src["url"])
            chapters = PARSERS[src["parser"]](folder, src)
            if not chapters:
                raise RuntimeError("the parser found no sections")
            meta = write_source(src, chapters)
        except FetchError as e:
            log(f"[refs] {src['id']}: FETCH FAILED. {e}")
            log("       Check your network or proxy settings (HTTPS_PROXY) and run the command again.")
            failed.append(src["id"])
            continue
        except Exception as e:  # noqa: BLE001
            log(f"[refs] {src['id']}: BUILD FAILED. {type(e).__name__}: {e}")
            failed.append(src["id"])
            continue
        built += 1
        log(f"[refs] {src['id']}: ok, {meta['chapters']} chapters, {meta['sections']} sections, "
            f"{meta['tables']} tables, {meta['lines']} lines, {time.time() - t1:.1f}s")
    log(f"[refs] built {built} source(s) in {time.time() - t0:.1f}s into {REFS.relative_to(ROOT)}/")
    if failed:
        log(f"[refs] failed: {', '.join(failed)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
