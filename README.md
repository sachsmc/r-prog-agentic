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
   git clone https://github.com/sachsmc/r-prog-agentic.git
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

<!-- demo:start -->
## Demo

Four short conversations show what the tutor does. They are real exchanges with the tutor in this repo, from 12 November 2026. The student is played by a second AI session. The words are unchanged. Headings in the tutor's replies are shown as bold text, and cuts are marked [...].

What to look for:

- The tutor runs code before it says what the code prints.
- It answers from the course first, and names the lecture and slide.
- Quotes from the reference books come with an address and a link, and are checked by a tool.
- It asks a question and waits, and does not hand out exercise answers unless asked.
- It keeps notes on the student and picks up where they left off.

### 1. Setup

The student types one word. The tutor checks the computer, installs what is missing, builds the reference books, asks about background, and proposes a plan.

<details>
<summary>Show the conversation</summary>

**Student**

> start

**Tutor**

Welcome to the course! I am your tutor for "Programming and statistical modelling in R".

I checked your computer. Everything needed is there:

- **R** 4.4.2: I can run code for you.
- **uv**: search over the course material works.
- **ripgrep**: fast text search works.

Two optional setup steps remain:

1. **R packages.** The lectures use some R packages. I can install them with `Rscript build/install_r_packages.R`. This needs internet and may take a few minutes.
2. **Reference books.** I can also search eight R books plus a few papers and cheatsheets. Building them takes one to two minutes, needs internet, and uses about 250 MB of disk. The course works without them, and you can ask for them later.

Tell me which of these you want, and then I will ask a few short questions about your background.

---

**Student**

> Yes, both

**Tutor**

The R packages are ready: all 20 packages the lectures use are installed. The reference books are still building in the background. I will tell you when they are done.

While that runs, three short questions:

1. How much R have you used? (none, a little, regularly)
2. Have you written your own functions or loops before?
3. What do you want from the course? For example: follow the lectures in order, prepare for a certain day, or get help with your own data.

Answer in your own words, in any language you like.

[...]

---

**Student**

> 1. I have used R a little, mostly running scripts my supervisor gave me and changing small things. 2. I have never written my own function. I copied a for loop once but I did not really understand it. 3. I want to follow the lectures, but I am most worried about loops and functions, so I would like to start there.

**Tutor**

Setup is finished, and I have a plan for you.

**Setup**

- All 20 R packages for the lectures are installed.
- The reference books are built: 12 sources, among them *R for Data Science*, *Advanced R*, and *Hands-On Programming with R*. I tested the search and it works.
- One source, `rosthoj-intro`, was skipped because its source file is not available. That is a note for the teacher, not a problem for you.

**Your plan**

Thanks for your answers. Starting with loops and functions is a good choice. Here is what I suggest:

1. **Short warm-up** from lecture 4: vectors, lists, and how to pick out elements with `[ ]` and `[[ ]]`. A loop works through these one element at a time, so loops are much easier once this is clear.
2. **Lecture 5: Flow control and loops**, then exercise 4. We will take the for loop apart piece by piece, so you understand it instead of copying it.
3. **Lecture 6: Functions**, then exercise 5. You will write your first own function here.
4. After that, back to the start: lectures 1 and 3, the rest of 4, then 7 to 10 in order.

I saved your background and this plan in `progress.md`, so we can pick up where we left off next time.

**Things you can type**

- "Teach me lecture 5"
- "Give me exercise 4"
- "Why does `c(1, 'a')` turn the number into text?"
- "Review my code in my-script.R"
- "Show me the solution to exercise 4"

You can also ask any question in your own words, in any language.

</details>

As a file: [`demo/01-setup.md`](demo/01-setup.md)

### 2. Course overview

The student asks how the course fits together. The tutor answers from the syllabus and from its own notes on this student. This comes later in the same session, after a lesson, an exercise, and a code review, which is why the tutor knows where the student is.

<details>
<summary>Show the conversation</summary>

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

</details>

As a file: [`demo/02-course-overview.md`](demo/02-course-overview.md)

### 3. A question about a lecture, then a deeper dive

