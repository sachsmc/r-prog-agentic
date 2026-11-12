"""Parser for the texinfo source of the R manuals (R-intro.texi)."""
from __future__ import annotations

import re
from pathlib import Path

from .common import Chapter, Section, slugify, tidy_markdown

CHAPTER = ("chapter", "appendix", "unnumbered", "top")
SECTION = ("section", "appendixsec", "appendixsection", "unnumberedsec")
SUB = {"subsection": "###", "appendixsubsec": "###", "unnumberedsubsec": "###", "subheading": "###",
       "subsubsection": "####", "subsubheading": "####", "heading": "###"}
DROP_BLOCKS = ("tex", "iftex", "menu", "ifinfo", "ifplaintext", "titlepage", "copying", "direntry",
               "macro", "ignore", "ifhtml", "html", "detailmenu")
DROP_LINE = re.compile(
    r"^@(c|comment|cindex|findex|vindex|kindex|pindex|tindex|noindent|page|sp|need|vskip|contents|"
    r"printindex|setfilename|settitle|syncodeindex|dircategory|finalout|include|insertcopying|"
    r"summarycontents|bye|group|end group|cartouche|end cartouche|center|title|subtitle|author|"
    r"paragraphindent|set|clear|defcodeindex|refill|raggedright|end raggedright)\b.*$")
SIMPLE = {"R": "R", "SPLUS": "S-Plus", "Sl": "S", "LaTeX": "LaTeX", "TeX": "TeX", "dots": "...",
          "enddots": "...", "copyright": "(c)", "minus": "-", "result": "=>", "bullet": "*",
          "tie": " ", "HTML": "HTML", "error": "error-->", "equiv": "==", "expansion": "==>"}
CODE = ("code", "samp", "file", "command", "option", "env", "kbd", "key", "verb", "t", "CRANpkg", "pkg")
EMPH = ("emph", "var", "dfn", "i", "slanted", "cite")
PLAIN = ("r", "w", "sc", "acronym", "abbr", "asis", "I", "math", "dmn", "email", "titlefont", "sansserif")


def node_anchor(name: str) -> str:
    """Anchor that makeinfo --html gives a node."""
    out = []
    for ch in re.sub(r"\s+", " ", name.strip()):
        if ch.isascii() and ch.isalnum():
            out.append(ch)
        elif ch == " ":
            out.append("-")
        else:
            out.append(f"_{ord(ch):04x}")
    s = "".join(out)
    return s if s[:1].isalpha() else "g_t" + s


def _braces(text: str, start: int) -> int:
    """Index just past the brace group that opens at text[start]."""
    depth = 0
    i = start
    while i < len(text):
        c = text[i]
        if c == "@" and i + 1 < len(text) and text[i + 1] in "{}@":
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return len(text)


CMD = re.compile(r"@([A-Za-z]+)\{")


def inline(text: str, code: bool = False) -> str:
    """Convert inline texinfo commands to markdown. Works from the inside out."""
    out = []
    i = 0
    while True:
        m = CMD.search(text, i)
        if not m:
            out.append(text[i:])
            break
        out.append(text[i:m.start()])
        end = _braces(text, m.end() - 1)
        name = m.group(1)
        arg = text[m.end():end - 1]
        if name in SIMPLE:
            rep = SIMPLE[name]
        elif name in CODE:
            inner = inline(arg, code=True)
            rep = inner if code else ("`" + inner.replace("`", "'") + "`" if inner else "")
        elif name in EMPH:
            inner = inline(arg, code)
            rep = inner if code else f"*{inner}*"
        elif name in ("strong", "b"):
            inner = inline(arg, code)
            rep = inner if code else f"**{inner}**"
        elif name == "footnote":
            rep = f" (Footnote: {inline(arg)})"
        elif name in ("uref", "url"):
            parts = [p.strip() for p in arg.split(",")]
            rep = f"[{inline(parts[1])}]({parts[0]})" if len(parts) > 1 and parts[1] else f"<{parts[0]}>"
        elif name in ("xref", "pxref", "ref"):
            node = re.sub(r"\s+", " ", arg.split(",")[0].strip())
            lead = {"xref": "See ", "pxref": "see ", "ref": ""}[name]
            rep = f'{lead}"{node}"'
        elif name in ("eqn", "deqn"):
            parts = arg.rsplit(",", 1)
            rep = inline(parts[-1] if len(parts) > 1 else parts[0], code=True).strip()
        elif name in ("image", "anchor", "value"):
            rep = "[figure: see the online manual]" if name == "image" else ""
        elif name in PLAIN:
            rep = inline(arg, code)
        else:
            rep = inline(arg, code)        # unknown macro: keep its text
        out.append(rep)
        i = end
    s = "".join(out)
    s = s.replace("@@", "\x01").replace("@{", "{").replace("@}", "}")
    s = re.sub(r"@[:*/]", "", s).replace("@.", ".").replace("@ ", " ").replace("@-", "")
    s = s.replace("``", '"').replace("''", '"')
    return s.replace("\x01", "@")


