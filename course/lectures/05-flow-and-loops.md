# Flow control and loops

Lecture 5 | Day 2, A | Slides: <https://sachsmc.github.io/r-programming/lectures/flow-and-loops.html>

# Flow control

## What?

- Normally the code gets run line by line, in order, top to bottom

- There are special commands that allow you change that

- *Conditional execution*, choose which code to run depending on logical conditions

  - `if(<condition>)`
  - `else if`
  - `else`

- *Loops*, repeat a chunk of code several times

  - `repeat`
  - `for`
  - `while`

## If then else

```r
if(<condition>) {

  <do something>

} else {

  <do something else>

}
```

If the `<condition>` evaluates to `TRUE`, then `something` gets executed, otherwise `something else` gets executed.

`<condition>` must be length one. No vectors allowed.

## Examples

```r
num_reps <- if(TRUE) 5000 else 200
num_reps
```

    #> [1] 5000

This is more useful when the condition inside the `if` is a result of some other computation

## Examples

```r
nonparametric <- median(mtcars$mpg) > (mean(mtcars$mpg) * sd(mtcars$mpg) / 2)

p_value <- if(nonparametric) {
  wilcox.test(mpg ~ vs, data = mtcars, exact = FALSE)$p.value
} else {
  t.test(mpg ~ vs, data = mtcars)$p.value
}
```

## Examples

There does not need to be anything returned from the expression, it could just modify data, make a figure, etc.

```r
if(log_transform) {

  data$Y <- log(data$Y)

}
```

## Many `if else`

There is no limit to the amount of `if else` statements. This is equivalent to having if statements repeatedly nested.

```r
letter <- "three"
number <- if(letter == "one") {
  1
} else if(letter == "two") {
  2
} else if(letter == "three") {
  3
} else {
  stop("Number not found!")
}
number
```

    #> [1] 3

## Related functions

- `switch`: evaluates its first argument, and chooses one of the subsequent arguments by name (unnamed the “default”)

```r
switch(letter, one = 1, two = 2, three = 3, stop("Number not found!"))
```

    #> [1] 3

- `cut`: Divides a numeric vector into intervals and produces a factor.

```r
(x1 <- rnorm(5))
```

    #> [1] -0.75503  2.11958  0.61405 -0.89105 -0.25565

```r
cut(x1, breaks = c(-Inf, -1, 0, 1, Inf),
    labels = c("<-1", "-1 to 0", "0 to 1", "> 1"))
```

    #> [1] -1 to 0 > 1     0 to 1  -1 to 0 -1 to 0
    #> Levels: <-1 -1 to 0 0 to 1 > 1

## Logical operators

`&` (logical AND) and `|` (OR) have scalar counterparts, called “short-circuit” operators

- `&&` and `||` evaluate the first argument, and then the second one **only if necessary**.

```r
FALSE && stop("Error")
```

    #> [1] FALSE

```r
TRUE || stop("Error")
```

    #> [1] TRUE

Common use case:

```r
p.value <- exp(log(runif(1, -.1, .1)))
p.value <- p.value[!is.na(p.value)]
p.char <- if(length(p.value) > 0 && p.value[[1]] < .05) {"<0.05"} else NULL
p.char
```

    #> [1] "<0.05"

## Other logical operators

- `xor` Exclusive OR
- `isTRUE` and `isFALSE`
- `any` and `all` for converting logical vectors to a single value, also have `na.rm` option

```r
any(c(FALSE, TRUE, FALSE))
```

    #> [1] TRUE

```r
all(c(FALSE, TRUE))
```

    #> [1] FALSE

## Exception handling

aka, how to not stop evaluation on an error. R has 3 types of exceptions: 1) Errors, 2) Warnings, 3) Messages. Errors stop the flow of execution, all three say something at the console.

Warnings and Messages can be suppressed by wrapping the expressions in `suppress(Warhings|Messages)`

`tryCatch` evaluates an expression and does something with the error that you decide.

```r
tryCatch({           # block of expressions to execute, until an error occurs
        cat("a...\n")
        stop("b!")    # error – breaks the linear control flow
        cat("c?\n")
    },
    error = function(e) {  # executed immediately on an error
        cat(sprintf("[error] %s\n", e[["message"]]))
    },
    finally = {  # always executed at the end, regardless of error occurrence
        cat("d.\n")
    }
)
```

    #> a...
    #> [error] b!
    #> d.

## `ifelse`

This is a function, not a statement like `if` and `else`.

It is vectorized and hence better suited for working with data.

`ifelse(<logical vector>, <yes vector>, <no vector>)`. All three vectors should be the same length or recycling happens.

It returns a vector with elements from `yes` when TRUE, and elements from `no` when FALSE.