The student asks about lecture 9. The tutor answers from the lecture, runs the lecture's code, and backs it with quotes from the reference books. Each quote has an address (book, chapter, section, line numbers) and was checked with `cite-check` before the tutor answered. Then the student asks about their own data, and the tutor goes deeper into the references.

<details>
<summary>Show the conversation</summary>

**Student**

> Thanks, that is a helpful map. I looked ahead at lecture 9 because my own data is a mess. What does it mean that data is "tidy"? And what does pivot_longer do?

**Tutor**

Both answers are in lecture 9 (`course/lectures/09-tidy-data.md`). Here is the short version.

**What "tidy" means**

Tidy data follows three rules (slide "Tidy data"):

1. Each variable forms a column.
2. Each observation forms a row.
3. Each type of observational unit forms a table.

A *variable* is something you measure, like weight or week. An *observation* is one unit you measured, like one patient at one visit.

The lecture takes this definition from a paper by Hadley Wickham, which is among the reference books. The paper adds a blunt line about the opposite:

> "Messy data is any other arrangement of the data." (tidy-data/02-defining-tidy-data/03-tidy-data:L12)

<https://www.jstatsoft.org/article/view/v059i10>

So "tidy" does not mean clean or free of errors. It is only about the *shape*: what is a row and what is a column.

**A messy example**

The lecture uses this small table (slide "Messy data example"). I ran it:

```r
#>   artist    wk1   wk2
#> 1 2 Pac       1     2
#> 2 Creed       3     4
#> 3 Mos Def     5     6
#> 4 Aaliyah     2    NA
```

It looks neat, but it breaks rule 1. "Week" is a variable, and it has no column of its own. It is hidden in the column *names* `wk1` and `wk2`. The lecture calls this "wide format". *R for Data Science* describes the same problem:

> "A common problem is a dataset where some of the column names are not names of variables, but values of a variable." (r4ds/12-tidy-data/03-pivoting:L27)

<https://r4ds.had.co.nz/tidy-data.html#pivoting>

**What `pivot_longer` does**

It fixes exactly this problem. It takes several columns and stacks them into two new columns: one for the old column names, one for the values (slide "Pivoting data"):

```r
billboard |>
    pivot_longer(
    cols = starts_with("wk"),
    names_to = "week",
    values_to = "rank",
    values_drop_na = TRUE
  )
#>   artist  week   rank
#> 1 2 Pac   wk1       1
#> 2 2 Pac   wk2       2
#> 3 Creed   wk1       3
#> 4 Creed   wk2       4
#> 5 Mos Def wk1       5
#> 6 Mos Def wk2       6
#> 7 Aaliyah wk1       2
```

The arguments, one by one:

- `cols`: which columns to stack. Here, all that start with "wk".
- `names_to`: the new column that receives the old column names (`wk1`, `wk2`).
- `values_to`: the new column that receives the numbers.
- `values_drop_na = TRUE`: leave out rows with a missing value. That is why Aaliyah has one row, not two.

The table went from 4 rows and 3 columns to 7 rows and 3 columns. Now every row is one artist in one week, and week is a real column. *R for Data Science* sums it up:

> "`pivot_longer()` makes datasets longer by increasing the number of rows and decreasing the number of columns." (r4ds/12-tidy-data/03-pivoting:L61)

The reverse is `pivot_wider` (slide "Pivoting from long to wide").

I checked all the quotes with `cite-check`, and they pass. The course and the books agree.

**Why bother**

Most R tools expect tidy data. With the long table you can group by week, plot rank against week, or put week in a model. With the wide table, each of those needs a workaround.

**Your own data**

"A mess" can mean many things, and not all of them are fixed by pivoting. What does your data look like? For example: do you have one row per person with columns like `weight_2020`, `weight_2021`? Describe the columns to me, or paste the first few rows, and I can tell you whether `pivot_longer` is the right tool.

---

**Student**

> Can you go one step deeper? My data has one column per year, like income_2019, income_2020, income_2021. Why is that a problem exactly, and what do the books or papers say I should do about it?

**Tutor**

