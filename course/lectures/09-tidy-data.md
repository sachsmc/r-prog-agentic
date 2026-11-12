# Tidy data

Lecture 9 | Day 3, C | Slides: <https://sachsmc.github.io/r-programming/lectures/tidy-data.html>

# Illustration

## Our `mean_sd` function

```r
library(palmerpenguins)
library(dplyr)

mean_sd <- function(x, na.rm = TRUE) {
  c(mean = mean(x, na.rm = na.rm),
    sd = sd(x, na.rm = na.rm))
}

penguins |> group_by(species, sex) |>
  summarize(mean_sd(body_mass_g))
```

    #> # A tibble: 16 x 3
    #> # Groups:   species, sex [8]
    #>    species   sex    `mean_sd(body_mass_g)`
    #>    <fct>     <fct>                   <dbl>
    #>  1 Adelie    female                  3369.
    #>  2 Adelie    female                   269.
    #>  3 Adelie    male                    4043.
    #>  4 Adelie    male                     347.
    #>  5 Adelie    <NA>                    3540
    #>  6 Adelie    <NA>                     477.
    #>  7 Chinstrap female                  3527.
    #>  8 Chinstrap female                   285.
    #>  9 Chinstrap male                    3939.
    #> 10 Chinstrap male                     362.
    #> 11 Gentoo    female                  4680.
    #> 12 Gentoo    female                   282.
    #> 13 Gentoo    male                    5485.
    #> 14 Gentoo    male                     313.
    #> 15 Gentoo    <NA>                    4588.
    #> 16 Gentoo    <NA>                     338.

This is not so nice to work with because we cannot see which row is the mean and which is the sd.

## Alternative 1

Return a data frame instead

```r
mean_sd_df <- function(x, na.rm = TRUE) {
  data.frame(
    variable = deparse1(substitute(x)),
    mean = mean(x, na.rm = na.rm),
    sd = sd(x, na.rm = na.rm))
}

penguins |> group_by(species, sex) |>
  summarize(mean_sd_df(body_mass_g))
```

    #> # A tibble: 8 x 5
    #> # Groups:   species [3]
    #>   species   sex    variable     mean    sd
    #>   <fct>     <fct>  <chr>       <dbl> <dbl>
    #> 1 Adelie    female body_mass_g 3369.  269.
    #> 2 Adelie    male   body_mass_g 4043.  347.
    #> 3 Adelie    <NA>   body_mass_g 3540   477.
    #> 4 Chinstrap female body_mass_g 3527.  285.
    #> 5 Chinstrap male   body_mass_g 3939.  362.
    #> 6 Gentoo    female body_mass_g 4680.  282.
    #> 7 Gentoo    male   body_mass_g 5485.  313.
    #> 8 Gentoo    <NA>   body_mass_g 4588.  338.

## Alternative 2

```r
mean_sd_ldf <- function(x, na.rm = TRUE) {
  data.frame(
    variable = deparse1(substitute(x)),
    stat = c("mean", "sd"),
    value = c(mean(x, na.rm = na.rm),
             sd(x, na.rm = na.rm)))
}

penguins |> group_by(species, sex) |>
  summarize(mean_sd_ldf(body_mass_g))
```

    #> # A tibble: 16 x 5
    #> # Groups:   species, sex [8]
    #>    species   sex    variable    stat  value
    #>    <fct>     <fct>  <chr>       <chr> <dbl>
    #>  1 Adelie    female body_mass_g mean  3369.
    #>  2 Adelie    female body_mass_g sd     269.
    #>  3 Adelie    male   body_mass_g mean  4043.
    #>  4 Adelie    male   body_mass_g sd     347.
    #>  5 Adelie    <NA>   body_mass_g mean  3540
    #>  6 Adelie    <NA>   body_mass_g sd     477.
    #>  7 Chinstrap female body_mass_g mean  3527.
    #>  8 Chinstrap female body_mass_g sd     285.
    #>  9 Chinstrap male   body_mass_g mean  3939.
    #> 10 Chinstrap male   body_mass_g sd     362.
    #> 11 Gentoo    female body_mass_g mean  4680.
    #> 12 Gentoo    female body_mass_g sd     282.
    #> 13 Gentoo    male   body_mass_g mean  5485.
    #> 14 Gentoo    male   body_mass_g sd     313.
    #> 15 Gentoo    <NA>   body_mass_g mean  4588.
    #> 16 Gentoo    <NA>   body_mass_g sd     338.

# Definitions

## Tidy data

These are two different ways to represent the same data. This is to illustrate the concept of *tidy data*

