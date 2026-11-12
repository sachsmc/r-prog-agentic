# Dynamic Documents

Lecture 3 | Day 1, A | Slides: <https://sachsmc.github.io/r-programming/lectures/dynamic-documents.html>

# What?

## Code and prose

A “literate document” or “dynamic document” is a file that contains **code** and **prose**

The idea was developed by Donald Knuth in the 1980s; his motivation was to use it for software development, but allowing programmers to “concentrate … on explaining to humans what we want the computer to do”.

When the document is **rendered** the code also gets run, from top to bottom in the order it appears in the document, and the results inserted dynamically into the output document

## How does it work?

In an rmarkdown (.Rmd) or Quarto (.qmd) document, at the top you have the **yaml header**, with key: value pairs listed inside a start and end fence (“`---`”). These key: value pairs contain information about the document and control how it is rendered.

*Prose* is written in **markdown**. This is a lightweight markup language (headers, bold, italics, links, figures, tables).

*Code* is inserted in between start and end fences (“\`\`\`”), called **chunks**. Options controlling how the code is run and output can be added to each chunk.

## Markdown

```r
---
title: Example yaml header
author: Homer J Simpson
format: html
---

# First level header
## Second level
### etc

*italics* for emphasis, **bold** for highlighting

- Lists
- can
- also
    + be
    + nested

1. Or enumerated
2. B
3. C

![alt text](path-to-image.png)

[text](link.html)

Equations:

$$
T = \frac{\overline{X} - \mu_0}{\hat{\sigma}/\sqrt{n}}
$$
```

## Code chunks

Look like this, and the output is below

````markdown
```{r}
rnorm(1)
```
````

    #> [1] -0.75503

In quarto, chunk options are inside the fence after `#|`, e.g., `#| echo: fenced`, each on their own line

In rmarkdown, chunk options are inside the brackets (this is compatible with quarto for now)

You can also have code *inline*:

```r
For example this `r rnorm(1)` will show up inline
```

which will put the output 2.11958 without showing the code.

## Rendering

- The code chunks will be run sequentially in the same, fresh R session (remember when I said restart R frequently when developing)
- The code and output will be inserted into an intermediate document, as directed by the code chunk options
- That document is then processed by [pandoc](https://pandoc.org) which turns it into a format designed for human readability, as directed by the document yaml header
  - html web pages
  - pdf documents (requires Latex)
  - word documents
  - html presentations (like this one)
  - …

## Presentations

I like to use `format: revealjs`

A new slide starts with a level-1 (#) or -2 (##) heading, followed by a title. Then you can include anything, lists, code, output, etc:

```r
## This is a slide title

Here is the _slide content_

## This starts a new slide

- More
- ... content

# This is a new section
```

## Getting output to look nice

Tools of the trade

- Figures are straightforward, can use captions and cross-references
- For inline output, you can write custom print methods, which we will try later
- Tables are the hardest, there are some packages that help
  - `knitr` and the function `kable`, also the package `kableExtra`
  - `xtable` (designed for pdf output)
  - `gtsummary`

## Customizing rendering

- Bibliographies and cross references fully supported
- With Quarto, layout and style can be controlled with commands inside `:::` fences
- html output: further tweaks with custom CSS
- PDF output: Latex and related commands
- word documents: template files? and some html is supported

## Table example

This function outputs the data in a markdown table, which is then interpreted and rendered nicely when the intermediate document is processed by pandoc

```r
knitr::kable(head(palmerpenguins::penguins))
```

| species | island | bill_length_mm | bill_depth_mm | flipper_length_mm | body_mass_g | sex | year |
|:---|:---|---:|---:|---:|---:|:---|---:|
| Adelie | Torgersen | 39.1 | 18.7 | 181 | 3750 | male | 2007 |
| Adelie | Torgersen | 39.5 | 17.4 | 186 | 3800 | female | 2007 |
| Adelie | Torgersen | 40.3 | 18.0 | 195 | 3250 | female | 2007 |
| Adelie | Torgersen | NA | NA | NA | NA | NA | 2007 |
| Adelie | Torgersen | 36.7 | 19.3 | 193 | 3450 | female | 2007 |
| Adelie | Torgersen | 39.3 | 20.6 | 190 | 3650 | male | 2007 |

## Endless possibilities

- In theory, in your paper/presentation, every number and figure that is a result of your analysis can be generated from code
- Easy to update if the data change
- Can inspect the source document to determine where the number came from
- In practice, do the best you can, and sometimes a well-documented “business process” is just as good
- Content comes first – the default “look” and layout is good enough for most applications, but you can also endless tweak that to suit your need

# How?

- Rmarkdown, works great, been around for a while now
- Quarto, relatively newer. Main advantage is increase flexibility of controlling output (and speed) and more features being introduced
- Sweave, old school format used in R. See the `survival` package vignettes and in particular the “noweb” subdirectory which takes the literate programming approach.
- Org mode, an emacs thing

# More about quarto

- [reference for code cell options](https://quarto.org/docs/reference/cells/cells-knitr.html)
- [reference for format options (html)](https://quarto.org/docs/reference/formats/html.html)

Cell options affect the execution and output of executable code blocks. They are specified within comments at the top of a block. For example:

````markdown
```{r}
#| label: fig-polar
#| echo: false
#| fig-cap: "A line plot on a polar axis"
```
````

# Even more

Defaults can be set globally in the YAML header, e.g.,

```yaml
---
execute:
  echo: true
---
```

- Quarto works well with python, Julia, and observable (javascript)
- You can organize collections of documents into books, websites, etc.

# Try it yourself

## Practical

We will briefly try out rmarkdown or quarto so that you are set up for taking notes and keeping track of your exercise solutions.

[Link to lesson](../exercises/dynamic-documents.html)

[Link home](../index.html)
