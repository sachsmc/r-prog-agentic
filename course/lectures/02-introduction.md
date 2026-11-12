# Introduction and Overview

Lecture 2 | Day 1 | Slides: <https://sachsmc.github.io/r-programming/lectures/introduction.html>

# Introduction

## Learning objectives

- Understand and apply programming principles to handle repetitive tasks
- Understand how to use and make your own functions in R
- Use loops in R
- Apply these principles to perform efficient data manipulation, analysis, and reporting

## Why?

If your research involves any data, it likely also involves:

- Data management and manipulation
- Analysis
- Reporting of results

This means lots of **code**.

We can borrow some ideas from software development to

1.  Make our lives easier – repetitive tasks, updates with new data
2.  Make science better – reproducible, understandable, reusable

## Goals

At a bare minimum, we want our code to be:

### Organized

- Coherent structure of
  - folders, files, and scripts

### Transportable

- Works on
  - my future computer
  - other people’s computers

### Understandable

- Clearly specified dependencies
- Readable code, sensible naming of things
- Written documentation explaining what and how

## Extras

Nice to have, but not absolutely necessary

### Provably correct

Through automated testing

- Pieces of code correctly do what they should
- Code works together correctly, not sensitive to minor changes in the data
- Valid statistical properties

### Version controlled

- History of development is tracked and documented

## Overview of this course

### Lectures

### Lessons

Work through a problem together, learn tools and strategies

Share solutions/questions/responses on padlet:

<https://leaflet.pub/ba70ae31-c031-4b23-ae9f-86e9e99637b5>

Course website:

<https://sachsmc.github.io/r-programming/>

## Schedule of topics

### Today

0.  AI and LLMs
1.  Reporting, dynamic documents
2.  Data structures and indexing

### Day 2

1.  Flow control and loops
2.  Creating and using functions

### Day 3

1.  Functions continued
2.  Working with data, merging and reshaping

### Day 4

1.  Data visualization
2.  Working with data, dates and characters

# About me

## What I do

- Develop and evaluate statistical methods
  - Write R packages
  - Write R code to test the methods
- Collaborate on research projects involving data analysis
  - Use register and other data from stats Denmark
  - Data analysis, visualization and reporting

## My R philosophy

- I started learning R in 2005 (version 2.2)
- There is almost no problem that can’t be solved with R
  - Flexible and dynamic
  - Plays nicely with almost any other programming language

## Course philosophy

- There are no stupid questions
- There are many ways to solve a problem, there is no single “right way”
- I will not force you to learn any particular way, e.g., `tidyverse` vs `data.table`, we will focus on learning the general principles.
  - Try them out, then choose one and get good at it
  - Same with project organization, choose a system and stick with it
- Show up to class and participate, you will pass and hopefully learn something useful

## Take notes and practice

To get credit for the course, you must attend at least 80% of the course.

I encourage you to work on the exercises and take notes as we proceed.

1.  Use quarto to blend code, output, and prose.
2.  Demonstrate mastery of at least 3 out of the 4 learning objectives.
3.  Review the previous day’s material and build on it in the next day.

## Interactive slides

Slides will occasionally allow you to interact with the code. Follow along with lectures and use it for short quizzes. Try it out:

```r
mod <- lm(mpg ~ cyl, data = mtcars)
summary(mod)
```

    #>
    #> Call:
    #> lm(formula = mpg ~ cyl, data = mtcars)
    #>
    #> Residuals:
    #>    Min     1Q Median     3Q    Max
    #> -4.981 -2.119  0.222  1.072  7.519
    #>
    #> Coefficients:
    #>             Estimate Std. Error t value Pr(>|t|)
    #> (Intercept)   37.885      2.074   18.27  < 2e-16 ***
    #> cyl           -2.876      0.322   -8.92  6.1e-10 ***
    #> ---
    #> Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    #>
    #> Residual standard error: 3.21 on 30 degrees of freedom
    #> Multiple R-squared:  0.726,  Adjusted R-squared:  0.717
    #> F-statistic: 79.6 on 1 and 30 DF,  p-value: 6.11e-10

# AI and LLMs

## What is an LLM? A statistician’s view

**A conditional probability model over text**

$$P(\text{next token} \mid \text{text so far})$$

- Text is chopped into **tokens** (~¾ word each)
- A **context window** is the max tokens it sees at once
- **Temperature** $\tau$ controls sampling sharpness: $\tau \to 0$ → greedy; $\tau \to \infty$ → uniform

