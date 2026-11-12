# Functions

Lecture 6 | Day 2, B | Slides: <https://sachsmc.github.io/r-programming/lectures/functions.html>

# Using functions

## A function and its components

Almost everything you do in R involves functions. You call a function by typing its name with its arguments (inputs) inside the parentheses:

```r
sample(x = 1:5, size = 2)
```

    #> [1] 2 1

The function takes the arguments you provide, does something, and then returns an object. To see what a function does, you can type its name without parentheses to see the source:

```r
sample
```

    #> function (x, size, replace = FALSE, prob = NULL)
    #> {
    #>     if (length(x) == 1L && is.numeric(x) && is.finite(x) && x >=
    #>         1) {
    #>         if (missing(size))
    #>             size <- x
    #>         sample.int(x, size, replace, prob)
    #>     }
    #>     else {
    #>         if (missing(size))
    #>             size <- length(x)
    #>         x[sample.int(length(x), size, replace, prob)]
    #>     }
    #> }
    #> <bytecode: 0x000001eea53b2350>
    #> <environment: namespace:base>

The source shows you the arguments, their default values, and the expression defining the function. You can also look at the help file for the documentation:

```r
help("sample")
# or
?sample
```

## Using functions – arguments

Functions can have 0 or more arguments, with or without defaults.

The arguments can be given in order, or by name

```r
set.seed(100)
sample(1:5, 2, FALSE)
```

    #> [1] 2 3

```r
## same as
set.seed(100)
sample(size = 2, replace = FALSE, x = 1:5)
```

    #> [1] 2 3

Names can be partially matched, which can be confusing:

```r
set.seed(100)
sample(si = 2, re = FALSE, x = 1:5)
```

    #> [1] 2 3

## The ellipsis argument

Some functions take `...` as an argument, e.g., `paste`, `list`, also the `apply` family.

There are 2 reasons for this:

1.  There could be varying numbers of arguments

```r
c(1, 2, 3)
```

    #> [1] 1 2 3

```r
##
c(1, 2)
```

    #> [1] 1 2

2.  To pass optional arguments to other functions involved

```r
library(palmerpenguins)
with(penguins,
     by(body_mass_g, species, mean)
     )
```

    #> species: Adelie
    #> [1] NA
    #> ------------------------------------------------------------
    #> species: Chinstrap
    #> [1] 3733.1
    #> ------------------------------------------------------------
    #> species: Gentoo
    #> [1] NA

```r
## na.rm gets passed to "mean"
with(penguins,
     by(body_mass_g, species, mean,
        na.rm = TRUE)
     )
```

    #> species: Adelie
    #> [1] 3700.7
    #> ------------------------------------------------------------
    #> species: Chinstrap
    #> [1] 3733.1
    #> ------------------------------------------------------------
    #> species: Gentoo
    #> [1] 5076

## Using functions – composition

Often we want to use the result of one function as the argument to another function. There are many ways to do this:

1.  Intermediate variables

```r
set.seed(100)
x <- rgamma(100, shape = 1, rate = 2)
logx <- log(x)
stdlogx <- scale(logx)
quantile(stdlogx, c(.25, .75))
```

    #>      25%      75%
    #> -0.34256  0.57462

2.  Nested function calls

```r
quantile(scale(log(x)), c(.25, .75))
```

    #>      25%      75%
    #> -0.34256  0.57462

3.  The pipe operator `|>` (available in R 4.0.1)

```r
x |> log() |> scale() |> quantile(c(.25, .75))
```

    #>      25%      75%
    #> -0.34256  0.57462

## Using functions – the apply family

Some functions will take other functions as arguments. An example is the `apply` family of functions, which applies a function over an index or iterator. See `help(apply)`

`apply` repeated applies a function over the dimensions of an array. `MARGIN` indicates which dimension, and then for each index in that dimension, it applies `FUN` to the sub-array

```r
M1 <- matrix(rnorm(1000), nrow = 100, ncol = 10)
colnames(M1) <- paste0("X", 1:10)
apply(M1, MARGIN = 2, FUN = median)
```

    #>        X1        X2        X3        X4        X5        X6        X7        X8
    #>  0.048747  0.013650  0.165528  0.172733 -0.148501  0.219452 -0.237232 -0.267033
    #>        X9       X10
    #> -0.073152  0.013362

## Apply continued

`tapply` is commonly used with data. It subsets the data `X` based on the `INDEX` argument, then applies a function to each subset:

