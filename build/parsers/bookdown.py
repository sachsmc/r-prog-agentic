"""Parser for bookdown (.Rmd) and Quarto (.qmd) book sources.

The source files are parsed directly. Nothing is rendered and no code is run.
Chapters come from level-1 headings and sections from level-2 headings.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

from .common import Chapter, IdRegistry, Section, slugify, tidy_markdown

HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
ATTR = re.compile(r"\s*\{([^{}]*)\}\s*$")
CHUNK = re.compile(r"^(\s*)(`{3,})\s*\{\s*([A-Za-z0-9_.]+)\s*[, ]?(.*)\}\s*$")
HIDDEN = re.compile(r"\b(echo|include)\s*[=:]\s*(FALSE|F|false)\b")
INDEX = re.compile(r"\\index[a-z]*\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}")
IMG = re.compile(r"!\[((?:[^\]\\]|\\.)*)\]\([^)]*\)(\{[^}]*\})?")
LANG = {"r": "r", "R": "r", "webr": "r", "webr-r": "r", "python": "python", "bash": "bash", "sh": "bash", "sql": "sql",
        "css": "css", "js": "js", "cpp": "cpp", "Rcpp": "cpp", "c": "c", "stan": "stan",
        "yaml": "yaml", "tex": "latex", "latex": "latex", "html": "html", "verbatim": "", "cat": ""}


def book_files(root: Path, opts: dict) -> list[str]:
    """Source files in reading order."""
    if opts.get("files"):
        return list(opts["files"])
    if opts.get("files_from_fetch"):
        return list(opts["_fetched"])
    if (root / "_quarto.yml").exists():
        cfg = yaml.safe_load((root / "_quarto.yml").read_text(encoding="utf-8"))
        book = cfg.get("book", {})
        out: list[str] = []

        def walk(items):
            for it in items or []:
                if isinstance(it, str):
                    out.append(it)
                elif isinstance(it, dict):
                    if "file" in it:
                        out.append(it["file"])
                    walk(it.get("chapters"))

        walk(book.get("chapters"))
        walk(book.get("appendices"))
        return out
    cfg = {}
    if (root / "_bookdown.yml").exists():
        cfg = yaml.safe_load((root / "_bookdown.yml").read_text(encoding="utf-8")) or {}
    if cfg.get("rmd_files"):
        files = cfg["rmd_files"]
        if isinstance(files, dict):
            files = files.get("html") or next(iter(files.values()))
        return list(files)
    # bookdown default: index first, then by name, skipping files that start with "_"
    names = sorted(p.name for p in root.iterdir()
                   if p.suffix.lower() == ".rmd" and not p.name.startswith("_"))
    names.sort(key=lambda n: (n.lower() != "index.rmd", n))
    return names


def strip_front_matter(text: str) -> str:
    m = re.match(r"^---\s*\n.*?\n(---|\.\.\.)\s*\n", text, re.S)
    return text[m.end():] if m else text


def atx_headings(lines: list[str]) -> list[str]:
    """Rewrite underlined (setext) headings as # headings, outside code."""
    out: list[str] = []
    fence = None
    for ln in lines:
        m = re.match(r"^\s*(`{3,}|~{3,})", ln)
        if m:
            if fence is None:
                fence = m.group(1)
            elif m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = None
        elif fence is None and out and out[-1].strip() and not out[-1].startswith(("#", "|", " ", "-", ">")):
            if re.match(r"^={3,}\s*$", ln):
                out[-1] = "# " + out[-1].strip()
                continue
            if re.match(r"^-{3,}\s*$", ln) and (len(out) < 2 or not out[-2].strip()):
                out[-1] = "## " + out[-1].strip()
                continue
        out.append(ln)
    return out


