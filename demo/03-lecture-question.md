# Demo 3: A question about a lecture, then a deeper dive

The student asks about lecture 9. The tutor answers from the lecture, runs the lecture's code, and backs it with quotes from the reference books. Each quote has an address (book, chapter, section, line numbers) and was checked with `cite-check` before the tutor answered. Then the student asks about their own data, and the tutor goes deeper into the references.

*A real exchange with the tutor in this repo, from 12 November 2026. The student is played by a second AI session. The words are unchanged. Headings in the tutor's replies are shown as bold text, and cuts are marked [...].*

---

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
