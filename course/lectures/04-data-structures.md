# Data structures in R

Lecture 4 | Day 1, B | Slides: <https://sachsmc.github.io/r-programming/lectures/data-structures.html>

## Overview

- R is a programming language, most often used to work with data
- I use the term ‘data’ loosely, can refer to
  - data to be analyzed
  - results from a data analysis
  - information used in an analysis (e.g., ICD diagnosis codes)
- Think carefully about organizing your data structures

> “Bad programmers worry about the code. Good programmers worry about data structures and their relationships.”

Linus Torvalds, creator of Linux

## Types of data

logical, numeric, character, factor, date, …

```r
TRUE
```

    #> [1] TRUE

```r
1.2
```

    #> [1] 1.2

```r
"hello"
```

    #> [1] "hello"

```r
factor("low", levels = c("low", "med", "high"))
```

    #> [1] low
    #> Levels: low med high

```r
as.Date("2022-05-11", format = "%Y-%m-%d")
```

    #> [1] "2022-05-11"

```r
NULL
```

    #> NULL

## Vectors

A one dimensional collection of data with the same type. Can be named or unnamed. Can be created in many ways:

```r
1:4
```

    #> [1] 1 2 3 4

```r
seq(1, 4, by = 1)
```

    #> [1] 1 2 3 4

```r
letters
```

    #>  [1] "a" "b" "c" "d" "e" "f" "g" "h" "i" "j" "k" "l" "m" "n" "o" "p" "q" "r" "s"
    #> [20] "t" "u" "v" "w" "x" "y" "z"

```r
rep(TRUE, times = 5)
```

    #> [1] TRUE TRUE TRUE TRUE TRUE

```r
x <- 1:4
names(x) <- c("a", "b", "c", "d")
x
```

    #> a b c d
    #> 1 2 3 4

## Missing and empty/null values

`NA` for missing, and note that this has a data type.

`NaN` for “not a number”, e.g., `0 / 0`

`NULL` is empty, and has 0 length

```r
c(NA, 1) ## different from the next line
```

    #> [1] NA  1

```r
c(NA, "a")
```

    #> [1] NA  "a"

```r
c(NULL, "a")
```

    #> [1] "a"

```r
list(NULL, NULL, 1:3)
```

    #> [[1]]
    #> NULL
    #>
    #> [[2]]
    #> NULL
    #>
    #> [[3]]
    #> [1] 1 2 3

## Indexing vectors

Subsequences of vectors are obtained with square brackets `[]`

Inside the square brackets goes the *index*, which can be itself a vector of numbers, logicals, or characters (if the vector is *named*)

```r
x <- 1:6
names(x) <- c("a", "b", "c", "d", "e", "f")
```

```r
x[c(1, 3, 5)]
```

    #> a c e
    #> 1 3 5

```r
x[-c(2, 4, 6)] # negative index only works for numeric
```

    #> a c e
    #> 1 3 5

```r
x[c(TRUE, FALSE, TRUE, FALSE, TRUE, FALSE)]
```

    #> a c e
    #> 1 3 5

```r
x[(x %% 2) == 1]  ## what does x %% 2 mean?
```

    #> a c e
    #> 1 3 5

```r
x[(x %% 2) != 0]
```

    #> a c e
    #> 1 3 5

```r
x[c("a", "c", "d")]
```

    #> a c d
    #> 1 3 4

## Lists

A *list* is a collection of things not required to be the same type. An element of a list can be any R object. Can also be named or not.

```r
list(1:4, letters[1:4], mean)
```

    #> [[1]]
    #> [1] 1 2 3 4
    #>
    #> [[2]]
    #> [1] "a" "b" "c" "d"
    #>
    #> [[3]]
    #> function (x, ...)
    #> UseMethod("mean")
    #> <bytecode: 0x000002007fb09d20>
    #> <environment: namespace:base>

```r
list(numbers = 1:4,
     letters = letters[1:4],
     mean = mean,
     list = list("a", 1, TRUE))
```

    #> $numbers
    #> [1] 1 2 3 4
    #>
    #> $letters
    #> [1] "a" "b" "c" "d"
    #>
    #> $mean
    #> function (x, ...)
    #> UseMethod("mean")
    #> <bytecode: 0x000002007fb09d20>
    #> <environment: namespace:base>
    #>
    #> $list
    #> $list[[1]]
    #> [1] "a"
    #>
    #> $list[[2]]
    #> [1] 1
    #>
    #> $list[[3]]
    #> [1] TRUE