def clean_heading(raw: str) -> tuple[str, str | None]:
    """Heading text without attributes, and the explicit id if there is one."""
    ident = None
    m = ATTR.search(raw)
    if m:
        raw = raw[:m.start()]
        i = re.search(r"#([\w:.-]+)", m.group(1))
        ident = i.group(1) if i else None
    raw = re.sub(r"^\((PART\\?\*?|APPENDIX)\)\s*", "", raw)
    return raw.strip(), ident


def plain(text: str) -> str:
    t = re.sub(r"`([^`]*)`", r"\1", text)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    return re.sub(r"[*_\\]", "", t).strip()


def clean_body(lines: list[str]) -> list[str]:
    """Drop hidden chunks and markup that only matters when rendering."""
    out: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        m = CHUNK.match(line)
        if m:
            indent, fence, engine, opts = m.groups()
            j = i + 1
            body: list[str] = []
            while j < n and not re.match(rf"^\s*{fence}\s*$", lines[j]):
                body.append(lines[j])
                j += 1
            head_opts = opts + " " + " ".join(b for b in body if b.lstrip().startswith("#|"))
            body = [b for b in body if not b.lstrip().startswith(("#|", "%%|"))]
            if not HIDDEN.search(head_opts) and engine != "asis" and any(b.strip() for b in body):
                out.append(f"{indent}```{LANG.get(engine, engine)}")
                out.extend(body)
                out.append(f"{indent}```")
            elif engine == "asis" and not re.search(r"echo\s*=\s*(FALSE|F)\b", opts):
                out.extend(body)
            i = j + 1
            continue
        m = re.match(r"^\s*(`{3,}|~{3,})", line)
        if m:                                    # ordinary fenced block: copy verbatim
            fence = m.group(1)
            out.append(line)
            i += 1
            while i < n:
                out.append(lines[i])
                if re.match(rf"^\s*{fence[0]}{{{len(fence)},}}\s*$", lines[i]):
                    i += 1
                    break
                i += 1
            continue
        if re.match(r"^\s*:{3,}", line):         # div fences: keep what is inside
            i += 1
            continue
        if re.match(r"^\s*<!--.*-->\s*$", line) or re.match(r"^\(ref:[\w-]+\)", line):
            i += 1
            continue
        if re.match(r"^\s*<!--", line):
            while i < n and "-->" not in lines[i]:
                i += 1
            i += 1
            continue
        line = INDEX.sub("", line)
        line = IMG.sub(lambda m: f"[figure: {m.group(1).strip() or 'image'}]", line)
        line = re.sub(r"<img\b[^>]*?(?:alt=\"([^\"]*)\")?[^>]*>", lambda m: f"[figure: {m.group(1) or 'image'}]", line)
        line = re.sub(r"</?(span|div|a|p|center|br)\b[^>]*>", "", line)
        m = HEADING.match(line)
        if m:
            text, _ = clean_heading(m.group(2))
            line = f"{m.group(1)} {text}"
        out.append(line)
        i += 1
    return out


