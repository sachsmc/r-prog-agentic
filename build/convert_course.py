# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""Build course/ from the source course repo at the commit pinned in sources.yml.

Steps: clone at the pin, turn webR cells into plain R chunks, render each
lecture, exercise and solution with Quarto to GitHub-flavoured markdown with the
code executed, strip slide-only markup, then write the syllabus and course.md.

Run:  uv run build/convert_course.py            (or: make course)
Needs: git, quarto, R with the packages listed in build/r-packages.txt.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import glob
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache"
SRC = CACHE / "course-src"
WORK = CACHE / "course-build"
OUT = ROOT / "course"
SITE = "https://sachsmc.github.io/r-programming"

# webR-only cell options that mean nothing to knitr.
WEBR_ONLY = re.compile(
    r"^#\|\s*(autorun|exercise|setup|check|solution|hint|min-lines|max-lines|"
    r"startover|runbutton|completion|persist|timelimit|envir|define|input|edit|caption)\s*[:=]"
)

SETUP_CHUNK = r"""
```{r}
#| include: false
set.seed(20261112)
options(width = 80, cli.unicode = FALSE, pillar.width = 80, digits = 5)
knitr::opts_chunk$set(error = TRUE, comment = "#>", collapse = FALSE)
local({
  old <- knitr::knit_hooks$get("error")
  knitr::knit_hooks$set(
    error = function(x, options) {
      out <- old(x, options)
      if (isTRUE(options$demo_error)) out else paste0("\n\nCHUNK-FAILED-MARKER\n\n", out)
    },
    plot = function(x, options) {
      cap <- options$fig.cap
      if (is.null(cap) || !nzchar(cap[1])) cap <- options$fig.alt
      if (is.null(cap) || !nzchar(cap[1])) cap <- if (isFALSE(options$echo))
        "plot, see the online slides" else "plot produced by the code above"
      paste0("\n\n[figure: ", cap[1], "]\n\n")
    }
  )
  # Interactive widgets cannot be shown in markdown: print a text note instead.
  widget_note <- function(x, ...) knitr::asis_output(
    "\n\n[figure: interactive plot, see the online slides]\n\n")
  reg <- function(...) for (cl in c("htmlwidget", "plotly"))
    registerS3method("knit_print", cl, widget_note, envir = asNamespace("knitr"))
  reg()
  # htmlwidgets registers its own method when it loads, so register again after.
  setHook(packageEvent("htmlwidgets", "onLoad"), reg, action = "append")
})
```
"""


def log(msg: str) -> None:
    print(msg, flush=True)


def run(cmd: list[str], cwd: Path | None = None, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, env=env, text=True, capture_output=True,
                          encoding="utf-8", errors="replace")


def need(tool: str) -> str:
    path = shutil.which(tool)
    if not path:
        sys.exit(f"error: '{tool}' was not found on PATH. Install it and try again.")
    return path


def find_r_bin() -> str | None:
    """Directory holding Rscript, or None if it is already on PATH."""
    if shutil.which("Rscript"):
        return None
    hits = sorted(glob.glob(r"C:\Program Files\R\R-*\bin\Rscript.exe"))
    if hits:
        return str(Path(hits[-1]).parent)
    sys.exit("error: Rscript was not found. Install R (https://cran.r-project.org) and try again.")


def load_sources() -> dict:
    return yaml.safe_load((ROOT / "sources.yml").read_text(encoding="utf-8"))


# ---------------------------------------------------------------- fetch

def fetch(repo: str, pin: str) -> None:
    if not (SRC / ".git").exists():
        SRC.parent.mkdir(parents=True, exist_ok=True)
        r = run(["git", "clone", "--quiet", repo, str(SRC)])
        if r.returncode:
            sys.exit(f"error: could not clone {repo}\n{r.stderr}")
    if run(["git", "cat-file", "-e", pin + "^{commit}"], cwd=SRC).returncode:
        r = run(["git", "fetch", "--quiet", "origin"], cwd=SRC)
        if r.returncode:
            sys.exit(f"error: could not fetch {repo}\n{r.stderr}")
    r = run(["git", "-c", "advice.detachedHead=false", "checkout", "--quiet", "--force", pin], cwd=SRC)
    if r.returncode:
        sys.exit(f"error: could not check out {pin}\n{r.stderr}")
    run(["git", "clean", "-fdxq"], cwd=SRC)