```r
## an empty list
list()
```

    #> list()

```r
## a list of 3 placeholders
vector(mode = "list", length = 3)
```

    #> [[1]]
    #> NULL
    #>
    #> [[2]]
    #> NULL
    #>
    #> [[3]]
    #> NULL

## Indexing lists

A list can be indexed with square brackets `[]` or double-square brackets `[[]]`, but there is a difference!

```r
xl <- list(numbers = 1:4,
     letters = letters[1:4],
     mean = mean,
     list = list("a", 1, TRUE))
```

```r
xl[[1]] ## returns the first element of the list (vector in this case)
```

    #> [1] 1 2 3 4

```r
xl[1] ## returns a sublist
```

    #> $numbers
    #> [1] 1 2 3 4

```r
xl[-1]
```

    #> $letters
    #> [1] "a" "b" "c" "d"
    #>
    #> $mean
    #> function (x, ...)
    #> UseMethod("mean")
    #> <bytecode: 0x000002007fb09d20>
    #> <environment: namespace:base>
    #>
    #> $list
    #> $list[[1]]
    #> [1] "a"
    #>
    #> $list[[2]]
    #> [1] 1
    #>
    #> $list[[3]]
    #> [1] TRUE

```r
xl[1:2] ## works with vectors
```

    #> $numbers
    #> [1] 1 2 3 4
    #>
    #> $letters
    #> [1] "a" "b" "c" "d"

```r
xl[[1:2]] ## works but does something different
```

    #> [1] 2

```r
xl$numbers
```

    #> [1] 1 2 3 4

```r
xl[["numbers"]]
```

    #> [1] 1 2 3 4

## Concatenating lists

New elements can be added by name or number

```r
xl$LETTERS <- LETTERS[1:4]
xl[[length(xl) + 1]] <- LETTERS[1:5]
xl
```

    #> $numbers
    #> [1] 1 2 3 4
    #>
    #> $letters
    #> [1] "a" "b" "c" "d"
    #>
    #> $mean
    #> function (x, ...)
    #> UseMethod("mean")
    #> <bytecode: 0x000002007fb09d20>
    #> <environment: namespace:base>
    #>
    #> $list
    #> $list[[1]]
    #> [1] "a"
    #>
    #> $list[[2]]
    #> [1] 1
    #>
    #> $list[[3]]
    #> [1] TRUE
    #>
    #>
    #> $LETTERS
    #> [1] "A" "B" "C" "D"
    #>
    #> [[6]]
    #> [1] "A" "B" "C" "D" "E"

The `c` function concatenates new elements to the list

```r
c(xl, AB = list(LETTERS[1:2]))
```

    #> $numbers
    #> [1] 1 2 3 4
    #>
    #> $letters
    #> [1] "a" "b" "c" "d"
    #>
    #> $mean
    #> function (x, ...)
    #> UseMethod("mean")
    #> <bytecode: 0x000002007fb09d20>
    #> <environment: namespace:base>
    #>
    #> $list
    #> $list[[1]]
    #> [1] "a"
    #>
    #> $list[[2]]
    #> [1] 1
    #>
    #> $list[[3]]
    #> [1] TRUE
    #>
    #>
    #> $LETTERS
    #> [1] "A" "B" "C" "D"
    #>
    #> [[6]]
    #> [1] "A" "B" "C" "D" "E"
    #>
    #> $AB
    #> [1] "A" "B"

```r
c(xl, AB = LETTERS[1:2]) # careful!
```

    #> $numbers
    #> [1] 1 2 3 4
    #>
    #> $letters
    #> [1] "a" "b" "c" "d"
    #>
    #> $mean
    #> function (x, ...)
    #> UseMethod("mean")
    #> <bytecode: 0x000002007fb09d20>
    #> <environment: namespace:base>
    #>
    #> $list
    #> $list[[1]]
    #> [1] "a"
    #>
    #> $list[[2]]
    #> [1] 1
    #>
    #> $list[[3]]
    #> [1] TRUE
    #>
    #>
    #> $LETTERS
    #> [1] "A" "B" "C" "D"
    #>
    #> [[6]]
    #> [1] "A" "B" "C" "D" "E"
    #>
    #> $AB1
    #> [1] "A"
    #>
    #> $AB2
    #> [1] "B"

