# Overview

As you know, we post things online.  Most blogs nowadays kinda support some
variant of markdown.  CaveMark is yet another markdown variant, but very unique
compared to anything out there.  You can read more about it in the 1st column
[here](https://cave.mn).

CaveMark is an efficient, lightweight, markdown variant.  It's differs by the
fact that it is typesetting (e.g. generates LaTeX-like output.  So, you don't
need to worry about figure/quote/theorem/definition/figure indexes), while
maintaing the simple markdown-ish syntax.  

The typesetting aspect, and the simple markdown-ish syntax makes CaveMark the
easiest markdown variant to author documents in.  If you use others, such as
[mistune](https://github.com/lepture/mistune) (which are not typesetting), you
will end up wasting more time writing far larger texts to achieve what CaveMark
does for you automatically.  Of course, CaveMark is also faster than
[mistune](https://github.com/lepture/mistune) with 50% less code lines.

**Note:** this is currently _pre-alpha_.  Some key features missing, and rough
edges.  But soon I will release the feature-complete CaveMark, with final
benchmarks against [mistune](https://github.com/lepture/mistune)!

# Benchmark

CaveMark is the fastest pure-Python markdown-to-HTML parser as shown by my
[early
benchmarks](https://github.com/Al-Caveman/cavemark/blob/master/benchmark/)
where it's noticeably faster than
[mistune](https://github.com/lepture/mistune) (latter used to be the fastest,
no longer now):

Results with Python:

```
cavemark     : 5.032131602000001 seconds
mistune      : 6.584615278999999 seconds
difference   : -1.5524836769999988 seconds
```

Results with PyPy3:

```
cavemark     : 0.9286151840000001 seconds
mistune      : 4.276765432 seconds
difference   : -3.3481502480000005 seconds
```

I will do a final benchmark later on when I finish the to-do tasks (some
features to add).  But, the addition of the missing features is pretty much not
related to speed. So being optimistic that CaveMark would remain the fasted
pure-Python markdown parser, after its features completion, is very high.


# Basic examples
Here is a basic example: of a document written in CaveMark's markdown-variant
syntax:

```markdown
# This is some main heading

## A subheading like usual

This is some paragraph^{this is some footnote}.  The footnote will be
automatically parsed and placed properly.  You don't need to worry about it.

This is another paragraph that cites this resource [myresource].  CaveMark will
cite it properly based on its type.  E.g. if it's a book/paper, it will put it
in a bibliography section, without you doing anything.  If it's an image, it
will show it as a neat image, with caption and all goodies.

CaveMark is stateful, and can generate HTML pages while still maintaing
consistent citation/footnote counts.  It just works.  This gives you the
liberty to also be able to split your large markdown text files into smaller
ones, and feed them one after the other, in order to achieve higher
scalability.
```

Here is an example of how to use CaveMark in your Python project:

```python
text_input = '# this is some _text_ file'
parser = cavemark.CaveMark()
parser.parse(text_input)
parser.flush()
html_output = parser.get_html()
parser.reset(html=True, footnotes=True, bibliography=True)
```

# Features

  - Simple markdown-like syntax for authors.
  - Typesetting (can generate beautiful documents, like LaTex depending on your
    themes, without needing to do the tidious formatting by yourself).
  - As a result, you easily type less to do much more.  On the other hand, if
    you use other markdown variants, such as
    [mistune](https://github.com/lepture/mistune), you (as a user posting
    texts in markdown) will need to write a tedius code to get close to what
    CaveMark does automatically.
  - Also lightweight, efficient and scalable. E.g. you can split large markdown
    files into many smaller chunks, and only load each chunk at once, while
    guaranteeing getting the same outcome as if you loaded the full file at
    once.  This is thanks to CaveMark's stateful design.

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
  - [ ] Full benchmark against [mistune](https://github.com/lepture/mistune)
    and show who is the Big Daddy now ([early
    benchmarks](https://github.com/Al-Caveman/cavemark/blob/master/benchmark/)
    done; CaveMark is faster so far!).
  - [ ] A few rough edges (e.g. how to report user errors when a cited resource
    does not exist).
