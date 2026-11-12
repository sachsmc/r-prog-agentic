# Install the R packages that the course material uses, if they are missing.
# Run from the repo root:  Rscript build/install_r_packages.R
pkgs <- readLines("build/r-packages.txt")
pkgs <- pkgs[nzchar(pkgs)]
missing <- setdiff(pkgs, rownames(installed.packages()))
if (length(missing) == 0) {
  cat("All", length(pkgs), "course packages are installed.\n")
} else {
  cat("Installing:", paste(missing, collapse = ", "), "\n")
  install.packages(missing, repos = "https://cloud.r-project.org")
  still <- setdiff(missing, rownames(installed.packages()))
  if (length(still) > 0) {
    stop("Could not install: ", paste(still, collapse = ", "))
  }
}