## Matrices

Just like in math, R matrices are like vectors that have 2 dimensions, and are indexed also by square brackets.

There are lots of matrix manipulation functions in base R

```r
M1 <- matrix(1:12, nrow = 3, ncol = 4)
M1
```

    #>      [,1] [,2] [,3] [,4]
    #> [1,]    1    4    7   10
    #> [2,]    2    5    8   11
    #> [3,]    3    6    9   12

```r
M2 <- matrix(1:12, nrow = 3, ncol = 4,
       dimnames = list(letters[1:3], LETTERS[1:4]))
M2
```

    #>   A B C  D
    #> a 1 4 7 10
    #> b 2 5 8 11
    #> c 3 6 9 12

```r
diag(M1)
```

    #> [1] 1 5 9

```r
lower.tri(M1)
```

    #>       [,1]  [,2]  [,3]  [,4]
    #> [1,] FALSE FALSE FALSE FALSE
    #> [2,]  TRUE FALSE FALSE FALSE
    #> [3,]  TRUE  TRUE FALSE FALSE

```r
row(M1)
```

    #>      [,1] [,2] [,3] [,4]
    #> [1,]    1    1    1    1
    #> [2,]    2    2    2    2
    #> [3,]    3    3    3    3

```r
col(M2)
```

    #>      [,1] [,2] [,3] [,4]
    #> [1,]    1    2    3    4
    #> [2,]    1    2    3    4
    #> [3,]    1    2    3    4

```r
diag(3) %*% M1
```

    #>      [,1] [,2] [,3] [,4]
    #> [1,]    1    4    7   10
    #> [2,]    2    5    8   11
    #> [3,]    3    6    9   12

## Indexing matrices

Using square brackets, we get a single value by using two numbers or names separated by a comma:

```r
M1[2, 3]
```

    #> [1] 8

```r
M2["b", "C"]
```

    #> [1] 8

A missing index means “everything”, so this returns a vector

```r
M1[2,]
```

    #> [1]  2  5  8 11

```r
## if you want the result to be a matrix (with 1 row)
M1[2, , drop = FALSE]
```

    #>      [,1] [,2] [,3] [,4]
    #> [1,]    2    5    8   11

Can also use a logical matrix or numeric as a single index

```r
M1[M1 < 7] ## but this returns a vector
```

    #> [1] 1 2 3 4 5 6

```r
M1[M1 < 7] <- 0 ## when used with assignment, the matrix is preserved
M1
```

    #>      [,1] [,2] [,3] [,4]
    #> [1,]    0    0    7   10
    #> [2,]    0    0    8   11
    #> [3,]    0    0    9   12

Index matrices are convenient but hard to understand

Before we used a single index for each dimension:

```r
M2[1, 3]
```

    #> [1] 7

```r
M2[2, 1]
```

    #> [1] 2

```r
M2[3, 4]
```

    #> [1] 12

If we create a series of paired single indices, and store them in a matrix with 2 columns, we can use that matrix as an index:

```r
imat <- rbind(c(1, 3),
              c(2, 1),
              c(3, 4))
imat
```

    #>      [,1] [,2]
    #> [1,]    1    3
    #> [2,]    2    1
    #> [3,]    3    4

```r
M2[imat]
```

    #> [1]  7  2 12

```r
M2[imat] <- NA
M2
```

    #>    A B  C  D
    #> a  1 4 NA 10
    #> b NA 5  8 11
    #> c  3 6  9 NA

## Matrix arithmetic

Matrix transpose, multiplication, inversion, eigenvalues, etc, are all available in R

```r
S1 <- matrix(runif(9), nrow = 3, ncol = 3)
S2 <- matrix(runif(9), nrow = 3, ncol = 3)
x <- c(1, 1.5, 3)

S1 %*% S2
```

    #>         [,1]    [,2]    [,3]
    #> [1,] 0.25278 0.21704 0.29072
    #> [2,] 0.89492 0.69500 1.14636
    #> [3,] 0.54008 0.57679 0.99417

```r
t(S1) %*% S2
```

    #>         [,1]    [,2]    [,3]
    #> [1,] 1.57289 1.04164 0.93338
    #> [2,] 0.58171 0.30170 0.33579
    #> [3,] 0.53096 0.39336 0.39793