**How it’s trained**

1.  **Next-token prediction** on massive text corpora
2.  **Instruction tuning** — follow prompts, be helpful
3.  **RLHF / RLAIF** — human (or AI) preference ranking

**Code is a strength**

Code is abundant, structured, and *correct by execution* — a uniquely checkable signal in training data.

## Why they’re confident — and sometimes wrong

**Hallucination**

> The model generates *plausible text*, not *verified truth*.

- Fabricated citations that look real *(always verify)*
- Confident wrong code that compiles but is subtly incorrect
- Invented API arguments or package functions

**Reasoning models** (o3, R1, extended thinking) trade compute for better multi-step work, but the same failure modes apply at higher stakes.

> [!IMPORTANT]
>
> **Always verify**
>
> Every citation · every number every derivation · every API call
>
> Treat model output as a **hypothesis, not a result.**

> [!WARNING]
>
> **Quiet deskilling**
>
> Outsourcing judgement builds dependency, not expertise. Stay in the loop intentionally.

## The context window and memory

**What the model “sees”**

|                      | Typical range    |
|----------------------|------------------|
| Small / fast models  | 8k–32k tokens    |
| Standard assistants  | 128k–200k tokens |
| Long-context leaders | 1M+ tokens       |

A context window is **not memory** — each new conversation starts fresh.

**What counts against it**

- Your prompt
- The entire conversation so far
- Any files or code you paste in
- Tool call results

**How to work within limits**

- **Chunking**: split long documents; summarise sections before sending
- **System prompts**: keep standing instructions short and reuse across sessions
- **External memory**: project `.md` files persist context across sessions
- **Agent memory**: tools like Claude Code maintain a `CLAUDE.md` project file that persists

> [!TIP]
>
> **Practical rule**
>
> If the conversation is getting long, start fresh — older context degrades response quality before it truncates.

## Three tiers of tools

Move up the tiers as the task grows in scope and complexity.

Tier 1 **Chat interfaces**

ChatGPT · Claude · Gemini · Copilot Chat

- Paste code, ask questions
- One-shot generation
- No access to your full repo
- Good for: explaining, drafting snippets, quick checks

Tier 2 **In-IDE assistants**

GitHub Copilot · RStudio Copilot `ellmer` · `chattr` · `gander` · `chatlas`

- Autocomplete in your editor
- **`gander` knows your data frame’s columns** — context-aware suggestions
- Good for: writing functions, transforming data, iterative coding

Tier 3 **Coding agents**

Claude Code · Codex · Copilot · Pi.dev · NanoClaw

- Repo-aware — reads your whole project
- Can run code, read errors, iterate
- Work toward a goal you set
- Good for: multi-file tasks, test-driven development, simulation scaffolding

> [!TIP]
>
> **Suggested on-ramp:** start with copilot in RStudio/vscode. It is the lowest-friction step up from copy-pasting to the chat window.

## Coding agents: from autocomplete to delegate

**What makes agents different**

- **Repo-aware**: they read your `DESCRIPTION`, existing tests, README
- **Tool-use**: they can run R/Python, call the shell, read error messages
- **Iterative**: they retry when tests fail — the loop is automated
- **Transparent**: all changes come as a **diff** you review and commit

**Human-in-the-loop is not optional**

- Read the code before accepting
- Run your own checks — don’t trust “tests pass” without verifying

**Workflow**

    You: "Write a function coverage() that
          computes CI coverage, with tests"

    Agent: reads repo → writes function
           → writes tests → runs tests
           → iterates on failures
           → proposes diff

    You:  review diff → run tests yourself
          → commit if happy

> [!WARNING]
>
> **The agent proposes; you decide.** Never let an agent do something without a human reviewing.

## Text-based computer skills

**Agents live in the terminal and work with plain text. A little fluency here pays outsized dividends.**

**Key skills**

- Navigate a project directory from the command line

- Read and write **plain text files** (`.md`, `.R`, `.py`, `.txt`)

- Understand what a **project root** looks like:

      my-project/
      ├── R/              # functions
      ├── analysis/       # scripts
      ├── tests/
      ├── README.md       # what is this project?
      ├── CLAUDE.md       # instructions for the agent
      └── renv.lock       # reproducible packages

**Markdown files that guide agents**

| File                      | Purpose                                |
|---------------------------|----------------------------------------|
| `README.md`               | human-facing project overview          |
| `CLAUDE.md` / `agents.md` | standing instructions for the AI agent |
| `skills.md`               | reusable task templates                |

