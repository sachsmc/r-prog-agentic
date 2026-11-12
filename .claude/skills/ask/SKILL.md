---
name: ask
description: Answer a question about R or the course content, grounded in the course material and the reference books, with checked citations. Use for any content question that is not a lesson, an exercise, or a code review.
---

# Ask

Goal: a correct, short answer that the student can check.

## 1. Course material first

- Look in `course/syllabus.md` for the lecture that covers the topic, and read the relevant part of that lecture.
- Or search: `uv run --script bin/search "the question" --source course`
- If the course covers it, base the answer on the course and name the lecture file and slide heading.

## 2. Then the references

Only if `refs/` exists. If it does not, say that the reference books are not built, and that `make refs` (or the `start` skill) builds them.

- Questions in plain words: `uv run --script bin/search "the question"`
- Exact names, arguments, operators, error messages: `rg -n 'pivot_longer\(' refs/ course/`
- Open the files that the best hits point to and read the lines around the hit. Do not answer from the snippet alone.

A hit looks like `adv-r/08-functions/05-lazy-evaluation:L5-L15`. The file is `refs/adv-r/08-functions/05-lazy-evaluation.md`. Line 2 of that file is the URL of the section in the online book.

## 3. Run code

If the answer includes R code or says what code prints, run it with `Rscript` first and show the real output.

## 4. Write the answer

- Answer the question first, in plain words. Then the example. Then the sources.
- For each claim taken from a reference, give the address and the URL, like this:
  `adv-r/08-functions/05-lazy-evaluation:L5-L6` <https://adv-r.hadley.nz/functions.html#lazy-evaluation>
- Quote only short passages. Put the quote in double quotes, followed by the address in brackets:
  "the exact words" (adv-r/08-functions/05-lazy-evaluation:L5)
- If the course and a reference disagree, say so and show both. The course comes first for this course.
- If neither covers the question, say that plainly. You may still answer from your own knowledge, and say that this is what you are doing.

## 5. Check the citations

Before you send an answer that has addresses or quotes:

- Save the draft to a temporary file and run `uv run --script bin/cite-check --file <draft>`.
- Fix every FAIL: correct the line numbers, or use the exact words, or drop the quote. Run it again until all pass.
- For a single quote you can run `uv run --script bin/cite-check <address> "quoted text"`.

## 6. Follow up

If the question shows a gap that a lecture covers, suggest that lecture. Note open questions in `progress.md`.