def make_worktree() -> None:
    global WORK
    # A fresh folder per run. Old ones are removed when nothing holds them open.
    for old in CACHE.glob("course-build*"):
        shutil.rmtree(old, ignore_errors=True)
    WORK = CACHE / f"course-build-{os.getpid()}"
    shutil.copytree(SRC, WORK, ignore=shutil.ignore_patterns(".git", "docs", "_extensions", "*_files"))
    # Render file by file, not as a website project.
    (WORK / "_quarto.yml").unlink(missing_ok=True)


# ---------------------------------------------------------------- order

def split_front(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}, text
    return yaml.safe_load(m.group(1)) or {}, text[m.end():]


def ordered(folder: Path) -> list[tuple[Path, dict]]:
    """Files in teaching order: the source site sorts listings by subtitle."""
    items = []
    for f in sorted(folder.glob("*.qmd")):
        if f.name == "index.qmd":
            continue
        meta, _ = split_front(f.read_text(encoding="utf-8"))
        items.append((f, meta))
    items.sort(key=lambda it: (str(it[1].get("subtitle", "")), it[0].name))
    return items


# ---------------------------------------------------------------- preprocess

def preprocess(text: str) -> str:
    meta, body = split_front(text)
    keep = {k: meta[k] for k in ("title", "subtitle", "author", "params") if k in meta}
    keep["engine"] = "knitr"
    keep["format"] = {"gfm": {"wrap": "none"}}
    execute = dict(meta.get("execute") or {})
    execute.setdefault("echo", True)
    execute["warning"] = False
    execute["message"] = False
    keep["execute"] = execute

    out: list[str] = []
    lines = body.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^(\s*)(`{3,})\s*\{(webr|r|mermaid)\b([^}]*)\}\s*$", line)
        if not m:
            out.append(line)
            i += 1
            continue
        indent, fence, kind, rest = m.groups()
        j = i + 1
        chunk: list[str] = []
        while j < len(lines) and not re.match(rf"^\s*{fence}\s*$", lines[j]):
            chunk.append(lines[j])
            j += 1
        if kind == "mermaid":
            # Keep the diagram source as text. Do not render it.
            chunk = [c for c in chunk if not c.lstrip().startswith("%%|")]
            out += [f"{indent}```mermaid", *chunk, f"{indent}```"]
        else:
            opts = [c for c in chunk if c.lstrip().startswith("#|")]
            code = [c for c in chunk if not c.lstrip().startswith("#|")]
            opts = [o for o in opts if not WEBR_ONLY.match(o.strip())]
            if any(re.match(r"#\|\s*error\s*[:=]\s*(true|TRUE)", o.strip()) for o in opts):
                opts.append(f"{indent}#| demo_error: true")
            head = "{r" + rest + "}" if kind == "r" else "{r}"
            out += [f"{indent}```{head}", *opts, *code, f"{indent}```"]
        i = j + 1

    front = yaml.safe_dump(keep, sort_keys=False, allow_unicode=True)
    return f"---\n{front}---\n{SETUP_CHUNK}\n" + "\n".join(out)


# ---------------------------------------------------------------- render

def render(qmd: Path, env: dict) -> str:
    r = run(["quarto", "render", qmd.name, "--to", "gfm", "--quiet"], cwd=qmd.parent, env=env)
    md = qmd.with_suffix(".md")
    if r.returncode or not md.exists():
        raise RuntimeError(f"quarto failed on {qmd.name}\n{r.stdout[-2000:]}\n{r.stderr[-4000:]}")
    return md.read_text(encoding="utf-8")


# ---------------------------------------------------------------- postprocess

IMG_MD = re.compile(r"!\[([^\]]*)\]\(([^)\s]*)[^)]*\)(\{[^}]*\})?")
IMG_HTML = re.compile(r"<img\b[^>]*>", re.I)
FAILED_NOTE = ("*Note: this code raised an error when the course material was built. "
               "It may be incomplete on purpose. Treat it as an exercise: work out what is needed to make it run.*")


def _figure(alt: str, src: str) -> str:
    alt = alt.strip()
    if not alt:
        alt = Path(src).stem.replace("-", " ").replace("_", " ") or "image"
    return f"[figure: {alt}]"


def _img_html(m: re.Match) -> str:
    tag = m.group(0)
    alt = re.search(r'alt="([^"]*)"', tag)
    src = re.search(r'src="([^"]*)"', tag)
    return _figure(alt.group(1) if alt else "", src.group(1) if src else "")


def postprocess(md: str) -> tuple[str, int]:
    md = md.replace("\r\n", "\n")
    # Quarto writes its own title block (title, then author). The file header replaces it.
    md = re.sub(r"\A\s*# [^\n]*\n(?:[^\n#`][^\n]*\n)?", "", md)
    md = re.sub(r"\\\[figure: ([^\n]*?)\\\]", r"[figure: \1]", md)
    out: list[str] = []
    fence: str | None = None
    failed = 0
    for line in md.split("\n"):
        m = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if m:
            if fence is None:
                fence = m.group(1)
                line = re.sub(r"^(\s*`{3,})\s+(\w)", r"\1\2", line)  # "``` r" -> "```r"
            elif m.group(1).startswith(fence) and not m.group(2).strip():
                fence = None
            out.append(line.rstrip())
            continue
        if fence is not None or line.startswith("    "):
            out.append(line.rstrip())
            continue
        if line.strip() == "CHUNK-FAILED-MARKER":
            failed += 1
            out.append(FAILED_NOTE)
            continue
        if re.match(r"^\s*</?div\b[^>]*>\s*$", line) or re.match(r"^\s*:{3,}", line):
            continue
        line = re.sub(r"</?(div|span)\b[^>]*>", "", line)
        line = IMG_MD.sub(lambda m: _figure(m.group(1), m.group(2)), line)
        line = IMG_HTML.sub(_img_html, line)
        line = re.sub(r"\s*\{[.#][^}`]*\}\s*$", "", line)          # trailing {.class}
        line = re.sub(r"\]\{[.#][^}`]*\}", "]", line)               # [text]{.class}
        if re.match(r"^#+\s*$", line):                               # empty slide heading
            continue
        out.append(line.rstrip())
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    return text, failed