Tidy data is a standard way of mapping the meaning of a dataset to its structure. A dataset is messy or tidy depending on how rows, columns and tables are matched up with observations, variables and types. In tidy data:

1.  Each variable forms a column.
2.  Each observation forms a row.
3.  Each type of observational unit forms a table.

Wickham, H. (2014). Tidy Data. *Journal of Statistical Software*, 59(10), 1–23. https://doi.org/10.18637/jss.v059.i10

## Variables and observations

In general,

- It is easier to describe and create functional relationships between variables (columns), than between observations.
  - Think of our mean, sd example. Relationship between mean and sd?
  - Regression
- It is easier to make comparisons between groups of observations than across variables
  - T-tests, anova, compare means across species

# In practice

## Making statistical output tidy

If you are writing the function that does the calculations, you are in control.

Tips and tricks:

- Assemble things in a data frame, the columns you group by will appear on their own.
- `deparse1(substitute(x))` creates a character string from the name of the object used as the argument `x`

## The `broom` package

```r
library(broom)
```

Broom provides a `tidy` function, which is a generic, it can be applied to lots of different objects:

```r
methods("tidy")
```

    #>   [1] tidy.Arima*                    tidy.Gam*
    #>   [3] tidy.Kendall*                  tidy.Line*
    #>   [5] tidy.Lines*                    tidy.Mclust*
    #>   [7] tidy.NULL*                     tidy.Polygon*
    #>   [9] tidy.Polygons*                 tidy.Sarlm*
    #>  [11] tidy.SpatialLinesDataFrame*    tidy.SpatialPolygons*
    #>  [13] tidy.SpatialPolygonsDataFrame* tidy.TukeyHSD*
    #>  [15] tidy.aareg*                    tidy.acf*
    #>  [17] tidy.anova*                    tidy.aov*
    #>  [19] tidy.aovlist*                  tidy.betamfx*
    #>  [21] tidy.betareg*                  tidy.biglm*
    #>  [23] tidy.binDesign*                tidy.binWidth*
    #>  [25] tidy.boot*                     tidy.btergm*
    #>  [27] tidy.cch*                      tidy.character*
    #>  [29] tidy.cld*                      tidy.clm*
    #>  [31] tidy.clmm*                     tidy.coeftest*
    #>  [33] tidy.confint.glht*             tidy.confusionMatrix*
    #>  [35] tidy.coxph*                    tidy.crr*
    #>  [37] tidy.cv.glmnet*                tidy.data.frame*
    #>  [39] tidy.default*                  tidy.density*
    #>  [41] tidy.dist*                     tidy.drc*
    #>  [43] tidy.durbinWatsonTest*         tidy.emmGrid*
    #>  [45] tidy.epi.2by2*                 tidy.ergm*
    #>  [47] tidy.factanal*                 tidy.felm*
    #>  [49] tidy.fitdistr*                 tidy.fixest*
    #>  [51] tidy.ftable*                   tidy.gam*
    #>  [53] tidy.garch*                    tidy.geeglm*
    #>  [55] tidy.glht*                     tidy.glm*
    #>  [57] tidy.glmRob*                   tidy.glmnet*
    #>  [59] tidy.glmrob*                   tidy.gmm*
    #>  [61] tidy.htest*                    tidy.ivreg*
    #>  [63] tidy.kappa*                    tidy.kde*
    #>  [65] tidy.kmeans*                   tidy.lavaan*
    #>  [67] tidy.leveneTest*               tidy.list*
    #>  [69] tidy.lm*                       tidy.lm.beta*
    #>  [71] tidy.lmRob*                    tidy.lmodel2*
    #>  [73] tidy.lmrob*                    tidy.logical*
    #>  [75] tidy.logitmfx*                 tidy.lsmobj*
    #>  [77] tidy.manova*                   tidy.map*
    #>  [79] tidy.margins*                  tidy.mediate*
    #>  [81] tidy.mfx*                      tidy.mjoint*
    #>  [83] tidy.mle2*                     tidy.mlm*
    #>  [85] tidy.mlogit*                   tidy.muhaz*
    #>  [87] tidy.multinom*                 tidy.negbin*
    #>  [89] tidy.negbinmfx*                tidy.nlrq*
    #>  [91] tidy.nls*                      tidy.numeric*
    #>  [93] tidy.orcutt*                   tidy.pairwise.htest*
    #>  [95] tidy.pam*                      tidy.plm*
    #>  [97] tidy.poLCA*                    tidy.poissonmfx*
    #>  [99] tidy.polr*                     tidy.power.htest*
    #> [101] tidy.prcomp*                   tidy.probitmfx*
    #> [103] tidy.pyears*                   tidy.rcorr*
    #> [105] tidy.ref.grid*                 tidy.regsubsets*
    #> [107] tidy.ridgelm*                  tidy.rlm*
    #> [109] tidy.rma*                      tidy.roc*
    #> [111] tidy.rq*                       tidy.rqs*
    #> [113] tidy.sarlm*                    tidy.spec*
    #> [115] tidy.speedglm*                 tidy.speedlm*
    #> [117] tidy.summary.glht*             tidy.summary.lm*
    #> [119] tidy.summary.plm*              tidy.summaryDefault*
    #> [121] tidy.summary_emm*              tidy.survdiff*
    #> [123] tidy.survexp*                  tidy.survfit*
    #> [125] tidy.survreg*                  tidy.svyglm*
    #> [127] tidy.svyolr*                   tidy.systemfit*
    #> [129] tidy.table*                    tidy.tobit*
    #> [131] tidy.ts*                       tidy.varest*
    #> [133] tidy.zoo*
    #> see '?methods' for accessing help and source code

