---
name: review
description: Review the student's R code against what the course teaches. Use when the student says "review my code", pastes a script, or gives a path to an R, Rmd, or qmd file.
---

# Review

Goal: honest, useful feedback that helps the student write better R. Do not rewrite their whole script.

## 1. Get the code and run it

- Read the file, or save pasted code to a temporary file.
- Run it with `Rscript` (or `quarto render` for a `.qmd`, if quarto is installed). Use the folder the code expects as the working directory.
- If it needs data you do not have, ask for it, or say clearly which parts you could not run.
- Note real errors and warnings. Do not guess what the code would do.

## 2. Check against the course

Look at these points, in this order. The lecture that covers each one is in brackets.

1. Does it run, and does it do what the student wants? (ask them if the aim is unclear)
2. Project layout and paths: no `setwd()` in scripts, paths built with `here()`, raw data kept apart from results. (lecture 1, projects)
3. Structure: clear steps, no long copy and paste blocks. Repeated code should become a loop or a function. (lectures 5 and 6)
4. Functions: one job each, clear arguments with sensible defaults, no reliance on global variables, a short comment on what goes in and what comes out. (lecture 6)
5. Data structures: the right type for the job, no surprises from coercion or recycling, tidy data where it helps. (lectures 4 and 9)
6. Vectorisation: use vector operations or the apply family where a loop is slow or clumsy. A clear loop is fine. (lectures 5 and 6)
7. Naming and readability: names that say what things are, consistent style, comments that explain why.
8. Dates, strings, and joins: use the tools from the lectures, and check the keys before merging. (lectures 7 and 8)
9. Graphics: clear labels, sensible scales and colours. (lecture 10)

Read the relevant lecture part before you make a claim about what the course teaches.

## 3. Give the feedback

- Start with one or two things that are good, and mean it.
- Then at most five points, most important first. For each: what you saw (with the line), why it matters, and a small example of the better way. Run your example before you show it.
- Point to the lecture file and slide heading for each point where there is one.
- Keep changes small. Show the changed lines, not a full rewrite, unless the student asks for one.
- If the student's way differs from the course but works well, say that it is fine.

## 4. Next step

Ask which point they want to work on first, and offer to look again after they change it. Add a line to `progress.md` with the main point to practise.