```r
library(palmerpenguins)
tapply(X = penguins$bill_depth_mm, INDEX = penguins$species,
       FUN = mean)
```

    #>    Adelie Chinstrap    Gentoo
    #>        NA    18.421        NA

## `lapply`

`lapply` is more general, in that it can take any index and apply any function that takes the index as an argument. It always returns a list. `sapply` does the same, but simplifies the result to an array, if possible.

```r
lapply(split(penguins$bill_depth_mm, penguins$species),
       FUN = mean)
```

    #> $Adelie
    #> [1] NA
    #>
    #> $Chinstrap
    #> [1] 18.421
    #>
    #> $Gentoo
    #> [1] NA

```r
sapply(split(penguins$bill_depth_mm, penguins$species),
       FUN = mean)
```

    #>    Adelie Chinstrap    Gentoo
    #>        NA    18.421        NA

## `mapply`

This is the multivariate version of `sapply` that allows vector arguments.

```r
mapply(rep, times = 1:4, x = 4:1)
```

    #> [[1]]
    #> [1] 4
    #>
    #> [[2]]
    #> [1] 3 3
    #>
    #> [[3]]
    #> [1] 2 2 2
    #>
    #> [[4]]
    #> [1] 1 1 1 1

See also the `purrr` package

## Notes on speed and flexibility

The apply family of functions is computationally equivalent to a loop (with pre-allocation)

Using apply instead of a for loop will not be faster computationally

It may be faster to write, but it may also be harder to understand

You can do whatever you want inside a for loop, how would you do something more complex with `lapply`?

# Writing your own functions

## A simple function

```r
hello <- function() {

  "Hello"

}

hello()
```

    #> [1] "Hello"

## A function with arguments

```r
hello <- function(name) {

  paste("Hello", name)

}
hello("Jim")
```

    #> [1] "Hello Jim"

```r
lapply(c("Jim", "Heather", "Bob"), hello)
```

    #> [[1]]
    #> [1] "Hello Jim"
    #>
    #> [[2]]
    #> [1] "Hello Heather"
    #>
    #> [[3]]
    #> [1] "Hello Bob"

## Local variables and scoping

```r
hello <- function(name) {

  name2 <- "Mike"
  paste("Hello", name, "meet", name2)

}
hello("Jim")
```

    #> [1] "Hello Jim meet Mike"

```r
name2
```

    #> Error: object 'name2' not found

`name2` is a local variable. It exists only inside the function.

```r
name2 <- "Billie"
hello("Jim")
```

    #> [1] "Hello Jim meet Mike"

Modifying local variables outside the function has no effect. But be careful:

```r
hello2 <- function(name) {

  paste("Hello", name, "meet", name2)

}
hello2("Jim")
```

    #> [1] "Hello Jim meet Billie"

## Arguments passed by value

Likewise, arguments modified inside the function do not change the object outside the function.

```r
HELLO <- function(name) {

  name <- toupper(name)
  paste("HELLO", name)

}
name <- "mark"
HELLO(name)
```

    #> [1] "HELLO MARK"

```r
name
```

    #> [1] "mark"

## Lexical scoping

This is called *lexical scoping*: it defines how R looks for objects when they are referred to by name

If R sees a variable it needs to use inside a function, and it is not an argument or local variable, then it follows these rules to find the object with that name:

1.  Look in the environment where the function was defined.
2.  If not found, look in the parent environment of 1
3.  If not found continue going down into parents until there are no more.

Note the specification sees a variable *and needs to use it*. This is called *lazy evaluation*: R does not evaluate anything until it needs to use it

## Lexical scoping example

This can be used to your advantage, e.g.,

```r
least_squares_constructor <- function(dataY, dataX) {

  function(beta) {
    sum((dataY - (beta[1] + beta[2] * dataX))^2, na.rm  =TRUE)
  }

}

model_penguin <- least_squares_constructor(penguins$flipper_length_mm,
                                        penguins$body_mass_g)
model_penguin
```

    #> function (beta)
    #> {
    #>     sum((dataY - (beta[1] + beta[2] * dataX))^2, na.rm = TRUE)
    #> }
    #> <environment: 0x000001eea3c535f0>

```r
ls(environment(model_penguin))
```

    #> [1] "dataX" "dataY"

```r
optim(par = c(0,0), fn = model_penguin)
```

    #> $par
    #> [1] 136.749793   0.015273
    #>
    #> $value
    #> [1] 16250
    #>
    #> $counts
    #> function gradient
    #>      113       NA
    #>
    #> $convergence
    #> [1] 0
    #>
    #> $message
    #> NULL

