"""Shared model and text helpers for the reference parsers.

A parser turns one upstream source into a list of Chapter objects. The writer in
fetch_refs.py turns those into files under refs/<source>/. Line numbers in the
written files are citation IDs, so everything here must be deterministic.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class Section:
    title: str
    slug: str
    url: str
    src: str                      # file in the upstream source
    lines: list[str] = field(default_factory=list)


@dataclass
class Chapter:
    title: str
    slug: str
    sections: list[Section] = field(default_factory=list)


def slugify(text: str, limit: int = 60) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return (s[:limit].rstrip("-")) or "section"


def pandoc_id(text: str) -> str:
    """Pandoc's automatic heading identifier."""
    t = re.sub(r"`([^`]*)`", r"\1", text)
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", t)          # links: keep the text
    t = re.sub(r"\^\[[^\]]*\]", "", t)                         # footnotes
    t = re.sub(r"[*~]", "", t)                                  # emphasis marks
    t = re.sub(r"\\(.)", r"\1", t)
    t = t.lower()
    t = re.sub(r"[^\w\s.-]", "", t, flags=re.UNICODE)
    t = re.sub(r"\s+", "-", t.strip())
    t = re.sub(r"^[^a-z]+", "", t)                              # up to the first letter
    return t or "section"


class IdRegistry:
    """Makes identifiers unique the way pandoc does: id, id-1, id-2, ..."""

    def __init__(self) -> None:
        self.seen: dict[str, int] = {}

    def auto(self, text: str) -> str:
        base = pandoc_id(text)
        if base not in self.seen:
            self.seen[base] = 0
            return base
        while True:
            self.seen[base] += 1
            cand = f"{base}-{self.seen[base]}"
            if cand not in self.seen:
                self.seen[cand] = 0
                return cand

    def explicit(self, ident: str) -> str:
        self.seen.setdefault(ident, 0)
        return ident


_ABBR = re.compile(
    r"(?:\b(?:e\.g|i\.e|etc|vs|cf|Fig|Figs|Eq|Sec|Dr|Mr|Mrs|Ms|Prof|St|No|al|approx|resp|Vol|pp?|ed|eds)\.|\b[A-Z]\.)$"
)
_MASK = re.compile(r"(`+)(?:(?!\1).)+\1|\$[^$\n]+\$|!?\[[^\]]*\]\([^)]*\)|<[^>\s][^>]*>")
_SPLIT = re.compile(r"(?<=[.!?])([\"')\]*_]*)\s+(?=[\"'(\[*_`]*[A-Z0-9`\x00])")


def split_sentences(text: str) -> list[str]:
    """One sentence per element. Inline code, math and links are never cut."""
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    held: list[str] = []

    def hold(m: re.Match) -> str:
        held.append(m.group(0))
        return f"\x00{len(held) - 1}\x00"

    masked = _MASK.sub(hold, text)
    parts: list[str] = []
    start = 0
    for m in _SPLIT.finditer(masked):
        head = masked[start:m.start()].rstrip()
        if _ABBR.search(head) or (re.fullmatch(r"\(?\d+\.", head) is not None):
            continue
        parts.append(masked[start:m.start()] + m.group(1))
        start = m.end()
    parts.append(masked[start:])
    out = []
    for p in parts:
        p = re.sub(r"\x00(\d+)\x00", lambda m: held[int(m.group(1))], p).strip()
        if p:
            out.append(p)
    return out


_LIST = re.compile(r"^(\s*)([-*+]|\d+[.)]|\(\d+\)|[a-z][.)])\s+\S")
_TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
_HTML_BLOCK = re.compile(r"^\s*</?(div|p|table|tr|td|th|thead|tbody|ul|ol|li|details|summary|center|iframe|script|style|br|hr|img|a|span|figure|figcaption|blockquote|pre|h\d)\b", re.I)


def tidy_markdown(lines: list[str]) -> list[str]:
    """Normalise markdown body text: one sentence per line, one list item per
    line, code and tables untouched, at most one blank line in a row."""
    out: list[str] = []
    para: list[str] = []
    item: list[str] | None = None
    fence: str | None = None
    math = False

    def flush() -> None:
        nonlocal para, item
        if para:
            out.extend(split_sentences(" ".join(s.strip() for s in para)))
            para = []
        if item is not None:
            head = item[0].rstrip()
            rest = " ".join(s.strip() for s in item[1:])
            out.append((head + " " + rest).rstrip() if rest else head)
            item = None

    def blank() -> None:
        if out and out[-1] != "":
            out.append("")

    for raw in lines:
        line = raw.rstrip()
        if fence is not None:
            out.append(line)
            m = re.match(r"^\s*(`{3,}|~{3,})\s*$", line)
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = None
            continue
        m = re.match(r"^\s*(`{3,}|~{3,})", line)
        if m:
            flush()
            fence = m.group(1)
            out.append(line)
            continue
        if math:
            out.append(line)
            if line.strip().endswith("$$") or line.strip() == r"\]":
                math = False
            continue
        if line.strip().startswith("$$") or line.strip() == r"\[":
            flush()
            out.append(line)
            math = not (line.strip().endswith("$$") and len(line.strip()) > 2)
            continue
        if not line.strip():
            flush()
            blank()
            continue
        if re.match(r"^#{1,6}\s", line):
            flush()
            blank()
            out.append(line)
            out.append("")
            continue
        if "|" in line and (line.lstrip().startswith("|") or _TABLE_SEP.match(line)
                            or (out and "|" in out[-1] and not para and item is None)):
            if para and len(para) == 1 and "|" in para[0]:
                out.append(para[0].rstrip())   # header row of a pipe table
                para = []
            else:
                flush()
            out.append(line)
            continue
        if line.lstrip().startswith(">") or _HTML_BLOCK.match(line):
            flush()
            out.append(line)
            continue
        if _LIST.match(line):
            flush()
            item = [line]
            continue
        if item is not None:
            if raw.startswith((" ", "\t")):
                item.append(line)
                continue
            flush()
        if raw.startswith("    ") and not para and (not out or out[-1] == ""):
            out.append(line)                    # indented code block
            continue
        para.append(line)
    flush()
    while out and out[-1] == "":
        out.pop()
    while out and out[0] == "":
        out.pop(0)
    return out
