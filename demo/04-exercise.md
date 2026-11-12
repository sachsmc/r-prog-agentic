# Demo 4: Help with an exercise

The tutor sets one task and waits. It runs the student's attempt, explains what went wrong, and leaves the fix to the student. When the student asks for a solution, it shows it at once.

*A real exchange with the tutor in this repo, from 12 November 2026. The student is played by a second AI session. The words are unchanged. Headings in the tutor's replies are shown as bold text, and cuts are marked [...].*

---

**Student**

> [...] I would like to try exercise 4 instead.

**Tutor**

[...]

**Exercise 4: Flow control and loops**

The set has four blocks: simple loops, loops for statistics on the penguins data, a numeric calculation, and an optional block. We take one task at a time.

**Task 1** (block "Simple loops and conditional statements")

Use a loop to print every number from 1 to 10.

You need no data and no packages for this one. Later tasks use the `palmerpenguins` package, which is already installed.

Try it and paste your code here, or give me the path to a file. A guess that does not work is welcome too. If you do not know where to begin, say "hint".

---

**Student**

> Here is my try:
>
> for (i in 1:10) {
>   print(1:10)
> }
>
> It prints a lot more than I expected and I do not understand why.

**Tutor**

Good try. You are closer than you think. I ran your code:

```
 [1]  1  2  3  4  5  6  7  8  9 10
 [1]  1  2  3  4  5  6  7  8  9 10
 [1]  1  2  3  4  5  6  7  8  9 10
 ... (10 lines in total, all the same)
```

It does not do what the task asks yet: you get ten lines of ten numbers, instead of ten lines with one number each. But the first line of your loop is exactly right.

**Why it prints so much.** A `for` loop has two pieces:

- `for (i in 1:10)` says: run the body 10 times. In the first round `i` is 1, in the second round `i` is 2, and so on up to 10.
- The body, inside `{ }`, is what runs in each round.

Your body is `print(1:10)`. That prints all ten numbers. The loop runs it 10 times, so you see all ten numbers, ten times over.

**Where to look.** Notice that `i` does not appear anywhere in your body. So every round does the same thing. The lecture has an example where the body does use it (lecture 5, slide "For loops"):

```r
for(i in 1:5) {
  if(i == 2) next
  print(paste("hello", i))
}
```

Change one thing inside your `print()` so that each round prints only the number for that round. Paste your new version when you have it.

---

**Student**

> Oh! I should print i, not 1:10. So it is print(i) inside the loop. For the next task with the even numbers, can you just show me the solution? I want to see how it is done.

**Tutor**

Yes, `print(i)` is it, and you found it yourself. I ran it:

```r
for (i in 1:10) {
  print(i)
}
#> [1] 1
#> [1] 2
#> ...
#> [1] 10
```

This matches the course solution exactly. The key idea you now have: `i` holds a different value in each round, and the body uses it.

**Task 2: the solution**

The task: change the loop so it prints only the *even* numbers from 1 to 10. Here is the solution from the course (exercise 4 solutions, "Simple loops and conditional statements"):

```r
for(i in 1:10){
  if((i %% 2) == 0) {
    print(i)
  }
}
#> [1] 2
#> [1] 4
#> [1] 6
#> [1] 8
#> [1] 10
```

How it works:

- The loop is the same as yours. `i` still goes from 1 to 10.
- The new piece is the `if` around `print(i)`. The number is printed only when the condition is `TRUE`.
- `%%` gives the remainder after division. I ran `7 %% 2`, which gives `1`, and `8 %% 2`, which gives `0`. An even number has remainder 0 when divided by 2.
- So `(i %% 2) == 0` asks: "is `i` even?"

This connects to what you learned today. Inside the loop, `i` is a single number, so the condition is a single `TRUE` or `FALSE`. That is exactly what `if` needs. This is why loops and `if` work so well together.

Trying a task first usually helps more than reading the answer, so here is a small one to make this solution your own: what would you change to print the *odd* numbers instead?

After that, the next task uses real data: a loop that prints the mean of each numeric variable in the `penguins` data. Or we stop here for today. Your choice.