# ---------------------------------------------------------------- assemble

def tokens(text: str) -> int:
    """Rough token estimate: four characters per token."""
    return round(len(text) / 4)


def header(kind: str, n: int, meta: dict, url: str) -> str:
    title = str(meta.get("title", "")).replace(" -- ", ": ")
    day = meta.get("subtitle", "")
    label = {"lecture": "Lecture", "exercise": "Exercise set", "solution": "Solutions for exercise set"}[kind]
    link = "Slides" if kind == "lecture" else "Online version"
    return f"# {title}\n\n{label} {n} | {day} | {link}: <{url}>\n\n"


def build(args: argparse.Namespace) -> int:
    for tool in ("git", "quarto"):
        need(tool)
    env = dict(os.environ)
    rbin = find_r_bin()
    if rbin:
        env["PATH"] = rbin + os.pathsep + env["PATH"]
    env["LC_ALL"] = env.get("LC_ALL", "C.UTF-8")
    env["TZ"] = "UTC"

    course = load_sources()["course"]
    log(f"[course] source {course['repo']} at {course['pin'][:10]}")
    fetch(course["repo"], course["pin"])
    make_worktree()

    lectures = ordered(SRC / "lectures")
    exercises = ordered(SRC / "exercises")
    sol_by_stem = {f.stem: (f, m) for f, m in ordered(SRC / "exercises" / "solutions")}

    jobs: list[dict] = []
    for n, (f, meta) in enumerate(lectures, 1):
        jobs.append(dict(kind="lecture", n=n, stem=f.stem, meta=meta, rel=f"lectures/{f.name}",
                         out=OUT / "lectures" / f"{n:02d}-{f.stem}.md",
                         url=f"{SITE}/lectures/{f.stem}.html"))
    for n, (f, meta) in enumerate(exercises, 1):
        jobs.append(dict(kind="exercise", n=n, stem=f.stem, meta=meta, rel=f"exercises/{f.name}",
                         out=OUT / "exercises" / f"{n:02d}-{f.stem}.md",
                         url=f"{SITE}/exercises/{f.stem}.html"))
        if f.stem in sol_by_stem:
            sf, smeta = sol_by_stem.pop(f.stem)
            jobs.append(dict(kind="solution", n=n, stem=f.stem, meta=smeta,
                             rel=f"exercises/solutions/{sf.name}",
                             out=OUT / "exercises" / "solutions" / f"{n:02d}-{f.stem}.md",
                             url=f"{SITE}/exercises/solutions/{f.stem}.html"))
    if sol_by_stem:
        sys.exit(f"error: solutions without a matching exercise: {sorted(sol_by_stem)}")

    def work(job: dict) -> dict:
        qmd = WORK / job["rel"]
        qmd.write_text(preprocess(qmd.read_text(encoding="utf-8")), encoding="utf-8")
        body, failed = postprocess(render(qmd, env))
        job["text"] = header(job["kind"], job["n"], job["meta"], job["url"]) + body
        job["failed"] = failed
        return job

    errors = []
    with cf.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(work, j): j for j in jobs}
        for fut in cf.as_completed(futures):
            j = futures[fut]
            try:
                fut.result()
                note = f", {j['failed']} chunk(s) did not run" if j["failed"] else ""
                log(f"[course] rendered {j['rel']}{note}")
            except Exception as e:  # noqa: BLE001
                errors.append(str(e))
                log(f"[course] FAILED {j['rel']}")
    if errors:
        sys.exit("error: rendering failed\n\n" + "\n\n".join(errors))

    # Solution scripts (.R) that sit beside the solution pages.
    extra = course.get("solution_scripts") or {}
    by_out = {(j["kind"], j["stem"]): j for j in jobs}
    for script, stem in sorted(extra.items()):
        src = SRC / "exercises" / "solutions" / script
        j = by_out.get(("solution", stem))
        if not src.exists() or j is None:
            sys.exit(f"error: solution script mapping {script} -> {stem} does not match the source repo")
        code = src.read_text(encoding="utf-8").replace("\r\n", "\n").rstrip()
        j["text"] += f"\n## Solution script: {script}\n\n```r\n{code}\n```\n"

    # Write course/ from scratch, keeping nothing stale.
    for sub in ("lectures", "exercises", "data", "example-project"):
        shutil.rmtree(OUT / sub, ignore_errors=True)
    for j in jobs:
        j["out"].parent.mkdir(parents=True, exist_ok=True)
        j["out"].write_text(j["text"], encoding="utf-8", newline="\n")

    ignore = shutil.ignore_patterns("*.qmd", "*.html", "*_files", ".Rhistory", ".RData", ".Rproj.user")
    shutil.copytree(SRC / "data", OUT / "data", ignore=ignore)
    shutil.copytree(SRC / "example-project", OUT / "example-project", ignore=ignore)
    for extra_file in course.get("extra_data") or []:
        shutil.copy2(SRC / extra_file, OUT / "data" / Path(extra_file).name)
    for proj in course.get("solution_projects") or []:
        shutil.copytree(SRC / "exercises" / "solutions" / proj,
                        OUT / "exercises" / "solutions" / proj, ignore=ignore)
    (OUT / ".here").write_text("", encoding="utf-8")

    syllabus = write_syllabus(jobs, course)
    parts = [syllabus]
    for kind in ("lecture", "exercise", "solution"):
        for j in sorted((j for j in jobs if j["kind"] == kind), key=lambda j: j["n"]):
            rel = j["out"].relative_to(ROOT).as_posix()
            parts.append(f"<!-- file: {rel} -->\n\n{j['text']}")
    course_md = "\n\n---\n\n".join(p.strip() for p in parts) + "\n"
    (OUT / "course.md").write_text(course_md, encoding="utf-8", newline="\n")

    n_failed = sum(j["failed"] for j in jobs)
    log(f"[course] wrote {len(jobs)} files, syllabus about {tokens(syllabus)} tokens, "
        f"course.md about {tokens(course_md)} tokens, {n_failed} chunk(s) marked as not running")
    return check()