It attempts to do organize statistical output into a tidy tibble.

```r
lmfit <- lm(flipper_length_mm ~ body_mass_g + species + sex,
            data = penguins)
lmfit
```

    #>
    #> Call:
    #> lm(formula = flipper_length_mm ~ body_mass_g + species + sex,
    #>     data = penguins)
    #>
    #> Coefficients:
    #>      (Intercept)       body_mass_g  speciesChinstrap     speciesGentoo
    #>         1.65e+02          6.55e-03          5.54e+00          1.80e+01
    #>          sexmale
    #>         2.48e+00

```r
tidy(lmfit)
```

    #> # A tibble: 5 x 5
    #>   term              estimate std.error statistic   p.value
    #>   <chr>                <dbl>     <dbl>     <dbl>     <dbl>
    #> 1 (Intercept)      165.       3.18         51.7  1.01e-159
    #> 2 body_mass_g        0.00655  0.000931      7.04 1.15e- 11
    #> 3 speciesChinstrap   5.54     0.785         7.06 9.92e- 12
    #> 4 speciesGentoo     18.0      1.44         12.5  1.46e- 29
    #> 5 sexmale            2.48     0.854         2.90 3.97e-  3

## More functions from `broom`

`tidy` returns data about the model coefficients, what about the other components of the model?

- `tidy()` summarizes information about model components
- `glance()` reports information about the entire model
- `augment()` adds information about observations to a dataset

## Benefits of tidy statistical output

The main reason for being tidy is to help with subsequent analysis and reporting. `lmfit` prints the necessary results, but look at `tidy(lmfit)`.

- Easier to organize into a table or figure
- Easier to merge or append with results from different models
- Possibly easier to store/save the results

# Tidy data for analysis

## Messy data example

Real data is often messy, and we want that to be tidy as well for easier analysis. Example of messy data:

```r
library(tidyr)
billboard <- tribble(
  ~artist, ~wk1, ~wk2,
   "2 Pac",     1,     2,
   "Creed",     3,     4,
   "Mos Def",     5,     6,
  "Aaliyah", 2, NA
)
billboard
```

    #> # A tibble: 4 x 3
    #>   artist    wk1   wk2
    #>   <chr>   <dbl> <dbl>
    #> 1 2 Pac       1     2
    #> 2 Creed       3     4
    #> 3 Mos Def     5     6
    #> 4 Aaliyah     2    NA

- A variable is encoded in columns (week)
- This is also called “wide format”

## Pivoting data

Converting from wide to long (`tidyr` package):

```r
billboard |>
    pivot_longer(
    cols = starts_with("wk"),
    names_to = "week",
    values_to = "rank",
    values_drop_na = TRUE
  )
```

    #> # A tibble: 7 x 3
    #>   artist  week   rank
    #>   <chr>   <chr> <dbl>
    #> 1 2 Pac   wk1       1
    #> 2 2 Pac   wk2       2
    #> 3 Creed   wk1       3
    #> 4 Creed   wk2       4
    #> 5 Mos Def wk1       5
    #> 6 Mos Def wk2       6
    #> 7 Aaliyah wk1       2

Base R

```r
longbb <- as.data.frame(billboard) |>
  reshape(direction = "long",
          varying = colnames(billboard)[-c(1)],
          timevar = "week", sep = "",
          v.names = "rank",
          idvar = "artist")
subset(longbb, !is.na(rank))
```

    #>            artist week rank
    #> 2 Pac.1     2 Pac    1    1
    #> Creed.1     Creed    1    3
    #> Mos Def.1 Mos Def    1    5
    #> Aaliyah.1 Aaliyah    1    2
    #> 2 Pac.2     2 Pac    2    2
    #> Creed.2     Creed    2    4
    #> Mos Def.2 Mos Def    2    6

