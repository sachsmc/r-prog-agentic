"""Parser for PDF sources: journal articles and layout-heavy cheatsheets.

mode "article": numbered headings ("2. Title", "2.1. Title") give chapters and
sections, text is joined and split into sentences.
mode "pages": one chapter per PDF and one section per page, lines kept as they
are extracted. Use it for cheatsheets, where reading order is only approximate.
"""
from __future__ import annotations

import logging
import re
import unicodedata
from pathlib import Path

from pypdf import PdfReader

from .common import Chapter, Section, slugify, split_sentences

logging.getLogger("pypdf").setLevel(logging.ERROR)

TOP = re.compile(r"^(\d{1,2})\.\s+(\S.{2,80})$")
SUBH = re.compile(r"^(\d{1,2}\.\d{1,2}(?:\.\d{1,2})?)\.?\s+(\S.{2,80})$")
BACK = re.compile(r"^(references|acknowledge?ments?|supplement(al|ary) materials?)$", re.I)


def page_lines(path: Path) -> list[list[str]]:
    pages = []
    for page in PdfReader(str(path)).pages:
        text = unicodedata.normalize("NFKC", page.extract_text() or "")
        pages.append([re.sub(r"\s+", " ", ln).strip() for ln in text.split("\n")])
    return pages


def flow(lines: list[str]) -> list[str]:
    """Join extracted lines into sentences. Undo end-of-line hyphenation."""
    text = ""
    for ln in lines:
        if not ln:
            continue
        if text.endswith("-") and ln[:1].islower():
            text = text[:-1] + ln
        else:
            text = (text + " " + ln) if text else ln
    return split_sentences(text)


def parse_article(root: Path, src: dict) -> list[Chapter]:
    opts = src.get("options") or {}
    fname = src["files"][0]
    url = src["base_url"]
    drop = [re.compile(p) for p in opts.get("drop_lines") or []]
    titles = {str(k): v for k, v in (opts.get("heading_titles") or {}).items()}
    lines = [ln for pg in page_lines(root / fname) for ln in pg
             if ln and not any(d.search(ln) for d in drop)]

    chapters: list[Chapter] = []
    chapter = Chapter(title="Abstract", slug="abstract")
    section = Section(title="Abstract", slug="intro", url=url, src=fname)
    buf: list[str] = []
    out: list[str] = []
    expect = 1

    def flush_text() -> None:
        nonlocal buf
        if buf:
            out.extend(flow(buf))
            buf = []

    def close_section() -> None:
        nonlocal out
        flush_text()
        if any(x.strip() for x in out):
            section.lines = out
            chapter.sections.append(section)
        out = []

    def close_chapter() -> None:
        close_section()
        if chapter.sections:
            chapters.append(chapter)

    for ln in lines:
        m = TOP.match(ln)
        if m and int(m.group(1)) in (expect, expect + 1) and not ln.endswith((".", ",")):
            close_chapter()
            expect = int(m.group(1)) + 1
            title = titles.get(m.group(1), m.group(2)).strip()
            chapter = Chapter(title=title, slug=slugify(title))
            section = Section(title=title, slug="intro", url=url, src=fname)
            continue
        m = SUBH.match(ln)
        if m and m.group(1).split(".")[0] == str(expect - 1) and not ln.endswith((".", ",")):
            title = titles.get(m.group(1), m.group(2)).strip()
            if m.group(1).count(".") == 1:
                close_section()
                section = Section(title=title, slug=slugify(title), url=url, src=fname)
            else:
                flush_text()
                out.extend(["", f"### {title}", ""])
            continue
        if BACK.match(ln):
            close_chapter()
            expect = 99
            title = ln.capitalize()
            chapter = Chapter(title=title, slug=slugify(title))
            section = Section(title=title, slug="intro", url=url, src=fname)
            continue
        buf.append(ln)
    close_chapter()
    return chapters


def parse_pages(root: Path, src: dict) -> list[Chapter]:
    chapters = []
    names = (src.get("options") or {}).get("titles") or {}
    for fname in src["files"]:
        stem = Path(fname).stem
        title = names.get(stem, stem)
        url = f"https://raw.githubusercontent.com/{src['upstream']}/{src['pin']}/{fname}"
        ch = Chapter(title=title, slug=slugify(stem))
        for n, lines in enumerate(page_lines(root / fname), 1):
            body = [ln for ln in lines if ln]
            if body:
                ch.sections.append(Section(title=f"page {n}", slug=f"page-{n}", url=f"{url}#page={n}",
                                           src=fname, lines=body))
        if ch.sections:
            chapters.append(ch)
    return chapters


def parse(root: Path, src: dict) -> list[Chapter]:
    mode = (src.get("options") or {}).get("mode", "article")
    return parse_pages(root, src) if mode == "pages" else parse_article(root, src)
