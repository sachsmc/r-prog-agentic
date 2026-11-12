# Flow control and loops: exercise solutions

Solutions for exercise set 4 | Day 2, A | Online version: <https://sachsmc.github.io/r-programming/exercises/solutions/flow-and-loops.html>

## Simple loops and conditional statements

1.  Use a loop to print every number from 1 to 10
2.  Modify the loop to print every *even* number from 1 to 10 (hint: add an `if` statement and use `(i %% 2) == 0` to check whether `i` is divisible by 2).

```r
## 1.
for(i in 1:10){
  print(i)
}
```

    #> [1] 1
    #> [1] 2
    #> [1] 3
    #> [1] 4
    #> [1] 5
    #> [1] 6
    #> [1] 7
    #> [1] 8
    #> [1] 9
    #> [1] 10

```r
## 2. The %% operator is the modulo function.
##    i %% 2 attempts to divide i by 2, with
##    whole numbers only and returns the remainder.
for(i in 1:10){
  if((i %% 2) == 0) {
  print(i)
  }
}
```

    #> [1] 2
    #> [1] 4
    #> [1] 6
    #> [1] 8
    #> [1] 10

## Loops for statistical analysis

```r
library(palmerpenguins)
```

1.  Write a loop that calculates and prints out the mean for each numeric variable in the `penguins` dataset

```r
for(i in 1:ncol(penguins)) {
  ## cat prints to the console without quotes
  cat(names(penguins)[i], " - ", sep = "")
  vari <- penguins[[i]] ## this iterates through the columns of penguins
  if(is.numeric(vari)) { ## check whether it is numeric
    cat("Mean:", mean(vari, na.rm = TRUE))
  } else {
    cat("not numeric")
  }
  cat("\n") # new line
}
```

    #> species - not numeric
    #> island - not numeric
    #> bill_length_mm - Mean: 43.922
    #> bill_depth_mm - Mean: 17.151
    #> flipper_length_mm - Mean: 200.92
    #> body_mass_g - Mean: 4201.8
    #> sex - not numeric
    #> year - Mean: 2008

2.  Modify your loop in 1 so that it prints out the mean, standard deviation, median, and interquartile range for each numeric variable in `penguins`.

```r
f.names <- c("mean", "std dev", "median", "interquartile range")
functions <- list(mean, sd, median, IQR)
## we will add an inner loop that iterates through these function and names

for(i in 1:ncol(penguins)) {
  cat(names(penguins)[i], ":\n", sep = "")
  vari <- penguins[[i]]

  if(is.numeric(vari)) {
    for(fn in 1:length(f.names)) {
      cat(f.names[fn], functions[[fn]](vari, na.rm = TRUE), "\n")
    }
  } else {
    cat("not numeric\n")
  }
  cat("--------\n") # new line
}
```

    #> species:
    #> not numeric
    #> --------
    #> island:
    #> not numeric
    #> --------
    #> bill_length_mm:
    #> mean 43.922
    #> std dev 5.4596
    #> median 44.45
    #> interquartile range 9.275
    #> --------
    #> bill_depth_mm:
    #> mean 17.151
    #> std dev 1.9748
    #> median 17.3
    #> interquartile range 3.1
    #> --------
    #> flipper_length_mm:
    #> mean 200.92
    #> std dev 14.062
    #> median 197
    #> interquartile range 23
    #> --------
    #> body_mass_g:
    #> mean 4201.8
    #> std dev 801.95
    #> median 4050
    #> interquartile range 1200
    #> --------
    #> sex:
    #> not numeric
    #> --------
    #> year:
    #> mean 2008
    #> std dev 0.81836
    #> median 2008
    #> interquartile range 2
    #> --------

3.  Write a loop to compute 500 bootstrap replicates of the means of bill length, bill depth, and flipper length. Remember to pre-allocate a data structure to store the 500 times 3 values. Provide an estimate of the correlation of the sample means.

```r
bootmeans <- matrix(NA, nrow = 500, ncol = 3,
                    dimnames = list(NULL, c("bill_length", "bill_depth", "flipper_length")))
for(i in 1:nrow(bootmeans)){
  bootindex <- sample(1:nrow(penguins), replace = TRUE)
  peng.star <- penguins[bootindex, ]

  bootmeans[i, 1] <- mean(peng.star$bill_length_mm, na.rm = TRUE)
  bootmeans[i, 2] <- mean(peng.star$bill_depth_mm, na.rm = TRUE)
  bootmeans[i, 3] <- mean(peng.star$flipper_length_mm, na.rm = TRUE)
}

summary(bootmeans)
```

    #>   bill_length     bill_depth   flipper_length
    #>  Min.   :43.0   Min.   :16.9   Min.   :199
    #>  1st Qu.:43.7   1st Qu.:17.1   1st Qu.:200
    #>  Median :43.9   Median :17.2   Median :201
    #>  Mean   :43.9   Mean   :17.2   Mean   :201
    #>  3rd Qu.:44.1   3rd Qu.:17.2   3rd Qu.:201
    #>  Max.   :44.8   Max.   :17.5   Max.   :204

