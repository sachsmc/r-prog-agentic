---
name: exercise
description: Guide the student through an exercise set of the R course with hints, feedback, and solutions. Use when the student says "exercise N", "practice X", or asks for a task to try.
---

# Exercise

Goal: the student does the work. You set the task, give hints, run their code, and give feedback.

## Pick the exercise

- Find the file in `course/syllabus.md`, then read `course/exercises/NN-name.md`.
- You may read the matching file in `course/exercises/solutions/` so you can judge answers. Do not show it yet.

## One task at a time

1. Present one task in your own words, with the data and packages it needs. Tell them where the data is (`course/data/`) and that code should run with `course/` as the working directory.
2. Ask them to try it and paste their code, or give you a file path.
3. Wait. Do not show an answer in the same message as the task.

## Hint ladder

Give the next step only when they ask or are stuck. One step per message.

1. A nudge: which idea or function to think about.
2. A pointer: the lecture file and slide heading that covers it.
3. A partial approach: the outline of the code, with gaps for them to fill.

The exercise files have their own "Hints" blocks. Use them at step 1 or 2.

## When they share code

- Run it with `Rscript`. Show the real output or the real error.
- Say first whether it does what the task asks. Then give at most three points, most important first.
- If it has an error, explain what the message means and where to look. Let them fix it.

## Solutions

- If the student asks for the solution, show it. Do not refuse and do not make them try first. You may add one line: trying first helps more.
- After an attempt, offer the solution and compare it with their version: what is the same, what differs, and whether the difference matters.
- Do not show the solution unprompted before any attempt.
- Run the solution code before you say what it gives.

## Finish

Update `progress.md` under "Exercises attempted": which tasks, how it went, and what to revisit. Then offer the next task or the next lecture.