```r
x %*% solve(S1) %*% x
```

    #>        [,1]
    #> [1,] 11.986

## Arrays

Arrays are like matrices, but with more dimensions. A matrix is an array with 2 dimensions. Arrays can have more than 2 dimensions.

The data gets filled in by the first dimension, then the second, then the third, …

```r
A1 <- array(1:32, dim = c(4, 4, 2))
A1
```

    #> , , 1
    #>
    #>      [,1] [,2] [,3] [,4]
    #> [1,]    1    5    9   13
    #> [2,]    2    6   10   14
    #> [3,]    3    7   11   15
    #> [4,]    4    8   12   16
    #>
    #> , , 2
    #>
    #>      [,1] [,2] [,3] [,4]
    #> [1,]   17   21   25   29
    #> [2,]   18   22   26   30
    #> [3,]   19   23   27   31
    #> [4,]   20   24   28   32

The data also get “unrolled” in the same way.

```r
c(A1)
```

    #>  [1]  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25
    #> [26] 26 27 28 29 30 31 32

Indexing works like it does with matrices:

```r
A1[2, 4, 2] # value
```

    #> [1] 30

```r
A1[2, 4, ] # vector
```

    #> [1] 14 30

```r
A1[, , 2] # matrix
```

    #>      [,1] [,2] [,3] [,4]
    #> [1,]   17   21   25   29
    #> [2,]   18   22   26   30
    #> [3,]   19   23   27   31
    #> [4,]   20   24   28   32

```r
A1[, , 2, drop = FALSE] ## still an array
```

    #> , , 1
    #>
    #>      [,1] [,2] [,3] [,4]
    #> [1,]   17   21   25   29
    #> [2,]   18   22   26   30
    #> [3,]   19   23   27   31
    #> [4,]   20   24   28   32

```r
i3 <- rbind(c(2, 4, 2),
            c(2, 4, 1),
            c(3, 2, 1))

A1[i3]
```

    #> [1] 30 14  7

## Data frames

Data frames look like matrices, but the columns can be different data types:

```r
d1 <- data.frame(logical = c(FALSE, TRUE, FALSE),
                 numeric = c(1, 2, 3),
                 char = c("a", "b", "c"))
d1
```

    #>   logical numeric char
    #> 1   FALSE       1    a
    #> 2    TRUE       2    b
    #> 3   FALSE       3    c

```r
d1[, "char"]
```

    #> [1] "a" "b" "c"

```r
d1[, "numeric"]
```

    #> [1] 1 2 3

While they look like matrices, they act more like lists:

```r
d1$numeric
```

    #> [1] 1 2 3

```r
d1[["char"]]
```

    #> [1] "a" "b" "c"

```r
d1[[1]]
```

    #> [1] FALSE  TRUE FALSE

```r
names(d1)
```

    #> [1] "logical" "numeric" "char"

```r
d1$missing <- c(NA, NA, NA)
d1
```

    #>   logical numeric char missing
    #> 1   FALSE       1    a      NA
    #> 2    TRUE       2    b      NA
    #> 3   FALSE       3    c      NA

## Indexing and manipulating data frames

Multiple ways to refer to a particular column:

```r
d1$numeric
```

    #> [1] 1 2 3

```r
d1[["numeric"]]
```

    #> [1] 1 2 3

```r
d1[, "numeric"]
```

    #> [1] 1 2 3

```r
d1[, 2]
```

    #> [1] 1 2 3

```r
d1[[2]]
```

    #> [1] 1 2 3

Subsetting

```r
subset(d1, logical == TRUE) ## knows where to find logical
```

    #>   logical numeric char missing
    #> 2    TRUE       2    b      NA

```r
d1[d1$numeric <= 2, ] ## need to tell it that numeric is in d1
```

    #>   logical numeric char missing
    #> 1   FALSE       1    a      NA
    #> 2    TRUE       2    b      NA

Manipulation

```r
d1$numeric.squared <- d1$numeric^2
d1
```

    #>   logical numeric char missing numeric.squared
    #> 1   FALSE       1    a      NA               1
    #> 2    TRUE       2    b      NA               4
    #> 3   FALSE       3    c      NA               9

```r
d1 <- within(d1, {
  numeric.cubed <- numeric^3
  not.logical <- !logical
})
d1
```

    #>   logical numeric char missing numeric.squared not.logical numeric.cubed
    #> 1   FALSE       1    a      NA               1        TRUE             1
    #> 2    TRUE       2    b      NA               4       FALSE             8
    #> 3   FALSE       3    c      NA               9        TRUE            27

