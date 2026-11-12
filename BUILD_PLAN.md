# Build plan: agent-ready R programming course

This file is the brief for the coding agent that builds this repo. Read it fully before writing code. Work phase by phase, and do not start a phase until the acceptance checks of the previous one pass. Commit at the end of each phase.

## Goal

A public repo that students clone and open in an agent harness (Claude Code first, others via `AGENTS.md`). The agent then acts as a tutor for the course "Programming and statistical modelling in R" (University of Copenhagen, Michael C Sachs), grounded in the course material and able to search and cite the course's reference books.

Source of the teaching content: https://github.com/sachsmc/r-programming (MIT licence, Quarto website, output in `docs/`).

## Facts measured on the source repo (12 Nov 2026)

- 12 lecture files in `lectures/*.qmd` (about 98k characters), 8 exercise sets in `exercises/*.qmd` (about 29k characters), solutions in `exercises/solutions/` (`.qmd` and `.R`, plus two worked project folders).
- All authored `.qmd` files together are about 162k characters, roughly 40k to 45k tokens.
- Lectures use `format: live-revealjs` with webR cells (the `r-wasm/live` Quarto extension). Seven lectures contain webR cells.
- Data lives in `data/` (`.rds`, `.csv`, `.xlsx`, `regdata.zip`) and `example-project/`.
- `resources.qmd` lists the references (see "Reference sources" below).
- Everything under `docs/`, `_extensions/`, and `*_files/` is rendered output or bundled libraries. Ignore it.

## Decisions already made

- Tooling language: Python, run with `uv` so students install nothing by hand. Scripts declare dependencies inline (PEP 723) or via one `pyproject.toml`.
- Solutions: the tutor shows a solution after the student has made an attempt, or when the student asks for it. Never refuse a direct request.
- Retrieval: one `search` command combining BM25 and embeddings, plus ripgrep for exact and regex lookup (see "ripgrep").
- Reference text is built on the student's machine from pinned upstream sources. Do not commit the processed text of third-party books to this repo (see "Licensing").
- Student-facing text: plain language, short sentences, no em dashes.

## Repo layout

```
AGENTS.md                # tutor policy and repo map, harness-neutral
CLAUDE.md                # contains only: @AGENTS.md
README.md                # "How to use this repo" for students
BUILD_PLAN.md            # this file
Makefile                 # course, refs, index, test, all
pyproject.toml
sources.yml              # reference sources: url, pin, licence, parser, base_url
course/
  syllabus.md            # about 2k tokens
  lectures/NN-name.md
  exercises/NN-name.md
  exercises/solutions/NN-name.md
  course.md              # concatenation of everything, for chat-only use
  data/
refs/                    # gitignored, built by `make refs`
  <source>/meta.json
  <source>/toc.md
  <source>/<NN-chapter>/<NN-section>.md
  <source>/<NN-chapter>/tables/*.md
.index/                  # gitignored: search.sqlite, vectors
bin/search
bin/cite-check
build/                   # convert_course.py, fetch_refs.py, parsers/, build_index.py
.claude/skills/<name>/SKILL.md
eval/
  golden.yml
  test_*.py
.github/workflows/
```

## Phase 1: course material in context

1. `build/convert_course.py` clones the source repo at a pinned commit and produces `course/`.
2. For each lecture and exercise file:
   - Convert webR cells (`{webr}` chunks and their `#|` options) to plain `{r}` chunks, and drop the `live-revealjs` format and `webr:` YAML keys.
   - Render with Quarto to GitHub-flavoured markdown with code executed, so output is included. Figures: keep the code and replace the image with a one-line text note such as `[figure: scatterplot of ...]` taken from alt text or caption when present.
   - Strip revealjs-only markup (fragments, column divs, speaker notes, incremental markers) while keeping the content inside.
   - If a chunk cannot run (for example an interactive exercise cell left blank on purpose), keep the code with `eval: false` and mark it as an exercise for the student.
   - Keep slide headings as markdown headings. Add a front line with title, course day, and a link to the online slide deck.