```r
cor(bootmeans)
```

    #>                bill_length bill_depth flipper_length
    #> bill_length        1.00000   -0.22223        0.66049
    #> bill_depth        -0.22223    1.00000       -0.58793
    #> flipper_length     0.66049   -0.58793        1.00000

## Loops for numeric calculation

Loops are sometimes unavoidable if a calculation depends on the value at one or more of the previous iterations.

One way to compute the [Kaplan-Meier curve for right censored data](https://en.wikipedia.org/wiki/Kaplan%E2%80%93Meier_estimator) is to loop through the death times and accumulate the product of 1 minus the number of deaths at each time over the number at risk at that time. Complete the following code to compute the KM curve and compare to the result from the survival package.

```r
amldat <- survival::aml
library(survival)

deathtimes <- c(0, sort(unique(amldat$time[amldat$status == 1])))
surv <- c(1, numeric(length(deathtimes) - 1))

for(i in 2:length(deathtimes)) {

  atrisk <- subset(amldat, time > deathtimes[i - 1])

  deaths_at_ti <- sum(atrisk$status[atrisk$time == deathtimes[i]] == 1)

  surv[i] <- surv[i - 1] * (1 - (deaths_at_ti /
                                     nrow(atrisk)))

}

plot(surv ~ deathtimes)
lines(survfit(Surv(time, status) ~ 1, data = amldat))
```

[figure: plot produced by the code above]

## Loops to do data manipulation

1.  Write a loop that contains an `if` then `else` statement that goes through the variables in `penguins` and replaces missing values with the mean for numeric double variables, and the most frequent value for characters or factors.

```r
my_mode <- function(x) {

  converter <- get(paste0("as.", class(x)))
  tab <- table(x) |> sort(decreasing = TRUE)
  names(tab)[1] |> converter()

}

for(colnum in 1:ncol(penguins)){

  thiscol <- penguins[[colnum]]
  if(is.double(thiscol)) {

    thismean <- mean(thiscol, na.rm = TRUE)
    penguins[is.na(thiscol), colnum] <- thismean

  } else {

    penguins[is.na(thiscol), colnum] <- my_mode(thiscol)

  }
}

summary(penguins)
```

    #>       species          island    bill_length_mm bill_depth_mm
    #>  Adelie   :152   Biscoe   :168   Min.   :32.1   Min.   :13.1
    #>  Chinstrap: 68   Dream    :124   1st Qu.:39.3   1st Qu.:15.6
    #>  Gentoo   :124   Torgersen: 52   Median :44.2   Median :17.3
    #>                                  Mean   :43.9   Mean   :17.2
    #>                                  3rd Qu.:48.5   3rd Qu.:18.7
    #>                                  Max.   :59.6   Max.   :21.5
    #>  flipper_length_mm  body_mass_g       sex           year
    #>  Min.   :172       Min.   :2700   female:165   Min.   :2007
    #>  1st Qu.:190       1st Qu.:3550   male  :179   1st Qu.:2007
    #>  Median :197       Median :4025                Median :2008
    #>  Mean   :201       Mean   :4199                Mean   :2008
    #>  3rd Qu.:213       3rd Qu.:4750                3rd Qu.:2009
    #>  Max.   :231       Max.   :6300                Max.   :2009

## Solution script: loops.R

```r
even10 <- c(FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, 
            FALSE, TRUE, FALSE, TRUE)

for(i in 1:10){
  if(i %in% c(2, 4, 6, 8, 10)) {
  print(i)
  }
}

library(palmerpenguins)


for(colnum in 1:8){
  
  thiscol <- penguins[[colnum]]
  if(is.double(thiscol)) {
    
    thismean <- mean(thiscol, na.rm = TRUE)
    penguins[is.na(thiscol), colnum] <- thismean
    
  } else if(is.integer(thiscol)) {
    
    tabbedvals <- sort(table(thiscol), decreasing = TRUE)
    penguins[is.na(thiscol), colnum] <- as.integer(names(tabbedvals)[1])
    
  } else if(is.factor(thiscol)){
    
    tabbedvals <- sort(table(thiscol), decreasing = TRUE)
    penguins[is.na(thiscol), colnum] <- as.factor(names(tabbedvals)[1])
    
  } 
    
}

summary(penguins)
```