def parse(root: Path, src: dict) -> list[Chapter]:
    opts = dict(src.get("options") or {})
    opts["_fetched"] = src.get("files") or []
    base = src["base_url"].rstrip("/") + "/"
    split = opts.get("split", "chapter")         # chapter | section | quarto
    per_file_ids = bool(opts.get("new_session")) or split == "quarto"
    lower = bool(opts.get("lowercase_pages"))
    files = [f for f in book_files(root, opts) if f not in (opts.get("exclude") or [])]

    reg = IdRegistry()
    chapters: list[Chapter] = []
    labels: dict[str, str] = {}
    first = True

    def page(ident: str) -> str:
        return (ident.lower() if lower else ident) + ".html"

    for fname in files:
        path = root / fname
        if not path.exists():
            raise FileNotFoundError(f"{src['id']}: listed file {fname} is not in the source")
        if per_file_ids:
            reg = IdRegistry()
        raw_text = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
        text = strip_front_matter(raw_text)
        lines = atx_headings(text.split("\n"))
        stem = Path(fname).stem

        # Find headings outside code fences.
        # Levels 3 and deeper are listed too: they take identifiers, in order.
        heads: list[tuple[int, int, str, str | None]] = []
        fence = None
        divs: list[bool] = []                    # open ::: blocks, True for callouts
        for idx, line in enumerate(lines):
            m = re.match(r"^\s*(`{3,}|~{3,})", line)
            if m:
                if fence is None:
                    fence = m.group(1)
                elif m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                    fence = None
                continue
            if fence is not None:
                continue
            d = re.match(r"^\s*:{3,}\s*(.*)$", line)
            if d:
                if d.group(1).strip():
                    divs.append("callout" in d.group(1))
                elif divs:
                    divs.pop()
                continue
            h = HEADING.match(line)
            if h and not any(divs):              # a heading inside a callout is its title
                raw = h.group(2)
                if re.match(r"^\((PART\\?\*?|APPENDIX)\)", raw):
                    heads.append((idx, 0, "", None))        # part divider: a break, not a chapter
                    continue
                title, ident = clean_heading(raw)
                heads.append((idx, len(h.group(1)), title, ident))
        if split == "quarto" and not any(level == 1 for _, level, _, _ in heads):
            # A page whose title is only in the YAML header.
            fm = re.match(r"^---\s*\n(.*?)\n(---|\.\.\.)\s*\n", raw_text, re.S)
            meta = (yaml.safe_load(fm.group(1)) or {}) if fm else {}
            lines = [f"# {meta.get('title') or Path(fname).stem}"] + lines
            heads = [(0, 1, str(meta.get("title") or Path(fname).stem), None)] + \
                    [(i + 1, lv, t, ident) for i, lv, t, ident in heads]

        chapter: Chapter | None = None
        chap_page = ""
        chap_title = ""

        def add_section(title: str, ident: str | None, url: str, body: list[str]) -> None:
            body = tidy_markdown(clean_body(body))
            if not any(b.strip() for b in body):
                return
            chapter.sections.append(Section(title=title, slug=slugify(ident or title), url=url,
                                            src=fname, lines=body))

        # A section runs to the next heading of level 1 or 2 (or a part divider).
        tops = [h for h in heads if h[1] <= 2]
        ends = {h[0]: (tops[n + 1][0] if n + 1 < len(tops) else len(lines)) for n, h in enumerate(tops)}
        for idx, level, title, ident in heads:
            if level == 0:
                continue
            if level > 2:
                reg.explicit(ident) if ident else reg.auto(title)
                continue
            body = lines[idx + 1:ends[idx]]
            if level == 1:
                cid = reg.explicit(ident) if ident else reg.auto(title)
                labels[cid] = plain(title)
                if split == "quarto":
                    chap_page = stem + ".html"
                else:
                    chap_page = "index.html" if first else page(cid)
                first = False
                chap_title = plain(title)
                chapter = Chapter(title=chap_title, slug=slugify(cid if split != "quarto" else stem))
                chapters.append(chapter)
                add_section(chap_title, "intro", base + chap_page, body)
            else:
                if chapter is None:                 # a file that starts with a level-2 heading
                    if not chapters:
                        continue
                    chapter = chapters[-1]
                sid = reg.explicit(ident) if ident else reg.auto(title)
                labels[sid] = plain(title)
                if split == "section":
                    url = base + page(sid)
                else:
                    url = base + chap_page + "#" + sid
                add_section(plain(title), sid, url, body)

    # Cheap cross-reference resolution: \@ref(label) -> "Section title"
    ref = re.compile(r"\\@ref\(([\w:.-]+)\)|@(sec-[\w-]+)")

    def resolve(m: re.Match) -> str:
        key = m.group(1) or m.group(2)
        return f'"{labels[key]}"' if key in labels else m.group(0)

    for ch in chapters:
        for s in ch.sections:
            s.lines = [ref.sub(resolve, ln) if ("@ref(" in ln or "@sec-" in ln) else ln for ln in s.lines]
    return [c for c in chapters if c.sections]