```r
rawdata <- c("12.63", "62.45", "<2") ## lower limit of detection
as.numeric(ifelse(rawdata == "<2", 1, rawdata))
```

    #> [1] 12.63 62.45  1.00

# Loops

## Basic concepts

A loop repeatedly and sequentially evaluates an expression, i.e.,

```r
{
  <stuff contained inside curly brackets>
}
```

A loop will continue forever unless you tell it to stop. You tell it to stop in different ways for different loop expressions

## Repeat

This is the simplest of loops, it will repeat an expression until it encounters `break`

This will run forever

```r
repeat {
  print("hello")
}
```

This will run exactly once

```r
repeat {
  print("hello")
  break
}
```

    #> [1] "hello"

Modify the above to run 5 times

<details>

```r
i <- 1
repeat {
  print("hello")
  if(i == 5) break
  i <- i + 1
}
```

</details>

## While

Notice the pattern, repeat an expression until a condition is met.

The condition usually depends on a variable that changes at each iteration, in this case `i`, the *iterator*

`while` loops explicitly state the condition at the start:

```r
i <- 1
while(i <= 5) {
  print("hello")
  i <- i + 1
}
```

    #> [1] "hello"
    #> [1] "hello"
    #> [1] "hello"
    #> [1] "hello"
    #> [1] "hello"

## For loops

A `for` loop explicitly states the sequence of the iterator at the start. Then the “end condition” is that the loop has reached the end of the sequence.

```r
for(i in 1:5) {
  print("hello")
}
```

    #> [1] "hello"
    #> [1] "hello"
    #> [1] "hello"
    #> [1] "hello"
    #> [1] "hello"

In this case, it is the most concise. I personally use `for` loops more than any other loop.

`break` can be used inside any loop to end it. `next` can be used to go to the next iteration.

```r
for(i in 1:5) {
  if(i == 2) next
  print(paste("hello", i))
}
```

    #> [1] "hello 1"
    #> [1] "hello 3"
    #> [1] "hello 4"
    #> [1] "hello 5"

## Example - Iterating through species

```r
library(palmerpenguins)

species_names <- levels(penguins$species)
mean_bill_length <- numeric(length(species_names))
names(mean_bill_length) <- species_names

for(i in species_names){  ## iterator is a character

  mean_bill_length[i] <- ## indexing by name
    mean(subset(penguins, species == i)$bill_length_mm, na.rm = TRUE)

}

mean_bill_length
```

    #>    Adelie Chinstrap    Gentoo
    #>    38.791    48.834    47.505

## Bootstrap

```r
mu.body_mass <- mean(penguins$body_mass_g, na.rm = TRUE)
bsmeans <- vector("numeric", length = 200)
for(i in 1:length(bsmeans)) {
  resampled.body_mass <- sample(penguins$body_mass_g, replace = TRUE)
  bsmeans[i] <- mean(resampled.body_mass, na.rm = TRUE)
}
hist(bsmeans)
abline(v = mu.body_mass, col = "red")
```

[figure: plot produced by the code above]

## Nested loops

A loop can itself contain a loop, or multiple loops.

```r
species_names <- levels(penguins$species)
island_names <- levels(penguins$island)
mean_bm_matrix <- matrix(NA, nrow = length(species_names),
                         ncol = length(island_names),
                         dimnames = list(species_names, island_names))

for(i in species_names) {
  for(j in island_names) {

    thisset <- subset(penguins, species == i &
                        island == j)

    if(nrow(thisset) == 0) next

    mean_bm_matrix[i, j] <- mean(thisset$body_mass_g, na.rm = TRUE)

  }
}
mean_bm_matrix
```

    #>           Biscoe  Dream Torgersen
    #> Adelie    3709.7 3688.4    3706.4
    #> Chinstrap     NA 3733.1        NA
    #> Gentoo    5076.0     NA        NA

## Note on speed

You may see people warn you not to use for loops in R, “because they are slow”.

That is partially true, but speed is not the only thing, for loops can be much clearer and more understandable than the alternatives.

**But**, the slow thing in R is changing the size of an object, so you can avoid that by creating a vector/matrix/array of the correct size to hold the results of the loop:

```r
system.time({
A1 <- NULL
for(i in 1:100000) {
  A1 <- c(A1, rnorm(1))
}
})
```

    #>    user  system elapsed
    #>   16.75    6.18   23.29

```r
system.time({
A2 <- numeric(100000)
for(i in 1:length(A2)) {
  A2[i] <- rnorm(1)
}
})
```

    #>    user  system elapsed
    #>    0.19    0.02    0.20

## Practical

1.  Practice working if and else statements
2.  Practice working with loops

[Link to lesson](../exercises/flow-and-loops.html)

[Link home](../index.html)