```r
with(d1, {

  sqrt(numeric)

})
```

    #> [1] 1.0000 1.4142 1.7321

Careful with attach if you know about it.

```r
attach(d1) ## this is like a global with/within
### many texts recommend not using attach

numeric
```

    #> [1] 1 2 3

```r
!logical
```

    #> [1]  TRUE FALSE  TRUE

```r
numeric.squared
```

    #> [1] 1 4 9

```r
og.num <- sqrt(numeric.squared) ## this does not work like within

detach(d1)
og.num ## still here
```

    #> [1] 1 2 3

```r
numeric.squared ## not attached anymore
```

    #> Error: object 'numeric.squared' not found

# Two important data gotchas

## Coercion

Coercion is what happens when data gets converted from one type to another (e.g., numeric to character).

This can also be done explicitly using the `as.` family of functions.

One of R’s “nice” features is that it will **automatically attempt to coerce data** when different types meet in an operation.

Examples

```r
c(FALSE, TRUE, FALSE) * 1.0
```

    #> [1] 0 1 0

```r
1 - c(FALSE, TRUE)
```

    #> [1] 1 0

```r
as.logical(1 - c(FALSE, TRUE))
```

    #> [1]  TRUE FALSE

```r
paste("A", 1:4, sep = "_")
```

    #> [1] "A_1" "A_2" "A_3" "A_4"

This is useful sometimes, other times it can cause problems:

```r
as.numeric(c("1.35", "2.5", "<.01"))
```

    #> [1] 1.35 2.50   NA

Hopefully R warns you if data is destroyed due to coercion.

If the data type is critical for an operation then it is up to you to check using the `is.` family of functions.

## Recycling

Vector and array arithmetic works elementwise, as long as the things have the same dimension.

If not, the shorter one is sometimes *recycled* to match the larger dimension thing

```r
c(1, 2) * c(1:6)
```

    #> [1]  1  4  3  8  5 12

```r
c(1, 2) * c(1:5)
```

    #> [1] 1 4 3 8 5

I often make this mistake when calculating proportions from a table:

```r
t1 <- table(mtcars$cyl, mtcars$gear)
t1
```

    #>
    #>      3  4  5
    #>   4  1  8  2
    #>   6  2  4  1
    #>   8 12  0  2

```r
## I want column proportions
t1 / colSums(t1)  ## this is wrong because of recycling rowwise
```

    #>
    #>            3        4        5
    #>   4 0.066667 0.533333 0.133333
    #>   6 0.166667 0.333333 0.083333
    #>   8 2.400000 0.000000 0.400000

```r
## create matrix of the same dimensions
t1 / rbind(colSums(t1), colSums(t1), colSums(t1))
```

    #>
    #>            3        4        5
    #>   4 0.066667 0.666667 0.400000
    #>   6 0.133333 0.333333 0.200000
    #>   8 0.800000 0.000000 0.400000

```r
## or use a built-in function
proportions(t1, margin = 2)
```

    #>
    #>            3        4        5
    #>   4 0.066667 0.666667 0.400000
    #>   6 0.133333 0.333333 0.200000
    #>   8 0.800000 0.000000 0.400000

Again, hopefully R warns you about this, but when in doubt check and validate lengths.

# Special data structures

## Attributes

Any object can have attributes, which are data that get attached to the object. It is a flexible way to include information with an object.

They are stored as names and value as in a list. Query or replace them with `attributes` or `attr`

```r
attributes(A1)
```

    #> $dim
    #> [1] 4 4 2

```r
attr(A1, "dim")
```

    #> [1] 4 4 2

```r
attr(A1, "note") <- "This is a new attribute"

A1
```

    #> , , 1
    #>
    #>      [,1] [,2] [,3] [,4]
    #> [1,]    1    5    9   13
    #> [2,]    2    6   10   14
    #> [3,]    3    7   11   15
    #> [4,]    4    8   12   16
    #>
    #> , , 2
    #>
    #>      [,1] [,2] [,3] [,4]
    #> [1,]   17   21   25   29
    #> [2,]   18   22   26   30
    #> [3,]   19   23   27   31
    #> [4,]   20   24   28   32
    #>
    #> attr(,"note")
    #> [1] "This is a new attribute"

