# Overview
As you know, we post things online.  Most blogs nowadays kinda support some
variant of markdown.  CaveMark is yet another markdown variant, but very unique
compared to anything out there.

CaveMark is an efficient, lightweight, markdown variant that generates
LaTeX-like output, but maintains the simple markdown syntax.  This makes it the
easiest markdown variant to author documents online.

# Features

  - Simple markdown-like syntax for authors.
  - Generates beautiful LaTeX-like HTML for your website.
  - As a result, you easily type less to do much more.  On the other hand, if
    you use other markdown variants, such as `mistune`, you (as a user posting
    texts in markdown) will need to write a tedius code to get close to what
    CaveMark does automatically.
  - It's also lightweight and efficient.  I will soon benchmark it against
    `mistune`, and I think it will be as fast, or faster.

 Currently, the following are supported:

  - [x] Headings.
  - [x] Emphasized texts.
  - [x] Inline citations.
  - [x] Automatic placement of floats (e.g. figures) based on your citations.
    These are called box resources.
  - [x] Both inline and block codes.
  - [x] Flexible way to add your custom resource types.
  - [x] Flexible way to customize HTML tags.
  - [x] Flexible way to ignore certain substrings (e.g. if you wish to ignore
    things between `\[...\]` for MathJax.

# Todo (soon)

  - [ ] Nested ordered/unordered lists.
  - [ ] Tables.
  - [ ] Benchmark against `mistune` and show who is the Big Daddy now.
  - [ ] A few rough edges (e.g. how to report user errors when a cited resource
    does not exist).
