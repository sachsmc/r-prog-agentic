# Flow control and loops: exercises

Exercise set 4 | Day 2, A | Online version: <https://sachsmc.github.io/r-programming/exercises/flow-and-loops.html>

### Learning objectives

In this lesson you will

1.  Practice working with `if` and `else` statements for conditional execution
2.  Practice working with loops for repeated execution

## Simple loops and conditional statements

1.  Use a loop to print every number from 1 to 10
2.  Modify the loop to print every *even* number from 1 to 10 (hint: add an `if` statement and use `(i %% 2) == 0` to check whether `i` is divisible by 2).

## Loops for statistical analysis

Load the `palmerpenguins` dataset:

```r
library(palmerpenguins)
penguins
```

    #> # A tibble: 344 x 8
    #>    species island    bill_length_mm bill_depth_mm flipper_length_mm body_mass_g
    #>    <fct>   <fct>              <dbl>         <dbl>             <int>       <int>
    #>  1 Adelie  Torgersen           39.1          18.7               181        3750
    #>  2 Adelie  Torgersen           39.5          17.4               186        3800
    #>  3 Adelie  Torgersen           40.3          18                 195        3250
    #>  4 Adelie  Torgersen           NA            NA                  NA          NA
    #>  5 Adelie  Torgersen           36.7          19.3               193        3450
    #>  6 Adelie  Torgersen           39.3          20.6               190        3650
    #>  7 Adelie  Torgersen           38.9          17.8               181        3625
    #>  8 Adelie  Torgersen           39.2          19.6               195        4675
    #>  9 Adelie  Torgersen           34.1          18.1               193        3475
    #> 10 Adelie  Torgersen           42            20.2               190        4250
    #> # i 334 more rows
    #> # i 2 more variables: sex <fct>, year <int>

1.  Write a loop that calculates and prints out the mean for each numeric variable in the `penguins` dataset

<details>

<summary>

Hints
</summary>

- How do you determine if a variable is numeric? You can use the `is.numeric` function, which returns TRUE or FALSE
- Inside a loop, sometimes `R` does not print things to the console, so you need to wrap them in the `print` function, e.g., `print(mean(x))` inside the loop.

</details>

2.  Modify your loop in 1 so that it prints out the mean, standard deviation, median, and interquartile range for each numeric variable in `penguins`.

<details>

<summary>

Hints
</summary>

- Use a nested loop where one of the iterators is the name of a function. To retrieve a function by name, use the `get` function, e.g., `get("mean")` returns the mean function, which can then saved as an intermediate object and be used like any other function.

</details>

3.  Write a loop to compute 500 bootstrap replicates of the means of bill length, bill depth, and flipper length. Remember to pre-allocate a data structure to store the 500 times 3 values. Provide an estimate of the correlation of the sample means.

<details>

<summary>

Hints
</summary>

- To get a bootstrap sample of a vector, use the `sample` function with the argument `replace = TRUE`.
- You can store the replicates in a matrix with 500 rows and 3 columns. Refer to the [data structures lecture](../lectures/data-structures.html) for information about indexing matrices.

</details>

## Loops for numeric calculation

Loops are sometimes unavoidable if a calculation depends on the value at one or more of the previous iterations.

One way to compute the [Kaplan-Meier curve for right censored data](https://en.wikipedia.org/wiki/Kaplan%E2%80%93Meier_estimator) is to loop through the death times and accumulate the product of 1 minus the number of deaths at each time over the number at risk at that time. Complete the following code to compute the KM curve and compare to the result from the survival package.

```r
amldat <- survival::aml
library(survival)

deathtimes <- c(0, sort(unique(amldat$time[amldat$status == 1])))
surv <- c(1, numeric(length(deathtimes) - 1))

for(i in 2:length(deathtimes)) {

  ## n_i = number still at risk
  atrisk <- subset(amldat, time > deathtimes[i - 1])

  ## count the number of deaths at time ti, call it d_i

  ## then compute 1 - d_i / n_i and multiply it by the previous survival probability

}

## plot(surv ~ deathtimes)
## lines(survfit(Surv(time, status) ~ 1, data = amldat))
```

## **Optional**: Loops to do data manipulation

> [!IMPORTANT]
>
> This exercises uses some concepts from functional programming, which we have not covered yet. Try it if you have time, but if not you can return to this after the functions lecture.

You may notice that some of the variables have missing values. We would like to replace the missing values with the “typical” value that is observed.

1.  Write a loop that contains an `if` then `else` statement that goes through the variables in `penguins` and replaces missing values with the mean for numeric double variables, and the most frequent value for characters or factors.

<details>

<summary>

Hints
</summary>

- Use this function to calculate the mode in a way that returns the same data type.

```r
my_mode <- function(x) {

  converter <- get(paste0("as.", class(x)))
  tab <- table(x) |> sort(decreasing = TRUE)
  names(tab)[1] |> converter()

}
```

- Inside the loop you will need to check whether the variable is of type “double”. Do this using the `is.double` function, which returns a TRUE or FALSE.
- To assign a new value `m` to only the missing elements of a vector `x`, you can do the following `x[is.na(x)] <- m`. Refer to the [data structures lecture](../lectures/data-structures.html) for information about indexing vectors

</details>
