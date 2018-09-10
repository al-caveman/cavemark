# Overview
As you know, we post things online.  Most blogs nowadays kinda support some
variant of markdown.  CaveMark is yet another markdown variant, but very unique
compared to anything out there.

CaveMark is an efficient, lightweight, markdown variant that generates
LaTeX-like output, but maintains the simple markdown syntax.  This makes it the
easiest markdown variant to author documents online.

Here is a basic example:

```md
# This is some main heading

## A subheading like usal

This is some paragraph^{this is some footnote}.  The footnote will be
automatically parsed and placed properly.  You don't need to worry about it.

This is another paragraph that cites this resource [myresource].  CaveMark will
cite it properly based on its time.  E.g. if it's a book/paper, it will put it
in a bibliography section, without you doing anything.  If it's an image, it
will show it as a neat image, with caption and all goodies.

You can also split your documents/text files as you want. CaveMark is stateful,
and can generate HTML pages while still maintaing consistent citation/footnote
counts.  It just works.
```

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
  - [x] Footnotes.
  - [x] Automatic placement of floats (e.g. figures) based on your citations.
    These are called box resources.
  - [x] Both inline and block codes.
  - [x] Flexible way to add your custom resource types.
  - [x] Flexible way to customize HTML tags.
  - [x] Flexible way to ignore certain substrings (e.g. if you wish to ignore
    things between `\[...\]` for MathJax.
  - [x] Stateful design, so you can split your text files however you want, and
    CaveMark's will keep track of everything to keep your page consistent.
    E.g. consistent citation indexes, footnotes, no redundant figures, etc.

# Todo (soon)

  - [ ] Nested ordered/unordered lists.
  - [ ] Tables.
  - [ ] Benchmark against `mistune` and show who is the Big Daddy now.
  - [ ] A few rough edges (e.g. how to report user errors when a cited resource
    does not exist).
