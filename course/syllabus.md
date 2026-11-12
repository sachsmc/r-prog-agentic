# Syllabus: Programming and statistical modelling in R

A four-day course at the University of Copenhagen, taught by Michael C Sachs. It takes people who already use R a little to the next level: organising projects, working with data structures, writing loops and functions, handling register data, and making graphics. Lectures are listed in teaching order.

Course website: <https://sachsmc.github.io/r-programming/>

Files are under `course/`. Data is in `course/data/`. Run R code with `course/` as the working directory so that `here("data", ...)` finds the files.

## 1. Project organization and workflow (Day 0)

- File: `course/lectures/01-projects.md`
- Goals:
    - Keep each project in one folder with a README and clear subfolders.
    - Understand the working directory and avoid `setwd()` in scripts.
    - Build file paths with the `here` package.
- Exercise: `course/exercises/01-projects.md`, solutions in `course/exercises/solutions/01-projects.md`
- Data: penguins (R package palmerpenguins)

## 2. Introduction and Overview (Day 1)

- File: `course/lectures/02-introduction.md`
- Goals:
    - Know the course goals, schedule, and how to get credit.
    - Understand in broad terms what an LLM is and why it can be wrong.
    - See why git and unit tests make AI coding tools safer to use.
- Exercise: none
- Data: none

## 3. Dynamic Documents (Day 1, A)

- File: `course/lectures/03-dynamic-documents.md`
- Goals:
    - Mix code, output, and prose in one Quarto document.
    - Write basic markdown and code chunks, and render to a report or slides.
    - Control output with chunk options and make tables look good.
- Exercise: `course/exercises/02-dynamic-documents.md`, solutions in `course/exercises/solutions/02-dynamic-documents.md`
- Data: penguins (R package palmerpenguins)

## 4. Data structures in R (Day 1, B)

- File: `course/lectures/04-data-structures.md`
- Goals:
    - Create and index vectors, lists, matrices, arrays, and data frames.
    - Spot and avoid surprises from coercion and recycling.
    - Recognise attributes, environments, S4 objects, tibbles, and data.tables.
    - Read data into R and write it out again.
- Exercise: `course/exercises/03-data-structures.md`, solutions in `course/exercises/solutions/03-data-structures.md`
- Data: reg-ex.rds, starwars.csv, starwars.xlsx, penguins (R package palmerpenguins)

## 5. Flow control and loops (Day 2, A)

- File: `course/lectures/05-flow-and-loops.md`
- Goals:
    - Control what code runs with `if`, `else`, logical operators, and `ifelse`.
    - Handle errors with `try` and `tryCatch`.
    - Write `for`, `while`, and `repeat` loops, including a bootstrap.
- Exercise: `course/exercises/04-flow-and-loops.md`, solutions in `course/exercises/solutions/04-flow-and-loops.md`
- Data: penguins (R package palmerpenguins)

## 6. Functions (Day 2, B)

- File: `course/lectures/06-functions.md`
- Goals:
    - Call functions well: arguments, `...`, composition, and the apply family.
    - Write your own functions and understand scoping and lazy evaluation.
    - Design and document functions, and know `do.call`, `get`, and recursion.
- Exercise: `course/exercises/05-functions.md`, solutions in `course/exercises/solutions/05-functions.md`
- Data: penguins (R package palmerpenguins)

## 7. Strings and dates (Day 3, A)

- File: `course/lectures/07-dates-and-strings.md`
- Goals:
    - Build and format strings with `paste`, `sprintf`, and `glue`.
    - Match and extract text with regular expressions.
    - Parse dates and do date arithmetic with `lubridate`.
- Exercise: `course/exercises/06-dates-and-strings.md`, solutions in `course/exercises/solutions/06-dates-and-strings.md`
- Data: med-2005-ex.rds, penguins (R package palmerpenguins)

## 8. Merging/joining data (Day 3, B)

- File: `course/lectures/08-merging-data.md`
- Goals:
    - Explain keys and one-to-many and many-to-many relationships.
    - Join tables in base R, `data.table`, and `dplyr`.
    - Do non-exact and rolling joins on register data.
- Exercise: `course/exercises/07-tidy-and-reshape.md`, solutions in `course/exercises/solutions/07-tidy-and-reshape.md`
- Data: lpr-ex.rds, med-2005-ex.rds to med-2010-ex.rds, penguins (R package palmerpenguins)

## 9. Tidy data (Day 3, C)

- File: `course/lectures/09-tidy-data.md`
- Goals:
    - Say what makes data tidy, in terms of variables and observations.
    - Turn model output into tidy data frames with `broom`.
    - Reshape between long and wide with pivoting and melting.
- Exercise: `course/exercises/07-tidy-and-reshape.md`, solutions in `course/exercises/solutions/07-tidy-and-reshape.md`
- Data: lpr-ex.rds, med-2005-ex.rds to med-2010-ex.rds, penguins (R package palmerpenguins)

## 10. Data visualization (Day 4, A)

- File: `course/lectures/10-dataviz.md`
- Goals:
    - Apply five principles for clear statistical graphics.
    - Build plots in layers with `ggplot2`, and know the base graphics basics.
    - Choose colour palettes, reuse plot elements, and combine figures.
- Exercise: `course/exercises/08-dataviz.md`, solutions in `course/exercises/solutions/08-dataviz.md`
- Data: penguins (R package palmerpenguins)

## 11. Summary and conclusion (Day 4, B)

- File: `course/lectures/11-conclusion.md`
- Goals:
    - Use Copilot and other LLMs for R code with care, and check what they write.
    - Recall the main points on projects, programming, and working with data.
    - Know where to go next and how to get help.
- Exercise: none
- Data: none
