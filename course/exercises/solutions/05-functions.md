# Functions: exercise solutions

Solutions for exercise set 5 | Day 2, B | Online version: <https://sachsmc.github.io/r-programming/exercises/solutions/functions.html>

## Iterating over data with functions

1.  Load the Palmer penguins dataset.
2.  Write a function to compute the mean and standard deviation of a numeric vector. We will apply this function to the numeric variables in `penguins`, and also by different subgroups

```r
library(palmerpenguins)

mean_sd1 <- function(x, na.rm = TRUE) {

  res <- c(mean = mean(x, na.rm = na.rm),
    sd = sd(x, na.rm = na.rm))

  res

}

mean_sd1(penguins$bill_depth_mm)
```

    #>    mean      sd
    #> 17.1512  1.9748

## Using the function

1.  Use your function to compute the mean and sd of all the numeric variables in `penguins`.

```r
numeric_cols <- sapply(penguins, is.numeric) ## determine which cols are numeric
apply(penguins[numeric_cols], MARGIN = 2, FUN = mean_sd1)
```

    #>      bill_length_mm bill_depth_mm flipper_length_mm body_mass_g       year
    #> mean        43.9219       17.1512           200.915     4201.75 2008.02907
    #> sd           5.4596        1.9748            14.062      801.95    0.81836

2.  Use your function to compute the mean and sd of body mass by species and sex

## Base R

```r
split(penguins$body_mass_g, list(penguins$species, penguins$sex)) |>
  lapply(FUN = mean_sd1)
```

    #> $Adelie.female
    #>    mean      sd
    #> 3368.84  269.38
    #>
    #> $Chinstrap.female
    #>    mean      sd
    #> 3527.21  285.33
    #>
    #> $Gentoo.female
    #>    mean      sd
    #> 4679.74  281.58
    #>
    #> $Adelie.male
    #>    mean      sd
    #> 4043.49  346.81
    #>
    #> $Chinstrap.male
    #>    mean      sd
    #> 3938.97  362.14
    #>
    #> $Gentoo.male
    #>    mean      sd
    #> 5484.84  313.16

```r
# sapply converts the result to a matrix
split(penguins$body_mass_g, list(penguins$species, penguins$sex)) |>
  sapply(FUN = mean_sd1)
```

    #>      Adelie.female Chinstrap.female Gentoo.female Adelie.male Chinstrap.male
    #> mean       3368.84          3527.21       4679.74     4043.49        3938.97
    #> sd          269.38           285.33        281.58      346.81         362.14
    #>      Gentoo.male
    #> mean     5484.84
    #> sd        313.16

```r
# tapply has a different syntax and each element of the matrix is a list
tapres <- tapply(penguins$body_mass_g, list(penguins$species, penguins$sex),
       mean_sd1)
tapres
```

    #>           female    male
    #> Adelie    numeric,2 numeric,2
    #> Chinstrap numeric,2 numeric,2
    #> Gentoo    numeric,2 numeric,2

```r
tapres[1,1]
```

    #> [[1]]
    #>    mean      sd
    #> 3368.84  269.38

## `dplyr`

```r
library(dplyr)
penguins |> group_by(species, sex) |>
  summarize(mean_sd1(body_mass_g))
```

    #> # A tibble: 16 x 3
    #> # Groups:   species, sex [8]
    #>    species   sex    `mean_sd1(body_mass_g)`
    #>    <fct>     <fct>                    <dbl>
    #>  1 Adelie    female                   3369.
    #>  2 Adelie    female                    269.
    #>  3 Adelie    male                     4043.
    #>  4 Adelie    male                      347.
    #>  5 Adelie    <NA>                     3540
    #>  6 Adelie    <NA>                      477.
    #>  7 Chinstrap female                   3527.
    #>  8 Chinstrap female                    285.
    #>  9 Chinstrap male                     3939.
    #> 10 Chinstrap male                      362.
    #> 11 Gentoo    female                   4680.
    #> 12 Gentoo    female                    282.
    #> 13 Gentoo    male                     5485.
    #> 14 Gentoo    male                      313.
    #> 15 Gentoo    <NA>                     4588.
    #> 16 Gentoo    <NA>                      338.