## Lazy evaluation example

```r
h01 <- function(x) {

    "Hello world!"

}
h01()
```

    #> [1] "Hello world!"

```r
h01(stop("Error"))
```

    #> [1] "Hello world!"

One way to manually check for arguments is with `missing`:

```r
h02 <- function(x) {

    if(missing(x)) {
        return("Missing x!")
    }
    "Hello world!"

}

h02()
```

    #> [1] "Missing x!"

```r
h02(1)
```

    #> [1] "Hello world!"

## Using `match.arg`

Look at the help file for `t.test`, and specifically the `alternative` argument. It is a vector with 3 elements, but only one is used. Also, it can be partially matched, e.g.,

```r
t.test(1:10, y = c(7:20), alternative = "gr")
```

    #>
    #>  Welch Two Sample t-test
    #>
    #> data:  1:10 and c(7:20)
    #> t = -5.43, df = 22, p-value = 1
    #> alternative hypothesis: true difference in means is greater than 0
    #> 95 percent confidence interval:
    #>  -10.528     Inf
    #> sample estimates:
    #> mean of x mean of y
    #>       5.5      13.5

How does that work? Using `match.arg` inside the function:

```r
mysummary <- function(x, type = c("mean", "median")) {
  type <- match.arg(type)
  switch(type,
         mean = mean(x),
         median = median(x))
}

mysummary(c(1, 2, 5))
```

    #> [1] 2.6667

## Anonymous functions

Your own functions do not need to be saved and assigned names. If a function does not have a name it is `anonymous`, I use these often with the apply family:

```r
bootmeans <- sapply(1:1000, function(i) {

  sample(penguins$body_mass_g, replace = TRUE) |>
    mean(na.rm = TRUE)

})
summary(bootmeans)
```

    #>    Min. 1st Qu.  Median    Mean 3rd Qu.    Max.
    #>    4053    4176    4203    4204    4230    4327

Since R 4.0.1, `\()` can be used as shorthand for `function()`:

```r
bootmeans <- sapply(1:1000, \(i) {

   sample(penguins$body_mass_g, replace = TRUE) |>
    mean(na.rm = TRUE)

})
summary(bootmeans)
```

    #>    Min. 1st Qu.  Median    Mean 3rd Qu.    Max.
    #>    4080    4173    4201    4201    4228    4357

## Operators

Operators are symbols like `+`, `<-`, `%*%`, `[`.

These are functions! To treat them like functions instead of operators, use backticks:

```r
2 + 2
```

    #> [1] 4

```r
`+`(2, 2)
```

    #> [1] 4

You can then treat operators as you would any other function, using them in apply or otherwise

You can also define your own operators:

```r
`% %` <- function(a, b) {

    paste(a, b)

}

"my" % % "name"
```

    #> [1] "my name"

```r
"my" % % "name" % % "is" % % "Mike"
```

    #> [1] "my name is Mike"

Assignment operators have a special syntax:

```r
`second<-` <- function(x, value){

    x[2] <- value
    x

}

x <- 1:10
second(x) <- 11
x
```

    #>  [1]  1 11  3  4  5  6  7  8  9 10

## Generic methods/functions

Look at the function `print`

```r
print
```

    #> function (x, ...)
    #> UseMethod("print")
    #> <bytecode: 0x000001eea1293b98>
    #> <environment: namespace:base>

It is a *generic function*. `UseMethod` says depending on the *class* of argument `object`, R will call a suitable *method* (a function) that does something designed for whatever `object` is.

You can find all the special methods by running `methods("print")` (try it now).

The class of the object is a simple attribute and the method is defined by appending the class name after the function name separated by a dot. This is called the **S3 class system**:

```r
x <- 1:4
class(x)
```

    #> [1] "integer"

```r
class(x) <- "myclass"

inherits(x, "myclass")
```

    #> [1] TRUE

```r
print.myclass <- function(x, ...) {

  cat(x, sep = "\n")

}

x
```

    #> 1
    #> 2
    #> 3
    #> 4

## Summary

In R, everything that happens is due to a function, and everything that exists is an object. Functions themselves are objects.

How do functions work together? We can classify functions according to their inputs and outputs:

| Input/Output | Data             | Function          |
|--------------|------------------|-------------------|
| Data         | Regular function | Function factory  |
| Function     | Functional       | Function operator |

These concepts are loosely defined, because functions can take both data and function arguments and return data and function results.

## Designing functions

When should you write a function? How should it be designed?

1.  The DRY principle: don’t repeat yourself
2.  Consider the audience

