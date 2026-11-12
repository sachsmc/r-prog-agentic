# Dates and character strings: exercise solutions

Solutions for exercise set 6 | Day 3, C | Online version: <https://sachsmc.github.io/r-programming/exercises/solutions/dates-and-strings.html>

## Read in the data

From the [data](../data/index.html), download and read in the file “med-2005-ex.rds”.

```r
library(here)
med2005 <- readRDS(here("data", "med-2005-ex.rds"))
```

## Dates

1.  Use the `lubridate` package (try the function `wday`) to calculate the day of the week when the dispensation occurred. Do dispensations occur less frequently on weekends?
2.  Calculate the month of the dispensation. Is there a seasonal trend on the number of dispensations?

```r
library(lubridate)

med2005$day_of_week <- wday(med2005$date, label = TRUE)

table(wday(med2005$date, label = TRUE)) |> plot()
```

[figure: plot produced by the code above]

```r
table(wday(med2005$date, label = FALSE))
```

    #>
    #>   1   2   3   4   5   6   7
    #> 588 557 596 605 565 545 596

```r
table(med2005$day_of_week %in% c("Sun", "Sat"))
```

    #>
    #> FALSE  TRUE
    #>  2868  1184

```r
binom.test(sum(med2005$day_of_week %in% c("Sat", "Sun")), nrow(med2005),
           p = 2 / 7)
```

    #>
    #>  Exact binomial test
    #>
    #> data:  sum(med2005$day_of_week %in% c("Sat", "Sun")) and nrow(med2005)
    #> number of successes = 1184, number of trials = 4052, p-value = 0.37
    #> alternative hypothesis: true probability of success is not equal to 0.28571
    #> 95 percent confidence interval:
    #>  0.27823 0.30647
    #> sample estimates:
    #> probability of success
    #>                 0.2922

```r
table(month(med2005$date, label = TRUE)) |> plot()
```

[figure: plot produced by the code above]

3.  Use `dplyr` or `data.table` to create a new variable that is the last dispensation for each individual during the year (using `group_by` then `mutate` or `:=` with `by`). Then calculate the number of days between each dispensation and the last one. What is the average number of days?

## `data.table`

```r
library(data.table)

med2005dt <- data.table(med2005)

med2005dt[, last_date := max(date),
          by = .(pid)]

med2005dt[, num_days := as.numeric(date - last_date)]
med2005dt[num_days == 0, num_days := NA]

summary(med2005dt)
```

    #>      pid                 date                atc                 dose
    #>  Length:4052        Min.   :2005-01-01   Length:4052        Min.   :   0
    #>  Class :character   1st Qu.:2005-03-30   Class :character   1st Qu.: 119
    #>  Mode  :character   Median :2005-06-29   Mode  :character   Median : 274
    #>                     Mean   :2005-06-30                      Mean   : 394
    #>                     3rd Qu.:2005-09-30                      3rd Qu.: 537
    #>                     Max.   :2005-12-31                      Max.   :3378
    #>
    #>  day_of_week   last_date             num_days
    #>  Sun:588     Min.   :2005-04-28   Min.   :-364
    #>  Mon:557     1st Qu.:2005-11-16   1st Qu.:-251
    #>  Tue:596     Median :2005-12-08   Median :-165
    #>  Wed:605     Mean   :2005-11-28   Mean   :-167
    #>  Thu:565     3rd Qu.:2005-12-23   3rd Qu.: -84
    #>  Fri:545     Max.   :2005-12-31   Max.   :  -1
    #>  Sat:596                          NA's   :400

```r
hist(med2005dt$num_days)
```

[figure: plot produced by the code above]

## `dplyr`

```r
library(dplyr)

med2005b <- med2005 |> group_by(pid) |>
  mutate(last_date = max(date))

med2005b <- med2005b |> mutate(num_days = as.numeric(date - last_date))
med2005b$num_days[med2005b$num_days == 0] <- NA

summary(med2005b)
```

    #>      pid                 date                atc                 dose
    #>  Length:4052        Min.   :2005-01-01   Length:4052        Min.   :   0
    #>  Class :character   1st Qu.:2005-03-30   Class :character   1st Qu.: 119
    #>  Mode  :character   Median :2005-06-29   Mode  :character   Median : 274
    #>                     Mean   :2005-06-30                      Mean   : 394
    #>                     3rd Qu.:2005-09-30                      3rd Qu.: 537
    #>                     Max.   :2005-12-31                      Max.   :3378
    #>
    #>  day_of_week   last_date             num_days
    #>  Sun:588     Min.   :2005-04-28   Min.   :-364
    #>  Mon:557     1st Qu.:2005-11-16   1st Qu.:-251
    #>  Tue:596     Median :2005-12-08   Median :-165
    #>  Wed:605     Mean   :2005-11-28   Mean   :-167
    #>  Thu:565     3rd Qu.:2005-12-23   3rd Qu.: -84
    #>  Fri:545     Max.   :2005-12-31   Max.   :  -1
    #>  Sat:596                          NA's   :400

```r
hist(med2005b$num_days)
```

[figure: plot produced by the code above]

## Regular expressions

The “atc” variable contains the ATC code for the drug that was dispensed. This is a standardized classification system for drugs, see <https://www.whocc.no/atc/structure_and_principles/>.

1.  Count how many dispensations there were for drugs in the class “J01”. Use the `grepl` function with a pattern. 2. Are there any “invalid” ATC codes in the dataset?

```r
grepl("^J01",med2005$atc) |>head()
```

    #> [1]  TRUE FALSE FALSE  TRUE  TRUE FALSE

```r
grepl("^J01.{4}$",med2005$atc) |> table()
```

    #>
    #> FALSE  TRUE
    #>  2397  1655

```r
## replace
gsub("^J01.{4}$", "mydrug", med2005$atc) |>head()
```

    #> [1] "mydrug"  "C10BX02" "C10BX03" "mydrug"  "mydrug"  "H05BX02"

```r
## check for invalid atcs
grepl("^[A-Z]{1}[0-9]{2}[A-Z]{2}[0-9]{2}$",
      c(med2005$atc[1:5], "100", "J01DD09b"))
```

    #> [1]  TRUE  TRUE  TRUE  TRUE  TRUE FALSE FALSE

```r
## no invalid atcs
grepl("^[A-Z]{1}[0-9]{2}[A-Z]{2}[0-9]{2}$",
  med2005$atc) |> table()
```

    #>
    #> TRUE
    #> 4052