## `data.table`

```r
library(data.table)
pengdt <- data.table(penguins)

pengdt[, mean_sd1(body_mass_g), by = list(species, sex)]
```

    #>       species    sex      V1
    #>        <fctr> <fctr>   <num>
    #>  1:    Adelie   male 4043.49
    #>  2:    Adelie   male  346.81
    #>  3:    Adelie female 3368.84
    #>  4:    Adelie female  269.38
    #>  5:    Adelie   <NA> 3540.00
    #>  6:    Adelie   <NA>  477.17
    #>  7:    Gentoo female 4679.74
    #>  8:    Gentoo female  281.58
    #>  9:    Gentoo   male 5484.84
    #> 10:    Gentoo   male  313.16
    #> 11:    Gentoo   <NA> 4587.50
    #> 12:    Gentoo   <NA>  338.19
    #> 13: Chinstrap female 3527.21
    #> 14: Chinstrap female  285.33
    #> 15: Chinstrap   male 3938.97
    #> 16: Chinstrap   male  362.14

```r
## . can be used as shorthand for list in data table
pengdt[, mean_sd1(body_mass_g), by = .(species, sex)]
```

    #>       species    sex      V1
    #>        <fctr> <fctr>   <num>
    #>  1:    Adelie   male 4043.49
    #>  2:    Adelie   male  346.81
    #>  3:    Adelie female 3368.84
    #>  4:    Adelie female  269.38
    #>  5:    Adelie   <NA> 3540.00
    #>  6:    Adelie   <NA>  477.17
    #>  7:    Gentoo female 4679.74
    #>  8:    Gentoo female  281.58
    #>  9:    Gentoo   male 5484.84
    #> 10:    Gentoo   male  313.16
    #> 11:    Gentoo   <NA> 4587.50
    #> 12:    Gentoo   <NA>  338.19
    #> 13: Chinstrap female 3527.21
    #> 14: Chinstrap female  285.33
    #> 15: Chinstrap   male 3938.97
    #> 16: Chinstrap   male  362.14

## Classes and custom generics

1.  Modify your mean and sd function so that the data structure that is returned has class “meansd”. There are two ways to do this:
    1.  Say the object you currently return is called `res`, instead of `res`, return `structure(res, class = "meansd")`
    2.  Add the line `class(res) <- "meansd"` before returning \`res\`\`
    3.  Use the `attr` function to create and assign additional information, for example the name of the variable, You can get the name of the object passed to `x` using `deparse1(substitute(x))`.

```r
mean_sd2 <- function(x, na.rm = TRUE) {
  res <- c(mean = mean(x, na.rm = na.rm),
           sd = sd(x, na.rm = na.rm))

  attr(res, "variable") <- deparse1(substitute(x))
  attr(res, "sampsize") <- sum(!is.na(x))
  class(res) <- "meansd"
  res
}
```

2.  Write a custom print function `print.meansd` that nicely prints the mean and standard deviation. Use the functions `round` and `paste` functions to create a string, then print it out using the `cat` function.

```r
print.meansd <- function(x, digits = 2) {

  msd <- paste0(round(x["mean"], digits = digits), " (",
                round(x["sd"], digits = digits), ")")

  cat("mean (sd) of ",
      attr(x, "variable"), ":",
      msd, "\n")

}

