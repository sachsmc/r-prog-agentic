# Data visualization: exercise solutions

Solutions for exercise set 8 | Day 4, C | Online version: <https://sachsmc.github.io/r-programming/exercises/solutions/dataviz.html>

## Create your own theme

Load the `ggplot2` package and customize your own theme. Look at the built-in themes and the `ggthemes` package for inspiration.

### Tips

1.  You can save your customization using the `theme()`, but that will only modify the current theme

```r
library(ggplot2)
library(palmerpenguins)

mytheme <- theme(strip.background = element_rect(fill = "steelblue"),
        text = element_text(family = "Comic sans"),
        plot.background = element_rect(fill = "grey81"),
        legend.background = element_rect(fill = NA),
        legend.position = "bottom"
        )

ggplot(penguins, aes(x = body_mass_g, y = bill_length_mm, color = species)) +
  geom_point() + facet_wrap(~ year) + mytheme
```

[figure: plot produced by the code above]

```r
theme_set(theme_bw())
ggplot(penguins, aes(x = body_mass_g, y = bill_length_mm, color = species)) +
  geom_point() + facet_wrap(~ year) + mytheme
```

[figure: plot produced by the code above]

2.  To make a fully custom theme, start with an existing one, and modify it

```r
my_fulltheme <- theme_grey() + mytheme

ggplot(penguins, aes(x = body_mass_g, y = bill_length_mm, color = species)) +
  geom_point() + facet_wrap(~ year) + my_fulltheme
```

[figure: plot produced by the code above]

3.  Save your favorite color scales as a function for easy reuse. Use `discrete_scale` or `continuous_scale`.

```r
my_qual_scale <- function(...) {
  discrete_scale("color", scale_name = "OI",
                 palette = function(x) {
                   res <- palette.colors(x, "Okabe-Ito")[1:x]
                   names(res) <- NULL
                   res
                 }, ...)
}

ggplot(penguins, aes(x = body_mass_g, y = bill_length_mm, color = species)) +
  geom_point() + facet_wrap(~ year) + my_fulltheme + my_qual_scale()
```

[figure: plot produced by the code above]

## Complex figures with base graphics

Check out this violin plot

```r
ggplot(penguins, aes(x = species, y = body_mass_g)) + geom_violin() + geom_jitter()
```

[figure: plot produced by the code above]

How would you produce a similar plot using base graphics? After doing so, reflect, do you appreciate to convenience and flexibility of `ggplot2`?

Use the `density` function to calculate the densities by species. The results are stored in a list with elements `x` and `y`. Then transform by rotating 90 degrees and mirroring. Plot the result using the `polygon` function.

```r
dens_by_species <- split(penguins$body_mass_g, penguins$species) |>
  lapply(density, na.rm = TRUE, cut = 0)

plot(body_mass_g ~ jitter(as.numeric(as.factor(species))),
     data = penguins, xaxt = "n", xlab = "species")

for(i in 1:length(dens_by_species)) {

  den <- dens_by_species[[i]]
  newx <- c(0.2 * (den$y / max(den$y)) + i,
            rev(-0.2 * (den$y / max(den$y)) + i))
  newy <- c(den$x, rev(den$x))

  polygon(newx,  newy)
}
axis(side = 1, at = 1:3, labels = levels(as.factor(penguins$species)))
```

[figure: plot produced by the code above]