> [!TIP]
>
> A well-written `CLAUDE.md` is worth hours of re-prompting — the agent reads it at the start of every session.

## git: the safety net that makes agents safe

**The five operations you need**

| Command      | What it does                                         |
|--------------|------------------------------------------------------|
| `git commit` | checkpoint — a snapshot you can return to            |
| `git branch` | parallel work — experiment without risk              |
| `git diff`   | **what changed** — what you review before committing |
| `git revert` | undo a commit cleanly                                |
| pull request | propose changes for review on GitHub/GitLab          |

**Why git makes agents safe**

> *An agent proposes work as diffs you review and commit — always visible, always reversible.*

**Workflow with an agent:**

    agent writes → you diff → you test
    → you commit → repeat

If anything looks wrong: `git checkout -- .` or `git revert` puts you back exactly where you were.

## Unit tests: making “correct” checkable

**A test is a function that runs your code on a known input and asserts the expected output. It turns “I think this is right” into a pass/fail signal.**

**In R with `testthat`:**

```r
test_that("my_function is correct", {
  expect_equal(my_function(input), known_output)
  expect_error(my_function(bad_input))
})
```

**Test-driven development (TDD):**

1.  **Red** — write a failing test for the behaviour you want
2.  **Green** — write the code that makes it pass
3.  **Refactor** — clean up; tests still pass

The agent *iterates against your tests* — without tests, it has no objective criterion.

**For statisticians: what to test**

- **Correctness**: numbers you can work out by hand (simple DGMs, closed-form results)
- **Boundary conditions**: edge cases, empty inputs, length-one vectors
- **Statistical properties**: symmetry, monotonicity, bounds on estimators
- **Reproducibility**: same seed → same result

> [!TIP]
>
> Tests are not bureaucracy — they are the contract between you and the code.

## Illustration (1/2) — Ask: write the function

**Prompt quality determines output quality.**

**A rigorous prompt:**

> *“Write an R function `coverage(truth, lower, upper)` that computes the empirical coverage probability of a set of confidence intervals. `truth` is a scalar, `lower` and `upper` are equal-length numeric vectors. Return the proportion of intervals that contain `truth`. Validate that `lower` and `upper` have equal length and that `lower <= upper` element-wise. Return a scalar between 0 and 1.”*

**Generated output:**

```r
coverage <- function(truth, lower, upper) {
  stopifnot(length(lower) == length(upper))
  stopifnot(all(lower <= upper))
  mean(lower <= truth & truth <= upper)
}
```

> [!IMPORTANT]
>
> **Generated code is a hypothesis, not a result.**
>
> Read it · understand it · test it.
>
> Would you submit a simulation result without checking the DGM?

**What made this prompt good?**

- Named the function and arguments
- Specified the return type
- Specified validation behaviour
- Specified the estimand (proportion)

*Vague prompt → vague output*

~2 min. Walk through why the prompt is specific. Compare to a lazy prompt: “write a coverage function in R.” The coverage function is small enough that the audience can read and understand it in 30 seconds — that is the point. With a complex function you still need to understand it before trusting it.

## Illustration (2/2) — Test it: validity and correctness

**Tests make the agent’s loop self-correcting.**

```r
library(testthat)

test_that("coverage() is correct", {
  # Correctness — worked out by hand
  expect_equal(coverage(0, c(-1, -1), c(1,  1)), 1)   # all cover
  expect_equal(coverage(0, c( 1,  2), c(3,  4)), 0)   # none cover
  expect_equal(coverage(0, c(-1,  1), c(1,  2)), 0.5) # half cover

  # Boundary — closed endpoint counts
  expect_equal(coverage(1, 1, 2), 1)

  # Validity — bad input rejected
  expect_error(coverage(0, c(1, 2), 3))
})
```

**The TDD loop with an agent:**

    Write tests → agent writes function
    → tests FAIL (Red)
    → agent revises
    → tests PASS (Green)
    → you review diff and commit

> [!TIP]
>
> The test numbers are **yours** — you worked them out by hand. The agent cannot fake correctness against truth you define.

## Summary

- AI can be a performance booster **if used effectively**
- Learn and practice with the tools, autocomplete, agents are superior to chat
- Remember **you are responsible** for the work that is produced, so test, verify, and read
- Effective prompting and testing requires good knowledge of the R foundations, concepts, and vocabulary

# Questions?

[Link home](../index.html)
