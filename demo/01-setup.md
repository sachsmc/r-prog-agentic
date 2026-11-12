# Demo 1: Setup

The student types one word. The tutor checks the computer, installs what is missing, builds the reference books, asks about background, and proposes a plan.

*A real exchange with the tutor in this repo, from 12 November 2026. The student is played by a second AI session. The words are unchanged. Headings in the tutor's replies are shown as bold text, and cuts are marked [...].*

---

**Student**

> start

**Tutor**

Welcome to the course! I am your tutor for "Programming and statistical modelling in R".

I checked your computer. Everything needed is there:

- **R** 4.4.2: I can run code for you.
- **uv**: search over the course material works.
- **ripgrep**: fast text search works.

Two optional setup steps remain:

1. **R packages.** The lectures use some R packages. I can install them with `Rscript build/install_r_packages.R`. This needs internet and may take a few minutes.
2. **Reference books.** I can also search eight R books plus a few papers and cheatsheets. Building them takes one to two minutes, needs internet, and uses about 250 MB of disk. The course works without them, and you can ask for them later.

Tell me which of these you want, and then I will ask a few short questions about your background.

---

**Student**

> Yes, both

**Tutor**

The R packages are ready: all 20 packages the lectures use are installed. The reference books are still building in the background. I will tell you when they are done.

While that runs, three short questions:

1. How much R have you used? (none, a little, regularly)
2. Have you written your own functions or loops before?
3. What do you want from the course? For example: follow the lectures in order, prepare for a certain day, or get help with your own data.

Answer in your own words, in any language you like.

[...]

---

**Student**

> 1. I have used R a little, mostly running scripts my supervisor gave me and changing small things. 2. I have never written my own function. I copied a for loop once but I did not really understand it. 3. I want to follow the lectures, but I am most worried about loops and functions, so I would like to start there.

**Tutor**

Setup is finished, and I have a plan for you.

**Setup**

- All 20 R packages for the lectures are installed.
- The reference books are built: 12 sources, among them *R for Data Science*, *Advanced R*, and *Hands-On Programming with R*. I tested the search and it works.
- One source, `rosthoj-intro`, was skipped because its source file is not available. That is a note for the teacher, not a problem for you.

**Your plan**

Thanks for your answers. Starting with loops and functions is a good choice. Here is what I suggest:

1. **Short warm-up** from lecture 4: vectors, lists, and how to pick out elements with `[ ]` and `[[ ]]`. A loop works through these one element at a time, so loops are much easier once this is clear.
2. **Lecture 5: Flow control and loops**, then exercise 4. We will take the for loop apart piece by piece, so you understand it instead of copying it.
3. **Lecture 6: Functions**, then exercise 5. You will write your first own function here.
4. After that, back to the start: lectures 1 and 3, the rest of 4, then 7 to 10 in order.

I saved your background and this plan in `progress.md`, so we can pick up where we left off next time.

**Things you can type**

- "Teach me lecture 5"
- "Give me exercise 4"
- "Why does `c(1, 'a')` turn the number into text?"
- "Review my code in my-script.R"
- "Show me the solution to exercise 4"

You can also ask any question in your own words, in any language.
