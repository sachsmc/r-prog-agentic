# Fixture for the review skill check. It has problems on purpose.
setwd("C:/Users/me/Documents/project")

library(palmerpenguins)

d <- penguins

x1 <- mean(d$bill_length_mm[d$species == "Adelie"], na.rm = TRUE)
x2 <- mean(d$bill_length_mm[d$species == "Chinstrap"], na.rm = TRUE)
x3 <- mean(d$bill_length_mm[d$species == "Gentoo"], na.rm = TRUE)

s1 <- sd(d$bill_length_mm[d$species == "Adelie"], na.rm = TRUE)
s2 <- sd(d$bill_length_mm[d$species == "Chinstrap"], na.rm = TRUE)
s3 <- sd(d$bill_length_mm[d$species == "Gentoo"], na.rm = TRUE)

res <- c()
for (i in 1:length(d$body_mass_g)) {
  res <- c(res, d$body_mass_g[i] / 1000)
}

print(c(x1, x2, x3))
print(c(s1, s2, s3))
print(mean(res, na.rm = TRUE))
