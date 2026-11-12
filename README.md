# How to use this repo

## What this is

This repo turns an AI coding assistant into a tutor for the course [Programming and statistical modelling in R](https://sachsmc.github.io/r-programming/) at the University of Copenhagen. The tutor knows the lectures and exercises, runs R code on your computer, and can look things up in the course's reference books. You talk to it in your own words, and it teaches, sets exercises, answers questions, and reviews your code.

## What you need

| Tool | What it is for | macOS | Windows | Linux (Debian, Ubuntu) |
|---|---|---|---|---|
| R | running the code | `brew install --cask r` | `winget install RProject.R` | `sudo apt install r-base` |
| git | getting this repo | `brew install git` | `winget install Git.Git` | `sudo apt install git` |
| uv | runs the search tools, installs nothing else by hand | `brew install uv` | `winget install astral-sh.uv` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| ripgrep | fast exact search | `brew install ripgrep` | `winget install BurntSushi.ripgrep.MSVC` | `sudo apt install ripgrep` |

You also need an agent harness. This is the program that lets the AI read files and run commands in this folder.

- **Claude Code** is the one this repo is tested with. Install it from <https://code.claude.com/docs/en/setup>. You need a Claude account.
- **Other harnesses** (Codex, Gemini CLI, Cursor, and others) also work if they read `AGENTS.md`. The tutor's rules are in `AGENTS.md`, and the skills are plain text files in `.claude/skills/`.

You can also use R from RStudio as usual. The tutor only needs R to be installed.

## Get started

1. Get the repo. Replace the address with the one your teacher gave you.

   ```
   git clone <address of this repo>
   cd r-prog-agentic
   ```

2. Open the folder in your harness. For Claude Code, type `claude` in a terminal in this folder.

3. Type `start`.

The first exchange looks something like this:

```
You:    start

Tutor:  I checked your setup. R, uv and ripgrep are all installed.

        The reference books are not built yet. I can search eight R books
        for you if we build them. It takes one to two minutes and needs
        internet. The course works without them. Shall I build them now?

You:    yes

Tutor:  Done. Three quick questions so I can pitch this right:
        1. How much R have you used?
        2. Have you written your own functions or loops before?
        3. What do you want from the course?
```

After that the tutor proposes where to begin, and keeps notes on your progress in a file called `progress.md`. That file stays on your computer.

## What you can ask

| You want to | Type something like |
|---|---|
| Set up and get oriented | `start` |
| Be taught a lecture step by step | `teach me lecture 4` or `continue` |
| Practise | `give me exercise 3` |
| Ask a question | `what is the difference between a list and a vector?` |
| Get feedback on your code | `review my code in analysis.R` |

You do not need special commands. Ask anything in your own words, in any language. For example: "why do I get `object not found`?", "show me another example of a for loop", or "explain that again, more slowly".

## How the references work

The tutor can search these books and papers: An Introduction to R, R for Data Science (1st edition), Statistical Inference via Data Science (ModernDive), Hands-On Programming with R, Advanced R, R Graphics Cookbook, R Markdown: The Definitive Guide, R Markdown Cookbook, two papers by Hadley Wickham, and seven Posit cheatsheets.

Most of these books may not be copied into a public repo. So the text is downloaded and prepared on your own computer:

```
uv run build/fetch_refs.py     # or: make refs
uv run build/build_index.py    # or: make index
```

- Time: about 30 seconds for the books and about 15 seconds for the search index on a laptop, plus a one-time download of a small search model (about 130 MB).
- Disk: about 100 MB in this folder (`refs/`, `.index/`, `.cache/`), plus about 125 MB for the search model in your user cache folder.
- It needs internet once. After that, search works offline.
- The course works without the references. The tutor then answers from the course material only, and says so.

## How to read a citation

When the tutor uses a reference book, it gives an address and a link, like this:

```
adv-r/08-functions/05-lazy-evaluation:L5-L6
https://adv-r.hadley.nz/functions.html#lazy-evaluation
```

- `adv-r` is the book (Advanced R). `08-functions` is the chapter. `05-lazy-evaluation` is the section.
- `L5-L6` means lines 5 to 6 of the file `refs/adv-r/08-functions/05-lazy-evaluation.md`.
- The link opens the same section in the online book.

To see the cited lines yourself, open that file in any editor and go to the line numbers. Or ask the tutor: "show me those lines". Addresses that start with `course/` point to the course material in the same way.

The tutor checks its own quotes with a tool before it answers. You can run the check too:

```
uv run --script bin/cite-check adv-r/08-functions/05-lazy-evaluation:L5 "function arguments are lazily evaluated"
```

## Solutions

You can always ask for a solution, and the tutor will show it. It will suggest that you try first, because that is how you learn the most. After you have tried, it compares your answer with the course solution.

## No terminal?

If you cannot or do not want to use an agent harness, use the file [`course/course.md`](course/course.md). It holds the syllabus, all lectures, all exercises, and all solutions in one file of about 64,000 tokens. Upload it to any chat assistant that accepts files and ask your questions there. That assistant cannot run R code or search the reference books, so check its answers by running the code yourself.

## Troubleshooting

**R not found.** Install R from <https://cran.r-project.org>. Then close and reopen your terminal. Check with `Rscript --version`. On Windows, if R is installed but still not found, add its `bin` folder (for example `C:\Program Files\R\R-4.5.0\bin`) to your PATH, or ask the tutor to help you do it.

**A package is missing.** Run `Rscript build/install_r_packages.R`. It installs the packages that the lectures use.

**`make` is not found.** You do not need it. Use the `uv run ...` commands shown above.

**Building the references fails behind a proxy.** The build downloads from github.com and huggingface.co. Set the proxy for your terminal and run it again:

```
export HTTPS_PROXY=http://your-proxy:port        # macOS, Linux
$env:HTTPS_PROXY = "http://your-proxy:port"      # Windows PowerShell
```

Sources that were already downloaded are kept, so the second run is faster.

**Search says "BM25 only".** The search model is missing, so search uses word matching only. It still works. To add the model, run `uv run build/build_index.py` while you are online.

**Search says the index is missing.** Run `uv run build/build_index.py`.

## Limits

- The tutor can be wrong. It is built to run code before it tells you what code does, and to cite its sources. Use the citations to check anything that matters.
- It does not know your grades, deadlines, or the rules of the course. Questions about credit, attendance, or exams go to the teacher.
- Check the current University of Copenhagen guidelines on the use of AI tools in your work.

## Licence and credits

The course material is by Michael C Sachs, Section of Biostatistics, University of Copenhagen. It comes from <https://github.com/sachsmc/r-programming> and is under the MIT licence.

The reference texts are not part of this repo. They are downloaded from their own sources when you build them, and each keeps its own licence:

| Source | Authors | Licence |
|---|---|---|
| [An Introduction to R](https://cran.r-project.org/doc/manuals/r-release/R-intro.html) | W. N. Venables, D. M. Smith and the R Core Team | R manual permission notice |
| [R for Data Science, 1st edition](https://r4ds.had.co.nz/) | Hadley Wickham, Garrett Grolemund | CC BY-NC-ND 3.0 US |
| [Statistical Inference via Data Science](https://moderndive.com/v2/) | Chester Ismay, Albert Y. Kim, Arturo Valdivia | CC BY-NC-SA 4.0 |
| [Hands-On Programming with R](https://rstudio-education.github.io/hopr/) | Garrett Grolemund | CC BY-NC-ND 4.0 |
| [Advanced R, 2nd edition](https://adv-r.hadley.nz/) | Hadley Wickham | CC BY-NC-SA 4.0 |
| [R Graphics Cookbook, 2nd edition](https://r-graphics.org/) | Winston Chang | no open licence stated, free to read online |
| [R Markdown: The Definitive Guide](https://bookdown.org/yihui/rmarkdown/) | Yihui Xie, J. J. Allaire, Garrett Grolemund | CC BY-NC-SA 4.0 |
| [R Markdown Cookbook](https://bookdown.org/yihui/rmarkdown-cookbook/) | Yihui Xie, Christophe Dervieux, Emily Riederer | CC BY-NC-SA 4.0 |
| [Tidy Data](https://www.jstatsoft.org/article/view/v059i10) | Hadley Wickham | CC BY 3.0 |
| [A Layered Grammar of Graphics](https://doi.org/10.1198/jcgs.2009.07098) | Hadley Wickham | copyright American Statistical Association and others |
| [Posit cheatsheets](https://rstudio.github.io/cheatsheets/) | Posit and contributors | CC BY 4.0 |

The exact versions and where each licence was read are in [`sources.yml`](sources.yml). The search model is [potion-retrieval-32M](https://huggingface.co/minishlab/potion-retrieval-32M) (MIT licence).

## For maintainers

- `make course` rebuilds `course/` from the pinned commit of the course repo. It needs quarto, R, and the packages in `build/r-packages.txt`.
- `make test` runs the unit tests and the retrieval evaluation. Recall at 5 on the 49 questions in `eval/golden.yml` (12 Nov 2026): BM25 0.94, dense 0.90, hybrid 0.94.
- `uv run eval/check_urls.py --n 20` checks section links against the online books.
- `uv run eval/run_skill_checks.py` runs scripted checks of the five skills. It needs the `claude` command.
- The design and the acceptance checks are in [`BUILD_PLAN.md`](BUILD_PLAN.md).