Some attributes are special, e.g., `class`, `comment`, `dim`, `dimnames`, …, and have special ways of querying and setting

```r
comment(A1) <- paste("I created this array on ", Sys.time())
A1
```

    #> , , 1
    #>
    #>      [,1] [,2] [,3] [,4]
    #> [1,]    1    5    9   13
    #> [2,]    2    6   10   14
    #> [3,]    3    7   11   15
    #> [4,]    4    8   12   16
    #>
    #> , , 2
    #>
    #>      [,1] [,2] [,3] [,4]
    #> [1,]   17   21   25   29
    #> [2,]   18   22   26   30
    #> [3,]   19   23   27   31
    #> [4,]   20   24   28   32
    #>
    #> attr(,"note")
    #> [1] "This is a new attribute"

```r
comment(A1)
```

    #> [1] "I created this array on  2026-11-12 09:22:12.145197"

## Environments – how does R find things?

An environment is kind of like a list, it contains a number of arbitrary objects.

The *global environment* is a special one, look at the upper right pane of Rstudio, or run

```r
## all of the objects in the global environment
ls()
```

    #>  [1] "A1"              "M1"              "M2"              "S1"
    #>  [5] "S2"              "d1"              "i3"              "imat"
    #>  [9] "og.num"          "pandoc_dir"      "quarto_bin_path" "t1"
    #> [13] "x"               "xl"

When you type a name in the console, it will first look for it in the global environment. If it cannot find it there, it will then look in the attached packages.

We will come back to environments when we talk about functions.

## Packages

Add on packages can be installed from a few different places, CRAN, Bioconductor, github, R-forge, and locally from package files.

They are installed to your system with `install.packages("pkgname")`

When you use `library("pkgname")`, the package is *attached*, so that objects in the package can be found just by typing the name:

```r
library(palmerpenguins)
head(penguins)
```

    #> # A tibble: 6 x 8
    #>   species island    bill_length_mm bill_depth_mm flipper_length_mm body_mass_g
    #>   <fct>   <fct>              <dbl>         <dbl>             <int>       <int>
    #> 1 Adelie  Torgersen           39.1          18.7               181        3750
    #> 2 Adelie  Torgersen           39.5          17.4               186        3800
    #> 3 Adelie  Torgersen           40.3          18                 195        3250
    #> 4 Adelie  Torgersen           NA            NA                  NA          NA
    #> 5 Adelie  Torgersen           36.7          19.3               193        3450
    #> 6 Adelie  Torgersen           39.3          20.6               190        3650
    #> # i 2 more variables: sex <fct>, year <int>

You can use objects from packages without attaching them with `::` (two colons)

```r
head(survival::aml)
```

    #>   time status          x
    #> 1    9      1 Maintained
    #> 2   13      1 Maintained
    #> 3   13      0 Maintained
    #> 4   18      1 Maintained
    #> 5   23      1 Maintained
    #> 6   28      0 Maintained

and you can get internal objects from a package with `:::` (three colons)

```r
library(survival)
plot.aareg ## error
```

    #> Error: object 'plot.aareg' not found

```r
head(survival:::plot.aareg) ## finds it
```

    #>
    #> 1 function (x, se = TRUE, maxtime, type = "s", ...)
    #> 2 {
    #> 3     if (!inherits(x, "aareg"))
    #> 4         stop("Must be an aareg object")
    #> 5     if (missing(maxtime))
    #> 6         keep <- 1:length(x$time)

## S4 objects

Some packages you may use (e.g., from Bioconductor) return *S4 objects*. These are kind of like lists, but to access objects (called ‘slots’) inside, use `@` (the at symbol).

For example

```r
## A simple class with two slots
track <- setClass("track", slots = c(x="numeric", y="numeric"))
## an object from the class
ts1 <- track(x = 1:10, y = 1:10 + rnorm(10))
ts1
```

    #> An object of class "track"
    #> Slot "x":
    #>  [1]  1  2  3  4  5  6  7  8  9 10
    #>
    #> Slot "y":
    #>  [1]  0.99348  1.06068  2.48869  3.43941  4.13535  5.22588  6.18689  7.93458
    #>  [9]  9.96068 12.72302

```r
ts1@x
```

    #>  [1]  1  2  3  4  5  6  7  8  9 10

## Tibbles