def write_syllabus(jobs: list[dict], course: dict) -> str:
    cfg = yaml.safe_load((ROOT / "build" / "syllabus.yml").read_text(encoding="utf-8"))
    data_files = sorted(p.name for p in (OUT / "data").iterdir() if p.is_file())
    ex = {j["stem"]: j for j in jobs if j["kind"] == "exercise"}

    def used(text: str) -> list[str]:
        hits = [d for d in data_files if d in text]
        if re.search(r"med-.{0,40}-ex\.rds", text) and not any(h.startswith("med-") for h in hits):
            hits.append("med-2005-ex.rds to med-2010-ex.rds")
        if re.search(r"\bpenguins\b", text):
            hits.append("penguins (R package palmerpenguins)")
        return hits

    out = [f"# Syllabus: {cfg['title']}\n", cfg["intro"].strip() + "\n"]
    out.append(f"Course website: <{SITE}/>\n")
    out.append("Files are under `course/`. Data is in `course/data/`. "
               "Run R code with `course/` as the working directory so that `here(\"data\", ...)` finds the files.\n")
    for j in sorted((j for j in jobs if j["kind"] == "lecture"), key=lambda j: j["n"]):
        entry = cfg["lectures"].get(j["stem"])
        if entry is None:
            sys.exit(f"error: build/syllabus.yml has no entry for lecture '{j['stem']}'")
        out.append(f"## {j['n']}. {j['meta'].get('title')} ({j['meta'].get('subtitle')})\n")
        out.append(f"- File: `{j['out'].relative_to(ROOT).as_posix()}`")
        for g in entry["goals"]:
            if not isinstance(g, str):
                sys.exit(f"error: build/syllabus.yml, lecture '{j['stem']}': a goal is not plain text "
                         f"({g!r}). Put it in quotes if it contains a colon.")
        out.append("- Goals:")
        out += [f"    - {g}" for g in entry["goals"]]
        e = ex.get(entry.get("exercise") or "")
        text = j["text"]
        if e:
            rel = e["out"].relative_to(ROOT).as_posix()
            out.append(f"- Exercise: `{rel}`, solutions in `{rel.replace('exercises/', 'exercises/solutions/')}`")
            text += e["text"]
        else:
            out.append("- Exercise: none")
        d = used(text)
        out.append(f"- Data: {', '.join(d) if d else 'none'}")
        out.append("")
    text = "\n".join(out).rstrip() + "\n"
    (OUT / "syllabus.md").write_text(text, encoding="utf-8", newline="\n")
    return text