## Melting (data.table and old tidyverse)

```r
library(data.table)

data.table(billboard) |>
  melt(measure.vars = patterns("^wk"),
       variable.name = "week",
       value.name = "rank",
       na.rm = TRUE)
```

    #>     artist   week  rank
    #>     <char> <fctr> <num>
    #> 1:   2 Pac    wk1     1
    #> 2:   Creed    wk1     3
    #> 3: Mos Def    wk1     5
    #> 4: Aaliyah    wk1     2
    #> 5:   2 Pac    wk2     2
    #> 6:   Creed    wk2     4
    #> 7: Mos Def    wk2     6

This makes it easier to compute summary statistics, or make figures of ranks by artist.

Most longitudinal data analyses will expect data in “long” format.

## Pivoting from long to wide

This also has its uses. Examples include computing correlation matrices, doing derived variable analysis, and tables are often more readable in wide or partial wide format.

```r
dfw <- tribble(
  ~id, ~time, ~value,
  "A", 1, 8.6,
  "A", 3, 4.5,
  "B", 1, 1.01,
  "B", 2, 3.3,
  "C", 1, 4.1,
  "C", 2, 5.2,
  "C", 3, 3.2
)
```

`tidyr`

```r
dfw |> pivot_wider(names_from = "time",
                   names_prefix = "time",
                   values_from = "value")
```

    #> # A tibble: 3 x 4
    #>   id    time1 time3 time2
    #>   <chr> <dbl> <dbl> <dbl>
    #> 1 A      8.6    4.5  NA
    #> 2 B      1.01  NA     3.3
    #> 3 C      4.1    3.2   5.2

base R

```r
as.data.frame(dfw) |>
  reshape(direction = "wide",
          idvar = "id" ,
          timevar = "time"
          )
```

    #>   id value.1 value.3 value.2
    #> 1  A    8.60     4.5      NA
    #> 3  B    1.01      NA     3.3
    #> 5  C    4.10     3.2     5.2

`data.table`

```r
data.table(dfw) |>
  dcast(id ~ time, value.var = "value")
```

    #> Key: <id>
    #>        id     1     2     3
    #>    <char> <num> <num> <num>
    #> 1:      A  8.60    NA   4.5
    #> 2:      B  1.01   3.3    NA
    #> 3:      C  4.10   5.2   3.2

## Real data

Are often much more complex, and can be messier. Here is one example we will use in the lesson:

```r
library(here)
readRDS(here("data", "lpr-ex.rds")) |> head(12)
```

    #>     pid  age sex      indat visit hdia diag1 diag2 diag3 diag4 diag5 diag6
    #> 1  A001 72.5   f 2010-01-27     1 H560  B632  H180  J050  <NA>  <NA>  <NA>
    #> 2  A001 72.5   f 2010-06-26     2 C871  D422  K820  A602  <NA>  <NA>  <NA>
    #> 3  A001 72.5   f 2010-07-20     3 C040  B710  <NA>  <NA>  <NA>  <NA>  <NA>
    #> 4  A001 72.5   f 2011-03-06     4 F412  F381  F632  E832  <NA>  <NA>  <NA>
    #> 5  A001 72.5   f 2011-12-23     5 F622  J720  <NA>  <NA>  <NA>  <NA>  <NA>
    #> 6  A002 81.5   f 2005-09-02     1 B481  K512  F750  K059  <NA>  <NA>  <NA>
    #> 7  A002 81.5   f 2008-05-05     2 K959  G959  E252  <NA>  <NA>  <NA>  <NA>
    #> 8  A002 81.5   f 2012-07-05     3 G902  D939  K329  G402  <NA>  <NA>  <NA>
    #> 9  A003 54.5   m 2006-07-30     1 E841  A062  <NA>  <NA>  <NA>  <NA>  <NA>
    #> 10 A003 54.5   m 2007-04-09     2 E071  J602  J490  J839  <NA>  <NA>  <NA>
    #> 11 A003 54.5   m 2008-03-14     3 H189  B752  B190  C751  I610  <NA>  <NA>
    #> 12 A003 54.5   m 2010-08-24     4 B090  I992  D021  <NA>  <NA>  <NA>  <NA>

## Practical

We will practice creating tidy data continuing with our mean sd function, and using the register data example to practice pivoting and doing grouped analyses.

[Link to lesson](../exercises/tidy-and-reshape.html)

[Link home](../index.html)