3. Number files in teaching order. Take the order from `lectures/index.qmd`, `exercises/index.qmd`, and `index.qmd` in the source repo.
4. Write `course/syllabus.md`: one entry per lecture with day, learning goals (two or three bullets, derived from the lecture content), the matching exercise file, and the data files used.
5. Write `course/course.md` as the concatenation: syllabus, then lectures, then exercises, then solutions.
6. Copy `data/` and `example-project/`.
7. Write `AGENTS.md` (see "Tutor policy") and `CLAUDE.md`.

Acceptance:
- `make course` runs from a clean clone and exits 0.
- Every lecture and exercise in the source has a counterpart in `course/`.
- No file in `course/` contains `{webr}`, `:::` div fences, or revealjs attributes.
- `course/syllabus.md` is under 2,500 tokens and `AGENTS.md` under 1,500 tokens.
- Manual check: in a fresh Claude Code session, "teach me lecture 1" produces a walk-through that follows the actual lecture.

## Phase 2: reference corpus (gxl-style)

The design follows the "literature as a filesystem" idea from gxl (https://gxl.ai/blog/biomedical-literature-as-a-filesystem/). Read that post first and adjust the layout below if it describes a better convention. The essentials are: document structure preserved as directories and files, every line addressable, tables as first-class files.

### Layout and addresses

- One directory per source, one directory per chapter, one file per section (split at the second heading level; split further if a section exceeds about 400 lines).
- One sentence or one code line per physical line where practical, so line ranges are tight. Never reflow after the build: line numbers are the citation IDs.
- Address format: `<source>/<chapter>/<section>:L<start>-L<end>`, for example `adv-r/06-functions/04-lazy-evaluation:L12-L18`. Because the ID is the file's own line number, `rg -n` and `cat -n` output is directly citable.
- Each section file starts with a three-line header: heading path, canonical URL of that section in the online book, and source pin. The header counts as lines 1 to 3.
- `meta.json` per source: title, authors, edition, URL, upstream repo, pinned commit or tag, licence, build date, section count.
- `toc.md` per source: nested list of chapters and sections with paths.
- Tables go to `tables/` as markdown, with a pointer line left in the section.
- Code chunks stay inline in fenced blocks. Do not execute reference book code.

### Reference sources

| id | Title | Upstream | Pin | Notes |
|---|---|---|---|---|
| `r-intro` | An Introduction to R (R core team) | `wch/r-source`, `doc/manual/R-intro.texi` | a release tag | texinfo parser needed, about 258k characters |
| `r4ds` | R for Data Science, 1st edition | `hadley/r4ds` | tag `first-ed` | 43 `.Rmd` files, about 636k characters. The `main` branch is the 2nd edition, do not use it |
| `moderndive` | Statistical Inference via Data Science | `moderndive/ModernDive_book` | commit on default branch | top-level `.qmd` files only (about 1.32M characters). Exclude `scripts/`, `_extensions/`. `lc-answers/` optional |
| `hopr` | Hands-On Programming with R | `rstudio-education/hopr` | commit | about 380k characters |
| `adv-r` | Advanced R, 2nd edition | `hadley/adv-r` | commit | about 811k characters |
| `rgcookbook` | R Graphics Cookbook, 2nd edition | `wch/rgcookbook` | commit | about 522k characters |
| `rmarkdown` | R Markdown: The Definitive Guide | `rstudio/rmarkdown-book` | commit | about 369k characters |
| `rmd-cookbook` | R Markdown Cookbook | `yihui/rmarkdown-cookbook` | commit | about 425k characters |
| `tidy-data` | Tidy Data (Wickham 2014, JSS) | PDF in the course repo | course repo commit | PDF parser |
| `layered-grammar` | A Layered Grammar of Graphics (2010, JCGS) | PDF in the course repo | course repo commit | PDF parser, check licence |
| `cheatsheets` | Seven Posit cheatsheets listed in `resources.qmd` | `rstudio/cheatsheets` | commit | PDFs are layout-heavy. Prefer the HTML or Quarto versions in that repo if they exist |
| `rosthoj-intro` | Introduction to R, by Susanne Rosthøj | http://biostat.ku.dk/r | n/a | not reachable during planning. Leave a stub entry in `sources.yml` marked `status: needs-source` and ask Michael for the file |

Total for the eight books is about 4.7M characters, roughly 1.2M to 1.35M tokens.

Parser order: one bookdown/Quarto parser covers seven of the eight books, so write it first. Then texinfo, then PDF. For `.Rmd` and `.qmd` sources, parse the source directly (do not render the books). Resolve bookdown cross-references to plain text where cheap, otherwise leave them.

### Licensing

Verify the licence of every source from its own repo or site and record it in `sources.yml`. Do not rely on this file for licence facts. Several of the books are believed to be under Creative Commons non-commercial licences, and some under no-derivatives terms, which is why processed text is built locally and `refs/` is gitignored. If a source turns out to be permissively licensed (for example CC BY), note it in `sources.yml` with `redistributable: true` so a prebuilt copy can be offered later. Raise anything unclear with Michael instead of guessing.

Acceptance:
- `make refs` builds every source with `status: ok` from a clean clone, with a progress line per source and a clear error if a fetch fails.
- Every section file has the header, and its URL resolves to the right page for a random sample of 20 sections (check by hand or with a script against the online books).
- A rebuild from the same pins is byte-identical (line IDs are stable).
- Total build time on a laptop is reported in the README.

## Phase 3: `search` and `cite-check`

### Index

- Chunks: section-aware, target about 300 tokens, never crossing a section file. Each chunk stores source, path, start and end line, and heading path. The indexed text is the heading path followed by the chunk text.
- Also index `course/` as source `course`, so one command covers both. Course hits get a rank boost or are listed first, since course material takes priority.
- Lexical: SQLite FTS5 with its built-in BM25 ranking.
- Dense: a small local embedding model that runs on CPU with no API key, small download, permissive licence. Check current options at build time and pick one (candidates: a static-embedding model such as the model2vec family, or a small sentence-transformers model). Prefer fast load time, since each `search` call is a new process. Store vectors in the same SQLite file or a `.npy` beside it. With fewer than 10k chunks, brute-force cosine similarity is fine.
- Fusion: reciprocal rank fusion (k = 60) over the two rankings.

### `bin/search`

```
search "query" [--source ID ...] [--k 8] [--mode hybrid|bm25|dense] [--json]
```

- Output per hit: rank, address with line range, heading path, a two-line snippet, and the BM25 and dense ranks.
- If the embedding model or vectors are missing, fall back to BM25 and print one line saying so.
- Target: under one second per query on a laptop after the first call.

### ripgrep

`rg` is the third retrieval route, used directly by the agent, not wrapped:

- Use it for exact strings and regex: function names, argument names, error messages, operators. `rg -n 'pivot_longer\(' refs/ course/` returns `path:line`, which is already a citation address.
- It does not rank and does not handle vocabulary mismatch, so it complements `search` and does not replace BM25. At this corpus size (about 5 MB of text) both are effectively instant, so the choice is about the kind of question, not speed.
- `AGENTS.md` tells the agent when to use which. The README lists ripgrep as a prerequisite and the `start` skill checks for it. If it is missing, the agent uses its built-in grep tool.

### `bin/cite-check`

```
cite-check <address> "quoted text"      # exit 0 if the quote is on those lines
cite-check --file answer.md             # checks every address and quote in a draft
```

- Matching ignores whitespace and markdown emphasis differences, nothing else.
- On failure, print the actual text of the cited lines.

Acceptance:
- `eval/golden.yml` has at least 40 questions, each with one or more correct section paths. Include at least 10 vocabulary-mismatch questions (for example "turn columns into rows" for pivoting, "repeat code for each group") and at least 10 exact-identifier questions.
- `make test` reports recall at 5 for bm25, dense, and hybrid. Hybrid must be at least as good as the better single mode. Report the numbers in the README. If dense adds nothing, say so to Michael before keeping the dependency.
- `cite-check` unit tests cover: a correct quote, a wrong line range, a paraphrase (must fail), and a missing file.

## Phase 4: skills and tutor policy

### Tutor policy (`AGENTS.md`)

Keep it short. It must state:

- What this repo is, and the map: `course/syllabus.md` first, one lecture at a time from `course/lectures/`, references through `bin/search`, `rg`, and direct file reads under `refs/`.
- Order of authority: course material first, then references. If they disagree, say so and show both.
- Run R code with `Rscript` before stating what it outputs. Never guess output.
- Cite reference claims with addresses and the section URL, and run `cite-check` on quoted text before answering.
- Teaching stance: ask what the student already knows, explain, then check understanding with a short question before moving on. Do not write the student's exercise answers for them unprompted.
- Solutions: after an attempt, or on request.
- Record progress in `progress.md` (gitignored): lectures covered, exercises attempted, open questions.
- Answer in the language the student writes in.

### Skills (`.claude/skills/<name>/SKILL.md`)

| Skill | Trigger | Behaviour |
|---|---|---|
| `start` | first use, "get started", "how do I use this" | Check R, Rscript, uv, ripgrep. Offer to run `make refs` (say how long it takes, and that the course works without it). Ask about background in three questions at most. Propose a path through the syllabus. Create `progress.md`. Show five example things to ask. |
| `lesson` | "teach me X", "lecture N", "continue" | Load one lecture. Go section by section: explain, run the code, pose a check question, wait for the answer. Finish by pointing to the matching exercise and updating `progress.md`. |
| `exercise` | "exercise N", "practice X" | Present one task at a time. Hint ladder: a nudge, then a pointer to the lecture section, then a partial approach. Run the student's code and give feedback. Show the solution after an attempt or on request, then compare it with the student's version. |
| `ask` | any content question | Check the course material first. Then `search`, `rg`, read the sections, answer with addresses and URLs, run `cite-check`. Say plainly when the references do not cover it. |
| `review` | "review my code", a pasted script or file path | Run it, then give feedback against what the course teaches (structure, naming, vectorisation, functions, project layout), most important point first. |

Write each skill body as plain markdown so other harnesses can use it. Add a short section to `AGENTS.md` listing the skills and their file paths for harnesses that do not load `.claude/skills/` on their own. Check the current skill file format in the Claude Code documentation before writing them.

Acceptance:
- For each skill, a scripted run in headless mode with a simulated student message, checked against a short rubric in `eval/` (for example: `lesson` asks a check question before continuing; `exercise` does not show the solution on the first turn unless asked; `ask` output passes `cite-check --file`).
- A full dry run of `start` on a machine without `refs/` built.

## Phase 5: student onboarding (`README.md`, "How to use this repo")

Write for a student who has used R a little and has never used an agent harness. Sections, in this order:

1. What this is, in three sentences, with a link to the course website.
2. What you need: R, git, an agent harness (Claude Code instructions first, then a short note for others), `uv`, ripgrep. One install line per operating system for each.
3. Get started: clone, open the folder in the harness, type "start". Show what the first exchange looks like.
4. What you can ask: a table of the five skills with one example prompt each, plus free-form questions.
5. How the references work: built on your own machine with `make refs`, how long it takes, how much disk it uses, and that the course works without them.
6. How to read a citation: what an address means, and how to open the cited lines yourself.
7. Solutions: you can always ask for them. The tutor will suggest trying first.
8. No terminal? Use `course/course.md`: upload it to any chat assistant. State its size in tokens.
9. Troubleshooting: R not found, `make refs` fails behind a proxy, search says "BM25 only".
10. A short note on limits: the tutor can be wrong, the citations are there so you can check, and questions about grading or course rules go to the teacher.
11. Licence and credits, including the reference books.

Acceptance:
- Someone following the README on a clean machine reaches a working `lesson` session without other help. Test the commands on macOS and Windows if possible, at least on Linux.

## Phase 6: sync and chat-only access

- GitHub Action: on a schedule and on manual dispatch, rebuild `course/` from the source repo and open a pull request if anything changed.
- CI on every push: `make course`, unit tests, and the retrieval evaluation on a small cached subset of `refs/`.
- Publish `course/course.md` as a release asset.
- Later, not now: an MCP server wrapping `search` and file reads, so chat-only students get the references too.

## Working rules for the build agent

- Verify before claiming: run the thing, and report what was run and what happened.
- Do not invent licence terms, model names, or harness features. Look them up.
- Keep dependencies few. Standard library and SQLite where possible.
- Ask Michael when blocked on: the Rosthøj source file, any unclear licence, or a retrieval result that suggests dropping the dense index.