# ---------------------------------------------------------------- checks

def check() -> int:
    """Phase 1 acceptance checks that a script can do."""
    problems: list[str] = []
    src_l = [f.stem for f, _ in ordered(SRC / "lectures")]
    src_e = [f.stem for f, _ in ordered(SRC / "exercises")]
    for kind, stems in (("lectures", src_l), ("exercises", src_e), ("exercises/solutions", src_e)):
        have = {re.sub(r"^\d+-", "", p.stem) for p in (OUT / kind).glob("*.md")}
        for s in stems:
            if s not in have:
                problems.append(f"missing course/{kind} counterpart for {s}")
    bad = re.compile(r"\{webr|^\s*:{3,}|\{\.[A-Za-z][\w-]*[^}]*\}|live-revealjs", re.M)
    for p in sorted(OUT.rglob("*.md")):
        if "solutions" in p.parts and p.parent.name != "solutions":
            continue  # copied project folders are not converted material
        if "example-project" in p.parts:
            continue
        text = p.read_text(encoding="utf-8")
        text_nocode = re.sub(r"^(`{3,}).*?^\1\s*$", "", text, flags=re.S | re.M)
        m = bad.search(text_nocode)
        if m:
            problems.append(f"{p.relative_to(ROOT).as_posix()}: slide markup left over: {m.group(0)!r}")
    syl = tokens((OUT / "syllabus.md").read_text(encoding="utf-8"))
    if syl > 2500:
        problems.append(f"syllabus.md is about {syl} tokens, limit 2500")
    agents = ROOT / "AGENTS.md"
    if agents.exists():
        a = tokens(agents.read_text(encoding="utf-8"))
        if a > 1500:
            problems.append(f"AGENTS.md is about {a} tokens, limit 1500")
    for p in problems:
        log(f"[check] FAIL {p}")
    if not problems:
        log("[check] ok: every lecture and exercise has a counterpart, no slide markup, size limits hold")
    return 1 if problems else 0


def update_pin() -> int:
    """Point the course pin in sources.yml at the newest upstream commit."""
    course = load_sources()["course"]
    r = run(["git", "ls-remote", course["repo"], "HEAD"])
    if r.returncode or not r.stdout.strip():
        sys.exit(f"error: could not read the newest commit of {course['repo']}\n{r.stderr}")
    new = r.stdout.split()[0]
    if new == course["pin"]:
        log(f"[course] pin is up to date ({new[:10]})")
        return 0
    path = ROOT / "sources.yml"
    text = path.read_text(encoding="utf-8")
    # The first match is the course pin. References from the same repo keep their own pin.
    path.write_text(text.replace(course["pin"], new, 1), encoding="utf-8", newline="\n")
    log(f"[course] pin moved from {course['pin'][:10]} to {new[:10]}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--jobs", type=int, default=min(4, os.cpu_count() or 2), help="parallel quarto renders")
    ap.add_argument("--check", action="store_true", help="only run the acceptance checks on course/")
    ap.add_argument("--update-pin", action="store_true",
                    help="set the pin in sources.yml to the newest upstream commit, then stop")
    args = ap.parse_args()
    if args.update_pin:
        return update_pin()
    if args.check:
        return check()
    return build(args)


if __name__ == "__main__":
    sys.exit(main())