def parse(root: Path, src: dict) -> list[Chapter]:
    fname = src["files"][0]
    base = src["base_url"]
    text = (root / fname).read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    text = re.sub(r"@c\s*%\*\*.*", "", text)
    lines = text.split("\n")

    chapters: list[Chapter] = []
    chapter: Chapter | None = None
    section: Section | None = None
    buf: list[str] = []
    node = "Top"
    stack: list[str] = []          # open list / table environments
    drop = 0
    verbatim: str | None = None
    para_item_prefix = ""

    def close() -> None:
        nonlocal buf
        if section is not None:
            section.lines = tidy_markdown(buf)
            if any(x.strip() for x in section.lines):
                chapter.sections.append(section)
        buf = []

    def emit(s: str) -> None:
        buf.append(s)

    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        if verbatim:
            if re.match(rf"^@end {verbatim}\b", line):
                emit("```")
                emit("")
                verbatim = None
            else:
                if re.match(r"^@(c|comment|group|end group|cartouche|end cartouche|noindent)\b", line):
                    continue
                emit(inline(line, code=True))
            continue
        m = re.match(r"^@(end\s+)?([A-Za-z]+)\b\s*(.*)$", line)
        cmd = m.group(2) if m else None
        is_end = bool(m and m.group(1))
        arg = m.group(3).strip() if m else ""
        if drop:
            if cmd in DROP_BLOCKS:
                drop += -1 if is_end else 1
            continue
        if cmd in DROP_BLOCKS and not is_end:
            drop = 1
            continue
        if cmd in ("ifnottex", "ifnotinfo", "ifnothtml", "ifclear", "ifset", "quotation", "display",
                   "format", "flushleft", "flushright", "ifnotplaintext", "iflatex", "ifdocbook"):
            continue
        if cmd == "node" and not is_end:
            node = arg.split(",")[0].strip()
            continue
        if cmd in CHAPTER and not is_end:
            close()
            title = inline(arg) or "Preface"
            chapter = Chapter(title=title, slug=slugify(node if cmd != "top" else "preface"))
            chapters.append(chapter)
            anchor = "" if cmd == "top" else "#" + node_anchor(node)
            section = Section(title=title, slug="intro", url=base + anchor, src=fname)
            continue
        if cmd in SECTION and not is_end and chapter is not None:
            close()
            title = inline(arg)
            section = Section(title=title, slug=slugify(node), url=base + "#" + node_anchor(node), src=fname)
            continue
        if section is None:
            continue
        if cmd in SUB and not is_end:
            emit("")
            emit(f"{SUB[cmd]} {inline(arg)}")
            emit("")
            continue
        if cmd in ("example", "smallexample", "verbatim", "lisp", "smalldisplay") and not is_end:
            emit("")
            emit("```r" if cmd != "verbatim" else "```")
            verbatim = cmd
            continue
        if cmd in ("itemize", "enumerate", "table", "ftable", "vtable", "multitable"):
            if is_end:
                if stack:
                    stack.pop()
                emit("")
            else:
                stack.append(cmd)
                emit("")
            continue
        if cmd in ("item", "itemx", "headitem") and not is_end:
            kind = stack[-1] if stack else "itemize"
            indent = "  " * (len(stack) - 1)
            if kind in ("table", "ftable", "vtable"):
                emit("")
                emit(f"{indent}- {inline(arg)}:")
            elif kind == "multitable":
                cells = [inline(c.strip()) for c in arg.split("@tab")]
                emit(f"{indent}- " + " | ".join(cells))
            else:
                mark = "1." if kind == "enumerate" else "-"
                emit("")
                emit(f"{indent}{mark} {inline(arg)}".rstrip())
            continue
        if DROP_LINE.match(line):
            continue
        if cmd == "tab":
            emit("  " + inline(arg))
            continue
        if line.startswith("@") and cmd and re.match(r"^@(end\s+)?[A-Za-z]+\s*$", line):
            continue                                 # stray block command with no text
        text_line = inline(line)
        if stack and text_line.strip():
            text_line = "  " * len(stack) + text_line.strip()
        emit(text_line)
    close()
    return [c for c in chapters if c.sections]
