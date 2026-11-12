---
name: lesson
description: Teach one lecture of the R course step by step. Use when the student says "teach me X", "lecture N", "next lecture", or "continue".
---

# Lesson

Goal: walk the student through one lecture, one section at a time, and make sure they follow.

## Pick the lecture

- Read `progress.md` if it exists, and `course/syllabus.md`.
- "Lecture N" or a topic name: find the file in the syllabus.
- "Continue": resume the lecture and section noted in `progress.md`. If nothing is noted, propose the next lecture in order.
- Read only that one lecture file from `course/lectures/`.

## Before you start

Tell the student the title, the goals from the syllabus, and how many parts there are. Ask what they already know about the topic, in one short question. Use the answer to decide how fast to go.

## For each section

A section is one or a few slide headings that belong together.

1. Explain the idea in your own plain words. Stay with what the lecture says. Use the lecture's own examples.
2. Show the code from the lecture. Run it with `Rscript` (working directory `course/`) and show the real output. Never guess output. If the lecture file marks a chunk as not running, say so and treat it as a small puzzle.
3. Where a figure is noted as `[figure: ...]`, describe what the plot shows, or offer to save it to a file with `ggsave()` or `png()` so they can open it.
4. Ask one short check question. Good check questions ask the student to predict output, spot an error, or change the code a little. Do not ask "does that make sense?".
5. Stop and wait for the answer. Do not go on to the next section in the same message.
6. When they answer: say what is right, correct what is wrong, and run code to show it if useful. Then move on.

If the student asks a side question, answer it (use the `ask` skill for anything the lecture does not cover) and then return to the lesson.

If the student wants to go faster, cover more per step, but keep the check questions.

## Finish

- Give a summary of three to five points.
- Point to the matching exercise from the syllabus, and offer to start it.
- Update `progress.md`: add the lecture under "Lectures covered" with the date, and note any open questions. If you stop in the middle, note the section where you stopped.