Your data has a shape that the tidy data paper names directly. Here is the deeper version.

**Why it is a problem**

Your data has two variables there: **year** and **income**. But it has three columns, and none of them is called "year". The years 2019, 2020, and 2021 are *values* of the variable year, and they sit in the column names.

The tidy data paper lists this as the first of the common problems with messy data: "column headers are values, not variable names" (tidy-data/03-tidying-messy-datasets/01-column-headers-are-values-not-variable-names:L5). It also describes your exact case:

> "Another common use of this data format is to record regularly spaced observations over time." (tidy-data/03-tidying-messy-datasets/01-column-headers-are-values-not-variable-names:L29)

<https://www.jstatsoft.org/article/view/v059i10>

In practice this hurts in three ways. I made up a small table to show it. These are invented numbers, not real data:

```r
#>   id    sex   income_2019 income_2020 income_2021
#> 1 A     f             310         325         340
#> 2 B     m             280          NA         295
#> 3 C     f             400         410         405
```

1. **You cannot use year in your code.** R cannot group by year, put year on the x-axis of a plot, or use year in a model, because year is not a column.
2. **You repeat yourself.** The mean income per year needs one line per column, like the copy-paste lines in the script we reviewed:

   ```r
   c(mean(wide$income_2019, na.rm = TRUE),
     mean(wide$income_2020, na.rm = TRUE),
     mean(wide$income_2021, na.rm = TRUE))
   #> [1] 330.0000 367.5000 346.6667
   ```
3. **New data breaks your code.** When `income_2022` arrives, you must edit every such place.

The course makes the same point in general terms: "It is easier to make comparisons between groups of observations than across variables" (course/lectures/09-tidy-data:L131, slide "Variables and observations"). Comparing years is a comparison across your columns, which is the hard direction.

**What the books say to do**

The paper's remedy:

> "To tidy it, we need to melt, or stack it." (same section, L15)
> "In other words, we need to turn columns into rows." (same section, L16)

