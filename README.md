# Overview

CaveMark is a typesetting markdown parser.  It is also the fastest pure-Python
markdown parser!  

If you don't know what's a typesetting parser read [this
](https://en.wikipedia.org/wiki/Typesetting).  I don't know any typesetting
markdown parser for Python.  So maybe CaveMark is the only one.  I know about
[Madoko](https://www.madoko.net/), but its syntax sucks and I guess it's not a
python module (JavaScript).  I never used Madoko.

This typesetting aspect makes CaveMark the easiest way to allow you write
pretty documents for your blog/website/whatever. than, say, mistune or any
other conventional markdown parser around.


# Benchmark

Speed is certainly not the main reason I made CaveMark, but I think the speed
benchmark is a nice way to show you how honestly I made CaveMark.  E.g. I
wasn't a lazy sucker that hoped people to just buy faster hard.

Before CaveMark was born, [mistune](https://github.com/lepture/mistune) used to
be the fastest pure-Python markdown parser.  So I am comparing against mistune
in this benchmark.  I tested against other pure-Python markdown parsers, and
they were too slow, so I am not even bothering with the others.

Results with CPython (repeated 3 times):

```
mistune : 13.928859449 seconds
cavemark: 5.57010197 seconds (2.5 times faster!)

mistune : 13.980875624 seconds
cavemark: 5.646393874 seconds (2.5 times faster!)

mistune : 13.941337609 seconds
cavemark: 5.608549864 seconds (2.5 times faster!)
```

Results with PyPy3 (repeated 3 times):

```
mistune : 10.141159687 seconds
cavemark: 1.728199896 seconds (5.9 times faster!)

mistune : 9.768847644000001 seconds
cavemark: 1.7137211739999998 seconds (5.7 times faster!)

mistune : 9.077121615 seconds
cavemark: 1.703783539 seconds (5.3 times faster!)
```

# Syntax

`#` defines section headings.  E.g. `# heading` becomes `<h1>heading</h1>`, `##
heading` becomes ``<h2>heading</h2>`.

`_` emphasizes texts.  E.g.  `_this_` = _this_.

Ordered lists are defined by `+`, and the unordered by `*`.  E.g.:

```
* this item is not orderd.
* another unordered item.
    + this item is nested and is ordered.
    + another ordered item.
```

The most unique bit (syntax-wise) is how resources are defined:

```
image  : myimage
url    : http://cave.mn/pics/cat.png
caption: caveman's cat looks happy
alt    : caveman's cat
```

Aside from `image`, many other resource types are defined, e.g. book, footnote,
quote, theorem, etc.  You can also easily add your own custom ones.

Citing a resource is by using `[]`.  E.g. `[myimage]` will cite the `myimage`
resource we defined earlier.

# Basic Example

```python
text_input = '''
# this is a _heading_

image  : myimage
url    : http://cave.mn/pics/cat.png
caption: caveman's cat
alt    : caveman's cat

footnote: mynote
text    : the cat is 1 yrs old

[myimage] shows a happy cat[mynote].
'''

parser = cavemark.CaveMark()
parser.parse(text_input)
parser.flush()
html_output = parser.get_html()
```

Which will show something neat:

* `[myimage]` automatically expands into _Figure 1_, and is clickable.
* `myimage` figure will be shown after the paragraph it is cited, alongside
  captions, figure index, bookmark, and everything!
* The footnote `mynote` will appear underneath the page, automatically.
* If you cite a book, a bibliography will also apear!


# Todo

  - [ ] Tables.
  - [ ] Add referenceable heading indices.
  - [ ] Documentation.