mean_sd2(penguins$body_mass_g)
```

    #> mean (sd) of  penguins$body_mass_g : 4201.75 (801.95)

## More functions

1.  Write another function that constructs a one-sample t-statistic from an estimated mean and standard deviation. Recall that the t-statistic to test the null hypothesis that $\mu = \mu_0$ is $$
    T = \frac{\overline{X} - \mu_0}{\hat{\sigma}/\sqrt{n}}
    $$ where $\overline{X}$ is the sample mean and $\hat{\sigma}$ is the sample standard deviation and $n$ is the sample size.
2.  Write another function that takes the t-statistic and calculates a p-value
3.  Compose your custom functions in order to test the null hypothesis that the mean body mass of penguins is 4000g. Try using the pipe operator `|>`.

```r
t_stat <- function(x, mu_0 = 0) {
  ## x should be of class "meansd"
  stopifnot(inherits(x, "meansd"))

  Tstat <- unname((x["mean"] - mu_0) /
                    (x["sd"] / sqrt(attr(x, "sampsize"))))
  attr(Tstat, "df") <- attr(x, "sampsize") - 1
  Tstat

}

p_value <- function(x) {

  2 * pt(-abs(x), df = attr(x, "df"))

}

mean_sd2(penguins$body_mass_g) |> t_stat(mu_0 = 4000) |> p_value()
```

    #> [1] 4.6998e-06
    #> attr(,"df")
    #> [1] 341

## Solution script: functions.R

```r
library(palmerpenguins)
library(dplyr)
library(data.table)

mean_sd <- function(x, na.rm = TRUE) {
  
  xname <- deparse1(substitute(x))
  
  res <- c(mean = mean(x, na.rm = na.rm), 
    sd = sd(x, na.rm = na.rm))
  
  class(res) <- "meansd"
  attr(res, "variable") <- xname
  attr(res, "sampsize") <- length(x)
  
  res
  
}

print.meansd <- function(x, digits = 2) {
  
  cat(attr(x, "variable"), ": ",
    paste0(
    round(x["mean"], digits = digits), 
    " (", 
    round(x["sd"], digits = digits), 
    ")"))
  
}



msd_bm <- mean_sd(x = penguins$body_mass_g)

msd_bm
print(msd_bm, digits = 0)

mean_sd(penguins$bill_depth_mm)

ex1 <- c(mean= 1, sd = .5)
class(ex1) <- "meansd"






numeric_cols <- sapply(penguins, is.numeric)
apply(penguins[numeric_cols], MARGIN = 2, FUN = mean_sd)


baseapply <- split(penguins$body_mass_g, list(penguins$species, penguins$sex)) |>
  lapply(FUN = mean_sd) 

## question 2
## tidyverse

penguins |> group_by(species, sex) |>
  summarize(mean_sd(body_mass_g, na.rm = TRUE))

penguins |> group_by(species, sex) |>
  summarize(mean.bm = mean(body_mass_g, na.rm = TRUE), 
            sd.bm = sd(body_mass_g, na.rm = TRUE))


## data.table

pengdt <- data.table(penguins)

pengdt[, (mean_sd(body_mass_g)), 
       by = list(species, sex)]

pengdt[, .(mean.bm = mean(body_mass_g, na.rm = TRUE), 
           sd.bm = sd(body_mass_g, na.rm = TRUE)), 
       by = .(species, sex)]



mean_sd2 <- function(x, na.rm = TRUE) {
  
  xname <- deparse1(substitute(x))
  
  res <- data.frame(mean = mean(x, na.rm = na.rm), 
           sd = sd(x, na.rm = na.rm), 
           variable = xname)
  
  res
  
}


peng_summary <- pengdt[, (mean_sd2(body_mass_g)), 
       by = list(species, sex)]

dcast(peng_summary, species + variable ~ sex, 
      value.var = c("mean", "sd"))

penguins |> group_by(species, sex) |>
  summarize(mean_sd2(body_mass_g, na.rm = TRUE))



mean_sd3 <- function(x, na.rm = TRUE) {
  
  xname <- deparse1(substitute(x))
  
  res <- data.frame(stat_value = c(
    mean(x, na.rm = na.rm), 
    sd(x, na.rm = na.rm)), 
    stat_type = c("mean", "sd"), 
    variable = xname)
  
  res
  
}
pengdt[, (mean_sd3(body_mass_g)), 
       by = list(species, sex)]


penguins |> group_by(species, sex) |>
  summarize(mean_sd2(body_mass_g, na.rm = TRUE))
```