- Don’t write a function unless you expect somebody to use it
- Consider the most likely use cases, and remember you can’t make everyone happy

3.  Balance ease-of-use with understandability

- Break down the task into a series of smaller tasks, and abstract them away into functions
- Reuse or build? Dependencies (using functions from other packages) may change in unpredictable ways
- Default arguments and error checking – you can’t prevent all errors, ultimately it is the users’ responsibility to use the tools correctly

## Documenting functions

The R help for functions must include a title, short description, arguments, return value, and examples (self-contained). Use this structure to document your functions:

```r
#' Construct a greeting
#'
#' Introduce someone to Mike
#'
#' @param name A character string of the person to be greeted
#'
#' @return A character string with the greeting
#' @examples
#' hello("Laura")
hello <- function(name) {
  name2 <- "Mike"
  paste("Hello", name, "meet", name2)
}
```

The is [roxygen2](https://roxygen2.r-lib.org/) format

Or if you are using quarto, use section headings and lists.

# Some more advanced topics

## `get` and `assign`

Recall that we can retrieve a variable from a data frame by using a character string, e.g., `penguins[["species"]]`.

We can use a character string to get or assign any other object using these functions. For example, this returns the function called mean

```r
get("mean")
```

    #> function (x, ...)
    #> UseMethod("mean")
    #> <bytecode: 0x000001eea2ab1d20>
    #> <environment: namespace:base>

which we can use like a function

```r
get("mean")(penguins$body_mass_g, na.rm = TRUE)
```

    #> [1] 4201.8

Likewise, an object can be created with `assign`

```r
assign("mean.body.mass", mean(penguins$body_mass_g, na.rm = TRUE))
mean.body.mass
```

    #> [1] 4201.8

## Uses of `get` and `assign`

Example, iterating over functions by name:

```r
summary_funcs <- c("mean", "sd", "median")
for(fn in summary_funcs) {
  cat(fn, "body mass: ")
  cat(get(fn)(penguins$body_mass_g, na.rm = TRUE), "\n")
}
```

    #> mean body mass: 4201.8
    #> sd body mass: 801.95
    #> median body mass: 4050

Example, retrieving a function programmatically,

```r
converter <- get(paste0("as.", class(penguins$flipper_length_mm)))
converter(mean(penguins$flipper_length_mm, na.rm = TRUE))
```

    #> [1] 200

Example, programmatically creating new variables,

```r
numeric_cols <- names(penguins)[sapply(penguins, is.numeric)]
for(col in numeric_cols){
  assign(paste0(col, ".scaled"),
         scale(penguins[[col]]))
}
```

## `do.call`

A variant on `get` is `do.call`. This takes a function as the first argument, then a list containing the arguments for the function, `do.call(<function>, <list of arguments to function>)`.

A common use for this is with functions that take a variable number of arguments, e.g., `cbind`, `paste`, where the arguments are created programmatically.

simple example,

```r
do.call("paste", list("A", "B", sep = "."))
```

    #> [1] "A.B"

arranging a list into a matrix

```r
mean.sd.by.species <- lapply(split(penguins$flipper_length_mm, penguins$species),
                             function(x) c(mean = mean(x, na.rm = TRUE), sd = sd(x, na.rm = TRUE)))
do.call("rbind", mean.sd.by.species)
```

    #>             mean     sd
    #> Adelie    189.95 6.5395
    #> Chinstrap 195.82 7.1319
    #> Gentoo    217.19 6.4850

## Global assigment operator

There is the `<<-` operator, which is used in functions and does (re)assignment **outside the function**. It searches the parent environments and reassigns where found, if not found it assigns in the global environment.

This is generally considered to be a bad idea, but now you know about it.

```r
name2 <- "Billie"
name2
```

    #> [1] "Billie"

```r
hello <- function(name) {

  name2 <<- "Mike"
  paste("Hello", name, "meet", name2)

}
hello("Jim")
```

    #> [1] "Hello Jim meet Mike"

```r
name2
```

    #> [1] "Mike"

## Recursive functions

Functions that call themselves are possible.

As with repeat loops, they need to have a *break condition*

```r
fibbo <- function(n) {

  if(n <= 2) {  ## exit condition
    1
  } else {
    n + fibbo(n - 1)
  }

}
```

These are actually useful when working with nested lists and directed acyclic graphs, for example.

## Practical

1.  Modify and write functions
2.  Use apply to iterate functions over data
3.  Write your own class and generic print function

[Link to lesson](../exercises/functions.html)

[Link home](../index.html)
