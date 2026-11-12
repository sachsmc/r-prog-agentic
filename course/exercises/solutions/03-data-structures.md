# Data structures: exercise solutions

Solutions for exercise set 3 | Day 1, B | Online version: <https://sachsmc.github.io/r-programming/exercises/solutions/data-structures.html>

## Vectors and matrices

1.  Take the sum of each row of `M1`
2.  Create a new matrix called `M2` that is `M1` with the diagonal elements replaced by 0s
3.  Create a new matrix called `M3` that is `M1` but with all values less than 4 replaced by -1
4.  Append the three matrices into an array with dimensions 4, 4, 3.

```r
M1 <- matrix(1:16, nrow = 4, ncol = 4)

## 1.
rowSums(M1)
```

    #> [1] 28 32 36 40

```r
# or the matrix arithmetic way
M1 %*% matrix(1, nrow = nrow(M1), ncol = 1)
```

    #>      [,1]
    #> [1,]   28
    #> [2,]   32
    #> [3,]   36
    #> [4,]   40

```r
## 2.
M2 <- M1
diag(M2) <- 0

## 3.
M3 <- M1
M3[M3 < 4] <- -1

## 4.
A1 <- array(NA, dim = c(4, 4, 3))
A1[,,1] <- M1
A1[,,2] <- M2
A1[,,3] <- M3
```

## Organizing output from a statistical analysis

```r
library(palmerpenguins)

by(penguins$body_mass_g, list(penguins$sex, penguins$species), summary)
```

    #> : female
    #> : Adelie
    #>    Min. 1st Qu.  Median    Mean 3rd Qu.    Max.
    #>    2850    3175    3400    3369    3550    3900
    #> ------------------------------------------------------------
    #> : male
    #> : Adelie
    #>    Min. 1st Qu.  Median    Mean 3rd Qu.    Max.
    #>    3325    3800    4000    4044    4300    4775
    #> ------------------------------------------------------------
    #> : female
    #> : Chinstrap
    #>    Min. 1st Qu.  Median    Mean 3rd Qu.    Max.
    #>    2700    3362    3550    3527    3694    4150
    #> ------------------------------------------------------------
    #> : male
    #> : Chinstrap
    #>    Min. 1st Qu.  Median    Mean 3rd Qu.    Max.
    #>    3250    3731    3950    3939    4100    4800
    #> ------------------------------------------------------------
    #> : female
    #> : Gentoo
    #>    Min. 1st Qu.  Median    Mean 3rd Qu.    Max.
    #>    3950    4462    4700    4680    4875    5200
    #> ------------------------------------------------------------
    #> : male
    #> : Gentoo
    #>    Min. 1st Qu.  Median    Mean 3rd Qu.    Max.
    #>    4750    5300    5500    5485    5700    6300

```r
massfit <- lm(body_mass_g ~ sex * species, data = penguins)
summary(massfit)
```

    #>
    #> Call:
    #> lm(formula = body_mass_g ~ sex * species, data = penguins)
    #>
    #> Residuals:
    #>    Min     1Q Median     3Q    Max
    #>   -827   -214     11    206    861
    #>
    #> Coefficients:
    #>                          Estimate Std. Error t value Pr(>|t|)
    #> (Intercept)                3368.8       36.2   93.03   <2e-16 ***
    #> sexmale                     674.7       51.2   13.17   <2e-16 ***
    #> speciesChinstrap            158.4       64.2    2.47   0.0142 *
    #> speciesGentoo              1310.9       54.4   24.09   <2e-16 ***
    #> sexmale:speciesChinstrap   -262.9       90.8   -2.89   0.0041 **
    #> sexmale:speciesGentoo       130.4       76.4    1.71   0.0889 .
    #> ---
    #> Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    #>
    #> Residual standard error: 309 on 327 degrees of freedom
    #>   (11 observations deleted due to missingness)
    #> Multiple R-squared:  0.855,  Adjusted R-squared:  0.852
    #> F-statistic:  384 on 5 and 327 DF,  p-value: <2e-16

```r
boxplot(body_mass_g ~ sex * species, data = penguins,
        col = rep(c("slateblue", "salmon"), 3))
legend("topleft", fill = c("slateblue", "salmon"),
       legend = c("Female", "Male"))
```

[figure: plot produced by the code above]

Inspect the `massfit` object. What type of data structure is it, and what does it contain?

> It is a list with class “lm”. It contains lots of information about the model fit.

You are planning a publication about the association/interaction between species and sex on body mass. The paper will include descriptive statistics, statistical inference, and some figures. You will likely present the results at a conference or in a lab meeting.

1.  What are some different approaches to save the results?
2.  Discuss the pros and cons of your suggested approaches.

> One approach would be to save is to save the regression fit as an rds file and read it into different R markdown documents to use it for different purposes. Also the figures could be saved as pngs and used in different documents. An alternative is to save the analysis dataset as a file, and the code used to reproduce the analysis, including the figures. The advantage of the 2nd approach is that the output can be tailored to the specific use of the results (e.g., change figure size/resolution for presentation vs manuscript).
