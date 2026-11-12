# Project organization and workflow

Lecture 1 | Day 0 | Slides: <https://sachsmc.github.io/r-programming/lectures/projects.html>

# Project organization

## Why?

See the **UCPH Policy for Research Data Management**

[figure: DataLifecycle default]

## Set up projects

Quick review of the file system

- File system discipline: put all the files related to a single project in a designated folder.
  - This applies to data, code, figures, notes, etc.
  - Depending on project complexity, you might enforce further organization into subfolders.
- A wide variety of tools to facilitate this are collected here:
  - [CRAN task view on Reproducible Research](https://cran.r-project.org/web/views/ReproducibleResearch.html#project-workflows)

## The importance of README

- Always include a README.txt or .md file at the root of the project
- Plan, Document, Share, and Preserve
- To include: *what* and *how*:
  - Title of the project
  - When it was last updated
  - What is included in the project directory
  - How to run the analysis and use the results (including what dependencies are needed)
  - A license describing the conditions of use

[Example 1](https://github.com/pablogonzalezginestet/megalearner/blob/master/README.md)

[Example 2](https://github.com/sachsmc/doubly-robust-glm/blob/master/README.md)

## An example project structure

```r
twee <- function(path = getwd(), level = Inf) {

  fad <-
    list.files(path = path, recursive = TRUE, no.. = TRUE, include.dirs = TRUE, all.files = TRUE)

  fad_split_up <- strsplit(fad, "/")

  too_deep <- lapply(fad_split_up, length) > level
  fad_split_up[too_deep] <- NULL

  jfun <- function(x) {
    n <- length(x)
    if(n > 1)
      x[n - 1] <- "|__"
    if(n > 2)
      x[1:(n - 2)] <- "   "
    x <- if(n == 1) c("-- ", x) else c("   ", x)
    x
  }
  fad_subbed_out <- lapply(fad_split_up, jfun)

  cat(unlist(lapply(fad_subbed_out, paste, collapse = "")), sep = "\n")
}

cat("example-project\n")
```

    #> example-project

```r
twee(here::here("example-project"))
```

    #> -- .here
    #> -- README.md
    #> -- code
    #>    |__01-process-data.R
    #>    |__02-primary-analysis.R
    #>    |__03-sensitivity-analysis.R
    #>    |__project-report.Rmd
    #> -- data
    #>    |__merge-analysis-dataset.rds
    #> -- documents
    #>    |__background.docx
    #>    |__protocol.docx
    #> -- output
    #>    |__Figure1.png
    #>    |__Figure2.png
    #>    |__Table1.rds
    #> -- rawdata
    #>    |__lisa-2012-full.csv
    #>    |__lisa-2013-full.csv
    #>    |__lisa-2014-full.csv
    #>    |__lisa-2015-full.csv

## R session and the working directory

```r
getwd()
```

    #> [1] "C:/Users/sachs/Teaching/r-prog-agentic/.cache/course-build-31100/lectures"

```r
list.dirs(".", recursive = FALSE)
```

    #> character(0)

```r
list.dirs("..", recursive = FALSE)
```

    #> [1] "../data"            "../example-project" "../exercises"
    #> [4] "../images"          "../lectures"

- The R session runs in the current *working directory*
- Input and output happens relative to that directory
- `"."` means “this directory”
- `".."` means “the directory that this one is contained in”

## Navigating the directory from R

Compose directories and files with `file.path` (it is safe and works in any operating system)

```r
read.csv(file.path("..", "rawdata", "lisa-2012-full.csv"))
saveRDS(analysis_file, file.path("..", "data", "analysis-data.rds"))
```

## The `here` package

```r
library(here)

here()
```

    #> [1] "C:/Users/sachs/Teaching/r-prog-agentic/.cache/course-build-31100"

```r
setwd("../exercises")
here()
```

    #> [1] "C:/Users/sachs/Teaching/r-prog-agentic/.cache/course-build-31100"

Upon librarying the `here` package, it will attempt to identify the root of your project directory: is there an `.Rproj` or `.here` file there? Then you can use the `here()` function to give the path to the root directory no matter where you are in the project directories.

```r
read.csv(here("rawdata", "lisa-2012-full.csv"))
saveRDS(analysis_file, here("data", "analysis-data.rds"))
```

Then, `here` allows you to build paths to subdirectories, starting from the project root.

Use this in your scripts, and everything will run nicely, both interactively **and** programmatically, no matter what your working directory is (as long as it is in the project).

# Workflow

## What?

Personal taste and habits (“workflow”) versus the logic and output that is the essence of your project (“product”)

- The naming/specific structure of your project directory.
- The editor you use to write your R code.

## Get comfortable

Your workflow does not matter, as long as you follow the principles.

Options for IDEs (all free):

- [Rstudio](https://www.rstudio.com/products/rstudio/download/#download)
- [VScode](https://code.visualstudio.com/docs/languages/r)
- [Emacs](https://www.gnu.org/software/emacs/)

All of these support projects, have integrated help files, code completion, and syntax highlighting.

## Setting the working directory

- Open the `.Rproj` file in a fresh R/Rstudio session
- Open an `.R` file in a new session
- Use the drop down menu in Rstudio: Session \> Set working directory
- Use `setwd()` in the terminal

*Avoid using `setwd()` in scripts*

## Bad vs good habits

**Do not**:

- use `setwd()` in scripts
- rely on `rm(list = ls())`
- save `.RData` when you quit R and don’t load `.RData` when you launch R.

**Do**:

- Restart your R session frequently while working
- Set the working directory on launch or interactively
- Use relative paths, or `here` if your project directory is complex

## Practical

- Create a toy project using your favorite tools
- Swap projects with your neighbor
- See if you can reproduce each others results

[Link to lesson](../exercises/projects.html)

[Link home](../index.html)
