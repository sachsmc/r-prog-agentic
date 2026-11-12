---
name: start
description: First-time setup and orientation for the R course tutor. Use when the student says "start", "get started", "how do I use this", or when progress.md does not exist yet.
---

# Start

Goal: get the student ready and agree on where to begin. Keep it short and friendly. Do one step at a time and wait for answers.

## 1. Check the tools

Run these and read the results. Do not show raw output unless something is wrong.

- `Rscript --version`
- `uv --version`
- `rg --version`
- `Rscript build/install_r_packages.R` only after asking, and only if R is present. It installs the R packages the lectures use.

Then report in plain words:

- R missing: the student cannot run code. Point to <https://cran.r-project.org> and the README section "What you need". You can still explain material, but say that you cannot run code until R is installed.
- uv missing: `search` and `cite-check` will not run. The course material still works. Point to the README.
- ripgrep missing: not a problem. Use your built-in grep tool instead.

## 2. Offer the reference books

Check whether `refs/` exists.

- If it does not, explain: the tutor can also search eight R books and a few papers and cheatsheets. Building them takes one to two minutes, needs internet, and uses about 250 MB of disk (most of it is the search model). The course works without it. Ask if they want it now.
- If yes, run `uv run build/fetch_refs.py` and then `uv run build/build_index.py`. Report what was built.
- If no, move on. They can ask for it later.
- If `refs/` exists but `.index/` does not, run `uv run build/build_index.py`.

## 3. Ask about background

Ask at most three questions, one message, short:

1. How much R have you used? (none, a little, regularly)
2. Have you written your own functions or loops before?
3. What do you want from the course? (for example: follow the lectures in order, prepare for a certain day, or get help with your own data)

## 4. Propose a path

Read `course/syllabus.md`. Suggest a path that fits the answers. For most students that is the lectures in order, starting with lecture 1. If they know some topics already, suggest which lectures to skim. Keep the proposal to a few lines and ask if it suits them.

## 5. Create progress.md

Create `progress.md` in the repo root with this shape:

```markdown
# Progress

## Student
- Background: ...
- Goal: ...
- Language: ...

## Plan
- ...

## Lectures covered

## Exercises attempted

## Open questions
```

## 6. Show what to ask

End with five example things they can type:

- "Teach me lecture 1"
- "Give me exercise 3"
- "Why does `c(1, 'a')` turn the number into text?"
- "Review my code in my-script.R"
- "Show me the solution to exercise 4"

Tell them they can also just ask any question in their own words, in any language.