Tibbles (cute name for ‘table’) are data frames with enhanced printing.

```r
library(tibble)
library(palmerpenguins)
class(penguins) ## this will be data.frame in the browser, but tbl_df in R
```

    #> [1] "tbl_df"     "tbl"        "data.frame"

```r
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

You can convert a regular data.frame to a tibble

```r
library(tibble)
mttbl <- as_tibble(mtcars)
mttbl
```

    #> # A tibble: 32 x 11
    #>      mpg   cyl  disp    hp  drat    wt  qsec    vs    am  gear  carb
    #>    <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl>
    #>  1  21       6  160    110  3.9   2.62  16.5     0     1     4     4
    #>  2  21       6  160    110  3.9   2.88  17.0     0     1     4     4
    #>  3  22.8     4  108     93  3.85  2.32  18.6     1     1     4     1
    #>  4  21.4     6  258    110  3.08  3.22  19.4     1     0     3     1
    #>  5  18.7     8  360    175  3.15  3.44  17.0     0     0     3     2
    #>  6  18.1     6  225    105  2.76  3.46  20.2     1     0     3     1
    #>  7  14.3     8  360    245  3.21  3.57  15.8     0     0     3     4
    #>  8  24.4     4  147.    62  3.69  3.19  20       1     0     4     2
    #>  9  22.8     4  141.    95  3.92  3.15  22.9     1     0     4     2
    #> 10  19.2     6  168.   123  3.92  3.44  18.3     1     0     4     4
    #> # i 22 more rows

The indexing behavior is slightly different from data frames:

```r
mttbl[, "mpg"] ## still a tibble
```

    #> # A tibble: 32 x 1
    #>      mpg
    #>    <dbl>
    #>  1  21
    #>  2  21
    #>  3  22.8
    #>  4  21.4
    #>  5  18.7
    #>  6  18.1
    #>  7  14.3
    #>  8  24.4
    #>  9  22.8
    #> 10  19.2
    #> # i 22 more rows

```r
mtcars[, "mpg"]
```

    #>  [1] 21.0 21.0 22.8 21.4 18.7 18.1 14.3 24.4 22.8 19.2 17.8 16.4 17.3 15.2 10.4
    #> [16] 10.4 14.7 32.4 30.4 33.9 21.5 15.5 15.2 13.3 19.2 27.3 26.0 30.4 15.8 19.7
    #> [31] 15.0 21.4

```r
mttbl[["mpg"]] ## gives a vector
```

    #>  [1] 21.0 21.0 22.8 21.4 18.7 18.1 14.3 24.4 22.8 19.2 17.8 16.4 17.3 15.2 10.4
    #> [16] 10.4 14.7 32.4 30.4 33.9 21.5 15.5 15.2 13.3 19.2 27.3 26.0 30.4 15.8 19.7
    #> [31] 15.0 21.4

```r
mttbl$mpg ## same as data.frame
```

    #>  [1] 21.0 21.0 22.8 21.4 18.7 18.1 14.3 24.4 22.8 19.2 17.8 16.4 17.3 15.2 10.4
    #> [16] 10.4 14.7 32.4 30.4 33.9 21.5 15.5 15.2 13.3 19.2 27.3 26.0 30.4 15.8 19.7
    #> [31] 15.0 21.4

## data.tables

`data.table` is a package that provides another data.frame extension.

It has many features for data manipulation and management with a focus on **speed**, both typing and computer speed for large datasets.

There is a special syntax for indexing and merging using square brackets, we will come back to this (because it is my favorite tool for data management)

```r
library(data.table)