"Melt" is the older word. Today the function is `pivot_longer`, as in lecture 9, slide "Pivoting data". *R for Data Science* says you need to decide three things (r4ds/12-tidy-data/03-pivoting:L37-L41, <https://r4ds.had.co.nz/tidy-data.html#pivoting>):

- "The set of columns whose names are values, not variables." For you: the three income columns.
- "The name of the variable to move the column names to." For you: `year`.
- "The name of the variable to move the column values to." For you: `income`.

Put together, and run on my made-up table:

```r
long <- wide |>
  pivot_longer(
    cols = starts_with("income_"),
    names_to = "year",
    names_prefix = "income_",
    names_transform = list(year = as.integer),
    values_to = "income"
  )
long
#>   id    sex    year income
#> 1 A     f      2019    310
#> 2 A     f      2020    325
#> 3 A     f      2021    340
#> 4 B     m      2019    280
#> 5 B     m      2020     NA
#> ...  (9 rows in total)
```

Two arguments here are not in the lecture's example. I know them from the `tidyr` documentation, so this part is my own knowledge: `names_prefix` cuts "income_" off the names, and `names_transform` turns the text "2019" into the number 2019. See `?pivot_longer`.

Now the mean per year is one short step, and it keeps working when 2022 is added:

```r
long |> group_by(year) |> summarize(mean_income = mean(income, na.rm = TRUE))
#>    year mean_income
#> 1  2019        330 
#> 2  2020        368.
#> 3  2021        347.
```

Same numbers as before.

**One honest caveat**

The wide shape is not wrong for every purpose. The paper says: "This form of storage is not tidy, but it is useful for data entry." (same section, L34). The course agrees that wide format "also has its uses", for example correlation matrices and readable tables (lecture 9, slide "Pivoting from long to wide"). So: keep the file as it is, pivot to long for analysis, and pivot back with `pivot_wider` when you need a table. I checked that the round trip gives back the original table.

All nine quotes pass `cite-check`.

**Check question**

Suppose your real data has 100 people and the three income columns. After `pivot_longer`, how many rows does the long table have? And what happens to a column like `sex` that you did not pivot?

If you like, tell me which other columns your file has, and we can write the pivot for your real data together.

</details>

As a file: [`demo/03-lecture-question.md`](demo/03-lecture-question.md)

### 4. Help with an exercise

The tutor sets one task and waits. It runs the student's attempt, explains what went wrong, and leaves the fix to the student. When the student asks for a solution, it shows it at once.

<details>
<summary>Show the conversation</summary>

**Student**

> [...] I would like to try exercise 4 instead.

**Tutor**

[...]

**Exercise 4: Flow control and loops**

The set has four blocks: simple loops, loops for statistics on the penguins data, a numeric calculation, and an optional block. We take one task at a time.

**Task 1** (block "Simple loops and conditional statements")

Use a loop to print every number from 1 to 10.

You need no data and no packages for this one. Later tasks use the `palmerpenguins` package, which is already installed.

Try it and paste your code here, or give me the path to a file. A guess that does not work is welcome too. If you do not know where to begin, say "hint".

---

**Student**

> Here is my try:
>
> for (i in 1:10) {
>   print(1:10)
> }
>
> It prints a lot more than I expected and I do not understand why.

**Tutor**

Good try. You are closer than you think. I ran your code:

```
 [1]  1  2  3  4  5  6  7  8  9 10
 [1]  1  2  3  4  5  6  7  8  9 10
 [1]  1  2  3  4  5  6  7  8  9 10
 ... (10 lines in total, all the same)
```

It does not do what the task asks yet: you get ten lines of ten numbers, instead of ten lines with one number each. But the first line of your loop is exactly right.

**Why it prints so much.** A `for` loop has two pieces:

- `for (i in 1:10)` says: run the body 10 times. In the first round `i` is 1, in the second round `i` is 2, and so on up to 10.
- The body, inside `{ }`, is what runs in each round.

Your body is `print(1:10)`. That prints all ten numbers. The loop runs it 10 times, so you see all ten numbers, ten times over.

**Where to look.** Notice that `i` does not appear anywhere in your body. So every round does the same thing. The lecture has an example where the body does use it (lecture 5, slide "For loops"):

```r
for(i in 1:5) {
  if(i == 2) next
  print(paste("hello", i))
}
```

Change one thing inside your `print()` so that each round prints only the number for that round. Paste your new version when you have it.

---

**Student**

> Oh! I should print i, not 1:10. So it is print(i) inside the loop. For the next task with the even numbers, can you just show me the solution? I want to see how it is done.

**Tutor**

Yes, `print(i)` is it, and you found it yourself. I ran it:

```r
for (i in 1:10) {
  print(i)
}
#> [1] 1
#> [1] 2
#> ...
#> [1] 10
```

This matches the course solution exactly. The key idea you now have: `i` holds a different value in each round, and the body uses it.

**Task 2: the solution**

The task: change the loop so it prints only the *even* numbers from 1 to 10. Here is the solution from the course (exercise 4 solutions, "Simple loops and conditional statements"):

```r
for(i in 1:10){
  if((i %% 2) == 0) {
    print(i)
  }
}
#> [1] 2
#> [1] 4
#> [1] 6
#> [1] 8
#> [1] 10
```

How it works:

- The loop is the same as yours. `i` still goes from 1 to 10.
- The new piece is the `if` around `print(i)`. The number is printed only when the condition is `TRUE`.
- `%%` gives the remainder after division. I ran `7 %% 2`, which gives `1`, and `8 %% 2`, which gives `0`. An even number has remainder 0 when divided by 2.
- So `(i %% 2) == 0` asks: "is `i` even?"

This connects to what you learned today. Inside the loop, `i` is a single number, so the condition is a single `TRUE` or `FALSE`. That is exactly what `if` needs. This is why loops and `if` work so well together.

Trying a task first usually helps more than reading the answer, so here is a small one to make this solution your own: what would you change to print the *odd* numbers instead?

After that, the next task uses real data: a loop that prints the mean of each numeric variable in the `penguins` data. Or we stop here for today. Your choice.

</details>

As a file: [`demo/04-exercise.md`](demo/04-exercise.md)
<!-- demo:end -->

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
