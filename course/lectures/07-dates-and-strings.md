# Strings and dates

Lecture 7 | Day 3, A | Slides: <https://sachsmc.github.io/r-programming/lectures/dates-and-strings.html>

# Basic string stuff

## Special characters

- Strings are enclosed in single or double quotes
- “\\” is treated as an “escape character” in strings, meaning whatever comes after it is treated as special, e.g., “\n” for newline, “\t” for tab
- To get quotes inside quotes, you can
  - mix single and double: `"'Woof', he barked"`
  - escape with backslash: `"\"Woof\", he barked"`
- To get a backslash, you need to escape the backslash: `"\\"`

## Combining strings

You know about `paste` and `paste0`. I like to use `sprintf(<format>, ...)`

The format contains special characters starting with “%” to determine how the character should look, and data passed to the `...` gets inserted into the format:

```r
library(palmerpenguins)
sprintf("mean and sd of %s: %.2f (%.2f)", "bill depth (mm)",
        mean(penguins$bill_depth_mm, na.rm = TRUE),
        sd(penguins$bill_depth_mm, na.rm = TRUE))
```

    #> [1] "mean and sd of bill depth (mm): 17.15 (1.97)"

“%s” means string, “%.2f” means a float with 2 digits after the decimal

Use “%%” to get a literal percent

```r
sprintf("n and percent male: %.0f (%.1f%%)",
        sum(penguins$sex == "male", na.rm = TRUE),
        100 * sum(penguins$sex == "male", na.rm = TRUE) / nrow(penguins) )
```

    #> [1] "n and percent male: 168 (48.8%)"

See also the `glue` package for a different way to do this.

## `glue`

`glue` is a package that allows you to insert R code into strings

```r
library(glue)

glue("n and percent male: {round(nmale)} ({round(percentmale, 1)}%)",
        nmale = sum(penguins$sex == "male", na.rm = TRUE),
        percentmale = 100 * sum(penguins$sex == "male", na.rm = TRUE) / nrow(penguins)            )
```

    #> n and percent male: 168 (48.8%)

It is quite flexible and works well with data frames as well

```r
library(dplyr)
penguins |> group_by(species) |>
  summarize(mean_bill = mean(bill_length_mm, na.rm = TRUE)) |>
  glue_data("The mean bill length for {species} is {round(mean_bill, 1)}mm")
```

    #> The mean bill length for Adelie is 38.8mm
    #> The mean bill length for Chinstrap is 48.8mm
    #> The mean bill length for Gentoo is 47.5mm

# Regular expressions

## Register example

“… any diagnosis of either D150, D152, or D159 before the date 1 January 2010”

```r
lpr$diag[lpr$date <= as.Date("2010-01-01")] %in%
  c("D150", "D152", "D159")
```

- We can save typing by being clever matching the codes (e.g., “starts with D15”)
- Dates and times are tricky, though this example is unambiguous

## Character matching

*Regular expressions* are abstract patterns of characters that describe a text sequence

You can use them with `grep` and related functions in base R. Also see the `stringr` package.

Example “starts with”

```r
grepl(pattern= "^D15",
      c("D150", "D152", "D159",
        "A250", "Z149"))
```

    #> [1]  TRUE  TRUE  TRUE FALSE FALSE

## Regexp operators

Certain characters in regexps have special meaning

- `^`: starts with
- `$`: ends with
- `|`: or
- `*`: 0 or more times
- `+`: 1 or more times
- `{n}`: n times
- `(...)`: sub-expression
- `[...]`: character classes

examples

```r
"^[A-Z][0-9]{3}$" ## match all ICD codes
"^D15[029]$" ## our codes of interest
```

## Get help

Regexps can be very complex, but for simple patterns they can save you time

Write and double-check your pattern:

- The cheatsheet on strings and regular expressions
- R 4 Data Science, chapter on regular expressions
- https://regex101.com/

# Dates and times

## Some faulty assumptions about dates and times

- All days have 24 hours
- All years have 365 days (ok not an assumption, but which ones?)
- Dates are always written “day - month - year”

## Use `lubridate`

`lubridate` will solve most of these problems:

- Importing dates from character strings
- Printing dates in a nice format
- Computing time intervals

## Register example

```r
as.Date("2010-01-01")
```

    #> [1] "2010-01-01"

```r
as.Date("2010-05-10") ## ambiguous!
```

    #> [1] "2010-05-10"

```r
library(lubridate)

ymd("2010-05-10")
```

    #> [1] "2010-05-10"

```r
ymd("2010-05-10") - ymd("2010-01-01")
```

    #> Time difference of 129 days

```r
as.numeric(ymd("2010-05-10") - ymd("2010-01-01"))
```

    #> [1] 129

## Practical

We will continue using the register data example to practice merging and defining new variables based on dates and strings.

[Link to lesson](../exercises/dates-and-strings.html)

[Link home](../index.html)
