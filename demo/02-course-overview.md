# Demo 2: Course overview

The student asks how the course fits together. The tutor answers from the syllabus and from its own notes on this student. This comes later in the same session, after a lesson, an exercise, and a code review, which is why the tutor knows where the student is.

*A real exchange with the tutor in this repo, from 12 November 2026. The student is played by a second AI session. The words are unchanged. Headings in the tutor's replies are shown as bold text, and cuts are marked [...].*

---

**Student**

> New day, new question. Before I go on: can you give me an overview of the whole course? What are the lectures, and how do they fit together?

**Tutor**

Here is the whole course in one view. It comes from `course/syllabus.md`. The course is four days plus a preparation day, with 11 lectures and 8 exercise sets.

**The lectures**

| # | Lecture | Day | What you learn | Exercise |
|---|---|---|---|---|
| 1 | Project organization and workflow | 0 | One folder per project, the working directory, paths with `here` | 1 |
| 2 | Introduction and overview | 1 | Course goals, what an LLM is, why git and tests matter | none |
| 3 | Dynamic documents | 1 | Code, output, and text in one Quarto document | 2 |
| 4 | Data structures | 1 | Vectors, lists, matrices, data frames, indexing, reading data | 3 |
| 5 | Flow control and loops | 2 | `if`, `else`, `ifelse`, `tryCatch`, `for`, `while`, `repeat` | 4 |
| 6 | Functions | 2 | Calling functions well, writing your own, scoping, lazy evaluation | 5 |
| 7 | Strings and dates | 3 | `paste`, `sprintf`, regular expressions, `lubridate` | 6 |
| 8 | Merging and joining data | 3 | Keys, joins in base R, `data.table`, and `dplyr` | 7 |
| 9 | Tidy data | 3 | What tidy means, `broom`, long and wide format | 7 |
| 10 | Data visualization | 4 | Principles for clear graphics, `ggplot2`, colours | 8 |
| 11 | Summary and conclusion | 4 | Using LLMs for R with care, main points, where to go next | none |

Lectures 8 and 9 share one exercise set.

**How they fit together**

Think of it as four layers. Each one builds on the one before.

1. **Getting organised (lectures 1 to 3).** Where your files live, and how to write a report that contains its own code. This is the frame around everything else. Your `setwd()` question from the code review belongs here.

2. **The building blocks (lecture 4).** Everything in R is stored in a data structure. You need to know how to pick out elements with `[ ]` and `[[ ]]` before you can do much with them.

3. **Programming (lectures 5 and 6).** This is the heart of the course. Loops repeat code over the elements of a data structure. Functions wrap code so you can reuse it. Lecture 6 builds directly on lecture 5.

4. **Working with real data (lectures 7 to 10).** Here you use the programming skills on practical tasks: clean up text and dates, combine tables, reshape them, and plot the result. This is the order of a real analysis too.

Lecture 11 ties it together.

**Where you are**

- Lecture 5: paused after part 2 of 7. The loop parts are still to come.
- Exercise 4: task 1 done, solution to task 2 seen.
- Your plan: finish lecture 5, then lecture 6, then go back to lectures 1, 3, and 4, and on to 7 to 10.

You chose to start in layer 3, which is fine. The one place it pinches is indexing from lecture 4, so I will add that as a short warm-up before the loop examples.

Do you want to continue lecture 5 now, or go on with exercise 4?