mtdt <- data.table(mtcars)
class(mtdt)
```

    #> [1] "data.table" "data.frame"

```r
head(mtdt)
```

    #>      mpg   cyl  disp    hp  drat    wt  qsec    vs    am  gear  carb
    #>    <num> <num> <num> <num> <num> <num> <num> <num> <num> <num> <num>
    #> 1:  21.0     6   160   110  3.90 2.620 16.46     0     1     4     4
    #> 2:  21.0     6   160   110  3.90 2.875 17.02     0     1     4     4
    #> 3:  22.8     4   108    93  3.85 2.320 18.61     1     1     4     1
    #> 4:  21.4     6   258   110  3.08 3.215 19.44     1     0     3     1
    #> 5:  18.7     8   360   175  3.15 3.440 17.02     0     0     3     2
    #> 6:  18.1     6   225   105  2.76 3.460 20.22     1     0     3     1

```r
setkey(mtdt, "mpg")
head(mtdt)
```

    #> Key: <mpg>
    #>      mpg   cyl  disp    hp  drat    wt  qsec    vs    am  gear  carb
    #>    <num> <num> <num> <num> <num> <num> <num> <num> <num> <num> <num>
    #> 1:  10.4     8   472   205  2.93 5.250 17.98     0     0     3     4
    #> 2:  10.4     8   460   215  3.00 5.424 17.82     0     0     3     4
    #> 3:  13.3     8   350   245  3.73 3.840 15.41     0     0     3     4
    #> 4:  14.3     8   360   245  3.21 3.570 15.84     0     0     3     4
    #> 5:  14.7     8   440   230  3.23 5.345 17.42     0     0     3     4
    #> 6:  15.0     8   301   335  3.54 3.570 14.60     0     1     5     8

```r
mtdt[, .(meanwt = mean(wt)), by = .(cyl)]
```

    #>      cyl meanwt
    #>    <num>  <num>
    #> 1:     8 3.9992
    #> 2:     6 3.1171
    #> 3:     4 2.2857

# Data import and export

## Reading in external data

The basic functions are `read.table, read.csv, read.csv2`

Via add on packages, R supports import of any data format I can think of.

The most flexible way to read in data is with the `rio` package. It guesses what the format is and uses the correct import tool (most of the time)

```r
library(rio)
library(here)
df <- import(here("data/starwars.xlsx"))
head(df)
```

    #>             Name homeworld species
    #> 1 Luke Skywalker  Tatooine   Human
    #> 2          C-3PO  Tatooine   Human
    #> 3          R2-D2  Alderaan   Human
    #> 4    Darth Vader  Tatooine   Human
    #> 5    Leia Organa  Tatooine   Human
    #> 6      Owen Lars  Tatooine   Human

## Big datasets

The slowness of reading in data usually comes from format guessing.

Supplying known column types can dramatically speed up import:

```r
df1 <- read.csv(here("data/starwars.csv"))

df1b <- read.csv(here("data/starwars.csv"),
                colClasses = c("character", "factor", "factor",
                               "numeric"))
```

`fread` from the data.table package is fast and also flexible:

```r
library(data.table)
fread(here("data/starwars.csv"))
```

    #>                   Name homeworld species   age
    #>                 <char>    <char>  <char> <int>
    #>  1:     Luke Skywalker  Tatooine   Human    27
    #>  2:              C-3PO  Tatooine   Human    12
    #>  3:              R2-D2  Alderaan   Human     8
    #>  4:        Darth Vader  Tatooine   Human    44
    #>  5:        Leia Organa  Tatooine   Human    25
    #>  6:          Owen Lars  Tatooine   Human    32
    #>  7: Beru Whitesun lars   Stewjon   Human    38
    #>  8:              R5-D4  Tatooine   Human     7
    #>  9:  Biggs Darklighter  Kashyyyk Wookiee    65
    #> 10:     Obi-Wan Kenobi  Corellia   Human    68

## Exporting data

Most import functions have their output counterparts, e.g., `write.table, write.csv, write.csv2, fwrite`. These are useful for writing out rectangular data for use in other programs.

Another under-used way of exporting objects is to use `saveRDS`, this saves any R object to a file, which then gives you exactly the same object when read into R using `readRDS`. I use this frequently for intermediate datasets, analysis results stored in a list, and even functions.

Example

```r
lmfit <- lm(mpg ~ wt, data = mtcars)
lmfit
```

    #>
    #> Call:
    #> lm(formula = mpg ~ wt, data = mtcars)
    #>
    #> Coefficients:
    #> (Intercept)           wt
    #>       37.29        -5.34

```r
saveRDS(lmfit, file = "reg-ex.rds")

readRDS("reg-ex.rds")
```

    #>
    #> Call:
    #> lm(formula = mpg ~ wt, data = mtcars)
    #>
    #> Coefficients:
    #> (Intercept)           wt
    #>       37.29        -5.34

## Practical

1.  Practice working with vectors and matrices
2.  Thing about ways to organize data and output into data structures
3.  Compare and contrast the base R, `data.table`, and `tibble` packages for working with data.

[Link to lesson](../exercises/data-structures.html)

[Link home](../index.html)
